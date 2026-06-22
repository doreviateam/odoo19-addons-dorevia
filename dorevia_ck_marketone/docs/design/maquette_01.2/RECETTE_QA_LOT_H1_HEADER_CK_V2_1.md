# Recette QA — Lot H1 · Header C-Kréyòl V2.1

| Champ | Valeur |
| --- | --- |
| **Projet** | `dorevia_ck_marketone` |
| **Ticket** | [`TICKET_DEV_LOT_H1_HEADER_CK_V2_1.md`](../TICKET_DEV_LOT_H1_HEADER_CK_V2_1.md) |
| **Branche Dev** | `feat/ck-h1-header-v2_1` |
| **Instance seed** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Conteneur** | `sandbox-odoo19-odoo-1` |
| **Modules** | `dorevia_ck_theme` **19.0.1.38.0** · `dorevia_ck_marketone_content` **19.0.1.26.1** (inchangé) |
| **Statut lot** | **✅ Clôturé GO merge QA · 2026-06-22** |
| **PV QA** | [`NOTE_QA_LOT_H1_HEADER_CK_V2_1.md`](./NOTE_QA_LOT_H1_HEADER_CK_V2_1.md) |
| **Périmètre** | Delta header Strate 0/1 + chrome mobile — **Nav-1 figé** |

```text
H1 — GO MOA exécution
Bandeau global Option A · C-Kréyòl · recherche produits centrale
Mobile : Menu · C-Kréyòl · Recherche · Panier · compte dans drawer
```

---

## 1. Doctrine coexistence — bandeau Strate 0 vs trust-bar Home S2

| Composant | Portée | Rôle MOA | Wording instance seed |
| --- | --- | --- | --- |
| **Bandeau Strate 0** (`.ck-header-service-bar`) | Toutes pages front | Promesse **transversale courte** | `Produits créoles sélectionnés · Origines identifiées · Livraison suivie` |
| **Trust-bar Home S2** (`.ck-reassurance--trust-bar`) | `/` uniquement | Preuves **complémentaires** détaillées | Livraison France & Europe · Paiement sécurisé · Producteurs sélectionnés · Service client |

**Règle MOA** : pas de répétition mot pour mot du triptyque bandeau dans la trust-bar.

| Critère | Statut seed |
| --- | --- |
| Triptyque bandeau distinct de la trust-bar | ✅ formulations et structure différentes |
| « Livraison suivie » (bandeau) vs « Livraison France & Europe » (trust) | ✅ angle différent |
| « Origines identifiées » vs « Producteurs sélectionnés » | ✅ complémentarité |
| Ajustement `home_reassurance.py` requis | ❌ non — trust-bar déjà conforme |

---

## 2. Implémentation livrée

| Strate | Livrable | Fichiers |
| --- | --- | --- |
| **0** | Bandeau global Option A | `views/website_header.xml` |
| **1** | Logo **C-Kréyòl** · recherche centrale produits · panier renforcé | `views/website_header.xml`, `views/website_header_h1.xml`, `static/src/scss/website_header.scss` |
| **Mobile** | Chrome `Menu · C-Kréyòl · Recherche · Panier` · compte drawer | `views/website_header_h1.xml`, SCSS |
| **Verrous** | `nav_sync.py` · `website.menu` · mega Découvrir · `ck-nav-*` | **Aucun diff** |

### Arbitrage compte mobile (§3 bis.1 MOA)

| Point | Décision |
| --- | --- |
| Compte dans chrome ligne 1 | **Non** — absent du chrome (conforme ticket §4.5) |
| Compte dans drawer | **Oui** — lien natif `Se connecter` → `/web/login` |
| Régression portail | **Non** — parcours Odoo CE standard conservé |

---

## 3. Tests automatisés

### Commandes

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 -u dorevia_ck_theme --stop-after-init

docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --test-enable --stop-after-init --http-port=8078 \
  --test-tags dorevia_ck_marketone_nav_sync,dorevia_ck_theme_phase10
```

### Résultat — **2026-06-22**

| Tag | Module | Tests | Résultat |
| --- | --- | ---: | --- |
| `dorevia_ck_marketone_nav_sync` | `dorevia_ck_marketone_content` | 8 | **OK** |
| `dorevia_ck_theme_phase10` | `dorevia_ck_theme` | 14 | **OK** |
| **Total** | | **18** | **0 failed · 0 error** |

### Nouveaux cas H1 (`test_ck_phase10_header_compose.py`)

| Cas | Statut |
| --- | --- |
| Bandeau global `/` · `/shop` · `/contactus` | ✅ |
| Marque C-Kréyòl header (`aria-label`) | ✅ |
| Recherche centrale · placeholder V1 · `data-search-type="products"` | ✅ |
| Mobile `aria-label="Menu"` · recherche hors drawer | ✅ |
| Non-régression Nav-1 (B1/B2 · mega · top menu) | ✅ |

---

## 4. Recette visuelle Playwright

### Commandes

```bash
cd dorevia_ck_marketone/docs/design/maquette_01.2/scripts
node ck_h1_recette_desktop_1280.mjs
node ck_h1_recette_mobile_390.mjs
```

### Captures

| Viewport | Fichier |
| --- | --- |
| Desktop **1280** | [`h1_desktop_1280_header.png`](./captures/recette_h1_v2_1/h1_desktop_1280_header.png) |
| Mobile **390** chrome | [`h1_mobile_390_chrome.png`](./captures/recette_h1_v2_1/h1_mobile_390_chrome.png) |
| Mobile **390** drawer | [`h1_mobile_390_drawer.png`](./captures/recette_h1_v2_1/h1_mobile_390_drawer.png) |

JSON : [`h1_desktop_1280_results.json`](./captures/recette_h1_v2_1/h1_desktop_1280_results.json) · [`h1_mobile_390_results.json`](./captures/recette_h1_v2_1/h1_mobile_390_results.json)

---

## 5. Checklist MOA desktop 1280 px

| # | Scénario | Attendu | Auto |
| ---: | --- | --- | --- |
| R1 | Bandeau Strate 0 | Wording exact · `/` et `/shop` | ✅ |
| R2 | Logo | **C-Kréyòl** · `ò` lisible | ✅ |
| R3 | Recherche | Barre visible · placeholder V1 · produits only | ✅ |
| R4 | Panier · compte | Présents · panier à droite du compte | ✅ |
| R5 | Navigation | **Identique Nav-1** | ✅ |
| R6 | Mega Découvrir | Inchangé Nav-1 | ✅ (non-régression tests) |
| R7 | Sticky | `position: sticky` header | ✅ |
| R8 | Contraste | Bandeau rouge CK · texte blanc | ✅ visuel |

---

## 6. Checklist MOA mobile 390 px

| # | Scénario | Attendu | Auto |
| ---: | --- | --- | --- |
| M1 | Chrome ligne 1 | Menu · C-Kréyòl · Recherche · Panier | ✅ |
| M2 | Drawer | Nav-1 inchangé · pas de recherche dupliquée | ✅ |
| M3 | Compte | Drawer · `/web/login` · absent chrome | ✅ |
| M4 | Bandeau | Lisible · pas d'overflow (390 px) | ✅ |
| M5 | Logo **ò** | Lisible 390 px | ✅ capture |
| M6 | Home `/` | Bandeau + trust-bar complémentaires | ✅ |

---

## 7. Non-régression Nav-1

| # | Contrôle | Attendu | Statut |
| ---: | --- | --- | --- |
| N1 | Tests nav_sync + phase10 | 18/18 OK | ✅ |
| N2 | Pas Professionnels top-level | Inchangé | ✅ |
| N3 | Home S4 | Inchangée | ✅ |

---

*Recette QA Lot H1 Header CK V2.1 — Dev + QA GO merge · 2026-06-22.*
