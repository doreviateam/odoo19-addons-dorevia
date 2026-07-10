# -*- coding: utf-8 -*-
"""Home V1 Section 2 — trust-bar réassurance post-Hero (MOA maquette V1)."""
from xml.sax.saxutils import escape

from odoo.addons.dorevia_ck_marketone_content.home_hero import HERO_VARIANT_MARKER

REASSURANCE_TRUST_BAR_MARKER = 'ck-reassurance--trust-bar'
REASSURANCE_DATA_NAME = 'CK Réassurance trust-bar'
REASSURANCE_SNIPPET_MARKER = 'data-snippet="s_ck_reassurance"'
FEATURED_MARKER = 'ck-featured-products'

TRUST_BAR_ITEMS = (
    ('fa-truck', 'Livraison France & Europe', 'Expédition suivie, délais annoncés.'),
    ('fa-lock', 'Paiement sécurisé', 'Paiement en ligne simple et protégé.'),
    ('fa-leaf', 'Producteurs sélectionnés', 'Des produits choisis dans les territoires créolophones.'),
    ('fa-comment', 'Service client', 'Une question ? CK vous accompagne.'),
)
TRUST_BAR_COPY_MARKER = 'CK vous accompagne'


def _arch_as_string(arch):
    if isinstance(arch, dict):
        return next(iter(arch.values()), '')
    return arch or ''


def _trust_item_html(icon, title, text):
    title_esc = escape(title)
    text_esc = escape(text)
    return (
        f'<div class="ck-reassurance__item o_colored_level">'
        f'<span class="ck-reassurance__icon fa {icon}" aria-hidden="true"></span>'
        f'<div class="ck-reassurance__copy">'
        f'<h3 class="ck-reassurance__title">{title_esc}</h3>'
        f'<p class="ck-reassurance__text">{text_esc}</p>'
        f'</div>'
        f'</div>'
    )


def build_home_reassurance_arch():
    """Bandeau horizontal compact — wording client MOA Section 2."""
    items = ''.join(_trust_item_html(*item) for item in TRUST_BAR_ITEMS)
    return (
        f'<section class="s_ck_reassurance ck-reassurance {REASSURANCE_TRUST_BAR_MARKER} o_colored_level" '
        f'{REASSURANCE_SNIPPET_MARKER} data-name="{REASSURANCE_DATA_NAME}" '
        f'aria-label="Preuves de confiance">'
        f'<div class="container">'
        f'<div class="ck-reassurance__grid">{items}</div>'
        f'</div>'
        f'</section>'
    )


def _find_reassurance_block_bounds(arch):
    idx = arch.find(REASSURANCE_SNIPPET_MARKER)
    if idx < 0:
        return -1, -1
    start = arch.rfind('<section', 0, idx)
    end = arch.find('</section>', idx)
    if start < 0 or end < 0:
        return -1, -1
    return start, end + len('</section>')


def reassurance_home_arch_is_valid(arch):
    """Recette Section 2 : trust-bar maquette · position entre Hero et Vedettes."""
    if REASSURANCE_TRUST_BAR_MARKER not in arch:
        return False
    if 'Livraison France &amp; Europe' not in arch and 'Livraison France & Europe' not in arch:
        return False
    if TRUST_BAR_COPY_MARKER not in arch:
        return False
    if 'parcours checkout natif' in arch or 'conditions Pro sur qualification' in arch:
        return False
    if 'Sélection créole' in arch or 'Livraison soignée' in arch:
        return False
    hero_pos = arch.find(HERO_VARIANT_MARKER)
    reassurance_pos = arch.find(REASSURANCE_TRUST_BAR_MARKER)
    featured_pos = arch.find(FEATURED_MARKER)
    if hero_pos < 0 or reassurance_pos < 0 or featured_pos < 0:
        return False
    return hero_pos < reassurance_pos < featured_pos


def _patch_homepage_reassurance_arch(arch, reassurance_arch):
    start, end = _find_reassurance_block_bounds(arch)
    if start < 0 or end < 0:
        if REASSURANCE_TRUST_BAR_MARKER in arch:
            return arch, False
        for marker in (
            HERO_VARIANT_MARKER,
            'data-snippet="s_ck_hero"',
            'class="s_ck_hero',
        ):
            marker_pos = arch.find(marker)
            if marker_pos < 0:
                continue
            section_end = arch.find('</section>', marker_pos)
            if section_end < 0:
                continue
            insert_at = section_end + len('</section>')
            return arch[:insert_at] + '\n' + reassurance_arch + '\n' + arch[insert_at:], True
        return arch, False
    return arch[:start] + reassurance_arch + arch[end:], True


def _bootstrap_home_reassurance_lang(env, page):
    """Patch trust-bar pour la langue courante de ``env``."""
    view = page.view_id.with_env(env).sudo()
    arch = _arch_as_string(view.arch_db or view.arch)
    if not arch.strip():
        return False

    if REASSURANCE_TRUST_BAR_MARKER in arch:
        hero_pos = arch.find(HERO_VARIANT_MARKER)
        reassurance_pos = arch.find(REASSURANCE_TRUST_BAR_MARKER)
        if hero_pos >= 0 and reassurance_pos > hero_pos:
            return False

    reassurance_arch = build_home_reassurance_arch()
    new_arch, patched = _patch_homepage_reassurance_arch(arch, reassurance_arch)
    if not patched or new_arch == arch:
        if REASSURANCE_TRUST_BAR_MARKER in arch:
            return False
        raise ValueError(
            'CK home réassurance : impossible d\'insérer le bloc trust-bar après le hero'
        )

    view.write({'arch_db': new_arch})
    if REASSURANCE_TRUST_BAR_MARKER not in new_arch:
        raise ValueError('CK home réassurance : bloc trust-bar absent après insertion')
    hero_pos = new_arch.find(HERO_VARIANT_MARKER)
    reassurance_pos = new_arch.find(REASSURANCE_TRUST_BAR_MARKER)
    if hero_pos < 0 or reassurance_pos < 0 or hero_pos >= reassurance_pos:
        raise ValueError(
            'CK home réassurance : trust-bar mal positionnée par rapport au hero'
        )
    return True


def bootstrap_home_reassurance(env):
    """Section 2 home — remplace le bloc réassurance cartes par la trust-bar maquette."""
    from .home_featured import _featured_target_langs

    website = env['website'].search([], limit=1)
    if not website:
        return False

    page = env['website.page'].sudo().search([
        ('url', '=', '/'),
        ('website_id', '=', website.id),
    ], limit=1)
    if not page or not page.view_id:
        return False

    changed = False
    for lang in _featured_target_langs(env, website):
        lang_env = env(context=dict(env.context, lang=lang))
        if _bootstrap_home_reassurance_lang(lang_env, page):
            changed = True
    return changed or True
