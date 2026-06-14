#!/usr/bin/env python3
"""Q1 cleanup — dépublier produit test QA · ajuster vedettes au catalogue réel.

Usage :
  odoo shell -d dorevia_ck_marketone_01 --no-http < ck_q1_cleanup_test_product.py
  docker restart sandbox-odoo19-odoo-1
"""
# Dépublier produit test QA
test = env['product.template'].search([
    ('website_published', '=', True),
    '|', ('name', 'ilike', 'Recette QA'), ('name', 'ilike', 'Produit test'),
])
if test:
    test.write({'website_published': False, 'is_published': False})
    print('unpublished', test.mapped('name'))

published = env['product.template'].search([('website_published', '=', True)])
count = len(published)
print('published CK products', count, published.mapped('name'))

# Ajuster data-number-of-records sur la home
page = env['website.page'].search([('url', '=', '/'), ('website_id', '=', 1)], limit=1)
arch = page.view_id.arch_db
if isinstance(arch, dict):
    arch_str = arch.get('fr_FR') or arch.get('en_US') or list(arch.values())[0]
else:
    arch_str = arch or ''

import re
new_arch = re.sub(r'data-number-of-records="\d+"', f'data-number-of-records="{count}"', arch_str)
if new_arch != arch_str:
    page.view_id.write({'arch_db': new_arch})
    print('data-number-of-records ->', count)

env.cr.commit()
print('done — restart Odoo required')
