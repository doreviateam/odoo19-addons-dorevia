# -*- coding: utf-8 -*-
from odoo import fields, models


class WebsiteMenu(models.Model):
    _inherit = 'website.menu'

    ck_nav_css_class = fields.Char(
        string='CK nav CSS class',
        help='Classe CSS optionnelle pour le rendu header Nav V2 (desktop/mobile).',
    )
    ck_nav_category_id = fields.Many2one(
        'product.public.category',
        string='CK nav category',
        ondelete='set null',
        help='Catégorie BO liée (rendu mobile L2 dynamique · palier parent navigable).',
    )

    def _ck_nav_is_desktop_universe(self):
        self.ensure_one()
        return 'ck-nav-desktop-universe' in (self.ck_nav_css_class or '').split()

    def _ck_nav_is_mobile_universe_child(self):
        self.ensure_one()
        return 'ck-nav-mobile-universe-child' in (self.ck_nav_css_class or '').split()

    def _ck_nav_eligible_l2_categories(self):
        """Enfants L2 éligibles pour le menu mobile (source BO, hors website.menu)."""
        from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
            _category_shop_url,
            _eligible_level2_children,
        )

        self.ensure_one()
        # Le header est rendu pour l'utilisateur public, qui n'a volontairement
        # pas d'ACL de lecture globale sur product.public.category. Le menu a été
        # construit côté serveur depuis des catégories publiées : on élève donc
        # uniquement la lecture de la catégorie explicitement liée au menu.
        category = self.sudo().ck_nav_category_id
        if not category:
            return []
        rows = []
        for child in _eligible_level2_children(self.env, category):
            url = _category_shop_url(self.env, child)
            if not url:
                continue
            rows.append({
                'id': child.id,
                'name': child.name,
                'url': url,
            })
        return rows

    def _ck_nav_has_eligible_l2(self):
        return bool(self._ck_nav_eligible_l2_categories())

    def _ck_nav_category_shop_url(self):
        """URL boutique de la catégorie liée (indépendante du url=# forcé par Odoo si enfants)."""
        from odoo.addons.dorevia_ck_marketone_content.nav_sync import _category_shop_url

        self.ensure_one()
        category = self.sudo().ck_nav_category_id
        if category:
            return _category_shop_url(self.env, category) or self._clean_url()
        return self._clean_url()
