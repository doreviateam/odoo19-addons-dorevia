# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, tools

_logger = logging.getLogger(__name__)


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

    def get_ck_shop_card_metadata_line(self, variant=None):
        """Ligne secondaire card boutique — tags · format · prix comparatif.

        P2A — l'origine n'est plus incluse ici, elle est affichée à part en
        eyebrow (cf. get_ck_shop_card_origin_label) : même donnée, présentation
        densifiée façon "marque" au-dessus du titre.
        """
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

    def get_ck_shop_card_origin_label(self, variant=None):
        """Eyebrow card boutique — origine seule, au-dessus du titre."""
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            _get_shop_card_origin_label,
        )

        self.ensure_one()
        variant = (variant or self.product_variant_id).sudo()
        if not variant:
            return ''
        return _get_shop_card_origin_label(self, variant)

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
