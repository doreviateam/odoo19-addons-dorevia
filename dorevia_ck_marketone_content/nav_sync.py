# -*- coding: utf-8 -*-
"""Lot Nav-1 — synchronisation header / menus CK Marketone V2."""
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
NAV_CSS_MOBILE_UNIVERS_GROUP = 'ck-nav-mobile-univers'

NAV_UNIVERSE_SPECS = (
    {
        'menu_label': 'Épicerie',
        'category_names': ('Épicerie créole', 'Épicerie'),
        'sequence': 20,
    },
    {
        'menu_label': 'Boissons',
        'category_names': ('Boissons',),
        'sequence': 30,
    },
    {
        'menu_label': 'Soin & Bien-être',
        'category_names': ('Maison & bien-être', 'Soin & bien-être', 'Soin'),
        'sequence': 40,
    },
    {
        'menu_label': 'Artisanat',
        'category_names': ('Artisanat',),
        'sequence': 50,
    },
)

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
})

MANAGED_ROOT_NAMES = frozenset({
    NAV_SHOP_ALL_LABEL,
    NAV_MOBILE_UNIVERS_LABEL,
    NAV_DECOUVRIR_LABEL,
    *(spec['menu_label'] for spec in NAV_UNIVERSE_SPECS),
})


def _find_public_category(Category, names):
    for name in names:
        category = Category.search([('name', '=', name)], limit=1)
        if category:
            return category
    return Category.browse()


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
                 is_mega=False, mega_content=''):
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


def _sync_universe_menus(env, website, root, Menu, Category):
    """Retourne la liste des entrées (label, url, sequence) visibles pour le mobile."""
    visible_entries = []
    for spec in NAV_UNIVERSE_SPECS:
        category = _find_public_category(Category, spec['category_names'])
        url = _category_shop_url(env, category)
        visible = bool(
            category
            and url
            and _category_has_published_products(env, category)
        )
        desktop = Menu.search([
            ('website_id', '=', website.id),
            ('parent_id', '=', root.id),
            ('name', '=', spec['menu_label']),
        ], limit=1)
        if visible:
            _upsert_menu(
                Menu,
                website=website,
                parent=root,
                name=spec['menu_label'],
                url=url,
                sequence=spec['sequence'],
                css_class=NAV_CSS_DESKTOP_UNIVERSE,
            )
            visible_entries.append((spec['menu_label'], url, spec['sequence']))
        elif desktop:
            _unlink_menu(desktop)
    return visible_entries


def _sync_mobile_univers_group(env, website, root, Menu, visible_entries):
    mobile_parent = Menu.search([
        ('website_id', '=', website.id),
        ('parent_id', '=', root.id),
        ('name', '=', NAV_MOBILE_UNIVERS_LABEL),
    ], limit=1)
    if not visible_entries:
        _unlink_menu(mobile_parent)
        if mobile_parent:
            for child in mobile_parent.child_id:
                _unlink_menu(child)
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
    managed_child_names = {label for label, _url, _seq in visible_entries}
    for child in parent.child_id:
        if child.name not in managed_child_names:
            _unlink_menu(child)
    for label, url, sequence in visible_entries:
        _upsert_menu(
            Menu,
            website=website,
            parent=parent,
            name=label,
            url=url,
            sequence=sequence,
            css_class='ck-nav-mobile-universe-child',
        )


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
        )
    elif menu:
        _unlink_menu(menu)


def _remove_legacy_root_menus(website, root, Menu):
    for menu in Menu.search([('website_id', '=', website.id), ('parent_id', '=', root.id)]):
        if menu.name in MANAGED_ROOT_NAMES:
            continue
        if menu.name in LEGACY_ROOT_MENU_NAMES or menu.url in ('/professionnels', '/contactus'):
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
        _logger.warning('Nav-1 : website %s sans menu racine — skip', website.id)
        return False
    Menu = env['website.menu'].sudo()
    Category = env['product.public.category'].sudo()

    _remove_legacy_root_menus(website, root, Menu)
    _sync_shop_all_menu(env, website, root, Menu)
    _dedupe_shop_root_menus(website, root, Menu)
    visible_universes = _sync_universe_menus(env, website, root, Menu, Category)
    _sync_mobile_univers_group(env, website, root, Menu, visible_universes)
    _sync_decouvrir_menu(env, website, root, Menu)
    return True


def bootstrap_ck_navigation(env):
    """Synchronise la navigation Nav V2 pour chaque site web."""
    Website = env['website'].sudo()
    synced = 0
    for website in Website.search([]):
        if sync_ck_navigation_for_website(env, website):
            synced += 1
    _logger.info('Nav-1 : navigation synchronisée pour %s site(s)', synced)
    return synced


def get_nav_category_mapping(env):
    """Mapping opérationnel menu → catégorie BO (recette / doc)."""
    Category = env['product.public.category'].sudo()
    rows = [{
        'menu_label': NAV_SHOP_ALL_LABEL,
        'category_names': [],
        'category_id': None,
        'category_name': 'Catalogue complet',
        'url': NAV_SHOP_ALL_URL,
        'visible': _shop_all_visible(env),
        'published_products': _shop_all_visible(env),
    }]
    for spec in NAV_UNIVERSE_SPECS:
        category = _find_public_category(Category, spec['category_names'])
        url = _category_shop_url(env, category) if category else None
        has_products = _category_has_published_products(env, category)
        rows.append({
            'menu_label': spec['menu_label'],
            'category_names': list(spec['category_names']),
            'category_id': category.id if category else None,
            'category_name': category.name if category else None,
            'url': url,
            'visible': bool(category and url and has_products),
            'published_products': has_products,
        })
    return rows
