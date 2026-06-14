# -*- coding: utf-8 -*-
"""Home Lot 2 — Produits vedettes SSR sans placeholders (MOA maquette V1)."""
import contextlib
import math
import re
from unittest.mock import MagicMock, Mock, patch

import odoo.http
from odoo.tools import DotDict, lazy
from werkzeug.test import EnvironBuilder

MIN_FEATURED_PRODUCTS = 5
FEATURED_SNIPPET_FILTER_XML_ID = 'website_sale.dynamic_snippet_new_products'
FEATURED_TEMPLATE_KEY = 'website_sale.dynamic_filter_template_product_product_products_item'
FEATURED_CHUNK_SIZE = 3

FEATURED_GRID_CLASSES = (
    's_ck_featured_products_grid ck-featured-products__grid ck-featured-products__grid--stable '
    'oe_website_sale o_wsale_products_opt_layout_catalog o_wsale_products_opt_design_thumbs '
    'o_wsale_products_opt_name_color_regular o_wsale_products_opt_rounded_2 o_wsale_products_opt_thumb_cover '
    'o_wsale_products_opt_has_cta o_wsale_products_opt_has_wishlist o_wsale_products_opt_wishlist_fixed '
    'o_wsale_products_opt_has_description o_wsale_products_opt_actions_subtle o_wsale_products_opt_cc1 '
    'pt16 pb48 o_colored_level'
)

FEATURED_TITLE_SECTION = """
<section class="s_ck_featured_products ck-featured-products pt48 pb-0 o_colored_level" data-snippet="s_ck_featured_products" data-name="Produits vedettes">
    <div class="container">
        <h2 class="ck-section-title h3 mb-0 o_editable">Produits vedettes</h2>
    </div>
</section>
""".strip()

_PLACEHOLDER_MARKERS = (
    'website.s_cover_default_image',
    's_cover_default',
    'o_wsale_product_grid_wrapper_placeholder',
    'is_sample',
)

_CARD_IMAGE_RE = re.compile(
    r'background-image:\s*url\(\s*/web/image/product\.(?:product|template)/\d+/',
    re.IGNORECASE,
)
_CARD_PRICE_RE = re.compile(r'oe_currency_value|itemprop="price"')
_CARD_LINK_RE = re.compile(r'href="/shop/[^"]+"')


def _arch_as_string(arch):
    if isinstance(arch, dict):
        return next(iter(arch.values()), '')
    return arch or ''


@contextlib.contextmanager
def _with_website_request(env, website):
    """Contexte HTTP minimal pour le rendu snippet (hors requête WSGI)."""
    lang_code = env.context.get('lang') or 'fr_FR'
    env = env(context=dict(env.context, lang=lang_code))
    request = Mock(
        httprequest=Mock(
            host='localhost',
            path='/',
            app=odoo.http.root,
            environ=EnvironBuilder(
                path='/',
                base_url='http://127.0.0.1:8069',
            ).get_environ(),
            cookies={},
            referrer='',
            remote_addr='127.0.0.1',
            url_root='http://127.0.0.1:8069/',
            args=[],
        ),
        type='http',
        future_response=odoo.http.FutureResponse(),
        params={},
        redirect=env['ir.http']._redirect,
        session=DotDict(
            odoo.http.get_default_session(),
            context={'lang': lang_code},
            force_website_id=website.id,
        ),
        geoip=odoo.http.GeoIP('127.0.0.1'),
        db=env.registry.db_name,
        env=env,
        registry=env.registry,
        lang=env['res.lang']._get_data(code=lang_code),
        website=website,
        render=lambda *args, **kwargs: '',
    )
    request.website_routing = website.id
    request.pricelist = lazy(website._get_and_cache_current_pricelist)
    request.cart = lazy(website._get_and_cache_current_cart)
    request.fiscal_position = lazy(website._get_and_cache_current_fiscal_position)
    router = MagicMock()
    router.return_value.bind.return_value.match.return_value[0].routing = {
        'type': 'http',
        'website': True,
        'multilang': True,
    }
    with contextlib.ExitStack() as stack:
        odoo.http._request_stack.push(request)
        stack.callback(odoo.http._request_stack.pop)
        stack.enter_context(patch('odoo.http.root.get_db_router', router))
        yield request


def _variant_has_valid_image(variant):
    template = variant.product_tmpl_id
    return bool(template.image_1920 or template.image_512 or variant.image_1920 or variant.image_512)


def get_ready_featured_variants(env, *, min_count=MIN_FEATURED_PRODUCTS, max_count=MIN_FEATURED_PRODUCTS):
    """Variantes publiées avec image BO — ordre catalogue website."""
    templates = env['product.template'].sudo().search([
        ('is_published', '=', True),
        ('website_published', '=', True),
        ('sale_ok', '=', True),
        ('image_1920', '!=', False),
    ], limit=max_count, order='website_sequence asc, id asc')
    variants = templates.mapped('product_variant_id').filtered(
        lambda v: v.is_published and v.sale_ok and _variant_has_valid_image(v)
    )
    if len(variants) < min_count:
        return env['product.product'].browse()
    return variants[:max_count]


def _normalize_card_fragment(fragment):
    return re.sub(r'<input\b([^>]*?)>', r'<input\1/>', fragment or '')


def card_fragment_is_valid(fragment):
    """Carte SSR : image produit réelle, prix et lien boutique — pas de placeholder."""
    if not fragment:
        return False
    lowered = fragment.lower()
    if any(marker in lowered for marker in _PLACEHOLDER_MARKERS):
        return False
    if not _CARD_IMAGE_RE.search(fragment):
        return False
    if not _CARD_PRICE_RE.search(fragment):
        return False
    if not _CARD_LINK_RE.search(fragment):
        return False
    return True


def _get_featured_snippet_filter(env):
    filt = env.ref(FEATURED_SNIPPET_FILTER_XML_ID, raise_if_not_found=False)
    if filt:
        return filt.sudo()
    return env['website.snippet.filter'].sudo().browse(1)


def render_featured_card_fragments(env, website, variants):
    """Pré-rendu serveur des cartes produit (grille SSR Q1 · pas Dynamic Products)."""
    snippet_filter = _get_featured_snippet_filter(env)
    if not snippet_filter:
        return []
    with _with_website_request(env, website):
        parts = snippet_filter._render(
            template_key=FEATURED_TEMPLATE_KEY,
            limit=len(variants),
            search_domain=[('id', 'in', variants.ids)],
            with_sample=False,
        )
    return [
        _normalize_card_fragment(part)
        for part in (parts or [])
        if card_fragment_is_valid(part)
    ]


def build_featured_ssr_arch(card_fragments):
    """Titre + grille SSR stable (3 colonnes desktop · pas de carousel)."""
    col_span = max(1, 12 // FEATURED_CHUNK_SIZE)
    col_class = f'col-12 col-md-{col_span} d-flex align-items-stretch'
    rows = []
    for row_index in range(math.ceil(len(card_fragments) / FEATURED_CHUNK_SIZE)):
        cols = []
        for col_index in range(FEATURED_CHUNK_SIZE):
            idx = row_index * FEATURED_CHUNK_SIZE + col_index
            if idx >= len(card_fragments):
                break
            cols.append(
                f'<div class="{col_class}"><div class="w-100 h-100">{card_fragments[idx]}</div></div>'
            )
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
    return FEATURED_TITLE_SECTION + '\n' + featured_grid


def _find_featured_block_bounds(arch):
    start = arch.find('<section class="s_ck_featured_products ck-featured-products pt48 pb-0')
    if start < 0:
        marker = arch.find('data-snippet="s_ck_featured_products"')
        if marker >= 0:
            start = arch.rfind('<section', 0, marker)
    end = -1
    if start >= 0:
        end = arch.find('<section class="s_ck_category_links', start)
        if end < 0:
            end = arch.find('data-snippet="s_ck_category_links"', start)
            if end >= 0:
                end = arch.rfind('<section', start, end)
    return start, end


def _find_featured_insertion_index(arch):
    insert_at = arch.find('<section class="s_ck_category_links')
    if insert_at < 0:
        marker = arch.find('data-snippet="s_ck_category_links"')
        if marker >= 0:
            insert_at = arch.rfind('<section', 0, marker)
    return insert_at


def _patch_homepage_featured_arch(arch, featured_arch):
    start, end = _find_featured_block_bounds(arch)
    if start >= 0 and end >= 0:
        if featured_arch:
            new_arch = arch[:start] + featured_arch + '\n' + arch[end:]
        else:
            new_arch = arch[:start] + arch[end:]
        return new_arch, True

    insert_at = _find_featured_insertion_index(arch)
    if insert_at < 0:
        return arch, False
    if featured_arch:
        new_arch = arch[:insert_at] + featured_arch + '\n' + arch[insert_at:]
        return new_arch, True
    return arch, True


def bootstrap_home_featured_products(env):
    """Lot 2 home — injecte la grille SSR vedettes ou masque la section si BO insuffisant."""
    website = env['website'].search([], limit=1)
    if not website:
        return False

    page = env['website.page'].sudo().search([
        ('url', '=', '/'),
        ('website_id', '=', website.id),
    ], limit=1)
    if not page or not page.view_id:
        return False

    view = page.view_id.sudo()
    arch = _arch_as_string(view.arch_db or view.arch)
    if not arch.strip():
        return False

    variants = get_ready_featured_variants(env)
    featured_arch = ''
    if variants:
        cards = render_featured_card_fragments(env, website, variants)
        if len(cards) >= MIN_FEATURED_PRODUCTS:
            featured_arch = build_featured_ssr_arch(cards[:MIN_FEATURED_PRODUCTS])

    new_arch, patched = _patch_homepage_featured_arch(arch, featured_arch)
    if not patched or new_arch == arch:
        return patched

    view.write({'arch_db': new_arch})
    return True
