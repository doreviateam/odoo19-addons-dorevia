# Recette manuelle — Collections commerciales — Lot A (BO)

| Champ | Valeur |
|-------|--------|
| **Ticket** | [`TICKET_MARKETONE_COLLECTION_LOT_A`](../tickets/TICKET_MARKETONE_COLLECTION_LOT_A.md) |
| **ADR** | [ADR-030](../cadrage/DECISIONS.md#adr-030--collection-commerciale-marketone) |
| **Base** | `ckr-marketone-01` |
| **URL shop (non-régression)** | http://localhost:18079/shop |
| **Version module** | `19.0.11.0.0` |
| **Statut recette** | **GO MOA** — Lot A BO (2026-05-19) |

---

## Prérequis

| Élément | Détail |
|---------|--------|
| Module | `dorevia_ckreyol_marketone` **≥ `19.0.11.0.0`** |
| Droits | Utilisateur **Website / Designer** (ou équivalent) |
| Tests auto | Tag `dorevia_marketone_collection_lot_a` — **9/9** OK |

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_collection_lot_a \
  --http-port=8075
```

---

## Règle publication (rappel MOA)

- Collection **non publiée** : peut exister **sans produit** (brouillon / préparation).
- Collection **publiée** : **≥ 1** produit avec **`Vente`** activée **et** **Publié sur le site** (`sale_ok` + `website_published`).

---

## Grille BO

| # | Scénario | Action | Attendu | MOA |
|---|----------|--------|---------|-----|
| **B1** | Menu | Site web → Configuration → **Collections commerciales** | Liste accessible | ☑ |
| **B2** | Brouillon vide | Créer collection (nom, slug, teaser, image optionnels) · **non publiée** · 0 produit | Enregistrement OK | ☑ |
| **B3** | Publication sans produit | Cocher **Publié** sans produit rattaché | **Erreur** utilisateur explicite | ☑ |
| **B4** | Publication avec produit | Rattacher ≥ 1 produit **vendable ET publié sur le site** · cocher **Publié** | Enregistrement OK · compteur produits ≥ 1 | ☑ |
| **B5** | Lien bidirectionnel | Voir détail ci-dessous | Produit ↔ collection visibles des deux côtés | ☑ |
| **B6** | Dates | `date_end` &lt; `date_start` | Erreur validation | ☑ |
| **B7** | Slug | Slug avec majuscules / espaces | Erreur validation | ☑ |
| **B8** | Non-régression shop | `/shop` navigateur | Sidebar inchangée · pas de `marketone_collection` dans l’URL | ☑ |

### Détail B4 (produit éligible)

1. Ouvrir une collection brouillon.
2. Onglet **Produits** : ajouter un produit avec **Vente** cochée **et** **Publié sur le site**.
3. Optionnel : pack vendable publié — accepté (A3).
4. Cocher **Publié** sur la collection → enregistrement **sans** erreur.

### Détail B5 (rattachement bidirectionnel)

1. Depuis la **collection** : onglet **Produits** — produit visible.
2. Depuis la **fiche produit** : champ **Collections commerciales** — collection visible.
3. Modification depuis l’un des deux écrans → cohérence après enregistrement.

---

## Réserves non bloquantes

| Sujet | Détail |
|-------|--------|
| QWeb `@class` | Warning — `views/pages/shop_clear_filters.xml` (sidebar `19.0.10.8.0`) |
| `read_group` | Deprecation — `models/marketone_shop_category.py` (C4 `19.0.10.9.0`) |

---

## Verdict MOA

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-05-19 | **GO MOA** | B1–B8 validés BO · 9/9 tests auto · pas d’exposition front Lot A |

---

## Captures (hors git)

| Fichier | Scénario |
|---------|----------|
| *À joindre* | B2–B5 · B8 `/shop` |
