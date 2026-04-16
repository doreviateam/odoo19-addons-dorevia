# -*- coding: utf-8 -*-

import csv
import logging
import random
import time
from io import StringIO

from psycopg2 import OperationalError, errorcodes
from psycopg2.errors import DeadlockDetected, LockNotAvailable, SerializationFailure

from odoo import _
from odoo.tools import config

from odoo.addons.dorevia_helloasso_connector.models.helloasso_client import (
    HelloAssoClientError,
    HelloAssoConnectionContext,
    fetch_client_credentials_token,
    fetch_form_payments_page,
)

from .helloasso_payment_mapper import map_api_payment_row, map_csv_payment_row

_logger = logging.getLogger(__name__)

_PG_CONCURRENCY_EXCEPTIONS_TO_RETRY = (
    LockNotAvailable,
    SerializationFailure,
    DeadlockDetected,
)
_MAX_TRIES_PG_SAVEPOINT = 6

# Verrou advisory transactionnel (libéré au commit) : sérialise les imports pivot sur un même compte HelloAsso.
_ADVISORY_LOCK_HELLOASSO_PAYMENT_NS = 0x484150  # « HAP » — évite les collisions inter-modules (2e clé = id compte).

_PG_CONCURRENCY_PGCODES = frozenset(
    {
        errorcodes.SERIALIZATION_FAILURE,
        errorcodes.DEADLOCK_DETECTED,
        errorcodes.LOCK_NOT_AVAILABLE,
    }
)


def _is_pg_concurrency_error(exc):
    if isinstance(exc, _PG_CONCURRENCY_EXCEPTIONS_TO_RETRY):
        return True
    if isinstance(exc, OperationalError):
        return getattr(exc, "pgcode", None) in _PG_CONCURRENCY_PGCODES
    return False


def _pg_advisory_xact_lock_helloasso_account_import(env, helloasso_account_id):
    """Bloque les autres transactions qui importent aussi sur ce compte (wizard, cron, etc.)."""
    k2 = int(helloasso_account_id) & 0x7FFFFFFF
    env.cr.execute(
        "SELECT pg_advisory_xact_lock(%s, %s)",
        (_ADVISORY_LOCK_HELLOASSO_PAYMENT_NS, k2),
    )


def _helloasso_payment_ref_id_map_sql(env, account_id, refs):
    """Lit id + ``helloasso_payment_ref`` en SQL (évite ``search`` ORM et les flush associés)."""
    uniq = [r for r in dict.fromkeys(refs) if r]
    if not uniq:
        return {}
    table = env["dorevia.helloasso.payment"]._table
    cr = env.cr
    out = {}
    chunk_size = 1000
    for i in range(0, len(uniq), chunk_size):
        chunk = list(uniq[i : i + chunk_size])
        placeholders = ", ".join(["%s"] * len(chunk))
        cr.execute(
            f'SELECT id, helloasso_payment_ref FROM "{table}" '
            f"WHERE helloasso_account_id = %s AND helloasso_payment_ref IN ({placeholders})",
            [account_id, *chunk],
        )
        for row_id, ref in cr.fetchall():
            out[ref] = row_id
    return out


def _helloasso_payment_ref_id_map_prefetch(env, account_id, refs):
    """Précharge ref→id avec savepoint sans flush préalable (réduit SerializationFailure sur prefetch)."""

    def _read():
        return _helloasso_payment_ref_id_map_sql(env, account_id, refs)

    return _savepoint_retry_pg(env, _read)


def _commit_pivot_phase_then_relock_for_bridge(env, helloasso_account_id):
    """Isole la phase pivot (commit) de la phase pont / V2 pour limiter les SerializationFailure.

    Le ``commit`` libère le verrou advisory transactionnel : on le reprend aussitôt pour que la
    phase pont reste sérialisée avec les autres imports sur le même compte HelloAsso.

    Désactivé si ``--test-enable`` : un commit intermédiaire casserait le rollback des tests.
    """
    if config.get("test_enable"):
        return
    env.flush_all()
    env.registry.signal_changes()
    env.cr.commit()
    _pg_advisory_xact_lock_helloasso_account_import(env, helloasso_account_id)


def _savepoint_retry_pg(env, func, flush_savepoint=False):
    """Exécute ``func()`` dans un savepoint ; rollback partiel + backoff si contention PostgreSQL.

    Par défaut ``flush_savepoint=False`` : évite le flush ORM automatique avant ``SAVEPOINT``, source
    fréquente de ``SerializationFailure`` (search/write concurrents dans la même requête).
    Passer ``flush_savepoint=True`` seulement si un cas métier exige explicitement le flush préalable.
    """
    for attempt in range(1, _MAX_TRIES_PG_SAVEPOINT + 1):
        tryleft = _MAX_TRIES_PG_SAVEPOINT - attempt
        try:
            with env.cr.savepoint(flush=flush_savepoint):
                return func()
        except Exception as exc:
            if not _is_pg_concurrency_error(exc):
                raise
            if getattr(env.cr, "_closed", False) or not tryleft:
                _logger.info(
                    "%s, maximum savepoint retries reached for HelloAsso payment row/bridge.",
                    exc.__class__.__name__,
                )
                raise
            wait_time = random.uniform(0.0, 0.2 * (2 ** (attempt - 1)))
            _logger.info(
                "%s, %s savepoint tries left, backoff %.04fs (HelloAsso payment)",
                exc.__class__.__name__,
                tryleft,
                wait_time,
            )
            time.sleep(wait_time)


def _run_membership_bridge_after_bulk_persist(env, payment_ids):
    """Rejoue le pont membership (hors contexte import massif) si le module bridge est chargé."""
    ids = [i for i in dict.fromkeys(payment_ids) if i]
    if not ids:
        return
    Payment = env["dorevia.helloasso.payment"]
    # Ne pas ``browse`` ici : un flush hors savepoint peut déclencher SerializationFailure.
    if not hasattr(Payment, "_membership_bridge_after_persist"):
        return
    for pid in ids:

        def _bridge_one(payment_id=pid):
            rec = env["dorevia.helloasso.payment"].browse(payment_id)
            rec.with_context(membership_bridge_skip_hook=False)._membership_bridge_after_persist()

        _savepoint_retry_pg(env, _bridge_one)


def preview_csv_payment_rows(env, helloasso_account, rows, import_platform_only=True):
    """Analyse les lignes CSV comme ``import_csv_payment_rows`` sans créer ni mettre à jour de pivot.

    Chaque élément retourné décrit une ligne du fichier (numérotation 1-based).
    """
    Payment = env["dorevia.helloasso.payment"]
    out = []
    for row_index, row in enumerate(rows or [], start=1):
        entry = {"row": row_index}
        try:
            vals = map_csv_payment_row(row, helloasso_account)
        except ValueError as err:
            entry["outcome"] = "error"
            entry["message"] = str(err)
            out.append(entry)
            continue

        ref = vals["helloasso_payment_ref"]
        entry["ref"] = ref
        entry["email"] = vals.get("payer_email") or ""
        entry["campaign_type"] = vals.get("campaign_type") or ""
        entry["payment_date"] = vals.get("payment_date")
        entry["is_platform_payment"] = bool(vals.get("is_platform_payment"))

        if import_platform_only and not vals.get("is_platform_payment"):
            entry["outcome"] = "skip_mvp"
            out.append(entry)
            continue

        existing = Payment.search(
            [
                ("helloasso_account_id", "=", helloasso_account.id),
                ("helloasso_payment_ref", "=", ref),
            ],
            limit=1,
        )
        entry["outcome"] = "update" if existing else "create"
        out.append(entry)
    return out


def import_csv_payment_rows(env, helloasso_account, rows, import_platform_only=True):
    account_id = helloasso_account.id
    _pg_advisory_xact_lock_helloasso_account_import(env, account_id)
    # Pendant la boucle : pas de pont membership (factures / partenaires) pour limiter les
    # flush concurrents ; rejouage en fin de lot sur les pivots touchés.
    env_skip = env(context=dict(env.context, membership_bridge_skip_hook=True))
    Payment = env_skip["dorevia.helloasso.payment"]
    account = helloasso_account.with_env(env_skip)
    stats = {
        "processed": 0,
        "created": 0,
        "updated": 0,
        "skipped": 0,
        "skip_offline": 0,
        "errors": [],
    }
    to_import_vals = []
    for row in rows:
        stats["processed"] += 1
        try:
            vals = map_csv_payment_row(row, account)
        except ValueError as err:
            stats["skipped"] += 1
            stats["errors"].append(str(err))
            continue

        if import_platform_only and not vals.get("is_platform_payment"):
            stats["skipped"] += 1
            stats["skip_offline"] += 1
            continue

        to_import_vals.append(vals)

    ref_to_id = _helloasso_payment_ref_id_map_prefetch(
        env_skip,
        account_id,
        [v["helloasso_payment_ref"] for v in to_import_vals],
    )

    affected_ids = []
    for vals in to_import_vals:
        ref_key = vals["helloasso_payment_ref"]

        def _persist_row(v=vals, rk=ref_key, m=ref_to_id):
            eid = m.get(rk)
            if eid:
                Payment.browse(eid).write(v)
                return "updated", eid
            created = Payment.create(v)
            return "created", created.id

        outcome, pivot_id = _savepoint_retry_pg(env_skip, _persist_row)
        if outcome == "created":
            ref_to_id[ref_key] = pivot_id
        if outcome == "updated":
            stats["updated"] += 1
        else:
            stats["created"] += 1
        affected_ids.append(pivot_id)

    if affected_ids:
        _commit_pivot_phase_then_relock_for_bridge(env, account_id)
    _run_membership_bridge_after_bulk_persist(env, affected_ids)
    return stats


def import_api_payment_rows(env, helloasso_account, payments, import_platform_only=True):
    account_id = helloasso_account.id
    _pg_advisory_xact_lock_helloasso_account_import(env, account_id)
    env_skip = env(context=dict(env.context, membership_bridge_skip_hook=True))
    Payment = env_skip["dorevia.helloasso.payment"]
    account = helloasso_account.with_env(env_skip)
    stats = {
        "processed": 0,
        "created": 0,
        "updated": 0,
        "skipped": 0,
        "skip_offline": 0,
        "errors": [],
    }
    to_import_vals = []
    for payment in payments or []:
        stats["processed"] += 1
        try:
            vals = map_api_payment_row(payment, account)
        except ValueError as err:
            stats["skipped"] += 1
            stats["errors"].append(str(err))
            continue

        if import_platform_only and not vals.get("is_platform_payment"):
            stats["skipped"] += 1
            stats["skip_offline"] += 1
            continue

        to_import_vals.append(vals)

    ref_to_id = _helloasso_payment_ref_id_map_prefetch(
        env_skip,
        account_id,
        [v["helloasso_payment_ref"] for v in to_import_vals],
    )

    affected_ids = []
    for vals in to_import_vals:
        ref_key = vals["helloasso_payment_ref"]

        def _persist_row(v=vals, rk=ref_key, m=ref_to_id):
            eid = m.get(rk)
            if eid:
                Payment.browse(eid).write(v)
                return "updated", eid
            created = Payment.create(v)
            return "created", created.id

        outcome, pivot_id = _savepoint_retry_pg(env_skip, _persist_row)
        if outcome == "created":
            ref_to_id[ref_key] = pivot_id
        if outcome == "updated":
            stats["updated"] += 1
        else:
            stats["created"] += 1
        affected_ids.append(pivot_id)

    if affected_ids:
        _commit_pivot_phase_then_relock_for_bridge(env, account_id)
    _run_membership_bridge_after_bulk_persist(env, affected_ids)
    return stats


def import_api_payments_for_account(
    env,
    helloasso_account,
    form_type,
    form_slug,
    import_platform_only=True,
    page_size=50,
    max_pages=20,
):
    stats = {
        "processed": 0,
        "created": 0,
        "updated": 0,
        "skipped": 0,
        "skip_offline": 0,
        "errors": [],
        "pages": 0,
    }
    params = helloasso_account._to_connection_params()
    connection_ctx = HelloAssoConnectionContext.from_primitives(
        params.get("client_id"),
        params.get("client_secret"),
        params.get("use_sandbox"),
        params.get("organization_slug"),
    )
    if not connection_ctx.organization_slug:
        raise HelloAssoClientError(_("Slug organisation HelloAsso manquant."))

    token_payload = fetch_client_credentials_token(connection_ctx)
    token = token_payload["access_token"]

    for page_index in range(1, max_pages + 1):
        items, _total, _raw = fetch_form_payments_page(
            connection_ctx,
            form_type,
            form_slug,
            token,
            page_index=page_index,
            page_size=page_size,
        )
        if not items:
            break
        page_stats = import_api_payment_rows(
            env,
            helloasso_account,
            items,
            import_platform_only=import_platform_only,
        )
        stats["pages"] += 1
        stats["processed"] += page_stats["processed"]
        stats["created"] += page_stats["created"]
        stats["updated"] += page_stats["updated"]
        stats["skipped"] += page_stats["skipped"]
        stats["skip_offline"] += page_stats["skip_offline"]
        stats["errors"].extend(page_stats["errors"])
        if len(items) < page_size:
            break
    return stats


def import_csv_payment_rows_message(stats):
    parts = [
        _("Traitées : %s") % stats.get("processed", 0),
        _("Créées : %s") % stats.get("created", 0),
        _("Mises à jour : %s") % stats.get("updated", 0),
        _("Ignorées : %s") % stats.get("skipped", 0),
    ]
    if stats.get("skip_offline"):
        parts.append(_("Ignorées hors ligne : %s") % stats["skip_offline"])
    if stats.get("errors"):
        parts.append(_("Erreurs : %s") % len(stats["errors"]))
    return " | ".join(parts)


def _strip_csv_row_keys(row):
    """HelloAsso / Excel peuvent ajouter des espaces en tête de colonnes ; les clés doivent matcher le mapper."""
    if not row:
        return row
    return {((k or "").strip()): v for k, v in row.items()}


def parse_payment_csv_content(csv_text):
    """Parse un export paiements HelloAsso (séparateur ``;`` par défaut FR).

    Si le fichier a été réenregistré sous Excel avec des virgules comme séparateur
    de champs, un ``DictReader`` en ``;`` ne voit aucune colonne nommée correctement
    d’où « Référence paiement manquante ». On essaie ``;`` puis ``,``.
    """
    text = (csv_text or "").strip()
    if not text:
        return []
    semicolon_rows = []
    for delimiter in (";", ","):
        reader = csv.DictReader(StringIO(text), delimiter=delimiter)
        fieldnames = reader.fieldnames or []
        header_keys = {(name or "").strip() for name in fieldnames if name}
        rows = [_strip_csv_row_keys(r) for r in reader]
        if "Référence paiement" in header_keys:
            return rows
        if delimiter == ";":
            semicolon_rows = rows
    return semicolon_rows
