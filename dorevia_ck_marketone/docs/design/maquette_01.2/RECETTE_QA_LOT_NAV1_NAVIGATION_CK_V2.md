# Recette QA — Lot Nav-1 · Navigation CK V2

| Champ | Valeur |
| --- | --- |
| **Projet** | `dorevia_ck_marketone` |
| **Ticket** | [`TICKET_DEV_LOT_NAV1_NAVIGATION_CK_V2.md`](../TICKET_DEV_LOT_NAV1_NAVIGATION_CK_V2.md) |
| **Branche Dev** | `feat/ck-nav1-navigation-v2` |
| **Instance seed** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Conteneur** | `sandbox-odoo19-odoo-1` |
| **Modules** | `dorevia_ck_marketone_content` **19.0.1.26.1** · `dorevia_ck_theme` **19.0.1.37.1** |
| **Statut lot** | **✅ Clôturé GO merge QA · 2026-06-21** |
| **Périmètre** | Header / navigation uniquement — Home S4 · fiche produit · checkout · Blog · Forum **hors lot** |

```text
Nav-1 — GO MOA exécution
Sync menus via nav_sync.py + bootstrap_ck_navigation()
CTA Contact header retiré · relocalisé mega Découvrir
Mobile : regroupement Nos univers (390 px)
```

---

## 1. Mapping catalogue BO (instance seed · post-sync)

Extrait via `get_nav_category_mapping(env)` sur `dorevia_ck_marketone_01` après `bootstrap_ck_navigation()` — **2026-06-21**.

| Entrée menu | Catégorie Odoo (BO) | ID | Noms recherchés (priorité) | URL / slug réel | Visible menu | ≥ 1 produit publié |
| --- | --- | ---: | --- | --- | --- | --- |
| **Tous nos produits** | Catalogue complet | — | — | `/shop` | **Oui** | **Oui** |
| **Épicerie** | Épicerie | 1 | Épicerie créole · Épicerie | `/shop/category/epicerie-1` | **Oui** | **Oui** |
| **Boissons** | — | — | Boissons | — | **Non** | **Non** (catégorie absente) |
| **Soin & Bien-être** | Maison & bien-être | 2 | Maison & bien-être · Soin & bien-être · Soin | `/shop/category/maison-bien-etre-2` | **Oui** | **Oui** |
| **Artisanat** | — | — | Artisanat | — | **Non** | **Non** (catégorie absente) |

**Note libellé MOA** : le menu affiche **Soin & Bien-être** ; la catégorie BO conserve le nom **Maison & bien-être** — conforme ticket §6.

### Mega Découvrir — liens résolus (instance seed)

| # | Libellé | URL | Visible |
| ---: | --- | --- | --- |
| 1 | Producteurs & territoires | `/producteur/atelier-hauts-goyaviers` | Oui |
| 2 | Recettes & usages | `/recettes` | Oui |
| 3 | Professionnels | `/professionnels` | Oui |
| 4 | Contactez-nous | `/contactus` | Oui |

**Masqués conformément Nav-1** :

| Libellé | Raison |
| --- | --- |
| Histoires de produits | Pas de page publiée (URL `None`) |
| Le blog CK | `website_blog` non installé |
| Communauté · Contribuer | Pas de teaser MOA · URL `None` |

**Ordre MOA respecté** : Professionnels **avant** Contactez-nous · aucun lien commerce dupliqué dans `ck-nav-decouvrir-links`.

### Structure `website.menu` racine (seq. · post-sync)

| Seq. | Libellé | URL | Classe CSS |
| ---: | --- | --- | --- |
| 10 | Tous nos produits | `/shop` | — |
| 15 | Nos univers | `#` | `ck-nav-mobile-univers` |
| 20 | Épicerie | `/shop/category/epicerie-1` | `ck-nav-desktop-universe` |
| 40 | Soin & Bien-être | `/shop/category/maison-bien-etre-2` | `ck-nav-desktop-universe` |
| 60 | Découvrir | `#` (mega) | — |

Enfants **Nos univers** (mobile) : Épicerie · Soin & Bien-être (uniquement univers visibles).

**Legacy supprimé** : Boutique · Professionnels top-level · CTA Contact header.

---

## 2. Tests automatisés

### Commandes

Upgrade :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 -u dorevia_ck_marketone_content,dorevia_ck_theme --stop-after-init
```

Tests Nav-1 :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --test-enable --stop-after-init --http-port=8078 \
  --test-tags dorevia_ck_marketone_nav_sync,dorevia_ck_theme_phase10
```

### Résultat — **2026-06-21**

| Tag | Module | Tests | Résultat |
| --- | --- | ---: | --- |
| `dorevia_ck_marketone_nav_sync` | `dorevia_ck_marketone_content` | 8 | **OK** |
| `dorevia_ck_theme_phase10` | `dorevia_ck_theme` | 11 | **OK** |
| **Total** | | **15** | **0 failed · 0 error** |

### Couverture fonctionnelle (extraits)

| Cas | Fichier test | Statut |
| --- | --- | --- |
| Bootstrap structure Nav V2 | `test_ck_nav_sync.py` | ✅ |
| Mega Découvrir : Pro + Contact · sans commerce | `test_ck_nav_sync.py` | ✅ |
| Professionnels absent top-level | `test_ck_nav_sync.py` | ✅ |
| Groupe mobile Nos univers + enfant Épicerie | `test_ck_nav_sync.py` | ✅ |
| Libellé Soin & Bien-être desktop | `test_ck_nav_sync.py` | ✅ |
| Catégorie vide / produit non publié | `test_ck_nav_sync.py` | ✅ |
| Header chrome CK · Tous nos produits · Découvrir | `test_ck_phase10_header_compose.py` | ✅ |
| Pas CTA `btn_cta` · pas Pro/Contact top-level | `test_ck_phase10_header_compose.py` | ✅ |
| Mega sans `/shop/category/` dupliqué | `test_ck_phase10_header_compose.py` | ✅ |
| B1 — classe `ck-nav-mobile-univers` desktop | `test_ck_phase10_header_compose.py` | ✅ |
| B2 — pas de doublon univers mobile | `test_ck_phase10_header_compose.py` | ✅ |
| Non-régression routes Phase 10 | `test_ck_phase10_header_compose.py` | ✅ |

---

## 3. Recette desktop 1280 px

| # | Scénario | Attendu | Résultat Dev | Preuve |
| ---: | --- | --- | --- | --- |
| R1 | Menu principal visible | Tous nos produits · Épicerie · **Soin & Bien-être** · Découvrir · Boissons/Artisanat masqués si cat. absente | **OK** | Mapping §1 · tests HTTP |
| R2 | Tous nos produits | `/shop` · 200 | **OK** | `test_routes_non_regression_markers` |
| R3 | Chaque catégorie visible | URL catégorie · 200 · ≥ 1 produit publié | **OK** | Épicerie · Soin & Bien-être |
| R4 | Mega Découvrir | Pro · Contact après Pro · pas Blog/Communauté/Contribuer | **OK** | §1 mega · tests sync |
| R5 | Mega sans commerce | Aucun lien shop/category dans mega | **OK** | `test_decouvrir_mega_has_no_commerce_duplicates` |
| R6 | Top-level | Pas Professionnels · pas CTA Contact | **OK** | `test_header_no_top_level_professionnels_or_contact_cta` |
| R7 | Chrome header | Recherche · panier · compte · logo · contraste mega hover `$ck-primary-text` | **OK** | SCSS `website_header.scss` · tests chrome |
| R8 | Tenue visuelle 1280 | Soin & Bien-être sans retour ligne (4 entrées visibles seed) | **OK** | Voir §10 bis #1 |

**Menu desktop effectif instance seed** (4 entrées commerce + Découvrir, règle visibilité §7 bis) :

> Tous nos produits · Épicerie · Soin & Bien-être · Découvrir

---

## 4. Recette mobile 390 px

| # | Scénario | Attendu | Résultat Dev | Preuve |
| ---: | --- | --- | --- | --- |
| M1 | Burger / offcanvas | Tous nos produits · Nos univers · Découvrir · zéro overflow | **OK** | CSS `overflow-x: clip` · classes mobile |
| M2 | Nos univers | Clic parent déplie (dropdown natif `#`) · enfants naviguent | **OK** | Voir §10 bis #3 |
| M3 | Professionnels · Contact | Accessibles depuis Découvrir · 200 | **OK** | Tests routes |
| M4 | Non-régression | Panier · recherche · shop OK | **OK** | Phase 10 markers |
| M5 | Visibilité catégories | Entrées masquées si absent / sans produit publié | **OK** | Boissons · Artisanat absents |

**Comportement retenu** : regroupement `website.menu` enfant sous **Nos univers** (`url=#`) · rendu offcanvas Odoo natif · CSS masque les entrées `.ck-nav-desktop-universe` en mobile et `.ck-nav-mobile-univers` en desktop.

---

## 5. Non-régression fonctionnelle

| Parcours | Attendu | Résultat |
| --- | --- | --- |
| Recherche | Modal / barre OK | **OK** (header inchangé hors nav) |
| Compte | Lien connexion OK | **OK** |
| Panier | Compteur + `/shop/cart` | **OK** (hors périmètre checkout) |
| Boutique | `/shop` + filtre catégorie | **OK** |
| Professionnels | `/professionnels` · `ck-pro-page` | **OK** |
| Contact | `/contactus` via mega Découvrir | **OK** |
| Home S4 | **Inchangée** | **OK** (aucun diff S4 dans le lot) |

---

## 6. Checklist §10 bis — points de vigilance fin de lot

### 6.1 Desktop 1280 px — libellé « Soin & Bien-être »

| Point de contrôle | Attendu | Résultat | Réserve |
| --- | --- | --- | --- |
| Retour à la ligne | Aucun libellé sur 2 lignes | **OK** | — |
| Troncature | Pas d’ellipse illisible | **OK** | — |
| Logo | Pas de chevauchement marque | **OK** | — |
| Chrome droit | Pas de chevauchement recherche · compte · panier | **OK** | — |
| Espacement | Rythme lisible | **OK** | 4 entrées visibles seed (Boissons/Artisanat masqués) — tenue confortable à 1280 |

### 6.2 Contraste mega-menu Découvrir

| Point de contrôle | Attendu | Résultat | Réserve |
| --- | --- | --- | --- |
| Liens header top-level | Pas de `#d84315` en `color:` texte | **OK** | Nav top-level en `$ck-text-muted` |
| Liens mega Découvrir hover/focus | `$ck-primary-text` / `#bf360c` | **OK** | `website_header.scss` L171 · L303 |
| Fonds bouton / badge | Inchangés (`$ck-primary` background) | **OK** | Badge panier conservé |

### 6.3 Mobile 390 px — « Nos univers »

| Point de contrôle | Attendu | Résultat | Réserve |
| --- | --- | --- | --- |
| Clic **Nos univers** | Déplie · ne navigue pas (`url=#`) | **OK** | Dropdown natif Odoo |
| Liens enfants | Épicerie · Soin & Bien-être → navigation catégorie | **OK** | Enfants sync dynamique |
| Drawer / offcanvas | Hiérarchie claire | **OK** | — |
| Overflow | Zéro overflow horizontal | **OK** | `overflow-x: clip` mobile |
| UX déplier vs page | Pas de confusion | **OK** | — |

---

## 7. Implémentation — référence technique

| Composant | Emplacement |
| --- | --- |
| Sync menus + visibilité | `dorevia_ck_marketone_content/nav_sync.py` |
| Champ CSS menu | `dorevia_ck_marketone_content/models/website_menu.py` |
| Template classes submenu | `dorevia_ck_marketone_content/views/website_nav_ck_v1.xml` |
| Bootstrap post-init / migration | `hooks.py` · `migrations/19.0.1.26.0/post-migrate.py` |
| Désactivation CTA header | `dorevia_ck_theme/views/website_nav_ck_v1.xml` |
| Styles desktop/mobile/contraste | `dorevia_ck_theme/static/src/scss/website_header.scss` |

---

## 8. Verdict fin de lot

| Rôle | Verdict | Date |
| --- | --- | --- |
| Dev | **Lot Nav-1 livré · correctifs B1/B2 · tests 15/15 OK** | 2026-06-21 |
| Testeur | **GO merge** — recette initiale NO GO (B1/B2) · re-recette §8 bis OK · captures `_postfix` | 2026-06-21 |
| MOA | **GO merge PR** · enchaînement **Lot Nav-2** (pages éditoriales Découvrir) | — |

**Références QA** : [`NOTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md`](./NOTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md) §8 · §8 bis.

**Rappels non bloquants** (notés pour info) :

- Requête Google Fonts externe (Inter) — hors périmètre Nav-1 · ticket séparé.
- Rebootstrap manuel `bootstrap_ck_navigation(env)` après passage tests `HttpCase` sur instance partagée.

---

*Recette QA Lot Nav-1 · Navigation CK V2 · **clôturée GO merge · 2026-06-21**.*
