# -*- coding: utf-8 -*-
"""Extension ``account.payment`` pour le connecteur Vault.

Le fichier n'est pas nommé ``account_payment.py`` pour éviter toute ambiguïté
avec les sources du module ``account`` (fichier homonyme) lors des imports
ou d'outillage qui parcourent les addons.
"""

from odoo import _, fields, models
from odoo.exceptions import UserError

from odoo.addons.dorevia_vault_connector.services import payload_builder, vault_client


class AccountPayment(models.Model):
    _inherit = "account.payment"

    DOREVIA_VAULT_STATES = ("in_process", "paid")

    dorevia_vault_status = fields.Selection(
        [
            ("todo", "À envoyer"),
            ("sent", "Envoyé"),
            ("failed", "Échec"),
        ],
        string="Statut Dorevia Vault",
        default="todo",
        copy=False,
        readonly=True,
    )
    dorevia_vault_last_attempt_at = fields.Datetime(
        string="Dernier essai Vault",
        copy=False,
        readonly=True,
    )
    dorevia_vault_error_message = fields.Text(
        string="Message d'erreur Vault",
        copy=False,
        readonly=True,
    )
    dorevia_vault_remote_ref = fields.Char(
        string="Référence distante",
        copy=False,
        readonly=True,
    )

    def action_post(self):
        res = super().action_post()
        for payment in self:
            if payment._is_dorevia_vault_eligible():
                payment._dorevia_vault_send()
        return res

    def action_validate(self):
        res = super().action_validate()
        for payment in self:
            if payment.dorevia_vault_status in ("todo", "failed") and payment._is_dorevia_vault_eligible():
                payment._dorevia_vault_send()
        return res

    def action_retry_dorevia_vault_send(self):
        for payment in self:
            if payment.state not in self.DOREVIA_VAULT_STATES:
                raise UserError(
                    _("Réessai Vault : uniquement sur un paiement confirmé ou validé.")
                )
            if payment.dorevia_vault_status not in ("failed", "todo"):
                raise UserError(
                    _("Réessai Vault : statut actuel incompatible (%s).")
                    % (payment.dorevia_vault_status or "")
                )
            if not payment._is_dorevia_vault_eligible():
                raise UserError(
                    _("Réessai Vault : connecteur inactif, URL manquante ou paiement non éligible.")
                )
            payment._dorevia_vault_send()
        return True

    def _is_dorevia_vault_eligible(self):
        self.ensure_one()
        icp = self.env["ir.config_parameter"].sudo()
        if icp.get_param("dorevia_vault_connector.enabled") != "True":
            return False
        url = (icp.get_param("dorevia_vault_connector.target_url") or "").strip()
        if not url:
            return False
        if self.payment_type not in ("inbound", "outbound"):
            return False
        if self.state not in self.DOREVIA_VAULT_STATES:
            return False
        return True

    def _dorevia_vault_send(self):
        self.ensure_one()
        now = fields.Datetime.now()
        self.write(
            {
                "dorevia_vault_last_attempt_at": now,
                "dorevia_vault_error_message": False,
            }
        )
        try:
            payload = payload_builder.build_payment_payload(self)
            result = vault_client.send_to_vault(self.env, payload)
        except Exception as err:  # noqa: BLE001
            self.write(
                {
                    "dorevia_vault_status": "failed",
                    "dorevia_vault_error_message": str(err),
                    "dorevia_vault_remote_ref": False,
                }
            )
            return
        if result.get("success"):
            self.write(
                {
                    "dorevia_vault_status": "sent",
                    "dorevia_vault_remote_ref": result.get("remote_ref") or False,
                    "dorevia_vault_error_message": False,
                }
            )
        else:
            self.write(
                {
                    "dorevia_vault_status": "failed",
                    "dorevia_vault_error_message": result.get("message") or _("Erreur inconnue"),
                    "dorevia_vault_remote_ref": False,
                }
            )
