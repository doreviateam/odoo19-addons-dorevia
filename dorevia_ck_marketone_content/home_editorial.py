# -*- coding: utf-8 -*-
"""Home Lot 5 — Bloc éditorial bas de page (MOA maquette V1)."""
from xml.sax.saxutils import escape

EDITORIAL_SECTION_MARKER = 'ck-home-editorial'
EDITORIAL_DATA_NAME = 'CK Éditorial bas de page'
EDITORIAL_TITLE = 'C-Kreyol, la boutique des saveurs créoles'
EDITORIAL_LEAD = (
    'CK met en ligne une sélection d\'agro-produits transformés dans les '
    'territoires créolophones. Notre mission : rendre l\'achat simple, les '
    'prix lisibles et la provenance compréhensible — pour les particuliers '
    'comme pour les professionnels qualifiés.'
)
EDITORIAL_CLOSING = (
    'Chaque fiche produit raconte l\'origine, l\'usage et le producteur.'
)
EDITORIAL_LINK_DEMARCHE_LABEL = 'Notre démarche →'
EDITORIAL_LINK_PRODUCER_LABEL = 'Fiche producteur →'
EDITORIAL_LINK_RECIPES_LABEL = 'Recettes &amp; savoirs →'
EDITORIAL_LINK_RECIPES_TEXT = 'Recettes & savoirs →'

EDITORIAL_LINK_A_PROPOS = '/a-propos'
EDITORIAL_LINK_PRODUCER = '/producteur/atelier-hauts-goyaviers'
EDITORIAL_LINK_RECIPES = '/recettes'

_TECHNICAL_MARKERS = (
    'inspiration réf.',
    'route-hint',
    'maquette complémentaire',
    'TODO',
    'FIXME',
)


def _arch_as_string(arch):
    if isinstance(arch, dict):
        return next(iter(arch.values()), '')
    return arch or ''


def build_home_editorial_arch():
    """Section éditoriale narrative CK · liens démarche / producteur / recettes."""
    title = escape(EDITORIAL_TITLE)
    lead = escape(EDITORIAL_LEAD)
    closing = escape(EDITORIAL_CLOSING)
    link_demarche = escape(EDITORIAL_LINK_DEMARCHE_LABEL)
    link_producer = escape(EDITORIAL_LINK_PRODUCER_LABEL)
    link_recipes = EDITORIAL_LINK_RECIPES_LABEL
    return f"""
<section class="s_text_block {EDITORIAL_SECTION_MARKER} pt48 pb48 o_colored_level" data-snippet="s_text_block" data-name="{EDITORIAL_DATA_NAME}">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-8 col-xl-7 o_colored_level">
                <h2 class="h4 mb-3">{title}</h2>
                <p class="text-muted mb-3">{lead}</p>
                <p class="mb-0">{closing}
                    <a href="{EDITORIAL_LINK_A_PROPOS}" class="fw-bold">{link_demarche}</a>
                    ·
                    <a href="{EDITORIAL_LINK_PRODUCER}" class="fw-bold">{link_producer}</a>
                    ·
                    <a href="{EDITORIAL_LINK_RECIPES}" class="fw-bold">{link_recipes}</a>
                </p>
            </div>
        </div>
    </div>
</section>
""".strip()


def _find_editorial_block_bounds(arch):
    start = arch.find(f'class="s_text_block {EDITORIAL_SECTION_MARKER}')
    if start < 0:
        idx = arch.find(f'data-name="{EDITORIAL_DATA_NAME}"')
        if idx >= 0:
            start = arch.rfind('<section', 0, idx)
    if start < 0:
        return -1, -1
    end = arch.find('</section>', start)
    if end < 0:
        return start, -1
    return start, end + len('</section>')


def _find_editorial_insertion_index(arch):
    for marker in (
        'class="s_text_block ck-dual-engage',
        'data-name="CK Dual Pro Newsletter home"',
        'ck-dual-engage--compact',
    ):
        idx = arch.find(marker)
        if idx < 0:
            continue
        section_start = arch.rfind('<section', 0, idx) if 'data-name' not in marker else idx
        if section_start < 0:
            section_start = idx
        section_close = arch.find('</section>', section_start)
        if section_close >= 0:
            return section_close + len('</section>')
    return -1


def _patch_homepage_editorial_arch(arch, editorial_arch):
    start, end = _find_editorial_block_bounds(arch)
    if start >= 0 and end >= 0:
        return arch[:start] + editorial_arch + arch[end:], True

    insert_at = _find_editorial_insertion_index(arch)
    if insert_at < 0:
        return arch, False
    new_arch = arch[:insert_at] + '\n' + editorial_arch + arch[insert_at:]
    return new_arch, True


def editorial_home_arch_is_valid(arch):
    """Recette Lot 5 : titre CK · texte narratif · liens · après dual · pas de copy technique."""
    if EDITORIAL_SECTION_MARKER not in arch:
        return False
    chunk_start = arch.find(EDITORIAL_SECTION_MARKER)
    chunk = arch[chunk_start:chunk_start + 6000]
    checks = [
        EDITORIAL_TITLE in chunk,
        EDITORIAL_LEAD[:40] in chunk,
        f'href="{EDITORIAL_LINK_A_PROPOS}"' in chunk,
        f'href="{EDITORIAL_LINK_PRODUCER}"' in chunk,
        f'href="{EDITORIAL_LINK_RECIPES}"' in chunk,
        EDITORIAL_LINK_DEMARCHE_LABEL in chunk,
        EDITORIAL_LINK_PRODUCER_LABEL in chunk,
        EDITORIAL_LINK_RECIPES_LABEL in chunk or EDITORIAL_LINK_RECIPES_TEXT in chunk,
    ]
    if not all(checks):
        return False
    lowered = chunk.lower()
    if any(marker in lowered for marker in _TECHNICAL_MARKERS):
        return False
    dual_pos = arch.find('ck-dual-engage')
    edito_pos = arch.find(EDITORIAL_SECTION_MARKER)
    if dual_pos >= 0 and edito_pos >= 0 and not (dual_pos < edito_pos):
        return False
    if 'pt48 pb48' not in chunk:
        return False
    return True


def bootstrap_home_editorial(env):
    """Lot 5 home — bloc éditorial bas de page après dual Pro/Newsletter."""
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

    if editorial_home_arch_is_valid(arch):
        return True

    editorial_arch = build_home_editorial_arch()
    new_arch, patched = _patch_homepage_editorial_arch(arch, editorial_arch)
    if not patched or new_arch == arch:
        return patched

    view.write({'arch_db': new_arch})
    return editorial_home_arch_is_valid(new_arch)
