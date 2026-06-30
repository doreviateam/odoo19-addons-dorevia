# -*- coding: utf-8 -*-
from odoo import fields, models

_CK_PRODUCER_IMAGE_FIELDS = frozenset({
    'image_128', 'image_256', 'image_512', 'image_1024', 'image_1920',
})


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ck_is_producer = fields.Boolean(
        string='Producteur CK',
        help='Identifie les partenaires éligibles comme producteur sur les fiches produit.',
    )
    ck_producer_short_description = fields.Text(
        string='Accroche producteur',
        translate=True,
        help='Texte court affiché dans le bloc producteur de la fiche produit.',
    )
    ck_producer_story_html = fields.Html(
        string='Histoire producteur',
        translate=True,
        sanitize_overridable=True,
        sanitize_attributes=False,
        help='Contenu long pour la future fiche producteur dédiée.',
    )
    ck_producer_location_label = fields.Char(
        string='Libellé géographique',
        translate=True,
        help="Libellé marketing libre (ex. Abymes, Guadeloupe). Non dérivé de l'adresse Odoo.",
    )

    def get_ck_producer_url(self):
        """URL publique canonique de la fiche producteur."""
        self.ensure_one()
        return f"/producteur/{self.env['ir.http']._slug(self)}"

    def get_ck_producer_image_url(self, field='image_512'):
        """URL image publique — contourne le placeholder /web/image pour les visiteurs."""
        self.ensure_one()
        if field not in _CK_PRODUCER_IMAGE_FIELDS:
            field = 'image_512'
        if not self.image_1920:
            return ''
        return f'/ck/producteur/{self.id}/image/{field}'

    def get_ck_producer_products(self):
        """Produits CK publiés et vendables liés à ce producteur."""
        self.ensure_one()
        return self.env['product.template'].sudo().search([
            ('ck_producer_id', '=', self.id),
            ('is_published', '=', True),
            ('sale_ok', '=', True),
        ], order='website_sequence asc, name asc')
