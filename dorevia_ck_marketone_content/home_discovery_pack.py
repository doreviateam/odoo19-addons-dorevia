# -*- coding: utf-8 -*-
"""Home Lot 3 — Coffrets découverte (MOA maquette V1)."""
import re
from xml.sax.saxutils import escape

from lxml import etree

DISCOVERY_PACK_BOOTSTRAP_ICP = 'ck.marketone.discovery_pack_bootstrap_enabled'
DISCOVERY_PACK_SECTION_MARKER = 'ck-discovery-pack'
DISCOVERY_PACK_STATIC_IMAGE = '/dorevia_ck_marketone_content/static/img/ck_discovery_pack.jpg'
DISCOVERY_PACK_DATA_NAME = 'CK Coffrets découverte'
DISCOVERY_PACK_CTA_URL = '/kits'
DISCOVERY_PACK_CTA_LABEL = 'Découvrir'
DISCOVERY_PACK_BADGE = 'Pack'
DISCOVERY_PACK_TITLE = 'Coffrets découverte'
DISCOVERY_PACK_LEAD = (
    'Idéal première commande ou cadeau — kits et coffrets gourmands '
    'pour découvrir l\'épicerie créole CK.'
)
DISCOVERY_PACK_EDITORIAL_NAME = 'Coffret découverte créole'
DISCOVERY_PACK_EDITORIAL_TEASER = (
    'Assortiment épicerie créole — sélection CK pour une première commande ou un cadeau.'
)

_PLACEHOLDER_IMAGE_MARKERS = (
    'website.s_cover_default_image',
    's_cover_default',
)


def _discovery_pack_bootstrap_enabled(env):
    """True sauf opt-out MOA explicite (chaîne ``'False'``). Absent = legacy True."""
    raw = env['ir.config_parameter'].sudo().get_param(
        DISCOVERY_PACK_BOOTSTRAP_ICP, 'True')
    return raw != 'False'


def _arch_as_string(arch):
    if isinstance(arch, dict):
        return next(iter(arch.values()), '')
    return arch or ''


def _format_price(product, env):
    if not product:
        return ''
    currency = product.currency_id or env.company.currency_id
    amount = product._get_contextual_price() if hasattr(product, '_get_contextual_price') else product.list_price
    return env['ir.qweb.field.monetary'].value_to_html(amount, {'display_currency': currency})


def get_discovery_pack_product(env):
    """Produit pack/coffret publié avec image BO — sinon vide (carte éditoriale)."""
    Product = env['product.template'].sudo()
    base_domain = [
        ('is_published', '=', True),
        ('website_published', '=', True),
        ('sale_ok', '=', True),
        ('image_1920', '!=', False),
    ]
    if 'pack_ok' in Product._fields:
        product = Product.search(base_domain + [('pack_ok', '=', True)], limit=1, order='website_sequence asc, id asc')
        if product:
            return product
    product = Product.search(base_domain + [('name', 'ilike', 'coffret')], limit=1, order='website_sequence asc, id asc')
    return product


def _discovery_visual_html(product):
    if product and product.image_1920:
        alt = escape(product.name or DISCOVERY_PACK_EDITORIAL_NAME)
        inner = (
            f'<img src="/web/image/product.template/{product.id}/image_512" '
            f'class="object-fit-cover w-100 h-100" alt="{alt}" loading="lazy"/>'
        )
        visual = (
            f'<div class="ck-discovery-pack__visual ratio ratio-4x3 rounded overflow-hidden h-100" '
            f'style="min-height: 180px;">{inner}</div>'
        )
        if product.website_url:
            return (
                f'<a href="{escape(product.website_url)}" class="d-block h-100 text-decoration-none">'
                f'{visual}</a>'
            )
        return visual
    alt = escape(DISCOVERY_PACK_EDITORIAL_NAME)
    return (
        f'<div class="ck-discovery-pack__visual ratio ratio-4x3 rounded overflow-hidden h-100" '
        f'style="min-height: 180px;">'
        f'<img src="{DISCOVERY_PACK_STATIC_IMAGE}" '
        f'class="object-fit-cover w-100 h-100" alt="{alt}" loading="lazy"/>'
        f'</div>'
    )


def build_discovery_pack_arch(env):
    """Section horizontale Coffrets découverte · CTA /kits · badge Pack."""
    product = get_discovery_pack_product(env)
    name = escape(product.name if product else DISCOVERY_PACK_EDITORIAL_NAME)
    teaser = escape(
        (product.description_sale or '').strip()[:180]
        if product and (product.description_sale or '').strip()
        else DISCOVERY_PACK_EDITORIAL_TEASER
    )
    price_html = _format_price(product, env) if product else ''
    price_block = (
        f'<span class="ck-discovery-pack__price fw-bold fs-5 mb-0">{price_html}</span>'
        if price_html else ''
    )
    product_link = ''
    if product and product.website_url:
        product_link = (
            f'<a href="{escape(product.website_url)}" class="text-decoration-none text-reset">'
            f'{name}</a>'
        )
    else:
        product_link = f'<span>{name}</span>'

    return f"""
<section class="s_text_block ck-discovery-pack ck-discovery-pack--polish-v1 pt48 pb48 o_colored_level" data-snippet="s_text_block" data-name="{DISCOVERY_PACK_DATA_NAME}">
    <div class="container">
        <h2 class="ck-section-title h3 mb-2">{DISCOVERY_PACK_TITLE}</h2>
        <p class="text-muted mb-4">{DISCOVERY_PACK_LEAD}</p>
        <div class="ck-discovery-pack__card overflow-hidden">
            <div class="row g-0 align-items-stretch">
                <div class="col-12 col-md-5 col-lg-4 p-3 p-md-4">
                    {_discovery_visual_html(product)}
                </div>
                <div class="col-12 col-md-7 col-lg-8 p-3 p-md-4 d-flex flex-column justify-content-center">
                    <span class="badge ck-discovery-pack__badge rounded-pill align-self-start mb-2">{DISCOVERY_PACK_BADGE}</span>
                    <h3 class="h5 mb-2">{product_link}</h3>
                    <p class="text-muted mb-3 mb-md-4">{teaser}</p>
                    <div class="ck-discovery-pack__actions d-flex flex-wrap align-items-center justify-content-between gap-3 mt-auto">
                        {price_block}
                        <a href="{DISCOVERY_PACK_CTA_URL}" class="btn btn-primary ck-discovery-pack__cta">{DISCOVERY_PACK_CTA_LABEL}</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
""".strip()


def _remove_discovery_pack_sections(arch):
    """Retire toutes les sections ``ck-discovery-pack`` (parsing etree XML — CODE-004 R-B)."""
    if DISCOVERY_PACK_SECTION_MARKER not in arch:
        return arch, False
    root = etree.fromstring(f'<ck-root>{arch}</ck-root>')
    removed = False
    for section in root.xpath('.//section[contains(@class, "ck-discovery-pack")]'):
        parent = section.getparent()
        if parent is not None:
            parent.remove(section)
            removed = True
    if not removed:
        return arch, False
    new_arch = ''.join(
        etree.tostring(child, encoding='unicode') for child in root
    )
    return new_arch, True


def _discovery_pack_opt_out_arch_is_valid(arch):
    """Opt-out MOA : section absente, pas de fuite markup."""
    if DISCOVERY_PACK_SECTION_MARKER in arch:
        return False
    return not _homepage_has_leaked_section_markup(arch)


def _dual_engage_boundary(arch, after=0):
    """Index de début du bloc dual / pro suivant (y compris fuite ``</section> class=``)."""
    leaked = re.search(
        r'</section>\s*(class="s_text_block ck-dual-engage)',
        arch[after:],
    )
    if leaked:
        return after + leaked.start(1)
    for needle in (
        '<section class="s_text_block ck-dual-engage',
        '<section class="s_ck_pro_banner',
        'class="s_text_block ck-dual-engage',
        'class="s_ck_pro_banner',
        'data-name="CK Dual Pro Newsletter',
    ):
        pos = arch.find(needle, after + 1)
        if pos >= 0:
            return pos
    return -1


def _discovery_pack_section_opens(arch):
    return re.findall(
        r'<section class="s_text_block ck-discovery-pack',
        arch,
    )


def _find_discovery_pack_bounds(arch):
    from .home_univers import find_univers_section_end_index

    univers_end = find_univers_section_end_index(arch)
    search_after = univers_end if univers_end >= 0 else 0
    end = _dual_engage_boundary(arch, search_after)
    if end < 0:
        return -1, -1

    needs_sweep = (
        _homepage_has_leaked_section_markup(arch)
        or len(_discovery_pack_section_opens(arch)) > 1
    )
    if needs_sweep and univers_end >= 0:
        return univers_end, end

    start = arch.find(
        f'<section class="s_text_block {DISCOVERY_PACK_SECTION_MARKER}',
        search_after,
    )
    if start < 0 or start >= end:
        marker = arch.find(f'data-name="{DISCOVERY_PACK_DATA_NAME}"', search_after)
        if marker >= 0:
            start = arch.rfind('<section', search_after, marker)
    if start < 0 or start >= end:
        start = search_after
    return start, end


def _find_discovery_pack_insertion_index(arch):
    from .home_univers import find_univers_section_end_index

    univers_end = find_univers_section_end_index(arch)
    if univers_end >= 0:
        return univers_end
    cat_end = arch.find('class="s_ck_category_links')
    if cat_end < 0:
        cat_end = arch.find('data-snippet="s_ck_category_links"')
        if cat_end >= 0:
            cat_end = arch.rfind('<section', 0, cat_end)
    if cat_end < 0:
        return -1
    insert_at = arch.find('<section class="s_text_block ck-dual-engage', cat_end)
    if insert_at < 0:
        insert_at = arch.find('<section class="s_ck_pro_banner', cat_end)
    return insert_at


def _patch_homepage_discovery_pack_arch(arch, discovery_arch):
    start, end = _find_discovery_pack_bounds(arch)
    if start >= 0 and end >= 0:
        new_arch = arch[:start] + discovery_arch + '\n' + arch[end:]
        return new_arch, True

    insert_at = _find_discovery_pack_insertion_index(arch)
    if insert_at < 0:
        return arch, False
    new_arch = arch[:insert_at] + discovery_arch + '\n' + arch[insert_at:]
    return new_arch, True


def _homepage_has_leaked_section_markup(arch):
    """True si une section home perd son ``<section`` ouvrant (fuite markup visible)."""
    return bool(re.search(
        r'</section>\s*class="s_text_block ck-(?:dual-engage|discovery-pack|home-editorial)',
        arch,
    ))


def discovery_pack_arch_is_valid(arch, env=None):
    """Recette legacy (section présente) ou opt-out MOA (section absente)."""
    if env is not None and not _discovery_pack_bootstrap_enabled(env):
        return _discovery_pack_opt_out_arch_is_valid(arch)
    if DISCOVERY_PACK_SECTION_MARKER not in arch:
        return False
    if _homepage_has_leaked_section_markup(arch):
        return False
    if len(_discovery_pack_section_opens(arch)) > 1:
        return False
    chunk_start = arch.find(DISCOVERY_PACK_SECTION_MARKER)
    chunk = arch[chunk_start:chunk_start + 8000]
    if f'href="{DISCOVERY_PACK_CTA_URL}"' not in chunk:
        return False
    if DISCOVERY_PACK_BADGE not in chunk:
        return False
    if 'ck-discovery-pack--polish-v1' not in chunk:
        return False
    if 'pt48 pb48' not in chunk:
        return False
    if 'stretched-link' in chunk:
        return False
    if 'ck-discovery-pack__actions' not in chunk:
        return False
    if 'fa-3x' in chunk:
        return False
    if 'ck-discovery-pack__visual--editorial' in chunk:
        return False
    if 'ck-discovery-pack__visual-icon' in chunk:
        return False
    if '/web/image/product.' not in chunk and DISCOVERY_PACK_STATIC_IMAGE not in chunk:
        return False
    lowered = chunk.lower()
    return not any(marker in lowered for marker in _PLACEHOLDER_IMAGE_MARKERS)


def bootstrap_home_discovery_pack(env):
    """Lot 3 home — injecte le bloc Coffrets découverte après les univers."""
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

    if not _discovery_pack_bootstrap_enabled(env):
        if _homepage_has_leaked_section_markup(arch):
            from .home_dual_engage import bootstrap_home_dual_engage

            bootstrap_home_dual_engage(env)
            arch = _arch_as_string(view.arch_db or view.arch)
        new_arch, removed = _remove_discovery_pack_sections(arch)
        if removed and new_arch != arch:
            view.write({'arch_db': new_arch})
            arch = new_arch
        return discovery_pack_arch_is_valid(arch, env=env)

    discovery_arch = build_discovery_pack_arch(env)
    if not discovery_arch:
        return False

    if _homepage_has_leaked_section_markup(arch):
        from .home_dual_engage import bootstrap_home_dual_engage

        bootstrap_home_dual_engage(env)
        arch = _arch_as_string(view.arch_db or view.arch)

    if discovery_pack_arch_is_valid(arch) and not _homepage_has_leaked_section_markup(arch):
        return True

    new_arch, patched = _patch_homepage_discovery_pack_arch(arch, discovery_arch)
    if not patched or new_arch == arch:
        return patched

    view.write({'arch_db': new_arch})
    if _homepage_has_leaked_section_markup(new_arch):
        from .home_dual_engage import bootstrap_home_dual_engage

        bootstrap_home_dual_engage(env)
        arch = _arch_as_string(view.arch_db or view.arch)
    return discovery_pack_arch_is_valid(arch) and not _homepage_has_leaked_section_markup(arch)
