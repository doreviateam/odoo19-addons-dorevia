# -*- coding: utf-8 -*-
"""Home Lot 2 / Section 3 — Produits vedettes SSR maquette CK (cartes dédiées)."""
import json
import re
from xml.sax.saxutils import escape

from odoo.tools import format_amount

MIN_FEATURED_PRODUCTS = 5
FEATURED_SECTION_MARKER = 'ck-featured-products'
FEATURED_GRID_MARKER = 'ck-featured-products__grid--stable'
FEATURED_CARD_MARKER = 'ck-product-card'
FEATURED_TITLE = 'Nos coups de cœur'
FEATURED_SUBTITLE = 'Sélection CK · origine, goût et savoir-faire créole'
FEATURED_SHOP_CTA = 'Toute la boutique →'
FEATURED_CARD_CTA = 'Voir le produit'
FEATURED_CARD_CART_CTA = 'Ajouter au panier'
FEATURED_CATEGORY_NAME = 'Coups de cœur'  # curation BO des vedettes (catégorie e-commerce dédiée)
FEATURED_CATEGORY_XMLID = 'dorevia_ck_marketone_content.public_categ_coups_de_coeur'
FEATURED_CURATED_MAX = 8

_DEMO_ORIGIN_BY_NAME_FRAGMENT = (
    ('goyav', 'Réunion'),
    ('galettes', 'Martinique'),
    ('manioc', 'Martinique'),
    ('manio', 'Guadeloupe'),
    ('cracker', 'Guadeloupe'),
    ('savon', 'Martinique'),
    ('vétiver', 'Martinique'),
    ('vetiver', 'Martinique'),
    ('colombo', 'Martinique'),
)

_ORIGIN_KEYWORDS = (
    'Réunion',
    'Guadeloupe',
    'Martinique',
    'Guyane',
    'Mayotte',
    'Sélection CK',
)

_CATEGORY_SHORT_LABELS = (
    'Épicerie',
    'Snacks',
    'Condiments',
    'Bien-être',
    'Boissons',
    'Packs',
)

_DEMO_CATEGORY_BY_NAME_FRAGMENT = (
    ('manio', 'Snacks'),
    ('cracker', 'Snacks'),
    ('savon', 'Bien-être'),
    ('vétiver', 'Bien-être'),
    ('vetiver', 'Bien-être'),
    ('colombo', 'Condiments'),
    ('goyav', 'Épicerie'),
    ('galettes', 'Épicerie'),
    ('manioc', 'Épicerie'),
)

_PLACEHOLDER_MARKERS = (
    'website.s_cover_default_image',
    's_cover_default',
    'o_wsale_product_grid_wrapper_placeholder',
    'is_sample',
)

_CARD_IMAGE_RE = re.compile(
    r"background-image:\s*url\(\s*['\"]?/web/image/product\.(?:template|product)/\d+/",
    re.IGNORECASE,
)
_CARD_PRICE_RE = re.compile(r'class="price"')
_CARD_LINK_RE = re.compile(r'class="card-cta(?:\s|")')
_CARD_COVER_RE = re.compile(r'ck-product-card__cover')
_CARD_CTA_TEXT_RE = re.compile(re.escape(FEATURED_CARD_CTA))
_FEATURED_LABELS_BLOCK_RE = re.compile(
    r'<p class="product-card-labels">[^<]+</p>',
)

FEATURED_TITLE_SECTION = ''  # rétro-compat tests import — section unique désormais


def _arch_as_string(arch):
    if isinstance(arch, dict):
        return next(iter(arch.values()), '')
    return arch or ''


def _variant_has_valid_image(variant):
    template = variant.product_tmpl_id
    if variant.image_1920 or variant.image_512:
        return True
    return bool(template.image_1920 or template.image_512)


def _template_featured_variant_cap(template):
    """Multi-variantes : une carte par variante publiée (ex. ligne manioc)."""
    if len(template.product_variant_ids) > 1:
        return len(template.product_variant_ids)
    return 1


def get_ready_featured_variants(env, *, min_count=MIN_FEATURED_PRODUCTS, max_count=MIN_FEATURED_PRODUCTS):
    """Variantes publiées — une entrée par variante si template multi-variantes."""
    templates = env['product.template'].sudo().search([
        ('is_published', '=', True),
        ('website_published', '=', True),
        ('sale_ok', '=', True),
    ], order='website_sequence asc, id asc')

    variants = env['product.product'].browse()
    for template in templates:
        if not template.image_1920 and not any(
            v.image_1920 or v.image_512 for v in template.product_variant_ids
        ):
            continue
        candidates = template.product_variant_ids.filtered(
            lambda v: v.is_published and v.sale_ok and _variant_has_valid_image(v)
        ).sorted(key=lambda v: v.id)
        if not candidates:
            continue
        cap = _template_featured_variant_cap(template)
        variants |= candidates[:cap]
        if len(variants) >= max_count:
            break

    if len(variants) < min_count:
        return env['product.product'].browse()
    return variants[:max_count]


def _merge_duplicate_featured_categories(env, canonical):
    """Fusionne les doublons « Coups de cœur » vers la catégorie xmlid canonique."""
    Category = env['product.public.category'].sudo()
    dupes = Category.search([
        ('name', '=', FEATURED_CATEGORY_NAME),
        ('id', '!=', canonical.id),
    ])
    if not dupes:
        return canonical
    Template = env['product.template'].sudo()
    for dupe in dupes:
        for tmpl in Template.search([('public_categ_ids', 'in', dupe.ids)]):
            cmds = [(3, dupe.id)]
            if canonical not in tmpl.public_categ_ids:
                cmds.append((4, canonical.id))
            tmpl.write({'public_categ_ids': cmds})
        dupe.unlink()
    return canonical


def _ensure_featured_category(env):
    """Catégorie e-commerce 'Coups de cœur' — support de la curation BO (créée si absente)."""
    category = env.ref(FEATURED_CATEGORY_XMLID, raise_if_not_found=False)
    if category:
        return _merge_duplicate_featured_categories(env, category.sudo())
    Category = env['product.public.category'].sudo()
    category = Category.search([('name', '=', FEATURED_CATEGORY_NAME)], limit=1)
    if not category:
        category = Category.create({'name': FEATURED_CATEGORY_NAME})
    module, name = FEATURED_CATEGORY_XMLID.split('.', 1)
    existing = env['ir.model.data'].sudo().search([
        ('module', '=', module),
        ('name', '=', name),
    ], limit=1)
    if not existing:
        env['ir.model.data'].sudo().create({
            'module': module,
            'name': name,
            'model': category._name,
            'res_id': category.id,
            'noupdate': True,
        })
    return _merge_duplicate_featured_categories(env, category.sudo())


def get_curated_featured_variants(env, *, max_count=FEATURED_CURATED_MAX):
    """Vedettes curatées en BO : produits publiés rangés dans 'Coups de cœur', ordre website_sequence.

    Renvoie un recordset vide si la catégorie n'existe pas ou ne contient aucun produit
    publié — le bootstrap retombe alors sur la sélection automatique (comportement #73).
    """
    category = env.ref(FEATURED_CATEGORY_XMLID, raise_if_not_found=False)
    if not category:
        return env['product.product'].browse()
    category = category.sudo()
    templates = env['product.template'].sudo().search([
        ('public_categ_ids', 'in', category.ids),
        ('is_published', '=', True),
        ('website_published', '=', True),
        ('sale_ok', '=', True),
    ], order='website_sequence asc, id asc')
    templates.mapped('product_tag_ids')
    variants = env['product.product'].browse()
    for template in templates:
        candidates = template.product_variant_ids.filtered(
            lambda v: v.is_published and v.sale_ok and _variant_has_valid_image(v)
        ).sorted(key=lambda v: v.id)
        if candidates:
            candidates.mapped('additional_product_tag_ids')
        if not candidates:
            continue
        cap = _template_featured_variant_cap(template)
        variants |= candidates[:cap]
        if len(variants) >= max_count:
            break
    return variants[:max_count]


def _get_featured_origin_label(template):
    for line in template.attribute_line_ids:
        attr_name = (line.attribute_id.name or '').lower()
        if 'origine' in attr_name or 'origin' in attr_name:
            value = line.value_ids[:1]
            if value and (value.name or '').strip():
                return value.name.strip()
    haystack = ' '.join(filter(None, [
        template.description_sale or '',
        template.name or '',
    ]))
    lowered = haystack.lower()
    for keyword in _ORIGIN_KEYWORDS:
        if keyword.lower() in lowered:
            return keyword
    name_lower = (template.name or '').lower()
    for fragment, origin in _DEMO_ORIGIN_BY_NAME_FRAGMENT:
        if fragment in name_lower:
            return origin
    return ''


def _get_featured_category_label(template):
    category = template.public_categ_ids[:1]
    if not category:
        return ''
    name = (category.name or '').strip()
    if '—' in name:
        name = name.split('—', 1)[0].strip()
    lowered = name.lower()
    for short in _CATEGORY_SHORT_LABELS:
        if short.lower() in lowered:
            return short
    name_lower = (template.name or '').lower()
    for fragment, label in _DEMO_CATEGORY_BY_NAME_FRAGMENT:
        if fragment in name_lower:
            return label
    return name.split()[0] if name else ''


def _get_featured_display_name(variant):
    template = variant.product_tmpl_id
    if len(template.product_variant_ids) <= 1:
        return template.name or variant.display_name or ''
    value_names = [
        name for name in variant.product_template_attribute_value_ids.mapped('name')
        if name
    ]
    if value_names:
        return value_names[0] if len(value_names) == 1 else ' · '.join(value_names)
    display = (variant.display_name or '').strip()
    template_name = (template.name or '').strip()
    if template_name and display.startswith(template_name):
        short = display[len(template_name):].strip(' ,()-')
        if short:
            return short
    return display or template_name


def _get_featured_image_url(variant):
    template = variant.product_tmpl_id
    if variant.image_1920 or variant.image_512:
        return f'/web/image/product.product/{variant.id}/image_512'
    if template.image_1920 or template.image_512:
        return f'/web/image/product.template/{template.id}/image_512'
    for sibling in template.product_variant_ids:
        if sibling.image_1920 or sibling.image_512:
            return f'/web/image/product.product/{sibling.id}/image_512'
    return f'/web/image/product.template/{template.id}/image_512'


def _get_featured_price_amount(env, website, variant):
    """Prix B2C de la carte vedette — sans requête HTTP (PR-4 / H1).

    Pipeline validé sur instance (candidat B) : prix pricelist + position fiscale
    + couche taxes ``_apply_taxes_to_price`` (TTC/HT selon
    ``website.show_line_subtotals_tax_selection``). Reproduit la sortie de l'ancien
    ``_get_combination_info`` (qui s'appuyait sur une fausse requête, supprimée)."""
    template = variant.product_tmpl_id
    pricelist = website.sudo().get_pricelist_available()[:1]
    currency = (pricelist.currency_id if pricelist else None) or website.currency_id
    if pricelist:
        pricelist_price = pricelist._get_product_price(variant, 1.0)
    else:
        # Sans pricelist publique : prix catalogue de la variante affichée (pas le template).
        pricelist_price = variant.lst_price
    company = website.company_id or env.company
    product_taxes = variant.sudo().taxes_id.filtered(lambda t: t.company_id == company)
    fpos = env['account.fiscal.position'].sudo()._get_fiscal_position(env.user.partner_id)
    taxes = fpos.map_tax(product_taxes) if fpos else product_taxes
    return template._apply_taxes_to_price(
        pricelist_price, currency, product_taxes, taxes, variant, website=website,
    )


def _get_featured_price_label(env, website, variant):
    price = _get_featured_price_amount(env, website, variant)
    return format_amount(env, price, website.currency_id)


def _normalize_label_token(value):
    return (value or '').strip().lower().replace('œ', 'oe')


def _is_excluded_featured_label(name):
    normalized = _normalize_label_token(name)
    if not normalized:
        return True
    excluded = {
        _normalize_label_token(FEATURED_CATEGORY_NAME),
        'coups de coeur',
    }
    return normalized in excluded or 'coups de coeur' in normalized


def _tag_display_name(name_value):
    if isinstance(name_value, dict):
        for key in ('fr_FR', 'en_US'):
            label = (name_value.get(key) or '').strip()
            if label:
                return label
        for label in name_value.values():
            text = (label or '').strip()
            if text:
                return text
        return ''
    if isinstance(name_value, str):
        stripped = name_value.strip()
        if stripped.startswith('{'):
            try:
                return _tag_display_name(json.loads(stripped))
            except json.JSONDecodeError:
                return stripped
        return stripped
    return (name_value or '').strip()


def _featured_label_parts_from_tags(tags):
    parts = []
    for tag in tags:
        name = _tag_display_name(tag.name)
        if name and not _is_excluded_featured_label(name):
            parts.append(name)
    return parts


def _featured_label_parts_from_sql(cr, template_id, variant_id=None):
    """Lecture SQL directe — template + variante (product_tag_ids + additional_product_tag_ids).

    QA M4 : accès SQL direct assumé pour la performance du rendu SSR des cartes
    (évite N lectures ORM par carte sur la home). Cible les tables de relation
    ``product_tag_product_template_rel`` / ``product_tag_product_product_rel``.
    Requête entièrement paramétrée (%s) — pas d'injection. Contournement
    volontaire des record rules (exécution en contexte sudo de seed/refresh).
    Un repli ORM existe dans ``_get_featured_labels_line`` si la lecture SQL ne
    renvoie aucune étiquette."""
    if variant_id:
        cr.execute(
            """
            SELECT pt.sequence, pt.name, pt.id
              FROM product_tag pt
             WHERE pt.id IN (
                    SELECT product_tag_id
                      FROM product_tag_product_template_rel
                     WHERE product_template_id = %s
                    UNION
                    SELECT product_tag_id
                      FROM product_tag_product_product_rel
                     WHERE product_product_id = %s
                   )
             ORDER BY pt.sequence, pt.id
            """,
            (template_id, variant_id),
        )
    else:
        cr.execute(
            """
            SELECT pt.sequence, pt.name, pt.id
              FROM product_tag pt
              JOIN product_tag_product_template_rel rel
                ON rel.product_tag_id = pt.id
             WHERE rel.product_template_id = %s
             ORDER BY pt.sequence, pt.id
            """,
            (template_id,),
        )
    parts = []
    seen = set()
    for _sequence, raw_name, tag_id in cr.fetchall():
        if tag_id in seen:
            continue
        seen.add(tag_id)
        name = _tag_display_name(raw_name)
        if name and not _is_excluded_featured_label(name):
            parts.append(name)
    return parts


def _featured_tags_for_card(template, variant=None):
    """Union ORM template + étiquettes variante, tri maquette."""
    template = template.sudo()
    variant = (variant or template.product_variant_ids[:1]).sudo()
    tags = template.product_tag_ids
    if variant:
        tags = tags | variant.additional_product_tag_ids
    return tags.sorted(key=lambda tag: (tag.sequence, tag.id))


def _get_featured_labels_line(template, variant=None):
    """Ligne descriptive client — product_tag_ids (+ variante), jamais « Coups de cœur »."""
    template = template.sudo()
    variant = (variant or template.product_variant_ids[:1]).sudo()
    variant_id = variant.id if variant else None
    parts = _featured_label_parts_from_sql(template.env.cr, template.id, variant_id)
    if not parts:
        parts = _featured_label_parts_from_tags(_featured_tags_for_card(template, variant))
    return ' · '.join(parts)


def _featured_arch_missing_product_labels(env, arch, variants):
    """True si des vedettes ont des étiquettes BO mais l'arch home ne les affiche pas."""
    if FEATURED_SECTION_MARKER not in (arch or ''):
        return False
    templates = variants.mapped('product_tmpl_id').sudo()
    for variant in variants:
        line = _get_featured_labels_line(variant.product_tmpl_id, variant)
        if not line:
            continue
        if not _FEATURED_LABELS_BLOCK_RE.search(arch):
            return True
        if line not in arch:
            return True
    return False


def _featured_arch_missing_cart_cta(env, website, arch, variants):
    """True si une vedette éligible au quick-add n'a pas le CTA panier dans l'arch home."""
    if FEATURED_SECTION_MARKER not in (arch or ''):
        return False
    for variant in variants:
        if not _featured_variant_allows_quick_add(env, website, variant):
            continue
        if 'class="card-cart-cta"' not in arch:
            return True
        product_marker = f'data-product-id="{variant.id}"'
        if product_marker not in arch:
            return True
    return False


def _featured_card_arch_chunk(arch, variant):
    marker = f'data-product-id="{variant.id}"'
    idx = arch.find(marker)
    if idx < 0:
        return ''
    start = arch.rfind('<article', 0, idx)
    end = arch.find('</article>', idx)
    if start < 0 or end < 0:
        return ''
    return arch[start:end]


def _featured_arch_stale_cards(env, website, arch, variants):
    """True si prix ou métadonnées SSR d'une vedette ne correspondent plus au BO."""
    if FEATURED_SECTION_MARKER not in (arch or ''):
        return False
    for variant in variants:
        chunk = _featured_card_arch_chunk(arch, variant)
        if not chunk:
            continue
        expected_title = escape(_get_featured_display_name(variant))
        title_match = re.search(r'class="product-card-title"[^>]*>([^<]+)', chunk)
        if title_match and title_match.group(1) != expected_title:
            return True
        expected_price = escape(_get_featured_price_label(env, website, variant))
        price_match = re.search(r'class="price"[^>]*>([^<]+)', chunk)
        if price_match and price_match.group(1) != expected_price:
            return True
        expected_labels = escape(_get_featured_card_metadata_line(env, website, variant))
        if expected_labels:
            labels_match = re.search(r'class="product-card-labels"[^>]*>([^<]+)', chunk)
            if labels_match and labels_match.group(1) != expected_labels:
                return True
    return False


def _format_featured_quantity_value(quantity):
    if quantity == int(quantity):
        return str(int(quantity))
    text = f'{quantity:.2f}'.rstrip('0').rstrip('.')
    return text.replace('.', ',')


def _format_featured_net_quantity(quantity, net_uom):
    if not quantity or quantity <= 0 or not net_uom:
        return ''
    qty_text = _format_featured_quantity_value(quantity)
    if net_uom.family == 'unit':
        unit_label = net_uom.name or 'pièce'
        if quantity != 1 and unit_label == 'pièce':
            unit_label = 'pièces'
        return f'{qty_text} {unit_label}'
    label = (net_uom.name or net_uom.code or '').strip()
    return f'{qty_text} {label}' if label else qty_text


def _compute_featured_reference_unit_price(price, quantity, net_uom, ref_uom):
    if price is None or price <= 0 or not quantity or quantity <= 0:
        return None
    if not net_uom or not ref_uom:
        return None
    if net_uom.family == 'unit' or net_uom.family != ref_uom.family:
        return None
    if net_uom.ratio <= 0 or ref_uom.ratio <= 0:
        return None
    divisor = quantity * net_uom.ratio
    if divisor <= 0:
        return None
    return price / divisor


def _format_featured_reference_price(env, website, price, template):
    if not template.ck_show_reference_price:
        return ''
    ref_uom = template.ck_reference_price_uom_id
    net_uom = template.ck_net_quantity_uom_id
    if not ref_uom or not net_uom:
        return ''
    unit_price = _compute_featured_reference_unit_price(
        price,
        template.ck_net_quantity,
        net_uom,
        ref_uom,
    )
    if unit_price is None:
        return ''
    amount = format_amount(env, unit_price, website.currency_id)
    ref_label = (ref_uom.name or ref_uom.code or '').strip()
    return f'{amount}/{ref_label}' if ref_label else amount


def _join_featured_metadata_parts(*parts):
    """Joint les segments d'étiquette en ignorant les valeurs vides (pas de « · » orphelin)."""
    return ' · '.join(part for part in parts if part)


def _get_featured_format_and_reference_parts(env, website, variant):
    """Format net (ex. 100 g) et prix comparatif (ex. 36,00 €/kg) — logique inchangée."""
    template = variant.product_tmpl_id
    qty_part = _format_featured_net_quantity(
        template.ck_net_quantity,
        template.ck_net_quantity_uom_id,
    )
    if not qty_part:
        return '', ''
    price = _get_featured_price_amount(env, website, variant)
    ref_part = _format_featured_reference_price(env, website, price, template)
    return qty_part, ref_part


def _get_featured_commercial_line(env, website, variant):
    """Format + prix comparatif (sans catégorie/origine) — conservé pour les tests unitaires."""
    qty_part, ref_part = _get_featured_format_and_reference_parts(env, website, variant)
    if not qty_part:
        return ''
    return _join_featured_metadata_parts(qty_part, ref_part)


def _get_featured_card_metadata_line(env, website, variant):
    """Ligne unique sous le titre : catégorie · origine · format · prix comparatif."""
    template = variant.product_tmpl_id
    labels = _get_featured_labels_line(template, variant)
    qty_part, ref_part = _get_featured_format_and_reference_parts(env, website, variant)
    return _join_featured_metadata_parts(labels, qty_part, ref_part)


_SAFE_CSS_COLOR_RE = re.compile(
    r'^#[0-9A-Fa-f]{3,8}$|^rgba?\([\d\s.,%]+\)$|^hsla?\([\d\s.,%]+\)$|^[a-zA-Z]+$'
)


def _safe_css_color(value):
    """QA L1 : n'autorise qu'une couleur CSS simple (hex/rgb/hsl/mot-clé) en inline style.

    Les valeurs `bg_color` / `text_color` du ruban e-commerce sont saisies en BO ;
    on les filtre avant injection dans un attribut `style` pour écarter tout
    contenu non couleur (défense XSS, risque faible mais réel)."""
    value = (value or '').strip()
    return value if _SAFE_CSS_COLOR_RE.match(value) else ''


def _featured_ribbon_badge_class(ribbon):
    """Classes maquette CK pour les libellés ruban courants."""
    name = (ribbon.name or '').lower()
    if 'nouveau' in name or 'new' in name:
        return 'badge-new'
    if any(token in name for token in ('coup', 'cœur', 'coeur', 'vente', 'sale', 'promo')):
        return 'badge-heart'
    return 'badge-ribbon'


def _featured_variant_allows_quick_add(env, website, variant):
    """Éligibilité ajout panier direct — alignée ``_website_show_quick_add`` sans requête HTTP."""
    template = variant.product_tmpl_id.sudo()
    if template.type == 'combo':
        return False
    if not variant.sale_ok or not template.sale_ok:
        return False
    if not template.website_published or not variant.active:
        return False
    if not template._is_add_to_cart_possible():
        return False
    if website.prevent_zero_price_sale and not _get_featured_price_amount(env, website, variant):
        return False
    return True


def _get_featured_badge_html(variant):
    """Badge carte = ruban e-commerce BO (`website_ribbon_id` sur le template)."""
    ribbon = variant.product_tmpl_id.website_ribbon_id
    if not ribbon:
        return ''
    label = escape(ribbon.name or '')
    css_class = _featured_ribbon_badge_class(ribbon)
    if css_class == 'badge-ribbon':
        styles = []
        bg_color = _safe_css_color(ribbon.bg_color)
        if bg_color:
            styles.append(f'background-color:{bg_color}')
        text_color = _safe_css_color(ribbon.text_color)
        if text_color:
            styles.append(f'color:{text_color}')
        style_attr = f' style="{"; ".join(styles)}"' if styles else ''
    else:
        style_attr = ''
    return f'<span class="badge {css_class} badge-float"{style_attr}>{label}</span>'


def build_featured_product_card_html(env, website, variant):
    """Carte produit home V1.1 — étiquettes BO, quantité nette, prix de référence."""
    template = variant.product_tmpl_id
    display_name = _get_featured_display_name(variant)
    href = escape(variant.website_url or template.website_url or '/shop')
    image_url = _get_featured_image_url(variant)
    price_label = escape(_get_featured_price_label(env, website, variant))
    metadata_line = escape(_get_featured_card_metadata_line(env, website, variant))
    badge_html = _get_featured_badge_html(variant)
    card_title = escape(display_name)
    card_aria = escape(f'{FEATURED_CARD_CTA} : {display_name}')

    labels_block = (
        f'<p class="product-card-labels">{metadata_line}</p>'
        if metadata_line else ''
    )
    if _featured_variant_allows_quick_add(env, website, variant):
        actions_html = f"""<div class="product-card-actions">
            <button type="button" class="card-cart-cta" data-product-id="{variant.id}" data-product-template-id="{template.id}">{FEATURED_CARD_CART_CTA}</button>
            <a href="{href}" class="card-cta card-cta--secondary">{FEATURED_CARD_CTA}</a>
        </div>"""
    else:
        actions_html = f"""<div class="product-card-actions product-card-actions--view-only">
            <a href="{href}" class="card-cta">{FEATURED_CARD_CTA}</a>
        </div>"""

    return f"""
<article class="{FEATURED_CARD_MARKER} product-card ck-product-card--interactive">
    <a href="{href}" class="ck-product-card__cover" aria-label="{card_aria}"></a>
    <div class="product-card-media ck-product-card__media" style="background-image:url('{image_url}')">
        {badge_html}
    </div>
    <div class="product-card-body">
        <h3 class="product-card-title">{card_title}</h3>
        {labels_block}
    </div>
    <div class="product-card-foot">
        <div class="product-card-pricing">
            <span class="price">{price_label}</span>
        </div>
        {actions_html}
    </div>
</article>""".strip()


def card_fragment_is_valid(fragment):
    """Carte SSR maquette : image template, prix, CTA Voir le produit — pas de placeholder."""
    if not fragment or FEATURED_CARD_MARKER not in fragment:
        return False
    lowered = fragment.lower()
    if any(marker in lowered for marker in _PLACEHOLDER_MARKERS):
        return False
    if not _CARD_IMAGE_RE.search(fragment):
        return False
    if not _CARD_PRICE_RE.search(fragment):
        return False
    if not _CARD_LINK_RE.search(fragment):
        return False
    if not _CARD_COVER_RE.search(fragment):
        return False
    if not _CARD_CTA_TEXT_RE.search(fragment):
        return False
    return True


def render_ck_featured_cards(env, website, variants):
    """Pré-rendu serveur des cartes maquette (pas Dynamic Products / oe_product_cart)."""
    cards = []
    for variant in variants:
        card = build_featured_product_card_html(env, website, variant)
        if card_fragment_is_valid(card):
            cards.append(card)
    return cards


# Alias rétro-compat Lot 2
render_featured_card_fragments = render_ck_featured_cards


def build_featured_ssr_arch(card_fragments):
    """Section vedettes maquette — en-tête + grille CSS 3 colonnes."""
    cards_inner = '\n            '.join(card_fragments)
    return f"""
<section class="s_ck_featured_products {FEATURED_SECTION_MARKER} ck-featured-products--maquette pt48 pb48 o_colored_level" data-snippet="s_ck_featured_products" data-name="Produits vedettes">
    <div class="container">
        <div class="ck-featured-products__head">
            <div class="ck-featured-products__head-text">
                <h2 id="featured-title" class="ck-featured-products__title h3 mb-0 o_editable">{FEATURED_TITLE}</h2>
                <p class="ck-featured-products__subtitle mb-0 o_editable">{FEATURED_SUBTITLE}</p>
            </div>
            <a href="/shop" class="btn btn-secondary ck-featured-products__shop-cta o_editable">{FEATURED_SHOP_CTA}</a>
        </div>
        <div class="{FEATURED_GRID_MARKER} ck-featured-products__grid product-grid">
            {cards_inner}
        </div>
    </div>
</section>
""".strip()


def _remove_all_featured_sections(arch):
    """Retire toute section vedettes injectée (évite les doublons après re-bootstrap)."""
    while True:
        marker = arch.find('data-snippet="s_ck_featured_products"')
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


def _find_featured_insertion_index(arch):
    insert_at = arch.find('<section class="s_ck_category_links')
    if insert_at < 0:
        marker = arch.find('data-snippet="s_ck_category_links"')
        if marker >= 0:
            insert_at = arch.rfind('<section', 0, marker)
    if insert_at >= 0:
        return insert_at
    # Repli si la section catégories est absente : insérer juste après la trust-bar
    # (réassurance), sinon après le hero — pour conserver l'ordre maquette.
    for anchor in ('data-snippet="s_ck_reassurance"', 'ck-reassurance--trust-bar',
                   'data-snippet="s_ck_hero"', 'id="hero-title"'):
        pos = arch.find(anchor)
        if pos >= 0:
            end = arch.find('</section>', pos)
            if end >= 0:
                return end + len('</section>')
    return insert_at


def _patch_homepage_featured_arch(arch, featured_arch):
    cleaned = _remove_all_featured_sections(arch)
    if not featured_arch:
        return cleaned, cleaned != arch

    insert_at = _find_featured_insertion_index(cleaned)
    if insert_at < 0:
        return arch, False
    new_arch = cleaned[:insert_at] + featured_arch + '\n' + cleaned[insert_at:]
    return new_arch, True


def refresh_home_featured_products(env):
    """Rafraîchit la section vedettes depuis le BO (produit ou catégorie)."""
    return bootstrap_home_featured_products(env)


def bootstrap_home_featured_products(env):
    """Lot 2 home — injecte la grille SSR vedettes maquette ou masque si BO insuffisant."""
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

    _ensure_featured_category(env)
    variants = get_curated_featured_variants(env)
    curated = bool(variants)
    if not curated:
        variants = get_ready_featured_variants(env)  # repli : sélection automatique (#73)
    featured_arch = ''
    if variants:
        cards = render_ck_featured_cards(env, website, variants)
        min_cards = 1 if curated else MIN_FEATURED_PRODUCTS
        if len(cards) >= min_cards:
            limit = len(cards) if curated else MIN_FEATURED_PRODUCTS
            featured_arch = build_featured_ssr_arch(cards[:limit])

    new_arch, patched = _patch_homepage_featured_arch(arch, featured_arch)
    stale_labels = _featured_arch_missing_product_labels(env, arch, variants)
    stale_cart_cta = _featured_arch_missing_cart_cta(env, website, arch, variants)
    stale_cards = _featured_arch_stale_cards(env, website, arch, variants)
    if not patched and not stale_labels and not stale_cart_cta and not stale_cards:
        return False
    if not featured_arch:
        if patched and new_arch != arch:
            view.write({'arch_db': new_arch})
        return patched
    if new_arch == arch and not stale_labels and not stale_cart_cta and not stale_cards:
        return patched

    view.write({'arch_db': new_arch})
    return True
