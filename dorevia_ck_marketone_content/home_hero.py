# -*- coding: utf-8 -*-
"""Home V1 Hero / Lot 1 — rapprochement maquette (MOA maquette V1)."""
import re
from xml.sax.saxutils import escape

# Visuel « bandeau crêpes manioc » recadré pour un crop carrousel peu profond :
# sujet centré verticalement dans le fichier source (cf. ck_hero_crepe_manioc.webp).
HERO_CREPE_FOCAL_SRC = '/dorevia_ck_marketone_content/static/img/ck_hero_crepe_manioc.webp'
HERO_CREPE_FOCAL_ALT = 'Galettes de manioc créoles dorées'
_HERO_LEGACY_FOCAL_CLASS = ' ck-hero__slide-media--focal-product'

HERO_VARIANT_MARKER = 'ck-hero--marketone-v1'
HERO_GRID_POC_MARKER = 'ck-grid-poc'
HERO_DATA_NAME = 'CK Hero home V1'
HERO_KICKER = 'Produits créoles · Producteurs · Savoir-faire'
HERO_TITLE = 'C-Kréyòl — les saveurs créoles en Europe'
HERO_LEAD = (
    "Une sélection de produits, producteurs et savoir-faire créoles, "
    "à découvrir depuis la France et l'Europe."
)
HERO_CTA_SHOP_LABEL = 'Découvrir la boutique'
HERO_CTA_PRODUCTEURS_LABEL = 'Voir les producteurs'
HERO_VISUAL_ALT = 'Sélection de produits créoles — épicerie et condiments'
HERO_CAROUSEL_ID = 'ckHeroVisualCarousel'
HERO_CAROUSEL_MARKER = 'ck-hero__visual-carousel'
HERO_CAROUSEL_INTERVAL_MS = 25000
HERO_SLIDE_SNIPPET = 's_ck_hero_slide'
HERO_EDITABLE_MEDIA_MARKER = 'o_editable_media'
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
    data_name = escape(f'Visuel hero {index + 1}')
    image = escape(src)
    return (
        f'<div class="carousel-item{active_class}" data-snippet="{HERO_SLIDE_SNIPPET}" '
        f'data-name="{data_name}">'
        f'<div class="ck-hero__slide-media o_editable">'
        f'<p class="o_not_editable" contenteditable="false">'
        f'<img src="{image}" class="ck-hero__visual-media {HERO_EDITABLE_MEDIA_MARKER} d-block w-100" '
        f'alt="{escape(alt)}" loading="{"eager" if active else "lazy"}" '
        f'width="800" height="500"/>'
        f'</p>'
        f'</div>'
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
    pause_btn = ''
    if len(slides) > 1:
        pause_btn = (
            '<button type="button" class="ck-hero__visual-pause" aria-pressed="false" '
            'aria-label="Mettre en pause le défilement automatique des visuels">'
            '<i class="fa fa-pause" aria-hidden="true"/></button>'
        )
    return (
        f'<div class="ck-hero__visual">'
        f'<div id="{HERO_CAROUSEL_ID}" '
        f'class="carousel slide {HERO_CAROUSEL_MARKER}{multi_class}"{ride_attrs}>'
        f'<div class="carousel-indicators ck-hero__visual-indicators">{indicators}</div>'
        f'<div class="carousel-inner">{items}</div>'
        f'{pause_btn}'
        f'</div>'
        f'</div>'
    )


def build_home_hero_arch(env):
    """Hero compact maquette V1 · kicker · dual CTA · carrousel visuel image-only."""
    kicker = escape(HERO_KICKER)
    title = escape(HERO_TITLE)
    lead = escape(HERO_LEAD)
    cta_shop = escape(HERO_CTA_SHOP_LABEL)
    cta_producteurs = escape(HERO_CTA_PRODUCTEURS_LABEL)
    visual = _hero_visual_html()
    return f"""
<section class="s_ck_hero ck-hero {HERO_VARIANT_MARKER} {HERO_GRID_POC_MARKER} ck-grid-spread o_colored_level" data-snippet="s_ck_hero" data-name="{HERO_DATA_NAME}">
    <div class="container ck-grid-wrap">
        <div class="ck-guides" aria-hidden="true">
            <div class="ck-guides__cols"></div>
            <div class="ck-guides__rows"></div>
            <div class="ck-guides__mline ck-guides__mline--l"></div>
            <div class="ck-guides__mline ck-guides__mline--r"></div>
        </div>
        <div class="ck-grid">
        <div class="ck-hero__grid ck-grid-band">
            <div class="ck-hero__content o_colored_level">
                <p class="ck-hero__kicker">{kicker}</p>
                <h1 class="ck-hero__title">{title}</h1>
                <p class="ck-hero__lead">{lead}</p>
                <div class="ck-hero__cta">
                    <a href="/shop" class="btn btn-primary">{cta_shop}</a>
                    <a href="/producteurs" class="btn btn-secondary">{cta_producteurs}</a>
                </div>
            </div>
            <div class="ck-hero__visual-col">
                {visual}
            </div>
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


def _inject_into_empty_homepage_wrap(arch, inner_html):
    """Installe du contenu dans la home vide Odoo 19 (parcours install fraîche)."""
    if 'oe_empty' not in arch:
        return arch, False
    new_arch, count = re.subn(
        r'<div id="wrap" class="oe_structure oe_empty"\s*/>',
        f'<div id="wrap" class="oe_structure">\n{inner_html}\n</div>',
        arch,
        count=1,
    )
    if count:
        return new_arch, True
    new_arch, count = re.subn(
        r'<div id="wrap" class="oe_structure oe_empty">\s*</div>',
        f'<div id="wrap" class="oe_structure">\n{inner_html}\n</div>',
        arch,
        count=1,
    )
    return (new_arch, bool(count)) if count else (arch, False)


def _prepend_hero_into_homepage_wrap(arch, inner_html):
    """Insère le hero en tête du wrap si d'autres blocs home ont déjà été posés."""
    if HERO_VARIANT_MARKER in arch:
        return arch, False
    match = re.search(r'<div id="wrap"[^>]*>', arch)
    if not match:
        return arch, False
    insert_at = match.end()
    return arch[:insert_at] + '\n' + inner_html + '\n' + arch[insert_at:], True


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
        HERO_GRID_POC_MARKER in chunk,
        'ck-grid-band' in chunk,
        escape(HERO_KICKER) in chunk,
        HERO_LEAD[:40] in chunk,
        'href="/shop"' in chunk,
        HERO_CTA_SHOP_LABEL in chunk,
        'href="/producteurs"' in chunk,
        HERO_CTA_PRODUCTEURS_LABEL in chunk,
        'ck-hero__visual' in chunk,
        'ck-hero__grid' in chunk,
        HERO_CAROUSEL_MARKER in chunk,
        HERO_VISUAL_STATIC_MARKER in chunk,
        'ck-hero__visual-media' in chunk,
        slide_count >= 1,
        slide_count <= HERO_VISUAL_MAX_SLIDES,
        visual_chunk.count(HERO_EDITABLE_MEDIA_MARKER) == slide_count,
        visual_chunk.count(f'data-snippet="{HERO_SLIDE_SNIPPET}"') == slide_count,
        'ck-hero__slide-media o_editable' in visual_chunk,
    ]
    if slide_count > 1:
        checks.append('ck-hero__visual-pause' in visual_chunk)
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
    from .home_page import ensure_website_homepage_page, remove_global_homepage_conflicts

    website = env['website'].search([], limit=1)
    if not website:
        return False

    page = ensure_website_homepage_page(env, website)
    if not page or not page.view_id:
        return False

    view = page.view_id.sudo()
    arch = _arch_as_string(view.arch_db or view.arch)
    if not arch.strip():
        return False

    if hero_home_arch_is_valid(arch):
        remove_global_homepage_conflicts(env)
        return True

    hero_arch = build_home_hero_arch(env)
    new_arch, patched = _patch_homepage_hero_arch(arch, hero_arch)
    if not patched:
        new_arch, patched = _inject_into_empty_homepage_wrap(arch, hero_arch)
    if not patched:
        new_arch, patched = _prepend_hero_into_homepage_wrap(arch, hero_arch)
    if not patched or new_arch == arch:
        return patched

    view.write({'arch_db': new_arch})
    if not page.is_published:
        page.write({'is_published': True})
    remove_global_homepage_conflicts(env)
    return hero_home_arch_is_valid(new_arch)


def repair_hero_crepe_focal(arch):
    """Stabilise le visuel crêpes manioc du hero (idempotent).

    - remplace l'ancienne image (attachment /web/image ou png source) par le
      fichier statique recadré centré ``ck_hero_crepe_manioc.webp`` ;
    - purge les métadonnées éditeur périmées (data-original-src, etc.) sur ce
      visuel pour qu'il soit traité comme une image statique propre ;
    - retire la classe ``ck-hero__slide-media--focal-product`` (override CSS
      ``object-position: 78%`` supprimé : cause de la divergence builder/public).

    Renvoie ``(new_arch, changed)``.
    """
    if not arch:
        return arch, False
    new_arch = arch

    if _HERO_LEGACY_FOCAL_CLASS in new_arch:
        new_arch = new_arch.replace(_HERO_LEGACY_FOCAL_CLASS, '')

    if 'crepe_manio' in new_arch or 'ck_hero_crepe_manioc' in new_arch:
        clean_img = (
            f'<img src="{HERO_CREPE_FOCAL_SRC}" '
            f'alt="{escape(HERO_CREPE_FOCAL_ALT)}" '
            f'class="ck-hero__visual-media {HERO_EDITABLE_MEDIA_MARKER} d-block w-100" '
            f'loading="eager" width="800" height="500"/>'
        )
        new_arch = re.sub(
            r'<img\b[^>]*?(?:crepe_manio|ck_hero_crepe_manioc)[^>]*?/?>',
            clean_img,
            new_arch,
            count=1,
        )

    return new_arch, (new_arch != arch)


def normalize_homepage_hero_crepe(env):
    """Applique ``repair_hero_crepe_focal`` sur la home (sudo, idempotent)."""
    from .home_page import get_website_homepage_page

    if not env.is_superuser():
        env = env(su=True)
    _website, page = get_website_homepage_page(env)
    if not page or not page.view_id:
        return False
    view = page.view_id.sudo()
    arch = _arch_as_string(view.arch_db or view.arch)
    new_arch, changed = repair_hero_crepe_focal(arch)
    if changed:
        view.write({'arch_db': new_arch})
    return changed
