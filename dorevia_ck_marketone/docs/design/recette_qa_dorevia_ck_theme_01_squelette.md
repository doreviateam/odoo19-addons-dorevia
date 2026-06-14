# Recette QA — Squelette `dorevia_ck_theme` (ticket 01)

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Module** | `dorevia_ck_theme` |
| **Ticket source** | [`ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md`](../ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md) |
| **Chemin module** | `odoo19-addons-dorevia/dorevia_ck_theme/` |
| **Date** | 2026-06-12 |
| **Statut QA** | **OK squelette statique** · **OK install/QWeb · OK visuel post-correction** — [`recette_qa_dorevia_ck_theme_01_visuelle_post_correction.md`](./recette_qa_dorevia_ck_theme_01_visuelle_post_correction.md) |

---

## 1. Verdict

```text
OK SQUELETTE TICKET 01 — SOCLE VALIDÉ (STATIQUE · INSTALL/QWEB · VISUEL POST-CORRECTION)
```

Validation **documentaire / statique** du squelette livré. Recettes instance — voir [`recette_qa_dorevia_ck_theme_01_fonctionnelle.md`](./recette_qa_dorevia_ck_theme_01_fonctionnelle.md) et [`recette_qa_dorevia_ck_theme_01_visuelle_post_correction.md`](./recette_qa_dorevia_ck_theme_01_visuelle_post_correction.md).

---

## 2. Périmètre contrôlé (statique)

| # | Critère | Verdict |
|---|---------|---------|
| 1 | Pas de `models/` | ✅ OK |
| 2 | Pas de `controllers/` | ✅ OK |
| 3 | Pas de JS métier | ✅ OK |
| 4 | Dépendances limitées : `website`, `website_sale`, `website_crm` | ✅ OK |
| 5 | QWeb limité (layout + website_sale héritages minimaux) | ✅ OK |
| 6 | Snippets CK présents (6 + registry + groupe) | ✅ OK |
| 7 | Tokens SCSS depuis `tokens.md` (`primary_variables.scss`) | ✅ OK |
| 8 | Assets déclarés (`primary_variables`, `bootstrap_overridden`, frontend) | ✅ OK |
| 9 | Pas de B2B, pricelists, portail | ✅ OK |
| 10 | Pas de panier / checkout custom | ✅ OK |
| 11 | Pas de logique métier | ✅ OK |
| 12 | Périmètre ticket 01 respecté | ✅ OK |

---

## 3. Hors périmètre confirmé (absent du squelette)

```text
origines custom · collections custom · filtre prix avancé
portail B2B · configuration B2B · pricelists / devis / portail client
module métier · extension e-commerce · catalogue parallèle
front autonome · injection HTML maquette · JS catalogue
```

---

## 4. Points à suivre sur instance (recette fonctionnelle)

| # | Point | Statut instance |
|---|-------|-----------------|
| 1 | XPath `product_details` (`website_sale.product`) | ✅ Validé |
| 2 | XPath `snippets_registry` / `snippet_structure` | ✅ Validé |
| 3 | Placeholder produits vedettes — raccord Dynamic Products natif | ⚠️ Zone `oe_structure` — composition CMS MOA |
| 4 | Arbitrage Google Fonts / self-host / alternative | ⚠️ `@import` retiré · fallbacks système · self-host = arbitrage prod |
| 5 | Compilation SCSS (bundles Odoo 19) | ✅ Validé post-correction `@import` |
| 6 | Rendu `/shop`, fiche produit, responsive | ✅ Validé |
| 7 | Absence de régression Odoo standard | ✅ Validé |
| 8 | Installation module sur Odoo 19 CE | ✅ Validé |
| 9 | Snippets visibles et éditables Website Builder | ✅ Registry · composition CMS MOA |
| 10 | Critères §10 ticket 01 (recette complète) | ✅ OK socle · réserves CMS/prod |

---

## 5. Prochaine étape

```text
1. ✅ Mise à disposition instance Odoo 19 CE
2. ✅ Modules : website · website_sale · website_crm
3. ✅ Installation dorevia_ck_theme + activation thème website
4. ✅ Recette QA — OK install/QWeb · OK visuel post-correction
```

```text
Aucune extension hors ticket 01 autorisée.
```

---

## 6. Gouvernance

| Question | Statut |
|----------|--------|
| Squelette validé QA statique ? | ✅ Oui |
| Correction ciblée `ck-theme` ? | ✅ **OK QA** (2026-06-12) |
| Recette fonctionnelle ? | ✅ **OK install/QWeb · OK visuel post-correction** — 2026-06-12 |
| Extension hors ticket 01 ? | ❌ Non autorisée |

---

*Recette QA squelette — ticket `dorevia_ck_theme_01` — complément fonctionnel à produire post-instance.*
