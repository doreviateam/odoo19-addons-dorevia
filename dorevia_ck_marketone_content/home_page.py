# -*- coding: utf-8 -*-
"""Homepage site-specific — résolution / vs page globale Odoo 19 (install fraîche)."""
from odoo.fields import Domain


def get_website_homepage_page(env, website=None):
    """Page d'accueil propre au site (``website_id``), pas la page / générique."""
    website = website or env['website'].sudo().search([], limit=1)
    if not website:
        return website, env['website.page'].browse()
    page = env['website.page'].sudo().search([
        ('url', '=', '/'),
        ('website_id', '=', website.id),
    ], limit=1)
    return website, page


def resolve_homepage_page_for_website(env, website):
    """Reproduit la sélection Odoo ``_get_page_info`` pour ``/``."""
    page_domain = Domain('url', '=', '/') & website.website_domain()
    return env['website.page'].sudo().search_fetch(
        page_domain,
        order='website_id asc',
        limit=1,
    )


def ensure_website_homepage_page(env, website=None):
    """Garantit une ``website.page`` ``/`` liée au site (COW depuis la page globale si besoin)."""
    website, page = get_website_homepage_page(env, website)
    if not website:
        return env['website.page'].browse()
    if page:
        return page

    Page = env['website.page'].sudo()
    View = env['ir.ui.view'].sudo()
    global_page = Page.search([
        ('url', '=', '/'),
        ('website_id', '=', False),
    ], limit=1)
    if global_page and global_page.view_id:
        new_view = global_page.view_id.with_context(website_id=website.id).copy({
            'website_id': website.id,
        })
        return Page.create({
            'name': global_page.name or 'Home',
            'url': '/',
            'website_id': website.id,
            'view_id': new_view.id,
            'is_published': True,
        })

    view = View.create({
        'name': 'Home',
        'type': 'qweb',
        'key': f'dorevia_ck_marketone_content.homepage_{website.id}',
        'arch': """<t name="Home" t-name="website.homepage">
    <t t-call="website.layout" pageName.f="homepage">
        <div id="wrap" class="oe_structure oe_empty"/>
    </t>
</t>""",
        'website_id': website.id,
    })
    return Page.create({
        'name': 'Home',
        'url': '/',
        'website_id': website.id,
        'view_id': view.id,
        'is_published': True,
    })


def remove_global_homepage_conflicts(env):
    """Supprime la page / générique qui peut primer sur la home site (``order website_id asc``)."""
    Page = env['website.page'].sudo()
    removed = False
    for website in env['website'].sudo().search([]):
        if not Page.search_count([('url', '=', '/'), ('website_id', '=', website.id)]):
            continue
        global_pages = Page.search([('url', '=', '/'), ('website_id', '=', False)])
        if global_pages:
            global_pages.unlink()
            removed = True
    return removed


def bootstrap_website_homepage_binding(env):
    """Post-install / migration — home site-specific publiée, sans doublon global /."""
    changed = False
    for website in env['website'].sudo().search([]):
        page = ensure_website_homepage_page(env, website)
        if not page:
            continue
        if not page.is_published:
            page.write({'is_published': True})
            changed = True
    if remove_global_homepage_conflicts(env):
        changed = True
    return changed
