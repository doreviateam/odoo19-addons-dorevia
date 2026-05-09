# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo.tests.common import SavepointCase


class TestCashGuardConstraints(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company

        cls.account = cls.env["account.account"].search(
            [("company_id", "=", cls.company.id), ("deprecated", "=", False)], limit=1
        )
        if not cls.account:
            cls.account = cls.env["account.account"].create(
                {
                    "name": "CG Constraint Account",
                    "code": "CGC001",
                    "account_type": "asset_current",
                    "company_id": cls.company.id,
                }
            )

        cls.bank_journal = cls.env["account.journal"].create(
            {
                "name": "CG Constraint Bank",
                "code": "CGCB",
                "type": "bank",
                "company_id": cls.company.id,
                "default_account_id": cls.account.id,
            }
        )
        cls.sale_journal = cls.env["account.journal"].create(
            {
                "name": "CG Constraint Sale",
                "code": "CGCS",
                "type": "sale",
                "company_id": cls.company.id,
            }
        )
        cls.budget_post = cls.env["account.budget.post"].create(
            {
                "name": "CG Constraint Budget Post",
                "account_ids": [(6, 0, [cls.account.id])],
                "company_id": cls.company.id,
            }
        )

    def _base_guard_vals(self):
        return {
            "date_from": "2026-05-01",
            "date_to": "2026-05-31",
            "bank_journal_id": self.bank_journal.id,
            "company_id": self.company.id,
            "alert_threshold": 0.0,
        }

    def test_invalid_dates(self):
        vals = self._base_guard_vals()
        vals.update({"date_from": "2026-05-31", "date_to": "2026-05-01"})
        with self.assertRaises(ValidationError):
            self.env["dorevia.cash.guard"].create(vals)

    def test_negative_threshold(self):
        vals = self._base_guard_vals()
        vals["alert_threshold"] = -1.0
        with self.assertRaises(ValidationError):
            self.env["dorevia.cash.guard"].create(vals)

    def test_journal_must_be_bank_or_cash(self):
        vals = self._base_guard_vals()
        vals["bank_journal_id"] = self.sale_journal.id
        with self.assertRaises(ValidationError):
            self.env["dorevia.cash.guard"].create(vals)

    def test_line_requires_budget_post(self):
        guard = self.env["dorevia.cash.guard"].create(self._base_guard_vals())
        with self.assertRaises(Exception):
            self.env["dorevia.cash.guard.line"].create(
                {
                    "guard_id": guard.id,
                    "projection_date": "2026-05-10",
                    "direction": "inflow",
                    "line_type": "planned",
                    "label": "Missing budget post",
                    "projected_amount": 10.0,
                    "sequence": 10,
                    "cash_state": "planned",
                }
            )

    def test_negative_projected_amount(self):
        guard = self.env["dorevia.cash.guard"].create(self._base_guard_vals())
        with self.assertRaises(ValidationError):
            self.env["dorevia.cash.guard.line"].create(
                {
                    "guard_id": guard.id,
                    "projection_date": "2026-05-10",
                    "budget_post_id": self.budget_post.id,
                    "direction": "inflow",
                    "line_type": "planned",
                    "label": "Negative projected",
                    "projected_amount": -10.0,
                    "sequence": 10,
                    "cash_state": "planned",
                }
            )

    def test_negative_realized_amount(self):
        guard = self.env["dorevia.cash.guard"].create(self._base_guard_vals())
        with self.assertRaises(ValidationError):
            self.env["dorevia.cash.guard.line"].create(
                {
                    "guard_id": guard.id,
                    "projection_date": "2026-05-10",
                    "budget_post_id": self.budget_post.id,
                    "direction": "inflow",
                    "line_type": "planned",
                    "label": "Negative realized",
                    "projected_amount": 10.0,
                    "realized_amount": -1.0,
                    "sequence": 10,
                    "cash_state": "planned",
                }
            )

    def test_company_coherence_with_journal(self):
        other_company = self.env["res.company"].create({"name": "CG Other Company"})
        other_account = self.env["account.account"].search(
            [("company_id", "=", other_company.id), ("deprecated", "=", False)], limit=1
        )
        if not other_account:
            other_account = self.env["account.account"].create(
                {
                    "name": "CG Other Account",
                    "code": "CGO001",
                    "account_type": "asset_current",
                    "company_id": other_company.id,
                }
            )
        other_journal = self.env["account.journal"].create(
            {
                "name": "CG Other Bank",
                "code": "CGOB",
                "type": "bank",
                "company_id": other_company.id,
                "default_account_id": other_account.id,
            }
        )
        vals = self._base_guard_vals()
        vals.update(
            {
                "company_id": self.company.id,
                "bank_journal_id": other_journal.id,
            }
        )
        with self.assertRaises(ValidationError):
            self.env["dorevia.cash.guard"].create(vals)
