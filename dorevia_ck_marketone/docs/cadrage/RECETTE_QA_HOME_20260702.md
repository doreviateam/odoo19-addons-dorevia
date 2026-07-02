# Recette QA Home C-Kreyol Marketone - CK-HOME-001C / 001A / 001B

| Champ | Valeur |
| --- | --- |
| Date | 2026-07-02 |
| Base | `dorevia_ck_marketone_01` |
| URL locale | `http://localhost:18079` |
| URL demo | `https://assure-violation-markets-factors.trycloudflare.com` |
| Versions code controlees | `dorevia_ck_marketone_content 19.0.1.78.0` ; `dorevia_ck_theme 19.0.1.115.0` |
| Commit de reference demande | `43aa89fa` - `fix(ck-home): CK-HOME-001B images vedettes visibles et visuel coffret qualifie` |
| Viewports | Desktop 1280 px ; mobile 390 px |

## Verdict global

**NO GO strict sur le critere CTA Coffrets**

Reprise hotfix effectuee apres upgrade sandbox.

Les deux anomalies initiales sont corrigees :

- Plus de texte technique visible entre Coffrets et Pro/Newsletter, desktop 1280 et mobile 390.
- La route directe `/kits` redirige bien vers `/shop?marketone_mode=pack` en local et tunnel.

Reserve fonctionnelle restante : le clic reel au centre du bouton visuel `Decouvrir` est intercepte par le lien etendu `Coffret decouverte creole` (`stretched-link`) et arrive sur `/shop/coffret-decouverte-creole-4583`, pas sur `/shop?marketone_mode=pack`. La route `/kits` est bonne, mais la cible cliquee par l'utilisateur n'est pas celle du bouton.

## Tableau de recette

| Zone | Desktop 1280 | Mobile 390 | Commentaire |
| --- | --- | --- | --- |
| Hero CK-HOME-001A | OK | OK | Kicker, H1, sous-titre et CTA presents. `/shop` et `/producteurs` repondent `200`. CTA empiles en mobile. |
| Reassurance | OK | OK | 4 items visibles, pas d'overflow horizontal. |
| Nos coups de coeur | OK | OK | Bloc visible, 4 cartes, images chargees, prix et liens fiche produit presents. |
| CTA panier vedette | OK | OK | Produit temoin : `Confiture de goyave`. Ajout panier OK, panier accessible. |
| Acheter par univers | OK | OK | 4 cartes : Epicerie, Boissons, Soin, Artisanat. Intro attendue presente. |
| Coffrets decouverte | Reserve fonctionnelle | Reserve fonctionnelle | Image coffret qualifiee OK, pas de fallback beige. `/kits` redirige OK vers `/shop?marketone_mode=pack`, mais le clic reel sur le bouton est intercepte par le lien etendu de la fiche coffret. |
| Dual Pro / Newsletter | OK | OK | Plus de fragment HTML technique visible. Message newsletter FR present : `Merci pour votre inscription !`; pas de `Thanks for registering`. |
| Editorial bas | OK | OK | Section presente ; plus de texte technique visible avant cette zone. |
| Footer | OK | OK | Graphie accentuee visible dans le HTML rendu : `© C-Kréyòl`. |
| Header smoke | OK | OK | Ordre Option C visible : Boutique, Epicerie, Boissons, Soin, Artisanat, Producteurs, Professionnels. Drawer mobile OK, pas d'overflow. |
| Tunnel achat | OK | Non applicable | URL publique : `/shop` 200, fiche vedette 200, ajout panier OK, retour home conserve hero/univers/coffret. |

## Controles HTTP

| Route | Local | Tunnel | Commentaire |
| --- | --- | --- | --- |
| `/` | `200` | `200` | Home chargee en FR avec `Accept-Language: fr-FR`. |
| `/shop` | `200` | `200` | Smoke achat OK. |
| `/producteurs` | `200` | `200` | CTA hero OK en local et tunnel. |
| `/shop/confiture-de-goyave-3` | `200` | `200` | Fiche produit temoin issue des vedettes. |
| `/kits` | `200` final `/shop?marketone_mode=pack` | `200` final `/shop?marketone_mode=pack` | Route directe corrigee. |

## Captures

- Desktop 1280 - vedettes : `docs/cadrage/captures/recette_home_20260702/home_desktop_1280_vedettes.jpg`
- Desktop 1280 - coffret post-hotfix : `docs/cadrage/captures/recette_home_20260702/home_desktop_1280_coffret_hotfix.jpg`
- Mobile 390 - vedettes : `docs/cadrage/captures/recette_home_20260702/home_mobile_390_vedettes.jpg`
- Mobile 390 - coffret : `docs/cadrage/captures/recette_home_20260702/home_mobile_390_coffret.jpg`

## Produit temoin panier

Produit utilise : **Confiture de goyave** (`/shop/confiture-de-goyave-3`).

Sur le tunnel public, le CTA panier d'une vedette ajoute bien le produit au panier ; `/shop/cart` affiche `Confiture de goyave`.

## Reserves connues hors scope

- Canonical / metas tunnel pouvant pointer vers localhost : hors scope, reserve connue.
- Refonte navigation, `/promotions`, bloc producteurs home CK-HOME-002 : hors scope.
