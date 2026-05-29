# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class GlcCoverageCockpit(models.TransientModel):
    _inherit = "glc.coverage.cockpit"

    # --- Q1 Couverture analytique ---
    quality_analytic_moves_checked = fields.Integer(
        string="Pièces contrôlées (analytique)",
        readonly=True,
    )
    quality_analytic_moves_covered = fields.Integer(
        string="Pièces couvertes (analytique)",
        readonly=True,
    )
    quality_analytic_moves_uncovered = fields.Integer(
        string="Pièces non couvertes (analytique)",
        readonly=True,
    )
    quality_analytic_coverage_rate = fields.Float(
        string="Taux couverture analytique (%)",
        readonly=True,
        digits=(16, 2),
    )
    quality_analytic_coverage_status = fields.Selection(
        selection=[
            ("green", "Vert"),
            ("orange", "Orange"),
            ("red", "Rouge"),
        ],
        string="Statut couverture analytique",
        readonly=True,
    )

    # --- Q2 Lettrage tiers ---
    quality_reconcile_rate_customer = fields.Float(
        string="Taux lettrage clients (%)",
        readonly=True,
        digits=(16, 2),
    )
    quality_reconcile_rate_supplier = fields.Float(
        string="Taux lettrage fournisseurs (%)",
        readonly=True,
        digits=(16, 2),
    )
    quality_unreconciled_amount_customer = fields.Monetary(
        string="Montant non lettré clients",
        readonly=True,
        currency_field="currency_id",
    )
    quality_unreconciled_amount_supplier = fields.Monetary(
        string="Montant non lettré fournisseurs",
        readonly=True,
        currency_field="currency_id",
    )
    quality_unreconciled_count_customer = fields.Integer(
        string="Lignes ouvertes clients",
        readonly=True,
    )
    quality_unreconciled_count_supplier = fields.Integer(
        string="Lignes ouvertes fournisseurs",
        readonly=True,
    )
    quality_aging_customer_0_30 = fields.Monetary(
        string="Créances 0-30 j",
        readonly=True,
        currency_field="currency_id",
    )
    quality_aging_customer_31_60 = fields.Monetary(
        string="Créances 31-60 j",
        readonly=True,
        currency_field="currency_id",
    )
    quality_aging_customer_61_90 = fields.Monetary(
        string="Créances 61-90 j",
        readonly=True,
        currency_field="currency_id",
    )
    quality_aging_customer_90_plus = fields.Monetary(
        string="Créances 90+ j",
        readonly=True,
        currency_field="currency_id",
    )
    quality_aging_supplier_0_30 = fields.Monetary(
        string="Dettes 0-30 j",
        readonly=True,
        currency_field="currency_id",
    )
    quality_aging_supplier_31_60 = fields.Monetary(
        string="Dettes 31-60 j",
        readonly=True,
        currency_field="currency_id",
    )
    quality_aging_supplier_61_90 = fields.Monetary(
        string="Dettes 61-90 j",
        readonly=True,
        currency_field="currency_id",
    )
    quality_aging_supplier_90_plus = fields.Monetary(
        string="Dettes 90+ j",
        readonly=True,
        currency_field="currency_id",
    )

    # --- Q3 Suivi paiement clients ---
    payment_customer_invoice_count = fields.Integer(
        string="Factures clients émises",
        readonly=True,
    )
    payment_customer_invoice_amount = fields.Monetary(
        string="Montant facturé clients",
        readonly=True,
        currency_field="currency_id",
    )
    payment_customer_paid_count = fields.Integer(string="Factures clients payées", readonly=True)
    payment_customer_paid_amount = fields.Monetary(
        string="Montant payé clients",
        readonly=True,
        currency_field="currency_id",
    )
    payment_customer_partial_count = fields.Integer(
        string="Factures clients partielles",
        readonly=True,
    )
    payment_customer_partial_amount = fields.Monetary(
        string="Montant partiel clients",
        readonly=True,
        currency_field="currency_id",
    )
    payment_customer_in_payment_count = fields.Integer(
        string="Factures clients en cours",
        readonly=True,
    )
    payment_customer_in_payment_amount = fields.Monetary(
        string="Montant en cours clients",
        readonly=True,
        currency_field="currency_id",
    )
    payment_customer_not_paid_count = fields.Integer(
        string="Factures clients non payées",
        readonly=True,
    )
    payment_customer_not_paid_amount = fields.Monetary(
        string="Montant non payé clients",
        readonly=True,
        currency_field="currency_id",
    )
    payment_customer_refund_count = fields.Integer(string="Avoirs clients", readonly=True)
    payment_customer_refund_amount = fields.Monetary(
        string="Montant avoirs clients",
        readonly=True,
        currency_field="currency_id",
    )
    payment_customer_residual = fields.Monetary(
        string="Reste à encaisser clients",
        readonly=True,
        currency_field="currency_id",
    )

    # --- Q3 Suivi paiement fournisseurs ---
    payment_supplier_invoice_count = fields.Integer(
        string="Factures fournisseurs reçues",
        readonly=True,
    )
    payment_supplier_invoice_amount = fields.Monetary(
        string="Montant facturé fournisseurs",
        readonly=True,
        currency_field="currency_id",
    )
    payment_supplier_paid_count = fields.Integer(
        string="Factures fournisseurs payées",
        readonly=True,
    )
    payment_supplier_paid_amount = fields.Monetary(
        string="Montant payé fournisseurs",
        readonly=True,
        currency_field="currency_id",
    )
    payment_supplier_partial_count = fields.Integer(
        string="Factures fournisseurs partielles",
        readonly=True,
    )
    payment_supplier_partial_amount = fields.Monetary(
        string="Montant partiel fournisseurs",
        readonly=True,
        currency_field="currency_id",
    )
    payment_supplier_in_payment_count = fields.Integer(
        string="Factures fournisseurs en cours",
        readonly=True,
    )
    payment_supplier_in_payment_amount = fields.Monetary(
        string="Montant en cours fournisseurs",
        readonly=True,
        currency_field="currency_id",
    )
    payment_supplier_not_paid_count = fields.Integer(
        string="Factures fournisseurs non payées",
        readonly=True,
    )
    payment_supplier_not_paid_amount = fields.Monetary(
        string="Montant non payé fournisseurs",
        readonly=True,
        currency_field="currency_id",
    )
    payment_supplier_refund_count = fields.Integer(string="Avoirs fournisseurs", readonly=True)
    payment_supplier_refund_amount = fields.Monetary(
        string="Montant avoirs fournisseurs",
        readonly=True,
        currency_field="currency_id",
    )
    payment_supplier_residual = fields.Monetary(
        string="Reste à payer fournisseurs",
        readonly=True,
        currency_field="currency_id",
    )

    def _quality_analytic_moves(self, date_from, date_to):
        self.ensure_one()
        moves = self.env["account.move"].search(
            [
                ("company_id", "=", self.company_id.id),
                ("state", "=", "posted"),
                ("move_type", "in", list(self._GLC_QUALITY_MOVE_TYPES)),
            ]
        )
        moves = moves.filtered(lambda move: self._glc_move_in_period(move, date_from, date_to))
        return moves.filtered(
            lambda move: move.line_ids.filtered(self._glc_is_coverage_controlled_line)
        )

    def _aggregate_quality_analytic(self, date_from, date_to):
        self.ensure_one()
        moves = self._quality_analytic_moves(date_from, date_to)
        checked = len(moves)
        covered = len(moves.filtered(self._glc_move_is_analytically_covered))
        uncovered = checked - covered
        rate = (covered / checked * 100.0) if checked else 100.0
        return {
            "quality_analytic_moves_checked": checked,
            "quality_analytic_moves_covered": covered,
            "quality_analytic_moves_uncovered": uncovered,
            "quality_analytic_coverage_rate": rate,
            "quality_analytic_coverage_status": self._glc_coverage_rate_status(rate),
        }

    def _reconcile_lines_domain_base(self, date_to, partner_type):
        self.ensure_one()
        return [
            ("company_id", "=", self.company_id.id),
            ("parent_state", "=", "posted"),
            ("account_id.account_type", "=", partner_type),
            ("display_type", "not in", ("line_section", "line_note")),
            ("date", "<=", date_to),
        ]

    def _aggregate_reconcile_side(self, date_to, partner_type):
        lines = self.env["account.move.line"].search(
            self._reconcile_lines_domain_base(date_to, partner_type)
        )
        total_amount = sum(abs(line.balance) for line in lines)
        reconciled_amount = sum(
            abs(line.balance) for line in lines if line.reconciled or not line.amount_residual
        )
        open_lines = lines.filtered(lambda line: line.amount_residual)
        unreconciled_amount = sum(self._glc_line_open_amount(line) for line in open_lines)
        rate = (reconciled_amount / total_amount * 100.0) if total_amount else 100.0
        aging = {
            "0_30": 0.0,
            "31_60": 0.0,
            "61_90": 0.0,
            "90_plus": 0.0,
        }
        for line in open_lines:
            bucket = self._glc_aging_bucket(line, date_to)
            aging[bucket] += self._glc_line_open_amount(line)
        return {
            "rate": rate,
            "unreconciled_amount": unreconciled_amount,
            "open_count": len(open_lines),
            "aging": aging,
        }

    def _aggregate_quality_reconcile(self, date_from, date_to):
        self.ensure_one()
        customer = self._aggregate_reconcile_side(date_to, "asset_receivable")
        supplier = self._aggregate_reconcile_side(date_to, "liability_payable")
        return {
            "quality_reconcile_rate_customer": customer["rate"],
            "quality_reconcile_rate_supplier": supplier["rate"],
            "quality_unreconciled_amount_customer": customer["unreconciled_amount"],
            "quality_unreconciled_amount_supplier": supplier["unreconciled_amount"],
            "quality_unreconciled_count_customer": customer["open_count"],
            "quality_unreconciled_count_supplier": supplier["open_count"],
            "quality_aging_customer_0_30": customer["aging"]["0_30"],
            "quality_aging_customer_31_60": customer["aging"]["31_60"],
            "quality_aging_customer_61_90": customer["aging"]["61_90"],
            "quality_aging_customer_90_plus": customer["aging"]["90_plus"],
            "quality_aging_supplier_0_30": supplier["aging"]["0_30"],
            "quality_aging_supplier_31_60": supplier["aging"]["31_60"],
            "quality_aging_supplier_61_90": supplier["aging"]["61_90"],
            "quality_aging_supplier_90_plus": supplier["aging"]["90_plus"],
        }

    def _payment_moves(self, date_from, date_to, move_types):
        self.ensure_one()
        moves = self.env["account.move"].search(
            [
                ("company_id", "=", self.company_id.id),
                ("state", "=", "posted"),
                ("move_type", "in", move_types),
            ]
        )
        return moves.filtered(lambda move: self._glc_move_in_period(move, date_from, date_to))

    def _aggregate_payment_side(self, date_from, date_to, invoice_type, refund_type):
        invoices = self._payment_moves(date_from, date_to, [invoice_type])
        refunds = self._payment_moves(date_from, date_to, [refund_type])
        states = {
            "paid": {"count": 0, "amount": 0.0},
            "partial": {"count": 0, "amount": 0.0},
            "in_payment": {"count": 0, "amount": 0.0},
            "not_paid": {"count": 0, "amount": 0.0},
        }
        residual = 0.0
        for move in invoices:
            state = move.payment_state
            if state not in states:
                state = "not_paid"
            states[state]["count"] += 1
            states[state]["amount"] += abs(move.amount_total_signed)
            if move.amount_residual:
                residual += abs(move.amount_residual_signed)
        return {
            "invoice_count": len(invoices),
            "invoice_amount": sum(abs(move.amount_total_signed) for move in invoices),
            "refund_count": len(refunds),
            "refund_amount": sum(abs(move.amount_total_signed) for move in refunds),
            "residual": residual,
            **{
                f"{key}_count": value["count"]
                for key, value in states.items()
            },
            **{
                f"{key}_amount": value["amount"]
                for key, value in states.items()
            },
        }

    def _aggregate_payment_tracking(self, date_from, date_to):
        self.ensure_one()
        customer = self._aggregate_payment_side(
            date_from, date_to, "out_invoice", "out_refund"
        )
        supplier = self._aggregate_payment_side(
            date_from, date_to, "in_invoice", "in_refund"
        )
        return {
            "payment_customer_invoice_count": customer["invoice_count"],
            "payment_customer_invoice_amount": customer["invoice_amount"],
            "payment_customer_paid_count": customer["paid_count"],
            "payment_customer_paid_amount": customer["paid_amount"],
            "payment_customer_partial_count": customer["partial_count"],
            "payment_customer_partial_amount": customer["partial_amount"],
            "payment_customer_in_payment_count": customer["in_payment_count"],
            "payment_customer_in_payment_amount": customer["in_payment_amount"],
            "payment_customer_not_paid_count": customer["not_paid_count"],
            "payment_customer_not_paid_amount": customer["not_paid_amount"],
            "payment_customer_refund_count": customer["refund_count"],
            "payment_customer_refund_amount": customer["refund_amount"],
            "payment_customer_residual": customer["residual"],
            "payment_supplier_invoice_count": supplier["invoice_count"],
            "payment_supplier_invoice_amount": supplier["invoice_amount"],
            "payment_supplier_paid_count": supplier["paid_count"],
            "payment_supplier_paid_amount": supplier["paid_amount"],
            "payment_supplier_partial_count": supplier["partial_count"],
            "payment_supplier_partial_amount": supplier["partial_amount"],
            "payment_supplier_in_payment_count": supplier["in_payment_count"],
            "payment_supplier_in_payment_amount": supplier["in_payment_amount"],
            "payment_supplier_not_paid_count": supplier["not_paid_count"],
            "payment_supplier_not_paid_amount": supplier["not_paid_amount"],
            "payment_supplier_refund_count": supplier["refund_count"],
            "payment_supplier_refund_amount": supplier["refund_amount"],
            "payment_supplier_residual": supplier["residual"],
        }

    def _aggregate_quality_payment(self, date_from, date_to):
        self.ensure_one()
        return {
            **self._aggregate_quality_analytic(date_from, date_to),
            **self._aggregate_quality_reconcile(date_from, date_to),
            **self._aggregate_payment_tracking(date_from, date_to),
        }

    def _uncovered_move_ids(self, date_from, date_to):
        self.ensure_one()
        moves = self._quality_analytic_moves(date_from, date_to)
        return moves.filtered(
            lambda move: not self._glc_move_is_analytically_covered(move)
        ).ids

    def _uncovered_move_line_domain(self, date_from, date_to):
        self.ensure_one()
        move_ids = self._uncovered_move_ids(date_from, date_to)
        if not move_ids:
            return [(0, "=", 1)]
        return [
            ("move_id", "in", move_ids),
            ("display_type", "not in", ("line_section", "line_note")),
        ]

    def action_open_quality_uncovered_moves(self):
        self.ensure_one()
        date_from, date_to = self._period_bounds()
        move_ids = self._uncovered_move_ids(date_from, date_to)
        return {
            "type": "ir.actions.act_window",
            "name": _("Pièces sans couverture analytique"),
            "res_model": "account.move",
            "view_mode": "list,form",
            "domain": [("id", "in", move_ids)],
            "context": {"create": False},
            "target": "current",
        }

    def action_open_quality_uncovered_move_lines(self):
        self.ensure_one()
        date_from, date_to = self._period_bounds()
        return {
            "type": "ir.actions.act_window",
            "name": _("Lignes sans couverture analytique"),
            "res_model": "account.move.line",
            "view_mode": "list,form",
            "domain": self._uncovered_move_line_domain(date_from, date_to),
            "context": {"create": False},
            "target": "current",
        }

    def action_open_unreconciled_customer_lines(self):
        self.ensure_one()
        date_from, date_to = self._period_bounds()
        domain = self._reconcile_lines_domain_base(date_to, "asset_receivable")
        domain.append(("amount_residual", "!=", 0))
        return {
            "type": "ir.actions.act_window",
            "name": _("Lignes clients non lettrées"),
            "res_model": "account.move.line",
            "view_mode": "list,form",
            "domain": domain,
            "context": {"create": False},
            "target": "current",
        }

    def action_open_unreconciled_supplier_lines(self):
        self.ensure_one()
        date_from, date_to = self._period_bounds()
        domain = self._reconcile_lines_domain_base(date_to, "liability_payable")
        domain.append(("amount_residual", "!=", 0))
        return {
            "type": "ir.actions.act_window",
            "name": _("Lignes fournisseurs non lettrées"),
            "res_model": "account.move.line",
            "view_mode": "list,form",
            "domain": domain,
            "context": {"create": False},
            "target": "current",
        }

    def _payment_move_action(self, title, date_from, date_to, move_types, payment_states=None):
        self.ensure_one()
        moves = self._payment_moves(date_from, date_to, move_types)
        if payment_states:
            moves = moves.filtered(lambda move: move.payment_state in payment_states)
        return {
            "type": "ir.actions.act_window",
            "name": title,
            "res_model": "account.move",
            "view_mode": "list,form",
            "domain": [("id", "in", moves.ids)],
            "context": {"create": False},
            "target": "current",
        }

    def action_open_payment_customer_invoices(self):
        self.ensure_one()
        date_from, date_to = self._period_bounds()
        return self._payment_move_action(
            _("Factures clients — période"),
            date_from,
            date_to,
            ["out_invoice"],
        )

    def action_open_payment_customer_open(self):
        self.ensure_one()
        date_from, date_to = self._period_bounds()
        return self._payment_move_action(
            _("Factures clients ouvertes"),
            date_from,
            date_to,
            ["out_invoice"],
            payment_states={"not_paid", "partial", "in_payment"},
        )

    def action_open_payment_supplier_invoices(self):
        self.ensure_one()
        date_from, date_to = self._period_bounds()
        return self._payment_move_action(
            _("Factures fournisseurs — période"),
            date_from,
            date_to,
            ["in_invoice"],
        )

    def action_open_payment_supplier_open(self):
        self.ensure_one()
        date_from, date_to = self._period_bounds()
        return self._payment_move_action(
            _("Factures fournisseurs ouvertes"),
            date_from,
            date_to,
            ["in_invoice"],
            payment_states={"not_paid", "partial", "in_payment"},
        )

    def _action_refresh_single(self):
        res = super()._action_refresh_single()
        for cockpit in self:
            date_from, date_to = cockpit._period_bounds()
            quality_vals = cockpit._aggregate_quality_payment(date_from, date_to)
            cockpit.with_context(glc_cockpit_auto_refreshing=True).write(quality_vals)
        return res