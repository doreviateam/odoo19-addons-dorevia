# Recette — Propagation BO → front · Section « Nos coups de cœur » · V1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` · C-Kreyol / CK |
| **Module** | `dorevia_ck_marketone_content` **19.0.1.25.9** |
| **Instance** | `dorevia_ck_marketone_01` · http://localhost:18079 |
| **Date** | 2026-06-17 |
| **Tests auto** | `--test-tags=dorevia_ck_marketone_featured_propagation` |
| **Objet** | Vérifier qu'une édition produit en BO se répercute sur la carte vedette |

```text
La section vedettes est un snapshot SSR (HTML figé) reconstruit par déclencheurs
ORM + cron 30 min. Cette recette valide la répercussion par champ rendu.
```

---

## 1. Rappel mécanisme

| Voie | Effet | Latence |
|------|-------|---------|
| **Déclencheurs ORM** (write produit / variante / tag / unité / ruban) | rebuild immédiat du SSR | instantané |
| **Cron** `ck_cron_sync_home_featured` | rattrape les cas hors-ORM (titre, prix, métadonnée périmés) | ≤ 30 min |
| **Scope curation (M1/D3)** | rebuild seulement si le produit est dans « Coups de cœur » peuplée | — |

> **Déploiement** : après `-u`, **redémarrer Odoo** (bundles assets) avant recette visuelle.

---

## 2. Champs réellement rendus sur la carte

Titre (**nom produit**) · métadonnée (**tags** + format/quantité + prix de référence) · **prix** · **badge** (ruban). La catégorie et l'origine **ne sont plus affichées** sur la carte (composition actuelle) — leur édition n'a donc pas d'effet attendu.

---

## 3. Grille de recette manuelle

Prérequis : un produit publié rangé dans « Coups de cœur », visible sur la home.

| # | Action BO | Attendu front (`/`) | Voie |
|---|-----------|---------------------|------|
| P1 | Renommer le produit (champ **Nom**) | Titre de la carte mis à jour | ORM immédiat |
| P2 | Changer le **prix de vente** | Prix de la carte mis à jour | ORM immédiat |
| P3 | Modifier le **prix de variante** (salé/sucré) | Carte de la variante concernée mise à jour | ORM immédiat |
| P4 | Ajouter / retirer une **étiquette** (tag) | Ligne métadonnée mise à jour | ORM immédiat |
| P5 | Renommer une **étiquette** existante | Ligne métadonnée mise à jour | ORM immédiat |
| P6 | Modifier **quantité nette / unité** | Format/prix réf mis à jour | ORM immédiat |
| P7 | Renommer / changer la couleur du **ruban** | Badge mis à jour | ORM immédiat |
| P8 | Assigner / retirer un **ruban** | Badge apparaît / disparaît | ORM immédiat |
| P9 | Changer **image** produit | Visuel de la carte mis à jour | ORM immédiat |
| P10 | Dé-publier / republier, retirer de la vente | Carte retirée / réintégrée | ORM immédiat |
| P11 | Sortir le produit de « Coups de cœur » | Carte retirée (ou repli auto si seuil) | ORM immédiat |
| S1 | Éditer un produit **hors** « Coups de cœur » | **Aucun** changement de la home | scope D3 |

### Étapes par contrôle

1. Ouvrir le BO produit, appliquer la modification, **enregistrer**.
2. Recharger `/` (vider le cache navigateur si besoin).
3. Vérifier l'attendu sur la carte.
4. En cas d'absence de mise à jour immédiate : attendre le cron (≤ 30 min) ou forcer `model._ck_sync_home_featured_labels_on_startup()`.

---

## 4. Edge cases / limites connues

- **Origine via valeur d'attribut** : renommer une valeur d'attribut « origine » n'est pas propagé (l'origine n'est plus rendue sur la carte ; seul `price_extra` de variante déclenche un refresh).
- **Catégorie / origine** : non rendues sur la carte actuelle → édition sans effet attendu (pas un défaut).
- **Liste de prix** : sans pricelist publique en recette, le prix vient de `variant.lst_price` ; un changement de pricelist n'est pas un déclencheur (hors périmètre recette CK actuelle).
- **Cron** : un changement appliqué hors ORM (SQL direct) n'est rattrapé qu'au prochain passage cron.

---

## 5. Critères d'acceptation

- P1 (titre) et P7/P8 (badge) : mise à jour immédiate — **les trous historiques sont corrigés** (`name` ajouté aux déclencheurs, override `product.ribbon`, détection titre dans le cron).
- P2–P6, P9–P11 : non-régression OK.
- S1 : aucun rebuild (scope curation respecté).
- Tests auto `dorevia_ck_marketone_featured_propagation` : verts.

---

*Recette propagation BO→front vedettes · `dorevia_ck_marketone_content` 19.0.1.25.9 · 2026-06-17.*
