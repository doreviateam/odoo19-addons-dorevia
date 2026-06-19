# -*- coding: utf-8 -*-
"""Purge les bundles CSS en échec (css_error_message) après recentrage tokens frontend."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    broken = env['ir.attachment'].browse()
    for att in env['ir.attachment'].search([
        ('url', 'like', '/web/assets/%'),
        '|',
        ('url', 'like', '%.css'),
        ('name', 'like', '%.css'),
    ]):
        raw = att.raw or b''
        if b'css_error_message' in raw or b'Undefined variable' in raw:
            broken |= att
    if broken:
        broken.unlink()
