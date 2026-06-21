# -*- coding: utf-8 -*-
"""Sections bas de fiche produit CK — Lot 2 (contenus longs conditionnels)."""

import re
from html import unescape

from lxml import etree, html as lxml_html
from markupsafe import Markup

from odoo.tools import html2plaintext

_USAGE_HEADING_RE = re.compile(
    r'^\s*(usage|conseils?\s+d[\u2019\']?usage)\s*:?\s*$',
    re.IGNORECASE,
)
_CONSERVATION_SPLIT_RE = re.compile(
    r'(Avant ouverture\s*:|Après ouverture\s*:)',
    re.IGNORECASE,
)
_SECTION_TITLE_ALIASES = {
    'origine & usage': 'origin_usage',
    'origine et usage': 'origin_usage',
    'description': 'origin_usage',
    'conseils d\'usage': 'usage',
    'conseils d’usage': 'usage',
    'usage': 'usage',
    'conservation': 'conservation',
    'ingrédients & allergènes': 'ingredients',
    'ingredients & allergenes': 'ingredients',
    'ingrédients': 'ingredients',
    'valeurs nutritionnelles': 'nutrition',
    'origine & producteur': 'origin_producer',
    'origine et producteur': 'origin_producer',
}
_SECTION_DISPLAY_TITLES = {
    'origin_usage': 'Origine & usage',
    'usage': "Conseils d'usage",
    'conservation': 'Conservation',
    'ingredients': 'Ingrédients & allergènes',
    'nutrition': 'Valeurs nutritionnelles',
    'origin_producer': 'Origine & producteur',
}


def _normalize_title(title):
    return re.sub(r'\s+', ' ', unescape(title or '').strip().lower())


def _section_key_from_title(title):
    return _SECTION_TITLE_ALIASES.get(_normalize_title(title), '')


def _display_title(key, parsed_title=''):
    if key in _SECTION_DISPLAY_TITLES:
        return _SECTION_DISPLAY_TITLES[key]
    return (parsed_title or '').strip() or _SECTION_DISPLAY_TITLES.get(key, '')


def _plain_text(value):
    return re.sub(r'\s+', ' ', html2plaintext(value or '')).strip()


def _nodes_to_markup(nodes):
    if not nodes:
        return Markup('')
    parts = []
    for node in nodes:
        if isinstance(node, str):
            text = node.strip()
            if text:
                parts.append(text)
            continue
        parts.append(lxml_html.tostring(node, encoding='unicode', method='html'))
    return Markup(''.join(parts))


def _is_usage_label(label):
    label = (label or '').strip().lower()
    if _USAGE_HEADING_RE.match(label):
        return True
    return label.startswith('usage') or label.startswith('conseils d')


def _split_usage_paragraphs(nodes):
    """Extrait le paragraphe Usage d'une section Origine & usage."""
    origin_nodes = []
    usage_nodes = []
    for node in nodes:
        tag = getattr(node, 'tag', None)
        if isinstance(tag, str):
            tag = tag.lower()
        if tag == 'p':
            strongs = node.xpath('.//strong')
            if strongs:
                label = (strongs[0].text_content() or '').strip()
                if _is_usage_label(label):
                    tail = _plain_text(etree.tostring(node, encoding='unicode', method='html'))
                    tail = re.sub(
                        r'^(usage|conseils d[\u2019\']?usage)\s*:?\s*',
                        '',
                        tail,
                        flags=re.IGNORECASE,
                    ).strip()
                    if tail:
                        usage_nodes.append(f'<p>{Markup.escape(tail)}</p>')
                    continue
        origin_nodes.append(node)
    return origin_nodes, usage_nodes


def _conservation_subtitles(nodes):
    """Découpe Conservation en sous-blocs Avant / Après ouverture si détectés."""
    markup = _nodes_to_markup(nodes)
    text = _plain_text(markup)
    if not _CONSERVATION_SPLIT_RE.search(text):
        return [], markup

    subtitles = []
    for match in _CONSERVATION_SPLIT_RE.finditer(text):
        label = match.group(1).rstrip(':').strip()
        start = match.end()
        end = _CONSERVATION_SPLIT_RE.search(text, start)
        end = end.start() if end else len(text)
        body = text[start:end].strip()
        if body:
            subtitles.append({
                'title': label,
                'body': Markup(f'<p>{Markup.escape(body)}</p>'),
            })
    if subtitles:
        return subtitles, Markup('')
    return [], markup


def _append_section(sections, key, title, body, subtitles=None):
    body_markup = body if isinstance(body, Markup) else Markup(body or '')
    body_plain = _plain_text(body_markup)
    subs = subtitles or []
    if not body_plain and not subs:
        return
    for existing in sections:
        if existing['key'] == key:
            if body_plain and not _plain_text(existing.get('body')):
                existing['body'] = body_markup
            if subs and not existing.get('subtitles'):
                existing['subtitles'] = subs
            return
    sections.append({
        'key': key,
        'title': _display_title(key, title),
        'body': body_markup,
        'subtitles': subs,
    })


def _parse_website_description_sections(raw_html):
    """Découpe ``website_description`` en sections CK (bootstrap ``ck-product-enrich`` ou h3)."""
    sections = []
    if not (raw_html or '').strip():
        return sections

    wrapper = lxml_html.fragment_fromstring(raw_html, create_parent='div')
    enrich_nodes = wrapper.xpath(".//div[contains(@class, 'ck-product-enrich')]")
    container = enrich_nodes[0] if enrich_nodes else wrapper

    children = [child for child in container if getattr(child, 'tag', None) is not None]
    if not children:
        return sections

    has_headings = any(child.tag in ('h2', 'h3', 'h4') for child in children)
    if not has_headings:
        body = _nodes_to_markup(children)
        if _plain_text(body):
            _append_section(sections, 'origin_usage', 'Origine & usage', body)
        return sections

    current_title = ''
    current_nodes = []

    def flush():
        nonlocal current_title, current_nodes
        if not current_title and not current_nodes:
            return
        key = _section_key_from_title(current_title) or 'origin_usage'
        parsed_title = current_title
        nodes = list(current_nodes)
        current_title = ''
        current_nodes = []

        if key == 'origin_usage':
            origin_nodes, usage_nodes = _split_usage_paragraphs(nodes)
            origin_body = _nodes_to_markup(origin_nodes)
            if _plain_text(origin_body):
                _append_section(
                    sections,
                    'origin_usage',
                    parsed_title or 'Origine & usage',
                    origin_body,
                )
            if usage_nodes:
                _append_section(
                    sections,
                    'usage',
                    "Conseils d'usage",
                    Markup(''.join(usage_nodes)),
                )
            return

        if key == 'conservation':
            subtitles, body = _conservation_subtitles(nodes)
            _append_section(sections, 'conservation', 'Conservation', body, subtitles=subtitles)
            return

        body = _nodes_to_markup(nodes)
        _append_section(sections, key, parsed_title, body)

    for child in children:
        if child.tag in ('h2', 'h3', 'h4'):
            flush()
            current_title = child.text_content().strip()
        else:
            current_nodes.append(child)
    flush()
    return sections


def _purchase_lead_plain(product):
    return _plain_text(product.description_ecommerce)


def _origin_from_attribute(product):
    from .ck_product_origin import ck_origin_from_attribute

    return ck_origin_from_attribute(product)


def _nutrition_from_documents(product):
    """Image document produit nommée « nutrition » — sans nouveau champ."""
    docs = product.sudo().product_document_ids.filtered(lambda doc: doc.shown_on_product_page)
    for doc in docs:
        attachment = doc.ir_attachment_id
        name = (attachment.name or '').lower()
        if 'nutrition' in name or 'nutri' in name:
            base_url = (product.website_url or '').rstrip('/')
            url = f'{base_url}/document/{doc.id}'
            return Markup(
                f'<p class="mb-2"><a href="{Markup.escape(url)}">'
                f'{Markup.escape(attachment.name)}</a></p>'
            )
    return Markup('')


def build_ck_product_page_detail_sections(product):
    """Construit les sections bas de fiche — uniquement les blocs alimentés."""
    product.ensure_one()
    try:
        return _build_ck_product_page_detail_sections(product)
    except Exception:
        return []


def _build_ck_product_page_detail_sections(product):
    sections = []
    lead_plain = _purchase_lead_plain(product)

    website_html = (product.website_description or '').strip()
    if website_html:
        sections.extend(_parse_website_description_sections(website_html))
    elif (product.description_sale or '').strip():
        body = product.description_sale
        if _plain_text(body) and _plain_text(body) != lead_plain:
            _append_section(sections, 'origin_usage', 'Origine & usage', body)

    # Origine catalogue (attribut) — section dédiée si pas déjà couverte par le texte.
    origin_label = _origin_from_attribute(product)
    if origin_label:
        has_origin_section = any(section['key'] == 'origin_producer' for section in sections)
        origin_in_text = any(
            origin_label.lower() in _plain_text(section.get('body')).lower()
            for section in sections
        )
        if not has_origin_section and not origin_in_text:
            _append_section(
                sections,
                'origin_producer',
                'Origine & producteur',
                Markup(f'<p>{Markup.escape(origin_label)}</p>'),
            )

    nutrition_body = _nutrition_from_documents(product)
    if _plain_text(nutrition_body):
        _append_section(sections, 'nutrition', 'Valeurs nutritionnelles', nutrition_body)

    # Retire les sections dont le corps est identique au lead zone achat.
    filtered = []
    for section in sections:
        body_plain = _plain_text(section.get('body'))
        if body_plain and lead_plain and body_plain == lead_plain:
            continue
        if not body_plain and not section.get('subtitles'):
            continue
        filtered.append(section)
    return filtered
