# Synthèse campagne — Durcissement Section 3 / vedettes CK · PR-1 → PR-4 + CTA panier · V1.1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` · C-Kreyol / CK |
| **Module** | `dorevia_ck_marketone_content` — version finale **19.0.1.25.1** (+ `dorevia_ck_theme` 19.0.1.31.3) |
| **Instance recette** | `dorevia_ck_marketone_01` · http://localhost:18079 |
| **Période** | 2026-06-17 |
| **Origine** | Rapports QA code [`RAPPORT_QA_CODE_DOREVIA_CK_THEME_20260617.docx`](../RAPPORT_QA_CODE_DOREVIA_CK_THEME_20260617.docx) · [`RAPPORT_QA_CODE_DOREVIA_CK_MARKETONE_CONTENT_20260617.docx`](../RAPPORT_QA_CODE_DOREVIA_CK_MARKETONE_CONTENT_20260617.docx) |
| **Recettes** | [`RECETTE_PR1_SECTION3_V1.md`](../RECETTE_PR1_SECTION3_V1.md) · [`RECETTE_QA_SECTION3_CTA_PANIER_V1.md`](../RECETTE_QA_SECTION3_CTA_PANIER_V1.md) |
| **Statut** | **Clôturée côté code · 4 PR durcissement + livraison CTA panier mergeables** |

> **V1.1 (2026-06-17)** — addendum : livraison CTA « Ajouter au panier » Section 3 (`19.0.1.25.0` + durcissement `19.0.1.25.1`) ; doctrine **D9**.

```text
Document de référence opposable — fige les décisions de doctrine issues du
durcissement QA et la dette résiduelle. À lire avant reprise/onboarding QA.
```

---

## 1. Contexte

Deux revues de code statiques (thème + contenu) ont produit une liste de constats notés par sévérité. Les correctifs sûrs et les trois points structurels (H1/H2/H3) ont été traités en **4 PR séquencées**, chacune recettée sur l'instance Docker avant merge, en respectant un découpage à surfaces de régression séparées (H1 et H2 jamais ensemble, guard H3 distinct de la refonte QWeb).

Garde-fou méthode : pas de migration QWeb, pas de changement de seuil produit, pas de refonte home dans cette campagne — durcissement uniquement.

---

## 2. Les PR (durcissement) + livraison CTA

| PR | Version | Contenu | Verdict recette |
|----|---------|---------|-----------------|
| **PR-1** | 19.0.1.21.16 | **L1** sanitization couleurs ruban (`_safe_css_color`) · **M2** footer légal robuste (repli + `_logger.warning`) · **M4** doc SQL direct · **M1** scope refresh vedettes (`_ck_touches_featured`) | GO avec réserves |
| **PR-2** | 19.0.1.22.0 | **M1 mode repli** (`featured.product_tmpl_ids`) · **guard empreinte CMS** dans `_bootstrap_cms_page` · module socle `home_arch.py` · **migration freeze** baseline | GO |
| **PR-3** | 19.0.1.23.0 | **H2** — suppression de l'override `ir_http._pre_dispatch` (écriture `arch_db` en GET) · **cron** `ck_cron_sync_home_featured` (30 min) | GO avec réserve (test hooks) |
| **PR-4** | 19.0.1.24.0 | **H1** — calcul de prix sans requête mockée (candidat B : `get_pricelist_available` → `_get_product_price` → `_apply_taxes_to_price`) · suppression `_with_website_request` + imports mock | GO |
| **CTA panier** | 19.0.1.25.0 → **.25.1** | **Quick-add vedettes** — dual-CTA SSR (`_featured_variant_allows_quick_add`), JS `ck_featured_cart_add.js` (service `cart` natif Odoo 19), self-healing `_featured_arch_missing_cart_cta`, migration 25.0. Durcissement 25.1 : `services.cart.add` + `catch`/notification, suppression sync compteur dupliqué. | GO mergeable (réserve QA levée) |

Côté thème (préalable, hors numérotation PR) : tests Phase 10 isolés (skip si contenu absent), retrait de `active` sur le slide hero insérable, commentaires de clarification (sticky dupliqué, dépendance images contenu, versionnage), signalement RGPD polices.

---

## 3. Doctrine figée (décisions opposables)

| # | Décision | Portée |
|---|----------|--------|
| **D1** | **Home pilotée par le code / self-healing** — les sections home se reconstruisent si l'arch est invalide ; les éditions MOA conservant une arch valide (images via media dialog) sont préservées, le wording reste code-owned. | `home_hero/univers/discovery/dual/editorial/reassurance` |
| **D2** | **Vedettes data-driven** — `bootstrap_home_featured_products` re-patche sa section à partir du BO (prix, curation) ; comportement spécifique conservé, hors guard empreinte. | `home_featured` |
| **D3** | **Refresh vedettes scopé curation** — un `write` produit ne reconstruit la home que si le produit appartient à « Coups de cœur » peuplée ; sinon (mode repli auto) comportement large conservé. | `product.template.write` |
| **D4** | **Pages CMS protégées MOA** — guard par empreinte (`ck_seed_arch.{view_key}`) : une page éditée en BO n'est plus écrasée au bootstrap ; empreinte posée après écriture (forme normalisée). | `_bootstrap_cms_page` |
| **D5** | **Freeze baseline obligatoire** — migration sans `view.write` posant les empreintes courantes ; précondition : exécuter avant toute édition MOA des pages CMS. | `migrations/19.0.1.22.0` |
| **D6** | **Aucune écriture `arch_db` pendant un GET** — l'auto-réparation passe par les write-triggers ORM (immédiat) + cron 30 min (cas hors-ORM). Staleness max acceptée : ~30 min. | `ir.http` retiré · cron |
| **D7** | **Pricing sans requête mockée** — prix B2C calculé via pricelist + position fiscale + `_apply_taxes_to_price`, sans simuler `odoo.http.request`. | `_get_featured_price_amount` |
| **D8** | **B1 (refactor guards home) écarté** — `bootstrap_home_univers` ne rentre pas dans un helper générique (conditions + effets de bord) ; gain cosmétique, non retenu. `should_reseed_home_section` reste disponible dans `home_arch.py` comme helper futur, non câblé. | — |
| **D9** | **Quick-add vedettes** — CTA « Ajouter au panier » sur les cards éligibles : éligibilité alignée sur `_website_show_quick_add` **sans requête** (combo exclu, `sale_ok`, publié, `_is_add_to_cart_possible`, `prevent_zero_price_sale`) ; ajout via le **service `cart` natif Odoo 19** (notifications stock/erreur natives), **pas de checkout custom** ; détection d'arch périmée `_featured_arch_missing_cart_cta` câblée bootstrap + sync (cohérent D6, aucune écriture en GET). | `home_featured` · `ck_featured_cart_add.js` |

---

## 4. Recettes (instance `dorevia_ck_marketone_01`)

| PR | Tests automatisés | Contrôles clés |
|----|-------------------|----------------|
| PR-1 | 44/44 + 8/8 (legal) | L1 filtre `javascript:` · footer `/legal /privacy /terms` · M1 curation OK |
| PR-2 | 20/20 (`cms_guard` + section3 + legal) | stabilité empreinte confirmée · freeze 8 pages · upgrade idempotent |
| PR-3 | 18/18 puis 10/10 | cron actif `nextcall` posé · **log read-only transaction absent** · `test_stale_arch_rebuilt_by_sync` |
| PR-4 | 30/30 | prix HTTP 5,80 € / 3,50 € / 3,50 € · parité mock 6/6 (admin + public) · log read-only absent |
| CTA panier | 31/31 (section3 + curation) | 3 CTA injectés · clic → compteur header MAJ · self-healing CTA OK · recette visuelle §4 (clic réel + mobile 390) **en attente MOA** |

Garde-fou non-régression : suites `dorevia_ck_marketone_home_section3` et `dorevia_ck_marketone_cms_guard` vertes à chaque PR.

> **Note déploiement** — Après un `-u` touchant des assets JS frontend (ex. CTA panier `ck_featured_cart_add.js`), **redémarrer le worker Odoo** pour régénérer les bundles `web.assets_frontend(_lazy)` : sans restart, l'interaction publique n'est pas servie et le clic ne déclenche rien. Vaut pour tout déploiement modifiant des assets, pas seulement ce CTA.

---

## 5. Dette résiduelle (hors campagne)

| ID | Sujet | Statut |
|----|-------|--------|
| **Lot2 seuil** | Tests `test_ck_home_lot2_*` échouent en mode curation (3 vedettes < seuil auto `MIN_FEATURED_PRODUCTS = 5`) — conflit de doctrine de seuil, indépendant du pricing. | Ticket séparé (périmètre étroit) |
| **C3 polices** | Google Fonts en CDN — auto-hébergement à faire (enjeu RGPD). | Chantier distinct |
| **H3 cible QWeb** | Migration des pages/sections (chaînes Python → templates QWeb XML, éditables/traduisibles). | Long terme, page par page |
| **B1 home** | Refactor DRY des guards home — volontairement écarté (D8). | Non planifié |
| **Heuristiques nom** | `name ilike 'goyav'` / fragments démo pour origines/catégories. | À piloter par données avant montée en charge |

---

## 6. Verrous go-live public

| Verrou | Détail | Statut |
|--------|--------|--------|
| **Contenu légal réel** | `/legal` `/privacy` `/terms` contiennent des données fictives marquées `[FICTIF]` + bandeau « recette interne ». | **NO GO public** maintenu |
| **RGPD polices (C3)** | IP visiteur transmise à Google Fonts. | À lever avant publication |

Les write-triggers + cron couvrent l'exploitation interne ; ces deux verrous restent bloquants pour une ouverture publique.

---

## 7. Reste à faire (post-merge)

- Commit global des 4 PR + livraison CTA panier (`git rm models/ir_http.py` inclus — stub neutralisé, suppression physique bloquée en sandbox).
- **Recette visuelle CTA §4** (clic panier réel + rendu mobile 390) — seul élément non-code restant avant validation MOA finale.
- Ticket lot2 (cf. [`TICKET_LOT2_SEUIL_VEDETTES_CURATION_V1.md`](./TICKET_LOT2_SEUIL_VEDETTES_CURATION_V1.md)).
- Chantiers distincts : C3 polices · contenu légal réel · H3 QWeb.

---

*Synthèse campagne durcissement Section 3 · PR-1 → PR-4 + CTA panier · `dorevia_ck_marketone_content` 19.0.1.25.1 · 2026-06-17.*
