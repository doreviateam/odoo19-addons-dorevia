# -*- coding: utf-8 -*-

from odoo import _, models
from odoo.exceptions import ValidationError


class GlcBudgetMixin(models.AbstractModel):
    _name = "glc.budget.mixin"
    _description = "Helpers budget prévisionnel GLC"

    def _glc_activites_plan(self):
        return self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")

    def _glc_financements_plan(self):
        return self.env.ref("dorevia_glc_analytics.analytic_plan_glc_financements")

    def _glc_check_analytic_account_for_line_type(self, account, line_type):
        if not account or not line_type:
            return
        activites = self._glc_activites_plan()
        financements = self._glc_financements_plan()
        if line_type == "funding":
            if account.plan_id != financements:
                raise ValidationError(
                    _("Une ligne de financement doit utiliser un compte du plan GLC - Financements.")
                )
            return
        if account.plan_id != activites:
            raise ValidationError(
                _("Une ligne de type recette ou charge doit utiliser un compte du plan GLC - Activités.")
            )
        if account.plan_id == financements:
            raise ValidationError(
                _("Les comptes du plan Financements GLC ne sont pas autorisés sur une recette ou une charge.")
            )
