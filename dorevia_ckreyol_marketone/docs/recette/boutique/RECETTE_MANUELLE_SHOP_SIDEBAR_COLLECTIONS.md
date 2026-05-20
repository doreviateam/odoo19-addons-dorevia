# Recette manuelle — Sidebar /shop — Collections (Lot B)

| Champ | Valeur |
|-------|--------|
| **Ticket** | [`TICKET_MARKETONE_COLLECTION_LOT_B_SIDEBAR`](../../tickets/boutique/TICKET_MARKETONE_COLLECTION_LOT_B_SIDEBAR.md) |
| **ADR** | [ADR-030](../../cadrage/DECISIONS.md#adr-030--collection-commerciale-marketone) |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Version module** | `19.0.12.0.0` (ordre rubriques : **`19.0.12.1.0`** — voir [`RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md`](./RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md)) |
| **Statut recette** | **GO MOA** — S1–S11 validés (2026-05-19) |

---

## Prérequis

| Élément | Détail |
|---------|--------|
| Lot A BO | **GO MOA** — `19.0.11.0.0` |
| Sidebar catégories | **GO MOA** — `19.0.10.8.0` + C4 `19.0.10.9.0` |
| Module | `dorevia_ckreyol_marketone` **≥ `19.0.12.0.0`** |
| Tests auto | `dorevia_marketone_shop_sidebar` + `dorevia_marketone_shop_sidebar_collections` — **0** failed |

---

## Collections candidates (éligibilité)

Une collection apparaît dans la sidebar **uniquement** si :

- `active` = oui ;
- **Publié** = oui (`website_published`) ;
- site web compatible (vide ou site courant) ;
- dans la fenêtre **date début / fin** si renseignée ;
- **≥ 1** produit vendable et publié sur le site (Lot A).

---

## Jeu de données recette MOA

Créer ou utiliser **au moins 2** collections **publiées** :

| ID | Collection (ex.) | Produits | Usage scénarios |
|----|------------------|----------|-----------------|
| **Col-A** | *Apéritif créole* (slug ex. `aperitif-creole`) | Dont produits **Martinique** | S2, S3, S4, S5 |
| **Col-B** | *Idées cadeaux* (slug ex. `idees-cadeaux`) | Peu ou **aucun** Martinique | S3 OR · S7 masquage C4 · S8 |

Optionnel (hors liste sidebar) : brouillon non publié · collection hors dates.

---

## Règle C4 (collections)

Afficher une collection dans la sidebar si :

- elle a **≥ 1** produit dans `search_product` courant (hors facette `marketone_collection`) ;
- **OU** son slug est **déjà actif** (case cochée / URL).

---

## Slugs invalides (MOA)

`/shop?marketone_collection=slug-inconnu` (ou collection brouillon / hors date) :

- **Attendu** : slug **ignoré** — pas de grille vide « totale » ;
- catalogue affiché avec les **autres** filtres éventuels (Origine, catégories, prix) ;
- **pas** de case pour un slug invalide dans la sidebar.

> Écart volontaire avec les **catégories** (slug secondaire invalide → grille vide).

---

## Grille de recette — Lot B

| # | Scénario | Action | Attendu | MOA | Tech |
|---|----------|--------|---------|-----|------|
| **S1** | Rubrique | `/shop` | **Collections** → **Catégories** → **Origines** → **Prix** (ordre `19.0.12.1.0`) | ☑ | ☑ |
| **S2** | Filtre simple | Cocher **Col-A** (publiée, produits vendables + publiés site) | Grille filtrée · `marketone_collection=` dans l’URL | ☑ | ☑ |
| **S3** | Multi OR | Cocher **Col-A** + **Col-B** | 2× `marketone_collection` · union produits (OR) | ☑ | ☑ |
| **S4** | AND Origine | **Col-A** + **Martinique** | Deux paramètres · grille = intersection | ☑ | ☑ |
| **S5** | AND catégories | **Col-A** + 1 catégorie principale | `marketone_category` + `marketone_collection` | ☑ | ☑ |
| **S6** | AND prix | Collection + fourchette prix | Non-régression | ☑ | ☑ |
| **S7** | C4 contexte | `/shop` nu → **Martinique** | **Col-B** absente si sans produit MQ ; **Col-A** si compatible | ☑ | ☑ |
| **S8** | Active conservée | **Col-B cochée d’abord** → puis **Martinique** | **Col-B** reste visible et cochée même si combinaison restrictive ou vide | ☑ | ☑ |
| **S9** | Effacer filtres | Filtres actifs → **Effacer** | Plus de `marketone_category` ni `marketone_collection` | ☑ | ☑ |
| **S10** | Porte | `/incontournables` | 301 featured · pas de `marketone_collection` | ☑ | ☑ |
| **S11** | Slug invalide | Ouvrir `/shop?marketone_collection=slug-inexistant` | Catalogue **sans** filtre collection (pas grille vide totale) | ☑ | ☑ |

### Détail S2 (produit éligible)

Le produit rattaché en BO doit être **vendable** (`Vente`) **et** **publié sur le site web**.

### Détail S5 (bidirectionnel — rappel)

- Collection → onglet **Produits** : produits visibles.
- Fiche produit → tags **Collections commerciales** : collection visible.

### Détail S7 (C4)

1. Noter collections visibles sur `/shop` nu.
2. Cocher **Martinique**.
3. **Col-B** (sans produit Martinique) **disparaît** de la liste (sauf S8 si déjà cochée).

### Détail S8 (active conservée)

**Ordre obligatoire** (sinon Col-B disparaît avant d’être cochable — cf. S7) :

1. Sur `/shop` nu, cocher **Col-B** (collection peu compatible Martinique).
2. **Ensuite** cocher **Martinique** (Origine).
3. **Attendu** : **Col-B** reste **visible et cochée** dans le bloc Collections, même si la grille devient restrictive ou **vide**.
4. Décocher **Col-B** → la liste se recalcule ; la grille peut se repeupler.

### Détail S9 (conservation croisée)

Collection → Origine → catégorie : paramètres **conservés** dans l’URL (JS).

---

## Verdict MOA

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-05-19 | **GO MOA** | S1–S11 · tests auto 28/28 · réserves QWeb / `read_group` non bloquantes |

---

## Captures (hors git)

| Fichier | Scénario |
|---------|----------|
| *À joindre* | S1, S7, S8, S9, S11 |

---

## Tests auto

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_shop_sidebar,dorevia_marketone_shop_sidebar_collections \
  --http-port=8076
```
