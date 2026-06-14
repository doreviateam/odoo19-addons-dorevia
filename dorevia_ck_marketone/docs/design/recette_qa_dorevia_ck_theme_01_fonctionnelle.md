# Recette QA fonctionnelle — `dorevia_ck_theme` (ticket 01)

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Module** | `dorevia_ck_theme` |
| **Ticket source** | [`ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md`](./ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md) |
| **Instance** | [`REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md`](./REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md) |
| **Recette squelette** | [`recette_qa_dorevia_ck_theme_01_squelette.md`](./recette_qa_dorevia_ck_theme_01_squelette.md) — **OK statique** |
| **Date** | 2026-06-12 |
| **Statut QA** | **Socle ticket 01 clôturé — phase CMS MOA** |

---

## 1. Verdict actuel

```text
OK INSTALLATION / QWEB — RECETTE VISUELLE KO (constat MOA/QA)
→ CORRECTION CSS CIBLÉE APPLIQUÉE
→ OK RECETTE VISUELLE POST-CORRECTION
```

| Couche | Verdict |
|--------|---------|
| Installation modules · xpath QWeb · snippets registry | ✅ OK |
| Contrôles automatisés HTTP / DB | ✅ OK |
| **Recette visuelle navigateur** | ❌ **KO bloquant** (bundle CSS cassé) |
| **Correction `@import` Google Fonts** | ✅ Appliquée ticket 01 — §8 |
| **Recette visuelle post-correction** | ✅ OK — [`recette_qa_dorevia_ck_theme_01_visuelle_post_correction.md`](./recette_qa_dorevia_ck_theme_01_visuelle_post_correction.md) |

> Le verdict « OK recette fonctionnelle avec réserves » (matin 2026-06-12) a été **rétrogradé**, puis repris après correction CSS. La recette visuelle post-correction valide le socle ticket 01, avec réserves CMS/prod maintenues.

---

## 2. Constats recette visuelle (bloquant)

**Symptôme** : HTML brut — liens bleus, `Times`, logo énorme, layout Odoo non stylé.

**Confirmé navigateur** :

| Contrôle | Résultat |
|----------|----------|
| `<body class="ck-theme">` | ✅ Présent |
| Lien `web.assets_frontend.min.css` | ✅ Présent |
| Styles calculés (typo, couleurs CK) | ❌ Natifs navigateur |
| Règles CSS effectives sur la page | ❌ ~2 règles seulement |

**Cause racine** : `@import url(...)` Google Fonts (Fraunces + DM Sans) dans `website.scss`, concaténé tel quel en tête du bundle Odoo. L’URL est **tronquée** avant `@charset`, ce qui invalide quasi tout le CSS :

```css
@import url("https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;

/* <inline asset> */
@charset "UTF-8";
...
0,9..40,600;0,9..40,700...
```

**Hors cause** : xpath `ck-theme` · `website.theme_id` · absence de thème actif (problème distinct, corrigé en amont).

---

## 3. Prérequis instance

| # | Prérequis | Statut | Note |
|---|-----------|--------|------|
| 1 | Base `dorevia_ck_marketone_01` HTTP 200 | ✅ | |
| 2 | Modules `website` · `website_sale` · `website_crm` · `dorevia_ck_theme` | ✅ | |
| 3 | **`website.theme_id` = `dorevia_ck_theme`** | ✅ | Obligatoire Odoo 19 pour inclure les SCSS theme dans le bundle |
| 4 | Purge assets après upgrade SCSS | ✅ | `ir.attachment` `/web/assets/%web.assets_frontend%` + restart |

---

## 4. Checklist recette (état post-analyse visuelle)

| # | Point | Verdict | Note |
|---|-------|---------|------|
| 1 | Installation `dorevia_ck_theme` | ✅ | |
| 2 | Installation socle `website` / `website_sale` / `website_crm` | ✅ | |
| 3 | Vues QWeb (11 clés `dorevia_ck_theme.*`) | ✅ | |
| 4 | **Compilation assets frontend — valide navigateur** | ✅ | KO avant correction · fix §8 · recette visuelle post-correction OK |
| 5 | XPath `products_ck_theme` (`ck-shop-page`) | ✅ | |
| 6 | XPath `layout_ck_theme` (`ck-theme`) | ✅ | |
| 7 | XPath `product_ck_theme` (`ck-product-chips`) | ✅ | |
| 8 | Groupe `CK Marketone` · 6 snippets registry | ✅ | |
| 9 | Rendu `/shop` · fiche produit HTTP 200 | ✅ | Template natif |
| 10 | Responsive smoke · panier · checkout | ✅ | |
| 11 | Absence B2B / models custom | ✅ | |
| 12 | Placeholder vedettes Dynamic Products | ⚠️ | Composition CMS MOA |
| 13 | Typo Fraunces + DM Sans | ⚠️ | Fallbacks système ticket 01 · self-host = arbitrage prod |

---

## 5. Contrôles automatisés (limites)

Script recette matin : **49 / 51** OK — **insuffisant** pour valider le rendu visuel.

| Contrôle auto | Limite constatée |
|---------------|------------------|
| Token `#d84315` dans fichier CSS | Présent dans le blob même si bundle invalide navigateur |
| Classe `ck-theme` dans fichier CSS | Idem |
| HTTP 200 sur asset CSS | 200 possible avec CSS syntaxiquement cassé |

**Leçon QA** : ajouter contrôle « `@charset` unique · pas d’`@import` URL tronquée · styles calculés `.ck-theme` background-color » en recette visuelle.

---

## 6. Réserves non bloquantes (hors CSS)

- Vedettes : zone `oe_structure` — Dynamic Products = CMS MOA
- Page Pro : composition CMS MOA
- Typo prod : Fraunces/DM Sans hors scope ticket 01 (self-host ou asset dédié ultérieur)

---

## 7. Hors périmètre confirmé

```text
origines custom · collections custom · B2B custom · catalogue parallèle
models/controllers custom · extension hors ticket 01
```

---

## 8. Correction ciblée CSS (ticket 01 — autorisée)

**Fichiers modifiés** :

| Fichier | Changement |
|---------|------------|
| `static/src/scss/website.scss` | Suppression `@import url(...)` Google Fonts |
| `static/src/scss/primary_variables.scss` | Fallbacks système : `georgia` · `system-ui` |

**Contrôle post-fix (automatisé)** :

| Contrôle | Résultat |
|----------|----------|
| URL Google Fonts CK absente du bundle | ✅ |
| `@charset` unique | ✅ |
| `.ck-theme` avec `background-color: #fffbf7` compilé | ✅ |
| Token `#d84315` compilé | ✅ |
| ~8000+ blocs CSS dans bundle minifié | ✅ |

**Action instance** : `odoo -u dorevia_ck_theme` · purge attachments frontend · restart conteneur · hard refresh navigateur.

---

## 9. Recette visuelle post-correction

Référence : [`recette_qa_dorevia_ck_theme_01_visuelle_post_correction.md`](./recette_qa_dorevia_ck_theme_01_visuelle_post_correction.md)

| Contrôle | Statut |
|----------|--------|
| Bundle CSS interprété par navigateur | ✅ 5625 règles CSS lues |
| `body.ck-theme` | ✅ `/` · `/shop` · fiche produit |
| Fond CK `#fffbf7` appliqué | ✅ |
| Typographie fallback système appliquée | ✅ |
| Plus de rendu HTML brut / Times / liens bleus natifs | ✅ |
| `/shop` avec `ck-shop-page` | ✅ |
| Fiche produit avec `ck-product-page` / `ck-product-chips` | ✅ |
| Responsive smoke mobile | ✅ |
| Panier / checkout natifs | ✅ |
| Pas de B2B/pricelist UI publique | ✅ |

Verdict :

```text
OK RECETTE VISUELLE POST-CORRECTION — SOCLE TICKET 01 VALIDÉ
```

---

## 10. Prochaine étape

```text
1. ✅ Socle ticket 01 — clôturé
2. ⏳ Phase CMS MOA — Website Builder uniquement (accueil · page Pro)
3. ☐ Arbitrage typo Fraunces/DM Sans prod
4. Extensions : ticket séparé + arbitrage MOA uniquement
```

---

*Recette QA fonctionnelle — ticket `dorevia_ck_theme_01` — socle clôturé 2026-06-12.*
