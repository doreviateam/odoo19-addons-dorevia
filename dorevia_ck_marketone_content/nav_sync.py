# -*- coding: utf-8 -*-
"""Navigation CK — sync header.

S2 : ``bootstrap_ck_catalogue_navigation`` / ``sync_ck_catalogue_navigation_for_website``
sont l'unique autorité. Les entrées V1 / V2.2 délèguent à V3 (compat imports /
migrations / modèles mega-menu BO).
"""
import logging

from .nav_mega_menu import (
    _category_has_published_products,
    _category_shop_url,
    _find_root_category,
    _tag_shop_url,
    build_artisanat_mega,
    build_boissons_mega,
    build_epicerie_mega,
    build_maison_mega,
    count_artisanat_families,
)
from .nav_v22_config import (
    ARTISANAT_MEGA_MIN_FAMILIES,
    LEGACY_NAV_MAISON_LABEL,
    LEGACY_ROOT_MENU_NAMES,
    MANAGED_CATALOGUE_FIXED_ROOT_NAMES,
    MANAGED_V1_ROOT_NAMES,
    MANAGED_V22_ROOT_NAMES,
    NAV_ALL_LABEL,
    NAV_ALL_SEQUENCE,
    NAV_ALL_URL,
    NAV_ARTISANAT_LABEL,
    NAV_BOISSONS_LABEL,
    NAV_CATALOGUE_BOUTIQUE_LABEL,
    NAV_CATALOGUE_BOUTIQUE_SEQUENCE,
    NAV_CATALOGUE_BOUTIQUE_URL,
    NAV_CATALOGUE_FIRST_CATEGORY_SEQUENCE,
    NAV_CATALOGUE_PRODUCTEURS_LABEL,
    NAV_CATALOGUE_PRODUCTEURS_SEQUENCE,
    NAV_CATALOGUE_PRODUCTEURS_URL,
    NAV_CATALOGUE_PROFESSIONNELS_LABEL,
    NAV_CATALOGUE_PROFESSIONNELS_SEQUENCE,
    NAV_CATALOGUE_PROFESSIONNELS_URL,
    NAV_CATALOGUE_RESERVED_ROOT_SEQUENCES,
    NAV_CATALOGUE_SEQUENCE_STEP,
    NAV_COFFRETS_LABEL,
    LEGACY_NAV_COUPS_LABEL,
    NAV_COMMUNAUTE_LABEL,
    NAV_COMMUNAUTE_URL,
    NAV_CSS_ESPACE_PRO,
    NAV_CSS_MEGA_PRODUCT,
    NAV_CSS_N3_GROUP_END,
    NAV_CSS_N3_RAYON,
    NAV_CSS_N3_RELATION,
    NAV_CSS_N3_SELECTION,
    NAV_CSS_NO_AUTOHIDE,
    NAV_CSS_PRODUCTEURS,
    NAV_CSS_SHOP_ROOT,
    NAV_EPICERIE_LABEL,
    NAV_ESPACE_PRO_LABEL,
    NAV_MAISON_LABEL,
    NAV_PRODUCTEURS_LABEL,
    NAV_PRODUCTEURS_URL,
    NAV_PRO_PAGE_URL,
    NAV_RAYON_SEQUENCE,
    NAV_RELATION_SEQUENCE,
    NAV_SELECTION_SEQUENCE,
    NAV_V1_BOUTIQUE_LABEL,
    NAV_V1_BOUTIQUE_SEQUENCE,
    NAV_V1_PRODUCTEURS_LABEL,
    NAV_V1_PRODUCTEURS_SEQUENCE,
    NAV_V1_PROFESSIONNELS_LABEL,
    NAV_V1_PROFESSIONNELS_SEQUENCE,
)

_logger = logging.getLogger(__name__)

# Rétrocompat tests Nav-Shop V2.1
NAV_SHOP_ALL_LABEL = NAV_ALL_LABEL
NAV_SHOP_ALL_URL = NAV_ALL_URL
NAV_CSS_DESKTOP_UNIVERSE = NAV_CSS_N3_RAYON
NAV_CSS_DESKTOP_UNIVERSE_CHILD = 'ck-nav-desktop-universe-child'
NAV_CSS_MOBILE_UNIVERS_GROUP = 'ck-nav-mobile-univers'
NAV_CSS_MOBILE_UNIVERSE_CHILD = 'ck-nav-mobile-universe-child'
NAV_DECOUVRIR_LABEL = 'Découvrir'
NAV_MOBILE_UNIVERS_LABEL = 'Nos univers'


def _shop_all_visible(env):
    return bool(env['product.template'].sudo().search([
        ('sale_ok', '=', True),
        ('is_published', '=', True),
        ('website_published', '=', True),
    ], limit=1))


def _page_url_visible(env, website, url):
    if not url or url == '#':
        return False
    page = env['website.page'].sudo().search([
        ('url', '=', url),
        '|', ('website_id', '=', False), ('website_id', '=', website.id),
    ], limit=1)
    return bool(page and page.is_published)


def _unlink_menu(menu):
    if menu:
        menu.unlink()


def _upsert_menu(Menu, *, website, parent, name, url, sequence, css_class='',
                 is_mega=False, mega_content='', category_id=None, child_menus=None,
                 preserve_existing_sequence=False):
    """Crée ou met à jour un website.menu.

    Identité (S2) :
    - si ``category_id`` est fourni, matching prioritaire sur ``ck_nav_category_id``
      (renommage BO de la catégorie sans doublon) ;
    - sinon fallback historique ``name`` + ``parent_id`` + ``website_id``.

    CK-NAV-003b : si ``preserve_existing_sequence`` est vrai et que le menu
    existe déjà, la ``sequence`` administrée en BO n'est pas écrasée par la
    valeur calculée — seule la création applique la séquence par défaut.
    """
    menu = Menu.browse()
    if category_id:
        menu = Menu.search([
            ('website_id', '=', website.id),
            ('parent_id', '=', parent.id),
            ('ck_nav_category_id', '=', category_id),
        ], limit=1)
    if not menu:
        menu = Menu.search([
            ('website_id', '=', website.id),
            ('parent_id', '=', parent.id),
            ('name', '=', name),
        ], limit=1)
    vals = {
        'name': name,
        'url': url,
        'sequence': sequence,
        'is_mega_menu': is_mega,
        'mega_menu_content': mega_content if is_mega else False,
        'ck_nav_css_class': css_class or False,
        'ck_nav_category_id': category_id or False,
    }
    if menu:
        if is_mega and menu.child_id:
            for child in menu.child_id:
                _unlink_menu(child)
        if preserve_existing_sequence:
            vals.pop('sequence')
        menu.write(vals)
    else:
        menu = Menu.create({
            **vals,
            'parent_id': parent.id,
            'website_id': website.id,
        })

    if child_menus is not None:
        managed_names = set()
        managed_category_ids = set()
        for child_spec in child_menus:
            managed_names.add(child_spec['name'])
            child_cat_id = child_spec.get('category_id')
            if child_cat_id:
                managed_category_ids.add(child_cat_id)
            _upsert_menu(
                Menu,
                website=website,
                parent=menu,
                name=child_spec['name'],
                url=child_spec['url'],
                sequence=child_spec.get('sequence', 10),
                css_class=child_spec.get('css_class', ''),
                category_id=child_cat_id,
                preserve_existing_sequence=preserve_existing_sequence,
            )
        for child in menu.child_id:
            keep = child.name in managed_names
            if child.ck_nav_category_id and child.ck_nav_category_id.id in managed_category_ids:
                keep = True
            if not keep:
                _unlink_menu(child)
        # Odoo force ``url='#'`` dès qu'un menu a des enfants : rétabli l'URL
        # catalogue pour l'idempotence et les liens split desktop/mobile.
        if url and menu.url != url:
            menu.write({'url': url})
    elif not is_mega and menu.child_id:
        for child in menu.child_id:
            _unlink_menu(child)
    return menu


def _prune_unmanaged_root_menus(website, root, Menu):
    for menu in Menu.search([('website_id', '=', website.id), ('parent_id', '=', root.id)]):
        if menu.name in MANAGED_V22_ROOT_NAMES:
            continue
        if menu.name in LEGACY_ROOT_MENU_NAMES or menu.url in ('/professionnels', '/contactus'):
            _unlink_menu(menu)
        elif menu.ck_nav_css_class and 'ck-nav-desktop-universe' in menu.ck_nav_css_class.split():
            _unlink_menu(menu)
        elif menu.ck_nav_css_class in (
            NAV_CSS_DESKTOP_UNIVERSE_CHILD,
            NAV_CSS_MOBILE_UNIVERS_GROUP,
            NAV_CSS_MOBILE_UNIVERSE_CHILD,
        ):
            _unlink_menu(menu)


def _sync_shop_all(env, website, root, Menu):
    if _shop_all_visible(env):
        _upsert_menu(
            Menu,
            website=website,
            parent=root,
            name=NAV_ALL_LABEL,
            url=NAV_ALL_URL,
            sequence=NAV_ALL_SEQUENCE,
            css_class=f'{NAV_CSS_NO_AUTOHIDE} {NAV_CSS_N3_RAYON} {NAV_CSS_SHOP_ROOT}',
        )
    else:
        menu = Menu.search([
            ('website_id', '=', website.id),
            ('parent_id', '=', root.id),
            ('name', '=', NAV_ALL_LABEL),
        ], limit=1)
        _unlink_menu(menu)


def _retire_legacy_maison_nav_menu(website, root, Menu, target_label):
    """Renomme ou retire l'ancienne entrée « Maison & Bien-être » avant upsert."""
    legacy = Menu.search([
        ('website_id', '=', website.id),
        ('parent_id', '=', root.id),
        ('name', '=', LEGACY_NAV_MAISON_LABEL),
    ], limit=1)
    if not legacy:
        return
    target = Menu.search([
        ('website_id', '=', website.id),
        ('parent_id', '=', root.id),
        ('name', '=', target_label),
    ], limit=1)
    if target and target.id != legacy.id:
        _unlink_menu(legacy)
    else:
        legacy.write({'name': target_label})


def _sync_mega_rayon(env, website, root, Menu, label, sequence, mega_html, css_extra=''):
    if label == NAV_MAISON_LABEL:
        _retire_legacy_maison_nav_menu(website, root, Menu, label)
    root_cat = _find_root_category(env, label)
    if root_cat and not _category_has_published_products(env, root_cat):
        menu = Menu.search([
            ('website_id', '=', website.id),
            ('parent_id', '=', root.id),
            ('name', '=', label),
        ], limit=1)
        _unlink_menu(menu)
        return
    url = _category_shop_url(env, root_cat) if root_cat else '#'
    css = f'{NAV_CSS_NO_AUTOHIDE} {NAV_CSS_N3_RAYON} {NAV_CSS_MEGA_PRODUCT} {css_extra}'.strip()
    _upsert_menu(
        Menu,
        website=website,
        parent=root,
        name=label,
        url=url or '#',
        sequence=sequence,
        css_class=css,
        is_mega=True,
        mega_content=mega_html,
        category_id=root_cat.id if root_cat else False,
    )


def _sync_artisanat(env, website, root, Menu):
    families_count = count_artisanat_families(env)
    root_cat = _find_root_category(env, NAV_ARTISANAT_LABEL)
    if not root_cat or not _category_has_published_products(env, root_cat):
        menu = Menu.search([
            ('website_id', '=', website.id),
            ('parent_id', '=', root.id),
            ('name', '=', NAV_ARTISANAT_LABEL),
        ], limit=1)
        _unlink_menu(menu)
        return
    url = _category_shop_url(env, root_cat)
    if families_count >= ARTISANAT_MEGA_MIN_FAMILIES:
        _upsert_menu(
            Menu,
            website=website,
            parent=root,
            name=NAV_ARTISANAT_LABEL,
            url=url or '#',
            sequence=NAV_RAYON_SEQUENCE[NAV_ARTISANAT_LABEL],
            css_class=f'{NAV_CSS_NO_AUTOHIDE} {NAV_CSS_N3_RAYON} {NAV_CSS_MEGA_PRODUCT} {NAV_CSS_N3_GROUP_END}',
            is_mega=True,
            mega_content=build_artisanat_mega(env),
            category_id=root_cat.id,
        )
    else:
        _upsert_menu(
            Menu,
            website=website,
            parent=root,
            name=NAV_ARTISANAT_LABEL,
            url=url or '#',
            sequence=NAV_RAYON_SEQUENCE[NAV_ARTISANAT_LABEL],
            css_class=f'{NAV_CSS_NO_AUTOHIDE} {NAV_CSS_N3_RAYON} {NAV_CSS_N3_GROUP_END}',
            category_id=root_cat.id,
        )


def _sync_communaute(env, website, root, Menu):
    """Entrée N3 Communauté — placeholder # en attendant blog/forum CK."""
    legacy = Menu.search([
        ('website_id', '=', website.id),
        ('parent_id', '=', root.id),
        ('name', '=', LEGACY_NAV_COUPS_LABEL),
    ])
    for menu in legacy:
        _unlink_menu(menu)
    _upsert_menu(
        Menu,
        website=website,
        parent=root,
        name=NAV_COMMUNAUTE_LABEL,
        url=NAV_COMMUNAUTE_URL,
        sequence=NAV_SELECTION_SEQUENCE[NAV_COMMUNAUTE_LABEL],
        css_class=f'{NAV_CSS_NO_AUTOHIDE} {NAV_CSS_N3_SELECTION}',
    )


def sync_communaute_header_for_website(env, website):
    """Remplacement chirurgical Coups de cœur → Communauté (sans resync rayons)."""
    root = website.menu_id
    if not root:
        _logger.warning(
            'Nav Communauté : website %s sans menu racine — skip', website.id,
        )
        return False
    _sync_communaute(env, website, root, env['website.menu'].sudo())
    return True


def sync_communaute_header(env):
    """Sync header Communauté sur tous les sites — périmètre ticket nav uniquement."""
    synced = 0
    for website in env['website'].sudo().search([]):
        if sync_communaute_header_for_website(env, website):
            synced += 1
    _logger.info('Nav Communauté : entrée synchronisée pour %s site(s)', synced)
    return synced


def sync_shop_root_icon_header(env):
    """Nav-U2 — resynchronise uniquement l'entrée racine boutique /shop."""
    synced = 0
    Menu = env['website.menu'].sudo()
    for website in env['website'].sudo().search([]):
        root = website.menu_id
        if not root:
            _logger.warning(
                'Nav-U2 racine boutique : website %s sans menu racine — skip',
                website.id,
            )
            continue
        _sync_shop_all(env, website, root, Menu)
        synced += 1
    _logger.info('Nav-U2 racine boutique : entrée synchronisée pour %s site(s)', synced)
    return synced


def _sync_coffrets(env, website, root, Menu):
    child_links = _coffrets_child_links(env)
    default_url = _tag_shop_url(env, 'coffret')
    menu = Menu.search([
        ('website_id', '=', website.id),
        ('parent_id', '=', root.id),
        ('name', '=', NAV_COFFRETS_LABEL),
    ], limit=1)

    if child_links:
        _upsert_menu(
            Menu,
            website=website,
            parent=root,
            name=NAV_COFFRETS_LABEL,
            url='#',
            sequence=NAV_SELECTION_SEQUENCE[NAV_COFFRETS_LABEL],
            css_class=f'{NAV_CSS_NO_AUTOHIDE} {NAV_CSS_N3_SELECTION} {NAV_CSS_N3_GROUP_END}',
            child_menus=[
                {'name': label, 'url': child_url, 'sequence': (idx + 1) * 10}
                for idx, (label, child_url) in enumerate(child_links)
            ],
        )
    elif default_url:
        _upsert_menu(
            Menu,
            website=website,
            parent=root,
            name=NAV_COFFRETS_LABEL,
            url=default_url,
            sequence=NAV_SELECTION_SEQUENCE[NAV_COFFRETS_LABEL],
            css_class=f'{NAV_CSS_NO_AUTOHIDE} {NAV_CSS_N3_SELECTION} {NAV_CSS_N3_GROUP_END}',
        )
    elif menu:
        _unlink_menu(menu)


def _coffrets_child_links(env):
    from .nav_v22_config import COFFRETS_ANGLES, COFFRETS_MINI_DROPDOWN_MIN_ANGLES
    from .nav_mega_menu import _tag_shop_url as tag_url

    rows = []
    for label, kind, source in COFFRETS_ANGLES:
        if kind != 'tag':
            continue
        url = tag_url(env, source)
        if url:
            rows.append((label, url))
    return rows[:5] if len(rows) >= COFFRETS_MINI_DROPDOWN_MIN_ANGLES else []


def _sync_producteurs(env, website, root, Menu):
    """Entrée stratégique MOA — lien direct annuaire producteurs dynamique."""
    _upsert_menu(
        Menu,
        website=website,
        parent=root,
        name=NAV_PRODUCTEURS_LABEL,
        url=NAV_PRODUCTEURS_URL,
        sequence=NAV_RELATION_SEQUENCE[NAV_PRODUCTEURS_LABEL],
        css_class=f'{NAV_CSS_NO_AUTOHIDE} {NAV_CSS_N3_RELATION} {NAV_CSS_PRODUCTEURS}',
    )


def _sync_espace_pro(env, website, root, Menu):
    if not _page_url_visible(env, website, NAV_PRO_PAGE_URL):
        menu = Menu.search([
            ('website_id', '=', website.id),
            ('parent_id', '=', root.id),
            ('name', '=', NAV_ESPACE_PRO_LABEL),
        ], limit=1)
        _unlink_menu(menu)
        return
    child_menus = [
        {'name': label, 'url': url, 'sequence': (idx + 1) * 10}
        for idx, (label, url) in enumerate(
            __import__(
                'odoo.addons.dorevia_ck_marketone_content.nav_v22_config',
                fromlist=['ESPACE_PRO_LINKS'],
            ).ESPACE_PRO_LINKS
        )
    ]
    _upsert_menu(
        Menu,
        website=website,
        parent=root,
        name=NAV_ESPACE_PRO_LABEL,
        url='#',
        sequence=NAV_RELATION_SEQUENCE[NAV_ESPACE_PRO_LABEL],
        css_class=f'{NAV_CSS_NO_AUTOHIDE} {NAV_CSS_N3_RELATION} {NAV_CSS_ESPACE_PRO}',
        child_menus=child_menus,
    )


def _remove_decouvrir_and_mobile_univers(website, root, Menu):
    for name in (NAV_DECOUVRIR_LABEL, NAV_MOBILE_UNIVERS_LABEL):
        menu = Menu.search([
            ('website_id', '=', website.id),
            ('parent_id', '=', root.id),
            ('name', '=', name),
        ], limit=1)
        _unlink_menu(menu)


def sync_ck_navigation_for_website(env, website):
    """HISTORIQUE V2.2 — neutralisé (S2).

    Conservé pour compatibilité des imports / migrations / modèles mega-menu.
    Délègue exclusivement à la navigation catalogue V3.
    """
    _logger.warning(
        'sync_ck_navigation_for_website (V2.2) is deprecated; '
        'delegating to sync_ck_catalogue_navigation_for_website (V3)'
    )
    return sync_ck_catalogue_navigation_for_website(env, website)


def bootstrap_ck_navigation(env):
    """HISTORIQUE V2.2 — neutralisé (S2). Délègue à V3 catalogue."""
    _logger.warning(
        'bootstrap_ck_navigation (V2.2) is deprecated; '
        'delegating to bootstrap_ck_catalogue_navigation (V3)'
    )
    return bootstrap_ck_catalogue_navigation(env)


# ---------------------------------------------------------------------------
# Nav V1 — historique (3 liens plats). Neutralisé S2 → délègue à V3.
# ---------------------------------------------------------------------------

def sync_ck_navigation_v1_for_website(env, website):
    """HISTORIQUE V1 — neutralisé (S2).

    Ne purge plus « Épicerie » ni les racines catalogue. Délègue à V3.
    """
    _logger.warning(
        'sync_ck_navigation_v1_for_website (V1) is deprecated; '
        'delegating to sync_ck_catalogue_navigation_for_website (V3)'
    )
    return sync_ck_catalogue_navigation_for_website(env, website)


def bootstrap_ck_navigation_v1(env):
    """HISTORIQUE V1 — neutralisé (S2). Délègue à V3 catalogue."""
    _logger.warning(
        'bootstrap_ck_navigation_v1 (V1) is deprecated; '
        'delegating to bootstrap_ck_catalogue_navigation (V3)'
    )
    return bootstrap_ck_catalogue_navigation(env)


def build_shop_nav_trees(env, Category):
    """Rétrocompat — arborescence racines catalogue pour tests / doc."""
    trees = []
    for label in NAV_RAYON_SEQUENCE:
        root = _find_root_category(env, label)
        if not root or not _category_has_published_products(env, root):
            continue
        children = []
        for child in root.child_id.sorted(key=lambda c: (c.sequence, c.name or '')):
            if not _category_has_published_products(env, child):
                continue
            url = _category_shop_url(env, child)
            if url:
                children.append({
                    'category_id': child.id,
                    'name': child.name,
                    'url': url,
                    'sequence': child.sequence,
                })
        trees.append({
            'category_id': root.id,
            'name': root.name,
            'url': _category_shop_url(env, root),
            'sequence': NAV_RAYON_SEQUENCE[label],
            'children': children,
        })
    return trees


# ---------------------------------------------------------------------------
# Nav V3 / CK-NAV-003 — Navigation catalogue dynamique (product.public.category)
# ---------------------------------------------------------------------------

def _category_visible_on_website(category, website):
    """Catégorie visible sur le website courant (globale ou affectée au site)."""
    cat_website = getattr(category, 'website_id', None)
    if cat_website and cat_website.id and cat_website.id != website.id:
        return False
    return True


def _eligible_level2_children(env, parent_category):
    """Sous-catégories directes éligibles (avec produits publiés) — utilisé par WebsiteMenu."""
    return [
        c for c in parent_category.child_id.sorted(key=lambda c: (c.sequence, c.name or ''))
        if _category_has_published_products(env, c)
    ]


def _get_ck_nav_root_categories(env, website):
    """Catégories e-commerce racines éligibles pour la navigation catalogue.

    CATALOG-ARCHI-001 Lot A : l'éligibilité passe par `_is_ck_exposable()`
    (statut CK + seuil produits qualifiés), plus stricte que la simple
    existence d'un produit publié (`_category_has_published_products`).
    """
    Category = env['product.public.category'].sudo()
    root_cats = Category.search([('parent_id', '=', False)], order='sequence, name')
    return root_cats.filtered(
        lambda c: _category_visible_on_website(c, website) and c._is_ck_exposable()
    )


def _get_ck_nav_child_categories(env, website, parent):
    """Sous-catégories directes éligibles (niveau 2) pour la navigation catalogue."""
    children = parent.child_id.sorted(key=lambda c: (c.sequence, c.name or ''))
    return [
        c for c in children
        if _category_visible_on_website(c, website) and c._is_ck_exposable()
    ]


def _strip_v22_menu_chrome(menu):
    """Retire mega-menu / CSS V2.2 sans supprimer l'entrée (préparation upsert V3)."""
    css = menu.ck_nav_css_class or ''
    if menu.is_mega_menu or (css and 'ck-nav-' in css):
        menu.write({
            'is_mega_menu': False,
            'mega_menu_content': False,
            'ck_nav_css_class': False,
        })


def _cleanup_ck_catalogue_root_menus(env, website, root, Menu, eligible_categories):
    """Purge les entrées V2.2 / mega / orphelins sans détruire les racines catalogue.

    S2 : ne plus supprimer aveuglément ``MANAGED_V22_ROOT_NAMES`` (ex. « Épicerie »)
    quand la catégorie catalogue correspondante est encore éligible — sinon
    l'upsert recrée l'entrée et casse idempotence / séquences BO.
    """
    eligible_category_ids = set(eligible_categories.ids)
    eligible_names = set(eligible_categories.mapped('name'))

    for m in Menu.search([
        ('website_id', '=', website.id),
        ('parent_id', '=', root.id),
    ]):
        # Racines fixes V3 — conserver, dépouiller le chrome V2.2
        if m.name in MANAGED_CATALOGUE_FIXED_ROOT_NAMES:
            _strip_v22_menu_chrome(m)
            continue

        # Entrée liée à une catégorie encore éligible
        if m.ck_nav_category_id and m.ck_nav_category_id.id in eligible_category_ids:
            _strip_v22_menu_chrome(m)
            continue

        # Même nom qu'une catégorie éligible (liaison category_id absente / legacy)
        if m.name in eligible_names:
            _strip_v22_menu_chrome(m)
            continue

        # Catégorie liée devenue inéligible / absente
        if m.ck_nav_category_id and m.ck_nav_category_id.id not in eligible_category_ids:
            _unlink_menu(m)
            continue

        # Libellés V2.2 hors catalogue (Tous nos produits, Nos producteurs, Communauté…)
        if m.name in MANAGED_V22_ROOT_NAMES:
            _unlink_menu(m)
            continue

        # Orphelins legacy / mega / CSS ck-nav
        if m.name in LEGACY_ROOT_MENU_NAMES:
            _unlink_menu(m)
        elif m.is_mega_menu:
            _unlink_menu(m)
        elif m.ck_nav_css_class and 'ck-nav-' in (m.ck_nav_css_class or ''):
            _unlink_menu(m)


def snapshot_ck_catalogue_navigation(env, website):
    """État structuré de la navigation catalogue (pour tests d'idempotence)."""
    root = website.menu_id
    if not root:
        return ()
    Menu = env['website.menu'].sudo()
    rows = []
    for menu in Menu.search([
        ('website_id', '=', website.id),
        ('parent_id', '=', root.id),
    ], order='sequence, id'):
        children = tuple(
            (
                child.name,
                child.url or '',
                child.sequence,
                child.ck_nav_category_id.id if child.ck_nav_category_id else False,
                bool(child.is_mega_menu),
                child.ck_nav_css_class or '',
            )
            for child in menu.child_id.sorted(key=lambda c: (c.sequence, c.id))
        )
        rows.append((
            menu.name,
            menu.url or '',
            menu.sequence,
            menu.ck_nav_category_id.id if menu.ck_nav_category_id else False,
            bool(menu.is_mega_menu),
            menu.ck_nav_css_class or '',
            children,
        ))
    return tuple(rows)


def _next_catalogue_category_root_sequence(sequence):
    """Prochain créneau catégorie en évitant Boutique / Producteurs / Professionnels."""
    while sequence in NAV_CATALOGUE_RESERVED_ROOT_SEQUENCES:
        sequence += NAV_CATALOGUE_SEQUENCE_STEP
    return sequence


def _managed_root_canonical_sequences(root_categories, professionnels_visible):
    """Séquences canoniques MOA des racines gérées (création + réparation collision).

    - Boutique : 10
    - Catégories exposables : 20, 30, … (en sautant 60/70)
    - Producteurs : 60
    - Professionnels : 70 (si page publiée)
    """
    by_menu_key = {
        ('fixed', NAV_CATALOGUE_BOUTIQUE_LABEL): NAV_CATALOGUE_BOUTIQUE_SEQUENCE,
        ('fixed', NAV_CATALOGUE_PRODUCTEURS_LABEL): NAV_CATALOGUE_PRODUCTEURS_SEQUENCE,
    }
    if professionnels_visible:
        by_menu_key[('fixed', NAV_CATALOGUE_PROFESSIONNELS_LABEL)] = (
            NAV_CATALOGUE_PROFESSIONNELS_SEQUENCE
        )
    sequence = NAV_CATALOGUE_FIRST_CATEGORY_SEQUENCE
    for category in root_categories:
        sequence = _next_catalogue_category_root_sequence(sequence)
        by_menu_key[('category', category.id)] = sequence
        sequence += NAV_CATALOGUE_SEQUENCE_STEP
    return by_menu_key


def _repair_managed_root_sequence_collisions(
    env, website, root, Menu, root_categories, professionnels_visible,
):
    """Normalise les collisions de séquence entre racines gérées.

    Doctrine MOA (S2 QA) :
    - une personnalisation BO *non ambiguë* (séquence unique parmi les racines
      gérées) est préservée ;
    - une collision héritée (ex. Épicerie=20 et Producteurs=20) est réparée en
      réassignant aux valeurs canoniques — jamais de départage par id ORM.
    """
    canonical = _managed_root_canonical_sequences(
        root_categories, professionnels_visible,
    )
    managed = []

    boutique = Menu.search([
        ('website_id', '=', website.id),
        ('parent_id', '=', root.id),
        ('name', '=', NAV_CATALOGUE_BOUTIQUE_LABEL),
    ], limit=1)
    if boutique:
        managed.append((boutique, canonical[('fixed', NAV_CATALOGUE_BOUTIQUE_LABEL)]))

    for category in root_categories:
        menu = Menu.search([
            ('website_id', '=', website.id),
            ('parent_id', '=', root.id),
            ('ck_nav_category_id', '=', category.id),
        ], limit=1)
        if not menu:
            menu = Menu.search([
                ('website_id', '=', website.id),
                ('parent_id', '=', root.id),
                ('name', '=', category.name),
            ], limit=1)
        if menu:
            managed.append((menu, canonical[('category', category.id)]))

    producteurs = Menu.search([
        ('website_id', '=', website.id),
        ('parent_id', '=', root.id),
        ('name', '=', NAV_CATALOGUE_PRODUCTEURS_LABEL),
    ], limit=1)
    if producteurs:
        managed.append((
            producteurs,
            canonical[('fixed', NAV_CATALOGUE_PRODUCTEURS_LABEL)],
        ))

    if professionnels_visible:
        professionnels = Menu.search([
            ('website_id', '=', website.id),
            ('parent_id', '=', root.id),
            ('name', '=', NAV_CATALOGUE_PROFESSIONNELS_LABEL),
        ], limit=1)
        if professionnels:
            managed.append((
                professionnels,
                canonical[('fixed', NAV_CATALOGUE_PROFESSIONNELS_LABEL)],
            ))

    if not managed:
        return

    by_sequence = {}
    for menu, _canon in managed:
        by_sequence.setdefault(menu.sequence, []).append(menu)

    colliding_sequences = {
        seq for seq, menus in by_sequence.items() if len(menus) > 1
    }
    if not colliding_sequences:
        return

    for menu, canon_seq in managed:
        old_seq = menu.sequence
        if old_seq in colliding_sequences and old_seq != canon_seq:
            menu.write({'sequence': canon_seq})
            _logger.info(
                'CK-NAV-003 : collision séquence racine « %s » (%s) → canonique %s',
                menu.name, old_seq, canon_seq,
            )


def sync_ck_catalogue_navigation_for_website(env, website):
    """CK-NAV-003 / S2 — Unique autorité de sync navigation catalogue CK."""
    root = website.menu_id
    if not root:
        _logger.warning(
            'CK-NAV-003 : website %s sans menu racine — skip', website.id,
        )
        return False

    Menu = env['website.menu'].sudo()

    # 1. Nettoyage V2.2 / mega-menus / orphelins legacy (sans détruire le catalogue)
    root_categories = _get_ck_nav_root_categories(env, website)
    _cleanup_ck_catalogue_root_menus(env, website, root, Menu, root_categories)

    # 2. Boutique — entrée fixe
    _upsert_menu(
        Menu,
        website=website,
        parent=root,
        name=NAV_CATALOGUE_BOUTIQUE_LABEL,
        url=NAV_CATALOGUE_BOUTIQUE_URL,
        sequence=NAV_CATALOGUE_BOUTIQUE_SEQUENCE,
    )

    # 3. Catégories e-commerce racines éligibles avec sous-catégories
    sequence = NAV_CATALOGUE_FIRST_CATEGORY_SEQUENCE

    for category in root_categories:
        sequence = _next_catalogue_category_root_sequence(sequence)
        child_categories = _get_ck_nav_child_categories(env, website, category)
        url = _category_shop_url(env, category) or NAV_CATALOGUE_BOUTIQUE_URL

        # Niveau 2 uniquement — pas de niveau 3 dans le header
        child_specs = [
            {
                'name': child.name,
                'url': _category_shop_url(env, child) or url,
                'sequence': (idx + 1) * NAV_CATALOGUE_SEQUENCE_STEP,
                'category_id': child.id,
            }
            for idx, child in enumerate(child_categories)
        ]

        _upsert_menu(
            Menu,
            website=website,
            parent=root,
            name=category.name,
            url=url,
            sequence=sequence,
            category_id=category.id,
            child_menus=child_specs,
            preserve_existing_sequence=True,
        )
        sequence += NAV_CATALOGUE_SEQUENCE_STEP

    # 4. Producteurs — séquence canonique MOA 60 (pas le compteur catégories)
    _upsert_menu(
        Menu,
        website=website,
        parent=root,
        name=NAV_CATALOGUE_PRODUCTEURS_LABEL,
        url=NAV_CATALOGUE_PRODUCTEURS_URL,
        sequence=NAV_CATALOGUE_PRODUCTEURS_SEQUENCE,
        preserve_existing_sequence=True,
    )

    # 5. Professionnels — séquence canonique MOA 70, conditionnel si page publiée
    professionnels_visible = _page_url_visible(
        env, website, NAV_CATALOGUE_PROFESSIONNELS_URL,
    )
    if professionnels_visible:
        _upsert_menu(
            Menu,
            website=website,
            parent=root,
            name=NAV_CATALOGUE_PROFESSIONNELS_LABEL,
            url=NAV_CATALOGUE_PROFESSIONNELS_URL,
            sequence=NAV_CATALOGUE_PROFESSIONNELS_SEQUENCE,
            preserve_existing_sequence=True,
        )
    else:
        for m in Menu.search([
            ('website_id', '=', website.id),
            ('parent_id', '=', root.id),
            ('name', '=', NAV_CATALOGUE_PROFESSIONNELS_LABEL),
        ]):
            _unlink_menu(m)

    # 6. Réparer collisions héritées (ex. Producteurs=20 ∩ Épicerie=20)
    _repair_managed_root_sequence_collisions(
        env, website, root, Menu, root_categories, professionnels_visible,
    )

    return True


def bootstrap_ck_catalogue_navigation(env):
    """CK-NAV-003 / S2 — Bootstrap navigation catalogue (unique autorité)."""
    synced = 0
    for website in env['website'].sudo().search([]):
        if sync_ck_catalogue_navigation_for_website(env, website):
            synced += 1
    _logger.info('CK-NAV-003 : navigation catalogue synchronisée pour %s site(s)', synced)
    return synced


def get_nav_category_mapping(env):
    rows = [{
        'menu_label': NAV_ALL_LABEL,
        'category_id': None,
        'category_name': 'Catalogue complet',
        'url': NAV_ALL_URL,
        'visible': _shop_all_visible(env),
        'published_products': _shop_all_visible(env),
        'level': 0,
        'children': [],
    }]
    for tree in build_shop_nav_trees(env, env['product.public.category'].sudo()):
        category = env['product.public.category'].sudo().browse(tree['category_id'])
        rows.append({
            'menu_label': tree['name'],
            'category_id': tree['category_id'],
            'category_name': category.name if category else tree['name'],
            'url': tree['url'],
            'visible': True,
            'published_products': _category_has_published_products(env, category),
            'level': 1,
            'children': tree['children'],
        })
    return rows
