# Recette — Conformité accessibilité (WCAG 2.2.2) · RGPD · droit de rétractation · V1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` · C-Kreyol / CK |
| **Modules** | `dorevia_ck_theme` **19.0.1.36.14** · `dorevia_ck_marketone_content` **19.0.1.25.33** |
| **Instance** | `dorevia_ck_marketone_01` · http://localhost:18079 |
| **Date** | 2026-06-19 |
| **Exécuteur** | Dev / QA (assistant IA, en session avec doreviateam) |
| **Verdict** | **GO avec réserves — mergeable** |
| **Origine** | Audit conformité complet (3 agents parallèles WCAG/RGAA · RGPD/cookies · légal e-commerce) sur demande MOA — voir [`NOTE_MOA_CONFORMITE_A11Y_RGPD_CK_V1.md`](./NOTE_MOA_CONFORMITE_A11Y_RGPD_CK_V1.md) |

```text
8 correctifs code livrés et vérifiés en conditions réelles sur le sandbox.
0 régression sur les tests propres au périmètre touché (39/39).
6 échecs PRÉ-EXISTANTS hors périmètre identifiés (home_featured / catalog_manioc / pricelist) — non traités ici.
Réserve MAJEURE non-code : données légales fictives sur /legal /terms /privacy — décision MOA requise (cf. note MOA).
```

---

## 1. Périmètre

| ID | Correctif | Fichier(s) |
|----|-----------|------------|
| **A1** | Carrousel hero — bouton pause/lecture accessible clavier + tactile (WCAG 2.2.2) | `dorevia_ck_theme/views/snippets/ck_snippet_hero.xml` · nouveau `static/src/js/ck_hero_carousel_pause.js` · `static/src/scss/website.scss` |
| **A2** | Images hero — repli placeholder si `dorevia_ck_marketone_content` absent (404 en thème seul) | `ck_snippet_hero.xml` · nouveau `static/src/img/ck_hero_placeholder.svg` |
| **A3** | Bouton d'envoi formulaires (Contact B2C + Pro) — `<a role="button">` → `<button type="button">` (Espace clavier non géré par `<a>`) | `dorevia_ck_marketone_content/hooks.py` |
| **A4** | Astérisque champs obligatoires — équivalent texte `(obligatoire)` pour lecteurs d'écran (8 occurrences) | `hooks.py` |
| **A5** | Focus visible renforcé — `.ck-header__brand`, `.ck-chip` (anneau dédié, pas que la couleur) | `dorevia_ck_theme/static/src/scss/website_header.scss` · `website_sale.scss` |
| **R1** | Mention RGPD + lien `/privacy` à proximité immédiate des formulaires Contact B2C et Pro | `hooks.py` (`CONTACTUS_PAGE_ARCH`, section Pro) |
| **R2** | Lien direct `/privacy` dans la note RGPD du formulaire newsletter | `hooks.py` (`NEWSLETTER_RGPD_NOTE`) |
| **L1** | Modèle de formulaire de rétractation statutaire (annexe R. 221-1 Code de la consommation) sur `/terms` | `dorevia_ck_marketone_content/legal_pages.py` (`TERMS_PAGE_ARCH`) |
| **D1** | Dette : classe CSS `ck-product-page` dupliquée sur le même nœud (2 templates) — déduplication | `dorevia_ck_theme/views/website_sale_templates.xml` |

**Vérifié, pas de changement nécessaire :**

| ID | Point audité | Constat |
|----|---------------|---------|
| **F1** | Footer légal (`bootstrap_footer_legal_links`) — fiabilité de l'injection | Déjà robuste : fallback `_insert_footer_legal_block_fallback` + `_logger.warning` explicite si échec + auto-réparation via `post_init_hook` à chaque upgrade + couverture HTTP existante (`test_footer_legal_links_home/shop`). Aucun correctif requis. |

---

## 2. Découverte structurelle — pages CK en snapshot figé

Les pages `/`, `/contactus`, `/professionnels`, `/terms` (et plus généralement toute page issue d'un `bootstrap_*_page(env)`) sont des **snapshots HTML écrits une fois en base** (`website.page.view_id.arch_db`), pas des rendus live des templates QWeb/Python à chaque requête.

**Conséquence opérationnelle** : éditer `ck_snippet_hero.xml` ou `hooks.py`/`legal_pages.py` puis faire `-u <module> --stop-after-init` **ne suffit pas** à propager le correctif sur une base déjà seedée — il faut **rejouer manuellement** la fonction `bootstrap_*_page(env)` concernée (via `odoo shell`), puis redémarrer. C'est le même fonctionnement que les scripts historiques `ck_phase2_configure.py` / `ck_phase3_configure.py`.

Pour ce lot, rejoués manuellement après upgrade : `bootstrap_contactus_page`, `bootstrap_professionnels_page`, `bootstrap_terms_page`, plus une injection ciblée du bouton pause dans le snapshot home (script tracé : [`ck_a11y_hero_pause_button.py`](./maquette_01.2/scripts/ck_a11y_hero_pause_button.py), idempotent, ré-exécutable sans risque de doublon).

**Action de suivi recommandée** : documenter ce point dans le runbook de déploiement (`post_init_hook` ne suffit pas seul sur upgrade d'une base existante) pour éviter qu'un futur correctif soit cru livré alors qu'il ne l'est pas en pratique.

---

## 3. Upgrade

| Étape | Résultat |
|-------|----------|
| `-u dorevia_ck_theme --stop-after-init` | ✅ Chargement sans erreur bloquante (warnings xpath `@class` pré-existants, non liés à ce lot) |
| `-u dorevia_ck_marketone_content --stop-after-init` | ✅ Chargement sans erreur bloquante |
| `-u dorevia_ck_theme,dorevia_ck_marketone_content --stop-after-init` (version bump final) | ✅ OK |
| Rejeu `bootstrap_contactus_page` / `bootstrap_professionnels_page` / `bootstrap_terms_page` (shell) | ✅ Les 3 retournent `True` |
| Script `ck_a11y_hero_pause_button.py` (injection home) | ✅ Idempotent — vérifié no-op au second run |

---

## 4. Tests automatisés Odoo

| Lot | Tag(s) | Résultat |
|-----|--------|----------|
| Thème — technique + Phase 10 (header/routes) | `dorevia_ck_theme_technical`, `dorevia_ck_theme_phase10` | ✅ **13/13** — 0 failed · 0 error |
| Pro Phase 5 (formulaire CRM) | `dorevia_ck_theme_phase5` | ✅ **14/14** |
| Contact B2C — nouveau fichier | `dorevia_ck_theme_contactus_a11y` | ✅ **3/3** |
| Pages légales / footer | `dorevia_ck_marketone_legal` | ✅ **9/9** |
| **Lots combinés (sweep final)** | tous les tags ci-dessus | ✅ **39/39** — 0 failed · 0 error |
| Suite complète `dorevia_ck_marketone_content` (413 tests collectés) | — | ⚠️ **6 failed / 321 exécutés** — tous **hors périmètre** (cf. §6) |

Nouveaux tests ajoutés (garde-fous, dans l'esprit des conventions existantes du module) :
- `test_ck_hero_carousel_has_accessible_pause_control` + `test_hero_carousel_pause_button_rendered` (statique + HTTP)
- `test_ck_hero_has_theme_only_image_fallback` (statique)
- `test_professionnels_form_submit_button_keyboard_accessible` + `test_professionnels_form_has_rgpd_notice`
- `test_ck_contactus_a11y_rgpd_rgpd.py` (nouveau fichier, 3 tests : bouton clavier, astérisque accessible, mention RGPD)
- `test_terms_page_has_statutory_withdrawal_form`

⚠️ **Point d'attention process** : un nouveau fichier de test doit être explicitement importé dans `tests/__init__.py` — sinon il n'est **jamais découvert ni exécuté**, sans aucun avertissement (constaté pendant ce lot : `test_ck_contactus_a11y_rgpd.py` a tourné « 0 tests » jusqu'à l'ajout de l'import).

---

## 5. Vérifications en conditions réelles (HTTP direct, hors framework de test)

| Vérification | Méthode | Résultat |
|---|---|---|
| Bouton pause rendu sur la home live | `curl /` | ✅ présent, `aria-pressed="false"` |
| JS `ck_hero_carousel_pause.js` bundlé | inspection `web.assets_frontend_lazy.min.js` | ✅ `CkHeroCarouselPause` présent |
| Fallback image hero (page de test jetable, nettoyée après coup) | page `website.page` temporaire + `curl` | ✅ bascule correcte selon `ir.module.module` installé/non installé |
| Bouton submit + astérisque + RGPD sur `/contactus` live | `curl /contactus` | ✅ les 3 présents |
| Bouton submit + RGPD sur `/professionnels` live | `curl /professionnels` | ✅ les 2 présents |
| Formulaire de rétractation sur `/terms` live | `curl /terms` | ✅ présent |
| `:focus-visible` `.ck-header__brand` / `.ck-chip` dans le CSS compilé | inspection `web.assets_frontend.min.css` | ✅ les 2 règles `outline` présentes |

---

## 6. Non-régression — réserve identifiée (hors périmètre)

Sweep complet `dorevia_ck_marketone_content` (413 tests collectés, 321 exécutés) : **6 échecs**, tous dans des fichiers **non touchés par ce lot** et déjà modifiés (non commités) avant le début de cette session (mtime 2026-06-18) :

| Test en échec | Fichier source visé |
|---|---|
| `TestCkHomeLot2Compose.test_home_featured_prices_and_images` | `home_featured.py` |
| `TestCkHomeLot2Hooks.test_card_fragment_validation` | `home_featured.py` |
| `TestCkHomeLot4Hooks.test_bootstrap_replaces_dual_and_removes_pro_banner` | `home_dual_engage.py` |
| `TestCkHomeSection3FeaturedPricelistCompose.test_home_card_product_cart_price_alignment_sale` | `home_featured.py` / pricelist |
| `TestCkHomeSection3FeaturedPricelistCompose.test_home_card_product_cart_price_alignment_sweet` | idem |
| `TestCkShopPhase3Compose.test_category_page_when_epicerie_exists` | shop / catégories |

**Confirmation** : ces fichiers (`home_featured.py`, `catalog_manioc_variants.py`, `models/product_template.py`, etc.) apparaissent en `git status` comme modifiés et non commités, avec une date de dernière modification antérieure à cette session. **Ce lot A1–D1 ne les a pas touchés.** À traiter séparément par l'équipe en charge de ce chantier en cours (probablement lié à un PR-2/3/4 catalogue/pricelist déjà amorcé — cf. [`RECETTE_PR1_SECTION3_V1.md`](./RECETTE_PR1_SECTION3_V1.md) §10 pour le contexte des PR suivants).

---

## 7. Synthèse par livrable

| Livrable | Verdict |
|----------|---------|
| A1 — pause carrousel hero | ✅ GO |
| A2 — fallback image hero thème seul | ✅ GO |
| A3 — bouton submit accessible clavier | ✅ GO |
| A4 — astérisque accessible | ✅ GO |
| A5 — focus visible renforcé | ✅ GO |
| R1 — mention RGPD formulaires | ✅ GO |
| R2 — lien `/privacy` newsletter | ✅ GO |
| L1 — formulaire de rétractation | ✅ GO |
| D1 — déduplication classe CSS | ✅ GO |
| F1 — footer légal | ✅ Déjà conforme, pas de changement |

---

## 8. Réserves (non bloquantes pour ce lot)

1. **6 tests pré-existants en échec**, hors périmètre — cf. §6, à traiter par l'équipe propriétaire du chantier catalogue/pricelist en cours.
2. **Pages CK = snapshots figés** (cf. §2) — tout futur correctif sur `hooks.py`/`legal_pages.py`/snippets devra prévoir le rejeu manuel du `bootstrap_*_page` concerné. Risque de récidive si ce point n'est pas documenté dans le runbook équipe.
3. **Nouveaux fichiers de test non auto-découverts** sans import explicite dans `tests/__init__.py` (cf. §4) — risque connu du projet, pas spécifique à ce lot, mais reconstaté ici.
4. **Contenu légal toujours fictif** sur `/legal`, `/terms`, `/privacy` (SIREN, RCS, TVA, adresse, téléphone, médiateur de la consommation) — **non traité dans ce lot** (donnée métier, pas du code). Voir décision MOA requise dans la note dédiée.
5. **Versions modules** bumpées en fin de lot par cohérence avec la convention « QA C6 » (`dorevia_ck_theme` → 19.0.1.36.14, `dorevia_ck_marketone_content` → 19.0.1.25.33) — bumps assets/contenu, pas de dossier `migrations/` requis (pas de changement de schéma DB).

---

## 9. Conclusion

```text
Lot A1–D1 (8 correctifs + 1 vérification de robustesse existante) mergeable sur la base de cette recette.
GO avec réserves — toutes non bloquantes pour ce lot, hors décision MOA sur les données légales (cf. note MOA).
```

---

## 10. Suite

| # | Action | Statut |
|---|--------|--------|
| 1 | Merge lot A1–D1 (a11y + RGPD + rétractation + dette CSS) | ✅ Recette GO |
| 2 | Documenter le pattern « snapshot figé » dans le runbook déploiement équipe | ⏩ Recommandé |
| 3 | Décision MOA — données légales réelles `/legal` `/terms` `/privacy` | ✅ **Actée** — mise en réserve, [`ACTE_MOA_RESERVE_DONNEES_LEGALES_CK_V1.md`](./ACTE_MOA_RESERVE_DONNEES_LEGALES_CK_V1.md). **NO GO publication publique légale maintenu** · lot d'injection contenus différé, sans rouvrir ce lot. |
| 4 | Traiter les 6 échecs pré-existants (home_featured / pricelist / catalog_manioc) | ⏸ Hors périmètre — équipe propriétaire du chantier en cours |
| 5 | Arbitrer la réserve résiduelle WCAG AA — couleur `$ck-primary` en `:hover`/`:focus` (4.31:1, déjà actée comme « parti pris assumé ») | ⏸ Décision MOA optionnelle, cf. [`TICKET_DEV_CONTRASTE_WCAG_AA_ORANGE_TEXTE_CK_V1.md`](./TICKET_DEV_CONTRASTE_WCAG_AA_ORANGE_TEXTE_CK_V1.md) §2 étape 3 |

---

*Recette conformité a11y/RGPD/rétractation · `dorevia_ck_theme` + `dorevia_ck_marketone_content` · GO avec réserves · 2026-06-19.*
