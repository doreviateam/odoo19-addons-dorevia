# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

from .glc_constants import GLC_EXPENSE_ACCOUNT_TYPES, GLC_INCOME_ACCOUNT_TYPES


class GlcQualityMixin(models.AbstractModel):
    """Helpers partagés couverture analytique / lettrage / paiement (GQ-6)."""

    _name = "glc.quality.mixin"
    _description = "Mixin qualité comptable cockpit GLC"

    _GLC_QUALITY_MOVE_TYPES = frozenset(
        {"out_invoice", "out_refund", "in_invoice", "in_refund"}
    )
    _GLC_PAYMENT_TRACKING_STATES = frozenset(
        {"not_paid", "in_payment", "partial", "paid", "reversed", "legacy"}
    )
    _GLC_EXCLUDED_ACCOUNT_TYPES = frozenset(
        {
            "asset_receivable",
            "liability_payable",
            "asset_cash",
            "liability_credit_card",
        }
    )

    @api.model
    def _glc_move_period_date(self, move):
        return move.invoice_date or move.date

    @api.model
    def _glc_move_in_period(self, move, date_from, date_to):
        ref_date = self._glc_move_period_date(move)
        return bool(ref_date and date_from <= ref_date <= date_to)

    @api.model
    def _glc_is_coverage_controlled_line(self, line):
        """Ligne métier pertinente pour le contrôle couverture analytique (Q1)."""
        if line.display_type in ("line_section", "line_note"):
            return False
        move = line.move_id
        if move.move_type not in self._GLC_QUALITY_MOVE_TYPES:
            return False
        account_type = line.account_id.account_type
        if account_type in self._GLC_EXCLUDED_ACCOUNT_TYPES:
            return False
        if (line.account_id.code or "").startswith(("512", "53")):
            return False
        return account_type in GLC_INCOME_ACCOUNT_TYPES + GLC_EXPENSE_ACCOUNT_TYPES

    @api.model
    def _glc_line_has_analytic_coverage(self, line):
        distribution = line.analytic_distribution or {}
        if distribution:
            return True
        return bool(
            self.env["account.analytic.line"].search_count(
                [("move_line_id", "=", line.id)], limit=1
            )
        )

    @api.model
    def _glc_move_is_analytically_covered(self, move):
        controlled = move.line_ids.filtered(self._glc_is_coverage_controlled_line)
        if not controlled:
            return True
        return all(self._glc_line_has_analytic_coverage(line) for line in controlled)

    @api.model
    def _glc_reconcile_partner_account_types(self):
        return ("asset_receivable", "liability_payable")

    @api.model
    def _glc_is_reconcile_controlled_line(self, line, partner_type):
        """Ligne tiers lettrable — stock à date fin période (Q2)."""
        if line.display_type in ("line_section", "line_note"):
            return False
        if line.parent_state != "posted":
            return False
        if line.account_id.account_type != partner_type:
            return False
        return True

    @api.model
    def _glc_line_open_amount(self, line):
        return abs(line.amount_residual)

    @api.model
    def _glc_aging_bucket(self, line, reference_date):
        maturity = line.date_maturity or line.date
        if not maturity or not reference_date:
            return "90_plus"
        days = (reference_date - maturity).days
        if days <= 30:
            return "0_30"
        if days <= 60:
            return "31_60"
        if days <= 90:
            return "61_90"
        return "90_plus"

    @api.model
    def _glc_coverage_rate_status(self, rate):
        if rate >= 100.0:
            return "green"
        if rate >= 95.0:
            return "orange"
        return "red"
