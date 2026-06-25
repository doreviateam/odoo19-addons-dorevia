# Recette QA — Axe B · Libellés navigation & badges · 19.0.1.41.0

| Champ | Valeur |
|---|---|
| Projet | `dorevia_ck_marketone` |
| Ticket | [TICKET_DEV_AXE_B_LIBELLES_NAV_BADGES_CK_20260625.md](./TICKET_DEV_AXE_B_LIBELLES_NAV_BADGES_CK_20260625.md) |
| Version livrée | `dorevia_ck_marketone_content` **19.0.1.41.0** |
| Date recette | 2026-06-25 |
| Rédacteur | Dev — transmission QA |
| Base attendue | `dorevia_ck_marketone_01` · `http://localhost:18079` |
| Méthode | Upgrade module · tests Odoo par tag · contrôles HTTP · captures |

---

## Périmètre de la livraison

| Correction | Canal | Détail |
|---|---|---|
| Header **Maison & Bien-être** → **Soin & Bien-être** | Config nav + sync BO | `nav_v22_config.NAV_MAISON_LABEL` · `bootstrap_ck_navigation()` · migration `19.0.1.41.0` |
| Mega-menu fallback titre rayon | Config nav | `nav_mega_menu.py` — libellé racine aligné |
| Ruban **New!** → **Nouveau !** | Donnée BO `product.ribbon` | `ribbon_sync.francize_new_product_ribbon()` · migration `19.0.1.41.0` |

**Hors périmètre confirmé (inchangé) :**

- Structure catégories BO · filmstrip Shop · cards · sidebar · Home « Nos coups de cœur »
- Entrée **Communauté** (`href="#"`) · absence de **Coups de cœur** en header N3
- Mega-menus : familles / sélections internes (sauf titre fallback rayon)

---

## Prérequis recette

1. Mettre à jour le module :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 \
  -u dorevia_ck_marketone_content --stop-after-init
```

2. Vérifier la version :

```sql
SELECT latest_version FROM ir_module_module
WHERE name = 'dorevia_ck_marketone_content';
-- Attendu : 19.0.1.41.0
```

---

## Tests automatisés

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 \
  --test-tags dorevia_ck_nav_axe_b,dorevia_ck_nav_communaute,dorevia_ck_header_v22,dorevia_ck_marketone_nav_sync \
  --stop-after-init
```

| Tag | Couverture |
|---|---|
| `dorevia_ck_nav_axe_b` | Menu **Soin & Bien-être** unique · pas de legacy · ruban **Nouveau !** |
| `dorevia_ck_nav_communaute` | Non-régression Communauté + rayons |
| `dorevia_ck_header_v22` | Rendu HTTP header · **Soin & Bien-être** visible |
| `dorevia_ck_marketone_nav_sync` | Sync navigation V2.2 |

**Attendu Dev :** tous les tests au vert (**34/34** sur sandbox `dorevia_ck_marketone_01`).

---

## Grille de recette manuelle

### Desktop (1280)

| # | Contrôle | Attendu | OK |
|---|---|---|---|
| 1 | Header N3 — libellé rayon soin | **Soin & Bien-être** visible | ☐ |
| 2 | Header N3 — ancien libellé | **Maison & Bien-être** absent | ☐ |
| 3 | Lien catégorie | Clic → `/shop/category/soin-bien-etre-2` (ou équivalent) · HTTP 200 | ☐ |
| 4 | Entrée Communauté | Présente · `href="#"` | ☐ |
| 5 | Coups de cœur header | Absent de la nav racine | ☐ |
| 6 | Mega-menu Soin & Bien-être | S'ouvre · titre fallback **Soin & Bien-être** si pas de visuel BO | ☐ |
| 7 | Badge produit | **Nouveau !** (pas **New!**) sur card Home / shop / fiche si ruban actif | ☐ |

### Mobile (390)

| # | Contrôle | Attendu | OK |
|---|---|---|---|
| 8 | Drawer navigation | **Soin & Bien-être** visible | ☐ |
| 9 | Ancien libellé | **Maison & Bien-être** absent | ☐ |
| 10 | Badges | **Nouveau !** lisible | ☐ |

### Non-régression

| # | Contrôle | Attendu | OK |
|---|---|---|---|
| 11 | Home section 3 | Titre **Nos coups de cœur** inchangé | ☐ |
| 12 | Produits Home vedettes | Même sélection qu'avant upgrade | ☐ |
| 13 | Filmstrip `/shop` | **Soin & Bien-être** (déjà conforme avant ticket) | ☐ |
| 14 | Panier · recherche · tri · filtres | Comportement inchangé | ☐ |
| 15 | Catalogue seed | 7 produits publiés | ☐ |

---

## Captures attendues

| Fichier suggéré | Scénario |
|---|---|
| `axe_b_01_header_desktop_1280.png` | Header desktop — **Soin & Bien-être** |
| `axe_b_02_header_mobile_390.png` | Drawer mobile |
| `axe_b_03_mega_soin_bien_etre.png` | Mega-menu ouvert |
| `axe_b_04_badge_nouveau.png` | Card produit avec badge **Nouveau !** |

Script header mis à jour : `scripts/ck_h22_recette_qa.mjs` (libellé **Soin & Bien-être**).

---

## Contrôles SQL rapides

```sql
-- Menu header
SELECT id, name, url FROM website_menu
WHERE parent_id = (SELECT menu_id FROM website WHERE id = 1 LIMIT 1)
  AND name ILIKE '%bien%';

-- Ruban Nouveau
SELECT id, name FROM product_ribbon WHERE name ILIKE '%nouveau%' OR name ILIKE '%new%';
```

**Attendu :**

- Une entrée `Soin & Bien-être` · URL catégorie soin · **0** entrée `Maison & Bien-être` au niveau racine N3
- Ruban `Nouveau !` présent · pas de `New!` actif sur produits visibles

---

## Fichiers modifiés (résumé Dev)

| Fichier | Nature |
|---|---|
| `nav_v22_config.py` | Config — `NAV_MAISON_LABEL` + `LEGACY_NAV_MAISON_LABEL` |
| `nav_sync.py` | Sync — retrait / renommage menu legacy |
| `nav_mega_menu.py` | Fallback mega-menu |
| `ribbon_sync.py` | Francisation ruban |
| `migrations/19.0.1.41.0/post-migrate.py` | Migration post-upgrade |
| `models/ck_mega_menu_*.py` | Libellés sélection BO admin |
| `tests/test_ck_nav_axe_b_labels.py` | Tests Axe B |
| `dorevia_ck_theme/tests/test_ck_header_v22.py` | Assertion HTTP header |

---

## Verdict QA

| Champ | Valeur |
|---|---|
| Verdict | **GO** — livraison 19.0.1.41.0 recevable |
| Détail | [RECETTE_QA_AXE_B_LIBELLES_NAV_BADGES_20260625_VERDICT.md](./RECETTE_QA_AXE_B_LIBELLES_NAV_BADGES_20260625_VERDICT.md) |
| Tests | **34/34** au vert |
| Observations hors périmètre | Ruban id=5 « Coup de cœur » sans fr_FR · menus sans fr_FR (Axe C) |

### Pré-validation Dev (sandbox)

| Contrôle | Résultat |
|---|---|
| Upgrade `19.0.1.41.0` | OK — migration exécutée |
| Tests `dorevia_ck_nav_axe_b` + `dorevia_ck_header_v22` | **16/16** au vert (passe ciblée) |
| Tests complets nav (`+ communaute + nav_sync`) | **34/34** au vert |
| Rendu HTTP header | **Soin & Bien-être** visible · **Maison & Bien-être** absent |
| URL catégorie conservée | `/shop/category/soin-bien-etre-2` |

---

> **Transmission QA** : après upgrade `19.0.1.41.0`, exécuter la grille ci-dessus et renseigner le verdict. En cas d'écart, joindre capture + requête SQL menu/ruban.
