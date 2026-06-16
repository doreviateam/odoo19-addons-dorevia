# -*- coding: utf-8 -*-
"""Home Section 4 — Acheter par univers · 3 cards visuelles catalogue."""
from xml.sax.saxutils import escape

UNIVERS_SECTION_MARKER = 'ck-univers-cards'
UNIVERS_DATA_NAME = 'CK Acheter par univers'
UNIVERS_TITLE = 'Acheter par univers'
UNIVERS_INTRO = 'Trois univers pour entrer dans la boutique en un clic.'

_UNIVERS_CARD_SPECS = (
    {
        'code': 'epicerie',
        'category_name': 'Épicerie créole',
        'title': 'Épicerie créole',
        'description': 'Farines, confitures, condiments et douceurs à découvrir.',
        'cta': "Voir l'épicerie",
        'image': '/dorevia_ck_marketone_content/static/img/ck_univers_epicerie.jpg',
    },
    {
        'code': 'soin',
        'category_name': 'Maison & bien-être',
        'title': 'Soin & bien-être',
        'description': 'Savons, soins et produits bien-être pour le corps et le quotidien.',
        'cta': 'Découvrir les soins',
        'image': '/dorevia_ck_marketone_content/static/img/ck_univers_soin.jpg',
    },
    {
        'code': 'artisanat',
        'category_name': 'Artisanat',
        'title': 'Artisanat & culture',
        'description': 'Objets, créations et supports culturels à découvrir ou offrir.',
        'cta': "Explorer l'artisanat",
        'image': '/dorevia_ck_marketone_content/static/img/ck_univers_artisanat.jpg',
    },
)

def _arch_as_string(arch):
    if isinstance(arch, dict):
        return next(iter(arch.values()), '')
    return arch or ''


def _category_shop_url(env, category):
    if not category:
        return '/shop'
    slug = env['ir.http'].sudo()._slug(category)
    return f'/shop/category/{slug}'


def _resolve_univers_cards(env):
    """Retourne les 3 cards avec URL catégorie BO (fallback /shop si absente)."""
    Category = env['product.public.category'].sudo()
    cards = []
    for spec in _UNIVERS_CARD_SPECS:
        category = Category.search([('name', '=', spec['category_name'])], limit=1)
        cards.append({
            **spec,
            'href': _category_shop_url(env, category),
        })
    return cards


def _build_univers_card_html(card):
    title = escape(card['title'])
    description = escape(card['description'])
    cta = escape(card['cta'])
    href = escape(card['href'])
    image = escape(card['image'])
    return f"""
            <a href="{href}" class="ck-univers-card ck-univers-card--{escape(card['code'])}">
                <div class="ck-univers-card__media" style="background-image: url('{image}');" role="img" aria-label="{title}"></div>
                <div class="ck-univers-card__overlay">
                    <h3 class="ck-univers-card__title">{title}</h3>
                    <p class="ck-univers-card__desc">{description}</p>
                    <span class="ck-univers-card__cta">{cta}</span>
                </div>
            </a>""".strip()


def build_home_univers_arch(env):
    cards = _resolve_univers_cards(env)
    if len(cards) != 3:
        return ''
    cards_inner = '\n            '.join(_build_univers_card_html(card) for card in cards)
    title = escape(UNIVERS_TITLE)
    intro = escape(UNIVERS_INTRO)
    return f"""
<section class="s_ck_univers_cards {UNIVERS_SECTION_MARKER} pt40 pb48 o_colored_level" data-snippet="s_ck_univers_cards" data-name="{UNIVERS_DATA_NAME}">
    <div class="container">
        <div class="ck-univers-cards__head text-center mb-4">
            <h2 id="univers-title" class="ck-univers-cards__title h3 mb-2 o_editable">{title}</h2>
            <p class="ck-univers-cards__intro mb-0 o_editable">{intro}</p>
        </div>
        <div class="ck-univers-cards__grid">
            {cards_inner}
        </div>
    </div>
</section>
""".strip()


def _remove_univers_sections(arch):
    while True:
        marker = arch.find(UNIVERS_SECTION_MARKER)
        if marker < 0:
            marker = arch.find('data-snippet="s_ck_univers_cards"')
        if marker < 0:
            break
        start = arch.rfind('<section', 0, marker)
        if start < 0:
            break
        close = arch.find('</section>', marker)
        if close < 0:
            break
        arch = arch[:start] + arch[close + len('</section>'):]
    return arch


def _remove_legacy_category_links(arch):
    """Retire l'ancienne section pills « Nos univers » si présente."""
    while True:
        marker = arch.find('data-snippet="s_ck_category_links"')
        if marker < 0:
            break
        start = arch.rfind('<section', 0, marker)
        if start < 0:
            break
        close = arch.find('</section>', marker)
        if close < 0:
            break
        arch = arch[:start] + arch[close + len('</section>'):]
    return arch


def _find_univers_insertion_index(arch):
    """Insère après Section 3 Coups de cœur."""
    marker = arch.find('data-snippet="s_ck_featured_products"')
    if marker >= 0:
        end = arch.find('</section>', marker)
        if end >= 0:
            return end + len('</section>')
    for anchor in ('ck-reassurance--trust-bar', 'data-snippet="s_ck_reassurance"',
                   'data-snippet="s_ck_hero"'):
        pos = arch.find(anchor)
        if pos >= 0:
            end = arch.find('</section>', pos)
            if end >= 0:
                return end + len('</section>')
    return -1


def find_univers_section_end_index(arch):
    """Index après la section univers — pour insertion Coffrets découverte."""
    marker = arch.find(UNIVERS_SECTION_MARKER)
    if marker < 0:
        marker = arch.find('data-snippet="s_ck_univers_cards"')
    if marker < 0:
        return -1
    end = arch.find('</section>', marker)
    if end < 0:
        return -1
    return end + len('</section>')


def _patch_homepage_univers_arch(arch, univers_arch):
    cleaned = _remove_legacy_category_links(_remove_univers_sections(arch))
    if not univers_arch:
        return cleaned, cleaned != arch

    insert_at = _find_univers_insertion_index(cleaned)
    if insert_at < 0:
        return arch, False
    tail = cleaned[insert_at:].lstrip('\n')
    new_arch = cleaned[:insert_at].rstrip() + '\n' + univers_arch + '\n' + tail
    return new_arch, True


def univers_arch_is_valid(arch):
    if UNIVERS_SECTION_MARKER not in arch:
        return False
    chunk_start = arch.find(UNIVERS_SECTION_MARKER)
    chunk = arch[chunk_start:chunk_start + 12000]
    if UNIVERS_TITLE not in chunk or UNIVERS_INTRO not in chunk:
        return False
    if chunk.count('ck-univers-card--') != 3:
        return False
    if 'data-bs-ride="carousel"' in chunk:
        return False
    if 'route-hint' in chunk:
        return False
    if 'Packs & découvertes' in chunk or 'packs-decouvertes' in chunk:
        return False
    for spec in _UNIVERS_CARD_SPECS:
        if escape(spec['title']) not in chunk and spec['title'] not in chunk:
            return False
        if escape(spec['cta']) not in chunk and spec['cta'] not in chunk:
            return False
    return True


def bootstrap_home_univers(env):
    """Section 4 home — injecte la grille 3 univers visuels après Coups de cœur."""
    if not env.is_superuser():
        env = env(su=True)
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

    if univers_arch_is_valid(arch) and 'data-snippet="s_ck_category_links"' not in arch:
        return True

    univers_arch = build_home_univers_arch(env)
    if not univers_arch:
        return False

    new_arch, patched = _patch_homepage_univers_arch(arch, univers_arch)
    if not patched:
        return univers_arch_is_valid(arch)
    if new_arch == arch:
        return univers_arch_is_valid(arch)

    view.write({'arch_db': new_arch})
    return univers_arch_is_valid(new_arch)
