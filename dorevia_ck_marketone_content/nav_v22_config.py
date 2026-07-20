# -*- coding: utf-8 -*-
"""Header CK V2.2 — configuration MOA figée (navigation N3 + mega-menus)."""

# CSS classes navigation N3
NAV_CSS_NO_AUTOHIDE = 'o_no_autohide_item'
NAV_CSS_N3_RAYON = 'ck-nav-n3-rayon'
NAV_CSS_N3_SELECTION = 'ck-nav-n3-selection'
NAV_CSS_N3_RELATION = 'ck-nav-n3-relation'
NAV_CSS_N3_GROUP_END = 'ck-nav-n3-group-end'
NAV_CSS_PRODUCTEURS = 'ck-nav-producteurs'
NAV_CSS_ESPACE_PRO = 'ck-nav-espace-pro'
NAV_CSS_MEGA_PRODUCT = 'ck-nav-mega-product'
NAV_CSS_SHOP_ROOT = 'ck-nav-shop-root'

# Entrées racine N3 — séquences MOA
NAV_ALL_LABEL = 'Tous nos produits'
NAV_ALL_URL = '/shop'
NAV_ALL_SEQUENCE = 10

NAV_EPICERIE_LABEL = 'Épicerie'
NAV_BOISSONS_LABEL = 'Boissons'
NAV_MAISON_LABEL = 'Soin & Bien-être'
LEGACY_NAV_MAISON_LABEL = 'Maison & Bien-être'  # ancien libellé N3 — retiré du header
NAV_ARTISANAT_LABEL = 'Artisanat'
NAV_COMMUNAUTE_LABEL = 'Communauté'
# S6-B2bis : libellé technique racine website_blog (purge chirurgicale, pas LEGACY).
NAV_BLOG_DEFAULT_LABEL = 'Blog'
NAV_COMMUNAUTE_URL = '#'
# S6-B2 — enfants gérés de Communauté (child_menus V3)
NAV_COMMUNAUTE_MAGAZINE_LABEL = 'Magazine'
NAV_COMMUNAUTE_RECETTES_LABEL = 'Recettes'
NAV_COMMUNAUTE_MAGAZINE_SEQUENCE = 10
NAV_COMMUNAUTE_RECETTES_SEQUENCE = 20
XMLID_CK_BLOG_MAGAZINE = 'dorevia_ck_marketone_content.ck_blog_magazine'
XMLID_CK_BLOG_RECETTES = 'dorevia_ck_marketone_content.ck_blog_recettes'
LEGACY_NAV_COUPS_LABEL = 'Coups de cœur'  # ancienne entrée N3 — retirée du header
NAV_COFFRETS_LABEL = 'Coffrets'
NAV_PRODUCTEURS_LABEL = 'Nos producteurs'
NAV_ESPACE_PRO_LABEL = 'Espace pro'

NAV_RAYON_SEQUENCE = {
    NAV_EPICERIE_LABEL: 20,
    NAV_BOISSONS_LABEL: 25,
    NAV_MAISON_LABEL: 30,
    NAV_ARTISANAT_LABEL: 35,
}
# S6-B1 A3 : Communauté = 55 (hors bloc catalogue 20…50, avant Producteurs 60).
# Conservé dans NAV_SELECTION_SEQUENCE pour compat _sync_communaute (migrations 39/40).
NAV_SELECTION_SEQUENCE = {
    NAV_COMMUNAUTE_LABEL: 55,
    NAV_COFFRETS_LABEL: 50,
}
NAV_RELATION_SEQUENCE = {
    NAV_PRODUCTEURS_LABEL: 60,
    NAV_ESPACE_PRO_LABEL: 70,
}

NAV_PRODUCTEURS_URL = '/producteurs'
NAV_PRO_PAGE_URL = '/professionnels'

# Mega-menu keys (sélection bloc visuel BO)
MEGA_MENU_EPICERIE = 'epicerie'
MEGA_MENU_BOISSONS = 'boissons'
MEGA_MENU_MAISON = 'maison_bien_etre'
MEGA_MENU_ARTISANAT = 'artisanat'

# Familles figées MOA — (libellé front, slug, alias recherche catégorie BO)
EPICERIE_FAMILIES = (
    ('Biscuits & crackers', 'biscuits-crackers', ('Biscuits', 'Biscuits & crackers')),
    ('Confitures & douceurs', 'confitures-douceurs', ('Confitures', 'Confitures & douceurs')),
    ('Farines & manioc', 'farines-manioc', ('Farines', 'Farines & manioc', 'Manioc')),
    ('Sauces & condiments', 'sauces-condiments', ('Sauces', 'Condiments', 'Épices')),
    ('Chocolat & cacao', 'chocolat-cacao', ('Chocolat', 'Cacao')),
    ('Café & infusions', 'cafe-infusions', ('Café', 'Infusions', 'Thé')),
)

BOISSONS_FAMILIES = (
    ('Jus & nectars', 'jus-nectars', ('Jus', 'Jus de fruits', 'Nectars')),
    ('Sirops créoles', 'sirops-creoles', ('Sirops', 'Sirop')),
    ('Boissons locales', 'boissons-locales', ('Boissons locales',)),
    ('Boissons fraîches', 'boissons-fraiches', ('Boissons fraîches',), True),  # conditionnel
    ('Apéritifs & boissons festives', 'aperitifs-boissons-festives', ('Apéritifs', 'Apéritif')),
    ('Préparations à boire', 'preparations-a-boire', ('Préparations',)),
)

MAISON_FAMILIES = (
    ('Savons & soins solides', 'savons-soins-solides', ('Savons', 'Savon')),
    ('Huiles & baumes', 'huiles-baumes', ('Huiles', 'Baumes')),
    ('Senteurs & bougies', 'senteurs-bougies', ('Senteurs', 'Bougies')),
    ('Maison & décoration', 'maison-decoration', ('Décoration', 'Maison')),
    ('Accessoires bien-être', 'accessoires-bien-etre', ('Accessoires',)),
    ('Rituels créoles', 'rituels-creoles', ('Rituels',)),
)

ARTISANAT_FAMILIES = (
    ('Objets décoratifs', 'objets-decoratifs', ('Objets décoratifs', 'Décoratif')),
    ('Arts de la table', 'arts-de-la-table', ('Arts de la table',)),
    ('Textile & accessoires', 'textile-accessoires', ('Textile',)),
    ('Bijoux & créations', 'bijoux-creations', ('Bijoux',)),
    ('Papeterie & affiches', 'papeterie-affiches', ('Papeterie', 'Affiches')),
    ('Créations artisanales', 'creations-artisanales', ('Créations artisanales',)),
)

# Sélections CK — (libellé, type, source)
# type: tag | supplier | category
EPICERIE_SELECTIONS = (
    ('Coups de cœur', 'tag', 'coup_de_coeur'),
    ('Nouveautés', 'tag', 'nouveaute'),
    ('Coffrets découverte', 'tag', 'coffret'),
    ('Produits La Platine', 'supplier', 'La Platine'),
    ('Idées cadeaux', 'tag', 'cadeau'),
)

BOISSONS_SELECTIONS = (
    ('Coups de cœur', 'tag', 'coup_de_coeur'),
    ('Nouveautés', 'tag', 'nouveaute'),
    ('Sans alcool', 'tag', 'sans_alcool'),
    ('Apéritif', 'tag', 'aperitif'),
)

MAISON_SELECTIONS = (
    ('Coups de cœur', 'tag', 'coup_de_coeur'),
    ('Nouveautés', 'tag', 'nouveaute'),
    ('Bien-être naturel', 'tag', 'bien_etre_naturel'),
    ('Maison', 'tag', 'maison'),
    ('Idées cadeaux', 'tag', 'cadeau'),
)

ARTISANAT_SELECTIONS = (
    ('Coups de cœur', 'tag', 'coup_de_coeur'),
    ('Nouveautés', 'tag', 'nouveaute'),
    ('Idées cadeaux', 'tag', 'cadeau'),
    ('Créateurs à découvrir', 'tag', 'createur'),
    ('Petites séries', 'tag', 'petite_serie'),
)

# Origines MOA — (libellé, slug attribut)
ORIGINS_EPICERIE = (
    ('Guadeloupe', 'guadeloupe'),
    ('Martinique', 'martinique'),
    ('Dominique', 'dominique'),
    ('Guyane', 'guyane'),
)

# Espace pro dropdown
ESPACE_PRO_LINKS = (
    ('Acheter pour mon commerce', f'{NAV_PRO_PAGE_URL}#acheter'),
    ('Demander les conditions pro', f'{NAV_PRO_PAGE_URL}#conditions'),
    ('Devenir partenaire / distributeur', f'{NAV_PRO_PAGE_URL}#partenaire'),
    ('Contacter C-Kréyòl', f'{NAV_PRO_PAGE_URL}#contact'),
)

# Coffrets mini-dropdown — angles commerciaux
COFFRETS_ANGLES = (
    ('Découverte', 'tag', 'coffret'),
    ('Cadeau', 'tag', 'cadeau'),
    ('Entreprise / pro', 'tag', 'coffret_pro'),
    ('Saison / fête', 'tag', 'saison'),
    ('Origine / territoire', 'tag', 'origine'),
)

COFFRETS_MINI_DROPDOWN_MIN_ANGLES = 3
ARTISANAT_MEGA_MIN_FAMILIES = 3

# Paramètre système — famille Boissons fraîches conditionnelle
PARAM_BOISSONS_FRAICHES = 'ck.nav.boissons_fraiches_enabled'

# Racines catalogue — correspondance libellé N3 → noms racine BO possibles
RAYON_ROOT_ALIASES = {
    NAV_EPICERIE_LABEL: ('Épicerie', 'Épicerie créole'),
    NAV_BOISSONS_LABEL: ('Boissons',),
    NAV_MAISON_LABEL: ('Maison & Bien-être', 'Maison & bien-être', 'Soin & Bien-être'),
    NAV_ARTISANAT_LABEL: ('Artisanat', 'Artisanat & Culture'),
}

LEGACY_ROOT_MENU_NAMES = frozenset({
    'Boutique', 'Professionnels', 'Contactez-nous', 'Contact Us', 'Contact us',
    'Accueil', 'Home', 'Shop', 'Contact', 'Catégories', 'Épicerie créole',
    'Soin & Bien-être', 'Artisanat', 'Découvrir', 'Nos univers',
    LEGACY_NAV_COUPS_LABEL,
})

MANAGED_V22_ROOT_NAMES = frozenset({
    NAV_ALL_LABEL,
    NAV_EPICERIE_LABEL,
    NAV_BOISSONS_LABEL,
    NAV_MAISON_LABEL,
    NAV_ARTISANAT_LABEL,
    # S6-B1 A1/A4 : Communauté retirée — racine éditoriale V3, plus un vestige V2.2.
    NAV_COFFRETS_LABEL,
    NAV_PRODUCTEURS_LABEL,
    NAV_ESPACE_PRO_LABEL,
})

# V1 — navigation simplifiée (3 liens plats, mega-menus mis en réserve)
NAV_V1_BOUTIQUE_LABEL = 'Boutique'
NAV_V1_PRODUCTEURS_LABEL = 'Producteurs'
NAV_V1_PROFESSIONNELS_LABEL = 'Professionnels'
NAV_V1_BOUTIQUE_SEQUENCE = 10
NAV_V1_PRODUCTEURS_SEQUENCE = 20
NAV_V1_PROFESSIONNELS_SEQUENCE = 30

MANAGED_V1_ROOT_NAMES = frozenset({
    NAV_V1_BOUTIQUE_LABEL,
    NAV_V1_PRODUCTEURS_LABEL,
    NAV_V1_PROFESSIONNELS_LABEL,
})

# ---------------------------------------------------------------------------
# NAV-003 — Navigation catalogue dynamique (product.public.category)
# ---------------------------------------------------------------------------

NAV_CATALOGUE_BOUTIQUE_LABEL = 'Boutique'
NAV_CATALOGUE_PRODUCTEURS_LABEL = 'Producteurs'
NAV_CATALOGUE_PROFESSIONNELS_LABEL = 'Professionnels'

NAV_CATALOGUE_BOUTIQUE_URL = '/shop'
NAV_CATALOGUE_PRODUCTEURS_URL = '/producteurs'
NAV_CATALOGUE_PROFESSIONNELS_URL = '/professionnels'

NAV_CATALOGUE_BOUTIQUE_SEQUENCE = 10
NAV_CATALOGUE_FIRST_CATEGORY_SEQUENCE = 20
NAV_CATALOGUE_SEQUENCE_STEP = 10
# Racines fixes stratégiques — ordres canoniques MOA (S2 / QA ordre header).
# Distincts des créneaux catégories (20, 30, …) pour éviter les collisions
# héritées du type Producteurs=20 ∩ Épicerie=20 (ordre non déterministe via id ORM).
NAV_CATALOGUE_PRODUCTEURS_SEQUENCE = 60
NAV_CATALOGUE_PROFESSIONNELS_SEQUENCE = 70
# S6-B1 A3 : après bloc catalogue (20…50), avant Producteurs (60).
NAV_CATALOGUE_COMMUNAUTE_SEQUENCE = 55

NAV_CATALOGUE_RESERVED_ROOT_SEQUENCES = frozenset({
    NAV_CATALOGUE_BOUTIQUE_SEQUENCE,
    NAV_CATALOGUE_COMMUNAUTE_SEQUENCE,
    NAV_CATALOGUE_PRODUCTEURS_SEQUENCE,
    NAV_CATALOGUE_PROFESSIONNELS_SEQUENCE,
})

MANAGED_CATALOGUE_FIXED_ROOT_NAMES = frozenset({
    NAV_CATALOGUE_BOUTIQUE_LABEL,
    NAV_CATALOGUE_PRODUCTEURS_LABEL,
    NAV_CATALOGUE_PROFESSIONNELS_LABEL,
})

# S6-B1 A4 : racines éditoriales V3 (hors catalogue). Ne pas fusionner dans
# MANAGED_CATALOGUE_FIXED_ROOT_NAMES — sémantique catalogue vs éditorial.
MANAGED_EDITORIAL_ROOT_NAMES = frozenset({
    NAV_COMMUNAUTE_LABEL,
})
