# TICKET — Exécution Culture v2 légère — Territoires additionnels `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_EXEC` |
| **Univers** | **Culture** — découvrir |
| **Lot** | Culture v2 légère — **+2 territoires** (`martinique`, `reunion`) |
| **Statut** | **Livré technique** — recette MOA en attente |
| **Version module** | `19.0.9.0.0` |
| **Recette** | [`RECETTE_MANUELLE_CULTURE_V2.md`](../recette/RECETTE_MANUELLE_CULTURE_V2.md) |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | Cadrage v2 **GO avec réserves** — [`TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_CADRAGE.md`](TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_CADRAGE.md) ; Culture v1 **GO MOA** `19.0.8.0.0` ; portes Boutique 6.1 / 6.2 **GO** ; **ADR-024**, **ADR-026**, **ADR-027** |
| **ADR** | ADR-024, ADR-026, **ADR-027** |
| **Contrats** | **C8** (v2) ; C7.4 ; non-régression C3.A / C3.B |
| **Recette v1** | [`RECETTE_MANUELLE_CULTURE_V1.md`](../recette/RECETTE_MANUELLE_CULTURE_V1.md) |

---

## Objectif

Prouver que la grammaire Culture **`/culture/<slug>`** (livrée en v1) est **réplicable** sur **deux territoires supplémentaires** — **`martinique`** et **`reunion`** — sans hub Culture, sans menu header, sans modèle Culture lourd, **sans** ouvrir Lot 6.3 Boutique ni Savoirs.

```text
Critère GO Culture v2 légère :
Un visiteur atteint /culture/martinique et /culture/reunion (profils publiés),
retrouve la même structure sobre que /culture/guadeloupe,
peut acheter via /shop?marketone_mode=origin&marketone_origin=<slug>,
et le socle Boutique (85+ tests) reste sans régression.
```

**Livraison** `19.0.9.0.0` — **Option A** : pas de code fonctionnel nouveau ; tests `dorevia_marketone_culture_v2` + recette v2. Profil BO `reunion` créé sur `ckr-marketone-01` (absent au point de contrôle).

---

## Décisions MOA figées (cadrage v2 — 2026-05-18)

| # | Décision |
|---|----------|
| **D1** | **+2 territoires** : slugs `martinique`, `reunion` — **sous réserve** profils BO disponibles ; ajustement slugs proposé **avant** GO exécution si écart |
| **D2** | **Option A** : aucun code fonctionnel nouveau si l’infra v1 couvre les slugs publiés — preuve par **BO + recette** (+ tests dédiés) |
| **D3** | Sections **génériques** conservées ; varient : `name_visitor`, `context_phrase`, slug, CTA porte Origines |
| **D4** | **Pas** d’image par territoire en v2 légère |
| **D5** | **Aucun** lien croisé entre territoires — pas de mini-hub |
| **D6** | Menu header Culture **reporté** |
| **D7** | SEO : **documentation** seulement |
| **D8** | Tag tests `dorevia_marketone_culture_v2` — périmètre ci-dessous |

### Réserves MOA

| # | Réserve |
|---|---------|
| R1 | Slugs `martinique` / `reunion` **sous réserve** des profils BO sur `ckr-marketone-01` |
| R2 | **Pas** de champs éditoriaux longs sur `marketone.shop.origin` |
| R3 | **Pas** de hub `/culture` |
| R4 | **Pas** de menu header Culture |
| R5 | **Pas** de Lot 6.3 Boutique ni Savoirs en parallèle |

---

## Point de contrôle pré-exécution (obligatoire)

Avant **GO exécution**, vérifier en BO sur **`ckr-marketone-01`** :

| Slug attendu | Profil `marketone.shop.origin` | Valeur attribut **Origine** | `website_published` | `website_id` |
|--------------|-------------------------------|----------------------------|---------------------|--------------|
| `martinique` | ☑ existe | ☑ lié | ☑ oui | ☑ My Website |
| `reunion` | ☑ créé exec | ☑ lié | ☑ oui | ☑ My Website |
| `guadeloupe` | ☑ pilote v1 | ☑ | ☑ | ☑ |

**Si écart** : proposer à MOA des slugs alternatifs alignés BO **avant** implémentation — mettre à jour ce ticket et la recette v2.

**Phrase courte** (`context_phrase`) : à renseigner pour chaque territoire v2 (chapô page Culture).

---

## Périmètre inclus (exécution)

### 1. Delta technique (D2 = A par défaut)

| Cas | Livrables |
|-----|-----------|
| **Infra v1 suffisante** (attendu) | Pas de changement `controllers/culture.py`, template, SCSS ; **tests** + **recette** + doc + version `19.0.9.0.0` |
| **Écart démontré** | Documenter le besoin minimal dans ce ticket **avant** code — pas de modèle Culture |

**Interdit** : nouveau modèle `marketone.culture.*` ; champs longs sur profil origine ; hub `/culture` ; liens inter-territoires ; images par territoire.

### 2. Contenu BO (recette — hors seed XML récit)

| Territoire | URL Culture | Porte Origines filtrée |
|------------|-------------|------------------------|
| Martinique | `/culture/martinique` | `/shop?marketone_mode=origin&marketone_origin=martinique` |
| La Réunion | `/culture/reunion` | `/shop?marketone_mode=origin&marketone_origin=reunion` |
| Pilote v1 | `/culture/guadeloupe` | inchangé — non-régression |

Produits : au moins **1 produit publié** par territoire v2 avec valeur **Origine** correspondante (recette manuelle).

### 3. Tests automatisés (D8)

| Fichier | Tag |
|---------|-----|
| `tests/test_marketone_culture_v2.py` | `dorevia_marketone_culture_v2` |

**Scénarios minimum** :

| # | Test |
|---|------|
| T1 | `GET /culture/martinique` → **200** si profil publié (données test ou BO recette) |
| T2 | `GET /culture/reunion` → **200** si profil publié |
| T3 | CTA / corps page → lien `marketone_mode=origin` + `marketone_origin=<slug>` |
| T4 | Liens Boutique : bandeau Origines facetté + fiche produit → `/culture/<slug>` |
| T5 | Non-régression Culture v1 : `guadeloupe` (tests `dorevia_marketone_culture_v1` **inchangés** ou rejoués) |
| T6 | Slug inconnu → **404** |

**Non-régression globale** : **85+** post-tests (Lots 1–6.2 + Culture v1 + v2) — **0** failed.

### 4. Documentation

| Livrable | Fichier |
|----------|---------|
| Recette MOA v2 | `docs/recette/RECETTE_MANUELLE_CULTURE_V2.md` |
| `ENV_REFERENCE` | Territoires v2, prérequis BO, tag tests |
| ADR-027 | Déjà dans `cadrage/DECISIONS.md` |
| Contrat C8 v2 | Note dans `cadrage/CONTRACTS.md` |

### 5. Version module

| Champ | Valeur |
|-------|--------|
| `__manifest__.py` | `19.0.9.0.0` — **incrément même si delta code minimal** (tests + doc) |

---

## Fichiers indicatifs (exécution)

```text
tests/test_marketone_culture_v2.py          # tag dorevia_marketone_culture_v2
tests/__init__.py                           # import
docs/recette/RECETTE_MANUELLE_CULTURE_V2.md
docs/recette/ENV_REFERENCE.md               # MAJ
__manifest__.py                             # 19.0.9.0.0
```

**Probablement inchangés** (D2 = A) : `controllers/culture.py`, `views/pages/culture_territory.xml`, `static/src/scss/_culture.scss`, `models/marketone_shop_origin.py` (champs).

---

## Hors périmètre (explicite)

| Exclusion | Report |
|-----------|--------|
| Hub `/culture` | Culture v3+ |
| Menu header Culture | Post maturité |
| Modèle ORM Culture | Interdit v2 |
| Champs éditoriaux longs | Interdit |
| Images / galerie par territoire | v3+ |
| Liens « Voir aussi » entre territoires | Interdit v2 |
| Lot 6.3 Promotions / Kits / Collections | Gel MOA |
| Savoirs / recettes | Ticket Savoirs |
| Seed XML contenu récit long | Interdit |

---

## Critères GO / NO GO exécution

### GO

- [x] Point de contrôle BO — `reunion` créé sur base recette
- [x] `GET /culture/martinique` et `/culture/reunion` → **200** (auto)
- [x] Même grammaire que `guadeloupe` (auto)
- [x] CTA et liens Boutique contextuels (auto)
- [x] Pas de hub ; pas de menu header ; pas de liens croisés (auto)
- [x] `marketone.shop.origin` inchangé (champs)
- [x] **91** post-tests — **0** failed
- [ ] Recette MOA v2 validée
- [ ] Mobile 375 px (recette MOA)

### NO GO

- [ ] Territoire v2 non accessible alors que profil publié (hors problème exploitation restart)
- [ ] Régression Boutique / Culture v1
- [ ] Hub ou liens croisés entre territoires
- [ ] Extension encyclopédique du profil origine

---

## Checklist validation MOA (exécution)

```text
[x] Cadrage Culture v2 GO avec réserves
[x] D1–D8 figées
[x] Point de contrôle BO validé (`reunion` créé)
[x] GO pour implémentation — `19.0.9.0.0`
[ ] Recette MOA GO  [ ] NO GO
```

### Réserve exploitation (conservée)

Après `-u` sur daemon déjà lancé : **redémarrer Odoo** si `GET /culture/<slug>` répond **404** alors que le profil est publié.

---

## Prochaine étape

1. **MOA** : recette [`RECETTE_MANUELLE_CULTURE_V2.md`](../recette/RECETTE_MANUELLE_CULTURE_V2.md).
2. **Culture v3+** (hub, menu) — ticket dédié.
3. **Ne pas** ouvrir Lot 6.3 ni Savoirs en parallèle.

---

## Références

| Document | Rôle |
|----------|------|
| [`TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_CADRAGE.md`](TICKET_MARKETONE_CULTURE_V2_TERRITOIRES_LEGERS_CADRAGE.md) | Cadrage v2 — **clôturé GO avec réserves** |
| [`TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC.md`](TICKET_MARKETONE_CULTURE_TERRITOIRES_EXEC.md) | Culture v1 — GO MOA |
| [`RECETTE_MANUELLE_CULTURE_V1.md`](../recette/RECETTE_MANUELLE_CULTURE_V1.md) | Recette pilote |
| [`cadrage/DECISIONS.md`](../cadrage/DECISIONS.md) — ADR-027 | Culture v2 légère |
| [`cadrage/CONTRACTS.md`](../cadrage/CONTRACTS.md) — C8 | Contrat Culture |
