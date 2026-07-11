# -*- coding: utf-8 -*-
"""ACL portail — lecture des données CK affichées sur le site (checkout recette P0)."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install', 'dorevia_ck_portal_website_acl')
class TestCkPortalWebsiteAcl(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.portal_group = cls.env.ref('base.group_portal')
        cls.badge = cls.env['ck.product.badge'].create({
            'name': 'Guadeloupe Portal QA',
            'code': 'guadeloupe_portal_qa',
            'badge_type': 'origin',
        })
        cls.uom = cls.env['dorevia.ck.card.uom'].search([], limit=1)
        if not cls.uom:
            cls.uom = cls.env['dorevia.ck.card.uom'].create({
                'name': 'g Portal QA',
                'code': 'g_portal_qa',
                'use_for_net_quantity': True,
                'active': True,
            })
        cls.product = cls.env['product.template'].create({
            'name': 'Produit portal ACL QA',
            'type': 'consu',
            'list_price': 6.5,
            'sale_ok': True,
            'is_published': True,
            'ck_badge_ids': [(6, 0, cls.badge.ids)],
            'ck_net_quantity': 320,
            'ck_net_quantity_uom_id': cls.uom.id,
        })
        cls.portal_partner = cls.env['res.partner'].create({
            'name': 'Portal ACL QA',
            'email': 'portal-acl-qa@ck-marketone.test',
        })
        cls.portal_user = cls.env['res.users'].with_context(no_reset_password=True).create({
            'name': 'Portal ACL QA',
            'login': 'portal-acl-qa@ck-marketone.test',
            'email': 'portal-acl-qa@ck-marketone.test',
            'partner_id': cls.portal_partner.id,
            'group_ids': [(6, 0, [cls.portal_group.id])],
            'password': 'portal-acl-qa-test',
        })

    def test_portal_can_read_ck_product_badge(self):
        badge = self.badge.with_user(self.portal_user)
        data = badge.read(['name', 'badge_type', 'icon'])
        self.assertEqual(data[0]['name'], 'Guadeloupe Portal QA')

    def test_portal_can_read_product_ck_badge_ids(self):
        product = self.product.with_user(self.portal_user)
        self.assertEqual(product.ck_badge_ids, self.badge)
        self.assertEqual(product.ck_badge_ids.mapped('name'), ['Guadeloupe Portal QA'])

    def test_portal_can_read_dorevia_ck_card_uom(self):
        uom = self.uom.with_user(self.portal_user)
        data = uom.read(['name', 'code'])
        self.assertTrue(data[0]['name'])

    def test_portal_cannot_write_ck_product_badge(self):
        badge = self.badge.with_user(self.portal_user)
        with self.assertRaises(Exception):
            badge.write({'name': 'Tentative écriture portail'})
