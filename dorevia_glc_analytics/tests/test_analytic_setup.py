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

    def test_single_plan_exists(self):
        plan_activites = self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")
        self.assertEqual(plan_activites.name, "GLC - Activités")

    def test_official_accounts_on_single_plan(self):
        plan = self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")
        accounts = self.env["account.analytic.account"].search([("plan_id", "=", plan.id)])
        official = accounts.filtered(
            lambda account: account.code
            in {
                "STRUCTURE",
                "BAR_REST",
                "PRESTA",
                "RESIDENCES",
                "DEPL_MIS",
                "LOC_PRIV",
                "LOC_RGL",
                "ADHESIONS",
                "DONS",
                "FIN_EXT",
                "FIN_INT",
            }
        )
        self.assertEqual(len(official), 11)
        codes = set(official.mapped("code"))
        self.assertEqual(
            codes,
            {
                "STRUCTURE",
                "BAR_REST",
                "PRESTA",
                "RESIDENCES",
                "DEPL_MIS",
                "LOC_PRIV",
                "LOC_RGL",
                "ADHESIONS",
                "DONS",
                "FIN_EXT",
                "FIN_INT",
            },
        )

    def test_glc_activity_types_set(self):
        structure = self.env.ref("dorevia_glc_analytics.analytic_account_glc_structure")
        bar = self.env.ref("dorevia_glc_analytics.analytic_account_glc_bar")
        residences = self.env.ref("dorevia_glc_analytics.analytic_account_glc_residences")
        adhesions = self.env.ref("dorevia_glc_analytics.analytic_account_glc_adhesions")
        fin_ext = self.env.ref("dorevia_glc_analytics.analytic_account_glc_subventions")
        fin_int = self.env.ref("dorevia_glc_analytics.analytic_account_glc_ressources_propres")
        self.assertEqual(structure.glc_activity_type, "charge")
        self.assertEqual(bar.glc_activity_type, "mixte")
        self.assertEqual(residences.glc_activity_type, "charge")
        self.assertEqual(adhesions.glc_activity_type, "recette")
        self.assertEqual(fin_ext.glc_activity_type, "recette")
        self.assertEqual(fin_ext.code, "FIN_EXT")
        self.assertEqual(fin_int.code, "FIN_INT")

    def test_no_legacy_glc_activity_types(self):
        legacy = self.env["account.analytic.account"].search(
            [("glc_activity_type", "in", ["charge_subventionnee", "financement"])]
        )
        self.assertFalse(legacy)

    def test_financements_plan_deprecated(self):
        plan = self.env.ref(
            "dorevia_glc_analytics.analytic_plan_glc_financements",
            raise_if_not_found=False,
        )
        if plan:
            accounts = self.env["account.analytic.account"].search(
                [("plan_id", "=", plan.id)]
            )
            self.assertFalse(accounts)

    def test_plan_applicability_non_blocking_palier_0(self):
        """Palier 0 : optional (non bloquant). Mandatory = Palier 1."""
        plan_activites = self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")
        activites_rules = {
            r.business_domain: r.applicability for r in plan_activites.applicability_ids
        }
        self.assertEqual(activites_rules.get("bill"), "optional")
        self.assertEqual(activites_rules.get("invoice"), "optional")

    def test_no_custom_activity_model(self):
        self.assertFalse(self.env.registry.get("glc.activity"))

    def test_security_groups_exist(self):
        self.assertTrue(self.env.ref("dorevia_glc_analytics.group_glc_user"))
        self.assertTrue(self.env.ref("dorevia_glc_analytics.group_glc_manager"))
