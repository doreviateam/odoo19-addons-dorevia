# -*- coding: utf-8 -*-

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_glc_analytics.models.glc_constants import GLC_FUNDING_ANALYTIC_CODES


@tagged("post_install", "-at_install")
class TestGlcAnalyticSetup(TransactionCase):
    """Palier 0 — socle analytique GLC plan unique."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.group_ids += cls.env.ref("analytic.group_analytic_accounting")

    def test_single_plan_exists(self):
        plan_activites = self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")
        self.assertEqual(plan_activites.name, "GLC - Activités")

    def test_all_glc_accounts_on_single_plan(self):
        plan = self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")
        accounts = self.env["account.analytic.account"].search([("plan_id", "=", plan.id)])
        self.assertEqual(len(accounts), 11)
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
                "ADHESIONS",
                "DONS",
                "SUBVENTIONS",
                "RESSOURCES_PROPRES",
            },
        )

    def test_funding_axes_identified_by_code(self):
        plan = self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")
        funding = self.env["account.analytic.account"].search(
            [
                ("plan_id", "=", plan.id),
                ("code", "in", list(GLC_FUNDING_ANALYTIC_CODES)),
            ]
        )
        self.assertEqual(len(funding), 4)
        self.assertEqual(set(funding.mapped("code")), set(GLC_FUNDING_ANALYTIC_CODES))

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
        activites_rules = {r.business_domain: r.applicability for r in plan_activites.applicability_ids}
        self.assertEqual(activites_rules.get("bill"), "optional")
        self.assertEqual(activites_rules.get("invoice"), "optional")

    def test_no_custom_activity_model(self):
        self.assertFalse(self.env.registry.get("glc.activity"))

    def test_security_groups_exist(self):
        self.assertTrue(self.env.ref("dorevia_glc_analytics.group_glc_user"))
        self.assertTrue(self.env.ref("dorevia_glc_analytics.group_glc_manager"))
