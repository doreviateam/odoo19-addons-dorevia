#!/usr/bin/env python3
"""Phase 2 — Home sobre · dorevia_ck_marketone_01 · GO §5bis 2026-06-13.

Vedettes : titre s_ck_featured_products + grille SSR (cartes pré-rendues, sans JS).
Voir ck_q1_ssr_featured.py pour régénérer les cartes après changement catalogue.

Usage :
  odoo shell -d dorevia_ck_marketone_01 --no-http < ck_phase2_configure.py
  docker restart sandbox-odoo19-odoo-1
"""
import json
import math
import re
import urllib.error
import urllib.request

website = env['website'].search([], limit=1)
page = env['website.page'].search([('url', '=', '/'), ('website_id', '=', website.id)], limit=1)
view = page.view_id
old_arch = view.arch_db or view.arch or ''
if isinstance(old_arch, dict):
    old_arch = old_arch.get(env.lang) or next(iter(old_arch.values()), '')

def extract_section(arch, snippet):
    m = re.search(
        rf'(<section[^>]*data-snippet="{snippet}"[^>]*>.*?</section>)',
        arch,
        re.DOTALL,
    )
    return m.group(1) if m else None

hero = extract_section(old_arch, 's_ck_hero') or str(env['ir.qweb']._render('dorevia_ck_theme.s_ck_hero', {}))

reassurance = extract_section(old_arch, 's_ck_reassurance') or str(env['ir.qweb']._render('dorevia_ck_theme.s_ck_reassurance', {}))
reassurance = reassurance.replace(
    'Producteurs et transformateurs identifiés.',
    'Producteurs et transformateurs repérés par CK.',
)
reassurance = reassurance.replace(
    'Checkout Odoo standard.',
    'Paiement en ligne sécurisé.',
)

def fetch_featured_cards(limit):
    payload = json.dumps({
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {
            'filter_id': 1,
            'template_key': 'website_sale.dynamic_filter_template_product_product_products_item',
            'limit': limit,
            'search_domain': [],
            'with_sample': False,
        },
        'id': 1,
    }).encode()
    for port in (8069, 8079, 18079):
        try:
            req = urllib.request.Request(
                f'http://127.0.0.1:{port}/website/snippet/filters',
                data=payload,
                headers={'Content-Type': 'application/json', 'X-Odoo-Database': env.cr.dbname},
                method='POST',
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                parts = json.loads(resp.read().decode()).get('result') or []
            if parts:
                return [re.sub(r'<input\b([^>]*?)>', r'<input\1/>', p) for p in parts]
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ConnectionError):
            continue
    return []


def build_featured_block(limit=5):
    parts = fetch_featured_cards(limit)
    if not parts:
        raise SystemExit('Cannot fetch featured product cards — is Odoo HTTP running?')
    chunk_size = 3
    featured_grid_classes = (
        's_ck_featured_products_grid ck-featured-products__grid ck-featured-products__grid--stable '
        'oe_website_sale o_wsale_products_opt_layout_catalog o_wsale_products_opt_design_thumbs '
        'o_wsale_products_opt_name_color_regular o_wsale_products_opt_rounded_2 o_wsale_products_opt_thumb_cover '
        'o_wsale_products_opt_has_cta o_wsale_products_opt_has_wishlist o_wsale_products_opt_wishlist_fixed '
        'o_wsale_products_opt_has_description o_wsale_products_opt_actions_subtle o_wsale_products_opt_cc1 '
        'pt16 pb48 o_colored_level'
    )
    col_class = f'col-12 col-md-{12 // chunk_size} d-flex align-items-stretch'
    rows = []
    for row_index in range(math.ceil(len(parts) / chunk_size)):
        cols = []
        for col_index in range(chunk_size):
            idx = row_index * chunk_size + col_index
            if idx >= len(parts):
                break
            cols.append(f'<div class="{col_class}"><div class="w-100 h-100">{parts[idx]}</div></div>')
        rows.append(f'<div class="row mb-4 g-3">{"".join(cols)}</div>')
    grid_inner = '\n                '.join(rows)
    featured_title = """
<section class="s_ck_featured_products ck-featured-products pt48 pb-0 o_colored_level" data-snippet="s_ck_featured_products" data-name="Produits vedettes">
    <div class="container">
        <h2 class="ck-section-title h3 mb-0 o_editable">Produits vedettes</h2>
    </div>
</section>
""".strip()
    featured_grid = f"""
<section class="{featured_grid_classes}" data-name="Produits vedettes grille SSR">
    <div class="container">
        <div class="ck-featured-products__ssr dynamic_snippet_template oe_unremovable">
            {grid_inner}
        </div>
    </div>
</section>
""".strip()
    return featured_title + '\n' + featured_grid


published_count = env['product.template'].search_count([('website_published', '=', True)])
featured = build_featured_block(published_count or 5)

categories = extract_section(old_arch, 's_ck_category_links')
if not categories or 'Artisanat et packs' in categories:
    categories = """
<section class="s_ck_category_links ck-category-links pt32 pb32 o_colored_level" data-snippet="s_ck_category_links" data-name="CK Liens univers">
    <div class="container text-center o_editable">
        <h2 class="ck-section-title h4 mb-4">Nos univers</h2>
        <div class="d-flex flex-wrap justify-content-center gap-2">
            <a href="/shop/category/epicerie-creole-1" class="ck-pill btn btn-outline-primary rounded-pill">Épicerie créole</a>
            <a href="/shop/category/maison-bien-etre-2" class="ck-pill btn btn-outline-primary rounded-pill">Maison &amp; bien-être</a>
        </div>
    </div>
</section>
""".strip()

dual_match = re.search(
    r'(<section class="s_text_block ck-dual-engage[^>]*>.*?</section>)',
    old_arch,
    re.DOTALL,
)
if dual_match:
    dual = dual_match.group(1)
else:
    newsletter_form = str(env['ir.qweb']._render('website_mass_mailing.s_newsletter_subscribe_form', {}))
    newsletter_form = newsletter_form.replace('data-list-id="0"', 'data-list-id="1"')
    dual = f"""
<section class="s_text_block ck-dual-engage pt64 pb64 o_colored_level" data-snippet="s_text_block" data-name="CK Dual Pro Newsletter">
    <div class="container">
        <div class="row g-4 align-items-stretch">
            <div class="col-lg-6 o_colored_level">
                <div class="ck-dual-engage__pro p-4 p-lg-5 h-100 rounded o_cc o_cc1">
                    <h2 class="h4 mb-3">Vous êtes professionnel ?</h2>
                    <p class="mb-4">Épicerie, boutique créole, restaurant, hôtel, traiteur, distributeur… CK étudie votre demande et vous oriente vers une sélection adaptée.</p>
                    <a href="/professionnels" class="btn btn-primary">Faire une demande professionnelle</a>
                </div>
            </div>
            <div class="col-lg-6 o_colored_level">
                <div class="ck-dual-engage__newsletter p-4 p-lg-5 h-100 rounded o_cc o_cc2">
                    <h2 class="h4 mb-3">Recevez les nouveautés créoles</h2>
                    <p class="mb-3">Produits, recettes, producteurs, idées d'usage et sélections CK.</p>
                    {newsletter_form}
                    <p class="small text-muted mt-2 mb-0">Sélections CK en cadence mesurée · désinscription à tout moment.</p>
                </div>
            </div>
        </div>
    </div>
</section>
""".strip()

pro_banner = extract_section(old_arch, 's_ck_pro_banner') or str(env['ir.qweb']._render('dorevia_ck_theme.s_ck_pro_banner', {}))

wrap_inner = '\n'.join([hero, reassurance, featured, categories, dual, pro_banner])

new_arch = f"""<t name="Homepage" t-name="website.homepage">
    <t t-call="website.layout" pageName.f="homepage">
        <div id="wrap" class="oe_structure oe_empty">
{wrap_inner}
        </div>
    </t>
</t>"""

view.write({'arch_db': new_arch})
page.write({'is_published': True})

p2 = env['website.page'].search([('url', '=', '/'), ('website_id', '=', False)], limit=1)
if p2 and p2.is_published:
    p2.write({'is_published': False})

env.cr.commit()
for s in ['s_ck_featured_products', 's_ck_featured_products_grid', 'ck-featured-products__grid--stable']:
    print('check', s, s in new_arch)
print('Phase 2 home recomposed · view_id', view.id, '· restart Odoo required')
