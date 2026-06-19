# -*- coding: utf-8 -*-
"""Hooks dorevia_ck_marketone_content — seed contenu CK Marketone.

Pages CMS, enrichissements catalogue, mailing list, fiche producteur pilote.
Module optionnel : ``dorevia_ck_theme`` reste un thème générique sans ce contenu.
"""
import logging
import re
from xml.sax.saxutils import escape

from .catalog_manioc_variants import bootstrap_catalog_vedettes_products
from .home_arch import _arch_fingerprint
from .home_discovery_pack import bootstrap_home_discovery_pack
from .home_featured import bootstrap_home_featured_products
from .legal_pages import (
    FOOTER_CONTACT_LINK_MARKER,
    FOOTER_LEGAL_LINK_HTML,
    FOOTER_PRIVACY_LINK_HTML,
    FOOTER_TERMS_LINK_HTML,
    LEGAL_PAGE_ARCH,
    LEGAL_PAGE_NAME,
    LEGAL_PAGE_URL,
    LEGAL_PAGE_VIEW_KEY,
    PRIVACY_PAGE_ARCH,
    PRIVACY_PAGE_NAME,
    PRIVACY_PAGE_URL,
    PRIVACY_PAGE_VIEW_KEY,
    TERMS_PAGE_ARCH,
    TERMS_PAGE_NAME,
    TERMS_PAGE_URL,
    TERMS_PAGE_VIEW_KEY,
)

_logger = logging.getLogger(__name__)

EPICERIE_CATEGORY_NAME = 'Épicerie créole'
EPICERIE_CATEGORY_DESCRIPTION = (
    '<p>Savons artisanaux, confitures, crackers et galettes de manioc — '
    'une sélection créole issue de nos producteurs et transformateurs.</p>'
)
# Enrichissements BO — description site (origine · usage · conservation) si vide.
PRODUCT_WEBSITE_DESCRIPTIONS = {
    'Confiture de goyave': (
        '<div class="ck-product-enrich">'
        '<h3 class="h5">Origine &amp; usage</h3>'
        '<p>Confiture artisanale créole — goyave sélectionnée par CK. '
        'Texture fondante, notes florales et légèrement acidulées.</p>'
        '<p><strong>Usage :</strong> tartines, yaourts, pâtisseries, accords fromages frais.</p>'
        '<h3 class="h5 mt-3">Ingrédients &amp; allergènes</h3>'
        '<p>Goyave, sucre, pectine, acidifiant (acide citrique). '
        'Peut contenir des traces de fruits à coque.</p>'
        '<h3 class="h5 mt-3">Conservation</h3>'
        '<p>Avant ouverture : conserver au sec, à l’abri de la lumière. '
        'Après ouverture : réfrigérer et consommer sous 3 semaines.</p>'
        '</div>'
    ),
    'Galettes de manioc': (
        '<div class="ck-product-enrich">'
        '<h3 class="h5">Origine &amp; usage</h3>'
        '<p>Galettes de manioc croustillantes — snack salé créole, sélection CK.</p>'
        '<p><strong>Usage :</strong> apéritif, accompagnement, casse-croûte.</p>'
        '<h3 class="h5 mt-3">Conservation</h3>'
        '<p>Conserver au sec. Refermer après ouverture.</p>'
        '</div>'
    ),
    'Manio Crackers': (
        '<div class="ck-product-enrich">'
        '<h3 class="h5">Origine &amp; usage</h3>'
        '<p>Crackers artisanaux Manio — recette créole, texture légère.</p>'
        '<p><strong>Usage :</strong> apéritif, dip, snack.</p>'
        '<h3 class="h5 mt-3">Conservation</h3>'
        '<p>Au sec, à l’abri de l’humidité.</p>'
        '</div>'
    ),
    'Savon vétiver': (
        '<div class="ck-product-enrich">'
        '<h3 class="h5">Origine &amp; usage</h3>'
        '<p>Savon artisanal au vétiver — bien-être créole, parfum végétal.</p>'
        '<p><strong>Usage :</strong> toilette quotidienne, cadeau.</p>'
        '<h3 class="h5 mt-3">Conservation</h3>'
        '<p>Conserver au sec entre deux utilisations.</p>'
        '</div>'
    ),
}

PRODUCT_ECOMMERCE_LEADS = {
    'Confiture de goyave': 'Confiture artisanale — sélection épicerie créole CK.',
    'Galettes de manioc': 'Galettes croustillantes — univers apéritif CK.',
    'Manio Crackers': 'Crackers artisanaux — snack créole CK.',
    'Savon vétiver': 'Savon au vétiver — univers bien-être CK.',
}


def _description_for_product(product):
    for key, html in PRODUCT_WEBSITE_DESCRIPTIONS.items():
        if key in (product.name or ''):
            return html
    return None


def _lead_for_product(product):
    for key, text in PRODUCT_ECOMMERCE_LEADS.items():
        if key in (product.name or ''):
            return text
    return None


def bootstrap_published_products(env):
    """Renseigne description site / e-commerce si champs BO vides."""
    updated = 0
    for product in env['product.template'].search([('is_published', '=', True)]):
        vals = {}
        if not (product.website_description or '').strip():
            html = _description_for_product(product)
            if html:
                vals['website_description'] = html
        if 'description_ecommerce' in product._fields and not (product.description_ecommerce or '').strip():
            lead = _lead_for_product(product)
            if lead:
                vals['description_ecommerce'] = f'<p>{lead}</p>'
        if vals:
            product.write(vals)
            updated += 1
    return updated


def bootstrap_epicerie_category(env):
    """Active titre + description catégorie principale si elle existe déjà en BO."""
    cat = env['product.public.category'].search([('name', '=', EPICERIE_CATEGORY_NAME)], limit=1)
    if not cat:
        return False
    vals = {
        'show_category_title': True,
        'show_category_description': True,
    }
    if not (cat.website_description or '').strip():
        vals['website_description'] = EPICERIE_CATEGORY_DESCRIPTION
    cat.write(vals)
    return True


PROFESSIONNELS_PAGE_URL = '/professionnels'
PROFESSIONNELS_VIEW_KEY = 'dorevia_ck_marketone_content.professionnels_page'
LEGACY_PROFESSIONNELS_VIEW_KEY = 'dorevia_ck_theme.professionnels_page'

PROFESSIONNELS_PAGE_ARCH = """
<div id="wrap" class="oe_structure ck-pro-page">
<section class="s_title pt64 pb16 o_colored_level" data-snippet="s_title" data-name="Titre">
    <div class="container s_allow_columns">
        <h1 class="display-5 fw-bold">Espace professionnel</h1>
        <p class="lead text-muted mb-0">Producteurs, fournisseurs, distributeurs et boutiques — qualifiez simplement votre demande avec CK.</p>
    </div>
</section>
<section class="s_text_block pt16 pb32 o_colored_level" data-snippet="s_text_block" data-name="Intro">
    <div class="container s_allow_columns">
        <p>CK met en relation producteurs et transformateurs créoles, distributeurs et points de vente en Europe. Les prix affichés sur la boutique concernent le grand public ; les conditions professionnelles sont étudiées avec vous après qualification de votre demande.</p>
    </div>
</section>
<section class="s_features pt32 pb32 o_cc o_cc1 o_colored_level" data-snippet="s_features" data-name="Double cible">
    <div class="container">
        <div class="row g-4">
            <div class="col-lg-6">
                <div class="h-100 p-4 border rounded o_colored_level">
                    <h2 class="h4-fs mb-2">Producteurs &amp; transformateurs</h2>
                    <p class="text-muted mb-3">Vous produisez ou transformez en zone créolophone et souhaitez faire connaître votre offre via CK.</p>
                    <ul class="mb-3">
                        <li>Proposer une offre · être référencé comme <strong>fournisseur</strong></li>
                        <li>Épicerie · boissons · bien-être — traçabilité et régularité</li>
                    </ul>
                    <a href="#ck-pro-form" class="btn btn-fill-primary">Proposer vos produits</a>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="h-100 p-4 border rounded o_colored_level">
                    <h2 class="h4-fs mb-2">Boutiques, distributeurs &amp; CHR</h2>
                    <p class="text-muted mb-3">Vous revendez ou servez des produits créoles et cherchez un partenaire fiable pour votre clientèle.</p>
                    <ul class="mb-3">
                        <li>Boutiques · épiceries · restaurants · hôtels · <strong>distributeurs</strong></li>
                        <li>Référencer des produits créoles · demander un contact commercial</li>
                    </ul>
                    <a href="#ck-pro-form" class="btn btn-fill-secondary">Demander un contact pro</a>
                </div>
            </div>
        </div>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Note qualification">
    <div class="container s_allow_columns">
        <p class="mb-0"><strong>Objectif :</strong> qualifier une demande professionnelle — pas de commande B2B en ligne, pas de tarif automatique. Notre équipe vous recontacte après lecture de votre message.</p>
    </div>
</section>
<section id="ck-pro-form" class="s_website_form pt32 pb64 o_colored_level" data-vcss="001" data-snippet="s_website_form" data-name="Formulaire Pro">
    <div class="container">
        <h2 class="h3-fs mb-2">Qualifiez votre demande</h2>
        <p class="text-muted mb-4">Décrivez votre projet et laissez vos coordonnées. Qualification portée par le message — sans champ CRM custom.</p>
        <form action="/website/form/" method="post" enctype="multipart/form-data" class="o_mark_required" data-mark="*" data-model_name="crm.lead" data-success-mode="message" data-success-message="Merci — votre demande a bien été enregistrée. Notre équipe vous recontactera." data-pre-fill="true">
            <div class="s_website_form_rows row s_col_no_bgcolor g-3">
                <div class="mb-0 col-12 s_website_form_field s_website_form_dnone">
                    <input type="hidden" class="form-control s_website_form_input" name="name" value="Demande professionnelle CK"/>
                </div>
                <div class="mb-0 col-12 col-lg-6 s_website_form_field s_website_form_custom s_website_form_required" data-type="char" data-name="Field">
                    <label class="s_website_form_label" for="ck_pro_partner"><span class="s_website_form_label_content">Société / structure</span><span class="s_website_form_mark" aria-hidden="true"> *</span><span class="visually-hidden"> (obligatoire)</span></label>
                    <input id="ck_pro_partner" type="text" class="form-control s_website_form_input" name="partner_name" required="" placeholder="Nom de votre structure"/>
                </div>
                <div class="mb-0 col-12 col-lg-6 s_website_form_field s_website_form_custom s_website_form_required" data-type="char" data-name="Field">
                    <label class="s_website_form_label" for="ck_pro_contact"><span class="s_website_form_label_content">Nom du contact</span><span class="s_website_form_mark" aria-hidden="true"> *</span><span class="visually-hidden"> (obligatoire)</span></label>
                    <input id="ck_pro_contact" type="text" class="form-control s_website_form_input" name="contact_name" required="" placeholder="Prénom Nom"/>
                </div>
                <div class="mb-0 col-12 col-lg-6 s_website_form_field s_website_form_required s_website_form_model_required" data-type="email" data-name="Field">
                    <label class="s_website_form_label" for="ck_pro_email"><span class="s_website_form_label_content">E-mail</span><span class="s_website_form_mark" aria-hidden="true"> *</span><span class="visually-hidden"> (obligatoire)</span></label>
                    <input id="ck_pro_email" type="email" class="form-control s_website_form_input" name="email_from" required="" placeholder="contact@entreprise.com"/>
                </div>
                <div class="mb-0 col-12 col-lg-6 s_website_form_field s_website_form_custom" data-type="char" data-name="Field">
                    <label class="s_website_form_label" for="ck_pro_phone"><span class="s_website_form_label_content">Téléphone</span></label>
                    <input id="ck_pro_phone" type="tel" class="form-control s_website_form_input" name="phone" placeholder="01 23 45 67 89"/>
                </div>
                <div class="mb-0 col-12 s_website_form_field s_website_form_required s_website_form_model_required" data-type="text" data-name="Field">
                    <label class="s_website_form_label" for="ck_pro_description"><span class="s_website_form_label_content">Nature de la demande professionnelle</span><span class="s_website_form_mark" aria-hidden="true"> *</span><span class="visually-hidden"> (obligatoire)</span></label>
                    <textarea id="ck_pro_description" class="form-control s_website_form_input" name="description" required="" rows="5" placeholder="Ex. : producteur · fournisseur · distributeur · boutique / CHR — décrivez votre projet et votre zone d'activité."></textarea>
                </div>
                <div class="mb-0 col-12 s_website_form_submit" data-name="Submit Button">
                    <div style="width: 200px;" class="s_website_form_label"/>
                    <button type="button" class="btn btn-primary s_website_form_send">Envoyer la demande</button>
                </div>
            </div>
        </form>
    </div>
</section>
<section class="s_text_block pt0 pb32 o_colored_level" data-snippet="s_text_block" data-name="Réassurance Pro">
    <div class="container s_allow_columns">
        <p class="mb-0"><strong>Données :</strong> vos coordonnées servent uniquement à traiter votre demande professionnelle — <a href="/privacy">en savoir plus sur la gestion de vos données</a>.</p>
    </div>
</section>
""".strip()


NEWSLETTER_MAILING_LIST_NAME = 'Newsletter CK'
NEWSLETTER_TITLE = 'Recevez les nouveautés créoles'
NEWSLETTER_LEAD = (
    "Produits, recettes, producteurs, idées d'usage et sélections CK."
)
NEWSLETTER_RGPD_NOTE = (
    'En vous inscrivant, vous acceptez de recevoir nos sélections créoles par e-mail. '
    'Désinscription possible à tout moment depuis chaque message — '
    '<a href="/privacy">politique de confidentialité</a>.'
)
PRO_DUAL_TITLE = 'Vous êtes professionnel ?'
PRO_DUAL_LEAD = (
    'Épicerie, boutique créole, restaurant, hôtel, traiteur, distributeur… '
    'CK étudie votre demande et vous oriente vers une sélection adaptée.'
)
PRO_DUAL_CTA_DEFAULT = 'Faire une demande professionnelle'


def bootstrap_newsletter_mailing_list(env):
    """Mailing list BO réelle pour inscription newsletter (Phase 9 · M9)."""
    MailingList = env['mailing.list'].sudo()
    mailing_list = MailingList.search(
        [('name', '=', NEWSLETTER_MAILING_LIST_NAME)],
        limit=1,
    )
    if not mailing_list:
        mailing_list = MailingList.create({'name': NEWSLETTER_MAILING_LIST_NAME})
    return mailing_list


def _localize_newsletter_form_html(form_html):
    """Libellés FR pour le snippet natif mass_mailing (polish home CK)."""
    if not form_html:
        return form_html
    for placeholder in ('Email Address', 'Your Email', 'Email'):
        form_html = form_html.replace(
            f'placeholder="{placeholder}"',
            'placeholder="Votre adresse e-mail"',
        )
    form_html = re.sub(
        r'>\s*Email Address\s*<',
        '>Votre adresse e-mail<',
        form_html,
        flags=re.I,
    )
    form_html = re.sub(
        r'>\s*Subscribe\s*</',
        ">S'inscrire</",
        form_html,
        flags=re.I,
    )
    form_html = form_html.replace('value="Subscribe"', "value=\"S'inscrire\"")
    return form_html


def render_newsletter_subscribe_form(env):
    """Snippet natif website_mass_mailing · list_id BO."""
    mailing_list = bootstrap_newsletter_mailing_list(env)
    form_html = str(
        env['ir.qweb']._render('website_mass_mailing.s_newsletter_subscribe_form', {})
    )
    form_html = re.sub(
        r'data-list-id="\d+"',
        f'data-list-id="{mailing_list.id}"',
        form_html,
        count=1,
    )
    return _localize_newsletter_form_html(form_html)


def build_dual_engage_compact_arch(env, *, pro_cta_href, pro_cta_label=None):
    """Bloc dual Pro + newsletter compact (Phase 9 · M9)."""
    newsletter_form = render_newsletter_subscribe_form(env)
    pro_cta_label = pro_cta_label or PRO_DUAL_CTA_DEFAULT
    return f"""
<section class="s_text_block ck-dual-engage ck-dual-engage--compact pt48 pb48 o_colored_level" data-snippet="s_text_block" data-name="CK Dual Pro Newsletter compact">
    <div class="container">
        <div class="row g-4 align-items-stretch">
            <div class="col-lg-6 o_colored_level">
                <div class="ck-dual-engage__pro p-4 p-lg-5 h-100 rounded o_cc o_cc1">
                    <h2 class="h4 mb-3">{PRO_DUAL_TITLE}</h2>
                    <p class="mb-4">{PRO_DUAL_LEAD}</p>
                    <a href="{pro_cta_href}" class="btn btn-primary">{pro_cta_label}</a>
                </div>
            </div>
            <div class="col-lg-6 o_colored_level">
                <div class="ck-dual-engage__newsletter p-4 p-lg-5 h-100 rounded o_cc o_cc2" id="ck-newsletter-subscribe">
                    <h2 class="h4 mb-3">{NEWSLETTER_TITLE}</h2>
                    <p class="mb-3">{NEWSLETTER_LEAD}</p>
                    {newsletter_form}
                    <p class="small text-muted mt-2 mb-0">{NEWSLETTER_RGPD_NOTE}</p>
                </div>
            </div>
        </div>
    </div>
</section>
""".strip()


def build_contactus_page_arch(env):
    """Page contact Phase 6 + dual newsletter compact (Phase 9)."""
    dual = build_dual_engage_compact_arch(
        env,
        pro_cta_href='/professionnels',
        pro_cta_label='Espace professionnel',
    )
    return f'{CONTACTUS_PAGE_ARCH}\n{dual}\n</div>'


def build_professionnels_page_arch(env):
    """Page Pro Phase 5 + dual newsletter compact (Phase 9)."""
    dual = build_dual_engage_compact_arch(
        env,
        pro_cta_href='#ck-pro-form',
        pro_cta_label='Qualifier ma demande',
    )
    return f'{PROFESSIONNELS_PAGE_ARCH}\n{dual}\n</div>'


CONTACTUS_PAGE_URL = '/contactus'
CONTACTUS_VIEW_KEY = 'dorevia_ck_marketone_content.contactus_page'
LEGACY_CONTACTUS_VIEW_KEY = 'dorevia_ck_theme.contactus_page'

CONTACTUS_PAGE_ARCH = """
<div id="wrap" class="oe_structure ck-contact-page">
<section class="s_title pt64 pb16 o_colored_level" data-snippet="s_title" data-name="Titre contact">
    <div class="container s_allow_columns">
        <h1 class="display-5 fw-bold">Nous contacter</h1>
        <p class="lead text-muted mb-0">Question produit, demande générale ou suivi boutique — ce formulaire est réservé aux particuliers. Les demandes professionnelles passent par l’espace Pro dédié.</p>
    </div>
</section>
<section class="s_features pt32 pb16 o_cc o_cc1 o_colored_level" data-snippet="s_features" data-name="Parcours contact">
    <div class="container">
        <div class="row g-4">
            <div class="col-md-4">
                <div class="h-100 p-4 border rounded o_colored_level">
                    <h2 class="h5-fs mb-2">Question produit</h2>
                    <p class="text-muted mb-3">Origine, usage, conservation ou disponibilité sur le catalogue B2C.</p>
                    <a href="#ck-contact-form" class="btn btn-link px-0">Poser une question →</a>
                </div>
            </div>
            <div class="col-md-4">
                <div class="h-100 p-4 border rounded o_colored_level">
                    <h2 class="h5-fs mb-2">Contact général</h2>
                    <p class="text-muted mb-3">Service client, suivi de commande ou information boutique.</p>
                    <a href="#ck-contact-form" class="btn btn-link px-0">Écrire à CK →</a>
                </div>
            </div>
            <div class="col-md-4">
                <div class="h-100 p-4 border rounded o_colored_level">
                    <h2 class="h5-fs mb-2">Partenaire / commercial</h2>
                    <p class="text-muted mb-3">Producteur, distributeur ou volume pro — qualification via l’espace Pro, pas ce formulaire.</p>
                    <a href="/professionnels" class="btn btn-fill-secondary">Espace professionnel →</a>
                </div>
            </div>
        </div>
    </div>
</section>
<section id="ck-contact-form" class="s_website_form pt32 pb32 o_colored_level" data-vcss="001" data-snippet="s_website_form" data-name="Formulaire contact B2C">
    <div class="container">
        <h2 class="h3-fs mb-2">Formulaire de contact</h2>
        <p class="text-muted mb-4">Réservé aux demandes particulières. Nous lisons chaque message et revenons vers vous dans un délai raisonnable.</p>
        <form id="contactus_form" action="/website/form/" method="post" enctype="multipart/form-data" class="o_mark_required" data-mark="*" data-model_name="mail.mail" data-success-mode="redirect" data-success-page="/contactus-thank-you" data-pre-fill="true">
            <div class="s_website_form_rows row s_col_no_bgcolor g-3">
                <div class="mb-0 col-12 col-lg-6 s_website_form_field s_website_form_custom s_website_form_required" data-type="char" data-name="Field">
                    <label class="s_website_form_label" for="ck_contact_name"><span class="s_website_form_label_content">Nom</span><span class="s_website_form_mark" aria-hidden="true"> *</span><span class="visually-hidden"> (obligatoire)</span></label>
                    <input id="ck_contact_name" type="text" class="form-control s_website_form_input" name="name" required="" data-fill-with="name"/>
                </div>
                <div class="mb-0 col-12 col-lg-6 s_website_form_field s_website_form_custom" data-type="char" data-name="Field">
                    <label class="s_website_form_label" for="ck_contact_phone"><span class="s_website_form_label_content">Téléphone</span></label>
                    <input id="ck_contact_phone" type="tel" class="form-control s_website_form_input" name="phone" data-fill-with="phone"/>
                </div>
                <div class="mb-0 col-12 col-lg-6 s_website_form_field s_website_form_required s_website_form_model_required" data-type="email" data-name="Field">
                    <label class="s_website_form_label" for="ck_contact_email"><span class="s_website_form_label_content">E-mail</span><span class="s_website_form_mark" aria-hidden="true"> *</span><span class="visually-hidden"> (obligatoire)</span></label>
                    <input id="ck_contact_email" type="email" class="form-control s_website_form_input" name="email_from" required="" data-fill-with="email"/>
                </div>
                <div class="mb-0 col-12 col-lg-6 s_website_form_field s_website_form_custom" data-type="char" data-name="Field">
                    <label class="s_website_form_label" for="ck_contact_company"><span class="s_website_form_label_content">Société</span></label>
                    <input id="ck_contact_company" type="text" class="form-control s_website_form_input" name="company" data-fill-with="commercial_company_name"/>
                </div>
                <div class="mb-0 col-12 s_website_form_field s_website_form_required s_website_form_model_required" data-type="char" data-name="Field">
                    <label class="s_website_form_label" for="ck_contact_subject"><span class="s_website_form_label_content">Sujet</span><span class="s_website_form_mark" aria-hidden="true"> *</span><span class="visually-hidden"> (obligatoire)</span></label>
                    <input id="ck_contact_subject" type="text" class="form-control s_website_form_input" name="subject" required=""/>
                </div>
                <div class="mb-0 col-12 s_website_form_field s_website_form_custom s_website_form_required" data-type="text" data-name="Field">
                    <label class="s_website_form_label" for="ck_contact_message"><span class="s_website_form_label_content">Message</span><span class="s_website_form_mark" aria-hidden="true"> *</span><span class="visually-hidden"> (obligatoire)</span></label>
                    <textarea id="ck_contact_message" class="form-control s_website_form_input" name="description" required="" rows="6" placeholder="Décrivez votre question produit ou votre demande boutique."></textarea>
                </div>
                <div class="mb-0 col-12 s_website_form_field s_website_form_dnone">
                    <input type="hidden" class="form-control s_website_form_input" name="email_to"/>
                </div>
                <div class="mb-0 col-12 s_website_form_submit" data-name="Submit Button">
                    <button type="button" class="btn btn-primary s_website_form_send">Envoyer</button>
                </div>
            </div>
        </form>
    </div>
</section>
<section class="s_text_block pt16 pb64 o_colored_level" data-snippet="s_text_block" data-name="Réassurance contact">
    <div class="container s_allow_columns">
        <p class="mb-2"><strong>Données :</strong> votre message sert uniquement à répondre à votre demande — <a href="/privacy">en savoir plus sur la gestion de vos données</a>.</p>
        <p class="mb-0"><strong>Professionnels :</strong> producteurs, distributeurs et boutiques — <a href="/professionnels">qualifiez votre demande sur l’espace Pro</a>.</p>
    </div>
</section>
""".strip()

A_PROPOS_PAGE_URL = '/a-propos'
A_PROPOS_VIEW_KEY = 'dorevia_ck_marketone_content.a_propos_page'
LEGACY_A_PROPOS_VIEW_KEY = 'dorevia_ck_theme.a_propos_page'

A_PROPOS_PAGE_ARCH = """
<div id="wrap" class="oe_structure ck-about-page">
<section class="s_title pt64 pb16 o_colored_level" data-snippet="s_title" data-name="Hero à propos">
    <div class="container s_allow_columns">
        <h1 class="display-5 fw-bold">Comprendre, acheter et faire confiance aux produits créoles</h1>
        <p class="lead text-muted mb-0">CK est une boutique en ligne qui relie les territoires créolophones aux clients en France et en Europe — avec une sélection exigeante et une logistique lisible.</p>
    </div>
</section>
<section class="s_features pt32 pb32 o_cc o_cc1 o_colored_level" data-snippet="s_features" data-name="Mission CK">
    <div class="container">
        <div class="row g-4">
            <div class="col-md-6 col-lg-3">
                <div class="h-100 p-4 border rounded o_colored_level">
                    <h2 class="h5-fs mb-2">Notre mission</h2>
                    <p class="text-muted mb-0">Rendre l’achat de produits créoles simple et compréhensible — origine, usage et transformation visibles pour chaque référence.</p>
                </div>
            </div>
            <div class="col-md-6 col-lg-3">
                <div class="h-100 p-4 border rounded o_colored_level">
                    <h2 class="h5-fs mb-2">Notre sélection</h2>
                    <p class="text-muted mb-0">Épicerie, condiments et bien-être cohérents avec l’univers CK — traçabilité et régularité de qualité.</p>
                </div>
            </div>
            <div class="col-md-6 col-lg-3">
                <div class="h-100 p-4 border rounded o_colored_level">
                    <h2 class="h5-fs mb-2">Confiance</h2>
                    <p class="text-muted mb-0">Relations durables avec des transformateurs créoles — valorisation du travail local, sans promesse marketplace ouverte.</p>
                </div>
            </div>
            <div class="col-md-6 col-lg-3">
                <div class="h-100 p-4 border rounded o_colored_level">
                    <h2 class="h5-fs mb-2">Logistique</h2>
                    <p class="text-muted mb-0">Expédition vers la France et l’Europe, délais annoncés avant paiement. Les conditions pro sont étudiées au cas par cas.</p>
                </div>
            </div>
        </div>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Engagements">
    <div class="container s_allow_columns">
        <ul class="mb-0">
            <li><strong>Pont créole / Europe</strong> — des territoires créolophones vers les clients européens.</li>
            <li><strong>Origines lisibles</strong> — Réunion, Antilles et territoires partenaires sur les fiches produits.</li>
            <li><strong>Relation directe</strong> — service client joignable · qualification Pro distincte · pas de portail opaque.</li>
        </ul>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Signal Pro">
    <div class="container s_allow_columns">
        <p class="mb-0">Vous êtes producteur, transformateur ou distributeur ? <a href="/professionnels">Qualifiez votre demande sur l’espace professionnel</a>.</p>
    </div>
</section>
<section class="s_text_block pt16 pb64 o_colored_level" data-snippet="s_text_block" data-name="Liens CK">
    <div class="container s_allow_columns">
        <p class="mb-0">Découvrir CK : <a href="/shop">Boutique</a> · <a href="/professionnels">Professionnels</a> · <a href="/contactus">Contact</a></p>
    </div>
</section>
</div>
""".strip()


def _wrap_website_page_arch(view_key, page_name, inner_arch):
    """Enveloppe le contenu CMS dans website.layout (page HTML complète + assets)."""
    inner = inner_arch.strip()
    if 't-call="website.layout"' in inner or "t-call='website.layout'" in inner:
        return inner
    return f"""<t name="{escape(page_name)}" t-name="{view_key}">
    <t t-call="website.layout">
{inner}
    </t>
</t>"""


def _resolve_cms_view(View, view_key, legacy_view_key=None):
    """Vue CMS par clé module contenu, avec reprise clé historique thème."""
    view = View.search([('key', '=', view_key)], limit=1)
    if view:
        return view
    if legacy_view_key:
        legacy = View.search([('key', '=', legacy_view_key)], limit=1)
        if legacy:
            legacy.write({'key': view_key})
            return legacy
    return View.browse()


def _bootstrap_cms_page(env, *, page_url, view_key, view_name, page_name, arch, legacy_view_key=None):
    """Crée ou met à jour une page CMS website (idempotent)."""
    website = env['website'].search([], limit=1)
    if not website:
        return False

    View = env['ir.ui.view'].sudo()
    Page = env['website.page'].sudo()
    arch = _wrap_website_page_arch(view_key, page_name, arch)

    page = Page.search([
        ('url', '=', page_url),
        ('website_id', '=', website.id),
    ], limit=1)

    # QA H3 : guard anti-écrasement — empreinte du dernier seed module. Si l'arch
    # courante diverge (édition MOA en BO), on ne réécrit pas la page.
    param = env['ir.config_parameter'].sudo()
    seed_key = f'ck_seed_arch.{view_key}'

    view = _resolve_cms_view(View, view_key, legacy_view_key)
    if not view:
        view = View.create({
            'name': view_name,
            'type': 'qweb',
            'key': view_key,
            'arch': arch,
            'website_id': website.id,
        })
        param.set_param(seed_key, _arch_fingerprint(view.arch_db or view.arch or ''))
    else:
        seeded_fp = param.get_param(seed_key)
        current_fp = _arch_fingerprint(view.arch_db or view.arch or '')
        if seeded_fp and current_fp != seeded_fp:
            _logger.info('CK CMS %s édité en BO — seed non écrasé', view_key)
        else:
            view.write({'arch': arch})
            # Empreinte de la forme NORMALISÉE relue après écriture (évite un faux
            # « édité » dû à la reformulation QWeb au write).
            param.set_param(seed_key, _arch_fingerprint(view.arch_db or view.arch or ''))

    page_vals = {
        'name': page_name,
        'url': page_url,
        'website_id': website.id,
        'view_id': view.id,
        'is_published': True,
        'website_indexed': True,
    }
    if page:
        page.write(page_vals)
    else:
        Page.create(page_vals)
    return True


def bootstrap_contactus_page(env):
    """Consolide /contactus — formulaire B2C + dual newsletter M9 (Phase 6 + 9)."""
    return _bootstrap_cms_page(
        env,
        page_url=CONTACTUS_PAGE_URL,
        view_key=CONTACTUS_VIEW_KEY,
        view_name='Contact CK Phase 9',
        page_name='Contact',
        arch=build_contactus_page_arch(env),
        legacy_view_key=LEGACY_CONTACTUS_VIEW_KEY,
    )


def bootstrap_a_propos_page(env):
    """Crée ou met à jour la page CMS /a-propos (Phase 6 · idempotent)."""
    return _bootstrap_cms_page(
        env,
        page_url=A_PROPOS_PAGE_URL,
        view_key=A_PROPOS_VIEW_KEY,
        view_name='À propos CK Phase 6',
        page_name='À propos',
        arch=A_PROPOS_PAGE_ARCH,
        legacy_view_key=LEGACY_A_PROPOS_VIEW_KEY,
    )


def bootstrap_mentions_legales_page(env):
    """Crée ou met à jour la page CMS /legal (lot go-live public · idempotent)."""
    return _bootstrap_cms_page(
        env,
        page_url=LEGAL_PAGE_URL,
        view_key=LEGAL_PAGE_VIEW_KEY,
        view_name='Mentions légales CK',
        page_name=LEGAL_PAGE_NAME,
        arch=LEGAL_PAGE_ARCH,
    )


def bootstrap_privacy_page(env):
    """Crée ou met à jour la page CMS /privacy (RGPD · idempotent)."""
    return _bootstrap_cms_page(
        env,
        page_url=PRIVACY_PAGE_URL,
        view_key=PRIVACY_PAGE_VIEW_KEY,
        view_name='Confidentialité CK',
        page_name=PRIVACY_PAGE_NAME,
        arch=PRIVACY_PAGE_ARCH,
    )


def bootstrap_terms_page(env):
    """Crée ou met à jour la page CMS /terms (CGV · idempotent)."""
    return _bootstrap_cms_page(
        env,
        page_url=TERMS_PAGE_URL,
        view_key=TERMS_PAGE_VIEW_KEY,
        view_name='CGV CK',
        page_name=TERMS_PAGE_NAME,
        arch=TERMS_PAGE_ARCH,
    )


def _insert_footer_link_after(arch, marker, link_html):
    """Insère link_html après marker si link_html href absent."""
    href_match = link_html.split('href="', 1)[1].split('"', 1)[0] if 'href="' in link_html else ''
    if href_match and href_match in arch:
        return arch
    if marker in arch:
        return arch.replace(marker, marker + '\n                                ' + link_html, 1)
    return arch


def _href_of(link_html):
    return link_html.split('href="', 1)[1].split('"', 1)[0] if 'href="' in link_html else ''


def _insert_footer_legal_block_fallback(arch, links_html):
    """QA M2 : repli — insère un bloc <ul> de liens légaux avant la fermeture du footer
    quand le marqueur Contact est absent (évite l'échec silencieux)."""
    items = '\n                                '.join(links_html)
    block = (
        '\n                            <ul class="list-unstyled ck-footer-legal-fallback">\n'
        f'                                {items}\n'
        '                            </ul>'
    )
    for anchor in ('</footer>', '</div></div>', '</div>'):
        idx = arch.rfind(anchor)
        if idx >= 0:
            return arch[:idx] + block + arch[idx:], True
    return arch, False


def bootstrap_footer_legal_links(env):
    """Liens footer Mentions légales · Confidentialité · CGV (idempotent)."""
    website = env['website'].search([], limit=1)
    if not website:
        _logger.warning('CK footer : aucun website — liens légaux non ajoutés')
        return False

    View = env['ir.ui.view'].sudo()
    footer = View.search([
        ('key', '=', 'website.footer_custom'),
        ('website_id', '=', website.id),
    ], limit=1)
    if not footer:
        footer = View.search([('key', '=', 'website.footer_custom')], limit=1)
    if not footer:
        _logger.warning(
            'CK footer : vue website.footer_custom introuvable — liens légaux non ajoutés'
        )
        return False

    arch = footer.arch_db or footer.arch or ''
    if isinstance(arch, dict):
        arch = next(iter(arch.values()), '')

    original = arch
    arch = _insert_footer_link_after(arch, FOOTER_CONTACT_LINK_MARKER, FOOTER_LEGAL_LINK_HTML)
    arch = _insert_footer_link_after(arch, FOOTER_LEGAL_LINK_HTML, FOOTER_PRIVACY_LINK_HTML)
    if FOOTER_LEGAL_LINK_HTML not in arch and 'href="/legal"' not in arch:
        arch = _insert_footer_link_after(arch, FOOTER_CONTACT_LINK_MARKER, FOOTER_PRIVACY_LINK_HTML)
    arch = _insert_footer_link_after(arch, FOOTER_PRIVACY_LINK_HTML, FOOTER_TERMS_LINK_HTML)
    if 'href="/terms' not in arch:
        if FOOTER_PRIVACY_LINK_HTML in arch:
            arch = _insert_footer_link_after(arch, FOOTER_PRIVACY_LINK_HTML, FOOTER_TERMS_LINK_HTML)
        elif FOOTER_LEGAL_LINK_HTML in arch:
            arch = _insert_footer_link_after(arch, FOOTER_LEGAL_LINK_HTML, FOOTER_TERMS_LINK_HTML)
        else:
            arch = _insert_footer_link_after(arch, FOOTER_CONTACT_LINK_MARKER, FOOTER_TERMS_LINK_HTML)

    # QA M2 : si l'insertion ciblée a échoué (marqueur Contact absent), repli + log
    # explicite plutôt qu'un abandon silencieux (verrou go-live).
    missing = [
        html for html in (FOOTER_LEGAL_LINK_HTML, FOOTER_PRIVACY_LINK_HTML, FOOTER_TERMS_LINK_HTML)
        if _href_of(html) not in arch
    ]
    if missing:
        arch, inserted = _insert_footer_legal_block_fallback(arch, missing)
        if not inserted:
            _logger.warning(
                'CK footer : liens légaux non insérés (marqueur Contact et ancre footer '
                'introuvables) — vérifier la structure de website.footer_custom : %s',
                ', '.join(_href_of(h) for h in missing),
            )

    if arch == original:
        return True

    footer.write({'arch': arch})
    return True


def bootstrap_footer_legal_link(env):
    """Alias rétrocompat — délègue à bootstrap_footer_legal_links."""
    return bootstrap_footer_legal_links(env)


def bootstrap_professionnels_page(env):
    """Crée ou met à jour la page CMS /professionnels (Phase 5 + dual M9 · idempotent)."""
    return _bootstrap_cms_page(
        env,
        page_url=PROFESSIONNELS_PAGE_URL,
        view_key=PROFESSIONNELS_VIEW_KEY,
        view_name='Professionnels CK Phase 9',
        page_name='Professionnels',
        arch=build_professionnels_page_arch(env),
        legacy_view_key=LEGACY_PROFESSIONNELS_VIEW_KEY,
    )


PRODUCER_PAGE_URL = '/producteur/atelier-hauts-goyaviers'
PRODUCER_VIEW_KEY = 'dorevia_ck_marketone_content.producer_page'
LEGACY_PRODUCER_VIEW_KEY = 'dorevia_ck_theme.producer_page'
PRODUCER_PAGE_NAME = 'Atelier Les Hauts Goyaviers'

PRODUCER_PAGE_ARCH_HEAD = """
<div id="wrap" class="oe_structure ck-producer-page">
<section class="s_title pt64 pb16 o_colored_level" data-snippet="s_title" data-name="Hero producteur">
    <div class="container s_allow_columns">
        <p class="text-muted mb-2"><span class="badge text-bg-secondary me-2">La Réunion</span><span class="badge text-bg-light border">Agro-transformation</span></p>
        <h1 class="display-5 fw-bold">Atelier Les Hauts Goyaviers</h1>
        <p class="lead text-muted mb-4">Trois générations de transformateurs — goyaviers de pleine terre, confitures artisanales et circuit court entre verger et atelier.</p>
        <p class="mb-0"><a href="#ck-producer-products" class="btn btn-primary me-2">Voir les produits</a><a href="/professionnels" class="btn btn-secondary">Demande professionnelle</a></p>
    </div>
</section>
<section class="s_text_block pt32 pb16 o_colored_level" data-snippet="s_text_block" data-name="Présentation">
    <div class="container s_allow_columns">
        <h2 class="h3-fs mb-3">Qui est ce producteur ?</h2>
        <p>Fondé à Saint-Pierre, au sud de La Réunion, l’Atelier Les Hauts Goyaviers est une structure familiale d’agriculteurs-transformateurs. Depuis trois générations, la famille cultive des goyaviers en pleine terre et transforme les récoltes dans un atelier attenant aux vergers.</p>
        <p><strong>Savoir-faire :</strong> confitures artisanales, cuisson lente, fruits triés à la main, traçabilité lot par lot.<br/>
        <strong>Lien territoire :</strong> microclimat du sud réunionnais, goyavier de pleine terre, circuit court verger → atelier.</p>
        <p class="mb-0">CK met en avant ce partenaire pour une origine lisible, une qualité constante et une histoire compréhensible avant l’achat — sans promesse marketplace ouverte.</p>
    </div>
</section>
<section class="s_features pt32 pb32 o_cc o_cc1 o_colored_level" data-snippet="s_features" data-name="Critères sélection CK">
    <div class="container">
        <h2 class="h3-fs mb-4">Pourquoi CK sélectionne ce producteur</h2>
        <div class="row g-4">
            <div class="col-md-6 col-lg-4">
                <div class="h-100 p-4 border rounded o_colored_level">
                    <h3 class="h5-fs mb-2">Qualité constante</h3>
                    <p class="text-muted mb-0">Texture, goût et régularité lot par lot avant mise en ligne.</p>
                </div>
            </div>
            <div class="col-md-6 col-lg-4">
                <div class="h-100 p-4 border rounded o_colored_level">
                    <h3 class="h5-fs mb-2">Origine traçable</h3>
                    <p class="text-muted mb-0">Réunion · vergers identifiés · transformation locale documentée.</p>
                </div>
            </div>
            <div class="col-md-6 col-lg-4">
                <div class="h-100 p-4 border rounded o_colored_level">
                    <h3 class="h5-fs mb-2">Cohérence CK</h3>
                    <p class="text-muted mb-0">Formats adaptés au marché européen · standards emballage et délais annoncés.</p>
                </div>
            </div>
        </div>
        <p class="text-muted small mt-3 mb-0">Critères en texte CMS — pas de scoring automatique.</p>
    </div>
</section>
""".strip()

PRODUCER_PAGE_ARCH_TAIL = """
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Signal logistique">
    <div class="container s_allow_columns">
        <p class="mb-0"><strong>Rôle CK :</strong> sélection, mise en ligne et expédition vers la France et l’Europe. Les conditions professionnelles sont étudiées au cas par cas — pas de tarif B2B automatique en ligne.</p>
    </div>
</section>
<section class="s_text_block pt16 pb64 o_colored_level" data-snippet="s_text_block" data-name="CTA sortie">
    <div class="container s_allow_columns">
        <p class="mb-0">Découvrir CK : <a href="/shop">Boutique</a> · <a href="/contactus">Contact</a> · <a href="/professionnels">Professionnels</a></p>
    </div>
</section>
</div>
""".strip()


def _producer_linked_products(env):
    """Produits publiés liés au pilote — URLs réelles uniquement (pas de tag BO V1)."""
    Product = env['product.template']
    domain = [('is_published', '=', True), ('sale_ok', '=', True)]
    products = Product.search(domain + [('name', 'ilike', 'goyav')], limit=4)
    if not products:
        products = Product.search(domain + [('name', 'ilike', 'confiture')], limit=4)
    if not products:
        products = Product.search(domain, limit=4)
    return products.filtered(lambda p: p.website_url)


def _producer_products_section_html(env):
    """Grille produits associés — liens BO réels ou renvoi boutique sobre."""
    products = _producer_linked_products(env)
    if not products:
        return """
<section id="ck-producer-products" class="s_text_block pt32 pb32 o_colored_level" data-snippet="s_text_block" data-name="Produits associés">
    <div class="container s_allow_columns">
        <h2 class="h3-fs mb-2">Produits disponibles via CK</h2>
        <p class="text-muted mb-3">Les références de l’atelier sont visibles dans la boutique — parcourez le catalogue pour découvrir les produits disponibles.</p>
        <a href="/shop" class="btn btn-primary">Voir la boutique</a>
    </div>
</section>
""".strip()

    cards = []
    for product in products:
        cards.append(
            f'<div class="col-md-6 col-lg-3">'
            f'<div class="h-100 p-3 border rounded o_colored_level">'
            f'<h3 class="h6-fs mb-2"><a href="{product.website_url}">{product.name}</a></h3>'
            f'<a href="{product.website_url}" class="btn btn-link px-0">Voir le produit →</a>'
            f'</div></div>'
        )
    grid = '\n'.join(cards)
    return f"""
<section id="ck-producer-products" class="s_features pt32 pb32 o_colored_level" data-snippet="s_features" data-name="Produits associés">
    <div class="container">
        <h2 class="h3-fs mb-2">Produits proposés via CK</h2>
        <p class="text-muted mb-4">Références disponibles en boutique — liens directs vers les fiches produits publiées.</p>
        <div class="row g-3 ck-producer-products__grid">
{grid}
        </div>
    </div>
</section>
""".strip()


def build_producer_page_arch(env):
    return '\n'.join([
        PRODUCER_PAGE_ARCH_HEAD,
        _producer_products_section_html(env),
        PRODUCER_PAGE_ARCH_TAIL,
    ])


def bootstrap_producer_page(env):
    """Crée ou met à jour la fiche producteur CMS pilote (Phase 7 · M1 · idempotent)."""
    return _bootstrap_cms_page(
        env,
        page_url=PRODUCER_PAGE_URL,
        view_key=PRODUCER_VIEW_KEY,
        view_name='Producteur CK Phase 7',
        page_name=PRODUCER_PAGE_NAME,
        arch=build_producer_page_arch(env),
        legacy_view_key=LEGACY_PRODUCER_VIEW_KEY,
    )


RECIPES_PAGE_URL = '/recettes'
RECIPES_VIEW_KEY = 'dorevia_ck_marketone_content.recipes_page'
LEGACY_RECIPES_VIEW_KEY = 'dorevia_ck_theme.recipes_page'
RECIPES_PAGE_NAME = 'Recettes & savoirs'

RECIPES_PAGE_ARCH_HEAD = """
<div id="wrap" class="oe_structure ck-recipes-page">
<section class="s_title pt64 pb16 o_colored_level" data-snippet="s_title" data-name="Hero recettes">
    <div class="container s_allow_columns">
        <p class="text-muted mb-2"><span class="badge text-bg-secondary me-2">Usages</span><span class="badge text-bg-light border">Cuisine créole</span></p>
        <h1 class="display-5 fw-bold">Recettes &amp; savoirs CK</h1>
        <p class="lead text-muted mb-0">Idées recettes, conseils d’usage et repères simples pour mieux profiter des produits créoles — contenu éditorial sobre, lié au catalogue CK.</p>
    </div>
</section>
<section id="ck-recipes-cards" class="s_features pt32 pb64 o_colored_level" data-snippet="s_features" data-name="Grille recettes">
    <div class="container">
        <div class="row g-4 ck-recipes-cards__grid">
""".strip()

RECIPES_PAGE_ARCH_TAIL = """
        </div>
    </div>
</section>
<section class="s_text_block pt16 pb64 o_colored_level" data-snippet="s_text_block" data-name="CTA sortie">
    <div class="container s_allow_columns">
        <p class="mb-0">Explorer CK : <a href="/shop">Boutique</a> · <a href="/a-propos">À propos</a> · <a href="/contactus">Contact</a></p>
    </div>
</section>
</div>
""".strip()


def _published_product_url(env, *name_fragments):
    """URL produit publié — premier match sur fragments de nom."""
    Product = env['product.template']
    domain = [('is_published', '=', True), ('sale_ok', '=', True)]
    for fragment in name_fragments:
        product = Product.search(domain + [('name', 'ilike', fragment)], limit=1)
        if product and product.website_url:
            return product.website_url, product.name
    product = Product.search(domain, limit=1)
    if product and product.website_url:
        return product.website_url, product.name
    return '/shop', 'Voir en boutique'


def _recipe_card_html(*, badge, category, title, body, href, link_label):
    return f"""
            <div class="col-md-6 col-lg-4">
                <div class="h-100 p-4 border rounded o_colored_level">
                    <p class="text-muted small mb-2"><span class="badge text-bg-light border me-1">{badge}</span><span class="badge text-bg-secondary">{category}</span></p>
                    <h2 class="h5-fs mb-2">{title}</h2>
                    <p class="text-muted mb-3">{body}</p>
                    <a href="{href}" class="btn btn-link px-0">{link_label} →</a>
                </div>
            </div>""".strip()


def build_recipes_page_arch(env):
    product_url, product_name = _published_product_url(env, 'goyav', 'confiture')
    cards = [
        _recipe_card_html(
            badge='Recette',
            category='Épicerie',
            title='Clafoutis créole au goyavier',
            body='Utilisez la confiture goyave CK en base de clafoutis — une idée dessert simple, liée à un produit du catalogue.',
            href=product_url,
            link_label=f'Voir {product_name}' if product_url != '/shop' else 'Voir en boutique',
        ),
        _recipe_card_html(
            badge='Guide',
            category='Épicerie',
            title='Bien choisir en boutique',
            body='Parcourez les références épicerie créole — condiments, confitures et snacks pour débuter la cuisine créole.',
            href='/shop',
            link_label='Voir la boutique',
        ),
        _recipe_card_html(
            badge='Conseil',
            category='Manioc',
            title='Galettes et snacks manioc',
            body='Accompagnement, apéritif ou casse-croûte — comprendre les usages des galettes et crackers du catalogue.',
            href='/shop',
            link_label='Voir en boutique',
        ),
        _recipe_card_html(
            badge='Guide achat',
            category='Découverte',
            title='Première commande CK',
            body='Commencez par une confiture, un snack ou un produit bien-être — nos repères pour une première commande réussie.',
            href='/shop',
            link_label='Coffrets en boutique',
        ),
        _recipe_card_html(
            badge='Usage',
            category='Bien-être',
            title='Savons et routine quotidienne',
            body='Savon artisanal au vétiver — usage toilette quotidienne ou idée cadeau depuis le catalogue CK.',
            href='/shop',
            link_label='Univers bien-être',
        ),
        _recipe_card_html(
            badge='Savoir',
            category='Sélection CK',
            title='Comprendre la sélection CK',
            body='Pourquoi nous choisissons certains producteurs — traçabilité, qualité et circuit court entre territoire et catalogue.',
            href='/producteur/atelier-hauts-goyaviers',
            link_label='Fiche producteur pilote',
        ),
    ]
    return '\n'.join([RECIPES_PAGE_ARCH_HEAD, '\n'.join(cards), RECIPES_PAGE_ARCH_TAIL])


def bootstrap_recipes_page(env):
    """Crée ou met à jour la page CMS /recettes (Phase 8 · M2 · idempotent)."""
    return _bootstrap_cms_page(
        env,
        page_url=RECIPES_PAGE_URL,
        view_key=RECIPES_VIEW_KEY,
        view_name='Recettes CK Phase 8',
        page_name=RECIPES_PAGE_NAME,
        arch=build_recipes_page_arch(env),
        legacy_view_key=LEGACY_RECIPES_VIEW_KEY,
    )


def bootstrap_all_marketone_content(env):
    """Ensemble des bootstraps contenu CK (post_init · migrations)."""
    bootstrap_newsletter_mailing_list(env)
    bootstrap_epicerie_category(env)
    bootstrap_published_products(env)
    bootstrap_catalog_vedettes_products(env)
    from .home_hero import bootstrap_home_hero

    bootstrap_home_hero(env)
    bootstrap_home_featured_products(env)
    from .home_univers import bootstrap_home_univers

    bootstrap_home_univers(env)
    bootstrap_home_discovery_pack(env)
    from .home_dual_engage import bootstrap_home_dual_engage
    from .home_editorial import bootstrap_home_editorial

    bootstrap_home_dual_engage(env)
    bootstrap_home_editorial(env)
    bootstrap_professionnels_page(env)
    bootstrap_contactus_page(env)
    bootstrap_a_propos_page(env)
    bootstrap_producer_page(env)
    bootstrap_recipes_page(env)
    bootstrap_mentions_legales_page(env)
    bootstrap_privacy_page(env)
    bootstrap_terms_page(env)
    bootstrap_footer_legal_links(env)


def post_init_hook(env):
    bootstrap_all_marketone_content(env)
