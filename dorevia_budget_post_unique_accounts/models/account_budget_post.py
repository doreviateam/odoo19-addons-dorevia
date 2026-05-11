# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountBudgetPost(models.Model):
    _inherit = "account.budget.post"

    active = fields.Boolean(
        string="Actif",
        default=True,
        help=(
            "Poste budgétaire pris en compte pour l’unicité des comptes. "
            "Archiver un poste permet de rattacher ses comptes à un autre poste actif."
        ),
    )

    @api.constrains("account_ids", "active", "company_id")
    def _check_account_unique_among_active_posts(self):
        """Un même compte ne peut être lié qu’à un seul poste budgétaire actif (par société)."""
        for post in self:
            if not post.active or not post.account_ids:
                continue
            for account in post.account_ids:
                other = self.env["account.budget.post"].search(
                    [
                        ("id", "!=", post.id),
                        ("company_id", "=", post.company_id.id),
                        ("active", "=", True),
                        ("account_ids", "in", account.ids),
                    ],
                    limit=1,
                )
                if other:
                    raise ValidationError(
                        _(
                            "Ce compte comptable (%(code)s) est déjà associé au poste "
                            "budgétaire actif « %(post)s ». Un compte ne peut appartenir "
                            "qu’à un seul poste budgétaire actif. Archivez l’autre poste "
                            "ou retirez le compte de celui-ci."
                        )
                        % {"code": account.code or account.name, "post": other.name}
                    )
