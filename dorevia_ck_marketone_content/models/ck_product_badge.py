# -*- coding: utf-8 -*-
from odoo import api, fields, models


class CkProductBadge(models.Model):
    _name = 'ck.product.badge'
    _description = 'Badge qualifié fiche produit CK'
    _order = 'sequence, name, id'

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True, index=True)
    badge_type = fields.Selection(
        selection=[
            ('origin', 'Origine'),
            ('ingredient', 'Ingrédient'),
            ('producer', 'Producteur'),
            ('platform', 'Plateforme'),
            ('dietary', 'Régime alimentaire'),
            ('quality', 'Qualité'),
        ],
        required=True,
        default='quality',
    )
    icon = fields.Char(
        string='Icône',
        help='Emoji ou classe CSS affichée avant le libellé.',
    )
    sequence = fields.Integer(default=10)
    requires_validation = fields.Boolean(
        string='Validation requise',
        help='Badge nécessitant une preuve formelle avant publication.',
    )
    is_sensitive_claim = fields.Boolean(
        string='Allégation sensible',
        help='Allégation réglementée (bio, sans gluten, etc.).',
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Le code technique du badge doit être unique.'),
    ]

    @api.constrains('code')
    def _check_code_normalized(self):
        for badge in self:
            code = (badge.code or '').strip()
            if not code:
                continue
            duplicate = self.search([
                ('id', '!=', badge.id),
                ('code', '=ilike', code),
            ], limit=1)
            if duplicate:
                raise models.ValidationError(
                    'Un badge existe déjà avec le code « %s ».' % code
                )
