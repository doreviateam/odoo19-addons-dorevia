# -*- coding: utf-8 -*-

from odoo import api, models

from .glc_constants import (
    GLC_EXCLUDED_GL_ACCOUNT_PREFIXES,
    GLC_EXPENSE_ACCOUNT_TYPES,
    GLC_INCOME_ACCOUNT_TYPES,
    GLC_PAYROLL_ACCOUNT_PREFIXES,
)


class GlcCoverageCockpit(models.TransientModel):
    """Helpers partagés couverture analytique / lettrage / paiement (GQ-6)."""

    _inherit = "glc.coverage.cockpit"

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
    _GLC_EXCLUDED_LINE_DISPLAY_TYPES = frozenset(
        {"line_section", "line_note", "tax", "payment_term"},
    )

    @api.model
    def _glc_move_period_date(self, move):
        return move.invoice_date or move.date

    @api.model
    def _glc_move_in_period(self, move, date_from, date_to):
        ref_date = self._glc_move_period_date(move)
        return bool(ref_date and date_from <= ref_date <= date_to)

    @api.model
    def _glc_account_code_excluded_from_q1(self, account_code):
        code = account_code or ""
        if code.startswith(("512", "53", "580")):
            return True
        for prefix in GLC_PAYROLL_ACCOUNT_PREFIXES + GLC_EXCLUDED_GL_ACCOUNT_PREFIXES:
            if code.startswith(prefix):
                return True
        return False

    @api.model
    def _glc_is_coverage_controlled_line(self, line):
        """Ligne comptable éligible au pilotage GLC (Q1 — confiance analytique)."""
        if line.display_type in self._GLC_EXCLUDED_LINE_DISPLAY_TYPES:
            return False
        if line.parent_state != "posted":
            return False
        account_type = line.account_id.account_type
        if account_type in self._GLC_EXCLUDED_ACCOUNT_TYPES:
            return False
        account_code = line.account_id.code or ""
        if self._glc_account_code_excluded_from_q1(account_code):
            return False
        if not (account_code.startswith("6") or account_code.startswith("7")):
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

    _GLC_INVOICE_MOVE_TYPES = frozenset(
        {"out_invoice", "out_refund", "in_invoice", "in_refund"}
    )
    _GLC_COCKPIT_PAID_PAYMENT_STATES = frozenset({"paid"})
    _GLC_CUSTOMER_INVOICE_MOVE_TYPES = frozenset({"out_invoice", "out_receipt"})
    _GLC_SUPPLIER_INVOICE_MOVE_TYPES = frozenset({"in_invoice", "in_receipt"})

    @api.model
    def _glc_is_cash_or_bank_account(self, account):
        """Compte trésorerie / virement interne (512, 53, 580)."""
        if not account:
            return False
        code = account.code or ""
        if code.startswith(("512", "53", "580")):
            return True
        return account.account_type == "asset_cash"

    @api.model
    def _glc_move_line_has_bank_reconciliation(self, move_line):
        """Vrai si la ligne est lettrée avec un compte banque / caisse."""
        partials = move_line.matched_debit_ids | move_line.matched_credit_ids
        for partial in partials:
            counterpart = (
                partial.debit_move_id
                if partial.debit_move_id != move_line
                else partial.credit_move_id
            )
            if self._glc_is_cash_or_bank_account(counterpart.account_id):
                return True
        return False

    @api.model
    def _glc_analytic_line_is_paid_for_cockpit(self, analytic_line):
        """Règle vue « Payé uniquement » du tableau détail cockpit."""
        move_line = analytic_line.move_line_id
        if not move_line:
            return False
        move = move_line.move_id
        if move.move_type in self._GLC_INVOICE_MOVE_TYPES:
            return move.payment_state in self._GLC_COCKPIT_PAID_PAYMENT_STATES
        if self._glc_is_cash_or_bank_account(move_line.account_id):
            return True
        if any(
            self._glc_is_cash_or_bank_account(line.account_id)
            for line in move.line_ids
        ):
            return True
        if self._glc_move_line_has_bank_reconciliation(move_line):
            return True
        return False

    @api.model
    def _glc_analytic_line_is_customer_invoice_for_cockpit(self, analytic_line):
        """Ligne ressource issue d'une facture / reçu client (KPI qualité documentaire)."""
        move_line = analytic_line.move_line_id
        if not move_line:
            return False
        return move_line.move_id.move_type in self._GLC_CUSTOMER_INVOICE_MOVE_TYPES

    @api.model
    def _glc_analytic_line_is_supplier_invoice_for_cockpit(self, analytic_line):
        """Ligne dépense issue d'une facture / reçu fournisseur (KPI qualité documentaire)."""
        move_line = analytic_line.move_line_id
        if not move_line:
            return False
        return move_line.move_id.move_type in self._GLC_SUPPLIER_INVOICE_MOVE_TYPES
