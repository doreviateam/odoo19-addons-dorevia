# TICKET — Lot 6.1 Porte Incontournables (cadrage) `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_LOT6_1_PORTE_INCONTOURNABLES` |
| **Lot** | 6.1 — **Cadrage uniquement** (pas de code) |
| **Statut** | **GO cadrage avec réserves légères** (2026-05-18) |
| **Type** | Ticket de cadrage / arbitrage |
| **Version cible module** | `19.0.6.0.0` (proposition, post-validation) |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | Lots 1–5 **GO** (socle e-commerce stabilisé, 2026-05-18) |
| **Contrats** | C1, C2, C3 (futur), C9 ; ADR-018 |
| **Référence legacy** | `dorevia_ckreyol_marketplace` — **inspiration**, pas copie |

---

## Objectif du cadrage

Préparer la **première porte catalogue** Marketone — **Incontournables** — sans implémenter de code dans ce ticket.

```text
Critère attendu (cadrage validé) :
Une première porte catalogue éditoriale peut orienter vers une sélection de produits
sans casser /shop, ni le moteur website_sale, ni le tunnel d’achat.
```

**Doctrine** (CONTRACTS C2–C3, ARCHITECTURE § Lot 6) :

```text
Les portes orientent.
Les filtres Odoo sélectionnent.
Marketone ne crée pas un moteur catalogue parallèle.
```

---

## Contexte — socle stabilisé (Lots 1–5)

| Étape | Route / scope | Statut |
|-------|---------------|--------|
| Accueil | `/` — `marketone-root` | GO |
| Boutique | `/shop` — `marketone-shop` | GO |
| Fiche produit | `/shop/<product>` — `marketone-product` | GO avec réserves |
| Panier | `/shop/cart` — `marketone-cart` | GO |
| Checkout invité | `/shop/checkout` → `/shop/address` — `marketone-checkout` | GO |

**Tests non-régression actuels** : **49/49** (`dorevia_marketone_smoke` … `lot5`).

**Ce ticket ne livre aucun fichier Python, XML, SCSS ni test.**

---

## Pourquoi la porte Incontournables en premier (MOA)

| Critère | Incontournables | Promotions | Kits/Packs |
|---------|-----------------|------------|------------|
| Cohérence éditoriale C-Kreyol | **Forte** (sélection) | Commerciale | Dépend `product_pack` |
| Risque métier | **Modéré** | Élevé (prix / promos) | Élevé (structure pack) |
| Dépendance module tiers | **Aucune** (si source Odoo standard) | Pricelist | `product_pack` |
| Test mécanique portes | **Oui**, sans moteur parallèle | Oui | Non retenu Lot 6.1 |

---

## Contraintes Lot 6.1 (non négociables)

| Contrainte | Application |
|------------|-------------|
| Pas de moteur catalogue parallèle | Filtre via hook `website_sale` (`_search_get_detail` / options contrôleur) |
| **Une seule porte** | Incontournables uniquement — pas promo, pack, origines, collections |
| Pas de `product_pack` | Hors périmètre |
| Pas de promotions | Hors périmètre |
| Pas de JS | QWeb + Python contrôleur minimal si validé |
| Pas de refonte `/shop` | Grille `website_sale` inchangée ; bandeau / titre **minimal** autorisé si MOA valide |
| Pas de rupture tunnel | Panier, checkout, fiche, home inchangés fonctionnellement |
| `website_sale` souverain | Panier, checkout, domaine produit natifs |
| Pas de cohabitation marketplace | **Interdit** `dorevia_ckreyol_marketplace` sur la même base (C11) |
| Pas de `request._ckr_*` | Pas d’état implicite sur `request` (ADR legacy) |

---

## Décisions à trancher (MOA + archi)

Chaque section propose des **options** et une **recommandation de cadrage** (non engageante tant que la case MOA n’est pas cochée).

---

### D1 — Nom du paramètre URL

| Option | Exemple | Pour | Contre |
|--------|---------|------|--------|
| **A — `marketone_mode`** | `/shop?marketone_mode=featured` | Aligné CONTRATS C2/C3 ; extensible Lots 6.2+ | Un paramètre par famille de portes |
| B — `mo_mode` | `/shop?mo_mode=featured` | Court | Moins lisible, hors convention doc |
| C — `marketone_gate` | `/shop?marketone_gate=incontournables` | Sémantique « porte » | Diverge de la matrice legacy / contrats |
| D — Paramètre dédié | `/shop?marketone_featured=1` | Isolement | Multiplie les clés URL (maintenance) |

**Valeur de mode proposée** : `featured` (legacy `ckr_mode=featured`) ou `incontournables` (lisible MOA).

| Sous-option | Valeur | Note |
|-------------|--------|------|
| D1a | `marketone_mode=featured` | **Recommandation cadrage** — cohérent CONTRATS, tests legacy |
| D1b | `marketone_mode=incontournables` | Libellé FR dans l’URL — SEO / partage |

**Décision MOA** : ☑ **`marketone_mode=featured`** — libellé visible : **Incontournables**

---

### D2 — Source de vérité de la sélection produits

La liste affichée sur `/shop?…` doit venir d’une **source explicite en BO**, pas d’IDs codés en dur.

| Option | Mécanisme | Pour | Contre |
|--------|-----------|------|--------|
| **A — Paramètre système + catégorie e-commerce publique** | `ir.config_parameter` → `product.public.category` | 100 % Odoo standard ; pas de modèle custom | Une seule catégorie « Incontournables » ; pas de dates de publication collection |
| B — Paramètre système + liste produits BO | `Many2many` sur `website` (4–N slots) | Éditorial fin, comme legacy homepage featured | Liste limitée ; pas une vraie « collection » scalable |
| C — Champ booléen produit | `product.template.is_marketone_featured` | Simple à filtrer | Pollution catalogue ; pas de groupe éditorial nommé |
| D — Tag produit (`product.tag`) | Tag « Incontournables » + filtre | Standard Odoo si module dispo | Vérifier disponibilité CE 19 ; sémantique tag ≠ sélection éditoriale |
| E — Modèle `marketone.shop.selection` minimal | M2M `product.template`, 1 enregistrement « Incontournables » | Proche legacy `ckr.shop.collection` sans importer marketplace | Nouveau modèle + ACL + écrans BO |
| F — Réutiliser `ckr.shop.collection` | Dépendance marketplace | Déjà en prod legacy | **Interdit** C11 — modules non cohabitants |

**Recommandation cadrage** : **Option A** (catégorie publique + param système) pour Lot 6.1 — surface minimale, zéro modèle Marketone si MOA accepte l’usage taxonomique. **Option E** si MOA exige une entité éditoriale nommée « Incontournables » distincte des catégories merchandising.

**Décision MOA** : ☑ **A** — `ir.config_parameter` → `product.public.category` « Incontournables »

---

### D3 — Catégorie publique Odoo (`product.public.category`)

| Question | Options |
|----------|---------|
| Utiliser une catégorie e-commerce ? | ☐ Oui · ☐ Non |
| Si oui — création | ☐ Catégorie dédiée « Incontournables » en BO recette · ☐ Catégorie existante : _______ |
| Produits | ☐ Un produit = une catégorie · ☐ Plusieurs catégories autorisées |
| Affichage sidebar | ☐ Conserver filtres natifs · ☐ Masquer facettes en mode porte (à trancher Lot 6.1 exécution) |

**Recommandation cadrage** : une catégorie **`Incontournables`** sur le site, produits recette rattachés en BO — pas de seed XML obligatoire (C10).

**Décision MOA** : ☑ Catégorie dédiée **Incontournables** · ☑ Multi-catégories produits · ☑ Filtres natifs Odoo **conservés** au Lot 6.1

---

### D4 — Tag ou champ produit existant

| Question | Réponse MOA |
|----------|-------------|
| Existe-t-il déjà un champ / tag « sélection » sur les produits recette ? | ☐ Oui : _______ · ☐ Non |
| Souhaite-t-on en créer un au Lot 6.1 ? | ☑ **Non** |
| Si tag : filtre AND avec `is_published` / `sale_ok` ? | ☐ Oui · ☐ Non |

**Recommandation cadrage** : **ne pas** introduire de champ custom au Lot 6.1 si **D2 = catégorie publique** suffit.

---

### D5 — Modèle collection custom Marketone

| Option | Description | Lot 6.1 |
|--------|-------------|---------|
| **Non** | Pas de `marketone.shop.collection` | **Recommandation** si D2 = catégorie publique |
| **Oui — minimal** | 1 record singleton « Incontournables », M2M produits, pas de `/collections/<slug>` | Si MOA refuse la catégorie comme porte éditoriale |
| **Report Lot 6.5** | Collections multi-slugs type legacy | Hors 6.1 |

**Décision MOA** : ☑ **Pas de modèle custom** — collections éditoriales avancées reportées

---

### D6 — URL d’entrée `/incontournables`

| Option | Comportement | Pour | Contre |
|--------|--------------|------|--------|
| **A — Alias 301** | `GET /incontournables` → **301** → `/shop?marketone_mode=featured` | SEO, bookmarks, legacy | Route contrôleur supplémentaire |
| B — Pas d’alias | Lien direct vers `/shop?…` uniquement | Minimal | Pas de raccourci mémorable |
| C — Page autonome | `/incontournables` rend une page hors `/shop` | — | **Rejeté** — viole conteneur unique `/shop` (C2) |

**Recommandation cadrage** : **Option A** (301), aligné legacy et `TICKET_MARKETONE_LOT0_CADRAGE` matrice portes.

**Décision MOA** : ☑ **A** — `/incontournables` → **301** → `/shop?marketone_mode=featured`

---

### D7 — URL canonique et partage

| Règle | Proposition |
|-------|-------------|
| Canonique | `/shop?marketone_mode=featured` (ou valeur D1 retenue) |
| Paramètres inconnus | Ignorés silencieusement (C3.3) |
| Multi-valeurs `marketone_mode` | Priorité déterministe — seul `featured` actif au Lot 6.1 |
| Conflit futur multi-portes | Priorité legacy : `pack > promo > featured > …` (C3.4) — **inactif** tant qu’une seule porte |

**Décision MOA** : ☑ Canonique `/shop?marketone_mode=featured` · ☑ Un seul mode actif · ☑ Paramètres inconnus ignorés

---

### D8 — Alias 301 et SEO

| Question | Proposition |
|----------|-------------|
| Code HTTP | **301** permanent (legacy) |
| `rel=canonical` sur `/shop` filtré | Pointe vers URL canonique **avec** paramètre porte (à valider SEO MOA) |
| Indexation | ☐ `noindex` sur URL paramétrée · ☐ indexation normale |

**Décision MOA** : ☑ **301** permanent `/incontournables` · SEO `canonical` / `noindex` : **documenter** sans élargir l’exécution

---

### D9 — Affichage sur `/shop` (présentation)

Sans refonte grille. Extensions **présentation** possibles sous `.marketone-shop` :

| Niveau | Contenu | Charge |
|--------|---------|--------|
| **Minimal** | Titre H1 « Incontournables » + intro courte + lien « Tous les produits » | **Retenu MOA** |
| Intermédiaire | + fil d’Ariane | Optionnel |
| Élevé | Bandeau hero, chips multi-portes, sidebar portes | **Hors 6.1** — risque refonte |

| Question | MOA |
|----------|-----|
| Bandeau hero / chips / Explorer ? | ☑ **Non** |
| Message si sélection vide ? | À préciser au ticket exécution (défaut : 200 + message + lien `/shop`) |

**Décision MOA** : ☑ Niveau **minimal** — pas de hero, pas de chips multi-portes, pas de refonte grille

---

### D10 — Implémentation technique (orientation, pas livrée au cadrage)

À valider avant ticket d’exécution :

| Couche | Intention |
|--------|-----------|
| Contrôleur | Héritage `WebsiteSale` — lecture param whitelisté, injection **options** recherche |
| Recherche | `product.template._search_get_detail` (Odoo 19) — **pas** de domaine QWeb |
| État | **Pas** de `request._marketone_*` ; options explicites |
| QWeb | Micro-héritage `website_sale.products` — titre / intro **si** D9 > minimal |
| SCSS | Sous `.marketone-shop` uniquement |
| Tests | Tag `dorevia_marketone_lot6_1_featured` (proposition) |

---

### D11 — Tests de non-régression exigés (post-implémentation)

| # | Test | Attendu |
|---|------|---------|
| R1 | `/shop?marketone_mode=featured` (ou valeur retenue) | 200, grille ⊆ sélection BO |
| R2 | Scope CSS | Toujours `marketone-shop` sur `/shop` |
| R3 | `/shop` sans param | Inchangé (grille complète) |
| R4 | `/incontournables` si D6=A | 301 → canonique |
| R5 | Param inconnu | Ignoré, `/shop` standard |
| R6 | Fiche produit hors sélection | Non listée en mode porte |
| R7 | Produit dans sélection | Listé, fiche + panier OK |
| R8 | Panier / checkout | 200, scopes `marketone-cart` / `marketone-checkout` |
| R9 | Home | `marketone-root`, pas de porte |
| R10 | Suite auto | 49 tests Lots 1–5 + tests lot6.1 verts |

---

### D12 — Régression panier / checkout (critère bloquant)

```text
Toute implémentation Lot 6.1 doit laisser inchangé le parcours validé Lot 5 :
fiche → panier → /shop/cart → checkout → /shop/address.
```

Recette manuelle courte obligatoire en fin de Lot 6.1 (extension `RECETTE_MANUELLE` ou fiche dédiée).

---

## Hors périmètre Lot 6.1

| Exclusion | Report |
|-----------|--------|
| Portes Promotions, Kits, Origines, Collections, Catégories | Lots 6.2+ |
| `product_pack`, pricelist promo | Lot 6.x dédiés |
| Routes `/collections`, `/collections/<slug>` | Lot collections |
| Homepage carousel « featured » (4 produits) | Ticket home éditorial séparé |
| JS, wishlist, portes multiples simultanées | Interdit |
| Dépendance `dorevia_ckreyol_marketplace` | Interdit C11 |
| Seed XML production | C10 |

---

## Référence legacy (lecture seule)

| Élément legacy | Comportement | Reprise Marketone ? |
|----------------|--------------|---------------------|
| `ckr_mode=featured` | Mode commercial chip + filtre | ☑ `marketone_mode=featured` |
| `featured_collection_id` | Param → `ckr.shop.collection` | ☑ Remplacé par catégorie publique + param système |
| `/incontournables` → 301 | Vers `/shop?ckr_mode=featured` | ☑ Vers `/shop?marketone_mode=featured` |
| Bandeau `ckr_shop_featured_banner` | QWeb lourd | ☐ Non — minimal D9 |
| `request._ckr_collection_ctx` | État implicite | **Non** |

---

## Livrables après validation de ce cadrage

| # | Livrable | Responsable |
|---|----------|-------------|
| 1 | Amendement `cadrage/CONTRATS.md` (C3 — noms paramètres, source Incontournables) | Archi |
| 2 | ADR-023 Lot 6.1 dans `cadrage/DECISIONS.md` | Archi |
| 3 | Ticket d’**exécution** `TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md` (ou section « Exécution » ci-dessous) | Archi |
| 4 | `RECETTE_MANUELLE_LOT6_1.md` (ébauche acceptable au cadrage) | Archi |
| 5 | Mise à jour `ROADMAP.md` — Lot 6.1 | Pilotage |

**Pas de code** avant case « Cadrage validé » ci-dessous.

---

## Critères GO / NO GO — validation cadrage

### GO cadrage (autorise ticket d’exécution)

- [x] D1–D9 tranchées et consignées (ADR-023)
- [x] Source : catégorie publique `product.public.category`
- [x] Canonique + alias `/incontournables` validés
- [x] Présentation minimale validée
- [x] Non-régression Lots 1–5 exigée
- [x] Une seule porte — Incontournables uniquement

### NO GO cadrage

- [ ] Besoin d’un moteur catalogue parallèle
- [ ] Besoin de plusieurs portes simultanées au Lot 6.1
- [ ] Dépendance obligatoire à `dorevia_ckreyol_marketplace`
- [ ] Refonte `/shop` ou rupture tunnel achat acceptée

---

## Checklist validation MOA (cadrage)

```text
[x] Lot 6.1 limité à Incontournables uniquement
[x] Socle Lots 1–5 rappelé comme prérequis
[x] Options D1–D12 documentées
[x] Décisions D1–D9 actées par MOA
[x] Niveau présentation / source produits validés
[x] Critère porte éditoriale sans casser website_sale accepté

Décision cadrage : [ ] GO cadrage  [x] GO cadrage avec réserves  [ ] NO GO / report
```

**Réserves cadrage** (2026-05-18) :

```text
1. Catégorie publique = source simple Lot 6.1 ; collection éditoriale à étudier plus tard.
2. SEO fin (canonical, noindex) à documenter sans surcharger l’exécution.
3. Filtres natifs Odoo conservés pour l’instant.
```

---

## Prochaine étape

1. Validation MOA du ticket d’exécution : [`TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md`](./TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md)
2. Implémentation `19.0.6.0.0` **après** GO ticket exécution uniquement

---

## Références

| Document | Lien |
|----------|------|
| ROADMAP Lot 6 | `docs/pilotage/ROADMAP.md` |
| CONTRATS C2–C3 | `docs/cadrage/CONTRACTS.md` |
| ARCHITECTURE § Lot 6 | `docs/cadrage/ARCHITECTURE.md` |
| Lot 0 matrice portes | `docs/tickets/TICKET_MARKETONE_LOT0_CADRAGE.md` |
| Legacy contrôleur | `dorevia_ckreyol_marketplace/controllers/website_sale_ckr.py` |
