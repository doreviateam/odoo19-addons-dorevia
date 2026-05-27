# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .glc_constants import GLC_FUNDING_CODES


class GlcAccountFundingRule(models.Model):
    """Mapping explicite compte comptable → financement GLC (contrôle A3)."""

    _name = "glc.account.funding.rule"
    _description = "Règle compte comptable → financement GLC"
    _order = "company_id, account_id"

    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    account_id = fields.Many2one(
        "account.account",
        string="Compte comptable",
        required=True,
        check_company=True,
        domain="[('account_type', 'in', ('income', 'income_other'))]",
    )
    funding_code = fields.Selection(
        selection=[(code, code.replace("_", " ").title()) for code in GLC_FUNDING_CODES],
        string="Financement attendu",
        required=True,
    )
    funding_analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string="Compte analytique financement",
        compute="_compute_funding_analytic_account_id",
        store=True,
        readonly=False,
        check_company=True,
    )
    active = fields.Boolean(default=True)

    _glc_account_funding_rule_uniq = models.Constraint(
        "unique(company_id, account_id)",
        "Une seule règle de financement par compte comptable et société.",
    )

    @api.depends("funding_code", "company_id")
    def _compute_funding_analytic_account_id(self):
        AnalyticAccount = self.env["account.analytic.account"]
        for rule in self:
            if not rule.funding_code:
                rule.funding_analytic_account_id = False
                continue
            rule.funding_analytic_account_id = AnalyticAccount.search(
                [
                    ("code", "=", rule.funding_code),
                    ("company_id", "in", [False, rule.company_id.id]),
                ],
                limit=1,
            )

    @api.constrains("funding_code", "funding_analytic_account_id")
    def _check_funding_analytic_account(self):
        for rule in self:
            if not rule.funding_analytic_account_id:
                raise ValidationError(
                    _(
                        "Aucun compte analytique GLC trouvé pour le financement « %(code)s ».",
                        code=rule.funding_code,
                    )
                )
