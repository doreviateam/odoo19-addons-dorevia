# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

# Champs du pivot dont un changement peut influencer le pont (import massif : évite write anodins).
_MEMBERSHIP_BRIDGE_PAYMENT_WRITE_TRIGGER_FIELDS = frozenset(
    {
        "helloasso_account_id",
        "company_id",
        "helloasso_payment_ref",
        "payer_email",
        "payer_firstname",
        "payer_lastname",
        "payment_date",
        "amount_tariff",
        "amount_total",
        "campaign_type",
        "campaign_name",
        "payment_kind",
        "payment_status",
        "payment_status_raw",
        "currency_id",
        "is_platform_payment",
        "is_offline_payment",
    }
)


def _membership_bridge_campaign_type_is_membership(campaign_type):
    """Export CSV HelloAsso FR : « Adhésion » ; API : « Membership » — les deux ouvrent le pont."""
    c = (campaign_type or "").strip().lower()
    if not c:
        return True
    if "membership" in c:
        return True
    if "adhésion" in c or "adhesion" in c:
        return True
    return False


class DoreviaHelloassoPayment(models.Model):
    _inherit = "dorevia.helloasso.payment"

    membership_v2_out_invoice_id = fields.Many2one(
        "account.move",
        string="Facture client (rail V2)",
        copy=False,
        ondelete="set null",
        domain="[('move_type', '=', 'out_invoice')]",
    )
    membership_v2_account_payment_id = fields.Many2one(
        "account.payment",
        string="Paiement comptable (rail V2)",
        copy=False,
        ondelete="set null",
    )
    membership_v2_processing_state = fields.Selection(
        [
            ("to_process", "À traiter"),
            ("processed", "Traité"),
            ("error", "Erreur"),
            ("noop", "Déjà traité"),
        ],
        string="État constatation V2",
        copy=False,
        index=True,
    )
    membership_v2_error_message = fields.Text(
        string="Détail erreur constatation V2",
        copy=False,
    )

    def action_open_membership_v2_invoice(self):
        """Ouvre la facture client liée (constatation V2) — raccourci opérateur (S6-3)."""
        self.ensure_one()
        move = self.membership_v2_out_invoice_id
        if not move:
            raise UserError(_("Aucune facture V2 liée à ce pivot."))
        return {
            "type": "ir.actions.act_window",
            "name": move.display_name,
            "res_model": "account.move",
            "res_id": move.id,
            "view_mode": "form",
            "views": [(False, "form")],
            "target": "current",
        }

    def action_open_membership_v2_account_payment(self):
        """Ouvre le paiement comptable enregistré (constatation V2) — raccourci opérateur (S6-3)."""
        self.ensure_one()
        pay = self.membership_v2_account_payment_id
        if not pay:
            raise UserError(_("Aucun paiement comptable V2 lié à ce pivot."))
        return {
            "type": "ir.actions.act_window",
            "name": pay.display_name,
            "res_model": "account.payment",
            "res_id": pay.id,
            "view_mode": "form",
            "views": [(False, "form")],
            "target": "current",
        }

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._membership_bridge_after_persist()
        return records

    def write(self, vals):
        res = super().write(vals)
        if vals and set(vals) & _MEMBERSHIP_BRIDGE_PAYMENT_WRITE_TRIGGER_FIELDS:
            self._membership_bridge_after_persist()
        return res

    @api.model
    def _membership_bridge_write_triggers_pivot(self, vals):
        """Utilisable en test : True si un ``write`` avec ``vals`` doit réévaluer le pont."""
        if not vals:
            return False
        return bool(set(vals) & _MEMBERSHIP_BRIDGE_PAYMENT_WRITE_TRIGGER_FIELDS)

    def _membership_bridge_after_persist(self):
        """Opt-in : compte avec adhésions + pont activé + produit ; sinon journalisation."""
        if self.env.context.get("membership_bridge_skip_hook"):
            return
        Bridge = self.env["dorevia.membership.helloasso.bridge"]
        AccountingV2 = self.env["dorevia.membership.helloasso.accounting.v2"]
        for payment in self:
            account = payment.helloasso_account_id
            if not account:
                continue
            if not account.use_for_members:
                _logger.info(
                    "HelloAsso membership bridge: compte « %s » sans « Adhésions (Membership) », "
                    "pivot %s collecté sans pont.",
                    account.display_name,
                    payment.helloasso_payment_ref,
                )
                continue
            if not account.membership_bridge_enabled:
                _logger.info(
                    "HelloAsso membership bridge: pont désactivé pour le compte « %s », "
                    "pivot %s collecté sans pont.",
                    account.display_name,
                    payment.helloasso_payment_ref,
                )
                continue
            product = account.membership_bridge_product_id
            if not product:
                _logger.info(
                    "HelloAsso membership bridge: pont activé sans produit d'adhésion sur le "
                    "compte « %s », pivot %s ignoré.",
                    account.display_name,
                    payment.helloasso_payment_ref,
                )
                continue
            if not _membership_bridge_campaign_type_is_membership(payment.campaign_type):
                _logger.debug(
                    "HelloAsso membership bridge: type de campagne « %s » (pivot %s), "
                    "hors adhésion — pont non invoqué.",
                    payment.campaign_type,
                    payment.helloasso_payment_ref,
                )
                continue
            rail = account.membership_pont_rail or "v1_line"
            if rail == "none":
                continue
            try:
                if rail == "v2_accounting":
                    out = AccountingV2.process_payment(payment, product)
                else:
                    out = Bridge.process_payment_to_membership_line(payment, product)
                _logger.info(
                    "HelloAsso membership bridge: pivot %s → état=%s (rail=%s)",
                    payment.helloasso_payment_ref,
                    out.get("state"),
                    rail,
                )
            except UserError as err:
                _logger.warning(
                    "HelloAsso membership bridge: pivot %s refusé par le pont — %s",
                    payment.helloasso_payment_ref,
                    err,
                )
            except Exception:
                _logger.exception(
                    "HelloAsso membership bridge: erreur inattendue pour le pivot %s",
                    payment.helloasso_payment_ref,
                )
