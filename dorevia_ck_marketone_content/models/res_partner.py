# -*- coding: utf-8 -*-
from odoo import fields, models

_CK_PRODUCER_IMAGE_SIZES = {
    'image_128': 128,
    'image_256': 256,
    'image_512': 512,
    'image_1024': 1024,
    'image_1920': 1920,
}


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
    ck_producer_website_image = fields.Image(
        string='Photo producteur (site web)',
        max_width=1920,
        max_height=1920,
        help='Visuel publié sur /producteurs et la fiche producteur. '
             'Indépendant du logo société (avatar contact).',
    )

    def get_ck_producer_url(self):
        """URL publique canonique de la fiche producteur."""
        self.ensure_one()
        return f"/producteur/{self.env['ir.http']._slug(self)}"

    def get_ck_producer_image_url(self, field='image_512'):
        """URL image publique — champ ck_producer_website_image, pas le logo contact."""
        self.ensure_one()
        if field not in _CK_PRODUCER_IMAGE_SIZES:
            field = 'image_512'
        if not self.ck_producer_website_image:
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
