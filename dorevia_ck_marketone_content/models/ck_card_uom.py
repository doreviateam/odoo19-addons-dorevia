# -*- coding: utf-8 -*-
from odoo import fields, models

_UOM_REFRESH_FIELDS = {
    'name', 'code', 'family', 'ratio', 'active',
    'use_for_net_quantity', 'use_for_reference_price',
}


class CkCardUom(models.Model):
    _name = 'dorevia.ck.card.uom'
    _description = 'Unité commerciale card home'
    _order = 'sequence, id'

    name = fields.Char(
        string='Libellé affiché',
        required=True,
        translate=True,
        help='Texte affiché sur la card (ex. g, kg, pièce).',
    )
    code = fields.Char(
        string='Code technique',
        required=True,
        index=True,
        help='Identifiant stable pour les migrations et l’intégration (ex. g, kg, unit).',
    )
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    family = fields.Selection(
        selection=[
            ('mass', 'Masse'),
            ('volume', 'Volume'),
            ('unit', 'Unité (pièce)'),
        ],
        string='Famille',
        required=True,
        help='Détermine les conversions possibles vers le prix de référence.',
    )
    ratio = fields.Float(
        string='Ratio vers unité de référence',
        required=True,
        default=1.0,
        help='Facteur appliqué à la quantité nette pour obtenir kg (masse) ou l (volume). '
             'Ex. 1 g → 0,001 kg ; 1 ml → 0,001 l ; 1 cl → 0,01 l.',
    )
    use_for_net_quantity = fields.Boolean(
        string='Quantité nette',
        default=True,
        help='Proposable sur la fiche produit comme unité de quantité nette.',
    )
    use_for_reference_price = fields.Boolean(
        string='Prix de référence',
        default=False,
        help='Proposable comme dénominateur du prix de référence (ex. kg, l).',
    )

    _code_uniq = models.Constraint('unique(code)', 'Le code unité card doit être unique.')

    def write(self, vals):
        templates = self.env['product.template'].sudo().search([
            '|',
            ('ck_net_quantity_uom_id', 'in', self.ids),
            ('ck_reference_price_uom_id', 'in', self.ids),
        ]) if _UOM_REFRESH_FIELDS.intersection(vals) else self.env['product.template']
        result = super().write(vals)
        if templates:
            templates._ck_refresh_home_featured_products()
        return result

    def unlink(self):
        templates = self.env['product.template'].sudo().search([
            '|',
            ('ck_net_quantity_uom_id', 'in', self.ids),
            ('ck_reference_price_uom_id', 'in', self.ids),
        ])
        result = super().unlink()
        if templates:
            templates._ck_refresh_home_featured_products()
        return result
