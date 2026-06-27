# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, tools
from odoo.exceptions import ValidationError
from odoo.tools import html2plaintext

_logger = logging.getLogger(__name__)

CK_ECOMMERCE_LEAD_MAX_CHARS = 255


FEATURED_REFRESH_FIELDS = {
    'name',
    'public_categ_ids',
    'ck_is_featured',
    'is_published',
    'website_published',
    'website_sequence',
    'website_ribbon_id',
    'sale_ok',
    'list_price',
    'image_1920',
    'image_512',
    'product_tag_ids',
    'attribute_line_ids',
    'ck_net_quantity',
    'ck_net_quantity_uom_id',
    'ck_reference_price_uom_id',
    'ck_show_reference_price',
}


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ck_net_quantity = fields.Float(
        string='Quantité nette',
        default=None,
        help='Quantité nette affichée sur la card home (ex. 320 g). Laisser vide si non applicable.',
    )
    ck_net_quantity_uom_id = fields.Many2one(
        comodel_name='dorevia.ck.card.uom',
        string='Unité de quantité nette',
        domain="[('use_for_net_quantity', '=', True), ('active', '=', True)]",
        ondelete='restrict',
    )
    ck_reference_price_uom_id = fields.Many2one(
        comodel_name='dorevia.ck.card.uom',
        string='Unité du prix de référence',
        domain="[('use_for_reference_price', '=', True), ('active', '=', True)]",
        ondelete='restrict',
    )
    ck_show_reference_price = fields.Boolean(
        string='Afficher le prix au kg / litre',
        default=True,
        help='Calcule et affiche le prix de référence sur la card home lorsque la quantité nette est renseignée.',
    )
    ck_is_featured = fields.Boolean(
        string='Afficher sur l\'accueil',
        default=False,
        help=(
            'Affiche ce produit dans les sélections de la page d\'accueil C-Kréyòl '
            'lorsque les règles de mise en avant le permettent.'
        ),
    )
    ck_producer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Producteur',
        domain="[('ck_is_producer', '=', True)]",
        ondelete='set null',
    )
    ck_badge_ids = fields.Many2many(
        comodel_name='ck.product.badge',
        relation='product_template_ck_badge_rel',
        column1='product_template_id',
        column2='badge_id',
        string='Badges qualifiés',
        help='Badges MOA sélectionnés manuellement — affichés en zone haute fiche produit.',
    )
    ck_discover_html = fields.Html(
        string='Section Découvrir',
        sanitize_overridable=True,
        sanitize_attributes=False,
        translate=True,
    )
    ck_ingredients = fields.Text(string='Ingrédients', translate=True)
    ck_allergens = fields.Text(string='Allergènes', translate=True)
    ck_nutrition_html = fields.Html(
        string='Informations nutritionnelles',
        sanitize_overridable=True,
        sanitize_attributes=False,
        translate=True,
    )
    ck_conservation_before = fields.Text(
        string='Conservation avant ouverture',
        translate=True,
    )
    ck_conservation_after = fields.Text(
        string='Conservation après ouverture',
        translate=True,
    )
    ck_packaging_label = fields.Char(
        string='Conditionnement client',
        translate=True,
        help='Libellé conditionnement affiché côté client (ex. Pot verre 320 g).',
    )

    @api.constrains('description_ecommerce')
    def _check_description_ecommerce_length(self):
        """R1 — accroche zone haute : texte brut ≤ 255 caractères."""
        for product in self:
            plain = html2plaintext(product.description_ecommerce or '').strip()
            if len(plain) > CK_ECOMMERCE_LEAD_MAX_CHARS:
                raise ValidationError(self.env._(
                    'L’accroche e-commerce ne doit pas dépasser %(max)s caractères '
                    '(actuellement %(count)s).',
                    max=CK_ECOMMERCE_LEAD_MAX_CHARS,
                    count=len(plain),
                ))

    def get_ck_shop_card_metadata_line(self, variant=None):
        """Ligne meta card boutique — origine · tags · format · prix comparatif (canon Home)."""
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            _get_shop_card_secondary_line,
        )

        self.ensure_one()
        variant = (variant or self.product_variant_id).sudo()
        if not variant:
            return ''
        website = self.env['website'].get_current_website()
        if not website:
            return ''
        return _get_shop_card_secondary_line(self.env, website, variant)

    def get_ck_product_page_detail_sections(self):
        """Sections bas de fiche produit CK (Lot 2) — affichage conditionnel."""
        from odoo.addons.dorevia_ck_marketone_content.product_page_details import (
            build_ck_product_page_detail_sections,
        )

        self.ensure_one()
        return build_ck_product_page_detail_sections(self)

    def get_ck_product_page_tabs(self, variant=None):
        """Blocs complémentaires fiche produit — empilement vertical + ancres MOA."""
        from odoo.addons.dorevia_ck_marketone_content.product_page_tabs import (
            build_ck_product_page_tabs,
        )

        self.ensure_one()
        product = self.sudo()
        variant = (variant or product.product_variant_id).sudo()
        return build_ck_product_page_tabs(product, variant)

    def get_ck_product_page_metadata_line(self, variant=None):
        """Ligne métadonnées zone haute — origine · producteur · poids net · prix réf."""
        from odoo.addons.dorevia_ck_marketone_content.product_page_v11 import (
            build_ck_product_page_metadata_line,
        )

        self.ensure_one()
        variant = (variant or self.product_variant_id).sudo()
        if not variant:
            return ''
        return build_ck_product_page_metadata_line(self.env, self, variant)

    def get_ck_related_products(self):
        """Produits liés CK — même producteur · même catégorie. 4 max, seulement si ≥ 2."""
        self.ensure_one()
        website = self.env['website'].get_current_website()
        if not website:
            return self.browse([])

        base_domain = [
            ('is_published', '=', True),
            ('sale_ok', '=', True),
            ('id', '!=', self.id),
        ]

        candidates = self.browse([])

        if self.ck_producer_id:
            candidates |= self.sudo().search(
                base_domain + [('ck_producer_id', '=', self.ck_producer_id.id)],
                limit=6, order='website_sequence asc',
            )

        if len(candidates) < 4 and self.public_categ_ids:
            candidates |= self.sudo().search(
                base_domain + [
                    ('public_categ_ids', 'in', self.public_categ_ids.ids),
                    ('id', 'not in', candidates.ids),
                ],
                limit=4, order='website_sequence asc',
            )

        candidates = candidates[:4]
        return candidates if len(candidates) >= 2 else self.browse([])

    def get_ck_variant_value_prices(self, attribute_line):
        """Prix absolus contextualisés par valeur d'attribut (sélecteur variantes CK)."""
        from odoo.addons.dorevia_ck_marketone_content.product_page_v11 import (
            build_ck_variant_value_prices,
        )

        self.ensure_one()
        return build_ck_variant_value_prices(self.env, self, attribute_line)

    def _ck_refresh_home_featured_products(self):
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            refresh_home_featured_products,
        )

        refresh_home_featured_products(self.env)

    def _ck_refresh_home_featured_if_stale(self):
        """Filet agnostique au champ : reconstruit seulement si une card affichée est périmée.

        Utilisé comme repli après un write variante (``product.product``) portant
        sur un champ hors liste explicite : tout changement qui modifie réellement
        le rendu d'une card vedette (titre, image, prix, métadonnée) est ainsi
        propagé immédiatement, sans sur-rebuild quand le snapshot est déjà à jour.
        """
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            _featured_arch_stale_any_lang,
            bootstrap_home_featured_products,
        )

        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        if not page or not page.view_id:
            return
        website = self.env['website'].search([], limit=1)
        if not website:
            return
        if _featured_arch_stale_any_lang(self.env, website, page):
            bootstrap_home_featured_products(self.env)

    def _ck_touches_featured(self):
        """Rebuild home si le produit est (ou était) marqué Afficher sur l'accueil."""
        return any(self.mapped('ck_is_featured'))

    def write(self, vals):
        touches_featured_fields = bool(FEATURED_REFRESH_FIELDS.intersection(vals))
        # Membre des vedettes AVANT écriture (capte une sortie de curation).
        was_featured = self._ck_touches_featured() if touches_featured_fields else False
        result = super().write(vals)
        # ... ou APRÈS écriture (capte une entrée en curation).
        if touches_featured_fields and (was_featured or self._ck_touches_featured()):
            self._ck_refresh_home_featured_products()
        return result

    def _register_hook(self):
        super()._register_hook()
        if tools.config.get('test_enable') or tools.config.get('test_tags'):
            return
        self._ck_sync_home_featured_labels_on_startup()

    @api.model
    def _ck_sync_home_featured_labels_on_startup(self):
        """Reconstruit la home si des étiquettes BO manquent des cards SSR (arch périmée)."""
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            _featured_arch_stale_any_lang,
            bootstrap_home_featured_products,
        )

        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        if not page or not page.view_id:
            return
        website = self.env['website'].search([], limit=1)
        if not website:
            return
        if not _featured_arch_stale_any_lang(self.env, website, page):
            return
        if bootstrap_home_featured_products(self.env):
            _logger.info('CK Section 3 : home reconstruite (arch vedettes périmée).')
