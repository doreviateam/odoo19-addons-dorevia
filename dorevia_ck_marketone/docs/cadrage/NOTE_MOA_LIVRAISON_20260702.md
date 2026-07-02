# Note MOA — Livraison explicative — Navigation, démo en ligne et home (2 juillet 2026)

| Champ | Valeur |
| --- | --- |
| Date | 2 juillet 2026 |
| Projet | C-Kréyòl Marketone — boutique en ligne |
| Destinataires | MOA, Produit, QA |
| Statut | **Livré et recetté — exploitable en démo** |
| Base | `dorevia_ck_marketone_01` |
| URL locale | http://localhost:18079 |
| URL démo publique | https://assure-violation-markets-factors.trycloudflare.com |
| Version contenu | `dorevia_ck_marketone_content` **19.0.1.81.0** |
| Version thème | `dorevia_ck_theme` **19.0.1.119.0** |
| Commit de référence | `68a0283b` — `feat(ck): CK-NAV-005 liens catégorie racine + polish Home et header wishlist` |

---

## Synthèse exécutive

Depuis le gel boutique V1, **six chantiers complémentaires** ont été livrés et validés :

1. **Navigation header** — catalogue dynamique stabilisé, ordre MOA confirmé, icône Boutique desktop.
2. **Démo en ligne** — boutique accessible via tunnel public pour présentation MOA / acheteur.
3. **Home — hygiène visible (CK-HOME-001C)** — marque, newsletter FR, 4ᵉ carte Boissons.
4. **Home — hero (CK-HOME-001A)** — promesse repositionnée produits + producteurs + savoir-faire · recette mobile 390 px (CA6) documentée.
5. **Home — polish UX (CK-HOME-POLISH-001)** — newsletter retirée de la Home, header favoris/panier clarifié, hero/prix/trust-bar/bloc Pro renforcés.
6. **Navigation — catégories racine cliquables (CK-NAV-005)** — Épicerie, Boissons, Soin & Bien-être et Artisanat : le libellé mène vers la page du rayon ; chevron / accordéon séparé si sous-catégories (desktop et mobile).

Le parcours acheteur reste intact : **Home → Shop → fiche produit → panier → checkout**. Aucun changement sur le tunnel de commande.

**Commits de référence** : `57eb3725` (hero 001A) · `68a0283b` (NAV-005 + polish Home + header wishlist)

---

## 1. Navigation — ce que vous voyez

### Ordre validé MOA (Option C)

```text
Boutique · Épicerie · Boissons · Soin & Bien-être · Artisanat · Producteurs · Professionnels
```

- **Boutique** : icône maison en desktop (≥ 992 px), libellé « Boutique » conservé pour l’accessibilité.
- **Épicerie, Boissons, Soin & Bien-être, Artisanat** : alimentés par les catégories e-commerce publiées ; sous-menus si sous-catégories éligibles.
- **Producteurs** : toujours visible (`/producteurs`).
- **Professionnels** : visible si la page CMS `/professionnels` est active.

### Ce qui a été corrigé sous le capot

| Sujet | Bénéfice MOA |
| --- | --- |
| **CK-NAV-003** | Navigation catalogue depuis le BO Odoo, sans mega-menu legacy. |
| **CK-NAV-003b** | Un ordre de menu ajusté manuellement en BO **n’est plus écrasé** au prochain resync catalogue. |
| **CK-NAV-004** | Bande de navigation centrée en desktop · icône Boutique. |
| **CK-NAV-005** | Catégories racines du header — Épicerie, Boissons, Soin & Bien-être et Artisanat — **cliquables** : le libellé mène vers `/shop/category/...` ; si le rayon a des sous-catégories, le chevron / accordéon les ouvre **sans changer d’URL** ni neutraliser le lien parent. |
| Réalignement séquences (2 juil.) | Ordre Option C appliqué sur catégories e-commerce et menus website. |

### Comment changer l’ordre demain

| Besoin | Action MOA |
| --- | --- |
| Réordonner les rayons visibles | **Website → Configuration → Menus** : modifier la **Séquence** des entrées (Épicerie, Boissons, etc.). |
| Nouveau rayon dans le header | Publier catégorie + produits → resync catalogue ; position initiale selon séquence catégorie BO. |
| Boutique | Reste en première position (comportement technique fixe). |

> Détail technique : [`NOTE_MOA_CLOTURE_CK_NAV_003_20260701.md`](NOTE_MOA_CLOTURE_CK_NAV_003_20260701.md) · [`NOTE_MOA_CLOTURE_CK_NAV_003B_SEQUENCE_BO_RESYNC_20260701.md`](NOTE_MOA_CLOTURE_CK_NAV_003B_SEQUENCE_BO_RESYNC_20260701.md) · [`NOTE_MOA_CLOTURE_CK_NAV_004_20260701.md`](NOTE_MOA_CLOTURE_CK_NAV_004_20260701.md) · [`NOTE_MOA_CLOTURE_CK_NAV_005_20260702.md`](NOTE_MOA_CLOTURE_CK_NAV_005_20260702.md)

### CK-NAV-005 — ce que change le clic (desktop et mobile)

Les catégories racines du header — **Épicerie, Boissons, Soin & Bien-être et Artisanat** — sont désormais traitées comme des entrées de navigation marchandes : le libellé mène vers la page du rayon correspondant (`/shop/category/...`).

Lorsqu’un rayon possède des sous-catégories, le chevron desktop ou l’accordéon mobile ouvre le sous-menu **sans quitter la page en cours** et **sans neutraliser le lien parent**. Soin & Bien-être, sans sous-menu sur l’instance de recette, reste un lien direct simple — conforme à la règle : tout item de niveau 0 avec destination est cliquable.

| Action | Résultat attendu |
| --- | --- |
| Clic sur **« Épicerie »** (libellé) | Navigation vers `/shop/category/epicerie-1` |
| Clic sur le **chevron** Épicerie (desktop) | Ouvre le dropdown des sous-catégories · **URL inchangée** |
| Clic sur **« Soin & Bien-être »** (libellé) | Navigation vers la page catégorie du rayon |
| Clic sur **« Boissons »** (libellé mobile, drawer) | Navigation vers la page catégorie Boissons |
| Clic sur le **toggle accordéon** Boissons (mobile) | Ouvre le panneau sous-catégories · **URL inchangée** |

**Pourquoi ce changement** : avant NAV-005, un rayon avec sous-catégories ne permettait pas d’accéder directement à sa page « toutes les produits du rayon » — seul le sous-menu était actionnable. C’est corrigé sans toucher à l’ordre des menus ni au back-office.

**Recette validée** : desktop 1280 px · mobile 390 px · routes catégorie en HTTP 200 · 43 tests auto, 0 échec.

---

## 2. Démo en ligne — comment présenter la boutique

### URL publique

**https://assure-violation-markets-factors.trycloudflare.com**

Parcours validé : Home → navigation → Shop → fiche produit → Producteurs → Professionnels.

### Réserves connues (non bloquantes pour une démo live)

| Point | Impact | À dire en présentation |
| --- | --- | --- |
| Meta / canonical pointent vers `localhost:18079` | Partage réseaux sociaux incorrect si on copie l’URL tunnel | Démo technique interne — URL tunnel à usage présentation, pas SEO prod. |
| Navigateur FR | OK en français | — |
| Tunnel Cloudflare | Dépend d’un processus actif côté infra | Ne pas couper le tunnel pendant la démo. |

> Détail : [`NOTE_MOA_CLOTURE_CK_DEMO_ONLINE_001_20260702.md`](NOTE_MOA_CLOTURE_CK_DEMO_ONLINE_001_20260702.md)

---

## 3. Home — CK-HOME-001C — ce qui change pour le visiteur

### Newsletter

- Message de succès en **français** : *Merci pour votre inscription !*
- Plus de texte anglais résiduel (*Thanks for registering*) sur la home.

### Marque C-Kréyòl

- Orthographe harmonisée **C-Kréyòl** (avec accent grave sur le ò) sur la home, le footer, les pages légales (`/legal`, `/privacy`, `/terms`).
- Ancienne forme « C-Kreyol » retirée des pages visibles.

### Section « Acheter par univers »

| Avant | Après |
| --- | --- |
| 3 cartes (Épicerie, Soin, Artisanat) | **4 cartes** : Épicerie · **Boissons** · Soin & Bien-être · Artisanat |
| Intro « Trois univers… » | Intro **« Quatre univers pour entrer dans la boutique en un clic. »** |
| — | Visuel Boissons : photo produit nectar Mont Pelé (alignée sur les autres cartes) |

### Ce qui ne change pas (001C)

- Section « Nos coups de cœur », coffrets découverte, bloc pro (structure).
- Tunnel achat, fiches produit, Producteurs.

> Détail 001C : [`NOTE_MOA_CLOTURE_CK_HOME_001C_20260702.md`](NOTE_MOA_CLOTURE_CK_HOME_001C_20260702.md)

### Hero CK-HOME-001A — livré

| Élément | Valeur |
| --- | --- |
| Kicker | `Produits créoles · Producteurs · Savoir-faire` |
| Titre | `C-Kréyòl — les saveurs créoles en Europe` |
| CTA principal | `Découvrir la boutique` → `/shop` |
| CTA secondaire | `Voir les producteurs` → `/producteurs` |

**Recette mobile (CA6)** : viewport **390 px** — pas d'overflow (`390/390`), textes 001A présents, 2 CTA empilés, visuel carrousel visible.

Capture : [`ck_home_001a_hero_mobile_390.png`](../design/maquette_01.2/captures/ck_home_001a_20260702/ck_home_001a_hero_mobile_390.png)

> Détail 001A : [`NOTE_MOA_CLOTURE_CK_HOME_001A_20260702.md`](NOTE_MOA_CLOTURE_CK_HOME_001A_20260702.md)

---

## 4. Home — CK-HOME-POLISH-001 — polish avant ouverture

Micro-lot de **corrections UX ciblées** sur la Home, sans remise en cause de la structure validée (hero, vedettes, univers, coffrets, footer).

### Ce que voit le visiteur

| Sujet | Avant | Après |
| --- | --- | --- |
| **Newsletter (Home)** | Bloc dual Pro + newsletter · message « Merci pour votre inscription ! » visible au chargement | **Bloc Pro seul** · pas de formulaire newsletter sur la Home |
| **Header desktop** | Favoris / panier peu distincts | Icônes **cœur** et **panier** séparées · badges compteur masqués à zéro |
| **Icône favoris** | Cœur rouge en permanence | **Cœur contour neutre** par défaut (comme compte/panier) · rouge CK au survol · badge rouge uniquement si favoris présents |
| **Hero** | Wording MOA inchangé | Lisibilité renforcée (fond semi-opaque desktop, CTA principal plus visible) |
| **Prix vedettes** | — | Prix TTC **15 px / graisse 700** sur « Nos coups de cœur » |
| **Trust-bar** | — | Icônes et hiérarchie renforcées (livraison, paiement, producteurs, service) |
| **Bloc Pro** | — | Wording B2B clarifié · CTA « Demander un accès professionnel » |

**Hors périmètre Home** : newsletter conservée sur `/contactus` et `/professionnels`. Stratégie Email Marketing / RGPD → lot futur.

> Détail : [`NOTE_MOA_LIVRAISON_CK_HOME_POLISH_001_20260702.md`](NOTE_MOA_LIVRAISON_CK_HOME_POLISH_001_20260702.md) · clôture [`NOTE_MOA_CLOTURE_CK_HOME_POLISH_001_20260702.md`](NOTE_MOA_CLOTURE_CK_HOME_POLISH_001_20260702.md)

---

## 5. Contrôles rapides MOA (5 minutes)

Sur l’URL démo ou `localhost:18079` :

1. **Hero** : kicker « Produits créoles… » · titre « C-Kréyòl — les saveurs créoles en Europe » · CTA producteurs.
2. **Header** : ordre Option C · icône Boutique · **clic sur tout rayon racine (Épicerie, Boissons, Soin & Bien-être, Artisanat) → page catégorie** · chevron ouvre sous-menu sans changer d’URL.
3. **Home** : 4 cartes univers · intro « Quatre univers » · **pas de newsletter** · bloc Pro seul en bas.
4. **Header favoris** : cœur **gris/contour** à vide · badge rouge seulement après ajout d’un favori.
5. **Footer** : © **C-Kréyòl** (avec accent).
6. **Shop** : `/shop` charge · fiche produit témoin OK.
7. **Producteurs** : `/producteurs` — photos chargées.
8. **Mobile 390 px — header** : drawer · lien catégorie séparé du toggle accordéon · pas de débordement horizontal.
9. **Mobile 390 px — hero 001A (CA6)** : textes et CTA conformes · empilement vertical · capture archivée (§ 3).

---

## 6. Rappel contexte V1 boutique

La **V1 boutique reste gelée** (tag `v1.0.0-boutique`). Les lots ci-dessus sont des **compléments post-gel** : navigation, démo, hygiène home.

Dettes V1.1 et backlog inchangés — cf. [`NOTE_MOA_CLOTURE_V1_BOUTIQUE_20260629.md`](NOTE_MOA_CLOTURE_V1_BOUTIQUE_20260629.md).

---

## 7. Suite backlog

Les lots **001C**, **001A**, **CK-HOME-POLISH-001** et **CK-NAV-005** sont **clôturés GO** (2 juillet 2026). Prochaines pistes :

| Lot / thème | Objectif | Statut |
| --- | --- | --- |
| **CK-NAV-005** | Catégories racine cliquables (lien + toggle) | **Clôturé GO** — [`NOTE_MOA_CLOTURE_CK_NAV_005_20260702.md`](NOTE_MOA_CLOTURE_CK_NAV_005_20260702.md) |
| **CK-HOME-POLISH-001** | Polish UX Home (newsletter, header, hero, prix…) | **Clôturé GO** — [`NOTE_MOA_CLOTURE_CK_HOME_POLISH_001_20260702.md`](NOTE_MOA_CLOTURE_CK_HOME_POLISH_001_20260702.md) |
| **CK-HOME-001B** | Vedettes E1 + coffret E2 (visuel) | **GO Dev** — [`TICKET_DEV_HOME_VISUAL_CK_HOME_001B.md`](TICKET_DEV_HOME_VISUAL_CK_HOME_001B.md) |
| **CK-HOME-002** (ex-001B producteurs) | Bloc producteurs / transformateurs en home | Backlog — cadrage à ouvrir |
| **SEO / canonical démo** | `web.base.url` ou override canonical sur URL tunnel / prod | Réserve CK-DEMO-ONLINE-001 |
| **V1.1 technique** | Dettes D1–D3 (cards Manio, ruban fallback, breakpoint 480–575 px) | Backlog — cf. clôture V1 |
| **D4 réseau header** | Appel `/shop/wishlist?count=1` sur `#top_menu` | Backlog technique |
| **Éditorial / i18n** | Rayons, fiches, traductions EN, contenu CMS | En cours / backlog |
| **Hors périmètre court terme** | Refonte `/producteurs`, communauté, forum, blog, déploiement prod | Non engagé |

**Recommandation MOA** : valider le cadrage [`NOTE_MOA_CADRAGE_CK_HOME_001B_20260702.md`](NOTE_MOA_CADRAGE_CK_HOME_001B_20260702.md) — priorité **vedettes + coffret** (E1/E2) ; hero et hygiène visible déjà stabilisés.

---

## Verdict MOA proposé

```text
Navigation Option C · NAV-005 catégories cliquables · démo tunnel
· home 001C + hero 001A + polish Home · header favoris neutre
→ GO exploitation démo
→ Prochaine étape : **exécution CK-HOME-001B** (vedettes + coffret) — ticket Dev ouvert
→ Code livré sur main : commit 68a0283b
```

---

*Note MOA — C-Kréyòl Marketone · Livraison explicative — 2 juillet 2026*
