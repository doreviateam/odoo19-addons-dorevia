# -*- coding: utf-8 -*-

from odoo import _, models
from odoo.exceptions import ValidationError

from .glc_constants import GLC_PERCENT_TOLERANCE


class GlcSalaryMixin(models.AbstractModel):
    _name = "glc.salary.mixin"
    _description = "Helpers ventilation salariale GLC"

    def _glc_activites_plan(self):
        return self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites")

    def _glc_financements_plan(self):
        return self.env.ref("dorevia_glc_analytics.analytic_plan_glc_financements")

    def _glc_check_activity_account(self, account):
        activites = self._glc_activites_plan()
        financements = self._glc_financements_plan()
        if not account:
            return
        if account.plan_id == financements:
            raise ValidationError(
                _("Les comptes du plan Financements GLC ne sont pas autorisés en ventilation salariale.")
            )
        if account.plan_id != activites:
            raise ValidationError(
                _("L'activité doit appartenir au plan GLC - Activités.")
            )

    def _glc_floats_equal(self, left, right, tolerance=GLC_PERCENT_TOLERANCE):
        return abs((left or 0.0) - (right or 0.0)) <= tolerance
