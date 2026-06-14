# Recette QA — Phase 10 · Recette globale go-live · CK V1.2.x

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Conteneur** | `sandbox-odoo19-odoo-1` |
| **Gouvernance** | [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) **§5undecies** |
| **Prérequis** | Phases 1–9 **clôturées OK partiel MOA · 2026-06-14** |
| **Modules** | `dorevia_ck_theme` **19.0.1.12.0** · `dorevia_ck_marketone_content` **19.0.1.0.0** |
| **Statut dossier** | **✅ Phase 10 §3–§9 clôturée OK partiel MOA · 2026-06-14** |
| **A1 header** | **✅ A1-OK clôturé · non rouvert** |
| **Rapport §3–§9** | [`RAPPORT_PHASE10_TRANSVERSALE_20260614.md`](./RAPPORT_PHASE10_TRANSVERSALE_20260614.md) |

```text
PHASE 10 — RECETTE GLOBALE GO-LIVE (pas nouvelle feature)
Priorité absolue : header / menu / branding CK
Dev interdit sans acte MOA GO exécution §5undecies explicite
Split thème / contenu : non rouvert
```

> Recette multi-base : header HTTP `X-Odoo-Database: dorevia_ck_marketone_01` · cache-bust `?qa_ts=1` recommandé MOA.

---

## 0. Rappel gouvernance

| Règle | Statut |
|-------|--------|
| Phases 1–9 clôturées OK partiel MOA | ✅ |
| Phase 10 = recette transversale go-live | ✅ **Doctrine actée** |
| Nouvelle feature / refonte fonctionnelle | ❌ **Interdit Phase 10** |
| Dev Phase 10 header | ☑ **GO exécution §5undecies acté · livré 19.0.1.11.0** |
| Recette MOA écran §2 | ✅ **A1-OK clôturé · 19.0.1.12.0** |
| Recette §3–§9 transversale | ✅ **OK partiel MOA · 2026-06-14** |
| Split thème / contenu §4bis | **Non rouvert** |
| Migrations historiques thème | Réserve post-V1 · **non bloquante** |
| Automation marketing | ❌ **Hors périmètre** |
| Phase postérieure sans verdict go-live | ❌ **Interdit** |

**Références header (dette transversale Phases 1–9)** :

| Document | Rôle |
|----------|------|
| [`RECETTE_QA_PHASE1_HEADER_FOOTER_CK_V1.md`](./RECETTE_QA_PHASE1_HEADER_FOOTER_CK_V1.md) | Baseline Phase 1 |
| [`note_reference_header_mega_menu_decouverte_ck_v1.md`](./note_reference_header_mega_menu_decouverte_ck_v1.md) | Cible H1 · mega Découvrir |
| [`COMPOSITION_HEADER_V1_2.md`](./COMPOSITION_HEADER_V1_2.md) | Composition header instance |

---

## 1. Périmètre Phase 10 (strict · recette uniquement)

| # | Axe recette | Priorité | Référence phase |
|---|-------------|----------|-----------------|
| 10.1 | **Header / menu / branding CK** | **P0 · absolue** | Phase 1 · dette go-live |
| 10.2 | Mobile 390 px (toutes pages 1–9) | P0 | Transversal |
| 10.3 | Footer / mentions / liens légaux | P1 | Phase 1 |
| 10.4 | Liens morts · routes · mapping BO | P1 | Transversal |
| 10.5 | Copy M5 (réassurance) | P1 | Phase 2 · 3 |
| 10.6 | Checkout / panier | P1 | Phase 3 · CE natif |
| 10.7 | Newsletter | P1 | Phase 9 |
| 10.8 | Formulaires (Contact B2C · CRM Pro · newsletter) | P1 | Phases 5–6–9 |
| 10.9 | Assets / cache / SSR | P1 | Transversal |
| 10.10 | Non-régression Phases 1–9 | P0 | Gates existants |
| 10.11 | Verdict MOA go-live V1 | — | Acte final distinct |

**Hors périmètre Phase 10** :

```text
Nouvelle page CMS · blog · portail · B2B custom · checkout custom
Refonte catalogue · origines/collections custom · automation marketing
Réouverture split dorevia_ck_theme / dorevia_ck_marketone_content
Modification profonde checkout (hors recette CE natif)
```

---

## 2. Grille prioritaire — Header / menu / branding CK · **P0**

> Dette UX/UI signalée Phases 7–9 : header très natif Odoo vs pages CK stylées. Phase 10 contrôle et arbitre — **correction Dev uniquement si actée MOA §5undecies exécution**.

### 2.1 Logo & identité

| # | Contrôle | Attendu go-live | Bloquant | Résultat |
|---|----------|-----------------|----------|----------|
| H1 | Logo site | Logo CK réel · pas « Your Logo » / placeholder Odoo | ☑ | ✅ Dev |
| H2 | Lien logo | Retour `/` · HTTP 200 | ☑ | ✅ Dev |
| H3 | Alt / accessibilité | Texte alternatif lisible | ☐ | ☐ |
| H4 | Cohérence marque | Aligné nom site **C-Kreyol** / CK Marketone acté instance | ☐ | ☐ |
| H5 | Favicon | Présent · pas défaut Odoo générique (si asset BO disponible) | ☐ | ☐ |

### 2.2 Header desktop (1280 px)

| # | Contrôle | Attendu go-live | Bloquant | Résultat |
|---|----------|-----------------|----------|----------|
| H6 | Entrées nav principales | **Boutique · Découvrir · Professionnels · Contactez-nous** | ☑ | ✅ Dev |
| H7 | Pas « Catégories » technique | Libellé client « Découvrir » ou équivalent acté H1 | ☐ | ✅ Dev |
| H8 | Entrée Producteurs | Option MOA post-recette · **non bloquant V1** si absent | ☐ | ✅ absent |
| H9 | Mega-menu Découvrir | Panel `o_mega_menu` natif CE · ouverture/fermeture OK | ☑ | ☐ MOA écran |
| H10 | Mega — liens BO réels | Épicerie créole · pas URL 404 · gate M4 | ☑ | ✅ Dev |
| H11 | Mega — colonne origines | Différée si 0 attribut BO · **non bloquant** si masquée | ☐ | ☐ |
| H12 | Mega — Comprendre / recettes | `/recettes` · `/a-propos` si acté MOA post-recette · **non bloquant V1** | ☐ | ☐ |
| H13 | Recherche native | Modal / champ fonctionnel | ☑ | ☐ |
| H14 | Panier native | Icône · lien `/shop/cart` | ☑ | ☐ |
| H15 | Compte / connexion | Comportement CE natif · pas régression | ☐ | ☐ |
| H16 | Sticky / scroll | Comportement stable · pas saut layout | ☐ | ☐ MOA écran |
| H17 | Contraste · lisibilité | Texte nav lisible sur fond header | ☑ | ☐ MOA écran |
| H18 | Cohérence visuelle CK | Tokens thème · habillage `ck-header` | ☐ | ☐ MOA écran |
| H19 | Pas overflow horizontal | 1280 / 1280 | ☑ | ☐ MOA écran |

### 2.3 Menu mobile (390 px)

| # | Contrôle | Attendu go-live | Bloquant | Résultat |
|---|----------|-----------------|----------|----------|
| H20 | Burger / offcanvas | Ouverture · fermeture · focus OK | ☑ | ☐ MOA écran |
| H21 | Nav mobile complète | Mêmes entrées que desktop (hors mega replié) | ☑ | ☐ MOA écran |
| H22 | Mega mobile | Accessible · pas overflow · pas contenu coupé | ☑ | ☐ MOA écran |
| H23 | Recherche mobile | Accessible depuis offcanvas ou barre | ☑ | ☐ |
| H24 | Panier mobile | Accessible | ☑ | ☐ |
| H25 | Touch targets | CTA / liens suffisamment grands | ☐ | ☐ MOA écran |
| H26 | Pas overflow horizontal | 390 / 390 | ☑ | ☐ MOA écran |
| H27 | Branding offcanvas | Cohérence CK vs pages stylées | ☐ | ☐ MOA écran |

### 2.4 Comportement transversal header

| # | Contrôle | Attendu | Bloquant | Résultat |
|---|----------|---------|----------|----------|
| H28 | Header identique pages 1–9 | `/` · `/shop` · `/contactus` · `/recettes` · etc. | ☑ | ✅ Dev |
| H29 | Pas effet natif Odoo non assumé | Arbitrage MOA post-habillage `ck-header` | ☐ | ☐ MOA écran |
| H30 | Non-régression parcours | Liens header · pas 404 critique depuis nav | ☑ | ✅ Dev |

**Synthèse header §2** :

| Nature | Verdict | Clôture §2 |
|--------|---------|------------|
| Contrat HTML / logo / assets / mega BO | ✅ **OK v2** | ☑ |
| Fonctionnel (nav · mega · mobile · overflow) | ✅ A1-OK MOA | ☑ |
| Branding CK header | ✅ A1-OK MOA · 19.0.1.12.0 | ☑ |
| Dette header acceptée go-live V1 | — | ☑ **Non · header validé** |

---

## 2bis. Pré-contrôle technique §2 · **OK partiel · 2026-06-14**

> **Méthode** : contrôle HTML/DOM fiable depuis le conteneur Odoo · DB `dorevia_ck_marketone_01` forcée · cache-bust `?qa_ts=1`.
> **Limite** : contrôle visuel écran (Codex / Playwright / Browser hôte) **non conclusif** (instabilité accès navigateur). **MOA écran 1280 + 390 requis** avant clôture §2.

### Verdict pré-contrôle technique

```text
Pré-contrôle technique Phase 10 §2 : OK partiel.
Contrat HTML / header / assets / logo : OK.
Contrôle visuel écran : non conclusif (instabilité hôte / navigateur).
MOA écran 1280 + 390 : requis avant clôture §2.
Point vivant : finition menu · rendu mobile · cohérence visuelle header · contraste · overflow.
```

### Observations DOM · `/` · `/contactus` · `/recettes`

| Contrôle | Résultat | Note |
|----------|----------|------|
| `<!DOCTYPE html>` · page complète | ✅ | |
| `body.ck-theme` | ✅ | |
| `web.assets_frontend` | ✅ | |
| Logo BO `C-Kreyol` · alt `C-Kreyol` | ✅ | Pas « Your Logo » |
| Header · footer présents | ✅ | |
| Nav cohérente (3 pages) | ✅ | **Boutique · Découvrir · Professionnels · Contactez-nous** |
| Entrée header **Producteurs** | ❌ absent | **Conforme gate Phase 1 / H1** · non bloquant V1 · option post-recette |
| `o_mega_menu` | ✅ | |
| Mega · **Épicerie créole** → `/shop/category/epicerie-creole-1` | ✅ | |
| Mega · `/recettes` · `/a-propos` | absent | Non bloquant V1 si MOA acte |
| Nav **Catégories** (libellé technique) | absent | Conforme H1 |

**Correction discours QA** : le constat Dev antérieur « Producteurs présent sur `/` et `/shop` » dans le header **n’est pas confirmé** sur le contrôle DOM MOA (`/`, `/contactus`, `/recettes`). Seul **Professionnels** apparaît comme entrée pro du header — pas **Producteurs**.

**Point MOA à apprécier écran** : entrée **Contactez-nous** dans la nav principale (vs capital Phase 1 « contact via footer / pas nav principal ») — arbitrage finition go-live si besoin · **non bloquant** sauf décision MOA contraire.

```text
Socle technique header : nettement plus propre (logo · assets · mega · liens BO).
OK visuel final : non signé sur cette passe seule.
Aucun GO exécution Dev §5undecies · aucun changement header tant que non acté.
```

**URLs MOA recontrôle visuel §2** :

```text
http://localhost:18079/?db=dorevia_ck_marketone_01&qa_ts=1
http://localhost:18079/contactus?db=dorevia_ck_marketone_01&qa_ts=1
http://localhost:18079/recettes?db=dorevia_ck_marketone_01&qa_ts=phase10
```

---

## 2ter. Livraison Dev header · GO §5undecies · **2026-06-14**

> Périmètre strict : habillage visuel header/menu/branding · pas de modification fonctionnelle.

### Acte MOA — GO exécution §5undecies ciblé header

```text
GO EXÉCUTION PHASE 10 — Header / menu / branding CK
Périmètre : logo · header desktop 1280 · mega Découvrir (habillage) · mobile 390
Hors scope : nouvelle page · refonte · checkout · Producteurs nav · mega fonctionnel
Module : dorevia_ck_theme 19.0.1.11.0
Validé par : MOA CK · 2026-06-14
```

### Livrables Dev

| Fichier | Rôle |
|---------|------|
| `views/website_header.xml` | Classe `ck-header` sur `header#top` |
| `static/src/scss/website_header.scss` | Sticky · logo · nav · hover · mega · offcanvas mobile · touch targets |
| `tests/test_ck_phase10_header_compose.py` | Contrat HTML · nav · non-régression 7 routes |
| `scripts/ck_phase10_ci.sh` | Gate upgrade + tests + smoke |

### Triptyque QA Dev · **OK · 2026-06-14**

| Niveau | Contrôle | Résultat |
|--------|----------|----------|
| **1. Contrat Odoo** | `--test-tags=dorevia_ck_theme_phase10` | ✅ 3/3 |
| **2. Smoke curl** | [`ck_phase10_ci.sh`](./scripts/ck_phase10_ci.sh) | ✅ 7 routes |
| **3. Playwright UX** | Desktop 1280 · mobile 390 | ☐ **MOA écran requis** |

### Smoke routes non-régression

| Route | HTTP | `ck-header` | Marqueur page |
|-------|------|-------------|---------------|
| `/` | ✅ 200 | ✅ | vedettes SSR |
| `/shop` | ✅ 200 | ✅ | `s_ck_shop_intro` |
| `/professionnels` | ✅ 200 | ✅ | `ck-pro-page` |
| `/contactus` | ✅ 200 | ✅ | `ck-contact-page` |
| `/a-propos` | ✅ 200 | ✅ | `ck-about-page` |
| `/recettes` | ✅ 200 | ✅ | `ck-recipes-page` |
| `/producteur/atelier-hauts-goyaviers` | ✅ 200 | ✅ | `ck-producer-page` |

### Verdict Dev · prêt recontrôle MOA

```text
Gate technique header : OK.
Habillage ck-header livré (tokens CK · sticky · nav hover · mega panel · mobile offcanvas).
Verdict visuel go-live V1 : non signé Dev — recontrôle MOA écran 1280 + 390 requis.
Verdicts MOA attendus post-recette §2 :
  · OK header/menu pour go-live V1
  · ou réserve mineure acceptée
  · ou correction complémentaire strictement listée
```

**URLs MOA recontrôle visuel post-Dev** :

```text
http://localhost:18079/?db=dorevia_ck_marketone_01&qa_ts=phase10
http://localhost:18079/shop?db=dorevia_ck_marketone_01&qa_ts=phase10
http://localhost:18079/professionnels?db=dorevia_ck_marketone_01&qa_ts=phase10
http://localhost:18079/contactus?db=dorevia_ck_marketone_01&qa_ts=phase10
```

---

## 3. Grille transversale go-live

### 3.1 Mobile 390 px — toutes pages Phases 1–9

| Page / route | Marqueur recette | Overflow 390 | Résultat |
|--------------|------------------|--------------|----------|
| `/` | Phase 2 · vedettes SSR · dual | ✅ | ✅ proxy |
| `/shop` | `s_ck_shop_intro` | ✅ | ✅ proxy |
| `/shop/<produit>` | `ck-product-page` | ✅ | ✅ proxy |
| `/shop/cart` | checkout container | ✅ | ✅ proxy |
| `/professionnels` | `ck-pro-page` | ✅ | ✅ proxy |
| `/contactus` | `ck-contact-page` | ✅ | ✅ proxy |
| `/a-propos` | `ck-about-page` | ✅ | ✅ proxy |
| `/recettes` | `ck-recipes-page` | ✅ | ✅ proxy |
| `/producteur/atelier-hauts-goyaviers` | `ck-producer-page` | ✅ | ✅ proxy |

**Gate mobile** : Playwright 390×844 ou recontrôle MOA manuel · **pas overflow horizontal**.

### 3.2 Footer / mentions

| # | Contrôle | Attendu | Bloquant | Résultat |
|---|----------|---------|----------|----------|
| F1 | Footer 4 colonnes | Structure Phase 1 visible | ☐ | ✅ proxy |
| F2 | Liens footer réels | Pas `#` · pas 404 footer | ☑ | ✅ proxy |
| F3 | Mentions légales | Si présentes BO · lien 200 · **non bloquant** si différé MOA | ☐ | ⚠️ absentes |
| F4 | Cohérence liens post Phases 6–8 | `/a-propos` · `/recettes` si ajoutés footer acté MOA | ☐ | ⚠️ non footer |

### 3.3 Liens morts · routes

| # | Contrôle | Attendu | Bloquant | Résultat |
|---|----------|---------|----------|----------|
| L1 | Nav principale | Tous liens 200 ou gate MOA documenté | ☑ | ✅ proxy |
| L2 | Mega-menu | Pas lien 404 publié | ☑ | ✅ proxy |
| L3 | Footer | Pas 404 | ☑ | ✅ proxy |
| L4 | Pages CMS 1–9 | Routes Phases 5–8 · 200 | ☑ | ✅ proxy |
| L5 | Produits publiés shop | Au moins 1 fiche 200 (instance pilote) | ☑ | ✅ proxy |
| L6 | Mapping BO | Catégories référencées existent | ☐ | ✅ proxy |

**Liste liens MOA à contrôler** (compléter lors recette) :

```text
/  /shop  /shop/cart  /contactus  /professionnels  /a-propos  /recettes
/producteur/atelier-hauts-goyaviers  /shop/category/epicerie-creole-1
```

### 3.4 Copy M5 (réassurance)

| Emplacement | Snippet / zone | Attendu | Bloquant | Résultat |
|-------------|----------------|---------|----------|----------|
| Home | `s_ck_reassurance` | Promesses **tenables** · pas sur-promesse | ☐ | ✅ proxy · relecture MOA |
| Shop | `ck-reassurance` (M5 compose) | Logistique · confiance · copy MOA | ☐ | ✅ proxy · relecture MOA |
| Fiche produit | réassurance M5 | Cohérent catalogue | ☐ | ⚠️ absent · non bloquant V1 |

**Gate M5** : toute promesse trop forte → **non bloquant go-live** si MOA accepte reformulation post-V1 · **bloquant** si mensonge / illégal.

### 3.5 Checkout / panier

| # | Contrôle | Attendu | Bloquant | Résultat |
|---|----------|---------|----------|----------|
| C1 | `/shop/cart` | HTTP 200 · container checkout CE | ☑ | ✅ proxy |
| C2 | Ajout panier | Depuis fiche produit publiée | ☑ | ✅ produit pilote |
| C3 | Parcours checkout CE | Natif · pas surcouche custom V1 | ☑ | ✅ proxy |
| C4 | Non-régression | Pas modification profonde checkout Phase 10 | ☑ | ✅ |

### 3.6 Newsletter (Phase 9)

| # | Contrôle | Attendu | Bloquant | Résultat |
|---|----------|---------|----------|----------|
| N1 | `/contactus` | `#ck-newsletter-subscribe` · dual compact | ☑ | ✅ proxy |
| N2 | `/professionnels` | Newsletter distincte · dual compact | ☑ | ✅ proxy |
| N3 | Mailing list BO | `Newsletter CK` · `data-list-id` | ☑ | ✅ gate9 |
| N4 | Subscribe fonctionnel | POST `/website_mass_mailing/subscribe` | ☑ | ✅ gate9 |
| N5 | RGPD | Mention consentement · désinscription | ☑ | ✅ proxy |
| N6 | Pas popup | Pas `s_newsletter_subscribe_popup` | ☑ | ✅ proxy |
| N7 | Home Phase 2 | Dual home intact · non-régression | ☑ | ✅ proxy |

### 3.7 Formulaires · séparation parcours

| Parcours | Page | Modèle | Attendu | Bloquant | Résultat |
|----------|------|--------|---------|----------|----------|
| Contact B2C | `/contactus` | `mail.mail` · `contactus_form` | Pas CRM Pro | ☑ | ✅ proxy |
| CRM Pro | `/professionnels` | `crm.lead` · `#ck-pro-form` | Pas contact B2C | ☑ | ✅ proxy |
| Newsletter | contact / pro | subscribe natif | Distinct formulaires | ☑ | ✅ proxy |

### 3.8 Assets / cache

| # | Contrôle | Attendu | Bloquant | Résultat |
|---|----------|---------|----------|----------|
| A1 | `web.assets_frontend` | Présent pages clés | ☑ | ✅ proxy |
| A2 | `body.ck-theme` | Présent pages clés | ☑ | ✅ proxy |
| A3 | Cache-bust recette | `?qa_ts=phase10t` · contenu à jour | ☐ | ✅ proxy |
| A4 | SSR vedettes home | `ck-featured-products__grid--stable` | ☑ | ✅ proxy |
| A5 | Pas assets cassés | Console sans 404 CSS/JS critique | ☑ | ✅ proxy |

### 3.9 Non-régression Phases 1–9

| Phase | Gate / script | Seuil | Résultat |
|-------|---------------|-------|----------|
| 1 | Recette header/footer | Baseline | ✅ A1-OK |
| 2 | `ck_phase2_*` / home markers | dual · vedettes | ✅ gate3 smoke |
| 3 | `ck_phase3_ci.sh` | smoke shop | ✅ 2026-06-14 |
| 4 | `ck_phase4_ci.sh` | fiche produit | ✅ 2026-06-14 |
| 5 | `ck_phase5_ci.sh` | pro CRM | ✅ 2026-06-14 |
| 6 | `ck_phase6_ci.sh` | contact · à-propos | ✅ 2026-06-14 |
| 7 | `ck_phase7_ci.sh` | producteur | ✅ 2026-06-14 |
| 8 | `ck_phase8_ci.sh` | recettes | ✅ 2026-06-14 |
| 9 | `ck_phase9_ci.sh` | newsletter | ✅ 2026-06-14 |
| 10 | `ck_phase10_ci.sh` | header | ✅ 2026-06-14 |

---

## 4. Critères go-live · bloquants / non bloquants

### 4.1 Bloquants go-live V1 (KO si échec)

```text
404 critique depuis nav principale · mega · footer
Overflow horizontal mobile 390 sur page clé parcours achat
Formulaire contact B2C confondu avec CRM Pro
Newsletter sans mention désinscription / consentement
Subscribe newsletter non fonctionnel
Panier / checkout CE inaccessible
Non-régression gates Phases 3–9 (smoke CI)
Séparation parcours Contact / Pro / Newsletter rompue
```

### 4.2 Non bloquants go-live V1 (dette documentée · OK partiel)

```text
Logo placeholder · finition branding header partielle
Mega-menu incomplet (origines · recettes non exposées) si gate MOA acté
Entrée nav Producteurs absente
Copy M5 à affiner métier
Mentions légales différées si MOA acte
Footer liens incomplets post Phases 6–8 si MOA acte
Header « trop natif Odoo » si MOA accepte dette go-live V1
Réserve migrations historiques thème §4bis post-V1
Marque blanche snippets (textes CK dans thème)
```

### 4.3 Matrice arbitrage MOA

| Situation | Verdict possible |
|-----------|------------------|
| Tous bloquants OK · dettes non bloquantes acceptées | **OK partiel MOA go-live V1** |
| Bloquant KO | **KO · correction requise** (Dev §5undecies exécution si correction code) |
| Header branding KO mais fonctionnel OK | **OK partiel** · dette header · ou **GO Dev header** acté séparément |

---

## 5. Garde-fous Phase 10 (rappel opposable)

| Garde-fou | Statut |
|-----------|--------|
| Pas nouvelle feature | ✅ |
| Pas refonte fonctionnelle | ✅ |
| Pas réouverture split thème/contenu | ✅ |
| Pas modification profonde checkout | ✅ |
| Pas automation marketing | ✅ |
| Pas nouvelle page CMS | ✅ |
| Pas phase postérieure sans verdict go-live | ✅ |
| Dev interdit sans GO §5undecies exécution | ✅ (GO header acté · périmètre strict) |

---

## 6. Triptyque QA Phase 10 (proposé)

| Niveau | Contrôle | Statut |
|--------|----------|--------|
| **1. Gates non-régression** | `ck_phase3_ci.sh` … `ck_phase9_ci.sh` | ✅ 8/8 |
| **2. Gate header Phase 10** | [`ck_phase10_ci.sh`](./scripts/ck_phase10_ci.sh) | ✅ |
| **3. Recontrôle transversal §3** | [`phase10_transversale_recette.py`](./scripts/phase10_transversale_recette.py) | ✅ 2026-06-14 |
| **4. §2 header A1** | A1-OK MOA | ✅ clôturé |

> Gate [`ck_phase10_ci.sh`](./scripts/ck_phase10_ci.sh) créé et validé post-GO exécution header · 2026-06-14

---

## 7. Modèle acte MOA — GO préparation §5undecies · **ACTÉ 2026-06-14**

```text
GO PRÉPARATION PHASE 10 — Recette globale go-live CK V1.2.x
Périmètre : dossier recette · grille header/menu · critères go-live
Exécution Dev : INTERDITE
Split thème/contenu : NON ROUVERT
Validé par : MOA CK
Date : 2026-06-14
```

---

## 8. Acte MOA — GO exécution §5undecies header · **ACTÉ 2026-06-14**

```text
GO EXÉCUTION PHASE 10 — Corrections header / menu / branding CK V1.2.x
Périmètre autorisé : logo · header desktop 1280 · mega Découvrir (habillage) · mobile 390
Interdit : nouvelle feature · nouvelle page · checkout custom · split thème/contenu · Producteurs nav
Modules : dorevia_ck_theme 19.0.1.11.0
Recette obligatoire : RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md §2
Validé par : MOA CK
Date : 2026-06-14
```

**Conditions préalables GO exécution** :

```text
☑ Dossier recette Phase 10 validé MOA (présent document)
☑ Périmètre Dev listé explicitement (header/menu/branding strict)
☑ Gates non-régression 1–9 définis
☑ Critères bloquants / non bloquants actés
```

---

## 9. Checklist verdict final go-live V1

| # | Item | ☐ |
|---|------|---|
| 1 | Grille header §2 exécutée · synthèse remplie | ☑ A1-OK |
| 2 | Mobile 390 toutes pages §3.1 | ☑ proxy |
| 3 | Footer / liens §3.2–3.3 | ☑ proxy · arbitrages F3/F4 |
| 4 | Copy M5 relue MOA §3.4 | ☑ proxy · ☐ relecture MOA métier |
| 5 | Checkout / panier §3.5 | ☑ proxy |
| 6 | Newsletter §3.6 | ☑ proxy |
| 7 | Formulaires / séparation §3.7 | ☑ proxy |
| 8 | Assets / cache §3.8 | ☑ proxy |
| 9 | Gates Phases 1–9 §3.9 | ☑ 8/8 |
| 10 | Aucun bloquant §4.1 ouvert | ☑ proxy |
| 11 | Dettes non bloquantes §4.2 actées MOA | ☑ **2026-06-14** |
| 12 | Garde-fous §5 respectés | ☑ |

### Verdict MOA Phase 10 §3–§9 · **signé 2026-06-14**

| Champ | Valeur |
|-------|--------|
| **Instance** | `dorevia_ck_marketone_01` |
| **Verdict recette Phase 10 transversale** | ✅ **OK partiel** |
| **Verdict go-live V1 Odoo CK** | **GO partiel interne** · **NO GO public** tant que mentions légales non traitées |
| **Dette header/menu** | ☑ **Validée A1-OK** · non rouvert |
| **Rapport §3–§9** | [`RAPPORT_PHASE10_TRANSVERSALE_20260614.md`](./RAPPORT_PHASE10_TRANSVERSALE_20260614.md) |
| **Validé par** | **MOA CK** |
| **Date** | **2026-06-14** |

#### Dettes §4.2 actées MOA

| # | Sujet | Décision MOA |
|---|-------|--------------|
| 1 | Hero / contenus accueil | Dette hors A1 · **lot dédié** · non bloquant séquence |
| 2 | Mega origines / recettes / à-propos | **Absence acceptée V1** · report volontaire documenté |
| 3 | Mentions légales footer | Non bloquant A7 · **bloquant go-live public** |
| 4 | Footer sans `/a-propos` · `/recettes` | **Accepté temporairement** · réexaminer si pages créées |
| 5 | M5 fiche produit | **Acceptable V1** si fiche native lisible · recontrôle lot fiche/boutique |
| 6 | Copy M5 home/shop | Présent · **relecture métier MOA** · non bloquant |
| 7 | Favicon BO | Présent · **relecture identité MOA** · non bloquant |

```text
Suite séquence MOA actée :
  1. ✅ Phase 10 §3–§9 transversale — OK partiel MOA
  2. A7 Git modules CK — acte MOA explicite dédié requis
  3. Chantier B navigateur (6.3a · 6.3b · SEO) — après A7
  4. Go-live public — NO GO tant que mentions légales non traitées
Aucun commit global sans demande explicite MOA.
```

---

## 10. Documents liés

| Document | Rôle |
|----------|------|
| [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) | §5undecies · gouvernance |
| [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) | Phase 10 séquence |
| [`recette_qa_composition_cms_ck_01.md`](../recette_qa_composition_cms_ck_01.md) | Composition CMS globale |
| [`RECETTE_QA_PHASE1` … `RECETTE_QA_PHASE9`](./) | Recettes phases · non-régression |

---

*Dossier recette Phase 10 — A1-OK · §3–§9 OK partiel MOA · GO partiel interne · NO GO public (mentions légales) · 2026-06-14.*
