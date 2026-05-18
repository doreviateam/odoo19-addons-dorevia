# Recette manuelle — Lot 6.1 (porte Incontournables)

| Champ | Valeur |
|-------|--------|
| **Lot** | 6.1 — Porte Incontournables |
| **Module** | `19.0.6.0.0` |
| **Base** | `ckr-marketone-01` — http://localhost:18079 |
| **Ticket exécution** | [`TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md`](../tickets/TICKET_MARKETONE_LOT6_1_INCONTOURNABLES_EXEC.md) |
| **Verdict** | **GO avec réserves** (2026-05-18) |

---

## Prérequis BO (obligatoires)

- [x] Paramètre `dorevia_ckreyol_marketone.featured_public_category_id` renseigné (id numérique de la catégorie)
- [x] Catégorie e-commerce **Incontournables** créée
- [x] **Site web** : la catégorie doit être rattachée au site courant (`website_id` = **My Website** sur `ckr-marketone-01`)
  - **Sans ce rattachement** : `/shop?marketone_mode=featured` peut renvoyer une **erreur 500** en recette réelle (constat MOA 2026-05-18)
- [x] 2–3 produits recette rattachés à cette catégorie (multi-catégories autorisé)

---

## Exploitation sandbox / recette

Après `-u dorevia_ckreyol_marketone` sur un **daemon Odoo long-running** (ex. `localhost:18079`), la route alias **`GET /incontournables`** peut ne pas répondre correctement tant que le processus n’a pas été **redémarré** (rechargement du routing HTTP).

| Contexte | Action |
|----------|--------|
| Tests `--stop-after-init` | Aucun redémarrage requis (processus neuf à chaque run) |
| Sandbox / recette navigateur | Redémarrer le conteneur ou le service Odoo après mise à jour module si `/incontournables` ne fait pas 301 |

```bash
# Exemple : redémarrer le stack sandbox
docker compose -f /Users/doreviateam/sandbox-odoo19/docker-compose.yml restart odoo
```

---

## Parcours MOA

| # | Test | Attendu | OK | KO |
|---|------|---------|----|----|
| L6-01 | `/incontournables` | 301 → `/shop?marketone_mode=featured` | ☑ | ☐ |
| L6-02 | Canonique | 200, titre **Incontournables**, intro, lien retour | ☑ | ☐ |
| L6-03 | Grille | Uniquement produits de la catégorie | ☑ | ☐ |
| L6-04 | Filtres Odoo | Sidebar / tri toujours utilisables | ☑ | ☐ |
| L6-05 | `/shop` sans param | Grille complète, pas de bandeau porte | ☑ | ☐ |
| L6-06 | Fiche + panier | Ajout panier OK depuis produit filtré | ☑ | ☐ |
| L6-07 | Non-régression | `/`, fiche, panier, checkout scopes Lots 2–5 | ☑ | ☐ |
| L6-08 | Mobile 375 px | Pas de débordement horizontal | ☑ | ☐ |

---

## Tests auto

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_smoke,dorevia_marketone_lot2,dorevia_marketone_lot2_1,dorevia_marketone_lot3,dorevia_marketone_lot4,dorevia_marketone_lot5,dorevia_marketone_lot6_1_featured \
  --http-port=8071
```

**Résultat MOA** : 60 post-tests, 0 failed, 0 error(s).

---

## Réserves documentées (GO avec réserves)

| # | Réserve | Mitigation |
|---|---------|------------|
| R1 | Catégorie sans `website_id` → 500 sur featured | Toujours rattacher la catégorie **Incontournables** au site **My Website** |
| R2 | Alias `/incontournables` absent après `-u` sans redémarrage daemon | Redémarrer Odoo sandbox avant recette HTTP sur alias |

---

## Verdict MOA

| Décision | ☑ |
|----------|---|
| **GO** | |
| **GO avec réserves** | ☑ |
| **NO GO** | |

**Date** : 2026-05-18 · **Validé par** : MOA recette manuelle
