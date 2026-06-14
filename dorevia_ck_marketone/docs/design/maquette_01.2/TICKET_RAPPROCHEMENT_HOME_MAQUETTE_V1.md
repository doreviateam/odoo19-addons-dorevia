# Ticket — Rapprochement Home Maquette V1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Type** | Ticket MOA / composition home · recette d’écarts visuels et commerciaux |
| **Instance cible** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Maquette référence** | CK V1.2 « Boutique élégante » — [`artifact/index.html`](./artifact/index.html) |
| **GO MOA cadrage** | **Acté 2026-06-14** — sans développement immédiat |
| **Statut ticket** | **Cadrage validé · en attente GO exécution Dev** |

---

## 0. Acte MOA — cadrage (2026-06-14)

```text
Décision MOA : GO cadrage ticket Rapprochement Home Maquette V1 — sans Dev immédiat.
Diagnostic partagé : socle Odoo fonctionnel propre, pas encore au niveau éditorial/commercial maquette.
Méthode : recette d’écarts par blocs — pas retouche CSS dispersée.
```

### Hors périmètre explicite (ne pas rouvrir)

| Lot | Statut |
|-----|--------|
| **A1 header Phase 10** | Clôturé — reprise header **uniquement** si écart réel confirmé dans ce ticket |
| **A7 modules CK maquette** | Mergé — pas de reprise Git modules |
| **Contenu légal local** | Clôturé PR #64 |
| **Chantier B** 6.3a / 6.3b / SEO | Clôturé navigateur MOA 2026-06-14 |

---

## 1. Diagnostic QA — écart maquette ↔ Odoo

### Constat Odoo actuel (capture recette)

- Header propre mais différent de la maquette (menu Découvrir vs Catégories, recherche icône vs champ visible, CTA Contact en première ligne).
- Hero très haut, aéré, image générique type bâtiment / cover Odoo par défaut.
- Réassurance visible — OK intention.
- Produits vedettes plus bas, **placeholders visibles** → impression non finie.
- **Absents** dans la zone visible maquette : coffret découverte horizontal, bloc double Pro/Newsletter structurant, texte éditorial bas « C-Kreyol, la boutique des saveurs créoles ».

### Intention maquette V1.2

- Page plus **compacte** et **marchande**.
- Logique **commerce + éditorial + conversion**.
- Blocs bas de page : coffret · dual Pro/newsletter · signature narrative CK.

### Verdict QA

```text
OK socle technique · OK snippets CK · KO rapprochement éditorial/commercial maquette finalisée.
Levier principal : blocs manquants + retrait placeholders — puis affinage densité / CTA / palette.
```

---

## 2. Objectif du ticket

Rapprocher la **page d’accueil Odoo** de la **maquette V1.2** en comblant les écarts **bloc par bloc**, sans refonte transversale.

**Doctrine** ([`note_05.md`](../../cadrage/note_05.md)) :

> Boutique claire, désirable, rassurante — élégance au service de la **conversion** (achat · fiche produit · panier · qualification Pro).

---

## 3. Ordre cible des blocs (maquette V1.2)

Référence : [`brief_01_2.md`](./brief_01_2.md) §5 · [`TABLEAU_TRADUCTION_ODOO_V1_2.md`](./TABLEAU_TRADUCTION_ODOO_V1_2.md)

```text
1. Header marchand          → A1 clos · vigilance seulement si écart confirmé
2. Hero court               → Lot 1
3. Réassurance immédiate    → Lot 0 (ajustements copy mineurs si besoin)
4. Produits vedettes        → Lot 2
5. Catégories / univers     → Lot 0 (conservé · recette non-régression)
6. Coffrets découverte      → Lot 3
7. Dual Pro / Newsletter    → Lot 4
8. Éditorial bas de page    → Lot 5
9. Footer                   → Phase 1 / contenu légal · hors ticket
```

**Ordre Phase 2 actuel** (référence baseline) :

```text
Hero → Réassurance → Vedettes → Catégories → Dual Pro/newsletter → Bandeau Pro → Footer
```

**Écart structurel** : insérer **Coffrets** après catégories · **Éditorial** avant footer · harmoniser **Dual** vs **Bandeau Pro** (éviter redondance Pro — arbitrage MOA à l’exécution).

---

## 4. Découpage par lots exécutables

### Lot 0 — Baseline · non-régression

| Élément | Action |
|---------|--------|
| Réassurance `s_ck_reassurance` | Conserver · copy M5 |
| Catégories `s_ck_category_links` | Conserver · gate M4 (2 catégories BO 200) |
| Header / footer Phase 1 | **Ne pas modifier** sans acte A1 |
| Tests existants | `dorevia_ck_theme_phase2` · smoke `/` · vedettes SSR |

---

### Lot 1 — Hero compact + visuel CK

| Champ | Détail |
|-------|--------|
| **Écart** | Hero trop haut · image institutionnelle · densité faible |
| **Cible maquette** | Promesse courte · CTA boutique + Pro · visuel produit/terroir |
| **Snippet** | `dorevia_ck_theme.s_ck_hero` |

| Voie | Faisabilité | Impact |
|------|-------------|--------|
| **Website Builder** | Copy · image BO · padding sections | Faible · sans merge thème |
| **CMS / homepage arch** | Réordonner padding classes sur vue `website.homepage` | `dorevia_ck_marketone_content` ou script configure |
| **SCSS thème** | `.ck-hero` hauteur max · ratio image | **`dorevia_ck_theme`** — **acte MOA séparé** si dépasse tokens existants |

**Critères QA Lot 1**

| ID | Critère |
|----|---------|
| H1 | Hero visible above-the-fold sans scroll excessif (1280 · 1440) |
| H2 | Aucune image cover Odoo générique (`website.s_cover_default_image`) en recette |
| H3 | CTA `/shop` + lien Pro `/professionnels` présents |
| H4 | Mobile 390 : hero empilé · pas d’overflow |

---

### Lot 2 — Produits vedettes sans placeholders

| Champ | Détail |
|-------|--------|
| **Écart** | Placeholders visibles · grille non finie |
| **Priorité** | **Haute** |
| **Mécanisme actuel** | Grille SSR `.ck-featured-products__grid--stable` · script [`ck_phase2_configure.py`](./scripts/ck_phase2_configure.py) · **5 produits BO** (Q1 §5ter) |

| Voie | Faisabilité | Impact |
|------|-------------|--------|
| **Données BO** | Images produit obligatoires · `is_published` · prix TTC | Catalogue / contenu |
| **CMS arch** | Masquer section si &lt; N produits prêts | Hook content ou Builder |
| **SSR grille** | Maintenir V1 — **pas** Dynamic Products / carousel (Q1 acté) | Script configure · migration content |

**Critères QA Lot 2**

```text
Sur desktop et mobile, aucun visuel placeholder ne doit apparaître sur la home publique.
```

| ID | Critère |
|----|---------|
| V1 | Grille SSR stable · **≥ 5** cartes produits réels |
| V2 | Chaque carte : image valide · prix · lien `/shop/…` HTTP 200 |
| V3 | Aucun `oe_product_image_img` vide / placeholder Odoo |
| V4 | Non-régression Q1 : pas de carousel · pas Dynamic Products |

---

### Lot 3 — Bloc Coffrets découverte

| Champ | Détail |
|-------|--------|
| **Écart** | Présent maquette · absent home Odoo visible |
| **Cible** | Section « Coffrets découverte » · carte produit horizontale · badge Pack · CTA Découvrir |
| **Route** | `/kits` ou `/shop?marketone_mode=pack` (Chantier B clôturé — lien fonctionnel) |

| Voie | Faisabilité | Impact |
|------|-------------|--------|
| **CMS Builder** | Section `s_text_block` + carte manuelle | Rapide · sans code |
| **Hook content** | `build_coffret_discovery_arch()` + bootstrap homepage | **`dorevia_ck_marketone_content`** · QWeb inline |
| **Snippet thème dédié** | `s_ck_discovery_pack` | **`dorevia_ck_theme`** — acte MOA si nouveau snippet |
| **Données** | 1 produit `pack_ok=True` publié avec image | BO · prep Chantier B réutilisable |

**Critères QA Lot 3**

```text
La home expose une entrée commerciale vers Kits & Coffrets, avec un produit réel ou une carte éditoriale cohérente.
```

| ID | Critère |
|----|---------|
| C1 | Bloc visible desktop + mobile |
| C2 | Lien `/kits` ou porte pack → 301/200 |
| C3 | Badge ou libellé Pack cohérent |
| C4 | Aucun placeholder image |

---

### Lot 4 — Bloc double Professionnels / Newsletter

| Champ | Détail |
|-------|--------|
| **Écart** | Maquette : bloc double structurant · Odoo : dual Phase 2 partiellement aligné visuellement |
| **Capital existant** | `build_dual_engage_compact_arch()` dans `dorevia_ck_marketone_content/hooks.py` (Phase 9 · contact/pro) |
| **Baseline Phase 2** | Dual 2 col + `s_newsletter_subscribe_form` natif · list_id mailing |

| Voie | Faisabilité | Impact |
|------|-------------|--------|
| **Réutiliser arch Phase 9** | Factoriser dual compact sur homepage | Content hooks |
| **Website Builder** | 2 colonnes · fond bleu-gris Pro · subscribe natif | Sans merge thème |
| **SCSS** | `.ck-dual-engage` radius · ombre · typo | Thème si classes existantes insuffisantes |

**Critères QA Lot 4**

```text
Le bloc pro/newsletter apparaît avant le footer, en deux colonnes desktop et empilé proprement mobile.
```

| ID | Critère |
|----|---------|
| D1 | Colonne gauche : « Vous êtes professionnel ? » · CTA `/professionnels` |
| D2 | Colonne droite : newsletter · formulaire fonctionnel ou placeholder MOA-validé |
| D3 | Desktop 1280/1440 : 2 colonnes · hauteurs équilibrées |
| D4 | Mobile 390 : empilement Pro puis newsletter · pas d’overflow |
| D5 | Non-régression M9 : `data-list-id` mailing si subscribe actif |

**Arbitrage MOA à l’exécution** : conserver ou retirer `s_ck_pro_banner` si redondant avec dual.

---

### Lot 5 — Bloc éditorial bas de page

| Champ | Détail |
|-------|--------|
| **Écart** | Signature narrative CK absente |
| **Cible maquette** | « C-Kreyol, la boutique des saveurs créoles » + liens démarche / producteur / recettes |

| Voie | Faisabilité | Impact |
|------|-------------|--------|
| **CMS pur** | `s_text_block` / `s_title` dans homepage arch | Builder ou hook content |
| **Pages liées** | `/a-propos` · `/recettes` · fiche producteur type (Phases 7–8) | Liens HTTP 200 |

**Critères QA Lot 5**

| ID | Critère |
|----|---------|
| E1 | Titre éditorial CK visible · pas de copy technique (« Inspiration réf. visuelle… ») |
| E2 | Liens : Notre démarche · Fiche producteur · Recettes — routes existantes 200 |
| E3 | Positionné **après** blocs marchands · **avant** footer |

---

### Lot 6 — Ajustements visuels transversaux (après blocs)

| Sujet | Action |
|-------|--------|
| Densité · marges | Rapprocher ±10–15 % maquette · tokens `--ck-space-*` existants |
| CTA rouge/orange | Harmoniser avec palette maquette |
| Bleu-gris Pro | Reprendre sur dual / coffret |
| Typo serif titres | Déjà en place · affiner hiérarchie H2 sections |

| Voie | Impact |
|------|--------|
| SCSS léger thème | **`dorevia_ck_theme`** — lot optionnel · acte MOA si hors tokens |
| Classes utilitaires Builder | Privilégier en V1 |

---

## 5. Matrice Website Builder vs module

| Bloc | Website Builder seul | Nécessite module / script |
|------|----------------------|---------------------------|
| Hero copy + image | ✅ | Script configure si arch homepage figée |
| Réassurance · catégories | ✅ | — |
| Vedettes sans placeholder | ⚠️ partiel (BO images) | ✅ SSR configure / hook content |
| Coffrets découverte | ⚠️ manuel | ✅ Recommandé : hook content idempotent |
| Dual Pro/newsletter | ✅ (2 col CMS) | ✅ Recommandé : réutiliser `build_dual_engage_compact_arch` |
| Éditorial bas | ✅ | ✅ Hook pour ordre blocs stable |
| Densité hero / dual | ⚠️ limité | SCSS thème si insuffisant |

**Module principal exécution** : `dorevia_ck_marketone_content` (composition homepage · données pilotes).  
**Module thème** : `dorevia_ck_theme` — **interventions minimales** · acte MOA par lot si SCSS/QWeb nouveau.

---

## 6. Recette responsive

| Viewport | Contrôles |
|----------|-----------|
| **1440** | Ordre blocs · densité · coffret horizontal · dual 2 col |
| **1280** | Idem · pas de régression header A1 |
| **390** | `scrollWidth = 390` · CTA visibles · empilement · pas placeholder |

**Scripts existants réutilisables** : `ck_phase3_mobile390.mjs` · `ck_phase3_desktop1280.mjs` · `ck_q1_ssr_verify.mjs` · gate `ck_phase9_ci.sh` (non-régression vedettes).

**Livrable recette** : `RECETTE_QA_RAPPROCHEMENT_HOME_MAQUETTE_V1.md` (à créer à l’exécution).

---

## 7. Critères de sortie globaux (GO MOA exécution)

| # | Critère |
|---|---------|
| 1 | Aucun placeholder image visible home publique |
| 2 | Aucun texte technique / commentaire dev visible |
| 3 | Liens fonctionnels : `/shop` · `/kits` · `/promotions` · `/professionnels` · `/contactus` |
| 4 | Blocs coffret · dual · éditorial visibles desktop + mobile |
| 5 | Aucun overflow mobile 390 |
| 6 | Tests HTTP Odoo verts (tags phase2/9 + smoke home) |
| 7 | Capture Odoo comparable maquette ±10–15 % espacements |
| 8 | Recette visuelle signée MOA |

---

## 8. Estimation d’impact (indicative)

| Lot | Effort Dev | Risque | Dépendances |
|-----|------------|--------|-------------|
| 0 Baseline | — | Faible | Phases 1–2 existantes |
| 1 Hero | S | Faible | Image BO · SCSS optionnel |
| 2 Vedettes | M | **Moyen** (données images) | Catalogue BO · script SSR |
| 3 Coffrets | M | Faible | Produit pack BO · Chantier B routes |
| 4 Dual | M | Faible | M9 mailing · `/professionnels` |
| 5 Éditorial | S | Faible | Pages Phases 6–8 |
| 6 Visuel | S–M | Faible | Tokens thème |

**Séquence recommandée** : 2 → 3 → 4 → 5 → 1 → 6 → recette globale.

*(Prioriser placeholders et blocs manquants avant polish CSS.)*

---

## 9. Gouvernance · prochaines étapes

| # | Étape | Responsable | Statut |
|---|-------|-------------|--------|
| 1 | Cadrage ticket (ce document) | MOA | ✅ **2026-06-14** |
| 2 | GO exécution Dev par lot | MOA | ☐ En attente |
| 3 | Composition homepage + données BO | Dev | ☐ |
| 4 | Recette responsive + captures | QA / MOA | ☐ |
| 5 | Verdict rapprochement home V1 | MOA | ☐ |
| 6 | Commit / PR | MOA | ☐ Acte dédié par lot ou lot groupé |

```text
Aucun développement · commit · PR sans acte MOA GO exécution explicite.
Header (A1) : ne pas rouvrir sauf écart confirmé et acté dans ce ticket.
```

---

## 10. Documents liés

| Document | Rôle |
|----------|------|
| [`brief_01_2.md`](./brief_01_2.md) | Structure cible V1.2 |
| [`TABLEAU_TRADUCTION_ODOO_V1_2.md`](./TABLEAU_TRADUCTION_ODOO_V1_2.md) | Mapping bloc → snippet |
| [`RECETTE_QA_PHASE2_HOME_SOBER_CK_V1.md`](./RECETTE_QA_PHASE2_HOME_SOBER_CK_V1.md) | Baseline Phase 2 · Q1 SSR |
| [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) | Doctrine phases · garde-fous |
| [`ticket_moa_composition_cms_ck_01`](../ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) | Capital CMS · pause home |
| [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) | Méthode traduction |
| [`RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md`](./RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md) | Écarts accueil §3 |

---

*Ticket Rapprochement Home Maquette V1 — cadrage MOA 2026-06-14 · sans exécution Dev.*
