# -*- coding: utf-8 -*-

from datetime import date

from odoo.tests import tagged

from .test_coverage_cockpit import TestGlcCoverageCockpit


@tagged("post_install", "-at_install")
class TestGlcCoverageCockpitTreasury(TestGlcCoverageCockpit):
    """Palier 5 — lecture trésorerie compte bancaire de référence (TREF)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.bank_journal = cls.env["account.journal"].search(
            [("type", "=", "bank"), ("company_id", "=", cls.env.company.id)],
            limit=1,
        )
        if not cls.bank_journal:
            raise AssertionError("Aucun journal bancaire disponible pour les tests TREF.")
        cls.bank_account = (
            cls.bank_journal.default_account_id
            or cls.bank_journal.payment_debit_account_id
            or cls.bank_journal.payment_credit_account_id
        )
        if not cls.bank_account:
            raise AssertionError("Aucun compte 512 sur le journal bancaire de test.")
        cls.env.company.write({"glc_default_bank_journal_id": cls.bank_journal.id})
        cls.suspense_account = cls.env["account.account"].search(
            [
                ("company_ids", "in", cls.env.company.id),
                ("code", "=", "471000"),
            ],
            limit=1,
        )
        if not cls.suspense_account:
            cls.suspense_account = cls.env["account.account"].create(
                {
                    "name": "Compte transitoire test TREF",
                    "code": "471000",
                    "account_type": "asset_current",
                }
            )
        cls.bank_journal_b, cls.bank_account_b = cls._create_secondary_bank_journal(
            code="512900",
            journal_code="LVT",
        )

    @classmethod
    def _create_secondary_bank_journal(cls, code, journal_code):
        account = cls.env["account.account"].search(
            [
                ("company_ids", "in", cls.env.company.id),
                ("code", "=", code),
            ],
            limit=1,
        )
        if not account:
            account = cls.env["account.account"].create(
                {
                    "name": "Compte bancaire secondaire test %s" % code,
                    "code": code,
                    "account_type": "asset_cash",
                }
            )
        journal = cls.env["account.journal"].search(
            [
                ("type", "=", "bank"),
                ("code", "=", journal_code),
                ("company_id", "=", cls.env.company.id),
            ],
            limit=1,
        )
        if not journal:
            journal = cls.env["account.journal"].create(
                {
                    "name": "Journal bancaire secondaire test",
                    "type": "bank",
                    "code": journal_code,
                    "company_id": cls.env.company.id,
                    "default_account_id": account.id,
                }
            )
        else:
            journal.default_account_id = account
        return journal, account

    def _create_bank_move(
        self,
        bank_journal,
        bank_account,
        amount,
        move_date,
        counterpart_account,
        inflow=True,
    ):
        amount = abs(amount)
        if inflow:
            line_vals = [
                (0, 0, {"account_id": bank_account.id, "debit": amount, "credit": 0.0}),
                (
                    0,
                    0,
                    {"account_id": counterpart_account.id, "debit": 0.0, "credit": amount},
                ),
            ]
        else:
            line_vals = [
                (
                    0,
                    0,
                    {"account_id": counterpart_account.id, "debit": amount, "credit": 0.0},
                ),
                (0, 0, {"account_id": bank_account.id, "debit": 0.0, "credit": amount}),
            ]
        move = self.env["account.move"].create(
            {
                "move_type": "entry",
                "date": move_date,
                "journal_id": bank_journal.id,
                "company_id": self.env.company.id,
                "line_ids": line_vals,
            }
        )
        move.action_post()
        return move

    def _create_internal_transfer(
        self,
        source_journal,
        source_account,
        dest_account,
        amount,
        move_date,
    ):
        amount = abs(amount)
        move = self.env["account.move"].create(
            {
                "move_type": "entry",
                "date": move_date,
                "journal_id": source_journal.id,
                "company_id": self.env.company.id,
                "line_ids": [
                    (0, 0, {"account_id": dest_account.id, "debit": amount, "credit": 0.0}),
                    (0, 0, {"account_id": source_account.id, "debit": 0.0, "credit": amount}),
                ],
            }
        )
        move.action_post()
        return move

    def _get_or_create_transfer_account(self, code="580001"):
        account = self.env["account.account"].search(
            [
                ("company_ids", "in", self.env.company.id),
                ("code", "=", code),
            ],
            limit=1,
        )
        if not account:
            account = self.env["account.account"].create(
                {
                    "name": "Transfert de liquidités test",
                    "code": code,
                    "account_type": "asset_current",
                }
            )
        return account

    def _get_or_create_vir_int_account(self):
        account = self.env["account.analytic.account"].search(
            [
                ("code", "=", "VIR_INT"),
                ("company_id", "in", [False, self.env.company.id]),
            ],
            limit=1,
        )
        if account:
            return account
        plan = self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")
        return self.env["account.analytic.account"].create(
            {
                "name": "Virement interne",
                "code": "VIR_INT",
                "plan_id": plan.id,
                "glc_activity_type": "mixte",
            }
        )

    def _create_internal_transfer_via_580(
        self,
        bank_journal,
        bank_account,
        transfer_account,
        vir_int_account,
        amount,
        move_date,
        outflow=True,
    ):
        amount = abs(amount)
        transfer_line = {
            "account_id": transfer_account.id,
            "analytic_distribution": {str(vir_int_account.id): 100},
        }
        bank_line = {"account_id": bank_account.id}
        if outflow:
            transfer_line.update({"debit": amount, "credit": 0.0})
            bank_line.update({"debit": 0.0, "credit": amount})
        else:
            transfer_line.update({"debit": 0.0, "credit": amount})
            bank_line.update({"debit": amount, "credit": 0.0})
        move = self.env["account.move"].create(
            {
                "move_type": "entry",
                "date": move_date,
                "journal_id": bank_journal.id,
                "company_id": self.env.company.id,
                "line_ids": [(0, 0, transfer_line), (0, 0, bank_line)],
            }
        )
        move.action_post()
        return move

    def _create_treasury_cockpit(self, year, month=6, bank_journal=None, skip_auto_refresh=False):
        date_from, date_to = self._month_bounds(year, month)
        env = self.env["glc.coverage.cockpit"]
        if skip_auto_refresh:
            env = env.with_context(glc_cockpit_auto_refreshing=True)
        values = {
            "company_id": self.env.company.id,
            "date_from": date_from,
            "date_to": date_to,
            "budget_scenario": "initial",
            "reference_bank_journal_id": (bank_journal or self.bank_journal).id,
        }
        return env.create(values)

    def test_tref01_customer_inflow_and_revenue_independent(self):
        """TREF-01 — encaissement + recette BAR : trésorerie et exploitation."""
        year = self._next_test_year()
        move_date = date(year, 6, 15)
        self._create_revenue_on_account(
            self.bar, 1000.0, invoice_date=move_date.isoformat()
        )
        self._create_bank_move(
            self.bank_journal,
            self.bank_account,
            800.0,
            move_date,
            self.suspense_account,
            inflow=True,
        )
        cockpit = self._create_treasury_cockpit(year)
        cockpit.action_refresh()

        self.assertAlmostEqual(cockpit.activity_revenue_realized, 1000.0)
        self.assertAlmostEqual(cockpit.treasury_inflow, 800.0)
        self.assertAlmostEqual(cockpit.treasury_outflow, 0.0)
        self.assertAlmostEqual(cockpit.treasury_net, 800.0)
        self.assertTrue(cockpit.treasury_has_data)

    def test_tref02_supplier_outflow_and_expense_independent(self):
        """TREF-02 — paiement fournisseur + dépense analytique."""
        year = self._next_test_year()
        move_date = date(year, 6, 20)
        self._create_expense_analytic_line(
            self.structure, 300.0, invoice_date=move_date.isoformat()
        )
        self._create_bank_move(
            self.bank_journal,
            self.bank_account,
            250.0,
            move_date,
            self.suspense_account,
            inflow=False,
        )
        cockpit = self._create_treasury_cockpit(year)
        cockpit.action_refresh()

        self.assertAlmostEqual(cockpit.general_expenses_realized, 300.0)
        self.assertAlmostEqual(cockpit.treasury_outflow, 250.0)
        self.assertAlmostEqual(cockpit.treasury_inflow, 0.0)
        self.assertAlmostEqual(cockpit.treasury_net, -250.0)

    def test_tref03_internal_transfer_excluded_from_exploitation(self):
        """TREF-03 — virement interne visible en trésorerie, hors KPI exploitation."""
        year = self._next_test_year()
        move_date = date(year, 6, 10)
        self._create_internal_transfer(
            self.bank_journal,
            self.bank_account,
            self.bank_account_b,
            500.0,
            move_date,
        )
        cockpit = self._create_treasury_cockpit(year)
        cockpit.action_refresh()

        self.assertAlmostEqual(cockpit.activity_revenue_realized, 0.0)
        self.assertAlmostEqual(cockpit.payroll_realized, 0.0)
        self.assertAlmostEqual(cockpit.general_expenses_realized, 0.0)
        self.assertAlmostEqual(cockpit.treasury_outflow, 500.0)
        self.assertAlmostEqual(cockpit.treasury_internal_outflow, 500.0)
        self.assertAlmostEqual(cockpit.treasury_inflow, 0.0)

        cockpit_b = self._create_treasury_cockpit(
            year, bank_journal=self.bank_journal_b, skip_auto_refresh=True
        )
        cockpit_b.action_refresh()
        self.assertAlmostEqual(cockpit_b.treasury_inflow, 500.0)
        self.assertAlmostEqual(cockpit_b.treasury_internal_inflow, 500.0)
        self.assertAlmostEqual(cockpit_b.activity_revenue_realized, 0.0)

    def test_tref06_internal_transfer_580_with_vir_int_analytic(self):
        """TREF-06 — 580001 + axe analytique : sortie → dépense, entrée → recette."""
        year = self._next_test_year()
        move_date = date(year, 6, 11)
        transfer_account = self._get_or_create_transfer_account()
        vir_int = self._get_or_create_vir_int_account()
        self._create_internal_transfer_via_580(
            self.bank_journal,
            self.bank_account,
            transfer_account,
            vir_int,
            750.0,
            move_date,
            outflow=True,
        )
        cockpit = self._create_treasury_cockpit(year)
        cockpit.action_refresh()

        self.assertAlmostEqual(cockpit.activity_revenue_realized, 0.0)
        self.assertAlmostEqual(cockpit.payroll_realized, 0.0)
        self.assertAlmostEqual(cockpit.general_expenses_realized, 750.0)
        self.assertAlmostEqual(cockpit.treasury_outflow, 750.0)
        self.assertAlmostEqual(cockpit.treasury_internal_outflow, 750.0)
        self.assertEqual(len(cockpit.treasury_line_ids), 1)

        detail_lines = cockpit.line_ids.filtered(
            lambda line: line.analytic_account_id == vir_int
            and line.month_key == "%04d-%02d" % (year, 6)
        )
        self.assertEqual(len(detail_lines), 1)
        self.assertAlmostEqual(detail_lines.revenue_realized, 0.0)
        self.assertAlmostEqual(detail_lines.expense_realized, 750.0)

    def test_tref07_internal_transfer_inflow_on_funding_axis(self):
        """TREF-07 — entrée 580 qualifiée financement → recette cockpit."""
        year = self._next_test_year()
        move_date = date(year, 6, 18)
        transfer_account = self._get_or_create_transfer_account()
        funding = self.env.ref("dorevia_glc_analytics.analytic_account_glc_ressources_propres")
        self._create_internal_transfer_via_580(
            self.bank_journal,
            self.bank_account,
            transfer_account,
            funding,
            9000.0,
            move_date,
            outflow=False,
        )
        cockpit = self._create_treasury_cockpit(year)
        cockpit.action_refresh()

        self.assertAlmostEqual(cockpit.funding_realized, 9000.0)
        self.assertAlmostEqual(cockpit.resources_realized, 9000.0)
        detail_lines = cockpit.line_ids.filtered(
            lambda line: line.analytic_account_id == funding
            and line.month_key == "%04d-%02d" % (year, 6)
        )
        self.assertEqual(len(detail_lines), 1)
        self.assertAlmostEqual(detail_lines.revenue_realized, 9000.0)
        self.assertAlmostEqual(detail_lines.expense_realized, 0.0)

    def test_tref04_payroll_outflow(self):
        """TREF-04 — paie 645 + sortie trésorerie."""
        year = self._next_test_year()
        move_date = date(year, 6, 25)
        self._create_payroll_on_account(
            self.structure,
            154.0,
            invoice_date=move_date.isoformat(),
            payroll_code="645200",
        )
        self._create_bank_move(
            self.bank_journal,
            self.bank_account,
            154.0,
            move_date,
            self.suspense_account,
            inflow=False,
        )
        cockpit = self._create_treasury_cockpit(year)
        cockpit.action_refresh()

        self.assertAlmostEqual(cockpit.payroll_realized, 154.0)
        self.assertAlmostEqual(cockpit.treasury_outflow, 154.0)
        self.assertAlmostEqual(cockpit.treasury_net, -154.0)

    def test_tref05_reference_bank_change_preserves_exploitation_kpis(self):
        """TREF-05 — changement compte de référence : exploitation inchangée."""
        year = self._next_test_year()
        move_date = date(year, 6, 12)
        self._create_revenue_on_account(
            self.bar, 2000.0, invoice_date=move_date.isoformat()
        )
        self._create_bank_move(
            self.bank_journal,
            self.bank_account,
            400.0,
            move_date,
            self.suspense_account,
            inflow=True,
        )
        self._create_bank_move(
            self.bank_journal_b,
            self.bank_account_b,
            700.0,
            move_date,
            self.suspense_account,
            inflow=True,
        )

        cockpit_a = self._create_treasury_cockpit(year, skip_auto_refresh=True)
        cockpit_a.action_refresh()
        exploitation_a = {
            "activity_revenue_realized": cockpit_a.activity_revenue_realized,
            "payroll_realized": cockpit_a.payroll_realized,
            "general_expenses_realized": cockpit_a.general_expenses_realized,
            "resources_realized": cockpit_a.resources_realized,
        }
        self.assertAlmostEqual(cockpit_a.treasury_inflow, 400.0)

        cockpit_b = self._create_treasury_cockpit(
            year, bank_journal=self.bank_journal_b, skip_auto_refresh=True
        )
        cockpit_b.action_refresh()
        exploitation_b = {
            "activity_revenue_realized": cockpit_b.activity_revenue_realized,
            "payroll_realized": cockpit_b.payroll_realized,
            "general_expenses_realized": cockpit_b.general_expenses_realized,
            "resources_realized": cockpit_b.resources_realized,
        }
        self.assertAlmostEqual(cockpit_b.treasury_inflow, 700.0)
        self.assertDictEqual(exploitation_a, exploitation_b)

    def test_reference_bank_journal_persisted_on_refresh(self):
        """Palier 5 — filtre compte bancaire conservé au refresh."""
        year = self._next_test_year()
        cockpit = self._create_treasury_cockpit(
            year, bank_journal=self.bank_journal_b, skip_auto_refresh=True
        )
        cockpit.write({"date_from": date(year, 6, 1), "date_to": date(year, 6, 30)})
        cockpit.action_refresh()
        self.assertEqual(cockpit.reference_bank_journal_id, self.bank_journal_b)

    def test_default_reference_bank_from_company(self):
        """Palier 5 — défaut société = journal compte courant GLC."""
        cockpit = self.env["glc.coverage.cockpit"].with_context(
            glc_cockpit_auto_refreshing=True
        ).create(
            {
                "company_id": self.env.company.id,
                "date_from": date(self.test_year, 1, 1),
                "date_to": date(self.test_year, 1, 31),
                "budget_scenario": "initial",
            }
        )
        self.assertEqual(
            cockpit.reference_bank_journal_id,
            self.env.company.glc_default_bank_journal_id,
        )
        self.assertEqual(cockpit.reference_bank_account_id, self.bank_account)
