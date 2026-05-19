# -*- coding: utf-8 -*-
"""Dédoublonnage données — origine La Réunion / Reunion (TICKET_MARKETONE_ORIGINE_REUNION_DEDUP)."""

import logging
import unicodedata

_logger = logging.getLogger(__name__)

CANONICAL_REUNION_LABEL = "La Réunion"
REUNION_SLUG = "reunion"


def _normalize_origin_label(name):
    """Normalise pour comparer libellés (sans accents, casse)."""
    if not name:
        return ""
    text = unicodedata.normalize("NFD", str(name))
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return " ".join(text.lower().split())


def _is_reunion_duplicate_label(name):
    return _normalize_origin_label(name) in {"reunion", "la reunion"}


def marketone_dedup_reunion_origin_values(env):
    """Fusionne les valeurs d'attribut Origines en doublon pour La Réunion / Reunion.

    Idempotent : sans effet si une seule valeur normalisée « reunion » existe déjà.
    """
    attr = env.ref(
        "dorevia_ckreyol_marketone.marketone_product_attribute_origin",
        raise_if_not_found=False,
    )
    if not attr:
        return

    Value = env["product.attribute.value"].sudo()
    reunion_values = Value.search([("attribute_id", "=", attr.id)]).filtered(
        lambda v: _is_reunion_duplicate_label(v.name)
    )
    if not reunion_values:
        return

    canonical = reunion_values.filtered(
        lambda v: (v.name or "").strip() == CANONICAL_REUNION_LABEL
    )[:1]
    if not canonical:
        canonical = reunion_values.sorted(key=lambda v: v.id)[:1]
    canonical = canonical[0]

    if canonical.name != CANONICAL_REUNION_LABEL:
        canonical.name = CANONICAL_REUNION_LABEL

    duplicates = reunion_values - canonical
    for duplicate in duplicates:
        _merge_origin_attribute_value(env, duplicate, canonical)

    _align_reunion_shop_origin_profiles(env, canonical)


def _merge_origin_attribute_value(env, source, target):
    """Réaffecte les produits de ``source`` vers ``target`` puis supprime ``source``."""
    if source == target or not source.exists():
        return

    Ptav = env["product.template.attribute.value"].sudo()
    templates = Ptav.search(
        [("product_attribute_value_id", "=", source.id)]
    ).mapped("product_tmpl_id")

    for tmpl in templates:
        for line in tmpl.attribute_line_ids.filtered(
            lambda ln: ln.attribute_id == source.attribute_id
        ):
            cmds = []
            if source in line.value_ids:
                cmds.append((3, source.id))
            if target not in line.value_ids:
                cmds.append((4, target.id))
            if cmds:
                line.write({"value_ids": cmds})

    leftover = Ptav.search([("product_attribute_value_id", "=", source.id)])
    if leftover:
        leftover.unlink()

    profiles = env["marketone.shop.origin"].sudo().search(
        [("attribute_value_id", "=", source.id)]
    )
    if profiles:
        profiles.write({"attribute_value_id": target.id})

    _logger.info(
        "Marketone: fusion origine %s (id=%s) → %s (id=%s)",
        source.name,
        source.id,
        target.name,
        target.id,
    )
    source.unlink()


def _align_reunion_shop_origin_profiles(env, canonical_value):
    """Profil porte ``reunion`` → valeur canonique + libellé visiteur."""
    Origin = env["marketone.shop.origin"].sudo()
    profiles = Origin.search([("slug", "=", REUNION_SLUG)])
    if not profiles:
        return
    profiles.write(
        {
            "attribute_value_id": canonical_value.id,
            "name_visitor": CANONICAL_REUNION_LABEL,
        }
    )
