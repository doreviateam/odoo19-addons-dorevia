# Recette QA — PR #73 · Section 3 « Nos coups de cœur »

| Champ | Valeur |
|-------|--------|
| **PR** | #73 — `feat/ck-home-section3-featured-images` |
| **Commits** | `3b96008` (feature) + `5cfece6` (fix tests) · base `e9a2965` (#72 mergé) |
| **Périmètre** | Section 3 home — SSR cartes maquette + alignement catalogue MOA |
| **Type de revue** | Revue de **code** (architecture, SSR, catalogue, SCSS, tests) + observation visuelle desktop partielle |
| **Modules** | `dorevia_ck_marketone_content` 19.0.1.14.0 → **19.0.1.17.0** · `dorevia_ck_theme` 19.0.1.25.1 → **19.0.1.27.0** |
| **Verdict** | **GO sous réserves** (favorable au merge — voir §4) |

> Note de méthode : la recette visuelle « live » (1280 / 390, clics « Voir », BO, `/shop`) n'a pas pu être pilotée automatiquement dans cette session, et la suite de tests n'est pas rejouable hors de l'environnement Docker recette. La revue ci-dessous est donc **fondée sur le code de la branche** et sur la couverture statique des tests ; les points nécessitant une confirmation runtime sont explicitement signalés.

---

## 1. Synthèse

La PR est **propre, cohérente avec la note d'architecture** et **fidèle à la maquette**. Le rendu de la Section 3 est une couche SSR custom CK (`home_featured.py`) qui lit les produits publiés dans Odoo (source de vérité) et génère des cartes au format maquette V1.2. Le modèle catalogue MOA (parent **Manio Crackers** + 2 variantes **Format**, **Galettes de manioc** en produit séparé) est explicitement construit/réparé et couvert par des tests dédiés.

Comparaison maquette ↔ SSR : structure **identique** (mêmes classes `product-card`, `product-card-media`, `badge badge-heart`/`badge-new badge-float`, `product-meta`, `chip-origin`, `chip-cat`, `product-card-foot`, `price`, `card-cta`, en-tête `#featured-title` + sous-titre + CTA `btn-secondary`). Les seules différences relèvent des **données** (images et prix réels Odoo au lieu des visuels Unsplash et prix factices de la maquette) — ce qui est exactement la doctrine retenue.

---

## 2. Checklist MOA — 11 points

| # | Contrôle | Verdict | Base |
|---|----------|---------|------|
| 1 | Rendu « Nos coups de cœur » proche maquette | ✅ **OK** | Structure SSR identique aux classes de `artifact/index.html`. Desktop observé conforme. |
| 2 | Images visibles · hauteur stable (> 0px) | ✅ **OK (structure)** · ⚠️ réserve image | `.product-card-media` en `aspect-ratio: 1/1` → hauteur stable même sans photo ; sélection exige une image. Voir réserve §4.1. |
| 3 | Variantes Manio Crackers salé / sucré | ✅ **OK** | Une carte par variante (`_template_featured_variant_cap`), libellés `Manio Crackers salé/sucré`, URL `?attribute_values=` (testé). |
| 4 | Modèle MOA : parent Manio + 2 variantes Format | ✅ **OK** | `catalog_manioc_variants._ensure_manioc_crackers_parent` + test `test_manioc_crackers_parent_two_format_variants`. |
| 5 | Galettes = produit séparé | ✅ **OK** | `_ensure_galettes_separate_product` (template distinct, sans `attribute_line_ids`) + test dédié. |
| 6 | Aucun produit fantôme | ✅ **OK** · note gouvernance | Dépréciation des anciens templates crackers séparés (`active=False`) ; sélection limitée aux produits BO publiés ; test `assertNotIn('manio-crackers-sale-5')`. Voir note §3.2. |
| 7 | Liens « Voir » → bonnes fiches/variantes | ✅ **OK** | `variant.website_url` (avec `attribute_values`) ; assertion `attribute_values=` dans l'arch home. |
| 8 | Prix issus d'Odoo | ✅ **OK** | `_get_featured_price_label` via `template._get_combination_info(...)` puis fallback `list_price`. (En recette, tous à 1,00 € = données de recette.) |
| 9 | `/shop` natif non modifié | ✅ **OK (code)** · smoke recommandé | Le SSR ne patche que la home `/` ; aucun template/route `/shop` modifié dans la PR. Confirmer par smoke runtime. |
| 10 | Mobile 390 sans overflow | ✅ **OK probable (code)** · à confirmer | Grille `repeat(3,1fr)` → 2 col ≤1023px → **1 col ≤479px** ; pas de largeur fixe ; `overflow:hidden` sur la carte. Confirmer `scrollWidth = 390` runtime. |
| 11 | Non-régression Sections 1 & 2 | ✅ **OK** | Aucun fichier Hero modifié par la PR (`git diff`). Hero `data-bs-interval="25000"` (`home_hero.py`) verrouillé par `test_ck_home_lot1_*` **et** `test_ck_home_section2_trust_bar_compose`. Ordre trust-bar → vedettes testé (`test_bootstrap_order_trust_bar_before_featured`). Hero + trust-bar observés intacts. |

**Bilan : 11/11 favorables**, dont 4 avec confirmation runtime conseillée (2, 9, 10) ou réserve image documentée (2).

---

## 3. Revue technique — au-delà de la checklist

### 3.1 ⚠️ Dette technique — calcul du prix via requête HTTP mockée *(non bloquant)*

`_with_website_request` (`home_featured.py`) construit une **fausse requête HTTP** (`Mock`, `MagicMock`, `patch`, `EnvironBuilder`, push sur `odoo.http._request_stack`) pour pouvoir appeler `_get_combination_info` hors d'un contexte WSGI — y compris depuis les **post-migrate** (`bootstrap_home_featured_products`).

- Risque : dépend d'internals `odoo.http` susceptibles d'évoluer ; si `_get_combination_info` lève dans ce contexte, l'exception remonte et peut interrompre le bootstrap/migration (et donc le rendu de la section).
- Recommandation : encadrer le calcul prix d'un `try/except` avec repli explicite sur `list_price`, et tracer un ticket pour remplacer le mock par un contexte website natif. **Non bloquant** (tests verts, rendu OK), mais à suivre.

### 3.2 Note gouvernance — sélection des « vedettes »

`get_ready_featured_variants` retient les **5 premiers** produits publiés avec image (`order='website_sequence asc, id asc'`), sans flag « vedette » explicite. Le set MOA attendu (Confiture de goyave, Manio salé, Manio sucré, Galettes, Savon vétiver) est garanti par la **donnée BO / `website_sequence`**, pas par un marquage produit. Conséquence : publier en BO un nouveau produit à faible séquence peut modifier les vedettes. À acter MOA (gouvernance catalogue) — cohérent avec la doctrine « BO source de vérité ».

### 3.3 Note — chips origine / catégorie partiellement heuristiques

`_get_featured_origin_label` / `_get_featured_category_label` lisent d'abord l'attribut **Origine** puis la description ; **à défaut**, ils retombent sur un mapping codé par fragment de nom (`'goyav'→Réunion`, `'manio'→Guadeloupe`, …). Donc un chip « Réunion »/« Guadeloupe » peut être **éditorial codé** et non issu d'une donnée BO. Acceptable en V1, mais à confirmer côté MOA si ces origines doivent exister en BO pour respecter strictement « BO = source de vérité ».

---

## 4. Réserves

### 4.1 ⚠️ Réserve image — à étendre à « Confiture de goyave »

La réserve documentée ne mentionne que **Galettes de manioc** (placeholder). Or :

- **Galettes de manioc** reçoit un PNG **1×1 transparent** (`_PLACEHOLDER_PNG`) → rendu en zone crème vide (`$ck-image-zone: #faf6f0`). Réserve connue.
- **Confiture de goyave** s'affiche en **aplat rouge plein** : ce n'est ni le CSS (zone média = crème) ni le code de la PR (ce produit n'est pas créé par `catalog_manioc_variants`) — c'est une **image placeholder rouge stockée dans la base de recette**. Cette occurrence **n'est pas documentée** dans la réserve.

→ Action : étendre la réserve « image à remplacer par la vraie photo BO » à **Confiture de goyave** (en plus de Galettes) avant la validation visuelle finale Section 3. **Non bloquant pour le merge** (la hauteur reste stable, le rendu n'est pas cassé), bloquant pour la *validation visuelle finale*.

### 4.2 Confirmation tests avant merge

La suite n'a pas pu être rejouée depuis l'environnement de revue (pas de Docker/Odoo, `localhost:18079` injoignable). La couverture statique est **solide** (16 méthodes pertinentes couvrant header, ordre, cartes ≥5, médias ≥5, prix/CTA, variantes, parent/Galettes, URL `attribute_values`, absence d'ancien slug, absence de carrousel natif). Le résultat consigné est **31 tests / 0 failed**.

→ Action **avant merge** : rejouer la commande sur l'état actuel de la branche (`5cfece6`) pour confirmer :

```bash
docker exec sandbox-odoo19-odoo-1 bash -c \
  'odoo -d dorevia_ck_marketone_01 --http-port=8079 --no-http \
   -u dorevia_ck_theme,dorevia_ck_marketone_content \
   --test-tags dorevia_ck_marketone_home_section3,dorevia_ck_marketone_catalog_manioc,dorevia_ck_marketone_home_section2,dorevia_ck_marketone_home_lot1 \
   --stop-after-init'
```

---

## 5. Verdict

**GO sous réserves** — favorable au merge de la PR #73.

Le code est de bonne qualité, conforme à la note d'architecture, fidèle à la maquette, et le modèle catalogue MOA est correctement construit et testé. Aucune anomalie bloquante au niveau code.

Conditions / suites :

1. **Avant merge** : rejouer la suite de tests sur la branche (§4.2) — confirmation 31/0.
2. **Post-merge / validation visuelle finale** : lever la réserve image en remplaçant les placeholders par les vraies photos BO — **Galettes de manioc** *et* **Confiture de goyave** (§4.1).
3. **À tracer (non bloquant)** : ticket dette technique sur `_with_website_request` (§3.1) ; acter la gouvernance « vedettes » et les chips heuristiques (§3.2, §3.3).

Une fois la suite confirmée verte, la PR peut être mergée ; la levée de réserve image et la dette technique se traitent en suivi sans bloquer la Section 4.

---

## Annexe — fichiers revus

| Fichier | Rôle |
|---------|------|
| `dorevia_ck_marketone/docs/design/maquette_01.2/NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md` | Note d'architecture (référence) |
| `dorevia_ck_marketone/docs/design/maquette_01.2/artifact/index.html` | Maquette de référence (comparaison structure) |
| `dorevia_ck_marketone_content/home_featured.py` | SSR cartes · sélection variantes · bootstrap home |
| `dorevia_ck_marketone_content/catalog_manioc_variants.py` | Alignement catalogue MOA (Manio + Galettes) |
| `dorevia_ck_marketone_content/hooks.py` | Intégration bootstrap catalogue |
| `dorevia_ck_marketone_content/migrations/19.0.1.15.0 → 1.17.0/post-migrate.py` | Régénération cartes + catalogue |
| `dorevia_ck_theme/static/src/scss/website.scss` | Styles `.ck-featured-products--maquette` (grille, média, cartes) |
| `dorevia_ck_theme/views/snippets/ck_snippet_featured_products.xml` | Squelette snippet éditeur |
| `tests/test_ck_catalog_manioc_variants.py`, `test_ck_home_section3_featured_compose.py`, `test_ck_home_section3_featured_hooks.py`, `test_ck_theme_technical.py` | Couverture Section 3 / catalogue |
