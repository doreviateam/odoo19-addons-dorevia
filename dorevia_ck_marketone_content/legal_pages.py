# -*- coding: utf-8 -*-
"""Contenus CMS pages légales CK — recette interne V1 (MOA 2026-06-14).

Données fictives explicitement marquées — non publiable en l'état.
"""

LEGAL_PAGE_URL = '/legal'
LEGAL_PAGE_VIEW_KEY = 'dorevia_ck_marketone_content.legal_page'
LEGAL_PAGE_NAME = 'Mentions légales'

PRIVACY_PAGE_URL = '/privacy'
PRIVACY_PAGE_VIEW_KEY = 'dorevia_ck_marketone_content.privacy_page'
PRIVACY_PAGE_NAME = 'Politique de confidentialité'

TERMS_PAGE_URL = '/terms'
TERMS_PAGE_VIEW_KEY = 'dorevia_ck_marketone_content.terms_page'
TERMS_PAGE_NAME = 'Conditions générales de vente'

RECETTE_BANNER_HTML = """
<section class="s_text_block pt16 pb0 o_cc o_cc2 o_colored_level ck-legal-recette-banner" data-snippet="s_text_block" data-name="Bandeau recette interne">
    <div class="container s_allow_columns">
        <p class="alert alert-warning mb-0 py-2 px-3"><strong>Version recette interne</strong> — certaines coordonnées légales sont fictives ou provisoires. Non publiable en l'état.</p>
    </div>
</section>
""".strip()

LEGAL_PAGE_ARCH = f"""
<div id="wrap" class="oe_structure ck-legal-page">
{RECETTE_BANNER_HTML}
<section class="s_title pt64 pb16 o_colored_level" data-snippet="s_title" data-name="Titre mentions légales">
    <div class="container s_allow_columns">
        <h1 class="display-5 fw-bold">Mentions légales</h1>
        <p class="lead text-muted mb-0">Informations légales relatives à la boutique en ligne <strong>C-Kreyol</strong>, éditée par <strong>Marketone SAS</strong>.</p>
    </div>
</section>
<section class="s_text_block pt32 pb16 o_colored_level" data-snippet="s_text_block" data-name="Éditeur">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Éditeur du site</h2>
        <p>Le site <strong>C-Kreyol</strong> est édité par&#160;:</p>
        <p><strong>Marketone SAS</strong>, société par actions simplifiée (SAS), au capital de <strong>10&#160;000&#160;€</strong> <em>[DONNÉE FICTIVE — À REMPLACER AVANT GO-LIVE PUBLIC]</em>, dont le siège social est situé <strong>12 rue Example, 44000 Nantes, France</strong> <em>[DONNÉE FICTIVE — À REMPLACER AVANT GO-LIVE PUBLIC]</em>.</p>
        <p>Immatriculée au <strong>RCS Nantes 123&#160;456&#160;789</strong> <em>[DONNÉE FICTIVE]</em> — <strong>SIREN 123&#160;456&#160;789</strong> <em>[SIREN FICTIF — NON PUBLIABLE]</em>.</p>
        <p>Numéro de TVA intracommunautaire&#160;: <strong>FR&#160;12&#160;123456789</strong> <em>[TVA FICTIVE — NON PUBLIABLE]</em>.</p>
        <p><strong>Directeur de la publication</strong>&#160;: Doreviateam.</p>
        <p><strong>Contact</strong>&#160;: <a href="mailto:contact.ck@marketone.com">contact.ck@marketone.com</a> — <a href="/contactus">formulaire de contact</a>.</p>
        <p>Téléphone&#160;: <strong>+33 (0)2 40 00 00 00</strong> <em>[TÉLÉPHONE FICTIF — NON PUBLIABLE]</em>.</p>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Hébergement">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Hébergement</h2>
        <p>Conformément aux obligations légales, le prestataire d'hébergement assurant le stockage du site est&#160;:</p>
        <ul>
            <li><strong>IONOS France</strong></li>
            <li><strong>1&amp;1 IONOS SARL</strong></li>
            <li><strong>7 place de la Gare, BP 70109, 57201 Sarreguemines Cedex, France</strong></li>
            <li>Téléphone&#160;: <strong>+33 (0)970 808 911</strong></li>
        </ul>
        <p class="text-muted mb-0"><em>Hébergeur acté MOA sous réserve de confirmation finale de l'infrastructure de production.</em></p>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Propriété intellectuelle">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Propriété intellectuelle</h2>
        <p class="mb-0">L'ensemble des éléments composant le site (structure, textes, visuels, logos, marques lorsqu'elles sont protégées) est la propriété de <strong>Marketone SAS</strong> ou fait l'objet d'une autorisation d'utilisation. Toute reproduction ou représentation non autorisée est interdite.</p>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Données personnelles">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Données personnelles</h2>
        <p>Les données personnelles collectées sur ce site (formulaires contact, newsletter, espace professionnel, commandes) sont traitées conformément à notre <a href="/privacy">politique de confidentialité</a>.</p>
        <p class="mb-0">Pour exercer vos droits&#160;: <a href="mailto:contact.ck@marketone.com">contact.ck@marketone.com</a> ou <a href="/contactus">contactez-nous</a>.</p>
    </div>
</section>
<section class="s_text_block pt16 pb64 o_colored_level" data-snippet="s_text_block" data-name="CGV renvoi">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Conditions générales de vente</h2>
        <p class="mb-0">Les ventes sur la boutique en ligne C-Kreyol sont soumises aux <a href="/terms">conditions générales de vente</a> acceptées électroniquement lors de la commande. Contact SAV&#160;: <a href="mailto:contact.ck@marketone.com">contact.ck@marketone.com</a> — <a href="/contactus">formulaire de contact</a>.</p>
    </div>
</section>
</div>
""".strip()

PRIVACY_PAGE_ARCH = f"""
<div id="wrap" class="oe_structure ck-privacy-page">
{RECETTE_BANNER_HTML}
<section class="s_title pt64 pb16 o_colored_level" data-snippet="s_title" data-name="Titre confidentialité">
    <div class="container s_allow_columns">
        <h1 class="display-5 fw-bold">Politique de confidentialité</h1>
        <p class="lead text-muted mb-0">Traitement des données personnelles sur la boutique <strong>C-Kreyol</strong> (RGPD · loi «&#160;Informatique et Libertés&#160;»).</p>
    </div>
</section>
<section class="s_text_block pt32 pb16 o_colored_level" data-snippet="s_text_block" data-name="Responsable">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Responsable du traitement</h2>
        <p><strong>Marketone SAS</strong> — contact&#160;: <a href="mailto:contact.ck@marketone.com">contact.ck@marketone.com</a>.</p>
        <p class="mb-0">Coordonnées complètes&#160;: <a href="/legal">mentions légales</a>.</p>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Données collectées">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Données collectées</h2>
        <ul>
            <li><strong>Formulaire contact</strong> — identité, e-mail, téléphone, message.</li>
            <li><strong>Newsletter</strong> — e-mail, préférences (consentement explicite).</li>
            <li><strong>Espace professionnel</strong> — identité pro, société, message qualification.</li>
            <li><strong>Commande boutique</strong> — identité, adresse, e-mail, historique commande.</li>
            <li><strong>Compte client</strong> (si activé) — identifiants, coordonnées, historique.</li>
            <li><strong>Navigation</strong> — logs techniques, cookies strictement nécessaires <em>[analytics — À PRÉCISER SI ACTIVÉ]</em>.</li>
        </ul>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Bases légales">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Bases légales</h2>
        <ul>
            <li>Commande / compte&#160;: exécution du contrat.</li>
            <li>Contact / SAV&#160;: intérêt légitime ou mesures précontractuelles.</li>
            <li>Newsletter&#160;: <strong>consentement explicite</strong>.</li>
            <li>Obligations légales&#160;: conservation comptable le cas échéant.</li>
        </ul>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Conservation">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Durées de conservation</h2>
        <p><em>[DURÉES RECETTE — À VALIDER MOA/JURIDIQUE]</em></p>
        <ul>
            <li>Newsletter&#160;: jusqu'à désinscription, puis suppression ou anonymisation sous 30&#160;jours.</li>
            <li>Contact&#160;: 3&#160;ans à compter du dernier échange.</li>
            <li>Commandes&#160;: durée légale comptable et commerciale <em>[À CONFIRMER COMPTABLE]</em>.</li>
            <li>CRM Pro&#160;: durée de la relation commerciale + 3&#160;ans.</li>
        </ul>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Destinataires">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Destinataires</h2>
        <p>Personnes habilitées de <strong>Marketone SAS</strong> et, le cas échéant&#160;:</p>
        <ul>
            <li>Hébergeur&#160;: 1&amp;1 IONOS SARL.</li>
            <li>Prestataire e-mail / newsletter&#160;: <em>[SOUS-TRAITANT À LISTER]</em>.</li>
            <li>Prestataire paiement&#160;: <em>[À LISTER SELON CHECKOUT ODOO]</em>.</li>
        </ul>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Vos droits">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Vos droits</h2>
        <p>Droits d'accès, rectification, effacement, limitation, opposition et portabilité lorsque applicable.</p>
        <p>Exercice&#160;: <a href="mailto:contact.ck@marketone.com">contact.ck@marketone.com</a> ou <a href="/contactus">formulaire de contact</a>.</p>
        <p class="mb-0">Réclamation&#160;: <a href="https://www.cnil.fr" rel="noopener noreferrer" target="_blank">CNIL</a>.</p>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Désinscription">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Désinscription newsletter</h2>
        <p class="mb-0">Lien de désinscription dans chaque e-mail, ou demande à <a href="mailto:contact.ck@marketone.com">contact.ck@marketone.com</a>.</p>
    </div>
</section>
<section class="s_text_block pt16 pb64 o_colored_level" data-snippet="s_text_block" data-name="Cookies">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Cookies et traceurs</h2>
        <p>Cookies strictement nécessaires (session, panier, sécurité). Cookies analytics ou marketing&#160;: <em>[NON ACTIVÉ EN RECETTE / À DOCUMENTER SI ACTIVATION]</em>.</p>
        <p class="mb-0">Dernière mise à jour&#160;: 2026-06-14 (version recette interne).</p>
    </div>
</section>
</div>
""".strip()

TERMS_PAGE_ARCH = f"""
<div id="wrap" class="oe_structure ck-terms-page">
{RECETTE_BANNER_HTML}
<section class="s_title pt64 pb16 o_colored_level" data-snippet="s_title" data-name="Titre CGV">
    <div class="container s_allow_columns">
        <h1 class="display-5 fw-bold">Conditions générales de vente</h1>
        <p class="lead text-muted mb-0">Ventes sur la boutique en ligne <strong>C-Kreyol</strong>, exploitée par <strong>Marketone SAS</strong>.</p>
    </div>
</section>
<section class="s_text_block pt32 pb16 o_colored_level" data-snippet="s_text_block" data-name="Vendeur">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Identification du vendeur</h2>
        <p><strong>Marketone SAS</strong> (SAS) — siège&#160;: 12 rue Example, 44000 Nantes <em>[FICTIF]</em> — SIREN 123&#160;456&#160;789 <em>[FICTIF]</em> — RCS Nantes 123&#160;456&#160;789 <em>[FICTIF]</em>.</p>
        <p class="mb-0">Contact&#160;: <a href="mailto:contact.ck@marketone.com">contact.ck@marketone.com</a> — <a href="/contactus">formulaire de contact</a>.</p>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Objet">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Objet</h2>
        <p class="mb-0">Les présentes CGV définissent les droits et obligations des parties dans le cadre de la vente en ligne de produits proposés sur C-Kreyol.</p>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Produits et prix">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Produits et prix</h2>
        <p>Produits décrits sur les fiches produit. Prix en <strong>euros TTC</strong> avant validation de commande. Frais de livraison indiqués avant paiement.</p>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Commande">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Commande et paiement</h2>
        <p>Commande validée après confirmation du paiement. Paiement en ligne via moyens proposés au checkout Odoo <em>[MODALITÉS SELON CONFIGURATION — RECETTE]</em>.</p>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Livraison">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Livraison</h2>
        <p><em>[MODALITÉS RECETTE — À STABILISER MOA]</em></p>
        <ul>
            <li>Zones&#160;: France métropolitaine ; UE selon transporteurs disponibles.</li>
            <li>Délais indicatifs communiqués avant validation.</li>
        </ul>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Rétractation">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Droit de rétractation</h2>
        <p>Délai de <strong>14&#160;jours</strong> à compter de la réception pour le consommateur, <strong>sous réserve des exclusions légales</strong> (denrées périssables, produits descellés hygiène/santé, etc.).</p>
        <p class="mb-0">Contact&#160;: <a href="mailto:contact.ck@marketone.com">contact.ck@marketone.com</a>. Frais de retour&#160;: <em>[À PRÉCISER MOA]</em>.</p>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Formulaire de rétractation">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Modèle de formulaire de rétractation</h2>
        <p class="text-muted">Conformément à l'annexe à l'article R. 221-1 du Code de la consommation. À compléter et renvoyer uniquement en cas de rétractation.</p>
        <div class="border rounded p-3 p-md-4 ck-terms-withdrawal-form">
            <p class="mb-2">À l'attention de <strong>Marketone SAS</strong>, 12 rue Example, 44000 Nantes <em>[FICTIF]</em> — <a href="mailto:contact.ck@marketone.com">contact.ck@marketone.com</a> :</p>
            <p class="mb-2">Je/nous (*) vous notifie/notifions (*) par la présente ma/notre (*) rétractation du contrat portant sur la vente du bien (*)/pour la prestation de services (*) ci-dessous :</p>
            <p class="mb-2">Commandé le (*)/reçu le (*) : ……………………………………………</p>
            <p class="mb-2">Nom du (des) consommateur(s) : ……………………………………………</p>
            <p class="mb-2">Adresse du (des) consommateur(s) : ……………………………………………</p>
            <p class="mb-2">Signature du (des) consommateur(s) (uniquement en cas de notification du présent formulaire sur papier) :</p>
            <p class="mb-2">Date : ……………………………………………</p>
            <p class="mb-0 small text-muted">(*) Rayez la mention inutile.</p>
        </div>
    </div>
</section>
<section class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Garanties">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Garanties légales</h2>
        <p class="mb-0">Garantie légale de conformité et garantie contre les vices cachés, selon le Code de la consommation et le Code civil.</p>
    </div>
</section>
<section id="cgv" class="s_text_block pt16 pb16 o_colored_level" data-snippet="s_text_block" data-name="Médiation">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Médiation de la consommation</h2>
        <p><strong>[Nom du médiateur — MÉDIATEUR À CONFIRMER AVANT PUBLICATION]</strong></p>
        <p><em>[Adresse / site web du médiateur — FICTIF RECETTE]</em></p>
        <p class="mb-0">Plateforme européenne ODR&#160;: <a href="https://ec.europa.eu/consumers/odr" rel="noopener noreferrer" target="_blank">ec.europa.eu/consumers/odr</a>.</p>
    </div>
</section>
<section class="s_text_block pt16 pb64 o_colored_level" data-snippet="s_text_block" data-name="Droit applicable">
    <div class="container s_allow_columns">
        <h2 class="h3-fs">Droit applicable</h2>
        <p class="mb-0">CGV soumises au <strong>droit français</strong>. Tribunaux compétents selon règles applicables au consommateur.</p>
    </div>
</section>
</div>
""".strip()

FOOTER_LEGAL_LINK_HTML = '<li class="mb-2"><a href="/legal">Mentions légales</a></li>'
FOOTER_PRIVACY_LINK_HTML = '<li class="mb-2"><a href="/privacy">Confidentialité</a></li>'
FOOTER_TERMS_LINK_HTML = '<li class="mb-2"><a href="/terms#cgv">CGV</a></li>'
FOOTER_CONTACT_LINK_MARKER = '<li class="mb-2"><a href="/contactus">Contact</a></li>'
