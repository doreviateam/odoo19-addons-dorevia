# -*- coding: utf-8 -*-
"""Page CMS /nos-producteurs — Header CK V2.2."""

NOS_PRODUCTEURS_PAGE_URL = '/nos-producteurs'
NOS_PRODUCTEURS_VIEW_KEY = 'dorevia_ck_marketone_content.nos_producteurs_page'
NOS_PRODUCTEURS_PAGE_NAME = 'Nos producteurs'
PRODUCER_PILOT_URL = '/producteur/atelier-hauts-goyaviers'


def _qualified_producers(env):
    """Fiches producteurs minimales — pages CMS publiées /producteur/…"""
    rows = []
    Page = env['website.page'].sudo()
    website = env['website'].search([], limit=1)
    if not website:
        return rows
    for page in Page.search([
        ('website_id', '=', website.id),
        ('is_published', '=', True),
        ('url', '=like', '/producteur/%'),
    ], order='url'):
        slug = (page.url or '').rsplit('/', 1)[-1]
        name = page.name or slug.replace('-', ' ').title()
        rows.append({
            'name': name,
            'origin': 'Territoire créole',
            'teaser': 'Producteur partenaire C-Kréyòl — origine et savoir-faire identifiés.',
            'url': page.url,
        })
    if not rows:
        rows.append({
            'name': 'Atelier Les Hauts Goyaviers',
            'origin': 'La Réunion',
            'teaser': 'Trois générations de transformateurs — confitures artisanales.',
            'url': PRODUCER_PILOT_URL,
        })
    return rows


def build_nos_producteurs_page_arch(env):
    producers = _qualified_producers(env)
    items = []
    for producer in producers[:24]:
        items.append(
            f'<div class="col-md-6 col-lg-4">'
            f'<div class="h-100 p-4 border rounded o_colored_level">'
            f'<p class="text-muted small mb-2">{producer["origin"]}</p>'
            f'<h2 class="h5-fs mb-2">{producer["name"]}</h2>'
            f'<p class="text-muted mb-3">{producer["teaser"]}</p>'
            f'<a href="{producer["url"]}" class="btn btn-link px-0">Voir les produits →</a>'
            f'</div></div>'
        )
    cards = '<div class="row g-4">' + ''.join(items) + '</div>'
    return f"""
<div id="wrap" class="oe_structure ck-producteurs-page">
<section class="s_title pt64 pb16 o_colored_level" data-snippet="s_title" data-name="Intro producteurs">
    <div class="container s_allow_columns">
        <h1 class="display-5 fw-bold">Nos producteurs &amp; artisans</h1>
        <p class="lead text-muted mb-0">
            Chaque produit C-Kréyòl est rattaché à un acteur identifié — origines lisibles,
            savoir-faire et traçabilité au cœur de notre sélection.
        </p>
    </div>
</section>
<section class="s_text_block pt16 pb64 o_colored_level" data-snippet="s_text_block" data-name="Grille producteurs">
    <div class="container">{cards}</div>
</section>
<section class="s_text_block pt0 pb64 o_colored_level" data-snippet="s_text_block" data-name="CTA producteurs">
    <div class="container s_allow_columns">
        <p class="mb-0">
            <a href="/shop" class="btn btn-primary me-2">Voir les produits</a>
            <a href="/professionnels#partenaire" class="btn btn-secondary">Proposer un producteur</a>
        </p>
    </div>
</section>
</div>
""".strip()


def bootstrap_nos_producteurs_page(env):
    from .hooks import _bootstrap_cms_page

    return _bootstrap_cms_page(
        env,
        page_url=NOS_PRODUCTEURS_PAGE_URL,
        view_key=NOS_PRODUCTEURS_VIEW_KEY,
        view_name='Nos producteurs CK V2.2',
        page_name=NOS_PRODUCTEURS_PAGE_NAME,
        arch=build_nos_producteurs_page_arch(env),
        website_indexed=False,
    )
