# -*- coding: utf-8 -*-

from datetime import date

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase
from unittest.mock import patch


class TestCashGuardWorkflow(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bank_journal = cls.env["account.journal"].search([("type", "=", "bank")], limit=1)
        if not cls.bank_journal:
            raise AssertionError("Aucun journal bancaire disponible pour les tests.")
        cls.company = cls.bank_journal.company_id
        cls.account = (
            cls.bank_journal.default_account_id
            or cls.bank_journal.payment_debit_account_id
            or cls.bank_journal.payment_credit_account_id
        )
        if not cls.account:
            raise AssertionError("Aucun compte de liquidite disponible sur le journal bancaire.")
        cls.budget_post = cls.env["account.budget.post"].create(
            {
                "name": "CG WF Budget Post",
                "account_ids": [(6, 0, [cls.account.id])],
            }
        )

        cls.group_user = cls.env.ref("dorevia_cash_guard.group_cash_guard_user")
        cls.group_manager = cls.env.ref("dorevia_cash_guard.group_cash_guard_manager")
        cls.base_user_group = cls.env.ref("base.group_user")
        cls.cash_manager = cls.env.ref("base.user_admin")
        cls.cash_user = cls.env["res.users"].search(
            [("share", "=", False), ("id", "!=", cls.cash_manager.id)],
            limit=1,
        )
        if not cls.cash_user:
            cls.cash_user = cls.cash_manager
        cls.cash_user.write({"group_ids": [(4, cls.base_user_group.id), (4, cls.group_user.id)]})
        cls.cash_manager.write(
            {
                "group_ids": [
                    (4, cls.base_user_group.id),
                    (4, cls.group_user.id),
                    (4, cls.group_manager.id),
                ]
            }
        )

    def _create_guard(self, user):
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 10)):
            return self.env["dorevia.cash.guard"].with_user(user).create(
                {
                    "date_from": "2026-05-01",
                    "date_to": "2026-05-31",
                    "bank_journal_id": self.bank_journal.id,
                    "company_id": self.company.id,
                    "alert_threshold": 100.0,
                }
            )

    def test_workflow_state_transitions(self):
        guard = self._create_guard(self.cash_user)
        guard.with_user(self.cash_user).action_validate()
        self.assertEqual(guard.state, "validated")
        guard.with_user(self.cash_manager).action_close()
        self.assertEqual(guard.state, "closed")
        guard.with_user(self.cash_manager).action_reopen()
        self.assertEqual(guard.state, "draft")

    def test_non_manager_cannot_reopen(self):
        if self.cash_user.id == self.cash_manager.id:
            self.skipTest("No dedicated non-manager user available in this environment.")
        guard = self._create_guard(self.cash_user)
        guard.with_user(self.cash_user).action_validate()
        with self.assertRaises(UserError):
            guard.with_user(self.cash_user).action_reopen()

    def test_user_can_edit_structural_fields_after_legacy_validate(self):
        """V1.1 : plus de verrouillage selon ``state`` en UI ; les anciens états restent en base."""
        if self.cash_user.id == self.cash_manager.id:
            self.skipTest("No dedicated non-manager user available in this environment.")
        guard = self._create_guard(self.cash_user)
        guard.with_user(self.cash_user).action_validate()
        guard.with_user(self.cash_user).write({"alert_threshold": 50.0})
        self.assertEqual(guard.alert_threshold, 50.0)

    def test_user_can_edit_lines_after_legacy_validate(self):
        if self.cash_user.id == self.cash_manager.id:
            self.skipTest("No dedicated non-manager user available in this environment.")
        guard = self._create_guard(self.cash_user)
        line = self.env["dorevia.cash.guard.line"].with_user(self.cash_user).create(
            {
                "guard_id": guard.id,
                "projection_date": "2026-05-03",
                "budget_post_id": self.budget_post.id,
                "direction": "outflow",
                "line_type": "planned",
                "label": "WF line",
                "projected_amount": 100.0,
                "sequence": 10,
                "cash_state": "planned",
            }
        )
        guard.with_user(self.cash_user).action_validate()
        line.with_user(self.cash_user).write({"projected_amount": 120.0})
        self.assertEqual(line.projected_amount, 120.0)
