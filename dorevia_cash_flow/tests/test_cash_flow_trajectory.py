# -*- coding: utf-8 -*-

from datetime import date
from unittest.mock import patch

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestCashFlowTrajectory(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bank_journal = cls.env["account.journal"].search([("type", "=", "bank")], limit=1)
        if not cls.bank_journal:
            raise AssertionError("Aucun journal bancaire disponible pour les tests Cash Flow.")
        cls.company = cls.bank_journal.company_id
        cls.account = (
            cls.bank_journal.default_account_id
            or cls.bank_journal.payment_debit_account_id
            or cls.bank_journal.payment_credit_account_id
        )
        if not cls.account:
            raise AssertionError("Aucun compte de liquidite sur le journal bancaire.")
        cls.budget_post = cls.env["account.budget.post"].search(
            [("account_ids", "in", [cls.account.id])], limit=1
        )
        if not cls.budget_post:
            cls.budget_post = cls.env["account.budget.post"].create(
                {
                    "name": "CF Trajectory Budget Post",
                    "account_ids": [(6, 0, [cls.account.id])],
                }
            )

    def _create_week_guard(self):
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 15)):
            return self.env["dorevia.cash.guard"].create(
                {
                    "date_from": "2026-05-01",
                    "date_to": "2026-05-31",
                    "bank_journal_id": self.bank_journal.id,
                    "company_id": self.company.id,
                    "alert_threshold": 100.0,
                    "periodicity": "week",
                }
            )

    def test_action_rejects_non_week_periodicity(self):
        guard = self.env["dorevia.cash.guard"].create(
            {
                "date_from": "2026-05-01",
                "date_to": "2026-05-31",
                "bank_journal_id": self.bank_journal.id,
                "company_id": self.company.id,
                "alert_threshold": 0.0,
                "periodicity": "month",
            }
        )
        wiz = self.env["dorevia.cash.flow.trajectory.wizard"].create(
            {"guard_id": guard.id, "company_id": self.company.id}
        )
        with self.assertRaises(UserError):
            wiz.action_open_chart()

    def test_last_actual_point_matches_observed_balance(self):
        guard = self._create_week_guard()
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 15)):
            with patch.object(type(guard), "_compute_bank_balance_at_date", return_value=42.0):
                guard.action_recompute_projection()
        wiz = self.env["dorevia.cash.flow.trajectory.wizard"].create(
            {"guard_id": guard.id, "company_id": self.company.id}
        )
        action = wiz.action_open_chart()
        self.assertEqual(action.get("type"), "ir.actions.client")
        self.assertEqual(action.get("tag"), "dorevia_cash_flow_trajectory_chart")
        self.assertEqual(action.get("params", {}).get("wizard_id"), wiz.id)
        self.assertEqual(action.get("params", {}).get("trajectory_mode"), "contextualized")
        self.assertEqual(action.get("params", {}).get("contextualized_kind"), "projection")
        actual_pts = wiz.point_ids.filtered(lambda p: p.segment == "actual")
        last_actual = max(actual_pts, key=lambda p: p.anchor_date or date.min)
        self.assertEqual(last_actual.anchor_date, guard.situation_date)
        self.assertEqual(last_actual.balance, guard.observed_balance)

    def test_projected_points_match_forecast_weeks(self):
        guard = self._create_week_guard()
        self.env["dorevia.cash.guard.line"].create(
            {
                "guard_id": guard.id,
                "projection_date": "2026-05-22",
                "budget_post_id": self.budget_post.id,
                "direction": "inflow",
                "line_type": "planned",
                "label": "Test inflow",
                "projected_amount": 300.0,
                "sequence": 10,
                "cash_state": "planned",
            }
        )
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 15)):
            with patch.object(type(guard), "_compute_bank_balance_at_date", return_value=50.0):
                guard.action_recompute_projection()
        wiz = self.env["dorevia.cash.flow.trajectory.wizard"].create(
            {"guard_id": guard.id, "company_id": self.company.id}
        )
        wiz.action_open_chart()
        forecast_weeks = guard.weekly_line_ids.filtered(
            lambda w: w.period_type == "forecast"
            and w.date_from > guard.situation_date
            and w.date_to <= wiz.chart_date_end
        ).sorted("week_index")
        proj_pts = wiz.point_ids.filtered(lambda p: p.segment == "projected").sorted("sequence")
        self.assertEqual(len(proj_pts), len(forecast_weeks))
        for pt, wk in zip(proj_pts, forecast_weeks):
            self.assertEqual(pt.balance, wk.projected_balance)
            self.assertEqual(pt.anchor_date, wk.date_to)

    def test_series_metadata_v1(self):
        guard = self._create_week_guard()
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 15)):
            with patch.object(type(guard), "_compute_bank_balance_at_date", return_value=0.0):
                guard.action_recompute_projection()
        wiz = self.env["dorevia.cash.flow.trajectory.wizard"].create(
            {"guard_id": guard.id, "company_id": self.company.id}
        )
        wiz.action_open_chart()
        for p in wiz.point_ids:
            if p.segment == "actual":
                self.assertEqual(p.series_key, "current_actual")
                self.assertEqual(p.series_type, "actual")
            else:
                self.assertEqual(p.series_key, "current_projected")
                self.assertEqual(p.series_type, "projected")

    def test_comfort_threshold_amount_aligns_with_guard(self):
        """Seuil de confort exposé sur l'assistant (graph + sous-titre côté client)."""
        guard = self._create_week_guard()
        guard.comfort_threshold_rate = 25.0
        wiz = self.env["dorevia.cash.flow.trajectory.wizard"].create(
            {"guard_id": guard.id, "company_id": self.company.id}
        )
        self.assertEqual(wiz.alert_threshold, 100.0)
        self.assertEqual(wiz.comfort_threshold_amount, 125.0)

    def test_resolve_reference_guard_prefers_system_reference(self):
        """Référence cockpit / graphique : priorité à la projection ``is_system_reference``."""
        guard_sys = self._create_week_guard()
        guard_sys.write({"is_system_reference": True})
        with patch.object(fields.Date, "context_today", return_value=date(2026, 6, 12)):
            guard_work = self.env["dorevia.cash.guard"].create(
                {
                    "date_from": "2026-06-01",
                    "date_to": "2026-08-31",
                    "bank_journal_id": self.bank_journal.id,
                    "company_id": self.company.id,
                    "alert_threshold": 100.0,
                    "periodicity": "week",
                }
            )
        with patch.object(type(guard_work), "_compute_bank_balance_at_date", return_value=20.0):
            guard_work.action_recompute_projection()
        Wiz = self.env["dorevia.cash.flow.trajectory.wizard"]
        resolved = Wiz._resolve_reference_guard()
        self.assertEqual(resolved, guard_sys)

    def test_open_reference_trajectory_opens_chart_with_resolved_guard(self):
        guard = self._create_week_guard()
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 15)):
            with patch.object(type(guard), "_compute_bank_balance_at_date", return_value=0.0):
                guard.action_recompute_projection()
        action = self.env["dorevia.cash.flow.trajectory.wizard"].action_open_reference_trajectory()
        self.assertEqual(action.get("type"), "ir.actions.client")
        self.assertEqual(action.get("params", {}).get("trajectory_mode"), "reference")
        self.assertNotIn("contextualized_kind", action.get("params", {}))
        wiz = self.env["dorevia.cash.flow.trajectory.wizard"].browse(
            action["params"]["wizard_id"]
        )
        self.assertEqual(wiz.guard_id, guard)
        self.assertTrue(wiz.point_ids)

    def test_open_reference_raises_when_no_eligible_guard(self):
        Guard = self.env["dorevia.cash.guard"].search([("company_id", "=", self.company.id)])
        backup = [(g.id, g.active) for g in Guard]
        Guard.write({"active": False})
        try:
            with self.assertRaises(UserError):
                self.env["dorevia.cash.flow.trajectory.wizard"].action_open_reference_trajectory()
        finally:
            for gid, active in backup:
                self.env["dorevia.cash.guard"].browse(gid).write({"active": active})

    def test_open_reference_prefers_latest_situation_date(self):
        with patch.object(fields.Date, "context_today", return_value=date(2026, 1, 12)):
            g_old = self.env["dorevia.cash.guard"].create(
                {
                    "date_from": "2026-01-01",
                    "date_to": "2026-01-31",
                    "bank_journal_id": self.bank_journal.id,
                    "company_id": self.company.id,
                    "alert_threshold": 50.0,
                    "periodicity": "week",
                }
            )
            with patch.object(type(g_old), "_compute_bank_balance_at_date", return_value=10.0):
                g_old.action_recompute_projection()
        with patch.object(fields.Date, "context_today", return_value=date(2026, 6, 12)):
            g_new = self.env["dorevia.cash.guard"].create(
                {
                    "date_from": "2026-06-01",
                    "date_to": "2026-08-31",
                    "bank_journal_id": self.bank_journal.id,
                    "company_id": self.company.id,
                    "alert_threshold": 100.0,
                    "periodicity": "week",
                }
            )
            with patch.object(type(g_new), "_compute_bank_balance_at_date", return_value=20.0):
                g_new.action_recompute_projection()
        action = self.env["dorevia.cash.flow.trajectory.wizard"].action_open_reference_trajectory()
        wiz = self.env["dorevia.cash.flow.trajectory.wizard"].browse(
            action["params"]["wizard_id"]
        )
        self.assertEqual(wiz.guard_id, g_new)
        self.assertTrue(wiz.point_ids)

    def test_open_reference_trajectory_ignores_navigation_context(self):
        """Référence : pas de fuite active_id / default_* vers une autre projection."""
        with patch.object(fields.Date, "context_today", return_value=date(2026, 1, 12)):
            g_old = self.env["dorevia.cash.guard"].create(
                {
                    "date_from": "2026-01-01",
                    "date_to": "2026-01-31",
                    "bank_journal_id": self.bank_journal.id,
                    "company_id": self.company.id,
                    "alert_threshold": 50.0,
                    "periodicity": "week",
                }
            )
            with patch.object(type(g_old), "_compute_bank_balance_at_date", return_value=10.0):
                g_old.action_recompute_projection()
        with patch.object(fields.Date, "context_today", return_value=date(2026, 6, 12)):
            g_new = self.env["dorevia.cash.guard"].create(
                {
                    "date_from": "2026-06-01",
                    "date_to": "2026-08-31",
                    "bank_journal_id": self.bank_journal.id,
                    "company_id": self.company.id,
                    "alert_threshold": 100.0,
                    "periodicity": "week",
                }
            )
            with patch.object(type(g_new), "_compute_bank_balance_at_date", return_value=20.0):
                g_new.action_recompute_projection()
        polluted = self.env(
            context=dict(
                self.env.context,
                active_id=g_old.id,
                active_ids=[g_old.id],
                active_model="dorevia.cash.guard",
                default_guard_id=g_old.id,
            )
        )
        action = polluted["dorevia.cash.flow.trajectory.wizard"].action_open_reference_trajectory()
        wiz = self.env["dorevia.cash.flow.trajectory.wizard"].browse(action["params"]["wizard_id"])
        self.assertEqual(wiz.guard_id, g_new)

    def test_guard_cockpit_same_guard_and_points_as_reference(self):
        guard = self._create_week_guard()
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 15)):
            with patch.object(type(guard), "_compute_bank_balance_at_date", return_value=0.0):
                guard.action_recompute_projection()
        action_ref = self.env["dorevia.cash.flow.trajectory.wizard"].action_open_reference_trajectory()
        action_ck = self.env["dorevia.cash.flow.trajectory.wizard"].action_open_guard_cockpit()
        self.assertTrue(action_ck["params"].get("cockpit"))
        self.assertEqual(action_ck["params"].get("guard_id"), guard.id)
        self.assertEqual(action_ck["params"].get("trajectory_mode"), "reference")
        wiz_r = self.env["dorevia.cash.flow.trajectory.wizard"].browse(
            action_ref["params"]["wizard_id"]
        )
        wiz_c = self.env["dorevia.cash.flow.trajectory.wizard"].browse(
            action_ck["params"]["wizard_id"]
        )
        self.assertEqual(wiz_r.guard_id, wiz_c.guard_id)
        self.assertEqual(len(wiz_r.point_ids), len(wiz_c.point_ids))

    def test_action_refresh_points_from_guard_idempotent(self):
        guard = self._create_week_guard()
        with patch.object(fields.Date, "context_today", return_value=date(2026, 5, 15)):
            with patch.object(type(guard), "_compute_bank_balance_at_date", return_value=0.0):
                guard.action_recompute_projection()
        wiz = self.env["dorevia.cash.flow.trajectory.wizard"].create(
            {"guard_id": guard.id, "company_id": self.company.id}
        )
        wiz.action_open_chart()
        n = len(wiz.point_ids)
        self.assertTrue(n)
        wiz.action_refresh_points_from_guard()
        self.assertEqual(len(wiz.point_ids), n)

