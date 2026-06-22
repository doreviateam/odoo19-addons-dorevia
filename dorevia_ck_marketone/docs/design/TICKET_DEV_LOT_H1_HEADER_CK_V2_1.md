# Ticket Dev — Lot H1 · Header C-Kréyòl V2.1 (delta Strate 0/1 + chrome mobile)

| Champ | Valeur |
| --- | --- |
| **Projet** | `dorevia_ck_marketone` · C-Kréyòl / CK Marketone |
| **Lot** | **H1** — Header média-commerce · delta post-Nav-1 |
| **Modules** | `dorevia_ck_theme` (principal) · `dorevia_ck_marketone_content` (si bandeau wording / coexistence home) |
| **Type** | Header / chrome / marque · lot technique recettable |
| **Priorité** | Haute |
| **Statut** | **GO MOA cadrage** — **exécution après relecture ticket** |
| **Instance recette** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Documents source** | [`note_07.md`](../cadrage/note_07.md) · [`note_07_reponse_moa.md`](../cadrage/note_07_reponse_moa.md) · [`note_07_retour_dev.md`](../cadrage/note_07_retour_dev.md) |

```text
Objectif : livrer le delta header V2.1 non couvert par Nav-1 —
bandeau service global (Option A), marque C-Kréyòl renforcée,
recherche centrale produits-only, chrome e-commerce et mobile chrome.

Nav-1 = baseline navigation FIGÉE — ne pas rouvrir nav_sync.py ni les menus.
```

---

## 1. Contexte

### 1.1 Cadrage MOA

Le header C-Kréyòl V2.1 vise un **header média-commerce** : e-commerce d’abord, réassurance, marque forte, découverte éditoriale via **Découvrir** (déjà livré Nav-1).

Arbitrages MOA actés le **2026-06-21** — voir [`note_07_reponse_moa.md`](../cadrage/note_07_reponse_moa.md) et amendements [`note_07.md`](../cadrage/note_07.md) §8 bis · §9 bis · §11 bis · §18.1 bis · §19 bis.

### 1.2 État post-Nav-1 (baseline figée)

| Élément | Statut |
| --- | --- |
| Navigation desktop | Tous nos produits · Épicerie · Soin & Bien-être · Découvrir |
| Navigation mobile | Tous nos produits · Nos univers · Découvrir |
| Mega Découvrir | Pro · Recettes · Contactez-nous · Producteurs pilote |
| Professionnels | **Sous Découvrir** — pas top-level |
| Modules Nav-1 | content **19.0.1.26.1** · theme **19.0.1.37.1** |
| Recette QA | GO merge · PR #78 |

**Règle absolue H1** : aucune modification de `nav_sync.py`, `website.menu` commerce, mega contenu, classes `ck-nav-*` navigation, tests tag `dorevia_ck_marketone_nav_sync`.

### 1.3 Delta H1 (ce ticket)

| Strate | Livrable H1 |
| --- | --- |
| **0** | Bandeau service global Option A |
| **1** | Logo **C-Kréyòl** · recherche centrale · compte · panier renforcés |
| **Mobile** | Chrome `Menu · C-Kréyòl · Recherche · Panier` · compte dans drawer |

---

## 2. Périmètre IN (Lot H1)

| # | Livrable |
| ---: | --- |
| H1-1 | **Strate 0** — bandeau global toutes pages : `Produits créoles sélectionnés · Origines identifiées · Livraison suivie` |
| H1-2 | Coexistence home `/` : pas de doublon message avec trust-bar S2 (cf. §9 bis `note_07`) |
| H1-3 | **Rebrand** logo header + `aria-label` : **C-Kréyòl** (caractère **ò** validé en recette) |
| H1-4 | Renforcement visuel logo (taille, poids, contraste — sans écraser recherche/panier) |
| H1-5 | **Recherche centrale** desktop : barre large visible · placeholder `Rechercher un produit, une saveur...` |
| H1-6 | Recherche mobile : accessible depuis chrome ligne 1 (icône ou champ selon layout retenu) |
| H1-7 | Moteur recherche : **produits / catalogue Odoo standard** uniquement — pas origine/recette/producteur |
| H1-8 | Chrome e-commerce : panier prioritaire visuellement sur compte · compteur lisible |
| H1-9 | **Mobile chrome** : `Menu · C-Kréyòl · Recherche · Panier` · compte dans offcanvas |
| H1-10 | SCSS tokens CK · contraste WCAG usages texte header (`$ck-primary-text` / `#bf360c` si `color:`) |
| H1-11 | Préservation sticky header (QWeb critical + `website_header.scss` — pattern Phase 10) |
| H1-12 | Tests header mis à jour (`dorevia_ck_theme_phase10` + tests H1 dédiés si créés) |
| H1-13 | Recette QA documentée desktop **1280** + mobile **390** |
| H1-14 | **Non-régression Nav-1** : navigation inchangée · 15 tests nav_sync + phase10 verts |

---

## 3. Hors périmètre (interdit dans H1)

| Zone | Raison |
| --- | --- |
| Sync menus · `nav_sync.py` | Nav-1 figé |
| Mega Découvrir · contenu liens | Nav-1 / Nav-2 |
| Professionnels top-level | Nav-1 bis si pivot MOA |
| Libellés « Épicerie créole » header | Nav-1 bis |
| Hub `/producteurs` | **H2** |
| Migration `/contactus` → `/contact` | Hors scope |
| Refonte shop · home S4 · fiche produit | Tickets distincts |
| Blog · forum · communauté | Hors V1 |
| Compte pro · B2B · favoris | Hors V1 |
| Recherche multi-contenus | Hors H1 |
| Page résultats vide custom | **H1 bis** backlog |
| Moteur recherche avancé | Hors H1 |

---

## 4. Spécifications fonctionnelles

### 4.1 Strate 0 — Bandeau service global

| Attribut | Valeur |
| --- | --- |
| Wording | `Produits créoles sélectionnés · Origines identifiées · Livraison suivie` |
| Portée | **Toutes les pages** (hors backend / éditeur si non pertinent) |
| Comportement | Statique · pas d’animation · pas de CTA |
| Style | Hauteur réduite · fond chaud ou rouge CK sobre · texte lisible |

**Home `/`** : vérifier coexistence avec trust-bar Section 2 — documenter le choix retenu en recette (allègement trust-bar ou rôles distincts).

### 4.2 Strate 1 — Logo C-Kréyòl

| Attribut | Valeur |
| --- | --- |
| Graphie | **C-Kréyòl** (accents officiels) |
| Technique actuelle | `C-Kreyol` typographique · `website_header.xml` |
| Cible | Texte renforcé ou asset header dédié MOA |
| Recette obligatoire | Lisibilité **ò** · 1280 + 390 px · pas de tofu / fallback illisible |

### 4.3 Strate 1 — Recherche

| Attribut | Valeur |
| --- | --- |
| Placeholder desktop | `Rechercher un produit, une saveur...` |
| Scope moteur | Produits publiés · catégories · termes fiche produit |
| Hors scope | Recettes · producteurs · pages CMS |
| Vigilance UX | Requêtes éditoriales → résultats vides Odoo standard (H1 bis) |

### 4.4 Strate 1 — Compte · Panier

| Règle | Détail |
| --- | --- |
| Compte | Standard Odoo CE · pas de logique pro |
| Panier | Visible · compteur · accent CK · priorité visuelle > compte |
| CTA Contact header | **Absent** (Nav-1) |

### 4.5 Mobile chrome

| Élément | Cible H1 |
| --- | --- |
| Ligne 1 | Menu (burger) · **C-Kréyòl** · Recherche · Panier |
| Compte | Dans le **drawer** (pas icône header si MOA chrome strict) |
| Drawer contenu | **Nav-1 inchangé** (Tous nos produits · Nos univers · Découvrir) |
| Contact | Via Découvrir + footer — **pas** entrée directe drawer |

---

## 5. Spécifications techniques (Odoo 19 CE)

### 5.1 Fichiers probables

| Composant | Emplacement |
| --- | --- |
| Bandeau Strate 0 | `dorevia_ck_theme/views/website_header.xml` (ou vue dédiée `website_header_service_bar.xml`) |
| Logo C-Kréyòl | `dorevia_ck_theme/views/website_header.xml` |
| Layout recherche | Héritages templates header Odoo 19 (`website.template_header_*`) |
| Styles | `dorevia_ck_theme/static/src/scss/website_header.scss` (+ fichier bandeau si séparé) |
| Coexistence home | Possible ajustement `home_reassurance.py` / snippet — **minimal** · documenter |

### 5.2 Principes

* Héritages QWeb · pas de HTML parallèle non maintenable ;
* Sticky : conserver duplication volontaire QWeb `<head>` + SCSS ;
* Pas de modification `nav_sync.py` ;
* Bump version `dorevia_ck_theme` (et content si touché) à chaque livraison.

### 5.3 Tests

| Tag / suite | Attendu |
| --- | --- |
| `dorevia_ck_theme_phase10` | Mis à jour · C-Kréyòl · bandeau · recherche placeholder |
| `dorevia_ck_marketone_nav_sync` | **15/15 inchangés** — non-régression Nav-1 |
| Tests H1 dédiés (recommandé) | Bandeau présent · pas de régression `#top_menu` structure Nav-1 |

---

## 6. Recette QA

### Desktop 1280 px

| # | Scénario | Attendu |
| ---: | --- | --- |
| R1 | Bandeau Strate 0 | Wording exact · discret · toutes pages testées (`/`, `/shop`) |
| R2 | Logo | **C-Kréyòl** lisible · **ò** correct |
| R3 | Recherche | Barre centrale visible · placeholder V1 |
| R4 | Panier · compte | Présents · panier ≥ compte visuellement |
| R5 | Navigation | **Identique Nav-1** — 4 entrées desktop |
| R6 | Mega Découvrir | Inchangé Nav-1 |
| R7 | Sticky scroll | Fond opaque · pas de transparence contenu |
| R8 | Contraste | Texte header lisible · usages `color:` conformes |

### Mobile 390 px

| # | Scénario | Attendu |
| ---: | --- | --- |
| M1 | Chrome ligne 1 | Menu · C-Kréyòl · Recherche · Panier |
| M2 | Drawer | Nav-1 inchangé · Nos univers OK · pas doublon univers |
| M3 | Compte | Dans drawer |
| M4 | Bandeau | Lisible · pas d’overflow horizontal |
| M5 | Logo **ò** | Lisible à 390 px |

### Non-régression Nav-1

| # | Contrôle | Attendu |
| ---: | --- | --- |
| N1 | Tests auto nav_sync + phase10 | 15/15 OK |
| N2 | Pas Professionnels top-level | Inchangé |
| N3 | Home S4 | Inchangée |

---

## 7. Livrables fin de lot

1. Code Strate 0 + Strate 1 + mobile chrome (PR module).
2. Tests header mis à jour · non-régression Nav-1 documentée.
3. Recette QA `RECETTE_QA_LOT_H1_HEADER_CK_V2_1.md` (à créer en fin de lot).
4. Bump versions `__manifest__.py` modules touchés.
5. Note coexistence bandeau / trust-bar home dans recette.

---

## 8. Critères d’acceptation MOA

| # | Critère | Attendu |
| ---: | --- | --- |
| C1 | Bandeau Option A global | Wording §4.1 · toutes pages |
| C2 | C-Kréyòl header | Graphie officielle · recette **ò** |
| C3 | Recherche centrale | Placeholder V1 · produits only |
| C4 | Mobile chrome | §4.5 |
| C5 | Nav-1 non régressé | Navigation + mega + mobile drawer |
| C6 | Tests | phase10 + nav_sync verts |
| C7 | Hors périmètre | Aucun diff navigation / nav_sync |
| C8 | Home S4 | Inchangée |
| C9 | Sticky / contraste | Non-régression Phase 10 |

---

## 9. Séquencement et dépendances

```text
Prérequis : Nav-1 mergé sur main (PR #78)
Lot H1      → ce ticket (delta header)
Lot H2      → hub /producteurs · pages provisoires
Lot H1 bis  → UX recherche vide
Lot Nav-2   → enrichissement éditorial Découvrir
Nav-1 bis   → pivot navigation si MOA (hors H1)
```

**Pas d’exécution Dev** tant que ce ticket n’a pas été **relu MOA / Dev**.

---

## 10. Verdict attendu

| Rôle | Verdict |
| --- | --- |
| MOA | GO cadrage acté · relecture ticket avant exécution |
| Dev | Ticket prêt exécution post-relecture |
| QA | Recette H1 + non-régression Nav-1 |

---

*Ticket Dev Lot H1 · Header C-Kréyòl V2.1 · delta post-Nav-1 · 2026-06-21.*
