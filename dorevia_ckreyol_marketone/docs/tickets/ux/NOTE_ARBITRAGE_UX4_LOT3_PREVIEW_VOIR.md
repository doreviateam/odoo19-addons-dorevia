# Note d’arbitrage MOA — UX-4 Lot 3 · Preview « Voir sans sortie »

| Champ | Valeur |
|-------|--------|
| **Statut** | **Validé MOA** — **GO avec réserve documentaire** (2026-05-22) |
| **Date** | 2026-05-22 |
| **Prérequis** | Lots 1–2 **clôturés GO avec réserve** · version réf. **`19.0.15.12.3`** |
| **Ticket** | [`TICKET_MARKETONE_UX4_SHOP_IN_PLACE.md`](TICKET_MARKETONE_UX4_SHOP_IN_PLACE.md) |
| **Recette cible** | § Lot 3 [`RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md`](../recette/ux/RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md) · critères **B9–B10** |
| **Objectif** | Permettre un **GO / NO GO / GO avec réserve** MOA **avant** toute ouverture de branche |

---

## 1. Contexte et doctrine MOA rappelée

Le socle `/shop` est stabilisé pour les actions **wishlist** (Lot 1) et **panier** (Lot 2) **sans sortie de page**. Le Lot 3 porte uniquement le CTA **« Voir »** de la tuile conversion.

**Orientations MOA actuelles (non négociables pour ce lot) :**

- ne pas transformer `/shop` en mini-application e-commerce complète ;
- conserver la **fiche produit** comme destination **complète** (SEO, variantes, contenu long) ;
- déclencher la preview **uniquement** via le CTA **« Voir »** ;
- **photo et titre** de la tuile restent des **liens standard** vers la fiche produit ;
- **pas de modal popup** (overlay bloquant type dialog).

**État actuel du CTA « Voir »** (post Lots 1–2) :

```xml
<a t-att-href="product_href" class="marketone-shop-card-cta">Voir</a>
```

→ navigation fiche produit, conforme au gel MOA photo/titre mais **hors doctrine UX-4** sur le CTA premier niveau « Voir ».

---

## 2. Synthèse recommandation Dev (sans engagement d’implémentation)

| Question | Recommandation provisoire | Confiance |
|----------|---------------------------|-----------|
| Preview vs fiche | **Preview in-page** sur clic « Voir » | Forte |
| Desktop | **Offcanvas latéral droit non modal** (Bootstrap / Odoo 19) | Forte |
| Mobile | **Bloc inline sous la tuile** (accordéon / expand) | Moyenne–forte |
| Photo / titre | **Maintenus** comme liens fiche | Forte (gel MOA) |
| Contenu minimal | Liste § 5 ci-dessous | Forte |
| Variantes | **Preview simple** si variante unique · **fallback fiche** si configurable | Forte |
| Verdict arbitrage | **GO avec réserve** — sous conditions § 8 | — |

---

## 3. Réponses aux questions MOA

### 3.1 — CTA « Voir » : preview in-page ou maintien fiche produit ?

| Option | Description | Pour | Contre |
|--------|-------------|------|--------|
| **A — Preview in-page** | Clic « Voir » → chargement fragment HTML · URL reste `/shop` | Aligné UX-4 · complète Lots 1–2 · comparaison produits sans rupture | JS + route dédiée · recette B9 |
| **B — Maintien fiche** | Statu quo · lien `product_href` | Zéro dev · SEO direct | Doctrine UX-4 non tenue · CTA 1er niveau encore éjectant |

**Recommandation : option A (preview in-page).**

La fiche produit reste accessible via **photo**, **titre** et lien secondaire **« Voir la fiche complète »** dans la preview — pas de remplacement de la fiche, seulement un **interstitiel léger** déclenché par « Voir ».

---

### 3.2 — Desktop : panneau latéral droit non modal — faisabilité et risques ?

**Faisabilité : oui**, avec l’écosystème déjà présent :

- Odoo 19 / Bootstrap 5 : composant **offcanvas** (`offcanvas-end`) ;
- pattern déjà utilisé côté boutique pour l’**offcanvas sidebar mobile** (UX-2) ;
- chargement **fragment HTML** via route dédiée (cf. ticket : `/shop/product/preview/<template_id>`) + injection dans le panneau.

**Comportement cible desktop :**

```text
[ Grille /shop visible ]  |  [ Panneau preview ~360–420 px ]
                          |  image · titre · prix · origine
                          |  description courte · CTA panier/wishlist
                          |  lien « Voir la fiche complète » · [×]
```

| Risque | Niveau | Mitigation proposée |
|--------|--------|---------------------|
| Conflit z-index (header, sidebar, panier survol) | Moyen | Scope SCSS `.marketone-shop-preview` · z-index documenté · recette visuelle B4 |
| Scroll body / focus piégé | Moyen | Offcanvas **non modal** (`backdrop: false` ou équivalent) · fermeture ESC · `aria-modal="false"` |
| Grille compressée / CLS | Faible | Panneau **superposé** (overlay latéral) plutôt que reflow colonne |
| Double handler JS (WebsiteSale) | Moyen | Interaction dédiée sur `.marketone-shop-card-cta` · `preventDefault` · pas de `a-submit` |
| Performance (N produits) | Faible | Un seul panneau réutilisé · fetch à la demande |

---

### 3.3 — Mobile : bloc inline sous carte ou panneau bas ?

| Option | Description | Pour | Contre |
|--------|-------------|------|--------|
| **A — Inline sous tuile** | Expand / accordéon sous la carte cliquée | Pas de second calque · scroll naturel · moins « app-like » · a11y simple | Saut de layout · une seule preview ouverte recommandée |
| **B — Panneau bas (bottom sheet)** | Offcanvas bottom | Gestuelle familière | Proche d’une modal · plus de JS · risque confusion avec offcanvas filtres |
| **C — Même offcanvas end qu’desktop** | Panneau droit étroit | Un seul template | Peu lisible · largeur insuffisante 390 px |

**Recommandation : option A (bloc inline sous tuile)** en mobile, **option desktop offcanvas end** — cohérent avec la spec recette L3.2 / L3.3 et avec la doctrine « ne pas mini-app ».

**Règle UX :** une seule preview ouverte à la fois ; re-clic « Voir » ou clic ailleurs → replie.

---

### 3.4 — Photo et titre : maintien liens fiche produit complète ?

**Recommandation : oui — confirmer le gel MOA.**

| Zone tuile | Comportement Lot 3 | Rôle |
|------------|-------------------|------|
| **Photo** | Lien `product_href` (inchangé) | Destination complète · SEO · habitudes utilisateur |
| **Titre h2** | Lien `product_href` (inchangé) | Idem |
| **CTA « Voir »** | Preview in-page (nouveau) | Exploration rapide sans quitter `/shop` |

Cette séparation est **volontaire** : la preview est un **raccourci**, pas le seul chemin vers la fiche. Recette **L3.5** et **B10** couvrent la non-régression.

---

### 3.5 — Contenu minimal de la preview

| Bloc | Source données (existant) | Disponibilité catalogue CK | Note |
|------|---------------------------|----------------------------|------|
| **Image** | `product._get_images()` / variante | ✅ | Même doctrine image v2 que la tuile |
| **Titre** | `product.name` | ✅ | — |
| **Prix** | `get_product_prices(product)` (website_sale) | ✅ | Cohérent tuile |
| **Origine** | `_marketone_get_origin_shop_lines()` | ✅ si attribut Origines | Déjà sur fiche · liens porte optionnels |
| **Collection** | `public_categ_ids` · portes Collections si mappées | ✅ partiel | Affichage **label seul** en V1 · pas de filtre depuis preview |
| **Description courte** | `description_sale` | ✅ | Absente de la tuile · pertinente en preview |
| **Bouton panier** | Réutilisation Lot 2 (`marketone_shop_cart_add` ou fragment QWeb) | ✅ | PTAV origine à transmettre (leçon `12.3`) |
| **Bouton wishlist** | Réutilisation Lot 1 (`marketone_shop_wishlist_toggle`) | ✅ | — |
| **Lien « Voir la fiche complète »** | `product_href` | ✅ | CTA secondaire explicite · **B10** |

**Hors V1 preview (explicitement) :**

- configurateur variantes complet ;
- avis clients / onglets fiche ;
- cross-sell / optional products ;
- contenu Culture / Savoirs long format.

---

### 3.6 — Produits à variantes : preview simple ou fallback fiche ?

**Constat catalogue Marketone (recette `ckr-marketone-01`) :**

- majorité des produits publiés : **1 variante** + attribut **Origines** en `no_variant` (valeur unique) ;
- cas multi-variantes : **minoritaires** mais possibles (évolution catalogue).

**Règle proposée V1 :**

| Condition produit | Comportement « Voir » |
|-------------------|----------------------|
| `product_variant_count == 1` et pas d’attribut stocké configurable | **Preview complète** (contenu § 3.5) |
| `product_variant_count > 1` **ou** attributs `always` / configurateur requis | **Fallback fiche produit** (`product_href`) **ou** preview **dégagée** + bandeau « Choisir les options sur la fiche complète » |

**Recommandation : fallback fiche** pour les produits configurables — évite un demi-configurateur dans la preview (dette + régression panier).

Alternative **GO avec réserve** : preview statique (image, titre, prix, origine, description) **sans** bouton panier si variante non résolue.

---

### 3.7 — Risques

| Risque | Niveau | Impact | Mitigation |
|--------|--------|--------|------------|
| **Régression tuile conversion (B4)** | Élevé | Layout Voir/prix/panier/wishlist | Lot 3 limité au handler « Voir » · recette conversion tile rejouée |
| **JS `website_sale` / Interactions Odoo 19** | Moyen | Double submit · conflits cart/wishlist | Interaction isolée · réutiliser services Lots 1–2 · tests `dorevia_marketone_shop_in_place` |
| **Accessibilité** | Moyen | Focus, ESC, lecteurs d’écran | Offcanvas non modal · `aria-expanded` sur « Voir » · focus trap **léger** (pas modal) · recette clavier |
| **Mobile 390 px** | Moyen | Débordement · scroll | Pattern inline · tests viewport · reprise leçon Lot 2 mobile |
| **Dette technique** | Moyen | Deux chemins d’achat (tuile vs preview) | Fragment QWeb unique · pas de modèle Python · route read-only |
| **SEO** | Faible | Liens photo/titre conservés | Pas de remplacement des URLs fiche |
| **Scope creep** | Élevé | Mini-app / modal / configurateur | Checklist hors périmètre § 4 · gel contenu V1 |

---

## 4. Périmètre proposé Lot 3 (si GO MOA)

### In

- Interaction JS preview sur `.marketone-shop-card-cta` uniquement ;
- Route fragment HTML `/shop/product/preview/<product_template_id>` ;
- QWeb preview + SCSS scoped `.marketone-shop-preview` ;
- Desktop : offcanvas end non modal ;
- Mobile : expand sous tuile ;
- Réutilisation handlers panier (Lot 2) et wishlist (Lot 1) dans le fragment ;
- Tests tag `dorevia_marketone_shop_in_place` · recette B9–B10 ;
- Mise à jour [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) § B9.

### Hors périmètre (V1)

- Modal popup ;
- changement comportement **photo** / **titre** ;
- configurateur variantes dans preview ;
- deep-link preview partageable (URL `/shop` + query optionnelle en **V2** seulement) ;
- preview depuis autre CTA que « Voir » ;
- refonte fiche produit / page wishlist / panier.

---

## 5. Architecture légère envisagée (information seulement)

```text
Clic « Voir » (.marketone-shop-card-cta)
    → preventDefault
    → GET /shop/product/preview/<template_id>
    → inject HTML dans offcanvas (desktop) ou bloc sous tuile (mobile)
    → panier / wishlist : interactions Lots 1–2 sur le fragment injecté

Photo / titre tuile : inchangés → product_href
Preview : lien « Voir la fiche complète » → product_href
```

**Estimation complexité relative :** comparable au Lot 2 (interaction + QWeb + route) · **supérieure** au Lot 1 (deux layouts desktop/mobile · gestion ouverture/fermeture).

---

## 6. Critères GO MOA Lot 3 proposés

| # | Critère |
|---|---------|
| G3.1 | Clic « Voir » : preview visible · **URL `/shop`** (query/hash acceptés, pas navigation fiche) |
| G3.2 | Desktop : panneau latéral droit · grille reste visible · **pas modal** |
| G3.3 | Mobile : preview sous tuile · pas de débordement horizontal 390 px |
| G3.4 | Photo + titre tuile : navigation fiche **inchangée** |
| G3.5 | Contenu minimal § 3.5 présent |
| G3.6 | Panier + wishlist depuis preview · comportement aligné Lots 1–2 |
| G3.7 | Lien « Voir la fiche complète » fonctionnel |
| G3.8 | Fermeture preview (× / ESC / re-clic) sans erreur JS |
| G3.9 | Régression B1 · B4 · B7 · B8 · B10 OK |
| G3.10 | Tests auto + recette § Lot 3 documentée |

---

## 7. Options de décision MOA

| Décision | Signification | Conditions |
|----------|---------------|------------|
| **GO Lot 3** | Ouverture branche autorisée | Acceptation périmètre § 4 · architecture § 5 · critères § 6 |
| **GO avec réserve** | Branche autorisée · arbitrage mobile ou variantes à préciser | Réserve documentée (ex. fallback variantes · L3.C1 connecté) |
| **NO GO Lot 3** | Gel maintenu · « Voir » reste lien fiche | Doctrine UX-4 partielle · Lots 1–2 seuls |
| **Pause prolongée** | Pas de branche · note validée | Statut actuel jusqu’à nouvel arbitrage |

---

## 8. Recommandation Dev pour arbitrage MOA

**Proposition : GO avec réserve documentaire** — sous réserve MOA explicite sur :

1. **Mobile inline** (vs bottom sheet) — recommandation inline ;
2. **Fallback fiche** pour produits multi-variantes / configurables en V1 ;
3. **Pas de deep-link** preview en V1 (option V2 si besoin analytics).

**Arguments pour :**

- complète la doctrine UX-4 sans contredire le gel photo/titre ;
- s’appuie sur les patterns Odoo 19 déjà maîtrisés (offcanvas, Interactions, fragments) ;
- réutilise Lots 1–2 (pas de nouveau moteur panier/wishlist) ;
- contenu preview **déjà disponible** côté données Marketone (origine, prix, description_sale).

**Arguments de prudence :**

- seul lot avec **deux UX distinctes** desktop/mobile ;
- risque régression tuile **B4** plus élevé que Lots 1–2 ;
- tentation scope creep si le preview grossit (→ respect strict § 4).

**Si NO GO :** le chantier UX-4 reste **GO partiel** (Lots 1–2) · « Voir » continue vers fiche · acceptable MOA mais incohérent avec U1/U4 référence boutique.

---

## 9. Prochaines étapes (post-arbitrage MOA)

| Étape | Responsable | Statut |
|-------|-------------|--------|
| Verdict MOA sur cette note | MOA | ✅ **GO avec réserve documentaire** |
| Mise à jour statut ticket UX-4 Lot 3 | Dev | ✅ |
| Mise à jour recette § Lot 3 (G3.1–G3.10) | Dev | ✅ |
| Branche `feat/marketone-ux4-lot3-preview-voir` | Dev | Autorisée · à ouvrir |
| PR `[CK][UX-4] Lot 3 — Preview Voir sans sortie de /shop` | Dev | Tôt · merge après recette MOA |

---

## 10. Références

| Document | Lien |
|----------|------|
| Ticket UX-4 | [`TICKET_MARKETONE_UX4_SHOP_IN_PLACE.md`](TICKET_MARKETONE_UX4_SHOP_IN_PLACE.md) |
| Recette UX-4 Lot 3 | [`RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md`](../recette/ux/RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md) § Lot 3 |
| Référence boutique B9–B10 | [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) |
| Tuile conversion (B4) | [`RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md`](../recette/boutique/RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md) |
| Rapport Lot 2 GO | [`RAPPORT_RECETTE_SHOP_UX4_LOT2_IN_PLACE_20260522.md`](../recette/ux/RAPPORT_RECETTE_SHOP_UX4_LOT2_IN_PLACE_20260522.md) |

---

**Verdict MOA :** ☑ **GO avec réserve documentaire** · ☐ GO · ☐ NO GO · ☐ Pause prolongée

**Commentaire MOA :**

```text
GO avec réserve documentaire pour ouverture du Lot 3.

Conditions : périmètre strict V1 · pas de mini-app /shop · pas de modal popup · pas de
configurateur variantes dans preview · pas de deep-link preview V1 · photo/titre inchangés.

Arbitrages validés :
- CTA « Voir » → preview in-page · URL /shop · fiche complète en destination secondaire ;
- Desktop : panneau latéral droit non modal · grille visible · fermeture × / ESC / re-clic ;
- Mobile : preview inline sous tuile · une seule ouverte · pas de bottom sheet V1 · 390 px ;
- Contenu V1 : image · titre · prix · origine · collection/label · description courte ·
  panier · wishlist · lien « Voir la fiche complète » ;
- Variantes : fallback fiche obligatoire pour produits configurables / multi-variantes V1.

Branche autorisée : feat/marketone-ux4-lot3-preview-voir
PR cible : [CK][UX-4] Lot 3 — Preview Voir sans sortie de /shop
Pas de merge sans recette MOA desktop + mobile.
```

**Date arbitrage :** 2026-05-22

**Signataire MOA :** MOA C-Kreyol Marketone
