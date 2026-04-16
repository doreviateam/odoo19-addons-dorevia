# -*- coding: utf-8 -*-

from odoo import _, api, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends(
        "restrict_mode_hash_table",
        "state",
        "inalterable_hash",
        "need_cancel_request",
        "move_type",
    )
    def _compute_show_reset_to_draft_button(self):
        """Masque le bouton « Remettre en brouillon » pour les factures client postées."""
        super()._compute_show_reset_to_draft_button()
        for move in self:
            if move.move_type == "out_invoice" and move.state == "posted":
                move.show_reset_to_draft_button = False

    def button_draft(self):
        """Filet de sécurité si l’action est appelée hors UI (RPC, tests)."""
        for move in self:
            if move.move_type == "out_invoice" and move.state == "posted":
                raise UserError(
                    _(
                        "Impossible de remettre en brouillon une facture client postée.\n\n"
                        "Utilisez une annulation ou un avoir pour corriger."
                    )
                )

        return super().button_draft()
