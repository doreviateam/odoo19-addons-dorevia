# Micro-ticket Dev — Card catalogue · pied canon Home (prix + CTA)

| Champ | Valeur |
| --- | --- |
| Date | 26 juin 2026 |
| Parent | [`TICKET_DEV_CARD_CTA_UNIFIE_CK.md`](TICKET_DEV_CARD_CTA_UNIFIE_CK.md) — **GO 65.0** |
| Module | `dorevia_ck_theme` |
| Priorité | Moyenne — polish UX post-GO |
| Estimation | **0,25–0,5 j-h Dev** + **0,25 j-h QA** |
| Statut | **Livré** — `19.0.1.66.0` |

---

## Contexte MOA

Le ticket CTA unifié est **GO technique** (bouton texte, grille 4/2/1, responsive). Restent deux écarts visuels vs le canon Home « Nos coups de cœur » :

| Écart | Home (canon) | Catalogue (actuel) |
| --- | --- | --- |
| Pied prix / CTA | **Même ligne** — prix à gauche, bouton compact à droite | Prix puis bouton **pleine largeur** en dessous |
| Séparateur | Ligne fine entre méta et zone prix/CTA | Absent ou peu visible |

---

## Réponse Dev — bouton pleine largeur : choix ou défaut ?

**Choix Dev explicite** (ticket 64.0 / 65.0), pas un héritage Odoo passif.

| Couche | Comportement natif Odoo 19 | Ce qu'on a livré |
| --- | --- | --- |
| `o_wsale_product_sub` | `flex-direction: row` (prix + boutons côte à côte) | **Surchargé** en `column` + `width: 100%` sur le CTA |
| Fichier | `product_tile.scss` (variables `--o-wsale-card-sub-*`) | `website_sale.scss` l. ~333–405 |

**Motif du choix** : après le NO GO 64.0 (CTA invisible < 992 px), la correction a privilégié **lisibilité mobile** (bouton pill pleine largeur, min-height 44 px) au détriment du layout desktop Home.

**Recommandation MOA (Option B)** : réaligner le **desktop** sur le canon Home ; conserver le pied **colonne + CTA pleine largeur uniquement sur mobile** (≤ 575 px) pour ne pas régresser la recette 390 px.

---

## Objectif

Sur les cards `.ck-product-card--shop` :

1. **Desktop ≥ 768 px** (et en priorité grille 4 cols ≥ 992 px) : prix et CTA sur **une ligne**, bouton **compact** (pas `width: 100%`), comme `--home` + mixin `ck-product-card-foot-desktop`.
2. **Séparateur** : `border-top` visible entre corps card (méta) et pied prix/CTA — reprendre `ck-product-card-foot` si masqué par Odoo.
3. **Mobile ≤ 575 px** : conserver pied **colonne** + CTA pleine largeur + min-height 44 px (non-régression QA 65.0).

---

## Implémentation pressentie

| # | Fichier | Action |
| --- | --- | --- |
| R1 | `product_card.scss` | Étendre `ck-product-card-foot-desktop` à `&--shop` **ou** inclure le mixin depuis `website_sale.scss` en `@media (min-width: 768px)` |
| R2 | `website_sale.scss` | Retirer `width: 100%` / `flex-direction: column` sur pied **desktop** ; garder ces règles dans `@media (max-width: 575.98px)` uniquement |
| R3 | `website_sale.scss` | Forcer `border-top: 1px solid $ck-border` sur `.ck-product-card__foot` / `.o_wsale_product_sub` shop si absent au rendu |
| R4 | Tests | Assertion HTTP optionnelle : présence `ck-product-card__foot` + pas de régression tags shop existants |
| R5 | Version | Bump `dorevia_ck_theme` → **19.0.1.66.0** (indicatif) |

**Ne pas toucher** : libellé CTA, `shop_ppr`, grille 4/2/1, neutralisation `visibility` < lg.

---

## Critères d'acceptation

- [ ] Desktop 1280 — `/shop` : prix et « Ajouter au panier » sur **une ligne** ; bouton **plus compact** que pleine largeur.
- [ ] Desktop — séparateur horizontal visible entre méta et pied (comme Home).
- [ ] Mobile 390 — CTA toujours visible, ≥ 44 px, pleine largeur OK.
- [ ] Tablette 800 — grille 2 cols inchangée ; CTA visible.
- [ ] Non-régression : panier, wishlist, Note 07, tests `dorevia_ck_shop_card`.

---

## Recette QA ciblée

| Viewport | Contrôle |
| --- | --- |
| 1280 | Comparaison visuelle Home vs `/shop` — hauteur card catalogue ≤ canon Home |
| 800 | CTA visible · 2 colonnes |
| 390 | CTA visible · 1 colonne · pas d'overflow |

Captures : avant/après pied card sur `/shop` (desktop + 390).

---

## Message commit suggéré

```text
[UX] Aligne le pied card shop sur le canon Home (prix + CTA)
```
