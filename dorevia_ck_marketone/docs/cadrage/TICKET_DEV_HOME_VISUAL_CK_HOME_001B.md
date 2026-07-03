# Ticket Dev — CK-HOME-001B — Réserves visuelles home (vedettes + coffrets)

| Champ | Valeur |
| --- | --- |
| Date | 2 juillet 2026 (révision 3 juillet 2026) |
| Projet | C-Kréyòl Marketone — Home |
| Périmètre | **001B-a + 001B-b uniquement** |
| Statut | **Clôturé — GO MOA** (recette 3 juillet 2026) |
| Clôture | [`NOTE_MOA_CLOTURE_CK_HOME_001B_20260703.md`](NOTE_MOA_CLOTURE_CK_HOME_001B_20260703.md) |
| Base recette | `dorevia_ck_marketone_01` — http://localhost:18079 |
| État des lieux | [`NOTE_ETAT_DES_LIEUX_CK_HOME_001B_20260703.md`](NOTE_ETAT_DES_LIEUX_CK_HOME_001B_20260703.md) |

---

## Versions

| Référence | `dorevia_ck_marketone_content` | `dorevia_ck_theme` |
| --- | --- | --- |
| Avant lot (cadrage) | 19.0.1.75.0 | 19.0.1.114.0 |
| **Livraison 001B** (`43aa89fa`) | **19.0.1.76.0** | **19.0.1.115.0** |
| **Hotfix coffrets** (`4a7fe568`) | **19.0.1.79.0** | *(inchangé)* |
| Sandbox actuelle (3 juil. 2026) | **19.0.1.82.0** | **19.0.1.120.0** |

Références MOA : [`NOTE_MOA_CADRAGE_CK_HOME_001B_20260702.md`](NOTE_MOA_CADRAGE_CK_HOME_001B_20260702.md) · [`RECETTE_QA_RAPPROCHEMENT_HOME_MAQUETTE_V1.md`](../design/maquette_01.2/RECETTE_QA_RAPPROCHEMENT_HOME_MAQUETTE_V1.md) (réserves E1/E2 d'origine) · [`RECETTE_QA_HOME_20260702.md`](RECETTE_QA_HOME_20260702.md) *(pré-hotfix 79.0 — à compléter par recette clôture post-79)*.

---

## Gouvernance — renommage lot « producteurs home »

L'intention initiale « **CK-HOME-001B = bloc producteurs / transformateurs** » est **dépréciée**.

| Ancien sens | Nouveau sens CK-HOME-001B | Futur lot producteurs home |
| --- | --- | --- |
| Bloc producteurs / transformateurs en home | **Réserves visuelles** post-001A (vedettes + coffret) | **`CK-HOME-002`** ou **`CK-HOME-PRODUCERS-001`** — à cadrer séparément |

---

## 1. Contexte

La home est **stabilisée** sur le fond et la structure (hero 001A, univers 001C, navigation, tunnel V1 gelé).

Les réserves P1 E1/E2 (recette QA juin 2026) ont été **traitées en code** le 2 juillet 2026. La **clôture MOA** reste ouverte : recette visuelle post-hotfix `79.0` (desktop 1280 + mobile 390), notamment validation du clic CTA « Découvrir » coffrets.

| ID | Bloc | Constat initial (juin) | État technique (3 juil.) |
| --- | --- | --- | --- |
| **E1** | Vedettes | Images non visibles (`0px`) | **Résolu** — `<img class="ck-product-card__img">` + SCSS `product_card.scss` |
| **E2** | Coffrets | Fallback beige éditorial | **Résolu** — produit seedé + asset statique ; validateur rejette `--editorial` |

---

## 2. Objectif (inchangé)

Rendre **« Nos coups de cœur »** et **« Coffrets découverte »** présentables en démo : images visibles, pas d'impression de catalogue incomplet. Correction visuelle ciblée — **sans refonte globale**.

---

## 3. Livraison technique

### 3.0 — Commits de référence

| Commit | Version | Contenu |
| --- | --- | --- |
| **`43aa89fa`** | `19.0.1.76.0` | Livraison 001B — vedettes `<img>`, SCSS, seed coffret, asset `ck_discovery_pack.jpg`, tests lot2/lot3, migration `76.0` |
| **`77.0`** | `19.0.1.77.0` | Hotfix — fuite markup dual, porte `/kits` (`controllers/home_portes.py`) |
| **`78.0`** | `19.0.1.78.0` | Hotfix — doublons coffrets / réparation dual |
| **`4a7fe568`** | `19.0.1.79.0` | Hotfix — retrait `stretched-link`, CTA `Découvrir` → `/kits`, captures recette, migration `79.0` |

Messages de commit :

```text
43aa89fa — fix(ck-home): CK-HOME-001B images vedettes visibles et visuel coffret qualifié
4a7fe568 — fix(ck-home): hotfix CK-HOME-001B coffrets — markup, /kits et CTA Découvrir
```

### 3.1 — CK-HOME-001B-a — Vedettes (E1) — livré

| Fichier | Modification livrée |
| --- | --- |
| `home_featured.py` | Balise `<img class="ck-product-card__img">` + validateur `_CARD_IMG_RE` |
| `dorevia_ck_theme/static/src/scss/product_card.scss` | Règles `&__img` (`aspect-ratio`, `object-fit`) |
| `tests/test_ck_home_lot2_*.py` | Assertions image `<img>` renforcées |
| `migrations/19.0.1.76.0/post-migrate.py` | Re-bootstrap vedettes |

**Inchangé fonctionnellement** : curation `ck_is_featured` · prix · liens `/shop/...` · panier · wishlist.

### 3.2 — CK-HOME-001B-b — Coffrets (E2) — livré

| Fichier | Modification livrée |
| --- | --- |
| `catalog_discovery_pack.py` | Seed produit « Coffret découverte créole » avec image |
| `static/img/ck_discovery_pack.jpg` | Asset statique de repli |
| `home_discovery_pack.py` | Validateur rejette `--editorial`, `stretched-link`, `fa-3x` ; layout `ck-discovery-pack--polish-v1` |
| `controllers/home_portes.py` | `/kits` → 301 `/shop?marketone_mode=pack` |
| `home_dual_engage.py` | Réparation fuite markup (hotfixes 77–78) |
| `tests/test_ck_home_lot3_*.py` | Assertions visuel qualifié + absence stretched-link |
| `migrations/19.0.1.76.0` · `77.0` · `78.0` · `79.0` | Re-bootstrap successifs |

**Inchangé fonctionnellement** : CTA `Découvrir` → `/kits` · textes éditoriaux par défaut.

---

## 4. Hors scope (strict — inchangé)

- Hero CK-HOME-001A · hygiène CK-HOME-001C · navigation header · footer · démo tunnel
- **`/promotions`** (réserve P2 — **001B-c** — ticket ultérieur, **NO GO** dans ce lot)
- Bloc producteurs home → **CK-HOME-002** / **CK-HOME-PRODUCERS-001**
- **Copy éditorial bas de page** (`home_editorial.py`) — backlog copy dédié
- Refonte home complète · Lot 6 polish global · SEO canonical · déploiement prod
- Tunnel achat · fiches produit (hors non-régression)
- **Développement additionnel 001B** : **NO GO** tant que la recette clôture MOA n'est pas faite

---

## 5. Critères d'acceptation

### CA1 — Vedettes (001B-a)

| Critère | État technique |
| --- | --- |
| Image visible desktop 1280 + mobile 390 | **OK** — smoke + tests |
| URLs `/web/image/product…` en 200 | **OK** — tests compose |
| Prix, liens, CTA panier inchangés | **OK** |

### CA2 — Coffret (001B-b)

| Critère | État technique |
| --- | --- |
| Plus de fallback `ck-discovery-pack__visual--editorial` | **OK** — validateur + smoke |
| Visuel qualifié (produit BO ou asset statique) | **OK** |
| Route `/kits` → collection pack | **OK** — 301 |
| Clic bouton « Découvrir » → `/kits` (pas intercepté) | **À valider MOA** — corrigé en `79.0` |

### CA3 — Mobile 390 px

- **À valider MOA** — captures 2 juil. existent ; repasse formelle post-`79.0` requise.

### CA4 — Non-régression

- Hero 001A · univers 001C · dual Pro · ordre blocs · `/shop` : **OK** tests lot1 + smoke.

### CA5 — Tests automatisés

- Tags `dorevia_ck_marketone_home_lot1/2/3` : **35/35 verts** (3 juil. 2026, sandbox `82.0`).

---

## 6. Recette QA / tests

### 6.1 Tests automatisés (validés 3 juil. 2026)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --http-port=8079 \
  --test-tags dorevia_ck_marketone_home_lot1,dorevia_ck_marketone_home_lot2,dorevia_ck_marketone_home_lot3 \
  --stop-after-init
```

> Utiliser `--http-port=8079` si le port `8069` est occupé par le serveur sandbox.

### 6.2 Recette MOA de clôture — **à prévoir (post-79.0)**

| Contrôle | Viewport | Priorité |
| --- | --- | --- |
| Images vedettes visibles | 1280 + **390** | P1 |
| Coffret sans fallback beige | 1280 + **390** | P1 |
| **Clic CTA « Découvrir »** → `/kits` (pas fiche produit interceptée) | 1280 + **390** | P1 |
| Overflow horizontal home | **390** | P1 |
| Hero 001A non régressé | 1280 | P1 |
| `/shop` + fiche témoin + ajout panier | 1280 | P1 |

Scripts réutilisables :

- `docs/design/maquette_01.2/scripts/ck_lot2_product_mobile390.mjs`
- Captures existantes : `docs/cadrage/captures/recette_home_20260702/` *(pré-hotfix 79.0 — à compléter)*

**Livrable attendu** : `NOTE_MOA_CLOTURE_CK_HOME_001B_20260703.md` (ou date réelle) + captures desktop + mobile 390 post-79.

### 6.3 Migrations (livrées)

| Version | Script |
| --- | --- |
| `19.0.1.76.0` | Vedettes + coffret + seed catalogue |
| `19.0.1.77.0` | Dual + discovery re-bootstrap |
| `19.0.1.78.0` | Réparation fuite / doublons |
| `19.0.1.79.0` | Coffrets sans `stretched-link` |

---

## 7. Implémentation — checklist Dev

- [x] Reproduire E1/E2 sur sandbox post-upgrade `19.0.1.75.0`
- [x] Corriger visibilité images vedettes (`<img>` + SCSS `product_card.scss`) — `43aa89fa`
- [x] Remplacer fallback coffret beige (seed produit + asset statique) — `43aa89fa`
- [x] Mettre à jour validateurs / tests lot2 et lot3 — `43aa89fa`
- [x] Migrations `76.0` + upgrade sandbox
- [x] Hotfixes markup dual / `/kits` / stretched-link — `77.0`–`79.0` / `4a7fe568`
- [x] Tests automatisés lot1/2/3 verts (3 juil. 2026)
- [x] **Recette MOA clôture** desktop 1280 + mobile 390 post-`79.0` — 3 juil. 2026
- [x] **Note MOA clôture** [`NOTE_MOA_CLOTURE_CK_HOME_001B_20260703.md`](NOTE_MOA_CLOTURE_CK_HOME_001B_20260703.md)
- [x] Vérifier hero 001A / univers 001C / dual inchangés (smoke + tests)

---

## 8. Verdict ticket

```text
CK-HOME-001B-a / 001B-b → Clôturé GO MOA (3 juillet 2026)
→ Livraison technique : 43aa89fa + hotfixes 77.0–79.0 (4a7fe568)
→ 001B-c /promotions et copy éditorial → hors périmètre / backlog
```

---

*Ticket Dev — C-Kréyòl Marketone · CK-HOME-001B — révision 3 juillet 2026*
