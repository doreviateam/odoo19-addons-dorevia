# -*- coding: utf-8 -*-
"""Photo producteur site web — initialiser depuis image_1920 existante si vide."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    producers = env['res.partner'].sudo().search([
        ('ck_is_producer', '=', True),
        ('ck_producer_website_image', '=', False),
        ('image_1920', '!=', False),
    ])
    for producer in producers:
        producer.ck_producer_website_image = producer.image_1920
