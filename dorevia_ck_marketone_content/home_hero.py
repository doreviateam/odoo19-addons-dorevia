# -*- coding: utf-8 -*-
"""Home V1 Hero / Lot 1 — rapprochement maquette (MOA maquette V1)."""
from xml.sax.saxutils import escape

HERO_VARIANT_MARKER = 'ck-hero--marketone-v1'
HERO_DATA_NAME = 'CK Hero home V1'
HERO_KICKER = 'Boutique créole · Livraison France & Europe'
HERO_TITLE = 'Les saveurs créoles, prêtes à commander.'
HERO_LEAD = (
    'Épicerie, boissons, coffrets et bien-être — prix visibles, '
    'producteurs sélectionnés dans les territoires créolophones, '
    'achat en confiance.'
)
HERO_CTA_SHOP_LABEL = 'Voir la boutique'
HERO_CTA_PRO_LABEL = 'Espace professionnel'
HERO_VISUAL_ALT = 'Sélection de produits créoles — épicerie et condiments'

_COVER_DEFAULT_MARKERS = (
    'website.s_cover_default_image',
    's_cover_default',
)


def _arch_as_string(arch):
    if isinstance(arch, dict):
        return next(iter(arch.values()), '')
    return arch or ''


def get_hero_visual_product(env):
    """Produit publié avec image BO pour visuel Hero — sinon placeholder éditorial."""
    Product = env['product.template'].sudo()
    domain = [
        ('is_published', '=', True),
        ('website_published', '=', True),
        ('sale_ok', '=', True),
        ('image_1920', '!=', False),
    ]
    return Product.search(domain, limit=1, order='website_sequence asc, id asc')


def _hero_visual_html(env):
    product = get_hero_visual_product(env)
    if product and product.image_1920:
        alt = escape(HERO_VISUAL_ALT)
        return (
            f'<div class="ck-hero__visual rounded overflow-hidden border">'
            f'<img src="/web/image/product.template/{product.id}/image_512" '
            f'class="ck-hero__visual-media" alt="{alt}" loading="eager" '
            f'width="800" height="500"/>'
            f'</div>'
        )
    return (
        '<div class="ck-hero__visual ck-hero__visual--editorial rounded overflow-hidden border '
        'd-flex align-items-center justify-content-center">'
        '<span class="fa fa-shopping-basket fa-3x text-muted" aria-hidden="true"></span>'
        '</div>'
    )


def build_home_hero_arch(env):
    """Hero compact maquette V1 · kicker · dual CTA · visuel produit BO ou placeholder."""
    kicker = escape(HERO_KICKER)
    title = escape(HERO_TITLE)
    lead = escape(HERO_LEAD)
    cta_shop = escape(HERO_CTA_SHOP_LABEL)
    cta_pro = escape(HERO_CTA_PRO_LABEL)
    visual = _hero_visual_html(env)
    return f"""
<section class="s_ck_hero ck-hero {HERO_VARIANT_MARKER} o_colored_level" data-snippet="s_ck_hero" data-name="{HERO_DATA_NAME}">
    <div class="container">
        <div class="row align-items-center g-4">
            <div class="col-lg-7 o_colored_level">
                <p class="ck-hero__kicker small text-uppercase fw-semibold text-muted mb-2">{kicker}</p>
                <h1 class="ck-hero__title mb-3">{title}</h1>
                <p class="ck-hero__lead text-muted mb-4">{lead}</p>
                <div class="d-flex flex-wrap gap-2 ck-hero__cta">
                    <a href="/shop" class="btn btn-primary">{cta_shop}</a>
                    <a href="/professionnels" class="btn btn-secondary">{cta_pro}</a>
                </div>
            </div>
            <div class="col-lg-5 o_colored_level">
                {visual}
            </div>
        </div>
    </div>
</section>
""".strip()


def _find_hero_block_bounds(arch):
    for marker in (
        f'data-name="{HERO_DATA_NAME}"',
        HERO_VARIANT_MARKER,
        'data-snippet="s_ck_hero"',
        'class="s_ck_hero',
    ):
        idx = arch.find(marker)
        if idx < 0:
            continue
        start = arch.rfind('<section', 0, idx)
        if start < 0:
            continue
        end = arch.find('</section>', start)
        if end >= 0:
            return start, end + len('</section>')
    return -1, -1


def _patch_homepage_hero_arch(arch, hero_arch):
    start, end = _find_hero_block_bounds(arch)
    if start < 0 or end < 0:
        return arch, False
    new_arch = arch[:start] + hero_arch + arch[end:]
    return new_arch, True


def hero_home_arch_is_valid(arch):
    """Recette Lot 1 : wording maquette · dual CTA · pas de cover Odoo générique."""
    if HERO_VARIANT_MARKER not in arch:
        return False
    chunk_start = arch.find(HERO_VARIANT_MARKER)
    chunk = arch[chunk_start:chunk_start + 5000]
    checks = [
        HERO_TITLE in chunk,
        escape(HERO_KICKER) in chunk,
        HERO_LEAD[:40] in chunk,
        'href="/shop"' in chunk,
        HERO_CTA_SHOP_LABEL in chunk,
        'href="/professionnels"' in chunk,
        HERO_CTA_PRO_LABEL in chunk,
        'ck-hero__visual' in chunk,
    ]
    if not all(checks):
        return False
    lowered = chunk.lower()
    if any(marker in lowered for marker in _COVER_DEFAULT_MARKERS):
        return False
    if 'ratio-16x10' in chunk:
        return False
    if 'ck-hero__visual-media' not in chunk and 'ck-hero__visual--editorial' not in chunk:
        return False
    hero_pos = arch.find(HERO_VARIANT_MARKER)
    featured_pos = arch.find('ck-featured-products')
    if featured_pos >= 0 and hero_pos >= featured_pos:
        return False
    return True


def bootstrap_home_hero(env):
    """V1 Hero home — remplace le hero existant par la variante maquette compacte."""
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

    if hero_home_arch_is_valid(arch):
        return True

    hero_arch = build_home_hero_arch(env)
    new_arch, patched = _patch_homepage_hero_arch(arch, hero_arch)
    if not patched or new_arch == arch:
        return patched

    view.write({'arch_db': new_arch})
    return hero_home_arch_is_valid(new_arch)
