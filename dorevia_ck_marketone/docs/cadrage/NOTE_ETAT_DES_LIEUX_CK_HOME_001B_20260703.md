# Note d'état des lieux — CK-HOME-001B — Vedettes + coffret

| Champ | Valeur |
| --- | --- |
| Date | 3 juillet 2026 |
| Projet | C-Kréyòl Marketone — Home |
| Destinataires | MOA, Produit, QA, Dev |
| Périmètre | Analyse post-livraison **sans développement** |
| Références | [`NOTE_MOA_CADRAGE_CK_HOME_001B_20260702.md`](NOTE_MOA_CADRAGE_CK_HOME_001B_20260702.md) · [`TICKET_DEV_HOME_VISUAL_CK_HOME_001B.md`](TICKET_DEV_HOME_VISUAL_CK_HOME_001B.md) · [`RECETTE_QA_HOME_20260702.md`](RECETTE_QA_HOME_20260702.md) |
| Base analysée | `dorevia_ck_marketone_01` — http://localhost:18079 |

---

## Synthèse exécutive

Le lot **CK-HOME-001B-a (vedettes E1)** et **001B-b (coffret E2)** ont été **largement livrés en code** entre le 2 et le 3 juillet 2026 (`43aa89fa` + hotfixes `77.0`–`79.0`). Les réserves P1 d'origine (images vedettes invisibles, fallback beige coffret) sont **résolues techniquement** sur la sandbox à jour.

En revanche, la **traçabilité MOA n'est pas bouclée** : pas de note de clôture 001B, ticket Dev encore au statut « GO ouverture » avec checklist non cochée, et recette QA du 2 juillet en **NO GO** sur un point (CTA coffret) **corrigé ensuite** en `79.0`.

**Verdict proposé : GO révision du ticket** avant toute nouvelle passe développement — puis **recette MOA de clôture** (desktop 1280 + mobile 390). Pas de recadrage fonctionnel MOA/Design sur E1/E2.

---

## Commits et versions

| Commit | Date | Contenu | Version `content` |
| --- | --- | --- | --- |
| `43aa89fa` | 2 juil. 2026 | **Livraison 001B** — `<img>` vedettes, SCSS `ck-product-card__img`, asset coffret statique, seed produit coffret, tests lot2/lot3 renforcés | **19.0.1.76.0** |
| *(intermédiaire)* | 2 juil. 2026 | Hotfix `77.0` — fuite markup dual, porte `/kits` | **19.0.1.77.0** |
| *(intermédiaire)* | 2 juil. 2026 | Hotfix `78.0` — doublons coffrets / dual | **19.0.1.78.0** |
| `4a7fe568` | 2 juil. 2026 | Hotfix `79.0` — retrait `stretched-link`, CTA `Découvrir` → `/kits`, captures recette, contrôleur `home_portes.py` | **19.0.1.79.0** |

**État sandbox au 3 juillet 2026** (post-upgrade univers Lot A) :

| Module | Version installée | Version HEAD repo |
| --- | --- | --- |
| `dorevia_ck_marketone_content` | **19.0.1.82.0** | **19.0.1.82.0** |
| `dorevia_ck_theme` | **19.0.1.120.0** | **19.0.1.120.0** |

Le ticket initial ciblait `19.0.1.76.0` / thème `19.0.1.115.0` — **obsolète** ; les livraisons ultérieures (polish Home `68a0283b`, univers banner `a3567caf`) n'ont pas rouvert E1/E2 mais **écartent** le ticket de référence sur les numéros de version.

---

## 1. Ce qui a déjà été livré

### 001B-a — Vedettes (E1)

| Livrable | Fichier / mécanisme |
| --- | --- |
| Balise `<img class="ck-product-card__img">` en plus du `background-image` | `home_featured.py` — `build_featured_product_card_html()` |
| SCSS hauteur visible (`aspect-ratio: 1/1`, `display: block`) | `dorevia_ck_theme/static/src/scss/product_card.scss` |
| Validateur renforcé (`_CARD_IMG_RE`) | `home_featured.py` — `card_fragment_is_valid()` |
| Tests HTTP + hooks | `test_ck_home_lot2_compose.py`, `test_ck_home_lot2_hooks.py` |
| Re-bootstrap migration `76.0` | `migrations/19.0.1.76.0/post-migrate.py` |

### 001B-b — Coffrets (E2)

| Livrable | Fichier / mécanisme |
| --- | --- |
| Asset statique `ck_discovery_pack.jpg` | `static/img/` |
| Seed produit « Coffret découverte créole » avec image | `catalog_discovery_pack.py` |
| Validateur rejette fallback `--editorial` et `stretched-link` | `home_discovery_pack.py` — `discovery_pack_arch_is_valid()` |
| Porte `/kits` → 301 `/shop?marketone_mode=pack` | `controllers/home_portes.py` |
| Hotfixes markup home (dual / doublons coffrets) | `home_dual_engage.py`, migrations `77.0`–`79.0` |
| Tests lot3 | `test_ck_home_lot3_compose.py`, `test_ck_home_lot3_hooks.py` |
| Captures recette 2 juil. | `docs/cadrage/captures/recette_home_20260702/` |

### Documentation existante (pré-livraison)

- Cadrage MOA : `NOTE_MOA_CADRAGE_CK_HOME_001B_20260702.md` (GO ticket Dev 001B-a + 001B-b).
- Ticket Dev : `TICKET_DEV_HOME_VISUAL_CK_HOME_001B.md`.
- Recette QA : `RECETTE_QA_HOME_20260702.md` (post-`78.0`, **avant** validation finale hotfix `79.0`).

---

## 2. Résolution E1 / E2 — constats

### E1 — Vedettes : **résolu côté technique**

| Critère CA1 ticket | État |
| --- | --- |
| Image produit visible desktop / mobile | **OK** — smoke HTML `/` : 4× `ck-product-card__img`, URLs `/web/image/product.*` |
| Prix, liens, curation `ck_is_featured` inchangés | **OK** — logique `get_curated_featured_variants()` intacte |
| Pas de placeholder Odoo | **OK** — tests + smoke |
| Tests `dorevia_ck_marketone_home_lot2` | **OK** — **0 failed / 0 error** (35 tests lot1+2+3, 3 juil. 2026) |

### E2 — Coffrets : **résolu côté technique, clôture MOA à confirmer**

| Critère CA2 ticket | État |
| --- | --- |
| Plus de fallback `ck-discovery-pack__visual--editorial` | **OK** — validateur + smoke : visuel `/web/image/product.template/4583/...` |
| Visuel qualifié (produit seedé ou asset) | **OK** — produit coffret BO + image |
| CTA `/kits` fonctionnel | **OK** — route **301** vers `/shop?marketone_mode=pack` ; HTML sans `stretched-link` |
| Clic utilisateur sur bouton « Découvrir » | **À revalider MOA** — corrigé en `79.0` ; recette du 2 juil. encore en NO GO sur ce point |

### Smoke live sandbox (3 juil. 2026)

- `/` → **200**
- Vedettes : **4 images** `<img>` visibles dans le HTML.
- Coffret : bloc `ck-discovery-pack--polish-v1`, **pas** de `stretched-link` ni fallback éditorial.
- `/kits` → **301** vers collection pack.

---

## 3. Ce qui reste ouvert ou ambigu

| # | Sujet | Détail | Responsable |
| --- | --- | --- | --- |
| O1 | **Note MOA clôture 001B** | Absente (`NOTE_MOA_CLOTURE_CK_HOME_001B_*.md` jamais rédigée) | Dev / QA doc |
| O2 | **Recette QA obsolète** | `RECETTE_QA_HOME_20260702.md` = NO GO CTA coffret — antérieure au hotfix `79.0` | QA — repasse recette |
| O3 | **Ticket Dev périmé** | Statut « GO ouverture », checklist §7 entièrement `[ ]`, versions 75/76 | Dev — révision doc |
| O4 | **CA3 mobile 390 px** | Captures 2 juil. existent ; pas de verdict MOA formalisé post-`79.0` | QA / MOA |
| O5 | **001B-c `/promotions`** | Toujours **P2 / hors ticket** — route 404 si testée | MOA arbitrage |
| O6 | **Copy éditorial bas** | Optionnel cadrage 001B — non traité | MOA / backlog copy |
| O7 | **Alignement cards Home ↔ Shop** | Hors scope 001B strict ; polish shop postérieur (`68a0283b`) peut créer écart visuel résiduel | Design / backlog |
| O8 | **WIP local Lot B univers** | Modifications non commitées `ck_banner_variant` (hors 001B) — **polluent** les tests si présentes sur le mount ; à écarter (`git stash` ou revert) | Dev hygiène |

### Non-régression post-livraisons ultérieures

Les commits `68a0283b` (polish Home / header wishlist) et `a3567caf` (banner univers) **ne modifient pas** `home_featured.py` ni `home_discovery_pack.py`. Aucune régression E1/E2 détectée sur les tests home lot1–3 après upgrade `82.0`.

---

## 4. Le ticket initial reste-t-il valable ?

**Oui, dans l'esprit** (001B-a + 001B-b, périmètre serré, critères CA1–CA5).

**Non, en l'état documentaire** :

- Versions cibles et checklist ne reflètent pas la livraison réelle (76 → 79, puis montée 82).
- Les hotfixes `77.0`–`79.0` ne sont pas documentés dans le ticket.
- Le contrôleur `/kits` et le seed `catalog_discovery_pack.py` y sont partiellement anticipés mais pas comme livrés.
- Statut encore « GO ouverture » alors que le **développement P1 est fait**.

---

## 5. Faut-il réviser le ticket avant un nouveau GO Dev ?

**Oui — révision documentaire recommandée**, pas une réécriture fonctionnelle.

Actions ticket suggérées :

1. Passer le statut en **« Livré technique — en attente recette clôture MOA »**.
2. Cocher la checklist §7 et documenter les commits `43aa89fa` + `4a7fe568`.
3. Mettre à jour les versions de référence (`79.0` minimum livraison 001B ; `82.0` sandbox actuelle).
4. Ajouter une section **hotfixes 77–79** (markup, `/kits`, stretched-link).
5. Renvoyer la recette MOA vers une **nouvelle note** post-`79.0` (ou mise à jour de `RECETTE_QA_HOME_20260702.md`).
6. Laisser **001B-c** et copy éditorial explicitement hors scope.

**Pas de nouveau GO développement** tant que la recette MOA de clôture n'a pas tranché O2/O4 — sauf anomalie visuelle remontée à la repasse.

---

## 6. Impacts par zone

| Zone | Impact 001B | État |
| --- | --- | --- |
| **Home — ordre blocs** | Inchangé : Hero → Réassurance → Vedettes → Univers → Coffrets → Dual → Éditorial | Conforme ticket |
| **Vedettes** | SSR + `<img>` ; curation BO `ck_is_featured` | Livré |
| **Coffret** | Produit seedé + CTA `/kits` | Livré |
| **Cards Home** | `ck-product-card--home` + `product_card.scss` | Livré E1 ; parité shop = hors scope |
| **Contenu BO** | Produit coffret auto-seedé ; vedettes via `ck_is_featured` | MOA peut enrichir catalogue |
| **Navigation univers** | Indirect — section 4 cartes 001C stable | Non impacté |
| **Tests** | Tags `dorevia_ck_marketone_home_lot1/2/3` | **35/35 verts** (3 juil. 2026, code commité) |
| **Recette** | Captures 2 juil. + scripts `ck_lot2_*` / `ck_lot3_*` | **Repasse MOA requise** post-79 |

---

## Tests automatisés (3 juillet 2026)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --http-port=8079 \
  --test-tags dorevia_ck_marketone_home_lot1,dorevia_ck_marketone_home_lot2,dorevia_ck_marketone_home_lot3 \
  --stop-after-init
```

| Résultat | Détail |
| --- | --- |
| **0 failed / 0 error** | 35 tests |
| Prérequis | Code commité sans WIP `ck_banner_variant` sur le mount addons |

---

## Verdict

```text
CK-HOME-001B — État des lieux post-43aa89fa / hotfixes 77.0–79.0

E1 vedettes    → Résolu technique (GO recette)
E2 coffret     → Résolu technique (GO recette — confirmer CTA post-79)
Développement  → Pas de nouveau GO Dev P1 sans anomalie MOA
Ticket initial → Valable sur le fond, à RÉVISER (statut, versions, checklist, hotfixes)
Clôture MOA    → À ouvrir (note clôture + repasse 1280/390)

→ GO révision du ticket TICKET_DEV_HOME_VISUAL_CK_HOME_001B.md
→ GO recette MOA de clôture (pas GO développement)
→ NO GO développement additionnel tant que la clôture MOA n'est pas faite
→ NO GO recadrage MOA/Design sur le périmètre E1/E2
```

---

## Prochaines étapes recommandées

| # | Action | Acteur |
| --- | --- | --- |
| 1 | Réviser le ticket Dev (statut, checklist, commits, versions) | Dev |
| 2 | Repasse recette MOA desktop 1280 + mobile 390 (vedettes + coffret + CTA Découvrir) | QA / MOA |
| 3 | Rédiger `NOTE_MOA_CLOTURE_CK_HOME_001B_20260703.md` si GO recette | QA / Dev doc |
| 4 | Écarter le WIP local `ck_banner_variant` (hors 001B, Lot univers B = NO GO) | Dev |
| 5 | Arbitrer 001B-c `/promotions` en backlog séparé | MOA |

---

*Note d'état des lieux — C-Kréyòl Marketone · CK-HOME-001B — 3 juillet 2026*
