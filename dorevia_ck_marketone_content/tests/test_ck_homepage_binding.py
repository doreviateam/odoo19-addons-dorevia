# -*- coding: utf-8 -*-
"""Homepage binding — page / site-specific vs globale (install fraîche)."""
from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_hero import (
    HERO_VARIANT_MARKER,
    bootstrap_home_hero,
    hero_home_arch_is_valid,
)
from odoo.addons.dorevia_ck_marketone_content.home_page import (
    bootstrap_website_homepage_binding,
    get_website_homepage_page,
    remove_global_homepage_conflicts,
    resolve_homepage_page_for_website,
)


@tagged('post_install', '-at_install', 'dorevia_ck_homepage_binding')
class TestCkHomepageBinding(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].sudo().search([], limit=1)
        cls.Page = cls.env['website.page'].sudo()

    def _site_home_arch(self):
        _website, page = get_website_homepage_page(self.env, self.website)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        return arch

    def test_bootstrap_removes_global_homepage_duplicate(self):
        bootstrap_home_hero(self.env)
        bootstrap_website_homepage_binding(self.env)
        global_count = self.Page.search_count([
            ('url', '=', '/'),
            ('website_id', '=', False),
        ])
        self.assertEqual(global_count, 0)
        _website, site_page = get_website_homepage_page(self.env, self.website)
        self.assertTrue(site_page)
        self.assertTrue(hero_home_arch_is_valid(self._site_home_arch()))

    def test_resolved_homepage_is_site_specific_with_hero(self):
        bootstrap_home_hero(self.env)
        bootstrap_website_homepage_binding(self.env)
        resolved = resolve_homepage_page_for_website(self.env, self.website)
        _website, site_page = get_website_homepage_page(self.env, self.website)
        self.assertEqual(resolved, site_page)
        self.assertTrue(hero_home_arch_is_valid(self._site_home_arch()))

    def test_global_shadowing_conflict_neutralized(self):
        bootstrap_home_hero(self.env)
        _website, site_page = get_website_homepage_page(self.env, self.website)
        View = self.env['ir.ui.view'].sudo()
        shadow_view = View.create({
            'name': 'Global Home Shadow QA',
            'type': 'qweb',
            'key': 'dorevia_ck_marketone_content.qa_global_home_shadow',
            'arch': """<t name="Home" t-name="website.homepage">
    <t t-call="website.layout" pageName.f="homepage">
        <div id="wrap" class="oe_structure oe_empty"/>
    </t>
</t>""",
        })
        self.Page.create({
            'name': 'Home Shadow',
            'url': '/',
            'website_id': False,
            'view_id': shadow_view.id,
            'is_published': True,
        })
        self.assertTrue(remove_global_homepage_conflicts(self.env))
        resolved = resolve_homepage_page_for_website(self.env, self.website)
        self.assertEqual(resolved, site_page)
        self.assertEqual(
            self.Page.search_count([('url', '=', '/'), ('website_id', '=', False)]),
            0,
        )


@tagged('post_install', '-at_install', 'dorevia_ck_homepage_binding')
class TestCkHomepageBindingHttp(HttpCase):

    def test_home_renders_hero_marker(self):
        bootstrap_home_hero(self.env)
        bootstrap_website_homepage_binding(self.env)
        html = self.url_open('/').text
        self.assertIn(HERO_VARIANT_MARKER, html)
        self.assertIn('Découvrir la boutique', html)
