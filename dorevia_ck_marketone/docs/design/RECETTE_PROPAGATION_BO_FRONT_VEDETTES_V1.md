# Recette — Propagation BO → front · Section « Nos coups de cœur » · V1.1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` · C-Kreyol / CK |
| **Module** | `dorevia_ck_marketone_content` **19.0.1.25.10** |
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

### Volet variantes (`product.product` d'un template multi-variantes — ex. Manio salé / sucré)

Une card représente **une variante précise**. Contrôles dédiés :

| # | Action BO sur la variante | Attendu front | Voie |
|---|---------------------------|---------------|------|
| V1 | Modifier le **prix de la variante** (price_extra) | Prix de **cette** card mis à jour, l'autre intacte | ORM immédiat (PTAV) |
| V2 | Renommer la **valeur d'attribut** (salé → …) | Titre de **cette** card mis à jour, l'autre intacte | ORM immédiat (`product.attribute.value`) |
| V3 | Donner une **image propre à la variante** | Visuel de **cette** card bascule sur l'image variante | ORM immédiat (`image_variant_1920`) |
| V4 | Dé-publier / retirer de la vente **une** variante | Seule **cette** card disparaît | ORM immédiat |
| V5 | Cliquer **Ajouter au panier** sur une variante | C'est bien **cette** variante qui entre au panier (`data-product-id`) | — |
| V6 | Produit **simple** (mono-variante) | Continue de fonctionner comme avant | non-régression |

### Étapes par contrôle

1. Ouvrir le BO produit, appliquer la modification, **enregistrer**.
2. Recharger `/` (vider le cache navigateur si besoin).
3. Vérifier l'attendu sur la carte.
4. En cas d'absence de mise à jour immédiate : attendre le cron (≤ 30 min) ou forcer `model._ck_sync_home_featured_labels_on_startup()`.

---

## 4. Edge cases / limites connues

- **Nom de variante (valeur d'attribut)** : désormais **propagé** au titre (override `product.attribute.value`) — V2.
- **Image de variante** : désormais **propagée** (`image_variant_1920` ajouté aux déclencheurs variante) — V3.
- **Remplacement d'image au même emplacement** (mêmes bytes, URL inchangée) : l'URL `/web/image/...` sert le contenu courant ; vider le cache navigateur si l'ancienne image persiste.
- **Catégorie / origine** : non rendues sur la carte actuelle → édition sans effet attendu (pas un défaut).
- **Liste de prix** : sans pricelist publique en recette, le prix vient de `variant.lst_price` ; un changement de pricelist n'est pas un déclencheur (hors périmètre recette CK actuelle).
- **Cron** : un changement appliqué hors ORM (SQL direct) n'est rattrapé qu'au prochain passage cron.

---

## 5. Critères d'acceptation

- P1 (titre) et P7/P8 (badge) : mise à jour immédiate — trous template corrigés (`name` aux déclencheurs, override `product.ribbon`, détection titre cron).
- **V1–V5 (variantes)** : prix, nom de valeur d'attribut, image variante, publication, panier — propagation immédiate et **sans contamination** entre variantes (trous variantes corrigés : `image_variant_1920` aux déclencheurs, override `product.attribute.value`, détection image cron).
- P2–P6, P9–P11, V6 : non-régression OK (produits simples inclus).
- S1 : aucun rebuild (scope curation respecté).
- Tests auto `dorevia_ck_marketone_featured_propagation` : verts (8 tests).

---

*Recette propagation BO→front vedettes · `dorevia_ck_marketone_content` 19.0.1.25.10 · 2026-06-17.*
