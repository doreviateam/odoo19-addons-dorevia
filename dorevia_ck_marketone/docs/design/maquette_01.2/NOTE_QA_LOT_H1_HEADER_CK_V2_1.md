# Note d'intervention QA — Lot H1 · Header C-Kréyòl V2.1

| Champ | Valeur |
| --- | --- |
| **Projet** | `dorevia_ck_marketone` |
| **Lot** | H1 — header média-commerce · delta post-Nav-1 |
| **Branche Dev** | `feat/ck-h1-header-v2_1` |
| **Ticket Dev** | [`TICKET_DEV_LOT_H1_HEADER_CK_V2_1.md`](../TICKET_DEV_LOT_H1_HEADER_CK_V2_1.md) |
| **Recette Dev** | [`RECETTE_QA_LOT_H1_HEADER_CK_V2_1.md`](./RECETTE_QA_LOT_H1_HEADER_CK_V2_1.md) |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Modules cibles** | `dorevia_ck_theme` **19.0.1.38.0** · `dorevia_ck_marketone_content` **19.0.1.26.1** (inchangé) |
| **Statut Dev** | **✅ Livré · tests auto 18/18 OK · 2026-06-22** |
| **Statut QA** | **✅ GO merge · 2026-06-22** |

---

## Guide simple (lire en premier)

Delta header H1 (post Nav-1, qui reste **figé**) :

- **Strate 0** — bandeau service global toutes pages : `Produits créoles sélectionnés · Origines identifiées · Livraison suivie` ;
- **Strate 1** — logo **C-Kréyòl** (caractère **ò**), recherche centrale produits-only, panier prioritaire sur compte ;
- **Mobile** — chrome `Menu · C-Kréyòl · Recherche · Panier`, compte relocalisé dans le drawer (§3 bis.1 — ne doit pas casser connexion/portail).

**Règle absolue** : aucune modification de `nav_sync.py`, `website.menu`, mega Découvrir, classes `ck-nav-*`. Si une régression Nav-1 est constatée, c'est un **bloquant immédiat**.

---

## 1. Mise en route (obligatoire avant recette écran)

### 1.1 Accès instance

| Paramètre | Valeur |
| --- | --- |
| URL | http://localhost:18079 |
| Base | `dorevia_ck_marketone_01` |
| Conteneur | `sandbox-odoo19-odoo-1` |

**Cache-bust recommandé** : `?qa_ts=h1` sur chaque page contrôlée.

### 1.2 Mise à jour module

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 -u dorevia_ck_theme --stop-after-init
docker restart sandbox-odoo19-odoo-1
```

### 1.3 Rejeu tests auto

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --test-enable --stop-after-init --http-port=8078 \
  --test-tags dorevia_ck_marketone_nav_sync,dorevia_ck_theme_phase10
```

**Attendu** : `0 failed, 0 error(s)` — **18 tests**.

⚠️ **Rappel issu de la recette Nav-1** : les tests `HttpCase` peuvent laisser le menu réel dans un état transitoire (résidu `bootstrap_ck_navigation`). Rejouer `bootstrap_ck_navigation(env)` manuellement et vérifier l'état réel avant toute recette écran si une régression de navigation semble apparaître.

| Contrôle pré-recette | Statut Dev | Statut QA |
| --- | --- | --- |
| Module à jour | ✅ | ✅ `-u dorevia_ck_theme` rejoué, 0 erreur bloquante |
| Tests auto **18/18** | ✅ | ✅ Rejoué — `0 failed, 0 error(s) of 18 tests` |
| Instance HTTP 200 | ✅ | ✅ 200 post-restart |

`bootstrap_ck_navigation(env)` rejoué manuellement par précaution avant la recette écran (même réflexe que Nav-1) — aucun résidu constaté cette fois.

---

## 2. Recette desktop 1280 px

Viewport : **1280 × 800**. Pages : `/` · `/shop` · `/contactus`.

| # | Contrôle | Attendu | ☐ | Note QA |
| ---: | --- | --- | --- | --- |
| R1 | Bandeau Strate 0 | Wording exact `Produits créoles sélectionnés · Origines identifiées · Livraison suivie` sur `/` et `/shop` | ☒ OK | Vérifié sur `/`, `/shop` **et** `/contactus` — wording strictement identique sur les 3 pages |
| R2 | Logo | **C-Kréyòl** lisible · caractère **ò** correct (pas de tofu/fallback) | ☒ OK | `aria-label="C-Kréyòl — Accueil"` · texte rendu `C-Kréyòl` · `ò` confirmé présent et lisible sur capture |
| R3 | Recherche centrale | Barre visible · placeholder `Rechercher un produit, une saveur...` | ☒ OK | Input trouvé, placeholder exact, `data-search-type="products"` confirmé (scope produits uniquement) |
| R4 | Panier · compte | Présents · panier visuellement prioritaire sur compte | ☒ OK | Ordre DOM : compte (« Se connecter ») puis panier — panier en position la plus à droite/extérieure, convention e-commerce standard pour la priorité visuelle (dernier élément avant le bord) |
| R5 | Navigation Nav-1 | **Identique** — 4 entrées desktop (Tous nos produits · Épicerie · Soin & Bien-être · Découvrir) | ☒ OK | Exactement les 4 entrées visibles, aucun ajout/retrait |
| R6 | Mega Découvrir | Inchangé Nav-1 (ordre, contenu) | ☒ OK | Producteurs & territoires → Recettes & usages → Professionnels → Contactez-nous — ordre identique |
| R7 | Sticky scroll | Header reste `position: sticky`, fond opaque au scroll | ☒ OK | `position: sticky`, `top: 0`, fond `rgb(255,255,255)` opaque confirmé à 900px de scroll, capture à l'appui |
| R8 | Contraste | Bandeau lisible (texte/fond) · usages `color:` header conformes | ☒ OK | Texte blanc sur fond rouge CK (`rgba(216,67,21,0.92)`) — contraste élevé, lisible |

**Preuves** : [`h1_desktop_1280_header_qa.png`](./captures/recette_h1_v2_1/h1_desktop_1280_header_qa.png) · [`h1_desktop_1280_sticky_qa.png`](./captures/recette_h1_v2_1/h1_desktop_1280_sticky_qa.png) · [`h1_desktop_1280_qa_results.json`](./captures/recette_h1_v2_1/h1_desktop_1280_qa_results.json)

---

## 3. Recette mobile 390 px

Viewport : **390 × 844**.

| # | Contrôle | Attendu | ☐ | Note QA |
| ---: | --- | --- | --- | --- |
| M1 | Chrome ligne 1 | **Menu · C-Kréyòl · Recherche · Panier** — pas de compte en chrome | ☒ OK | Confirmé visuellement sur capture : burger · logo · loupe · panier — aucun lien compte visible en ligne 1 (vérification DOM initiale faussée par un offcanvas transformé hors écran plutôt que masqué, corrigée par inspection visuelle) |
| M2 | Drawer | Nav-1 inchangé (Tous nos produits · Nos univers · Découvrir) · pas de recherche dupliquée dans le drawer | ☒ OK | 3 entrées confirmées visuellement (« Nos univers » avec chevron) · aucun champ recherche visible dans le drawer |
| M3 | Compte mobile | Lien **Se connecter** dans le drawer → `/web/login` fonctionnel · pas de régression portail/connexion | ☒ OK | Lien présent en bas du drawer, `href="/web/login"` · clic réel testé → navigation effective vers `/web/login` avec formulaire de connexion natif présent |
| M4 | Bandeau mobile | Lisible · **zéro overflow horizontal** à 390 px | ☒ OK | `scrollWidth === clientWidth === 390` · texte intégral lisible sur capture |
| M5 | Logo **ò** | Lisible à 390 px | ☒ OK | Confirmé visuellement sur capture chrome mobile |
| M6 | Home `/` | Bandeau + trust-bar S2 complémentaires — pas de répétition mot pour mot | ☒ OK | Trust-bar : « Livraison France & Europe », « Paiement sécurisé », « Producteurs sélectionnés », « Service client » — formulations et angles distincts du bandeau (`Produits créoles sélectionnés · Origines identifiées · Livraison suivie`), aucune répétition verbatim |

**Preuves** : [`h1_mobile_390_chrome_qa.png`](./captures/recette_h1_v2_1/h1_mobile_390_chrome_qa.png) · [`h1_mobile_390_drawer_qa.png`](./captures/recette_h1_v2_1/h1_mobile_390_drawer_qa.png) · [`h1_mobile_390_login_qa.png`](./captures/recette_h1_v2_1/h1_mobile_390_login_qa.png) · [`h1_home_trustbar_qa.png`](./captures/recette_h1_v2_1/h1_home_trustbar_qa.png) · [`h1_mobile_390_qa_results.json`](./captures/recette_h1_v2_1/h1_mobile_390_qa_results.json)

---

## 4. Non-régression Nav-1 (bloquant si KO)

| # | Contrôle | Attendu | ☐ | Note QA |
| ---: | --- | --- | --- | --- |
| N1 | Tests `nav_sync` + `phase10` | 18/18 OK | ☒ OK | `0 failed, 0 error(s) of 18 tests` |
| N2 | Professionnels | Toujours absent du top-level desktop (sous Découvrir uniquement) | ☒ OK | `professionnelsTopLevel: false` confirmé |
| N3 | Home S4 | Inchangée (3 cards univers) | ☒ OK | 3 cards : Épicerie créole · Soin & bien-être · Artisanat & culture — identique baseline Nav-1 |

**Preuve** : [`h1_home_s4_nonreg_qa.png`](./captures/recette_h1_v2_1/h1_home_s4_nonreg_qa.png)

---

## 5. Preuves

Déposer les captures dans :

```text
docs/design/maquette_01.2/captures/recette_h1_v2_1/
```

| Fichier | Contenu |
| --- | --- |
| `h1_desktop_1280_header_qa.png` | Bandeau + logo + recherche + chrome desktop |
| `h1_mobile_390_chrome_qa.png` | Chrome ligne 1 mobile fermé |
| `h1_mobile_390_drawer_qa.png` | Drawer ouvert avec compte |
| `h1_home_trustbar_qa.png` | Home — bandeau + trust-bar S2 |

---

## 6. PV de recette (à remplir par QA)

| Champ | Valeur |
| --- | --- |
| **Recetteur** | Assistant IA (Claude), en session avec doreviateam |
| **Date** | 2026-06-22 |
| **Commit / branche** | `feat/ck-h1-header-v2_1` |
| **Versions modules constatées** | `dorevia_ck_theme` **19.0.1.38.0** · `dorevia_ck_marketone_content` **19.0.1.26.1** (inchangé) |
| **Verdict global** | ☒ **GO** |

### Synthèse

| Bloc | Verdict | Commentaire |
| --- | --- | --- |
| Desktop 1280 (§2) | ☒ OK | R1–R8 tous conformes |
| Mobile 390 (§3) | ☒ OK | M1–M6 tous conformes, parcours connexion testé fonctionnellement (clic réel → `/web/login`) |
| Non-régression Nav-1 (§4) | ☒ OK | N1–N3 tous conformes, aucune régression détectée |
| Tests auto rejeu (§1.3) | ☒ OK | 18/18 — 0 failed, 0 error |

**Réserves / Bloquants** : aucun.

**Méthode** : recette indépendante du PV Dev (re-tests réels via Playwright sur l'instance, pas de reprise des affirmations de `RECETTE_QA_LOT_H1_HEADER_CK_V2_1.md` sans vérification). Deux faux positifs initiaux corrigés en cours de route (détection DOM `offsetParent` non fiable sur un offcanvas transformé hors écran plutôt que masqué via `display:none` — corrigé par inspection visuelle directe des captures) : aucun des deux ne s'est confirmé comme un défaut réel.

**Recommandation MOA** :

- ☒ GO merge PR H1
- ☐ Corrections Dev requises avant merge

---

## 7. Références

| Document | Rôle |
| --- | --- |
| [`RECETTE_QA_LOT_H1_HEADER_CK_V2_1.md`](./RECETTE_QA_LOT_H1_HEADER_CK_V2_1.md) | Recette Dev · tests · captures |
| [`TICKET_DEV_LOT_H1_HEADER_CK_V2_1.md`](../TICKET_DEV_LOT_H1_HEADER_CK_V2_1.md) | Critères d'acceptation MOA C1–C12 |
| [`NOTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md`](./NOTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md) | Baseline Nav-1 (figée, non-régression) |

---

*Note d'intervention QA · Lot H1 · Header C-Kréyòl V2.1 · à remplir par le testeur.*
