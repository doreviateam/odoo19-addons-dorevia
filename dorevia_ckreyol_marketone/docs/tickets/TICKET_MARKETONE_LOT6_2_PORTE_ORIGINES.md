# TICKET — Lot 6.2 Porte Origines (cadrage) `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES` |
| **Lot** | 6.2 — **Cadrage uniquement** (pas de code) |
| **Statut** | **Ouvert** — en attente validation MOA |
| **Type** | Ticket de cadrage / arbitrage |
| **Version cible module** | `19.0.7.0.0` (proposition, post-validation) |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | Lots 1–5 **GO** ; Lot 6.1 **GO avec réserves** (`19.0.6.0.0`) ; **ADR-024** / **NOTE_UNIVERS_CK_MARKETONE** **GO** |
| **Contrats** | C2, C3 (extension), C9 ; ADR-018, **ADR-024** |
| **Référence legacy** | `dorevia_ckreyol_marketplace` — **lecture seule** (`SPEC_IMPL_ORIGINES`, `CONTRAT_URL_ORIGINES`) |

---

## Objectif du cadrage

Préparer la **deuxième porte catalogue** Marketone — **Origines** — en respectant la doctrine des **trois univers** (ADR-024), **sans implémenter de code** dans ce ticket.

```text
Critère attendu (cadrage validé) :
La porte Origines oriente l’achat dans /shop sans moteur parallèle,
tout en réservant le récit territoire à l’univers Culture (espaces dédiés, lots ultérieurs).
```

**Doctrine portes** (inchangée) :

```text
Les portes orientent.
Les filtres Odoo sélectionnent.
Marketone ne crée pas un moteur catalogue parallèle.
```

**Doctrine univers** (ADR-024) :

```text
Boutique  — acheter   → porte Origines = filtre / orientation /shop
Culture   — découvrir → récit territoires = espaces dédiés, hors scope exécution Lot 6.2
Savoirs   — transmettre → hors scope Lot 6.2
```

---

## Double lecture Origines — cœur du cadrage

| Facette | Univers | Lot 6.2 | Lots ultérieurs |
|---------|---------|---------|-----------------|
| **Porte Boutique** | Boutique | `/shop?marketone_mode=origin` (+ facettes origine) ; filtre produits via attribut catalogue ; bandeau minimal | — |
| **Contenu Culture** | Culture | **Hors scope** — pas de hub territoire, pas de pages CMS longues | Rubriques territoire / producteur ; liens depuis porte ou fiche |

**Risque MOA** : confondre **facette catalogue** (Boutique) et **encyclopédie territoire** (Culture) sur la même URL. Ce ticket **impose** la séparation.

**Garde-fou** : sur `/shop`, le visiteur comprend **quelle porte** est active (titre + phrase courte) — héritage signal éditorial legacy S1–S2, **niveau minimal** comme Lot 6.1 (pas hero Explorer).

---

## Contexte — socle et Lot 6.1

| Étape | Route / scope | Statut |
|-------|---------------|--------|
| Socle Lots 1–5 | home, shop, product, cart, checkout | **GO** |
| Lot 6.1 Incontournables | `marketone_mode=featured`, `/incontournables` → 301 | **GO avec réserves** |
| Tests non-régression | 60/60 (`…lot6_1_featured`) | **OK** |

**Pattern technique validé Lot 6.1** (à réutiliser, pas à réinventer) :

- `_get_search_options` → options injectées ;
- `product.template._search_get_detail` → `base_domain` ;
- `_get_shop_domain` → alignement fourchette prix ;
- `_get_additional_shop_values` → variables QWeb bandeau ;
- alias HTTP → **301** vers URL canonique ;
- **pas** de `request._marketone_*`.

**Ce ticket ne livre aucun fichier Python, XML, SCSS ni test.**

---

## Contraintes Lot 6.2 (non négociables)

| Contrainte | Application |
|------------|-------------|
| **Une seule porte** | Origines uniquement — pas promo, pack, collections, ni seconde porte simultanée |
| Pas de moteur parallèle | Même hooks `website_sale` que 6.1 |
| Pas de refonte `/shop` | Grille native ; bandeau **minimal** |
| Pas de hub Culture obligatoire | Pas de page territoire longue en v1 porte |
| Fiche produit | Pas d’encyclopédie ; affichage origines **sobre** si déjà prévu Lot 4 — pas d’élargissement lourd |
| `website_sale` souverain | Panier, checkout, tunnel inchangés |
| Pas de marketplace | Pas d’import `ckr.shop.origin` ni dépendance module legacy |
| Pas de `request._ckr_*` / `request._marketone_*` | Options explicites uniquement |
| ADR-024 | Culture et Savoirs **non** implémentés au Lot 6.2 |
| Non-régression | 60 tests + tag `dorevia_marketone_lot6_2_origin` (proposition) |

---

## Décisions à trancher (MOA + archi)

### D1 — Paramètre URL mode porte

| Option | Exemple | Note |
|--------|---------|------|
| **A — `marketone_mode=origin`** | `/shop?marketone_mode=origin` | **Recommandation** — aligné `CONTRACTS.md` C2 whitelist |
| B — `marketone_mode=origines` | Libellé FR URL | Moins aligné contrats |

**Décision MOA** : ☐ **`marketone_mode=origin`** — libellé visible : **Origines**

---

### D2 — Facette origine(s) sur `/shop`

Legacy : `ckr_origin=<slug>` répétable, logique **OU**.

| Option | Mécanisme | Pour | Contre |
|--------|-----------|------|--------|
| **A — `marketone_origin=<slug>`** | Slug répété en query | Cohérent préfixe `marketone_*` | Nouveau paramètre à documenter |
| B — Réutiliser nom legacy `ckr_origin` | Compat bookmarks anciens | SEO legacy | Dette nommage `ckr_*` |
| C — Facette uniquement via attributs Odoo natifs | `attribute_values` standard | Zéro param custom | Moins de contrôle bandeau porte |

**Recommandation cadrage** : **A** pour la facettes explicites + **D1** pour la porte seule.

**Décision MOA** : ☐ Paramètre facette : _______________

---

### D3 — Comportement `marketone_mode=origin` **sans** facette origine

Legacy acté : **catalogue complet** + bandeau porte (pas de filtre caché).

| Option | Comportement |
|--------|--------------|
| **A — Catalogue complet + bandeau** | Aligné legacy MOA — entrée « toutes les origines » |
| B — Catalogue vide jusqu’à choix facette | Plus strict — risque UX |

**Recommandation** : **A**.

**Décision MOA** : ☐ _______________

---

### D4 — Source de vérité « rattachement produit ↔ origine »

| Option | Mécanisme | Pour | Contre |
|--------|-----------|------|--------|
| **A — Attribut catalogue `product.attribute` « Origine »** | `attribute_line_ids` sur template, multi-valeurs, `no_variant` | Standard Odoo ; filtre natif possible | Métadonnées visiteur (slug, phrase) limitées |
| B — A + modèle Marketone léger `marketone.shop.origin` | M2M vers `product.attribute.value` ; slug, phrase, visibilité site | Sépare catalogue (A1) et récit routage (legacy CK) | Nouveau modèle + BO + ACL |
| C — Tag produit seul | Simple | Hors doctrine « pas tag libre seul » (legacy) | Rejeté cadrage |
| D — Importer `ckr.shop.origin` | Existant | — | **Interdit** C11 |

**Recommandation cadrage** : **A** minimum ; **B** si MOA exige slugs stables et phrases visiteur **sans** dupliquer la liste produits.

**Décision MOA** : ☐ A seul · ☐ A + profil Marketone léger

---

### D5 — Alias HTTP

| Alias | Cible proposée | Legacy |
|-------|----------------|--------|
| `/origines` | **301** → `/shop?marketone_mode=origin` | `/origines` → 301 |

**Décision MOA** : ☐ Alias `/origines` validé

---

### D6 — Référence origine invalide (slug inconnu / non publié)

| Option | Comportement |
|--------|--------------|
| **A — 302/301 vers `/shop` nu** | Legacy — pas de contexte erroné |
| B — 200 + grille vide + message | Acceptable si message explicite |

**Recommandation** : **A** (repli propre).

**Décision MOA** : ☐ _______________

---

### D7 — Présentation sur `/shop` (univers Boutique)

Niveau **minimal** (symétrique Lot 6.1) :

| Élément | Contenu proposé |
|---------|-----------------|
| Titre | **Origines** (ou nom origine si une seule facette active) |
| Intro | 1–2 phrases — ex. *« Parcourez les produits selon leur territoire d’origine. »* |
| Lien retour | **Tous les produits** → `/shop` |
| État vide | Message si filtre actif et 0 produit |

**Interdit** : hero Explorer, chips multi-portes, sidebar portes dédiée, refonte grille.

**Décision MOA** : ☐ Présentation minimale validée

---

### D8 — Fiche produit (Lot 4 — rappel, pas refonte)

| Option | Comportement |
|--------|--------------|
| **A — Affichage texte origines** (champs BO / attribut) sans lien vers porte | Évite confusion variante — legacy |
| B — Liens vers `/shop?marketone_origin=<slug>` | Orientation Boutique explicite |
| C — Liens vers pages Culture (futur) | Hors 6.2 |

**Recommandation cadrage** : **A** ou **B** — **pas** de bloc encyclopédique.

**Décision MOA** : ☐ _______________

---

### D9 — Culture (hors Lot 6.2 — engagement MOA)

| Sujet | Décision attendue |
|-------|-------------------|
| Pages territoire `/culture/…` ou équivalent | ☐ Report lot Culture dédié |
| Hub « toutes les origines » éditorial | ☐ Non requis v1 (legacy §13.8) |
| Liens depuis bandeau porte vers Culture | ☐ Optionnel post-6.2 ; pas bloquant |

---

### D10 — SEO

Comme Lot 6.1 : **documenter** canonical / noindex ; implémentation **hors** scope élargi sauf décision MOA.

**Décision MOA** : ☐ Note doc seulement

---

### D11 — Cumul avec `marketone_mode=featured`

`CONTRACTS` C3.4 : priorité legacy `pack > promo > featured > origin > collection`.

| Option | Comportement |
|--------|--------------|
| **A — Un seul `marketone_mode` actif** (whitelist, dernier ignoré ou priorité) | Simple — cohérent 6.1 |
| B — Cumul featured + origin | Complexité — **non recommandé** Lot 6.2 |

**Recommandation** : **A** — un mode ; facettes `marketone_origin` **en plus** du mode porte si MOA valide D2.

**Décision MOA** : ☐ _______________

---

## Référence legacy (lecture seule)

| Élément legacy | Comportement | Reprise Marketone ? |
|----------------|--------------|---------------------|
| `ckr_mode=origin` | Porte + options `_search_get_detail` | ☑ `marketone_mode=origin` (si D1 validé) |
| `ckr_origin=<slug>` | Facette OU | ☑ `marketone_origin` (si D2-A validé) |
| `ckr.shop.origin` | Profil slug / phrase / visibilité | ☑ Inspiration **B** — modèle **Marketone** neuf si MOA |
| Attribut « Origine » | Vérité catalogue multi-valeurs | ☑ **A** recommandé |
| `/origines` → 301 | Alias | ☑ Si D5 validé |
| Bandeaux QWeb lourds `ckr_shop_origin_*` | Hero porte | ☐ Non — minimal D7 |
| `ckr_mode=origin` seul = catalogue complet | Bandeau sans filtre | ☑ Si D3-A validé |
| Slug invalide → `/shop` nu | Repli | ☑ Si D6-A validé |
| Fiche : origines non cliquables | Culture / variante | ☑ Référence D8 |

**Ne pas reprendre** : monolithe `website_sale_ckr.py`, `request._ckr_sidebar_facet_omit`, exceptions redirect comme flux principal, cumul multi-`ckr_mode` chips.

---

## Hors périmètre Lot 6.2

| Exclusion | Report |
|-----------|--------|
| Pages Culture territoire | Lot Culture |
| Recettes / Savoirs | Lot Savoirs |
| Promotions, packs, collections, Incontournables (autre mode) | Autres lots 6.x |
| `product_pack` | Décision MOA séparée |
| Refonte Explorer homepage | Lot accueil |
| Navigation multi-univers complète | ADR-024 — planning global |
| Seed XML origines | BO manuel recette |

---

## Livrables après validation de ce cadrage

| # | Livrable | Responsable |
|---|----------|-------------|
| 1 | Amendement `CONTRACTS.md` — C3.B Origines (si GO) | Archi |
| 2 | ADR-025 Lot 6.2 (proposition) dans `DECISIONS.md` | Archi |
| 3 | Ticket **exécution** `TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md` | Archi |
| 4 | `RECETTE_MANUELLE_LOT6_2.md` (ébauche) | Archi |
| 5 | `ROADMAP.md` — Lot 6.2 | Pilotage |

**Pas de code** avant case « Cadrage validé » ci-dessous.

---

## Critères GO / NO GO — validation cadrage

### GO cadrage (autorise ticket d’exécution)

- [ ] D1–D11 tranchées et consignées
- [ ] Séparation Boutique (porte) / Culture (report) explicitée et acceptée
- [ ] Source produit : attribut catalogue (+ profil Marketone si validé)
- [ ] Canonique + alias `/origines` validés
- [ ] Présentation minimale validée
- [ ] Non-régression Lots 1–5 + 6.1 exigée
- [ ] Une seule porte — Origines uniquement

### NO GO cadrage

- [ ] Hub Culture obligatoire dans le même lot
- [ ] Moteur catalogue parallèle
- [ ] Dépendance `dorevia_ckreyol_marketplace`
- [ ] Refonte `/shop` ou rupture tunnel

---

## Checklist validation MOA (cadrage)

```text
[ ] Lot 6.2 limité à Origines (porte Boutique) uniquement
[ ] ADR-024 / Note Univers pris comme référence
[ ] Culture (récit territoire) reportée hors exécution 6.2
[ ] Options D1–D11 documentées
[ ] Pattern technique 6.1 (hooks website_sale) accepté
[ ] Critère porte sans casser website_sale accepté

Décision cadrage : [ ] GO cadrage  [ ] GO cadrage avec réserves  [ ] NO GO / report
```

---

## Prochaine étape

1. **MOA** : trancher D1–D11 et valider ce ticket de cadrage.
2. **Archi** : CONTRATS C3.B + ADR-025 + ticket exécution.
3. **Dev** : implémentation **uniquement** après GO ticket exécution.

---

## Références

| Document | Lien |
|----------|------|
| Note univers | `docs/cadrage/NOTE_UNIVERS_CK_MARKETONE.md` |
| ADR-024 | `docs/cadrage/DECISIONS.md` |
| Lot 6.1 cadrage / exec | `TICKET_MARKETONE_LOT6_1_*` |
| Legacy origines | `dorevia_ckreyol_marketplace/docs/mvp_01/CONTRAT_URL_ORIGINES.md`, `SPEC_IMPL_ORIGINES.md` |
| ROADMAP | `docs/pilotage/ROADMAP.md` |
