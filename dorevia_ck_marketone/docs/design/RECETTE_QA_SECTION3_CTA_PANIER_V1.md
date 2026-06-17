# Recette QA — Section 3 · CTA « Ajouter au panier » · V1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` · C-Kreyol / CK |
| **Lot** | **CTA panier vedettes** — conversion directe section « Nos coups de cœur » |
| **Modules** | `dorevia_ck_marketone_content` **19.0.1.25.1** · `dorevia_ck_theme` **19.0.1.31.3** |
| **Instance** | `dorevia_ck_marketone_01` · http://localhost:18079 |
| **Date** | 2026-06-17 |
| **Exécuteur** | Dev / QA |
| **Verdict** | **GO MOA** — recette visuelle §4 validée 2026-06-17 |
| **Source MOA** | Demande MOA — dual CTA vedettes home |

```text
CTA principal : Ajouter au panier (service cart Odoo 19 /shop/cart/add).
CTA secondaire : Voir le produit (outline / lien mobile).
Périmètre : section home « Nos coups de cœur » uniquement — pas de refonte checkout.
```

---

## 1. Périmètre livré

| ID | Livrable | Fichier |
|----|----------|---------|
| **H1** | HTML dual-CTA SSR + éligibilité `_featured_variant_allows_quick_add` | `home_featured.py` |
| **H2** | Détection arch périmée `_featured_arch_missing_cart_cta` (bootstrap + sync boot) | `home_featured.py`, `models/product_template.py` |
| **H3** | Interaction panier Odoo 19 (`Interaction` + service `cart`) | `static/src/js/ck_featured_cart_add.js` |
| **H4** | Styles hiérarchie CTA desktop/mobile | `dorevia_ck_theme/static/src/scss/website.scss` |
| **H5** | Migration fail-fast reconstruction home | `migrations/19.0.1.25.0/post-migrate.py` |

**Hors périmètre (confirmé)** : refonte cards globales · tunnel checkout · logique panier custom · gestion variantes au-delà du standard Odoo · boutique / catégories.

---

## 2. Upgrade

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 \
  -u dorevia_ck_marketone_content,dorevia_ck_theme --stop-after-init --no-http
```

| Étape | Résultat attendu |
|-------|------------------|
| Chargement modules sans erreur | ✅ |
| Migration `25.0` — bootstrap home | ✅ CTA panier présents dans `ir_ui_view` |
| Sync boot — arch périmée sans CTA | ✅ Reconstruction loguée |

**Contrôle post-upgrade (shell ou SQL)** :

```text
card-cart-cta count ≥ 1 (3 en curation recette)
product-card-actions count ≥ 1
```

---

## 3. Tests automatisés Odoo

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 \
  --test-enable --stop-after-init --no-http --http-port=8071 \
  --test-tags=dorevia_ck_marketone_home_section3,dorevia_ck_marketone_home_section3_curation
```

| Lot | Résultat attendu |
|-----|------------------|
| Section 3 hooks + compose + curation | ✅ **31/31** — 0 failed · 0 error |

**Points couverts par les tests** :

- Présence `card-cart-cta` + `card-cta--secondary` dans l'arch home
- Produit `sale_ok=False` → pas de bouton panier (`product-card-actions--view-only`)
- Validateur `card_fragment_is_valid` compatible classe secondaire
- Non-régression prix, cover, étiquettes, ordre trust-bar → vedettes

---

## 4. Grille MOA — 10 critères d'acceptation

| # | Critère MOA | Procédure | Résultat |
|---|-------------|-----------|----------|
| 1 | CTA « Ajouter au panier » sur chaque card vedette éligible | Home `/fr` — 3 cards curation | ✅ |
| 2 | CTA « Voir le produit » conservé | Lien `card-cta--secondary` sur chaque card | ✅ |
| 3 | Hiérarchie visuelle : panier > voir produit | Desktop 1280 + mobile 390 | ✅ |
| 4 | Clic panier → ajout via mécanisme standard Odoo | Playwright — clic Confiture | ✅ |
| 5 | Compteur panier header mis à jour | `.my_cart_quantity` 0 → 1 | ✅ |
| 6 | Produits simples cohérents (Confiture, Manio salé/sucré) | 3 boutons panier présents | ✅ |
| 7 | Accès fiche produit intact | Cover + lien secondaire (structure inchangée) | ✅ (code) |
| 8 | Lisibilité desktop | Pas d'overflow · 3 CTA visibles | ✅ |
| 9 | Lisibilité mobile | `scrollWidth=390` · pas d'overflow | ✅ |
| 10 | Aucun contournement checkout standard | Service `cart` natif · pas de redirect checkout | ✅ |

**Script recette** : `maquette_01.2/scripts/ck_section3_cta_panier_recette.mjs`  
**Captures** : `maquette_01.2/captures/recette_section3_cta_panier/` · rapport JSON `verdict: GO`  
**Prérequis runtime** : redémarrage Odoo après upgrade pour recharger le bundle `web.assets_frontend_lazy` (interaction JS).

**Produit non éligible (optionnel)** : désactiver `sale_ok` sur une vedette test → rebuild home → seul « Voir le produit ».

---

## 5. Contrôles navigateur détaillés

### 5.1 Desktop (1280px)

| Contrôle | Attendu |
|--------|---------|
| Structure card foot | Prix · unité · `[Ajouter au panier]` + `[Voir le produit]` côte à côte |
| Style bouton panier | Plein couleur primaire CK |
| Style lien produit | Outline secondaire |
| Overlay cover | Clic zone média/titre → fiche produit |
| Clic bouton panier | Pas de navigation ; compteur + notification cart native si stock/lot |

### 5.2 Mobile (390px)

| Contrôle | Attendu |
|--------|---------|
| Empilement CTA | Bouton panier pleine largeur · lien « Voir le produit » dessous |
| Pas d'overflow horizontal | `scrollWidth ≤ viewport` |
| Bouton prioritaire | « Ajouter au panier » reste l'action dominante |

### 5.3 Erreur réseau / RPC (25.1+)

| Contrôle | Attendu |
|--------|---------|
| Échec `/shop/cart/add` | Toast danger « Impossible d'ajouter… » (service `notification`) |
| Bouton réactivé | `disabled` retiré après échec |
| Avertissement stock Odoo | Toast / notification cart native via `notification_info.warning` (service `cart`) |

---

## 6. Revue code QA (synthèse)

| Point | Verdict |
|-------|---------|
| Éligibilité sans requête HTTP mockée | ✅ Alignée `_website_show_quick_add` |
| Endpoint panier | ✅ Standard — service `cart` → `/shop/cart/add` |
| Conflit overlay / CTA | ✅ z-index foot 2 > cover 1 + `prevent` JS |
| Self-healing arch | ✅ Bootstrap + sync startup |
| Feedback erreur (25.1) | ✅ `catch` + `notification` · warnings via service `cart` |
| Points non bloquants | `aria-label` bouton générique · double calcul prix (micro-opt) |

---

## 7. Non-régression

| Zone | Contrôle |
|------|----------|
| Hero S4 / trust-bar | Ordre sections inchangé |
| Prix vedettes PR-4 | 5,80 € · 3,50 € · 3,50 € (recette) |
| `/shop` natif | Aucun template shop modifié par ce lot |
| Cron sync vedettes PR-3 | Inchangé |

---

## 8. Verdict

| Statut | Condition |
|--------|-----------|
| **GO MOA** | Tests §3 verts · upgrade §2 OK · grille §4 validée (Playwright 2026-06-17) |

---

## 9. Références

- Note architecture Section 3 : [`maquette_01.2/NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md`](./maquette_01.2/NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md)
- Recette campagne PR-1→4 : [`RECETTE_PR1_SECTION3_V1.md`](./RECETTE_PR1_SECTION3_V1.md)
- Doctrine durcissement : [`maquette_01.2/SYNTHESE_CAMPAGNE_DURCISSEMENT_SECTION3_PR1_PR4_V1.md`](./maquette_01.2/SYNTHESE_CAMPAGNE_DURCISSEMENT_SECTION3_PR1_PR4_V1.md) (si présente)
