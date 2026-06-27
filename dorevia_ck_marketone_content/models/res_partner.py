# -*- coding: utf-8 -*-
from odoo import fields, models


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
        help='Libellé marketing libre (ex. Abymes, Guadeloupe). Non dérivé de l’adresse Odoo.',
    )
