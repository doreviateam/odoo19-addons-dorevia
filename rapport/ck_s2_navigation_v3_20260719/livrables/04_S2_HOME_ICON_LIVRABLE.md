# S2 — Correctif icône Accueil (drawer mobile)

**Module** : `dorevia_ck_marketone_content` **19.0.1.99.0**  
**Base** : `77197a3` (séquences atomiques)  
**Cause QA** : NO GO 390×844 — premier item drawer = texte « Boutique », sans icône maison ni `aria-label` d’accueil.

## Cause racine

La branche QWeb shop-root (`website_nav_ck_shop_v2.xml`) ne s’active que si `submenu._ck_nav_is_shop_root()` (classe `ck-nav-shop-root`).  
Le sync V3 créait Boutique **sans** `css_class` → fallback texte visible.

## Correctif

1. `sync_ck_catalogue_navigation_for_website` : Boutique reçoit `css_class=NAV_CSS_SHOP_ROOT`.
2. Rendu shop-root : `fa-home` + `aria-label` / `title` / `visually-hidden` = **Accueil** (plus de libellé « Boutique » visible).
3. Tests sync + header alignés.

## Hors périmètre

Pas de push / PR / déploiement. Contre-recette QA 390px à rejouer après upgrade module.
