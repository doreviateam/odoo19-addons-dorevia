# Recette manuelle — Recadrage BO produit (cadrage2)

| Champ | Valeur |
|-------|--------|
| **Lot** | Recadrage BO produit — cadrage2 |
| **Décision MOA** | [`DECISION_MOA_RECADRAGE_BO.md`](./DECISION_MOA_RECADRAGE_BO.md) |
| **Livraison Dev** | [`NOTE_LIVRAISON_LOT_RECADRAGE_BO.md`](./NOTE_LIVRAISON_LOT_RECADRAGE_BO.md) |
| **Base** | `ckr-marketone-01` |
| **URL shop (non-régression)** | http://localhost:18079/shop |
| **Version module** | `19.0.16.0.0` |
| **Statut recette** | **Clôturé — GO avec réserves MOA** (2026-06-08) |
| **Réception MOA** | [`RECEPTION_MOA_LOT_RECADRAGE_BO.md`](./RECEPTION_MOA_LOT_RECADRAGE_BO.md) |

---

## Objectif

Valider que la fiche produit CK est **odoo-iste côté back-office** :

- plus de bloc « Tuile commerce /shop » sous l’image principale ;
- 4 onglets CK lisibles ;
- libellés métier (sans « tuile », « /shop », « CLI ») ;
- **aucune régression** sur le rendu `/shop`.

---

## Prérequis

| Élément | Détail |
|---------|--------|
| Module | `dorevia_ckreyol_marketone` **≥ `19.0.16.0.0`** |
| Mise à jour | `-u dorevia_ckreyol_marketone` sur la base de recette |
| Droits recette | Utilisateur **admin** ou **Website / Designer** |
| Produit test | Au moins 1 produit avec **Vente** cochée (`sale_ok`) et **publié** sur le site |
| Produit tuile (optionnel) | 1 produit avec vignette catalogue validée (`shop_tile_status = Validée pour affichage catalogue`) pour R8 |

### Tests automatisés (avant recette manuelle)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 \
  --test-tags=dorevia_marketone_bo \
  --stop-after-init --http-port=0
```

Attendu : **0 échec** (9 tests).

Non-régression image /shop :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 \
  --test-tags=dorevia_marketone_shop_tile \
  --stop-after-init --http-port=0
```

Attendu : tests HTTP grille / fiche **OK** (éventuel échec import JPEG pilote hors périmètre BO).

---

## Accès recette

1. Se connecter à Odoo : http://localhost:18079 — base **`ckr-marketone-01`**.
2. Menu **Vente → Produits → Produits** (ou **Site web → eCommerce → Produits**).
3. Ouvrir un produit **vendable** (`sale_ok` coché), de préférence déjà publié sur le site.

---

## Grille BO — fiche produit

| # | Scénario | Action | Attendu | MOA |
|---|----------|--------|---------|-----|
| **R1** | Image principale | Ouvrir la fiche · zone en-tête / image | **Une seule** zone image produit standard (`image_1920`) | ☑ |
| **R2** | Absence bloc legacy | Même écran · sous l’image principale | **Aucun** groupe « Tuile commerce /shop » · aucun second bloc image CK collé à l’image principale | ☑ |
| **R3** | Onglets CK visibles | Produit `sale_ok` · onglets du bas | Présence de **Publication site**, **Catalogue CK**, **Qualité image / contenu** | ☑ |
| **R4** | Onglet Publication site | Ouvrir **Publication site** | Champs : publication (`is_published`), catégories eCommerce, description boutique · **pas** de doublon visible dans l’onglet Ventes (groupe « Ecommerce Shop » allégé) | ☑ |
| **R5** | Onglet Catalogue CK | Ouvrir **Catalogue CK** | Champ **Collections commerciales** · message d’aide sur les **origines** (attribut + menu Configuration) | ☑ |
| **R6** | Rattachement collection | Depuis **Catalogue CK** : ajouter une collection · enregistrer | Collection visible · cohérence avec fiche collection (onglet Produits) | ☑ |
| **R7** | Onglet Qualité image | Ouvrir **Qualité image / contenu** | **Vignette catalogue normalisée**, **Statut média catalogue**, **Note qualité visuelle** | ☑ |
| **R8** | Libellés métier | Parcourir R4–R7 · survol des champs | **Aucun** libellé utilisateur contenant « Tuile », « /shop » ou « CLI » | ☑ |
| **R9** | Onglet Technique (utilisateur standard) | Utilisateur **sans** mode développeur / hors `no_one` | Onglet **Technique** **absent** | ☑ |
| **R10** | Onglet Technique (mode dev) | Activer **mode développeur** · rouvrir la fiche | Onglet **Technique** visible · champs pipeline en **lecture seule** (version recette, traité le, run batch) | ☑ |
| **R11** | Produit non vendable | Ouvrir un produit **sans** `sale_ok` | Onglets CK **masqués** (comportement `invisible="not sale_ok"`) | ☑ |

### Détail R4 — Publication site

1. Onglet **Publication site**.
2. Vérifier le toggle **Publié** / publication site.
3. Vérifier **Catégories eCommerce** (tags).
4. Saisir ou consulter **Description boutique** (`description_ecommerce`).
5. Enregistrer → pas d’erreur · valeurs conservées au rechargement.

### Détail R7 — Qualité image

1. Onglet **Qualité image / contenu**.
2. Lire le texte d’aide : fallback vers **image produit principale** si vignette non validée.
3. Si produit avec vignette validée en base : image dérivée visible · statut **Validée pour affichage catalogue** (ou équivalent métier).

---

## Grille non-régression front `/shop`

| # | Scénario | Action | Attendu | MOA |
|---|----------|--------|---------|-----|
| **F1** | Grille boutique | Naviguer vers `/shop` | Page charge · grille produits **identique** à avant recadrage BO (pas de régression layout / cartes) | ☑ |
| **F2** | Produit avec vignette validée | Repérer un produit connu avec vignette catalogue active | Vignette normalisée affichée en grille (si flag `marketone.shop_tile_enabled` actif) | ☑ |
| **F3** | Produit sans vignette validée | Repérer un produit sans dérivé validé | Image produit principale (`image_1920`) en grille | ☑ |
| **F4** | Fiche produit front | Cliquer un produit · page `/shop/<slug>` | Fiche **inchangée** · pas d’exposition du dérivé `image_shop_tile` sur la fiche (comportement existant) | ☑ |
| **F5** | Panier / wishlist | Ajouter un produit au panier (smoke) | Parcours achat **non impacté** | ☑ |

---

## Critères GO / NO GO

### GO MOA si

- R1–R11 : **tous validés** ;
- F1–F5 : **aucune régression** constatée ;
- tests auto `dorevia_marketone_bo` : **0 échec**.

### NO GO si

- Bloc « Tuile commerce /shop » encore visible sous l’image principale ;
- Onglets CK absents sur produit vendable ;
- Libellés techniques visibles côté utilisateur métier ;
- Régression visuelle ou fonctionnelle sur `/shop`.

---

## Verdict MOA

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-06-08 | ☑ GO avec réserves · ☐ GO · ☐ NO GO | Recette R1–R11 et F1–F5 validée sur `ckr-marketone-01`. Réserve hors périmètre BO : `test_t5_import_manifest_validates_offline` reste en échec sur JPEG pilotes absents de l’environnement. |

### Notes d'exécution 2026-06-08

- Tests automatisés `dorevia_marketone_bo` : **9/9 OK**.
- Tests automatisés `dorevia_marketone_shop_tile` : **11/12 OK** ; échec connu sur `test_t5_import_manifest_validates_offline` (JPEG pilotes absents), non bloquant pour le lot BO.
- Produit BO contrôlé : `Assortiment apéritif créole` (`product.template` 181), `sale_ok=True`.
- Produit non vendable contrôlé : `Livraison standard` (`product.template` 1), `sale_ok=False`.
- R6 validé par présence et conservation du rattachement existant **Apéritif créole** dans l'onglet **Catalogue CK** ; aucune écriture métier supplémentaire n'a été effectuée.
- Front `/shop` contrôlé : grille OK, `image_shop_tile` visible pour `Pâtes de manioc Mayotte` (`validated_grid`), fallback image standard visible pour `Maniocookies salés La Platine` (`validated_storage`), fiche produit sans exposition du dérivé, ajout panier OK.

---

## Références

| Document | Rôle |
|----------|------|
| [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../REFERENCE_RECETTE_BOUTIQUE_MOA.md) | Invariants anti-régression `/shop` |
| [`DOCTRINE_IMAGE_V2.md`](../../cadrage/DOCTRINE_IMAGE_V2.md) | Master + dérivé vignette |
| [`ENV_REFERENCE.md`](../reference/ENV_REFERENCE.md) | Base et commandes Docker |
