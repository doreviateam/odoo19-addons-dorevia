# -*- coding: utf-8 -*-
"""Semence recette RT-PAY — cockpit détail « Payé uniquement ».

Usage (sandbox) :
  docker compose exec -T odoo odoo shell -c /etc/odoo/odoo.conf \\
    -d glc-rgl-test-import --no-http \\
    < /mnt/odoo19-addons-dorevia/dorevia_glc_analytics/scripts/recette_detail_paid_seed.py
"""
from datetime import date

AMT = {
    "rev_paid": 1100.0,
    "rev_unpaid": 820.0,
    "exp_paid": 430.0,
    "exp_unpaid": 310.0,
    "rh_paid": 520.0,
    "rh_unpaid": 610.0,
    "bank_no_inv": 275.0,
    "vir_int": 9000.0,
}


partner = env["res.partner"].search([("company_id", "in", [False, env.company.id])], limit=1)


def _pay(invoice):
    wizard = (
        env["account.payment.register"]
        .with_context(active_model="account.move", active_ids=invoice.ids)
        .create({})
    )
    wizard.action_create_payments()


def _payroll_bill(analytic, amount, invoice_date):
    payroll = env["account.account"].search(
        [("company_ids", "in", env.company.id), ("code", "=", "645200")], limit=1
    )
    inv = env["account.move"].create(
        {
            "move_type": "in_invoice",
            "partner_id": partner.id,
            "invoice_date": invoice_date,
            "date": invoice_date,
            "invoice_line_ids": [
                (
                    0,
                    0,
                    {
                        "name": "RT-PAY RH seed",
                        "quantity": 1,
                        "price_unit": amount,
                        "account_id": payroll.id,
                        "analytic_distribution": {str(analytic.id): 100},
                        "tax_ids": [(6, 0, [])],
                    },
                )
            ],
        }
    )
    inv.action_post()
    return inv


def _revenue(analytic, amount, invoice_date):
    inv = env["account.move"].create(
        {
            "move_type": "out_invoice",
            "partner_id": partner.id,
            "invoice_date": invoice_date,
            "date": invoice_date,
            "invoice_line_ids": [
                (
                    0,
                    0,
                    {
                        "name": "RT-PAY ressource seed",
                        "quantity": 1,
                        "price_unit": amount,
                        "analytic_distribution": {str(analytic.id): 100},
                        "tax_ids": [(6, 0, [])],
                    },
                )
            ],
        }
    )
    inv.action_post()
    return inv


def _expense(analytic, amount, invoice_date):
    inv = env["account.move"].create(
        {
            "move_type": "in_invoice",
            "partner_id": partner.id,
            "invoice_date": invoice_date,
            "date": invoice_date,
            "invoice_line_ids": [
                (
                    0,
                    0,
                    {
                        "name": "RT-PAY dépense seed",
                        "quantity": 1,
                        "price_unit": amount,
                        "analytic_distribution": {str(analytic.id): 100},
                        "tax_ids": [(6, 0, [])],
                    },
                )
            ],
        }
    )
    inv.action_post()
    return inv


def _bank_expense(analytic, amount, move_date, bank_journal, bank_account):
    expense = env["account.account"].search(
        [
            ("company_ids", "in", env.company.id),
            ("code", "=", "622100"),
        ],
        limit=1,
    )
    move = env["account.move"].create(
        {
            "move_type": "entry",
            "date": move_date,
            "journal_id": bank_journal.id,
            "line_ids": [
                (
                    0,
                    0,
                    {
                        "account_id": expense.id,
                        "debit": amount,
                        "credit": 0.0,
                        "analytic_distribution": {str(analytic.id): 100},
                    },
                ),
                (
                    0,
                    0,
                    {"account_id": bank_account.id, "debit": 0.0, "credit": amount},
                ),
            ],
        }
    )
    move.action_post()
    return move


def _vir_int_inflow(amount, move_date, bank_journal, bank_account):
    transfer = env["account.account"].search(
        [("company_ids", "in", env.company.id), ("code", "=", "580001")], limit=1
    )
    vir_int = env["account.analytic.account"].search([("code", "=", "VIR_INT")], limit=1)
    move = env["account.move"].create(
        {
            "move_type": "entry",
            "date": move_date,
            "journal_id": bank_journal.id,
            "line_ids": [
                (
                    0,
                    0,
                    {
                        "account_id": transfer.id,
                        "debit": 0.0,
                        "credit": amount,
                        "analytic_distribution": {str(vir_int.id): 100},
                    },
                ),
                (
                    0,
                    0,
                    {"account_id": bank_account.id, "debit": amount, "credit": 0.0},
                ),
            ],
        }
    )
    move.action_post()
    return move


# --- exécution ---
year = max(env["glc.budget"].search([]).mapped("year") + [2050]) + 1
move_date = date(year, 6, 18)
invoice_date = move_date.isoformat()

bar = env.ref("dorevia_glc_analytics.analytic_account_glc_bar")
structure = env.ref("dorevia_glc_analytics.analytic_account_glc_structure")
prestations = env.ref("dorevia_glc_analytics.analytic_account_glc_prestations")
missions = env.ref("dorevia_glc_analytics.analytic_account_glc_missions")

bank_journal = env["account.journal"].search(
    [("type", "=", "bank"), ("company_id", "=", env.company.id)], limit=1
)
bank_account = bank_journal.default_account_id
env.company.glc_default_bank_journal_id = bank_journal

_pay(_revenue(bar, AMT["rev_paid"], invoice_date))
_revenue(bar, AMT["rev_unpaid"], invoice_date)
_pay(_expense(structure, AMT["exp_paid"], invoice_date))
_expense(structure, AMT["exp_unpaid"], invoice_date)
_pay(_payroll_bill(prestations, AMT["rh_paid"], invoice_date))
_payroll_bill(prestations, AMT["rh_unpaid"], invoice_date)
_bank_expense(missions, AMT["bank_no_inv"], move_date, bank_journal, bank_account)
_vir_int_inflow(AMT["vir_int"], move_date, bank_journal, bank_account)

cockpit = env["glc.coverage.cockpit"].create(
    {
        "company_id": env.company.id,
        "date_from": date(year, 6, 1),
        "date_to": date(year, 6, 30),
        "budget_scenario": "initial",
        "reference_bank_journal_id": bank_journal.id,
    }
)
cockpit.action_refresh()

lines = cockpit.line_ids.filtered(
    lambda l: l.line_kind == "activity" and l.month_key == "%04d-06" % year
)
paid = {
    "rev": sum(lines.mapped("revenue_realized_paid")),
    "rh": sum(lines.mapped("payroll_realized_paid")),
    "exp": sum(lines.mapped("expense_realized_paid")),
}
eng = {
    "rev": sum(lines.mapped("revenue_realized")),
    "rh": sum(lines.mapped("payroll_realized")),
    "exp": sum(lines.mapped("expense_realized")),
}

print("=== RT-PAY seed OK ===")
print("Cockpit ID:", cockpit.id)
print("Période:", cockpit.date_from, "→", cockpit.date_to)
print("URL:", "http://localhost:18079/web#id=%s&model=glc.coverage.cockpit&view_type=form" % cockpit.id)
print("--- Vue complète (juin) ---")
print("Ressource:", round(eng["rev"], 2))
print("Cumul RH:", round(eng["rh"], 2))
print("Dépense:", round(eng["exp"], 2))
print("Solde:", round(eng["rev"] - eng["rh"] - eng["exp"], 2))
print("--- Vue payée uniquement ---")
print("Ressource:", round(paid["rev"], 2))
print("Cumul RH:", round(paid["rh"], 2))
print("Dépense:", round(paid["exp"], 2))
print("Solde:", round(paid["rev"] - paid["rh"] - paid["exp"], 2))
