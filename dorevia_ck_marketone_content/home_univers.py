# -*- coding: utf-8 -*-
"""Home Section 4 — Acheter par univers · 4 cards visuelles catalogue."""
import re
from xml.sax.saxutils import escape

UNIVERS_SECTION_MARKER = 'ck-univers-cards'
UNIVERS_DATA_NAME = 'CK Acheter par univers'
UNIVERS_TITLE = 'Acheter par univers'
UNIVERS_INTRO = 'Quatre univers pour entrer dans la boutique en un clic.'
UNIVERS_CARD_SNIPPET = 's_ck_univers_card'
UNIVERS_SECTION_SNIPPET = 's_ck_univers_cards'
UNIVERS_EDITABLE_MEDIA_MARKER = 'o_editable_media'
UNIVERS_CARD_EDITABLE_CLASS = 'ck-univers-card'
UNIVERS_CARD_COUNT = 4
# Bump à chaque changement des JPG par défaut (force refresh navigateur, cf. §7 note arch).
UNIVERS_IMAGES_VERSION = '6'


def _univers_image_src(path):
    """URL image module + cache-bust (static Odoo : max-age 7j)."""
    base = path.split('?', 1)[0]
    return f'{base}?v={UNIVERS_IMAGES_VERSION}'


def _univers_default_images_cache_busted(arch):
    """True si les JPG module encore présents portent le ?v= courant."""
    token = f'?v={UNIVERS_IMAGES_VERSION}'
    for spec in _UNIVERS_CARD_SPECS:
        fname = spec['image'].rsplit('/', 1)[-1]
        if fname not in arch:
            continue
        if f'{fname}{token}' not in arch:
            return False
    return True

_UNIVERS_CARD_SPECS = (
    {
        'code': 'epicerie',
        'category_names': ('Épicerie créole', 'Épicerie'),
        'title': 'Épicerie créole',
        'description': 'Farines, confitures, condiments et douceurs à découvrir.',
        'cta': "Voir l'épicerie",
        'image': '/dorevia_ck_marketone_content/static/img/ck_univers_epicerie.jpg',
    },
    {
        'code': 'boissons',
        'category_names': ('Boissons',),
        'title': 'Boissons',
        'description': 'Sirops, jus, infusions et boissons créoles pour accompagner les moments du quotidien.',
        'cta': 'Voir les boissons',
        'image': '/dorevia_ck_marketone_content/static/img/ck_univers_boissons.jpg',
    },
    {
        'code': 'soin',
        'category_names': ('Maison & bien-être',),
        'title': 'Soin & bien-être',
        'description': 'Savons, soins et produits bien-être pour le corps et le quotidien.',
        'cta': 'Découvrir les soins',
        'image': '/dorevia_ck_marketone_content/static/img/ck_univers_soin.jpg',
    },
    {
        'code': 'artisanat',
        'category_names': ('Artisanat',),
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


def _find_univers_category(Category, spec):
    for name in spec.get('category_names', ()):
        category = Category.search([('name', '=', name)], limit=1)
        if category:
            return category
    return Category.browse()


def _resolve_univers_cards(env):
    """Retourne les 4 cards avec URL catégorie BO (fallback /shop si absente)."""
    Category = env['product.public.category'].sudo()
    cards = []
    for spec in _UNIVERS_CARD_SPECS:
        category = _find_univers_category(Category, spec)
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
    image = escape(_univers_image_src(card['image']))
    card_data_name = escape(f"Univers {card['title']}")
    return f"""
            <div class="ck-univers-card ck-univers-card--{escape(card['code'])}" data-snippet="{UNIVERS_CARD_SNIPPET}" data-name="{card_data_name}">
                <div class="ck-univers-card__media o_editable">
                    <p class="o_not_editable" contenteditable="false">
                        <img src="{image}" alt="{title}" class="ck-univers-card__img {UNIVERS_EDITABLE_MEDIA_MARKER}" loading="lazy" decoding="async"/>
                    </p>
                </div>
                <a href="{href}" class="ck-univers-card__cover" aria-label="{title}" tabindex="-1"/>
                <div class="ck-univers-card__overlay">
                    <h3 class="ck-univers-card__title o_editable">{title}</h3>
                    <p class="ck-univers-card__desc o_editable">{description}</p>
                    <a href="{href}" class="ck-univers-card__cta">{cta}</a>
                </div>
            </div>""".strip()


def build_home_univers_arch(env):
    cards = _resolve_univers_cards(env)
    if len(cards) != UNIVERS_CARD_COUNT:
        return ''
    cards_inner = '\n            '.join(_build_univers_card_html(card) for card in cards)
    title = escape(UNIVERS_TITLE)
    intro = escape(UNIVERS_INTRO)
    return f"""
<section class="s_ck_univers_cards {UNIVERS_SECTION_MARKER} pt48 pb48" data-name="{UNIVERS_DATA_NAME}">
    <div class="container">
        <div class="ck-univers-cards__head mb-4">
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
    if chunk.count('ck-univers-card--') != UNIVERS_CARD_COUNT:
        return False
    if chunk.count(f'data-snippet="{UNIVERS_CARD_SNIPPET}"') != UNIVERS_CARD_COUNT:
        return False
    if chunk.count(UNIVERS_EDITABLE_MEDIA_MARKER) != UNIVERS_CARD_COUNT:
        return False
    if chunk.count('ck-univers-card__cover') != UNIVERS_CARD_COUNT:
        return False
    if re.search(r'class="ck-univers-card[^"]*"[^>]*data-href=', chunk):
        return False
    if 'ck-univers-card--epicerie' not in chunk:
        return False
    if 'ck-univers-card--boissons' not in chunk:
        return False
    if 'ck-univers-card__media o_editable' not in chunk:
        return False
    if f'data-snippet="{UNIVERS_SECTION_SNIPPET}"' in chunk.split('ck-univers-cards__grid')[0]:
        return False
    if re.search(r'<a\s[^>]*class="ck-univers-card ck-univers-card--', chunk):
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


def _univers_arch_matches_bo(env, arch):
    if not univers_arch_is_valid(arch):
        return False
    if not _univers_default_images_cache_busted(arch):
        return False
    if 'ck-univers-cards__head text-center' in arch:
        return False
    if UNIVERS_INTRO not in arch:
        return False
    chunk_start = arch.find(UNIVERS_SECTION_MARKER)
    if chunk_start >= 0:
        chunk = arch[chunk_start:chunk_start + 12000]
        if 'pt48 pb48' not in chunk:
            return False
    return all(card['href'] in arch for card in _resolve_univers_cards(env))


def bootstrap_home_univers(env):
    """Section 4 home — injecte la grille 4 univers visuels après Coups de cœur."""
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

    if _univers_arch_matches_bo(env, arch) and 'data-snippet="s_ck_category_links"' not in arch:
        from .home_discovery_pack import bootstrap_home_discovery_pack

        bootstrap_home_discovery_pack(env)
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
    if not univers_arch_is_valid(new_arch):
        return False
    from .home_discovery_pack import bootstrap_home_discovery_pack

    bootstrap_home_discovery_pack(env)
    return univers_arch_is_valid(new_arch)
