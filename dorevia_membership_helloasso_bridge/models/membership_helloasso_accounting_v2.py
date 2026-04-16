# -*- coding: utf-8 -*-

"""Constatation comptable V2 : pivot → facture client postée → paiement enregistré.

Idempotence : liens conservés sur ``dorevia.helloasso.payment`` ; pas d'appel direct
``membership.membership_line.create`` (l'adhésion suit la facture via l'OCA).
"""

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.fields import Command
from odoo.tools import format_date

from . import membership_helloasso_bridge_user_messages as bu_msg

_logger = logging.getLogger(__name__)


class DoreviaMembershipHelloassoAccountingV2(models.AbstractModel):
    _name = "dorevia.membership.helloasso.accounting.v2"
    _description = "Pont HelloAsso : pivot → facturation + paiement (rail V2)"

    _HELLOASSO_SALE_JOURNAL_CODE = "DVHAS"
    _V2_INVOICE_LINE_SUFFIX = " — HelloAsso"
    _V2_INVOICE_REF_PREFIX = "HelloAsso:"

    _HELLOASSO_METHOD_BUCKETS = ("carte", "virement", "especes", "hors_ligne")
    _HELLOASSO_METHOD_LABELS = {
        "carte": "HelloAsso - Carte",
        "virement": "HelloAsso - Virement",
        "especes": "HelloAsso - Espèces",
        "hors_ligne": "HelloAsso - Hors ligne",
    }
    _HELLOASSO_METHOD_CODES = {
        "carte": "dorha_cart",
        "virement": "dorha_wire",
        "especes": "dorha_cash",
        "hors_ligne": "dorha_off",
    }

    @api.model
    def _get_helloasso_sale_journal(self, company):
        """Journal de ventes dédié (code fixe), créé une seule fois par société."""
        Journal = self.env["account.journal"].sudo()
        domain = Journal._check_company_domain(company) if hasattr(
            Journal, "_check_company_domain"
        ) else [("company_id", "child_of", company.id)]
        existing = Journal.search(
            [*domain, ("code", "=", self._HELLOASSO_SALE_JOURNAL_CODE)],
            limit=1,
        )
        if existing:
            return existing
        template = Journal.search([*domain, ("type", "=", "sale")], limit=1)
        if not template or not template.default_account_id:
            raise UserError(
                _(
                    "Aucun journal de ventes modèle avec compte par défaut pour la société « %s »."
                )
                % (company.display_name,)
            )
        return Journal.create(
            {
                "name": "Dorevia HelloAsso — Adhésions",
                "code": self._HELLOASSO_SALE_JOURNAL_CODE,
                "type": "sale",
                "company_id": company.id,
                "default_account_id": template.default_account_id.id,
            }
        )

    @api.model
    def _default_bank_journal(self, company):
        Journal = self.env["account.journal"].sudo()
        domain = Journal._check_company_domain(company) if hasattr(
            Journal, "_check_company_domain"
        ) else [("company_id", "child_of", company.id)]
        bank = Journal.search([*domain, ("type", "=", "bank")], limit=1)
        if not bank:
            raise UserError(
                _("Aucun journal de banque pour la société « %s ».")
                % (company.display_name,)
            )
        return bank

    @api.model
    def _v2_invoice_line_description(self, payment, membership_product):
        """Libellé ligne facture V2 : campagne ou produit, suffixe HelloAsso sans doublon."""
        payment.ensure_one()
        membership_product.ensure_one()
        campaign = (payment.campaign_name or "").strip()
        base_name = campaign or membership_product.display_name
        if "HelloAsso" in base_name:
            return base_name
        return f"{base_name}{self._V2_INVOICE_LINE_SUFFIX}"

    @api.model
    def _v2_invoice_ref(self, payment):
        """Référence facture V2 : préfixe lisible + ref pivot (recherche / audit)."""
        payment.ensure_one()
        return f"{self._V2_INVOICE_REF_PREFIX}{payment.helloasso_payment_ref}"

    @api.model
    def _v2_get_or_create_utm_record(self, model_xmlid, name, maxlen=128):
        """Trouve ou crée un enregistrement UTM par nom exact (évite les doublons)."""
        name = (name or "").strip()
        if not name:
            return self.env[model_xmlid]
        name = name[:maxlen]
        Model = self.env[model_xmlid].sudo()
        found = Model.search([("name", "=", name)], limit=1)
        if found:
            return found
        return Model.create({"name": name})

    @api.model
    def _v2_invoice_utm_vals(self, payment):
        """Campagne / médium / source pour le bloc Marketing de ``account.move`` (Odoo UTM)."""
        payment.ensure_one()
        ref = payment.helloasso_payment_ref or str(payment.id)
        campaign_label = (payment.campaign_name or "").strip()
        if not campaign_label:
            campaign_label = "HelloAsso (%s)" % (ref,)
        medium_label = (payment.campaign_type or "").strip()
        if not medium_label:
            medium_label = "HelloAsso — Adhésion"
        source = self._v2_get_or_create_utm_record("utm.source", "HelloAsso")
        medium = self._v2_get_or_create_utm_record("utm.medium", medium_label)
        campaign = self._v2_get_or_create_utm_record("utm.campaign", campaign_label, maxlen=256)
        return {
            "campaign_id": campaign.id,
            "medium_id": medium.id,
            "source_id": source.id,
        }

    @api.model
    def _v2_normalize_identity_token(self, value):
        return " ".join(((value or "").strip()).lower().split())

    @api.model
    def _v2_payer_identity_name_variants(self, payment):
        """Variantes de nom complet (prénom / nom) pour rapprocher le pivot d'une fiche Odoo."""
        fn = (payment.payer_firstname or "").strip()
        ln = (payment.payer_lastname or "").strip()
        if not fn and not ln:
            return frozenset()
        if fn and ln:
            return frozenset(
                {
                    self._v2_normalize_identity_token(f"{fn} {ln}"),
                    self._v2_normalize_identity_token(f"{ln} {fn}"),
                }
            )
        return frozenset({self._v2_normalize_identity_token(fn or ln)})

    @api.model
    def _v2_partner_identity_matches_pivot(self, partner, identity_variants):
        if not identity_variants:
            return False
        name_norm = self._v2_normalize_identity_token(partner.name)
        if name_norm in identity_variants:
            return True
        first = getattr(partner, "firstname", None) or ""
        last = getattr(partner, "lastname", None) or ""
        if (first or last) and first.strip() and last.strip():
            combo = self._v2_normalize_identity_token(f"{first} {last}")
            combo_rev = self._v2_normalize_identity_token(f"{last} {first}")
            if combo in identity_variants or combo_rev in identity_variants:
                return True
        return False

    @api.model
    def _v2_default_receivable_account(self, company):
        Account = self.env["account.account"].sudo()
        receivable = Account.search(
            [
                ("company_ids", "in", [company.id]),
                ("account_type", "=", "asset_receivable"),
            ],
            limit=1,
        )
        if not receivable:
            raise UserError(
                _(
                    "Pont V2 — aucun compte comptable client (receivable) pour la société « %s »."
                )
                % company.display_name
            )
        return receivable

    @api.model
    def _v2_find_or_create_partner_for_payment(self, payment):
        """Résout le client : identité (prénom + nom + e-mail) ; crée la fiche si besoin.

        Si prénom et nom sont renseignés sur le pivot : on cherche une fiche avec le même
        e-mail **et** le même couple nom/prénom (tolérance d’ordre). Sinon on **crée** un
        contact, même si l’e-mail existe déjà sur une autre fiche (ex. parent / enfant).

        Si prénom ou nom manque : comportement historique — une seule fiche par e-mail
        (0 = erreur, >1 = ambiguïté).
        """
        payment.ensure_one()
        Partner = self.env["res.partner"].sudo().with_company(payment.company_id).with_context(active_test=False)
        email = (payment.payer_email or "").strip().lower()
        company = payment.company_id
        domain = [
            ("email", "=ilike", email),
            "|",
            ("company_id", "=", False),
            ("company_id", "=", company.id),
        ]
        candidates = Partner.search(domain)
        identity_variants = self._v2_payer_identity_name_variants(payment)
        fn = (payment.payer_firstname or "").strip()
        ln = (payment.payer_lastname or "").strip()

        if fn and ln:
            matches = [
                p
                for p in candidates
                if self._v2_partner_identity_matches_pivot(p, identity_variants)
            ]
            if len(matches) > 1:
                raise UserError(
                    _(
                        "Pont V2 — plusieurs contacts correspondent à l'identité payeur "
                        "(e-mail « %(email)s », prénom / nom). Fusionner les fiches ou corriger le pivot."
                    )
                    % {"email": email}
                )
            if len(matches) == 1:
                return matches[0]
            receivable = self._v2_default_receivable_account(company)
            # OCA partner_firstname (dépendance via dorevia_helloasso_members) : pas de ``name`` ici.
            partner = Partner.create(
                {
                    "is_company": False,
                    "type": "contact",
                    "firstname": fn,
                    "lastname": ln,
                    "email": email,
                    "company_id": company.id,
                    "property_account_receivable_id": receivable.id,
                }
            )
            _logger.info(
                "Pont V2 : contact créé automatiquement « %s » <%s> (société %s, pivot %s).",
                partner.display_name,
                email,
                company.display_name,
                payment.helloasso_payment_ref,
            )
            return partner

        if not candidates:
            raise UserError(
                _(
                    "Pont V2 — aucun contact enregistré pour l'e-mail « %(email)s » "
                    "(société %(company)s). Renseigner prénom et nom payeur sur le pivot pour "
                    "créer la fiche automatiquement, ou créer le contact manuellement."
                )
                % {"email": email, "company": company.display_name}
            )
        if len(candidates) > 1:
            raise UserError(
                _(
                    "Pont V2 — ambiguïté : plusieurs contacts partagent l'e-mail « %(email)s » "
                    "(règle pont). Renseigner prénom et nom payeur sur le pivot pour lever "
                    "l'ambiguïté, ou fusionner les fiches."
                )
                % {"email": email}
            )
        return candidates[0]

    @api.model
    def _classify_helloasso_payment_method(self, payment):
        """§5.3 : classification (tests et enregistrement paiement)."""
        payment.ensure_one()
        raw = f"{payment.payment_method or ''} {payment.payment_method_raw or ''}".lower()
        if not raw.strip():
            _logger.debug(
                "HelloAsso V2 : moyen de paiement vide sur le pivot %s — "
                "utilisation « HelloAsso - Hors ligne » (§5.3).",
                payment.helloasso_payment_ref,
            )
            return "hors_ligne"
        if any(
            k in raw
            for k in (
                "carte",
                "card",
                "cb",
                "visa",
                "master",
                "amex",
            )
        ):
            return "carte"
        if any(
            k in raw
            for k in (
                "virement",
                "transfer",
                "sepa",
                "prélèvement",
                "prelevement",
                "prelev",
            )
        ):
            return "virement"
        if any(k in raw for k in ("espèce", "espece", "cash", "liquide")):
            return "especes"
        _logger.warning(
            "HelloAsso V2 : moyen de paiement non reconnu %r sur le pivot %s — "
            "utilisation « HelloAsso - Hors ligne » (§5.3).",
            raw.strip(),
            payment.helloasso_payment_ref,
        )
        return "hors_ligne"

    @api.model
    def _get_or_create_helloasso_payment_method_line(self, bank_journal, payment):
        """Ligne de méthode de paiement entrante sur le journal banque (idempotent par libellé §5.3)."""
        bucket = self._classify_helloasso_payment_method(payment)
        if bucket not in self._HELLOASSO_METHOD_BUCKETS:
            bucket = "hors_ligne"
        label = self._HELLOASSO_METHOD_LABELS[bucket]
        Line = self.env["account.payment.method.line"].sudo()
        existing = Line.search(
            [
                ("journal_id", "=", bank_journal.id),
                ("name", "=", label),
            ],
            limit=1,
        )
        if existing:
            return existing
        template = bank_journal.inbound_payment_method_line_ids[:1]
        if not template:
            raise UserError(
                _("Le journal « %s » n'a pas de méthode de paiement entrante modèle.")
                % (bank_journal.display_name,)
            )
        code = self._HELLOASSO_METHOD_CODES[bucket]
        Method = self.env["account.payment.method"].sudo()
        method = Method.search(
            [("code", "=", code), ("payment_type", "=", "inbound")], limit=1
        )
        if not method:
            method = Method.create(
                {
                    "name": label,
                    "code": code,
                    "payment_type": "inbound",
                }
            )
        return Line.create(
            {
                "journal_id": bank_journal.id,
                "payment_method_id": method.id,
                "name": label,
                "payment_account_id": template.payment_account_id.id,
                "sequence": 90 + self._HELLOASSO_METHOD_BUCKETS.index(bucket),
            }
        )

    @api.model
    def _register_payment_on_invoice(
        self, move, bank_journal, payment_date, amount, pivot_payment=None
    ):
        if pivot_payment is not None:
            method_line = self._get_or_create_helloasso_payment_method_line(
                bank_journal, pivot_payment
            )
        else:
            lines = bank_journal.inbound_payment_method_line_ids
            if not lines:
                raise UserError(
                    _("Le journal « %s » n'a pas de méthode de paiement entrante.")
                    % (bank_journal.display_name,)
                )
            method_line = lines[0]
        wizard = (
            self.env["account.payment.register"]
            .with_context(active_model="account.move", active_ids=move.ids)
            .create(
                {
                    "journal_id": bank_journal.id,
                    "payment_date": payment_date,
                    "amount": amount,
                    "payment_method_line_id": method_line.id,
                }
            )
        )
        return wizard._create_payments()

    def _resolve_partner_amount_dates(self, payment, membership_product):
        """Résout le partenaire (identité prénom+nom+e-mail ou repli e-mail seul) + montant / dates."""
        payment.ensure_one()
        membership_product.ensure_one()

        if not payment.active:
            raise UserError(
                bu_msg.payment_archived_v2(
                    payment.helloasso_payment_ref or str(payment.id)
                )
            )

        if not membership_product.membership:
            raise UserError(
                bu_msg.product_not_membership(membership_product.display_name)
            )
        if membership_product.type != "service":
            raise UserError(bu_msg.product_must_be_service())

        email = (payment.payer_email or "").strip().lower()
        if not email:
            raise UserError(bu_msg.payment_missing_payer_email())

        partner = self._v2_find_or_create_partner_for_payment(payment)

        if not partner.active:
            raise UserError(
                bu_msg.partner_archived_v2(
                    partner.display_name,
                    payment.helloasso_payment_ref or str(payment.id),
                )
            )

        if (
            membership_product.company_id
            and membership_product.company_id != payment.company_id
        ):
            raise UserError(
                bu_msg.membership_product_company_mismatch(
                    membership_product.company_id.display_name,
                    payment.company_id.display_name,
                )
            )
        if partner.company_id and partner.company_id != payment.company_id:
            raise UserError(
                bu_msg.partner_company_mismatch(
                    partner.display_name, payment.company_id.display_name
                )
            )

        pay_date = fields.Date.today()
        if payment.payment_date:
            pay_date = fields.Datetime.to_datetime(payment.payment_date).date()

        date_from = membership_product.membership_date_from
        date_to = membership_product.membership_date_to
        if not date_from or not date_to:
            raise UserError(
                bu_msg.membership_product_dates_required(
                    membership_product.display_name
                )
            )
        if pay_date < date_from or pay_date > date_to:
            raise UserError(
                bu_msg.payment_date_outside_product_window(
                    self.env,
                    pay_date,
                    membership_product.display_name,
                    date_from,
                    date_to,
                )
            )

        amount = payment.amount_tariff or payment.amount_total
        if amount in (False, None) or amount == 0:
            amount = membership_product.list_price

        if payment.currency_id != payment.company_id.currency_id:
            raise UserError(
                _("Le rail V2 ne gère pas encore les devises autres que celle de la société.")
            )

        return {
            "partner": partner,
            "pay_date": pay_date,
            "amount": float(amount),
        }

    def _assert_rail_v2(self, payment):
        payment.ensure_one()
        account = payment.helloasso_account_id
        if not account:
            raise UserError(_("Pont V2 — pivot sans compte HelloAsso."))
        rail = account.membership_pont_rail or "v1_line"
        if rail != "v2_accounting":
            raise UserError(
                _(
                    "Pont V2 — le compte HelloAsso « %(acc)s » n'est pas en rail "
                    "constatation comptable (rail actuel : %(rail)s)."
                )
                % {"acc": account.display_name, "rail": rail}
            )

    @api.model
    def _pivot_v2_write_isolated(self, payment, vals):
        """Écriture pivot V2 + commit sur curseur dédié (visible après UserError / abort transaction)."""
        if not vals:
            return
        payment.ensure_one()
        pid = payment.id
        registry = payment.env.registry
        uid = payment.env.uid
        ctx = dict(payment.env.context or {})
        ctx["membership_bridge_skip_hook"] = True
        with registry.cursor() as cr:
            env2 = api.Environment(cr, uid, ctx)
            pay2 = env2["dorevia.helloasso.payment"].browse(pid).sudo()
            if pay2.exists():
                pay2.write(vals)
                cr.commit()
                return
        # Pivot pas encore visible hors transaction courante (ex. tests sans commit) :
        # même env — ne survit pas à un abort RPC, mais couvre les TransactionCase.
        payment.invalidate_recordset(list(vals))
        payment.with_context(membership_bridge_skip_hook=True).sudo().write(vals)

    @api.model
    def _rollback_v2_accounting(self, payment, move, account_payment):
        """F2-4 : annule encaissement puis facture. Pas d'unlink facture annulée (audit).

        Si ``button_cancel`` échoue (journal verrouillé, période clôturée…), on conserve
        ``membership_v2_out_invoice_id`` pour traçabilité / retry — pas d'unlink agressif.
        """
        payment = payment.sudo()
        move = move and move.sudo()
        account_payment = account_payment and account_payment.sudo()
        ret = {"invoice_cancel_failed": False, "draft_unlink_failed": False}

        self._pivot_v2_write_isolated(
            payment, {"membership_v2_account_payment_id": False}
        )
        if account_payment and account_payment.exists():
            try:
                account_payment.action_cancel()
            except Exception as err:
                _logger.warning(
                    "Pont V2 F2-4 rollback : action_cancel paiement id=%s (%s)",
                    account_payment.id,
                    err,
                )
            try:
                account_payment.unlink()
            except Exception as err:
                _logger.warning(
                    "Pont V2 F2-4 rollback : unlink paiement id=%s (%s)",
                    account_payment.id,
                    err,
                )

        if not move or not move.exists():
            self._pivot_v2_write_isolated(
                payment, {"membership_v2_out_invoice_id": False}
            )
            return ret

        if move.state == "draft":
            try:
                move.unlink()
            except Exception as err:
                _logger.warning(
                    "Pont V2 F2-4 rollback : unlink brouillon id=%s (%s)",
                    move.id,
                    err,
                )
                ret["draft_unlink_failed"] = True
                self._pivot_v2_write_isolated(
                    payment, {"membership_v2_out_invoice_id": move.id}
                )
                return ret
            self._pivot_v2_write_isolated(
                payment, {"membership_v2_out_invoice_id": False}
            )
            return ret

        if move.state == "posted":
            try:
                move.button_cancel()
            except Exception as err:
                _logger.warning(
                    "Pont V2 F2-4 rollback : button_cancel facture id=%s (%s)",
                    move.id,
                    err,
                )
                ret["invoice_cancel_failed"] = True
                self._pivot_v2_write_isolated(
                    payment, {"membership_v2_out_invoice_id": move.id}
                )
                return ret

        if move.exists() and move.state == "cancel":
            self._pivot_v2_write_isolated(
                payment, {"membership_v2_out_invoice_id": False}
            )
            return ret

        if move.exists() and move.state == "posted":
            ret["invoice_cancel_failed"] = True
            self._pivot_v2_write_isolated(
                payment, {"membership_v2_out_invoice_id": move.id}
            )
            return ret

        self._pivot_v2_write_isolated(payment, {"membership_v2_out_invoice_id": False})
        return ret

    @api.model
    def _v2_error_message_for_rollback(self, exc, rollback_info):
        parts = [str(exc)] if exc else []
        if rollback_info.get("invoice_cancel_failed"):
            parts.append(
                _(
                    "Annulation de la facture impossible (verrouillage, période clôturée, etc.). "
                    "La facture reste liée au pivot pour traitement manuel ou nouvel essai."
                )
            )
        if rollback_info.get("draft_unlink_failed"):
            parts.append(
                _(
                    "Suppression du brouillon de facture impossible ; la facture reste liée au pivot."
                )
            )
        return "\n".join(p for p in parts if p).strip() or False

    @api.model
    def process_payment(self, payment, membership_product):
        """Facture + paiement, ou no-op strict si déjà soldé (F2-4 : rollback + état pivot)."""
        payment.ensure_one()
        membership_product.ensure_one()
        self._assert_rail_v2(payment)

        if payment.membership_v2_out_invoice_id:
            move = payment.membership_v2_out_invoice_id.sudo()
            if move.state == "cancel":
                raise UserError(
                    _("La facture V2 liée au pivot est annulée ; traitement manuel requis.")
                )
            if move.state == "draft":
                bank_journal_draft = self._default_bank_journal(move.company_id)
                method_line_draft = self._get_or_create_helloasso_payment_method_line(
                    bank_journal_draft, payment
                )
                if method_line_draft:
                    move.write(
                        {"preferred_payment_method_line_id": method_line_draft.id}
                    )
                move.action_post()
            if move.state == "posted":
                if move.payment_state in ("paid", "in_payment"):
                    payment.with_context(membership_bridge_skip_hook=True).write(
                        {
                            "membership_v2_processing_state": "noop",
                            "membership_v2_error_message": False,
                        }
                    )
                    return {
                        "state": "noop",
                        "move": move,
                        "payment": payment.membership_v2_account_payment_id,
                        "message": _(
                            "Déjà traité : facture soldée pour ce pivot (idempotence V2)."
                        ),
                    }
                company = payment.company_id
                bank_journal = self._default_bank_journal(company)
                pay_date = fields.Date.today()
                if payment.payment_date:
                    pay_date = fields.Datetime.to_datetime(payment.payment_date).date()
                account_payment = self.env["account.payment"]
                try:
                    payments = self._register_payment_on_invoice(
                        move,
                        bank_journal,
                        pay_date,
                        abs(move.amount_residual),
                        pivot_payment=payment,
                    )
                    account_payment = payments[:1] if payments else self.env["account.payment"]
                    payment.with_context(membership_bridge_skip_hook=True).write(
                        {
                            "membership_v2_account_payment_id": account_payment.id
                            if account_payment
                            else False,
                            "membership_v2_processing_state": "processed",
                            "membership_v2_error_message": False,
                        }
                    )
                except Exception as exc:
                    rb = self._rollback_v2_accounting(payment, move, account_payment)
                    msg = self._v2_error_message_for_rollback(exc, rb)
                    self._pivot_v2_write_isolated(
                        payment,
                        {
                            "membership_v2_processing_state": "error",
                            "membership_v2_error_message": msg,
                        },
                    )
                    _logger.exception(
                        "Pont V2 F2-4 : échec enregistrement paiement (pivot %s, facture %s)",
                        payment.helloasso_payment_ref,
                        move.id,
                    )
                    raise
                return {
                    "state": "completed",
                    "move": move,
                    "payment": account_payment,
                    "message": _("Paiement complété sur la facture V2 existante."),
                }

        try:
            data = self._resolve_partner_amount_dates(payment, membership_product)
        except UserError as exc:
            self._pivot_v2_write_isolated(
                payment,
                {
                    "membership_v2_processing_state": "error",
                    "membership_v2_error_message": str(exc),
                },
            )
            raise

        partner = data["partner"]
        pay_date = data["pay_date"]
        amount = data["amount"]

        company = payment.company_id
        sale_journal = self._get_helloasso_sale_journal(company)
        bank_journal = self._default_bank_journal(company)

        Move = self.env["account.move"].sudo()
        move = Move.browse()
        account_payment = self.env["account.payment"]
        payment.with_context(membership_bridge_skip_hook=True).write(
            {
                "membership_v2_processing_state": "to_process",
                "membership_v2_error_message": False,
            }
        )
        try:
            move_vals = {
                "move_type": "out_invoice",
                "partner_id": partner.id,
                "company_id": company.id,
                "journal_id": sale_journal.id,
                "invoice_date": pay_date,
                "date": pay_date,
                "ref": self._v2_invoice_ref(payment),
                "invoice_line_ids": [
                    Command.create(
                        {
                            "product_id": membership_product.id,
                            "quantity": 1.0,
                            "price_unit": amount,
                            "name": self._v2_invoice_line_description(
                                payment, membership_product
                            ),
                        }
                    )
                ],
            }
            move_vals.update(self._v2_invoice_utm_vals(payment))
            move = Move.create(move_vals)
            method_line = self._get_or_create_helloasso_payment_method_line(
                bank_journal, payment
            )
            if method_line:
                move.write({"preferred_payment_method_line_id": method_line.id})
            move.action_post()
            if method_line and not move.preferred_payment_method_line_id:
                move.write({"preferred_payment_method_line_id": method_line.id})

            payments = self._register_payment_on_invoice(
                move,
                bank_journal,
                pay_date,
                abs(move.amount_residual),
                pivot_payment=payment,
            )
            account_payment = payments[:1] if payments else self.env["account.payment"]

            payment.with_context(membership_bridge_skip_hook=True).write(
                {
                    "membership_v2_out_invoice_id": move.id,
                    "membership_v2_account_payment_id": account_payment.id
                    if account_payment
                    else False,
                    "membership_v2_processing_state": "processed",
                    "membership_v2_error_message": False,
                }
            )
        except Exception as exc:
            rb = self._rollback_v2_accounting(payment, move, account_payment)
            msg = self._v2_error_message_for_rollback(exc, rb)
            self._pivot_v2_write_isolated(
                payment,
                {
                    "membership_v2_processing_state": "error",
                    "membership_v2_error_message": msg,
                },
            )
            _logger.exception(
                "Pont V2 F2-4 : constatation interrompue (pivot %s)",
                payment.helloasso_payment_ref,
            )
            raise

        return {
            "state": "created",
            "move": move,
            "payment": account_payment,
            "message": _("Facture postée et paiement enregistré."),
        }
