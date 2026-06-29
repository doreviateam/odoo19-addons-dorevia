# -*- coding: utf-8 -*-
"""Navigation CK V2.2 — sync header / mega-menus (ticket Header & Mega-menus CK V2.2)."""
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
    MANAGED_V22_ROOT_NAMES,
    NAV_ALL_LABEL,
    NAV_ALL_SEQUENCE,
    NAV_ALL_URL,
    NAV_ARTISANAT_LABEL,
    NAV_BOISSONS_LABEL,
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
                 is_mega=False, mega_content='', category_id=None, child_menus=None):
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
        menu.write(vals)
    else:
        menu = Menu.create({
            **vals,
            'parent_id': parent.id,
            'website_id': website.id,
        })

    if child_menus is not None:
        managed = set()
        for child_spec in child_menus:
            managed.add(child_spec['name'])
            _upsert_menu(
                Menu,
                website=website,
                parent=menu,
                name=child_spec['name'],
                url=child_spec['url'],
                sequence=child_spec.get('sequence', 10),
                css_class=child_spec.get('css_class', ''),
            )
        for child in menu.child_id:
            if child.name not in managed:
                _unlink_menu(child)
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
    root = website.menu_id
    if not root:
        _logger.warning('Nav sync V2.2 : website %s sans menu racine — skip', website.id)
        return False
    Menu = env['website.menu'].sudo()

    _prune_unmanaged_root_menus(website, root, Menu)
    _remove_decouvrir_and_mobile_univers(website, root, Menu)
    _sync_shop_all(env, website, root, Menu)

    _sync_mega_rayon(
        env, website, root, Menu,
        NAV_EPICERIE_LABEL,
        NAV_RAYON_SEQUENCE[NAV_EPICERIE_LABEL],
        build_epicerie_mega(env),
    )
    _sync_mega_rayon(
        env, website, root, Menu,
        NAV_BOISSONS_LABEL,
        NAV_RAYON_SEQUENCE[NAV_BOISSONS_LABEL],
        build_boissons_mega(env),
    )
    _sync_mega_rayon(
        env, website, root, Menu,
        NAV_MAISON_LABEL,
        NAV_RAYON_SEQUENCE[NAV_MAISON_LABEL],
        build_maison_mega(env),
        css_extra=NAV_CSS_N3_GROUP_END,
    )
    _sync_artisanat(env, website, root, Menu)
    _sync_communaute(env, website, root, Menu)
    _sync_coffrets(env, website, root, Menu)
    _sync_producteurs(env, website, root, Menu)
    _sync_espace_pro(env, website, root, Menu)
    return True


def bootstrap_ck_navigation(env):
    Website = env['website'].sudo()
    synced = 0
    for website in Website.search([]):
        if sync_ck_navigation_for_website(env, website):
            synced += 1
    _logger.info('Nav sync V2.2 : navigation synchronisée pour %s site(s)', synced)
    return synced


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
