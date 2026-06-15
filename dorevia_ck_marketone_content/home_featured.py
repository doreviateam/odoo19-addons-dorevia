# -*- coding: utf-8 -*-
"""Home Lot 2 / Section 3 — Produits vedettes SSR maquette CK (cartes dédiées)."""
import contextlib
import re
from unittest.mock import MagicMock, Mock, patch
from xml.sax.saxutils import escape

import odoo.http
from odoo.tools import DotDict, format_amount, lazy
from werkzeug.test import EnvironBuilder

MIN_FEATURED_PRODUCTS = 5
FEATURED_SECTION_MARKER = 'ck-featured-products'
FEATURED_GRID_MARKER = 'ck-featured-products__grid--stable'
FEATURED_CARD_MARKER = 'ck-product-card'
FEATURED_TITLE = 'Nos coups de cœur'
FEATURED_SUBTITLE = 'Sélection CK · prix TTC · origine et famille visibles'
FEATURED_SHOP_CTA = 'Toute la boutique →'

_DEMO_ORIGIN_BY_NAME_FRAGMENT = (
    ('goyav', 'Réunion'),
    ('galettes', 'Martinique'),
    ('manioc', 'Martinique'),
    ('manio', 'Guadeloupe'),
    ('cracker', 'Guadeloupe'),
    ('savon', 'Martinique'),
    ('vétiver', 'Martinique'),
    ('vetiver', 'Martinique'),
    ('colombo', 'Martinique'),
)

_ORIGIN_KEYWORDS = (
    'Réunion',
    'Guadeloupe',
    'Martinique',
    'Guyane',
    'Mayotte',
    'Sélection CK',
)

_CATEGORY_SHORT_LABELS = (
    'Épicerie',
    'Snacks',
    'Condiments',
    'Bien-être',
    'Boissons',
    'Packs',
)

_DEMO_CATEGORY_BY_NAME_FRAGMENT = (
    ('manio', 'Snacks'),
    ('cracker', 'Snacks'),
    ('savon', 'Bien-être'),
    ('vétiver', 'Bien-être'),
    ('vetiver', 'Bien-être'),
    ('colombo', 'Condiments'),
    ('goyav', 'Épicerie'),
    ('galettes', 'Épicerie'),
    ('manioc', 'Épicerie'),
)

_PLACEHOLDER_MARKERS = (
    'website.s_cover_default_image',
    's_cover_default',
    'o_wsale_product_grid_wrapper_placeholder',
    'is_sample',
)

_CARD_IMAGE_RE = re.compile(
    r"background-image:\s*url\(\s*['\"]?/web/image/product\.(?:template|product)/\d+/",
    re.IGNORECASE,
)
_CARD_PRICE_RE = re.compile(r'class="price"')
_CARD_LINK_RE = re.compile(r'class="card-cta"')

FEATURED_TITLE_SECTION = ''  # rétro-compat tests import — section unique désormais


def _arch_as_string(arch):
    if isinstance(arch, dict):
        return next(iter(arch.values()), '')
    return arch or ''


@contextlib.contextmanager
def _with_website_request(env, website):
    """Contexte HTTP minimal pour prix catalogue (hors requête WSGI)."""
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
    if variant.image_1920 or variant.image_512:
        return True
    return bool(template.image_1920 or template.image_512)


def _template_featured_variant_cap(template):
    """Multi-variantes : une carte par variante publiée (ex. ligne manioc)."""
    if len(template.product_variant_ids) > 1:
        return len(template.product_variant_ids)
    return 1


def get_ready_featured_variants(env, *, min_count=MIN_FEATURED_PRODUCTS, max_count=MIN_FEATURED_PRODUCTS):
    """Variantes publiées — une entrée par variante si template multi-variantes."""
    templates = env['product.template'].sudo().search([
        ('is_published', '=', True),
        ('website_published', '=', True),
        ('sale_ok', '=', True),
    ], order='website_sequence asc, id asc')

    variants = env['product.product'].browse()
    for template in templates:
        if not template.image_1920 and not any(
            v.image_1920 or v.image_512 for v in template.product_variant_ids
        ):
            continue
        candidates = template.product_variant_ids.filtered(
            lambda v: v.is_published and v.sale_ok and _variant_has_valid_image(v)
        ).sorted(key=lambda v: v.id)
        if not candidates:
            continue
        cap = _template_featured_variant_cap(template)
        variants |= candidates[:cap]
        if len(variants) >= max_count:
            break

    if len(variants) < min_count:
        return env['product.product'].browse()
    return variants[:max_count]


def _get_featured_origin_label(template):
    for line in template.attribute_line_ids:
        attr_name = (line.attribute_id.name or '').lower()
        if 'origine' in attr_name or 'origin' in attr_name:
            value = line.value_ids[:1]
            if value and (value.name or '').strip():
                return value.name.strip()
    haystack = ' '.join(filter(None, [
        template.description_sale or '',
        template.name or '',
    ]))
    lowered = haystack.lower()
    for keyword in _ORIGIN_KEYWORDS:
        if keyword.lower() in lowered:
            return keyword
    name_lower = (template.name or '').lower()
    for fragment, origin in _DEMO_ORIGIN_BY_NAME_FRAGMENT:
        if fragment in name_lower:
            return origin
    return ''


def _get_featured_category_label(template):
    category = template.public_categ_ids[:1]
    if not category:
        return ''
    name = (category.name or '').strip()
    if '—' in name:
        name = name.split('—', 1)[0].strip()
    lowered = name.lower()
    for short in _CATEGORY_SHORT_LABELS:
        if short.lower() in lowered:
            return short
    name_lower = (template.name or '').lower()
    for fragment, label in _DEMO_CATEGORY_BY_NAME_FRAGMENT:
        if fragment in name_lower:
            return label
    return name.split()[0] if name else ''


def _get_featured_display_name(variant):
    template = variant.product_tmpl_id
    if len(template.product_variant_ids) <= 1:
        return template.name or variant.display_name or ''
    value_names = [
        name for name in variant.product_template_attribute_value_ids.mapped('name')
        if name
    ]
    if value_names:
        return value_names[0] if len(value_names) == 1 else ' · '.join(value_names)
    display = (variant.display_name or '').strip()
    template_name = (template.name or '').strip()
    if template_name and display.startswith(template_name):
        short = display[len(template_name):].strip(' ,()-')
        if short:
            return short
    return display or template_name


def _get_featured_image_url(variant):
    template = variant.product_tmpl_id
    if variant.image_1920 or variant.image_512:
        return f'/web/image/product.product/{variant.id}/image_512'
    return f'/web/image/product.template/{template.id}/image_512'


def _get_featured_price_label(env, website, variant):
    template = variant.product_tmpl_id
    with _with_website_request(env, website):
        info = template._get_combination_info(product_id=variant.id, add_qty=1.0)
    price = info.get('price_reduce') or info.get('price') or template.list_price
    return format_amount(env, price, website.currency_id)


def _get_featured_badge_html(index):
    if index == 0:
        return '<span class="badge badge-heart badge-float">Coup de cœur</span>'
    if index == 1:
        return '<span class="badge badge-new badge-float">Nouveau</span>'
    return ''


def build_featured_product_card_html(env, website, variant, index):
    """Carte produit maquette V1.2 — variante explicite si template multi-variantes."""
    template = variant.product_tmpl_id
    name = escape(_get_featured_display_name(variant))
    href = escape(variant.website_url or template.website_url or '/shop')
    image_url = _get_featured_image_url(variant)
    price_label = escape(_get_featured_price_label(env, website, variant))
    origin = escape(_get_featured_origin_label(template))
    category = escape(_get_featured_category_label(template))
    badge_html = _get_featured_badge_html(index)

    meta_parts = []
    if origin:
        meta_parts.append(f'<span class="chip-origin">{origin}</span>')
    if category:
        meta_parts.append(f'<span class="chip-cat">{category}</span>')
    meta_block = (
        f'<div class="product-meta">{"".join(meta_parts)}</div>'
        if meta_parts else ''
    )

    return f"""
<article class="{FEATURED_CARD_MARKER} product-card">
    <a href="{href}" class="product-card-media ck-product-card__media" style="background-image:url('{image_url}')">
        {badge_html}
    </a>
    <div class="product-card-body">
        {meta_block}
        <h3><a href="{href}">{name}</a></h3>
    </div>
    <div class="product-card-foot">
        <span class="price">{price_label}</span>
        <a href="{href}" class="card-cta">Voir</a>
    </div>
</article>""".strip()


def card_fragment_is_valid(fragment):
    """Carte SSR maquette : image template, prix, CTA Voir — pas de placeholder."""
    if not fragment or FEATURED_CARD_MARKER not in fragment:
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


def render_ck_featured_cards(env, website, variants):
    """Pré-rendu serveur des cartes maquette (pas Dynamic Products / oe_product_cart)."""
    cards = []
    for index, variant in enumerate(variants):
        card = build_featured_product_card_html(env, website, variant, index)
        if card_fragment_is_valid(card):
            cards.append(card)
    return cards


# Alias rétro-compat Lot 2
render_featured_card_fragments = render_ck_featured_cards


def build_featured_ssr_arch(card_fragments):
    """Section vedettes maquette — en-tête + grille CSS 3 colonnes."""
    cards_inner = '\n            '.join(card_fragments)
    return f"""
<section class="s_ck_featured_products {FEATURED_SECTION_MARKER} ck-featured-products--maquette pt48 pb48 o_colored_level" data-snippet="s_ck_featured_products" data-name="Produits vedettes">
    <div class="container">
        <div class="ck-featured-products__head">
            <div>
                <h2 id="featured-title" class="ck-featured-products__title h3 mb-0 o_editable">{FEATURED_TITLE}</h2>
                <p class="ck-featured-products__subtitle mb-0 o_editable">{FEATURED_SUBTITLE}</p>
            </div>
            <a href="/shop" class="btn btn-secondary ck-featured-products__shop-cta o_editable">{FEATURED_SHOP_CTA}</a>
        </div>
        <div class="{FEATURED_GRID_MARKER} ck-featured-products__grid product-grid">
            {cards_inner}
        </div>
    </div>
</section>
""".strip()


def _find_featured_block_bounds(arch):
    marker = arch.find('data-snippet="s_ck_featured_products"')
    start = arch.rfind('<section', 0, marker) if marker >= 0 else -1
    if start < 0:
        start = arch.find(f'<section class="s_ck_featured_products {FEATURED_SECTION_MARKER}')
    end = -1
    if start >= 0:
        end = arch.find('<section class="s_ck_category_links', start)
        if end < 0:
            end_marker = arch.find('data-snippet="s_ck_category_links"', start)
            if end_marker >= 0:
                end = arch.rfind('<section', start, end_marker)
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
    """Lot 2 home — injecte la grille SSR vedettes maquette ou masque si BO insuffisant."""
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
        cards = render_ck_featured_cards(env, website, variants)
        if len(cards) >= MIN_FEATURED_PRODUCTS:
            featured_arch = build_featured_ssr_arch(cards[:MIN_FEATURED_PRODUCTS])

    new_arch, patched = _patch_homepage_featured_arch(arch, featured_arch)
    if not patched or new_arch == arch:
        return patched

    view.write({'arch_db': new_arch})
    return True
