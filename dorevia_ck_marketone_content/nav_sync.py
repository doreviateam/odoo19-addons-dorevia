# -*- coding: utf-8 -*-
"""Navigation CK — sync header / menus (Nav-1 · Nav-Shop)."""
import logging
from xml.sax.saxutils import escape

_logger = logging.getLogger(__name__)

NAV_SHOP_ALL_LABEL = 'Tous nos produits'
NAV_SHOP_ALL_URL = '/shop'
NAV_SHOP_ALL_SEQUENCE = 10

NAV_MOBILE_UNIVERS_LABEL = 'Nos univers'
NAV_MOBILE_UNIVERS_SEQUENCE = 15

NAV_DECOUVRIR_LABEL = 'Découvrir'
NAV_DECOUVRIR_SEQUENCE = 60

NAV_CSS_DESKTOP_UNIVERSE = 'ck-nav-desktop-universe'
NAV_CSS_DESKTOP_UNIVERSE_CHILD = 'ck-nav-desktop-universe-child'
NAV_CSS_MOBILE_UNIVERS_GROUP = 'ck-nav-mobile-univers'
NAV_CSS_MOBILE_UNIVERSE_CHILD = 'ck-nav-mobile-universe-child'
NAV_CSS_NO_AUTOHIDE = 'o_no_autohide_item'

NAV_SHOP_CATEGORY_SEQUENCE_BASE = 20
NAV_SHOP_CATEGORY_SEQUENCE_STEP = 5

# Ordre MOA · URLs None = masqué sauf page teaser MOA (non implémenté Nav-1).
DECOUVRIR_LINK_SPECS = (
    ('Producteurs & territoires', '/producteur/atelier-hauts-goyaviers'),
    ('Histoires de produits', None),
    ('Recettes & usages', '/recettes'),
    ('Le blog CK', '/blog'),
    ('Professionnels', '/professionnels'),
    ('Contactez-nous', '/contactus'),
    ('Communauté', None),
    ('Contribuer', None),
)

LEGACY_ROOT_MENU_NAMES = frozenset({
    'Boutique',
    'Professionnels',
    'Contactez-nous',
    'Contact Us',
    'Contact us',
    'Accueil',
    'Home',
    'Shop',
    'Contact',
    'Catégories',
    'Épicerie créole',
    'Soin & Bien-être',
    'Artisanat',
})

MANAGED_FIXED_ROOT_NAMES = frozenset({
    NAV_SHOP_ALL_LABEL,
    NAV_MOBILE_UNIVERS_LABEL,
    NAV_DECOUVRIR_LABEL,
})


def _category_shop_url(env, category):
    if not category:
        return None
    slug = env['ir.http'].sudo()._slug(category)
    return f'/shop/category/{slug}'


def _category_has_published_products(env, category):
    if not category:
        return False
    Product = env['product.template'].sudo()
    domain = [
        ('sale_ok', '=', True),
        ('is_published', '=', True),
        ('website_published', '=', True),
        ('public_categ_ids', 'child_of', category.id),
    ]
    return bool(Product.search(domain, limit=1))


def _blog_route_visible(env):
    module = env['ir.module.module'].sudo().search([
        ('name', '=', 'website_blog'),
        ('state', '=', 'installed'),
    ], limit=1)
    return bool(module)


def _page_url_visible(env, website, url):
    if not url or url == '#':
        return False
    if url == '/blog':
        return _blog_route_visible(env)
    Page = env['website.page'].sudo()
    page = Page.search([
        ('url', '=', url),
        '|', ('website_id', '=', False), ('website_id', '=', website.id),
    ], limit=1)
    if not page:
        return False
    return bool(page.is_published)


def _shop_all_visible(env):
    Product = env['product.template'].sudo()
    return bool(Product.search([
        ('sale_ok', '=', True),
        ('is_published', '=', True),
        ('website_published', '=', True),
    ], limit=1))


def _resolve_decouvrir_links(env, website):
    links = []
    for label, url in DECOUVRIR_LINK_SPECS:
        if not url:
            continue
        if url == '/blog' and not _blog_route_visible(env):
            continue
        if not _page_url_visible(env, website, url):
            continue
        links.append((label, url))
    return links


def _build_decouvrir_mega_content(links):
    if not links:
        return (
            '<div class="container py-3">'
            '<p class="text-muted mb-0">Contenus Découvrir à venir.</p>'
            '</div>'
        )
    rows = ''.join(
        f'<a class="nav-link" href="{escape(url)}">{escape(label)}</a>'
        for label, url in links
    )
    return (
        '<div class="container py-2">'
        '<div class="row"><div class="col-lg-10">'
        '<h5 class="dropdown-header">Découvrir CK</h5>'
        f'<nav class="nav flex-column ck-nav-decouvrir-links">{rows}</nav>'
        '</div></div></div>'
    )


def _unlink_menu(menu):
    if menu:
        menu.unlink()


def _upsert_menu(Menu, *, website, parent, name, url, sequence, css_class='',
                 is_mega=False, mega_content='', category_id=None):
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
        menu.write(vals)
    else:
        menu = Menu.create({
            **vals,
            'parent_id': parent.id,
            'website_id': website.id,
        })
    return menu


def _sorted_category_children(category):
    return category.child_id.sorted(key=lambda c: (c.sequence, c.name or ''))


def _eligible_level2_children(env, category):
    return _sorted_category_children(category).filtered(
        lambda c: _category_has_published_products(env, c)
    )


def build_shop_nav_trees(env, Category):
    """Arborescence Nav-Shop : racines + enfants directs éligibles (max 2 niveaux header)."""
    trees = []
    roots = Category.search([('parent_id', '=', False)], order='sequence, name')
    menu_sequence = NAV_SHOP_CATEGORY_SEQUENCE_BASE
    for category in roots:
        if not _category_has_published_products(env, category):
            continue
        children = []
        child_seq = 1
        for child in _eligible_level2_children(env, category):
            url = _category_shop_url(env, child)
            if not url:
                continue
            children.append({
                'category_id': child.id,
                'name': child.name,
                'url': url,
                'sequence': child_seq,
            })
            child_seq += 1
        url = _category_shop_url(env, category)
        if not url:
            continue
        trees.append({
            'category_id': category.id,
            'name': category.name,
            'url': url,
            'sequence': menu_sequence,
            'children': children,
        })
        menu_sequence += NAV_SHOP_CATEGORY_SEQUENCE_STEP
    return trees


def _prune_menu_children(Menu, parent_menu, managed_names):
    for child in parent_menu.child_id:
        if child.name not in managed_names:
            _unlink_menu(child)


def _sync_desktop_shop_menus(env, website, root, Menu, trees):
    active_root_names = set()
    for tree in trees:
        active_root_names.add(tree['name'])
        parent_menu = _upsert_menu(
            Menu,
            website=website,
            parent=root,
            name=tree['name'],
            url=tree['url'],
            sequence=tree['sequence'],
            css_class=NAV_CSS_DESKTOP_UNIVERSE,
            category_id=tree['category_id'],
        )
        managed_child_names = set()
        # Nav-Shop V2.1 — passe corrective MOA : pas d'entrée "Toute {root}" en
        # tête du dropdown L2. La racine elle-même est déjà cliquable (lien
        # direct vers l'univers via ck-nav-universe-split__link) ; ce doublon
        # de navigation était explicitement proscrit par l'arbitrage MOA.
        child_rows = list(tree['children'])
        for child in child_rows:
            managed_child_names.add(child['name'])
            _upsert_menu(
                Menu,
                website=website,
                parent=parent_menu,
                name=child['name'],
                url=child['url'],
                sequence=child['sequence'],
                css_class=NAV_CSS_DESKTOP_UNIVERSE_CHILD,
            )
        _prune_menu_children(Menu, parent_menu, managed_child_names)

    stale = Menu.search([
        ('website_id', '=', website.id),
        ('parent_id', '=', root.id),
        ('ck_nav_css_class', '=', NAV_CSS_DESKTOP_UNIVERSE),
    ])
    for menu in stale:
        if menu.name not in active_root_names:
            _unlink_menu(menu)
    return trees


def _sync_mobile_univers_group(env, website, root, Menu, trees):
    """Mobile — racines sous Nos univers ; L2 rendu depuis BO (QWeb · ck_nav_category_id)."""
    mobile_parent = Menu.search([
        ('website_id', '=', website.id),
        ('parent_id', '=', root.id),
        ('name', '=', NAV_MOBILE_UNIVERS_LABEL),
    ], limit=1)
    if not trees:
        if mobile_parent:
            _prune_menu_children(Menu, mobile_parent, set())
        _unlink_menu(mobile_parent)
        return

    parent = _upsert_menu(
        Menu,
        website=website,
        parent=root,
        name=NAV_MOBILE_UNIVERS_LABEL,
        url='#',
        sequence=NAV_MOBILE_UNIVERS_SEQUENCE,
        css_class=NAV_CSS_MOBILE_UNIVERS_GROUP,
    )
    managed_names = set()
    seq = NAV_SHOP_CATEGORY_SEQUENCE_BASE
    for tree in trees:
        managed_names.add(tree['name'])
        _upsert_menu(
            Menu,
            website=website,
            parent=parent,
            name=tree['name'],
            url=tree['url'],
            sequence=seq,
            css_class=NAV_CSS_MOBILE_UNIVERSE_CHILD,
            category_id=tree['category_id'],
        )
        seq += NAV_SHOP_CATEGORY_SEQUENCE_STEP
    _prune_menu_children(Menu, parent, managed_names)


def _sync_decouvrir_menu(env, website, root, Menu):
    links = _resolve_decouvrir_links(env, website)
    mega_html = _build_decouvrir_mega_content(links)
    _upsert_menu(
        Menu,
        website=website,
        parent=root,
        name=NAV_DECOUVRIR_LABEL,
        url='#',
        sequence=NAV_DECOUVRIR_SEQUENCE,
        css_class=NAV_CSS_NO_AUTOHIDE,
        is_mega=True,
        mega_content=mega_html,
    )


def _sync_shop_all_menu(env, website, root, Menu):
    visible = _shop_all_visible(env)
    menu = Menu.search([
        ('website_id', '=', website.id),
        ('parent_id', '=', root.id),
        ('name', '=', NAV_SHOP_ALL_LABEL),
    ], limit=1)
    if visible:
        _upsert_menu(
            Menu,
            website=website,
            parent=root,
            name=NAV_SHOP_ALL_LABEL,
            url=NAV_SHOP_ALL_URL,
            sequence=NAV_SHOP_ALL_SEQUENCE,
            css_class=NAV_CSS_NO_AUTOHIDE,
        )
    elif menu:
        _unlink_menu(menu)


def _remove_legacy_root_menus(website, root, Menu, active_shop_names):
    protected = MANAGED_FIXED_ROOT_NAMES | set(active_shop_names)
    for menu in Menu.search([('website_id', '=', website.id), ('parent_id', '=', root.id)]):
        if menu.name in protected:
            continue
        if menu.name in LEGACY_ROOT_MENU_NAMES or menu.url in ('/professionnels', '/contactus'):
            _unlink_menu(menu)
        elif menu.ck_nav_css_class in (
            NAV_CSS_DESKTOP_UNIVERSE,
            NAV_CSS_DESKTOP_UNIVERSE_CHILD,
        ):
            _unlink_menu(menu)


def _dedupe_shop_root_menus(website, root, Menu):
    for menu in Menu.search([
        ('website_id', '=', website.id),
        ('parent_id', '=', root.id),
        ('url', '=', NAV_SHOP_ALL_URL),
        ('name', '!=', NAV_SHOP_ALL_LABEL),
    ]):
        _unlink_menu(menu)


def sync_ck_navigation_for_website(env, website):
    root = website.menu_id
    if not root:
        _logger.warning('Nav sync : website %s sans menu racine — skip', website.id)
        return False
    Menu = env['website.menu'].sudo()
    Category = env['product.public.category'].sudo()

    trees = build_shop_nav_trees(env, Category)
    active_shop_names = {tree['name'] for tree in trees}

    _remove_legacy_root_menus(website, root, Menu, active_shop_names)
    _sync_shop_all_menu(env, website, root, Menu)
    _dedupe_shop_root_menus(website, root, Menu)
    _sync_desktop_shop_menus(env, website, root, Menu, trees)
    _sync_mobile_univers_group(env, website, root, Menu, trees)
    _sync_decouvrir_menu(env, website, root, Menu)
    return True


def bootstrap_ck_navigation(env):
    """Synchronise la navigation CK pour chaque site web."""
    Website = env['website'].sudo()
    synced = 0
    for website in Website.search([]):
        if sync_ck_navigation_for_website(env, website):
            synced += 1
    _logger.info('Nav sync : navigation synchronisée pour %s site(s)', synced)
    return synced


def get_nav_category_mapping(env):
    """Mapping opérationnel menu → catégorie BO (recette / doc)."""
    Category = env['product.public.category'].sudo()
    rows = [{
        'menu_label': NAV_SHOP_ALL_LABEL,
        'category_id': None,
        'category_name': 'Catalogue complet',
        'url': NAV_SHOP_ALL_URL,
        'visible': _shop_all_visible(env),
        'published_products': _shop_all_visible(env),
        'level': 0,
        'children': [],
    }]
    for tree in build_shop_nav_trees(env, Category):
        category = Category.browse(tree['category_id'])
        rows.append({
            'menu_label': tree['name'],
            'category_id': tree['category_id'],
            'category_name': category.name if category else tree['name'],
            'url': tree['url'],
            'visible': True,
            'published_products': _category_has_published_products(env, category),
            'level': 1,
            'children': [
                {
                    'menu_label': child['name'],
                    'category_id': child['category_id'],
                    'url': child['url'],
                    'level': 2,
                }
                for child in tree['children']
            ],
        })
    return rows
