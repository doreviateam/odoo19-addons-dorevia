# -*- coding: utf-8 -*-

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestGlcAnalyticSetup(TransactionCase):
    """Palier 0 — socle analytique GLC."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.group_ids += cls.env.ref("analytic.group_analytic_accounting")

    def test_plans_exist(self):
        plan_activites = self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")
        plan_financements = self.env.ref("dorevia_glc_analytics.analytic_plan_glc_financements")
        self.assertEqual(plan_activites.name, "GLC - Activités")
        self.assertEqual(plan_financements.name, "GLC - Financements")

    def test_activity_accounts_count_and_codes(self):
        plan = self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")
        accounts = self.env["account.analytic.account"].search([("plan_id", "=", plan.id)])
        self.assertEqual(len(accounts), 7)
        codes = set(accounts.mapped("code"))
        self.assertEqual(
            codes,
            {
                "STRUCTURE",
                "BAR",
                "PRESTATIONS",
                "RESIDENCES",
                "MISSIONS",
                "PRIVATISATIONS",
                "LOCATION_RADIO",
            },
        )

    def test_financement_accounts_count_and_codes(self):
        plan = self.env.ref("dorevia_glc_analytics.analytic_plan_glc_financements")
        accounts = self.env["account.analytic.account"].search([("plan_id", "=", plan.id)])
        self.assertEqual(len(accounts), 4)
        codes = set(accounts.mapped("code"))
        self.assertEqual(codes, {"ADHESIONS", "DONS", "SUBVENTIONS", "RESSOURCES_PROPRES"})

    def test_glc_activity_types_set(self):
        structure = self.env.ref("dorevia_glc_analytics.analytic_account_glc_structure")
        bar = self.env.ref("dorevia_glc_analytics.analytic_account_glc_bar")
        adhesions = self.env.ref("dorevia_glc_analytics.analytic_account_glc_adhesions")
        self.assertEqual(structure.glc_activity_type, "charge")
        self.assertEqual(bar.glc_activity_type, "mixte")
        self.assertEqual(adhesions.glc_activity_type, "financement")

    def test_plan_applicability_non_blocking_palier_0(self):
        """Palier 0 : optional (non bloquant). Mandatory = Palier 1."""
        plan_activites = self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")
        plan_financements = self.env.ref("dorevia_glc_analytics.analytic_plan_glc_financements")
        activites_rules = {r.business_domain: r.applicability for r in plan_activites.applicability_ids}
        financements_rules = {r.business_domain: r.applicability for r in plan_financements.applicability_ids}
        self.assertEqual(activites_rules.get("bill"), "optional")
        self.assertEqual(activites_rules.get("invoice"), "optional")
        self.assertEqual(financements_rules.get("invoice"), "optional")
        self.assertEqual(financements_rules.get("bill"), "unavailable")

    def test_no_custom_activity_model(self):
        self.assertFalse(self.env.registry.get("glc.activity"))

    def test_security_groups_exist(self):
        self.assertTrue(self.env.ref("dorevia_glc_analytics.group_glc_user"))
        self.assertTrue(self.env.ref("dorevia_glc_analytics.group_glc_manager"))
