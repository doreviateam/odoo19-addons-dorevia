# -*- coding: utf-8 -*-
from odoo import models

from ..runtime import is_ck_preprod_runtime_active


class Website(models.Model):
    _inherit = "website"

    def ck_preprod_guard_runtime_active(self):
        """Exposé QWeb — bandeau/CTA uniquement si préprod CK runtime."""
        try:
            from odoo.http import request  # noqa: PLC0415 — import Odoo runtime

            req = request
        except Exception:
            req = None
        return is_ck_preprod_runtime_active(self.env, req)
