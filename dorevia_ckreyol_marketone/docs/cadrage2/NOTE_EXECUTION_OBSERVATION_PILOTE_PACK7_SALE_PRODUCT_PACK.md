# Note exécution — Observation pilote pack 7 `sale_product_pack`

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-08 |
| **Base** | `ckr-marketone-01` |
| **Cadre** | [`CADRE_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md`](./CADRE_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md) |
| **Décision MOA** | [`DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md`](./DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md) |
| **Verdict exécution** | **Observation technique O1–O6 + F1–F3 exécutée** |
| **Retours métier** | **O7–O8 à compléter** par ventes · logistique · compta |
| **Activation prod globale** | **NO GO** |

---

## Doctrine

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

---

## Configuration vérifiée

| Pack | Produit | Configuration |
|------|---------|---------------|
| **7** | Maniocookies salés La Platine | `detailed` · `ignored` |
| **8** | Crackers manioc Sainte-Anne | `non_detailed` · `ignored` |

Modules plateforme installés : `sale_product_pack`, `stock_product_pack`, `sale_stock_product_pack`.

---

## Résultats observation technique

Exécution Odoo en rollback, sans écriture durable de recette.

| Point | Pack 7 `detailed` | Pack 8 `non_detailed` |
|-------|-------------------|------------------------|
| **O1 — Commande** | **6 lignes** : 1 parent + 5 composants | **1 ligne** pack |
| **O2 — Lignes composants** | 5 lignes composants visibles · sous-total composants **0 €** | Aucune ligne composant |
| **O3 — Confirmation** | Commande `sale` | Commande `sale` |
| **O4 — Préparation / picking** | Picking `done` · **6 moves** | Picking `done` · **1 move** |
| **O5 — Stock** | Moves composants présents | Move pack parent seul |
| **O6 — Facturation** | Total facture **4,17 €** · total commande **4,17 €** | Total facture **25,00 €** · total commande **25,00 €** |

Contrôle livraison : `qty_delivered` parent = **1** sur les deux packs.

---

## Smoke front

| Point | Résultat |
|-------|----------|
| **F1** | `/shop?marketone_mode=pack` affiche la porte **Kits & Coffrets** avec packs **7** et **8** |
| **F2** | `/kits` arrive sur `/shop?marketone_mode=pack` |
| **F3** | Panier `website_sale` pack **8** = **1 ligne** |

Produit hors pack **9** absent de la porte pack.

---

## Points métier à compléter

| Point | Statut |
|-------|--------|
| **O7 — Lisibilité BO** | À compléter par ventes · logistique · compta |
| **O8 — Intérêt métier** | À arbitrer MOA après retour des équipes |

Options de sortie inchangées : maintien pilote seul, extension limitée, GO généralisation, ou retour pack 7 en `non_detailed`.

---

## Verdict actif

| Niveau | Statut |
|--------|--------|
| Observation technique pilote | ☑ **Exécutée** |
| Retour métier O7–O8 | ☐ **À compléter** |
| GO généralisation | ☐ **Reporté** |
| GO activation prod globale | ☐ **NO GO** |
