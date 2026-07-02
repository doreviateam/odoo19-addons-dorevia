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
| Version contenu | `dorevia_ck_marketone_content` **19.0.1.75.0** |
| Version thème | `dorevia_ck_theme` **19.0.1.114.0** (navigation desktop) |

---

## Synthèse exécutive

Depuis le gel boutique V1, quatre chantiers complémentaires ont été livrés et validés :

1. **Navigation header** — catalogue dynamique stabilisé, ordre MOA confirmé, icône Boutique desktop.
2. **Démo en ligne** — boutique accessible via tunnel public pour présentation MOA / acheteur.
3. **Home — hygiène visible (CK-HOME-001C)** — marque, newsletter FR, 4ᵉ carte Boissons.
4. **Home — hero (CK-HOME-001A)** — promesse repositionnée produits + producteurs + savoir-faire · recette mobile 390 px (CA6) documentée.

Le parcours acheteur reste intact : **Home → Shop → fiche produit → panier → checkout**. Aucun changement sur le tunnel de commande.

**Commit de référence 001A** : `57eb3725` — `feat(ck-home): CK-HOME-001A repositionner le hero`

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
| Réalignement séquences (2 juil.) | Ordre Option C appliqué sur catégories e-commerce et menus website. |

### Comment changer l’ordre demain

| Besoin | Action MOA |
| --- | --- |
| Réordonner les rayons visibles | **Website → Configuration → Menus** : modifier la **Séquence** des entrées (Épicerie, Boissons, etc.). |
| Nouveau rayon dans le header | Publier catégorie + produits → resync catalogue ; position initiale selon séquence catégorie BO. |
| Boutique | Reste en première position (comportement technique fixe). |

> Détail technique : [`NOTE_MOA_CLOTURE_CK_NAV_003_20260701.md`](NOTE_MOA_CLOTURE_CK_NAV_003_20260701.md) · [`NOTE_MOA_CLOTURE_CK_NAV_003B_SEQUENCE_BO_RESYNC_20260701.md`](NOTE_MOA_CLOTURE_CK_NAV_003B_SEQUENCE_BO_RESYNC_20260701.md) · [`NOTE_MOA_CLOTURE_CK_NAV_004_20260701.md`](NOTE_MOA_CLOTURE_CK_NAV_004_20260701.md)

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

- Section « Nos coups de cœur », coffrets découverte, bloc pro / newsletter (structure).
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

## 4. Contrôles rapides MOA (5 minutes)

Sur l’URL démo ou `localhost:18079` :

1. **Hero** : kicker « Produits créoles… » · titre « C-Kréyòl — les saveurs créoles en Europe » · CTA producteurs.
2. **Header** : ordre Option C · icône Boutique · dropdowns Épicerie / Boissons / Artisanat.
3. **Home** : 4 cartes univers · intro « Quatre univers » · bloc newsletter en FR.
4. **Footer** : © **C-Kréyòl** (avec accent).
5. **Shop** : `/shop` charge · fiche produit témoin OK.
6. **Producteurs** : `/producteurs` — photos chargées.
7. **Mobile 390 px — header** : menu drawer · pas de débordement horizontal (cf. démo CK-DEMO-ONLINE-001).
8. **Mobile 390 px — hero 001A (CA6)** : textes et CTA conformes · empilement vertical · capture archivée (§ 3).

---

## 5. Rappel contexte V1 boutique

La **V1 boutique reste gelée** (tag `v1.0.0-boutique`). Les lots ci-dessus sont des **compléments post-gel** : navigation, démo, hygiène home.

Dettes V1.1 et backlog inchangés — cf. [`NOTE_MOA_CLOTURE_V1_BOUTIQUE_20260629.md`](NOTE_MOA_CLOTURE_V1_BOUTIQUE_20260629.md).

---

## 6. Suite backlog

Les lots home **001C** et **001A** sont **clôturés GO** (2 juillet 2026). Prochaines pistes, par priorité produit :

| Lot / thème | Objectif | Statut |
| --- | --- | --- |
| **CK-HOME-001B** | Réserves visuelles home (vedettes E1, coffret E2, arbitrage `/promotions` E3) | **Cadrage ouvert** — [`NOTE_MOA_CADRAGE_CK_HOME_001B_20260702.md`](NOTE_MOA_CADRAGE_CK_HOME_001B_20260702.md) |
| **SEO / canonical démo** | `web.base.url` ou override canonical sur URL tunnel / prod | Réserve CK-DEMO-ONLINE-001 |
| **V1.1 technique** | Dettes D1–D3 (cards Manio, ruban fallback, breakpoint 480–575 px) | Backlog — cf. clôture V1 |
| **D4 réseau header** | Appel `/shop/wishlist?count=1` sur `#top_menu` | Backlog technique |
| **Éditorial / i18n** | Rayons, fiches, traductions EN, contenu CMS | En cours / backlog |
| **Hors périmètre court terme** | Refonte `/producteurs`, communauté, forum, blog, déploiement prod | Non engagé |

**Recommandation MOA** : valider le cadrage [`NOTE_MOA_CADRAGE_CK_HOME_001B_20260702.md`](NOTE_MOA_CADRAGE_CK_HOME_001B_20260702.md) — priorité **vedettes + coffret** (E1/E2) ; hero et hygiène visible déjà stabilisés.

---

## Verdict MOA proposé

```text
Navigation Option C · démo tunnel · home CK-HOME-001C · hero CK-HOME-001A (CA6 mobile documenté)
→ GO exploitation démo
→ Prochaine étape : cadrage CK-HOME-001B ou dette SEO tunnel selon priorité MOA
```

---

*Note MOA — C-Kréyòl Marketone · Livraison explicative — 2 juillet 2026*
