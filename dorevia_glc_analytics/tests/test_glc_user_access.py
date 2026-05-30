# -*- coding: utf-8 -*-

import uuid
from datetime import date

from odoo.exceptions import AccessError
from odoo.fields import Command
from odoo.tests import tagged

from .test_coverage_cockpit_quality import TestGlcCoverageCockpitQuality


@tagged("post_install", "-at_install")
class TestGlcUserAccess(TestGlcCoverageCockpitQuality):
    """Lot A suite — accès Utilisateur GLC non administrateur."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.glc_controller = cls._create_glc_controller_user()
        cls.analytic_only_user = cls._create_analytic_only_user()

    @classmethod
    def _create_glc_controller_user(cls):
        """Profil cible : Utilisateur GLC sans droits comptables étendus."""
        return cls.env["res.users"].create(
            {
                "name": "Contrôleur GLC Test",
                "login": "glc_controller_%s" % uuid.uuid4().hex[:8],
                "group_ids": [
                    Command.set(
                        [
                            cls.env.ref("base.group_user").id,
                            cls.env.ref("dorevia_glc_analytics.group_glc_user").id,
                        ]
                    )
                ],
            }
        )

    @classmethod
    def _create_analytic_only_user(cls):
        """Profil insuffisant : analytique sans lecture comptable."""
        return cls.env["res.users"].create(
            {
                "name": "Analytique seul Test",
                "login": "glc_analytic_only_%s" % uuid.uuid4().hex[:8],
                "group_ids": [
                    Command.set(
                        [
                            cls.env.ref("base.group_user").id,
                            cls.env.ref("analytic.group_analytic_accounting").id,
                        ]
                    )
                ],
            }
        )

    def _cockpit_env(self, user):
        return self.env(user=user)["glc.coverage.cockpit"]

    def test_glc_user_can_open_and_refresh_cockpit(self):
        """Utilisateur GLC — ouverture et refresh sans erreur."""
        year = self._next_test_year()
        self._create_revenue_on_account(self.bar, 1500.0, invoice_date="%s-06-10" % year)

        cockpit = self._cockpit_env(self.glc_controller).create(
            {
                "company_id": self.env.company.id,
                "date_from": date(year, 6, 1),
                "date_to": date(year, 6, 30),
            }
        )
        cockpit.action_refresh()

        self.assertTrue(cockpit.is_refreshed)
        self.assertTrue(cockpit.line_ids)
        self.assertAlmostEqual(cockpit.resources_realized, 1500.0)

    def test_glc_user_can_read_detail_lines_after_refresh(self):
        """Utilisateur GLC — lecture des lignes calculées (ACL lecture seule)."""
        year = self._next_test_year()
        self._create_revenue_on_account(self.bar, 800.0, invoice_date="%s-06-12" % year)
        cockpit = self._cockpit_env(self.glc_controller).create(
            {
                "company_id": self.env.company.id,
                "date_from": date(year, 6, 1),
                "date_to": date(year, 6, 30),
            }
        )
        cockpit.action_refresh()
        bar_lines = cockpit.line_ids.filtered(
            lambda line: line.analytic_account_id == self.bar
        )
        self.assertTrue(bar_lines)
        self.assertAlmostEqual(sum(bar_lines.mapped("revenue_realized")), 800.0)

    def test_glc_user_drilldown_q1_q2_q3_actions(self):
        """Utilisateur GLC — actions drill-down Q1/Q2/Q3 retournées."""
        year = self._next_test_year()
        invoice_date = "%s-06-18" % year
        self._create_revenue_on_account(self.bar, 600.0, invoice_date=invoice_date)
        self._create_invoice_one_line(
            price_unit=400.0,
            move_type="out_invoice",
            invoice_date=invoice_date,
            tax_ids=[Command.clear()],
            post=True,
        )
        cockpit = self._cockpit_env(self.glc_controller).create(
            {
                "company_id": self.env.company.id,
                "date_from": date(year, 6, 1),
                "date_to": date(year, 6, 30),
            }
        )
        cockpit.action_refresh()

        q1_lines = cockpit.action_open_quality_lines_to_qualify()
        self.assertEqual(q1_lines["res_model"], "account.move.line")
        q2_customer = cockpit.action_open_unreconciled_customer_lines()
        self.assertEqual(q2_customer["res_model"], "account.move.line")
        q3_open = cockpit.action_open_payment_customer_open()
        self.assertEqual(q3_open["res_model"], "account.move")

    def test_glc_user_cannot_mutate_cockpit_lines_manually(self):
        """Utilisateur GLC — pas de CRUD manuel sur les lignes calculées."""
        year = self._next_test_year()
        self._create_revenue_on_account(self.bar, 500.0, invoice_date="%s-06-05" % year)
        cockpit = self._cockpit_env(self.glc_controller).create(
            {
                "company_id": self.env.company.id,
                "date_from": date(year, 6, 1),
                "date_to": date(year, 6, 30),
            }
        )
        cockpit.action_refresh()
        line = cockpit.line_ids[:1]
        self.assertTrue(line)

        line_model = self.env(user=self.glc_controller)["glc.coverage.cockpit.line"]
        with self.assertRaises(AccessError):
            line_model.create(
                {
                    "cockpit_id": cockpit.id,
                    "line_kind": "activity",
                    "period_date": date(year, 6, 1),
                    "month_key": "%04d-06" % year,
                    "activity_label": "Injection manuelle",
                }
            )
        line_as_user = line.with_user(self.glc_controller)
        with self.assertRaises(AccessError):
            line_as_user.write({"activity_label": "Modification interdite"})
        with self.assertRaises(AccessError):
            line_as_user.unlink()

    def test_glc_user_has_account_readonly_via_group(self):
        """Doctrine — Utilisateur GLC inclut lecture comptable (groupe implicite)."""
        self.assertTrue(
            self.glc_controller.has_group("account.group_account_readonly")
        )

    def test_account_readonly_required_to_read_move_lines(self):
        """Sans lecture comptable, Q2/Q3 et agrégations sur account.move.line échouent."""
        year = self._next_test_year()
        invoice = self._create_revenue_on_account(
            self.bar, 1200.0, invoice_date="%s-06-14" % year
        )
        domain = [("move_id", "=", invoice.id)]
        self.assertGreater(
            self.env(user=self.glc_controller)["account.move.line"].search_count(
                domain
            ),
            0,
        )
        with self.assertRaises(AccessError):
            self.env(user=self.analytic_only_user)["account.move.line"].search_count(
                domain
            )
