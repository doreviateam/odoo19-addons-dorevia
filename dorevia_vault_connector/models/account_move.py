# -*- coding: utf-8 -*-

from odoo import _, fields, models
from odoo.exceptions import UserError

from odoo.addons.dorevia_vault_connector.services import payload_builder, vault_client


class AccountMove(models.Model):
    _inherit = "account.move"

    DOREVIA_VAULT_MOVE_TYPES = (
        "out_invoice",
        "in_invoice",
        "out_refund",
        "in_refund",
    )

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
        for move in self:
            if move._is_dorevia_vault_eligible():
                move._dorevia_vault_send()
        return res

    def action_retry_dorevia_vault_send(self):
        """Rejeu manuel sur un document comptable posté éligible."""
        for move in self:
            if move.move_type not in self.DOREVIA_VAULT_MOVE_TYPES or move.state != "posted":
                raise UserError(
                    _(
                        "Réessai Vault : uniquement sur un document posté de type vente, achat ou avoir."
                    )
                )
            if move.dorevia_vault_status not in ("failed", "todo"):
                raise UserError(
                    _("Réessai Vault : statut actuel incompatible (%s).")
                    % (move.dorevia_vault_status or "")
                )
            if not move._is_dorevia_vault_eligible():
                raise UserError(
                    _("Réessai Vault : connecteur inactif ou URL manquante, ou document non éligible.")
                )
            move._dorevia_vault_send()
        return True

    def _is_dorevia_vault_eligible(self):
        self.ensure_one()
        icp = self.env["ir.config_parameter"].sudo()
        if icp.get_param("dorevia_vault_connector.enabled") != "True":
            return False
        url = (icp.get_param("dorevia_vault_connector.target_url") or "").strip()
        if not url:
            return False
        if self.move_type not in self.DOREVIA_VAULT_MOVE_TYPES:
            return False
        if self.state != "posted":
            return False
        return True

    def _dorevia_vault_send(self):
        """N'interrompt jamais la validation comptable : toute erreur → statut ``failed``."""
        self.ensure_one()
        now = fields.Datetime.now()
        self.write(
            {
                "dorevia_vault_last_attempt_at": now,
                "dorevia_vault_error_message": False,
            }
        )
        try:
            payload = payload_builder.build_payload(self)
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
