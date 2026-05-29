# -*- coding: utf-8 -*-

from odoo import _, models
from odoo.exceptions import ValidationError

from odoo.addons.dorevia_glc_analytics.models.glc_constants import GLC_FUNDING_ANALYTIC_CODES


class GlcBudgetMixin(models.AbstractModel):
    _name = "glc.budget.mixin"
    _description = "Helpers budget prévisionnel GLC"

    def _glc_activites_plan(self):
        return self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")

    def _glc_check_analytic_account_for_line_type(self, account, line_type):
        if not account or not line_type:
            return
        activites = self._glc_activites_plan()
        if line_type == "funding":
            if account.code not in GLC_FUNDING_ANALYTIC_CODES:
                raise ValidationError(
                    _("Une ligne de financement doit utiliser un axe financement GLC.")
                )
            return
        if account.plan_id != activites:
            raise ValidationError(
                _("Une ligne de type recette ou charge doit utiliser un axe du plan GLC - Activités.")
            )
        if account.code in GLC_FUNDING_ANALYTIC_CODES:
            raise ValidationError(
                _("Les axes financement GLC ne sont pas autorisés sur une recette ou une charge.")
            )
