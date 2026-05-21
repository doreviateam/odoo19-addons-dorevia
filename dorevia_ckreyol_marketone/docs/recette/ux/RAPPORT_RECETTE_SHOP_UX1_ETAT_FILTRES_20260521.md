# Rapport recette — UX-1 État utilisateur `/shop` — 2026-05-21

| Champ | Valeur |
|-------|--------|
| Recette | `RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md` |
| Base | `ckr-marketone-01` |
| URL | `http://localhost:18079/shop` |
| Version code | **`19.0.15.9.4`** |
| Statut | **GO MOA** — wording état vide validé |

---

## GO MOA wording état vide (`19.0.15.9.4`)

Validation MOA (2026-05-21) :

| Élément | Libellé validé | Verdict |
|---------|----------------|---------|
| Compteur haut (0 résultat + filtres) | **`Aucun produit trouvé`** | **GO** |
| État vide central | **`Aucun produit ne correspond à cette sélection`** | **GO** |
| CTA | **`Effacer les filtres`** — conservé · bien positionné | **GO** |
| Chips `(0)` | Cause compréhensible · boutique non perçue comme vide | **GO** |

**Réserve non bloquante** : le compteur haut reste visuellement discret — acceptable à ce stade.

---

## Chronologie

| Version | Résultat |
|---------|----------|
| `9.0`–`9.1` | Layout · chips `(n)` · sidebar · 58 tests |
| `9.2` | État vide central contextualisé |
| `9.3` | Première passe wording « disponible » / « critères » |
| **`9.4`** | **GO MOA** — **`Aucun produit trouvé`** + **`…cette sélection`** |

---

## Tests automatisés

Attendu : **`0 failed, 0 error(s) of 58 tests`**.

Contrôles wording `9.4` :

- `test_zero_label` → `Aucun produit trouvé` si contexte filtré
- `test_shop_grid_title_zero_results_search` → compteur + état central MOA
- `test_shop_empty_state_filtered_with_category` → idem

---

## Smoke navigateur post-`9.4`

| Cas | Résultat |
|-----|----------|
| `/shop` | `50 produits disponibles` |
| Filtres actifs avec résultats | chips `(n)` · compteur « disponibles » |
| Combo 0 résultat (ex. Biscuits sucrés + La Réunion) | **`Aucun produit trouvé`** · **`…cette sélection`** · chips `(0)` · **Effacer les filtres** |
| Sidebar | Collections → Catégories → Origines |
| CSS / mobile | OK |

> Déploiement : `-u dorevia_ckreyol_marketone` + **restart** Odoo requis après upgrade code (sinon ancien wording `9.3` servi).

---

## Règle MOA retenue

| Zone | 0 résultat **avec** filtres | 0 résultat **sans** filtre |
|------|----------------------------|----------------------------|
| Compteur haut | **`Aucun produit trouvé`** | **`Aucun produit disponible`** |
| État central | **`Aucun produit ne correspond à cette sélection`** | `Aucun produit défini` (Odoo natif) |

---

## Captures

| Fichier | Rôle |
|---------|------|
| `capture_recette_ux1_ok_biscuits_20260521_2104.png` | GO layout + chips |
| `capture_recette_ux1_ok_mobile_combo_20260521_2104.png` | GO mobile |
| `capture_recette_ux1_avant_wording_etat_vide_20260521.png` | Historique KO pré-`9.3` |

---

## Verdict

```text
GO MOA wording état vide — 19.0.15.9.4 — Aucun produit trouvé + …cette sélection — Effacer les filtres OK — chips (0) OK — réserve non bloquante : discrétion compteur haut.
```

**Clôture UX-1 / wording état vide** : **GO MOA**.
