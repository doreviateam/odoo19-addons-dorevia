#!/usr/bin/env python3
"""Q1 §6quater — Produits vedettes en rendu serveur (SSR) · sans hydratation JS.

Le dynamic snippet Odoo laisse `.dynamic_snippet_template` vide côté HTML source ;
si le RPC frontend échoue ou si la recette inspecte avant hydratation → 0 carte.
Ce script pré-rend les cartes via l'API `/website/snippet/filters` et les injecte dans la home.

Usage :
  docker exec -i sandbox-odoo19-odoo-1 odoo shell -d dorevia_ck_marketone_01 --no-http \\
    < ck_q1_ssr_featured.py
  docker restart sandbox-odoo19-odoo-1
"""
import json
import math
import re
import urllib.error
import urllib.request

website = env['website'].browse(1)
published = env['product.template'].search([
    ('website_published', '=', True),
    ('is_published', '=', True),
])
count = len(published)
print('published CK products', count, published.mapped('name'))

FILTER_ID = 1
TEMPLATE_KEY = 'website_sale.dynamic_filter_template_product_product_products_item'
CHUNK_SIZE = 3
LIMIT = count or 5

# Options Odoo sans hover zoom / actions onhover (sources de layout shift)
FEATURED_GRID_CLASSES = (
    's_ck_featured_products_grid ck-featured-products__grid ck-featured-products__grid--stable '
    'oe_website_sale o_wsale_products_opt_layout_catalog o_wsale_products_opt_design_thumbs '
    'o_wsale_products_opt_name_color_regular o_wsale_products_opt_rounded_2 o_wsale_products_opt_thumb_cover '
    'o_wsale_products_opt_has_cta o_wsale_products_opt_has_wishlist o_wsale_products_opt_wishlist_fixed '
    'o_wsale_products_opt_has_description o_wsale_products_opt_actions_subtle o_wsale_products_opt_cc1 '
    'pt16 pb48 o_colored_level'
)

payload = json.dumps({
    'jsonrpc': '2.0',
    'method': 'call',
    'params': {
        'filter_id': FILTER_ID,
        'template_key': TEMPLATE_KEY,
        'limit': LIMIT,
        'search_domain': [],
        'with_sample': False,
    },
    'id': 1,
}).encode()

parts = []
for port in (8069, 8079, 18079):
    try:
        req = urllib.request.Request(
            f'http://127.0.0.1:{port}/website/snippet/filters',
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'X-Odoo-Database': env.cr.dbname,
            },
            method='POST',
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode())
        parts = body.get('result') or []
        if parts:
            print('fetched cards via HTTP port', port, '· count', len(parts))
            break
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ConnectionError) as exc:
        print('HTTP port', port, 'failed:', exc)

if not parts:
    raise SystemExit('No product cards fetched — is Odoo HTTP running?')

# arch_db exige du XML valide : les cartes Odoo utilisent <input> HTML non auto-fermants
parts = [re.sub(r'<input\b([^>]*?)>', r'<input\1/>', fragment) for fragment in parts]

col_span = max(1, 12 // CHUNK_SIZE)
col_class = f'col-12 col-md-{col_span} d-flex align-items-stretch'
rows = []
for row_index in range(math.ceil(len(parts) / CHUNK_SIZE)):
    cols = []
    for col_index in range(CHUNK_SIZE):
        idx = row_index * CHUNK_SIZE + col_index
        if idx >= len(parts):
            break
        cols.append(f'<div class="{col_class}"><div class="w-100 h-100">{parts[idx]}</div></div>')
    rows.append(f'<div class="row mb-4 g-3">{"".join(cols)}</div>')
grid_inner = '\n                '.join(rows)

featured_grid = f"""
<section class="{FEATURED_GRID_CLASSES}" data-name="Produits vedettes grille SSR">
    <div class="container">
        <div class="ck-featured-products__ssr dynamic_snippet_template oe_unremovable">
            {grid_inner}
        </div>
    </div>
</section>
""".strip()

featured_title = """
<section class="s_ck_featured_products ck-featured-products pt48 pb-0 o_colored_level" data-snippet="s_ck_featured_products" data-name="Produits vedettes">
    <div class="container">
        <h2 class="ck-section-title h3 mb-0 o_editable">Produits vedettes</h2>
    </div>
</section>
""".strip()

featured = featured_title + '\n' + featured_grid

page = env['website.page'].search([('url', '=', '/'), ('website_id', '=', website.id)], limit=1)
view = page.view_id
arch = view.arch_db or view.arch or ''
if isinstance(arch, dict):
    arch = arch.get(env.lang) or next(iter(arch.values()), '')

# Remplacer tout le bloc vedettes (titre + dynamic ou SSR) jusqu'aux catégories
start = arch.find('<section class="s_ck_featured_products ck-featured-products pt48 pb-0')
end = arch.find('<section class="s_ck_category_links', start)
if start < 0 or end < 0:
    raise SystemExit('Featured block boundaries not found in homepage arch')

arch = arch[:start] + featured + '\n' + arch[end:]

if 'ck-featured-products__grid--stable' not in arch:
    raise SystemExit('SSR block not injected — check homepage arch structure')

from odoo.tools.translate import xml_translate
xml_translate(lambda t: None, arch)

view.write({'arch_db': arch})
env.cr.commit()

cards_in_arch = arch.count('o_carousel_product_card')
links_in_arch = len(re.findall(r'href="/shop/[^"]+-\d+"', arch))
print('SSR injected · view_id', view.id, '· cards in arch', cards_in_arch, '· shop links', links_in_arch)
print('restart Odoo required')
