# TICKET — Lot 6.3b Porte Kits & Coffrets (cadrage cadrage2)

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_LOT6_3B_PORTE_KITS_COFFRETS` |
| **Lot** | 6.3b — Porte **Kits & Coffrets** (cadrage MOA) |
| **Statut** | **Clôturé — GO cadrage MOA avec réserves** (2026-06-08) |
| **Priorité MOA** | **2e reprise front** post-6.3a |
| **Version cible module** | `19.0.18.0.0` (indicatif — après GO cadrage) |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | Lots 1–5 **GO** · 6.1 **GO** · 6.2 **GO** · 6.3a **GO clôture MOA** `19.0.17.0.0` · BO `19.0.16.0.0` **GO avec réserves** · ADR-034 **validé** |
| **Cadrage parent** | [`TICKET_LOT6_3_PORTE_PROMO_PACK.md`](./TICKET_LOT6_3_PORTE_PROMO_PACK.md) — § 6.3b |
| **ADR** | [ADR-034](../cadrage/DECISIONS.md#adr-034--arbitrage-architecture-cadrage2-socle-odoo-natif) · [ADR-005](../cadrage/DECISIONS.md#adr-005--dépendances-minimales-lot-1) · ADR-002 · ADR-003 · ADR-009 |
| **Contrats** | C2 · C3.1–C3.7 · **C3.E** (préparatoire) |
| **Arbitrage** | [`ARBITRAGE_ARCHITECTURE_CADRAGE2.md`](./ARBITRAGE_ARCHITECTURE_CADRAGE2.md) §5 · étape 9 |
| **Fiche MOA réunion** | [`FICHE_MOA_LOT6_3B_KITS_COFFRETS.md`](./FICHE_MOA_LOT6_3B_KITS_COFFRETS.md) |
| **Reprise front** | [`REPRISE_LOTS_FRONT_CADRAGE2.md`](./REPRISE_LOTS_FRONT_CADRAGE2.md) |
| **Clôture amont** | [`RECEPTION_MOA_LOT6_3A_PROMO.md`](./RECEPTION_MOA_LOT6_3A_PROMO.md) |

---

## En-tête recette obligatoire (ADR-034 · REPRISE §2)

```markdown
**ADR-034 :** [ARBITRAGE_ARCHITECTURE_CADRAGE2.md](./ARBITRAGE_ARCHITECTURE_CADRAGE2.md)

**Fonctionnalité Odoo native préservée :** Produits pack · Listes de prix · Vente eCommerce

**Mécanisme Odoo concerné :** product.template (pack_ok) · product_pack / product.pack.line · website_sale · (sale_product_pack si activé)

**Non-régression référence boutique :** [REFERENCE_RECETTE_BOUTIQUE_MOA.md](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) — sections B1 · B2 · B3 · B4 · B6 · B7
```

> Recette détaillée : [`RECETTE_MANUELLE_LOT6_3B_PACK.md`](../recette/lots/RECETTE_MANUELLE_LOT6_3B_PACK.md) — **GO clôture MOA**.

---

## Objectif MOA

Définir comment Marketone **expose** la porte **Kits & Coffrets** en s’appuyant sur les **mécanismes standards Odoo** (module OCA `product_pack` si validé), sans créer de moteur pack parallèle côté Marketone.

```text
Le front peut présenter, orienter et mettre en avant les kits/coffrets vendables.
La composition, le stock et la vérité prix restent Odoo (product_pack + pricelist).
Aucun moteur pack / prix parallèle côté Marketone.
```

**Hors périmètre cadrage** : implémentation code · recette navigateur · ticket exécution (ouverts **après** GO cadrage MOA).

---

## Doctrine applicable

| Principe | Application Lot 6.3b |
|----------|----------------------|
| **Odoo exécute. Marketone habille et oriente.** | Porte = query `/shop` + présentation QWeb · filtre = hook `_search_get_detail` |
| **ADR-002** | `website_sale` souverain pour prix affichés, panier, checkout |
| **ADR-034** | Interdiction moteur pack/prix Marketone · pas de liste composants codée en dur |
| **ADR-005** | `product_pack` = dépendance **optionnelle** — activation **par décision MOA explicite** (→ ADR-035) |
| **C3.1–C3.2** | Filtre via `_search_get_detail` — **pas** de domaine QWeb |
| **C3.4** | Priorité modes : **pack > promo > featured > origin > collection** |
| **C3.6** | **Un seul** `marketone_mode` actif par requête |
| **C3.7** | Filtres natifs sidebar **conservés** |

---

## Héritage décisions MOA (cadrage parent — figées)

| # | Décision | Statut |
|---|----------|--------|
| **M1** | 6.3a Promo seul · 6.3b Kits & Coffrets = lot séparé | ✓ **Clôturé** (6.3a GO MOA) |
| **M4** | Libellé visiteur : **Kits & Coffrets** — « Pack » = terme technique/interne | ✓ Figé |
| **M5** | Chip header **Promotions** livré en 6.3a · chip **Kits & Coffrets** livré en 6.3b | ✓ Clôturé |
| **M6** | SEO canonical : note documentaire · implémentation = ticket SEO séparé | ✓ Figé |

---

## Interdictions explicites (MOA · ADR-034)

| Interdit | Raison |
|----------|--------|
| Champ « est un kit » custom Marketone sur `product.template` | Double vérité — utiliser `pack_ok` natif |
| Table ou modèle `marketone.pack.*` | Moteur parallèle |
| Liste composants codée en dur (IDs produits) | Non maintenable · bypass `product_pack` |
| Filtre porte pack = **seule** catégorie « Kits & Coffrets » sans `pack_ok` | Confusion catégorie éditoriale vs offre packagée réelle |
| Calcul prix pack en Python/JS front | Odoo pricelist + règles pack natives |
| Route catalogue autonome `/kits` (hors alias **301**) | C2 conteneur `/shop` unique |
| Tunnel checkout / panier custom | ADR-002 |
| Refonte Palier B2 complète « Tout · Promo · Kits · … » | Ticket UX séparé |

---

## Source de vérité proposée (C3.E)

| Critère | Règle proposée Dev |
|---------|-------------------|
| Produit éligible porte | `product.template.pack_ok = True` |
| Publication site | `sale_ok` + `is_published` / visibilité eCommerce standard |
| Composants | Résolution **native** `product.pack.line` — affichage fiche selon options pack OCA |
| Prix affiché grille / fiche | **Pricelist Odoo** + comportement natif `website_sale` — pas de prix pack Marketone |
| Catégorie principale | **Kits & Coffrets** recommandée pour les vrais coffrets (mapping MOA) — **complément** à `pack_ok`, pas substitut |

> **Distinction MOA** : un produit peut avoir la catégorie principale « Kits & Coffrets » sans être un pack OCA (`pack_ok=False`) — il **n’apparaît pas** sur la porte pack. Inversement : `pack_ok=True` **doit** apparaître sur la porte même si la catégorie principale est autre (cas limite à éviter en BO).

---

## Comportement `/shop` proposé

| Élément | Proposition Dev |
|---------|-----------------|
| Canonique | `/shop?marketone_mode=pack` |
| Alias 301 | `GET /kits` → **301** → `/shop?marketone_mode=pack` (legacy marketplace · C2.4) |
| Filtre grille | Option `marketone_pack_only=True` → `_search_get_detail` → `[('pack_ok', '=', True)]` |
| État vide | 200 + message sobre — **pas** 404 · **pas** 500 |
| Présentation | Titre **Kits & Coffrets** · intro courte · lien « Tous les produits » → `/shop` |
| Chip header | Lien **Kits & Coffrets** → `/kits` (301) — pattern chip Promotions 6.3a |
| Priorité modes | Si `pack` + `promo` cumulés en query → **pack** gagne (C3.4) — tests explicites |

---

## Dépendances OCA — état technique (Dev · 2026-06-08)

Modules présents dans le dépôt `odoo19-addons-oca/` :

| Module | Version | `installable` | Rôle |
|--------|---------|---------------|------|
| **`product_pack`** | `19.0.1.0.2` | **True** | Champ `pack_ok` · lignes composants BO · pricelist pack |
| **`sale_product_pack`** | `19.0.1.0.0` | **False** | Explosion lignes commande vente · stock composants |

> **Point d’attention MOA** : sans `sale_product_pack` installable, la porte front filtre et vend le **produit pack** via `website_sale` standard ; le comportement **backend** (explosion composants, réservation stock composants) reste hors v1.

**Recommandation Dev pré-cadrage** : viser **`product_pack` minimum** pour la porte catalogue ; traiter **`sale_product_pack`** (port 19.0 ou alternative) comme **prérequis vente/stock** si MOA exige la gestion composants en commande.

---

## Grille d’impacts métier — à valider MOA

Analyse demandée par **M2** (reportée depuis cadrage parent) avant GO exécution :

### Vente

| Question | Enjeu | Options MOA |
|----------|-------|-------------|
| **K-V1** | Ajout panier eCommerce | Produit pack = **une ligne** panier (standard) vs explosion composants visible visiteur |
| **K-V2** | Prix pack au checkout | Pricelist Odoo seule · options `pack_component_price` OCA (detailed / totalized / ignored) |
| **K-V3** | Dépendance `sale_product_pack` | **Obligatoire** vs **reportée** si non installable 19.0 |

### Stock

| Question | Enjeu |
|----------|-------|
| **K-S1** | Mouvement stock | Pack seul vs décrément composants — comportement natif Odoo + OCA |
| **K-S2** | Disponibilité grille | Afficher pack indisponible si composant manquant ? (comportement Odoo standard) |

### Préparation / logistique

| Question | Enjeu |
|----------|-------|
| **K-P1** | Bon de préparation | Picking pack vs picking composants |
| **K-P2** | Étiquetage expédition | Coffret présenté comme unité visuelle unique (OK MOA pilote) |

### Facturation

| Question | Enjeu |
|----------|-------|
| **K-F1** | Lignes facture | Alignement avec options pack OCA · pas de ligne Marketone custom |

### UX / BO

| Question | Enjeu |
|----------|-------|
| **K-U1** | Fiche produit site | Afficher liste composants ? (pack **detailed** vs **non_detailed**) |
| **K-U2** | BO recette | Quels produits pilote configurer en `pack_ok=True` ? (voir § jeu recette) |
| **K-U3** | Cohérence catégories | Règle mapping **Kits & Coffrets** + `pack_ok` — formation MOA BO |

---

## Décisions MOA tranchées (cadrage GO 2026-06-08)

| # | Question | Verdict MOA |
|---|----------|-------------|
| **K1** | Activer **`product_pack`** dans le manifest Marketone | ☑ **Oui** |
| **K2** | Activer **`sale_product_pack`** (vente composants) | ☑ **Non en v1** — report OCA |
| **K3** | Source filtre porte **`pack_ok=True` uniquement** | ☑ **Validé** |
| **K4** | Chip header **Kits & Coffrets** | ☑ **Oui** |
| **K5** | Libellé porte **Kits & Coffrets** | ☑ **Validé** |
| **K6** | Composants fiche = **natif OCA** · aucun widget Marketone | ☑ **Validé** |
| **K7** | État vide porte | ☑ **Validé** |
| **K8** | Non-régression 6.1 / 6.2 / 6.3a + panier | ☑ **Validé** |
| **K9** | **ADR-035** | ☑ **Acceptée MOA** |

**Réserve MOA** : v1 sans explosion composants vente/stock/préparation/facturation — [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md).

**Décision MOA** : [`DECISION_MOA_LOT6_3B_KITS_COFFRETS.md`](./DECISION_MOA_LOT6_3B_KITS_COFFRETS.md)

---

## Décisions MOA à trancher (cadrage 6.3b) — archivé

| # | Question | Proposition Dev | Verdict MOA |
|---|----------|-----------------|-------------|
| **K1** | Activer **`product_pack`** dans le manifest Marketone ? | **Oui** — condition sine qua non porte pack réelle | ☑ Oui |
| **K2** | Activer **`sale_product_pack`** (vente composants) ? | **Oui** si installable 19.0 · sinon ticket port OCA préalable | ☑ Non en v1 |
| **K3** | Source filtre porte | **`pack_ok=True` uniquement** (recommandé C3.E) | ☑ Validé |
| **K4** | Chip header **Kits & Coffrets** | **Oui** — lien `/kits` · symétrie Promotions | ☑ Oui |
| **K5** | Libellé porte | **Kits & Coffrets** (héritage M4) | ☑ Validé |
| **K6** | Fiche produit — composants visibles | **Natif OCA** selon `pack_type` BO — Marketone n’ajoute pas de widget custom | ☑ Validé |
| **K7** | État vide porte | Message sobre + grille vide (pattern 6.3a P4) | ☑ Validé |
| **K8** | Non-régression portes 6.1 / 6.2 / 6.3a | Obligatoire — smoke REFERENCE B1–B7 | ☑ Validé |
| **K9** | ADR-035 | Rédiger si **K1=Oui** — amendement ADR-005 | ☑ Acceptée MOA |

---

## Jeu recette proposé (indicatif — après GO cadrage)

Produits candidats déjà mappés catégorie **Kits & Coffrets** sur le pilote 50 SKU :

| Produit | Rôle recette suggéré |
|---------|---------------------|
| Coffret biscuits et douceurs | Pack **A** — visible porte |
| Coffret gourmand îles créoles | Pack **B** — visible porte |
| Assortiment apéritif créole | Pack **C** — si MOA valide lot packagé |
| Trio sirops des Antilles | Pack **D** — si MOA valide trio packagé |
| Maniocookies salés La Platine | **Hors porte** — produit unitaire |

**Préparation Dev** (post-GO cadrage) : script `prep_recette_lot6_3b_pack.py` — configurer `pack_ok` + lignes composants sur 2–4 produits · laisser ≥ 1 produit unitaire publié.

---

## Non-régression obligatoire

| Document | Sections |
|----------|----------|
| [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) | **B1** smoke · **B2** compteur/chips · **B3** sidebar · **B4** tuiles · **B6** portes existantes · **B7** UX-4 |
| Porte 6.3a Promo | `/promotions` · mode promo inchangé |
| Portes 6.1 / 6.2 | `/incontournables` · `/origines` · modes featured / origin |
| Priorité modes | `pack` > `promo` > `featured` — tests cumul query |
| Panier / checkout | Smoke Lot 5 — prix panier = moteur Odoo |

---

## Note de livraison (exécution — phrase obligatoire)

```text
Aucun moteur Odoo remplacé — les kits et coffrets s’appuient sur product_pack
(pack_ok, composants natifs) et les listes de prix Odoo.
Marketone présente et filtre la grille /shop uniquement.
```

---

## Hors périmètre Lot 6.3b

- Coupons `sale_loyalty` · programmes fidélité
- Refonte chips header Palier B2 (Tout · Promo · Kits · …)
- SEO canonical / noindex implémenté (ticket MOA SEO)
- BO custom « gestion kits CK » hors `product_pack` standard
- Pages catalogue autonomes hors `/shop`
- Modification tunnel checkout / code promo saisie checkout
- Résolution composants dans **collections** sidebar (ADR D3 — ticket séparé)

---

## Critères GO cadrage (avant ticket exécution)

- [x] **K1–K9** tranchées MOA (2026-06-08)
- [x] Grille impacts **K-V / K-S / K-P / K-F / K-U** validée · réserve `sale_product_pack` documentée
- [x] Décision **`product_pack`** actée · **`sale_product_pack` hors v1**
- [x] **ADR-035** acceptée MOA — [`DECISIONS.md`](../cadrage/DECISIONS.md#adr-035--activation-product_pack-lot-63b-kits--coffrets)
- [x] Contrat **C3.E** mis à jour (`CONTRACTS.md`) — **figé exécution**
- [x] Ticket exécution [`TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md) — **livré Dev `19.0.18.0.0`**

---

## Critères GO exécution (indicatif)

```text
/kits → 301 → /shop?marketone_mode=pack
Grille = produits pack_ok publiés uniquement · prix affichés = Odoo natif
Chip header Kits & Coffrets visible · pas de régression Promotions / Incontournables / Origines
Portes 6.1 / 6.2 / 6.3a / sidebar / panier : non-régression
Tests auto lot6_3b verts · recette MOA signée
Note livraison : « aucun moteur Odoo remplacé »
```

---

## Extension code attendue (indicatif — après GO cadrage)

| Couche | Fichier / objet |
|--------|-----------------|
| Manifest | `depends` + **`product_pack`** *(+ `sale_product_pack` si K2)* |
| Modèle | `product.template._search_get_detail` — branche `marketone_pack_only` |
| Contrôleur | `WebsiteSale` — mode `pack` · alias `/kits` · priorité C3.4 |
| QWeb | `views/pages/shop_pack.xml` · chip header `header.xml` |
| Tests | Tag `dorevia_marketone_lot6_3b_pack` |
| Docs | `RECETTE_MANUELLE_LOT6_3B_PACK.md` · `PREP_RECETTE_LOT6_3B_PACK.md` |

Pattern de référence : [`TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md) · livraison `19.0.17.0.0`.

---

## Références

| Document | Rôle |
|----------|------|
| [`CONTRACTS.md`](../cadrage/CONTRACTS.md) § C3.E | Contrat porte Kits & Coffrets |
| [`TICKET_LOT6_3_PORTE_PROMO_PACK.md`](./TICKET_LOT6_3_PORTE_PROMO_PACK.md) | Cadrage parent · § 6.3b |
| [`RECEPTION_MOA_LOT6_3A_PROMO.md`](./RECEPTION_MOA_LOT6_3A_PROMO.md) | Clôture amont 6.3a |
| [`MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md`](../cadrage/MAPPING_CATEGORIES_PRINCIPALES_RECETTE.md) | Règle Kits & Coffrets |
| [`TAXONOMIE_CATALOGUE.md`](../cadrage/TAXONOMIE_CATALOGUE.md) | Distinction pack vs collection |
| `odoo19-addons-oca/product_pack/` | Module OCA — `pack_ok` |
| `odoo19-addons-oca/sale_product_pack/` | Module OCA vente — **non installable** au 2026-06-08 |

---

## Verdict MOA cadrage

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-06-08 | ☑ **GO cadrage avec réserves** | K1–K9 validés · ADR-035 acceptée · réserve `sale_product_pack` → ticket OCA |

**Statut post-recette** : [`RECETTE_MANUELLE_LOT6_3B_PACK.md`](../recette/lots/RECETTE_MANUELLE_LOT6_3B_PACK.md) signée · clôture [`RECEPTION_MOA_LOT6_3B_PACK.md`](./RECEPTION_MOA_LOT6_3B_PACK.md) **GO MOA**.
