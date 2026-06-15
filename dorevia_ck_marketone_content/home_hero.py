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
HERO_CAROUSEL_ID = 'ckHeroVisualCarousel'
HERO_CAROUSEL_MARKER = 'ck-hero__visual-carousel'
HERO_CAROUSEL_INTERVAL_MS = 25000
HERO_VISUAL_STATIC_MARKER = 'ck_hero_home_v1'
HERO_VISUAL_MAX_SLIDES = 3
HERO_VISUAL_IMAGES = (
    {
        'src': '/dorevia_ck_marketone_content/static/img/ck_hero_home_v1.jpg',
        'alt': HERO_VISUAL_ALT,
    },
    {
        'src': '/dorevia_ck_marketone_content/static/img/ck_hero_home_v2.jpg',
        'alt': 'Cuisine créole — plats et saveurs des îles',
    },
    {
        'src': '/dorevia_ck_marketone_content/static/img/ck_hero_home_v3.jpg',
        'alt': 'Produits frais et épicerie fine créole',
    },
)

_COVER_DEFAULT_MARKERS = (
    'website.s_cover_default_image',
    's_cover_default',
)


def _arch_as_string(arch):
    if isinstance(arch, dict):
        return next(iter(arch.values()), '')
    return arch or ''


def _hero_visual_slide_html(index, src, alt, *, active=False):
    active_class = ' active' if active else ''
    return (
        f'<div class="carousel-item{active_class}" data-name="Visuel hero {index + 1}">'
        f'<img src="{src}" class="ck-hero__visual-media d-block w-100" '
        f'alt="{escape(alt)}" loading="{"eager" if active else "lazy"}" '
        f'width="800" height="500"/>'
        f'</div>'
    )


def _hero_visual_indicator_html(index, *, active=False):
    active_attrs = ' class="active" aria-current="true"' if active else ''
    return (
        f'<button type="button" data-bs-target="#{HERO_CAROUSEL_ID}" '
        f'data-bs-slide-to="{index}"{active_attrs} '
        f'aria-label="Visuel {index + 1}"></button>'
    )


def _hero_visual_html():
    """Carrousel image-only dans le cadre visuel hero — max 3 visuels · dégradation 1 slide."""
    slides = HERO_VISUAL_IMAGES[:HERO_VISUAL_MAX_SLIDES]
    indicators = ''.join(
        _hero_visual_indicator_html(i, active=(i == 0))
        for i in range(len(slides))
    )
    items = ''.join(
        _hero_visual_slide_html(i, slide['src'], slide['alt'], active=(i == 0))
        for i, slide in enumerate(slides)
    )
    ride_attrs = (
        f' data-oe-protected="false" data-bs-ride="carousel" data-bs-interval="{HERO_CAROUSEL_INTERVAL_MS}" data-bs-pause="hover"'
        if len(slides) > 1
        else ''
    )
    multi_class = ' ck-hero__visual-carousel--multi' if len(slides) > 1 else ''
    return (
        f'<div class="ck-hero__visual">'
        f'<div id="{HERO_CAROUSEL_ID}" '
        f'class="carousel slide {HERO_CAROUSEL_MARKER}{multi_class}"{ride_attrs}>'
        f'<div class="carousel-indicators ck-hero__visual-indicators">{indicators}</div>'
        f'<div class="carousel-inner">{items}</div>'
        f'</div>'
        f'</div>'
    )


def build_home_hero_arch(env):
    """Hero compact maquette V1 · kicker · dual CTA · carrousel visuel image-only."""
    kicker = escape(HERO_KICKER)
    title = escape(HERO_TITLE)
    lead = escape(HERO_LEAD)
    cta_shop = escape(HERO_CTA_SHOP_LABEL)
    cta_pro = escape(HERO_CTA_PRO_LABEL)
    visual = _hero_visual_html()
    return f"""
<section class="s_ck_hero ck-hero {HERO_VARIANT_MARKER} o_colored_level" data-snippet="s_ck_hero" data-name="{HERO_DATA_NAME}">
    <div class="container">
        <div class="ck-hero__grid">
            <div class="ck-hero__content o_colored_level">
                <p class="ck-hero__kicker">{kicker}</p>
                <h1 class="ck-hero__title">{title}</h1>
                <p class="ck-hero__lead">{lead}</p>
                <div class="ck-hero__cta">
                    <a href="/shop" class="btn btn-primary">{cta_shop}</a>
                    <a href="/professionnels" class="btn btn-secondary">{cta_pro}</a>
                </div>
            </div>
            <div class="ck-hero__visual-col o_colored_level">
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
    """Recette Lot 1 : wording maquette · dual CTA · carrousel image-only dans cadre visuel."""
    if HERO_VARIANT_MARKER not in arch:
        return False
    chunk_start = arch.find(HERO_VARIANT_MARKER)
    chunk = arch[chunk_start:chunk_start + 8000]
    visual_col_start = chunk.find('ck-hero__visual-col')
    visual_chunk = chunk[visual_col_start:visual_col_start + 4000] if visual_col_start >= 0 else ''
    slide_count = visual_chunk.count('carousel-item')
    checks = [
        HERO_TITLE in chunk,
        escape(HERO_KICKER) in chunk,
        HERO_LEAD[:40] in chunk,
        'href="/shop"' in chunk,
        HERO_CTA_SHOP_LABEL in chunk,
        'href="/professionnels"' in chunk,
        HERO_CTA_PRO_LABEL in chunk,
        'ck-hero__visual' in chunk,
        'ck-hero__grid' in chunk,
        HERO_CAROUSEL_MARKER in chunk,
        HERO_VISUAL_STATIC_MARKER in chunk,
        'ck-hero__visual-media' in chunk,
        slide_count >= 1,
        slide_count <= HERO_VISUAL_MAX_SLIDES,
    ]
    if not all(checks):
        return False
    content_chunk = chunk.split('ck-hero__visual-col', 1)[0]
    if 'data-bs-ride="carousel"' in content_chunk:
        return False
    lowered = chunk.lower()
    if any(marker in lowered for marker in _COVER_DEFAULT_MARKERS):
        return False
    if 'ratio-16x10' in chunk:
        return False
    if '/web/image/product.template/' in visual_chunk:
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
