# -*- coding: utf-8 -*-

from odoo import _, models
from odoo.exceptions import ValidationError

from odoo.addons.dorevia_glc_analytics.models.glc_constants import (
    GLC_FUNDING_ANALYTIC_CODES,
)


class GlcBudgetMixin(models.AbstractModel):
    _name = "glc.budget.mixin"
    _description = "Helpers budget prévisionnel GLC"

    def _glc_activites_plan(self):
        return self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")

    def _glc_check_analytic_account_for_line_type(self, account, line_type):
        if not account or not line_type:
            return
        activites = self._glc_activites_plan()
        if account.plan_id != activites:
            raise ValidationError(
                _("Les lignes budgétaires GLC doivent utiliser un compte du plan GLC - Activités.")
            )
        is_funding = account.code in GLC_FUNDING_ANALYTIC_CODES
        if line_type == "funding":
            if not is_funding:
                raise ValidationError(
                    _("Une ligne de financement doit utiliser un axe ressource GLC (ex. FIN_EXT, FIN_INT).")
                )
            return
        if is_funding:
            raise ValidationError(
                _("Les axes financement / ressources ne sont pas autorisés sur une recette ou une charge.")
            )
