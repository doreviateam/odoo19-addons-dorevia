# Décision MOA — GO reprise Odoo V1 · CK V1.2.x

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Statut** | **Chantier A : session A1 ouverte · verdict A1 en attente · Chantier B : navigateur clôturé MOA 2026-06-14 · A7 doc validée · GO A7 après A1** |
| **Date acte §5decies GO Phase 9** | **2026-06-14** |
| **Date clôture Phase 9 MOA** | **2026-06-14** |
| **Date clôture Phase 7 MOA** | **2026-06-14** |
| **Date clôture Phase 8 MOA** | **2026-06-14** |
| **Date dossier Phase 9** | **2026-06-14** |
| **Date acte §5nonies GO Phase 8** | **2026-06-14** |
| **Date clôture Phase 5 MOA** | **2026-06-13** |
| **Date acte §5sexies GO Phase 5** | **2026-06-13** |
| **Date clôture Phase 4 MOA** | **2026-06-13** |
| **Date acte §5quinquies GO Phase 4** | **2026-06-13** |
| **Date acte §5quater GO Phase 3** | **2026-06-13** |
| **Date clôture Phase 3 QA** | **2026-06-13** |
| **Date d’acte M1–M9** | 2026-06-13 |
| **Date acte H1** | 2026-06-13 |
| **Date acte §5 GO exécution Phase 1** | **2026-06-13** |
| **Date acte §5bis GO exécution Phase 2** | **2026-06-13** |
| **Date acte §5ter levée Q1 Phase 2** | **2026-06-13** |
| **Date ajustement M9** | 2026-06-13 |
| **Recette QA dictionnaire CE** | [`RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md`](./RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md) — **validée MOA** · M9 OK CE avec réserve |
| **Passe QA pré-Phase 1** | [`RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md`](./RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md) §0quater — **OK réserves classées · Codex 2026-06-13** |
| **Palier autorisé** | **Phase 10** — session A1 ouverte · pas de GO Dev header sans verdict A1 · A7 après A1 · **Chantier B : merge acté · recettes navigateur** |
| **Chaîne** | Phases 1–9 clôturées OK partiel MOA → **Phase 10 recette finale go-live** (suspendue · acte MOA distinct) |
| **Guide intégration** | [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) |
| **Maquette** | [`decision_moa_verdict_maquette_v1_2_x_vision_complete.md`](./decision_moa_verdict_maquette_v1_2_x_vision_complete.md) |
| **Arbitrage source** | [`ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md`](./ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md) |
| **Séquence préparation** | [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) |

```text
VERDICT MOA PHASE 1 : OK ACTÉ (2026-06-13)
GO EXÉCUTION §5BIS PHASE 2 : ACTÉ — HOME SOBRE
Q1 PHASE 2 : LEVÉE (2026-06-13) — réserve SSR actée §5ter
GO EXÉCUTION §5quater PHASE 3 : ACTÉ · CLÔTURÉE OK partiel maîtrisé (gate portable OK)
PHASE 4 : CLÔTURÉE OK partiel MOA (2026-06-13) · gate portable OK
PHASE 5 : CLÔTURÉE OK partiel MOA (2026-06-13) · gate portable OK
PHASE 6 : CLÔTURÉE OK MOA (2026-06-13) · gate portable OK
PHASE 7 : CLÔTURÉE OK partiel MOA (2026-06-14)
PHASE 8 : CLÔTURÉE OK partiel MOA (2026-06-14) · gate portable OK
PHASE 9 : CLÔTURÉE OK partiel MOA · gate portable OK · 2026-06-14
PHASE 10+ : SUSPENDUES
```

> Règle MOA : **maquette validée ≠ reprise intégrale HTML**. Reprise Odoo = traduction **bloc par bloc · par paliers · avec recette MOA/QA à chaque phase**.

> Orientation MOA (2026-06-13) : la maquette V1.2.x constitue une **V1 mature de référence** — suffisante pour lancer l’intégration Odoo contrôlée, sans prétendre à l’exhaustivité de la vision CK future.

---

## 0. Rappel — ce qui est déjà acté

| Étape | Verdict | Document |
|-------|---------|----------|
| Maquette V1.2.x · 9 pages | **OK** | [`decision_moa_verdict_maquette_v1_2_x_vision_complete.md`](./decision_moa_verdict_maquette_v1_2_x_vision_complete.md) |
| Arbitrage V1 traduisible | **OK QA MOA** | [`ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md`](./ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md) |
| Décisions M1–M9 | **Actées** | Ce document §1 |
| Décision H1 header & mega-menu | **Actée** | Ce document §1bis · [`note_reference_header_mega_menu_decouverte_ck_v1.md`](./note_reference_header_mega_menu_decouverte_ck_v1.md) |
| GO préparation reprise Odoo V1 | **Acté** (M8) | Ce document · [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) |
| Recette QA dictionnaire CE | **Validée MOA** | [`RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md`](./RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md) · M9 §0bis |
| Passe QA pré-Phase 1 (H1) | **OK réserves classées** | [`RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md`](./RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md) §0quater · Codex 2026-06-13 |
| GO exécution Odoo V1 | **Acté** | §5 · **2026-06-13** · Phase 1 uniquement — Header + footer BO |
| Recette QA Phase 1 | **OK QA · acté MOA** | [`RECETTE_QA_PHASE1_HEADER_FOOTER_CK_V1.md`](./RECETTE_QA_PHASE1_HEADER_FOOTER_CK_V1.md) §6.0 |
| Verdict MOA final Phase 1 | **OK acté** | 2026-06-13 · prérequis §5bis |
| GO Phase 2 (Home sobre) | **Acté · OK partiel QA** | §5bis · [`RECETTE_QA_PHASE2_HOME_SOBER_CK_V1.md`](./RECETTE_QA_PHASE2_HOME_SOBER_CK_V1.md) §6.0 |
| **Q1 Phase 2 — Produits vedettes** | **✅ Levée · réserve SSR actée** | §5ter · **2026-06-13** · recette §6septies |
| GO Phase 3 (Shop) | **✅ Clôturée OK partiel maîtrisé** | **2026-06-13** · gate [`ck_phase3_ci.sh`](./scripts/ck_phase3_ci.sh) · [`RECETTE_QA_PHASE3_SHOP_CK_V1.md`](./RECETTE_QA_PHASE3_SHOP_CK_V1.md) |
| GO Phase 4 (Fiche produit) | **✅ Clôturée OK partiel MOA** | **2026-06-13** · [`RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md`](./RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md) |
| GO Phase 5 (Pro + CRM) | **✅ Clôturée OK partiel MOA** | **2026-06-13** · [`RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md`](./RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md) |
| Préparation Phase 6 (Contact + À propos) | **✅ §5septies acté** | **2026-06-13** |
| Exécution Phase 6 Dev | **✅ Livrée** | **2026-06-13** · `19.0.1.4.0` · gate OK |
| Recette MOA/QA Phase 6 | **✅ Clôturée OK MOA** | **2026-06-13** · [`RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md`](./RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md) |
| Préparation Phase 7 (Fiche producteur M1) | **✅ §5octies acté** | **2026-06-13** |
| Exécution Phase 7 Dev | **✅ Livrée** | **19.0.1.6.0** · `_wrap_website_page_arch` · gate renforcé |
| Recette MOA/QA Phase 7 | **✅ Clôturée OK partiel MOA** | **2026-06-14** · [`RECETTE_QA_PHASE7_FICHE_PRODUCTEUR_CK_V1.md`](./RECETTE_QA_PHASE7_FICHE_PRODUCTEUR_CK_V1.md) |
| Préparation Phase 8 (Recettes M2) | **✅ §5nonies dossier préparé · QA documentaire OK** | **2026-06-14** |
| Acte §5nonies GO Phase 8 | **✅ Acté MOA** | **2026-06-14** · Recettes statiques / Savoirs · M2 |
| Exécution Phase 8 Dev | **✅ Livrée** | **19.0.1.7.0** · `/recettes` · `bootstrap_recipes_page()` · gate OK |
| Recette MOA/QA Phase 8 | **✅ Clôturée OK partiel MOA** | **2026-06-14** · [`RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md`](./RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md) |
| Préparation Phase 9 (Newsletter M9) | **✅ §5decies dossier préparé · QA documentaire OK** | **2026-06-14** |
| Acte §5decies GO Phase 9 | **✅ Acté MOA** | **2026-06-14** · Newsletter M9 simple |
| Exécution Phase 9 Dev | **✅ Livrée** | **19.0.1.8.0** · dual compact contact/pro · gate OK |
| Recette MOA/QA Phase 9 | **✅ Clôturée OK partiel MOA** | **2026-06-14** · [`RECETTE_QA_PHASE9_NEWSLETTER_CK_V1.md`](./RECETTE_QA_PHASE9_NEWSLETTER_CK_V1.md) |
| **Réserve architecture module** | **Levée · QA isolation OK acté** | **2026-06-14** · split §4bis · `19.0.1.10.0` |

---

## 1. Décisions MOA M1–M9 — actées

| # | Point | Décision MOA actée | Date | Garde-fou / commentaire |
|---|-------|-------------------|------|-------------------------|
| **M1** | Fiche producteur V1 | **Option A — CMS pilote** | 2026-06-13 | Présentation · origine · savoir-faire · critères CK · visuels · produits associés · CTA. Pas annuaire · pas portail · pas espace connecté. |
| **M2** | Page recettes V1 | **CMS statique** | 2026-06-13 | Recettes / savoirs / usages simples. Pas blog complexe · pas contribution utilisateur V1. |
| **M3** | Filtres shop V1 | **Différer filtres avancés** | 2026-06-13 | V1 = catégories · attributs simples · tri natif · navigation standard. Pas AJAX · pas search custom · pas catalogue parallèle. |
| **M4** | Catégories home ×3 | **Intégrer si catégories BO prêtes, sinon différer** | 2026-06-13 | Liens uniquement vers catégories Odoo propres. |
| **M5** | Promesses réassurance | **Copy opérationnelle à valider avant go-live** | 2026-06-13 | Sobres · fiables · tenables. Reformuler toute promesse trop forte. |
| **M6** | Périmètre V1 Odoo | **V1 prioritaire complète maîtrisée, bloc par bloc** | 2026-06-13 | Ni home seule · ni reprise intégrale prototype. Voir §2. |
| **M7** | Méthode traduction | **Bloc par bloc** | 2026-06-13 | Pas big bang · pas collage HTML · pas reprise intégrale prototype. |
| **M8** | GO reprise Odoo | **GO préparation acté · GO exécution §5 distinct** | 2026-06-13 | Préparation doc / tickets / séquence autorisée. Exécution après §5 « Acté ». |
| **M9** | Newsletter · bloc dual | **Colonne Pro V1 prioritaire · newsletter V1 possible avec réserve** | 2026-06-13 | **Ajusté MOA 2026-06-13** : OK CE avec réserve (`mass_mailing` · `website_mass_mailing`). Newsletter **non bloquante Phase 1** · **non obligatoire** si intégration lourde. Pas automation marketing avancée · pas promo excessive. Réserves : RGPD · mailing list · `data-list-id` · snippet natif vs `s_ck_dual_engage` · reCAPTCHA · ton CK. |

---

## 1bis. Décision MOA H1 — header & mega-menu · actée

| Champ | Valeur |
|-------|--------|
| **Date acte** | 2026-06-13 |
| **Compatible Phase 1** | Oui — **GO exécution §5 acté 2026-06-13** |
| **Note détaillée** | [`note_reference_header_mega_menu_decouverte_ck_v1.md`](./note_reference_header_mega_menu_decouverte_ck_v1.md) |

### Header V1 cible

```text
Boutique · Découvrir · Producteurs · Professionnels
```

| Entrée | Décision MOA actée |
|--------|-------------------|
| **Découvrir** | Libellé retenu (pas « Univers ») · **mega-menu natif Odoo CE** |
| Mega-menu — Acheter par univers | Épicerie créole · Manioc & dérivés · Incontournables CK · Packs & découvertes · Nouveautés — **liens BO réels uniquement (M4)** |
| Mega-menu — Explorer par origine | Guadeloupe · Martinique · Réunion — **si données BO prêtes** · sinon différer |
| Mega-menu — Comprendre et cuisiner | Recettes & savoirs · Conseils d’usage · Découvrir les produits créoles |
| **Producteurs** | Lien simple **ou** dropdown léger · **pas de mega-menu lourd V1** · pas annuaire · renvoi fiche pilote ou page CMS |
| **Professionnels** | **Lien direct** `/professionnels` · pas de friction · priorité qualification B2B |

### Garde-fous H1

```text
Mega-menu natif CE uniquement · configuration BO first
Adaptation CSS CK légère seulement si nécessaire
Pas de mega-menu custom JS · pas de navigation mobile complexe
Recette mobile 390 px obligatoire · pas de liens fictifs
```

**Motif libellé Découvrir** : plus clair client · logique découverte produit · moins abstrait qu’« Univers » · meilleur remplacement de « Catégories ».

---

## 2. Périmètre V1 Odoo acté (M6)

| Domaine | Inclus V1 | Exclu V1 |
|---------|-----------|----------|
| **Transversal** | ☑ Header **H1** : Boutique · Découvrir (mega CE) · Producteurs (léger) · Pro direct · footer (configuration BO) | ☐ Surcouche autonome · mega-menu Producteurs · mega custom JS |
| **Home** | ☑ Hero · réassurance · produits vedettes · signal Pro · bloc dual (Pro prioritaire) | ☐ Éditorial long · coffret si produit absent |
| **Home — conditionnel M4** | ☑ Catégories ×3 **si BO prêtes** | ☐ Catégories fictives |
| **Commerce** | ☑ Shop natif · catégorie principale · fiche achat · contenu enrichi simple · attributs origine | ☐ Filtres avancés (M3) · cross-sell · associations |
| **B2B** | ☑ `/professionnels` · CRM natif (consolidation) | ☐ Portail · pricing pro public |
| **Confiance** | ☑ `/a-propos` simple · `/contactus` | ☐ |
| **Producteur M1** | ☑ 1 fiche CMS pilote · produits associés · bloc mini fiche produit | ☐ Annuaire · portail · fournisseur Odoo natif V1 |
| **Éditorial M2** | ☑ Page recettes statique | ☐ Blog · forum · communauté |
| **Relation continue M9** | ☑ Colonne Pro bloc dual **prioritaire** · newsletter **V1 possible avec réserve** | ☐ Newsletter obligatoire V1 · automation · campagnes avancées |

**Stack** : Odoo 19 CE · Website Builder · snippets first · `dorevia_ck_theme`.

---

## 3. Ordre d’exécution Odoo — par paliers (post GO §5)

Séquence détaillée :

[`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md)

Dictionnaire Maquette ↔ Odoo :

[`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md)

Vérification CE instance :

[`RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md`](./RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md)

**Principe GO par palier** :

```text
Pas de big bang · pas de reprise intégrale HTML
Pas de modification visible massive sans recette
Chaque phase : livrée · documentée · recettée MOA/QA · puis GO palier suivant
```

Résumé :

```text
Phase 0 — Capital conservé (déjà en instance)
Phase 1 — Header + footer BO                    ← **OK QA** (revalidation 2026-06-13)
Phase 2 — Home sobre                            ← **OK partiel QA** (2026-06-13)
Phase 3 — Shop + catégorie principale BO        ← **CLÔTURÉE OK partiel maîtrisé · gate portable OK**
Phase 4 — Fiche produit (achat + enrichissement simple)   ← **Clôturée OK partiel MOA · 2026-06-13**
Phase 5 — Pro + CRM (consolidation)   ← **Clôturée OK partiel MOA · 2026-06-13**
Phase 6 — Contact + À propos   ← **Clôturée OK MOA ✅**
Phase 7 — Fiche producteur CMS pilote (M1)   ← **Clôturée OK partiel MOA · 2026-06-14**
Phase 8 — Recettes statiques (M2)   ← **Clôturée OK partiel MOA · 2026-06-14**
Phase 9 — Newsletter M9 simple   ← **Clôturée OK partiel MOA · 2026-06-14**
Phase 10 — Recette globale go-live   ← **Préparation · pas nouvelle feature · focus header/menu**
```

Ticket référence : [`ticket_moa_composition_cms_ck_01`](../ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md)

Recette post-traduction : [`recette_qa_composition_cms_ck_01.md`](../recette_qa_composition_cms_ck_01.md)

---

## 4. Garde-fous maintenus

```text
Odoo 19 CE · Website Builder · snippets first · dorevia_ck_theme
Pas de surcouche autonome · pas de catalogue parallèle
Pas de panier/checkout custom · pas de logique B2B custom V1
Pas d’annuaire producteurs · pas de portail · pas de blog complexe
Pas de reprise intégrale du prototype HTML
Réserve architecture §4bis : split thème / contenu — dorevia_ck_theme générique + dorevia_ck_marketone_content optionnel
```

Capital Odoo conservé : `/professionnels` · menu Pro · header · routes sécurisées.

---

## 4bis. Architecture — généricité `dorevia_ck_theme` · **SPLIT ACTÉ · QA OK · 2026-06-14**

### Constat initial (2026-06-14)

Le module `dorevia_ck_theme` n’était **pas** verrouillé sur le nom de base `dorevia_ck_marketone_01`, mais **fortement couplé** au contenu CK Marketone via `hooks.py` et les migrations `19.0.1.x`.

### Découplage livré

| Module | Version | Rôle |
|--------|---------|------|
| **`dorevia_ck_theme`** | `19.0.1.10.0` | Thème **CK générique** : tokens · SCSS · snippets · layout · héritages `website_sale` · `post_init_hook` = maintenance technique uniquement |
| **`dorevia_ck_marketone_content`** | `19.0.1.0.0` | Contenu CK **optionnel** : pages CMS · producteur · recettes · enrichissements catalogue · mailing list · bootstraps métier |

```text
Instance CK Marketone : installer les deux modules
Autre base : dorevia_ck_theme seul — aucun seed contenu CK si content non installé
```

**Garde-fous isolation** (`19.0.1.10.0`) :

```text
post_init_hook thème : maintenance technique uniquement (pas de pages · produits · catégories · newsletter)
Manifest thème : plus de dépendance website_crm · mass_mailing · website_mass_mailing
Migrations thème 19.0.1.1.0 → 19.0.1.8.0 : bootstraps uniquement si dorevia_ck_marketone_content state=installed en base
Helper is_marketone_content_installed(env) — pas de test ImportError seul
Si content non installé : migrations thème sortent sans injecter de contenu
```

**Réserve marque blanche** (non bloquante · V1) : snippets thème conservent des libellés CK (« Boutique C-Kreyol », « Espace professionnel CK », « C-Kreyol Marketone », etc.) — **thème CK**, pas marque blanche multi-marque.

**Réserve architecture secondaire** (non bloquante · post-V1) : si `dorevia_ck_marketone_content` **est** installé, les migrations historiques du thème peuvent encore déclencher des bootstraps contenu (compatibilité CK). Pour une séparation ultra-propre, les bootstraps contenu devraient vivre **uniquement** dans les migrations du module contenu.

### Verdict MOA · **ACTÉ · 2026-06-14**

```text
OK QA split thème / contenu.
dorevia_ck_theme est désormais déployable seul sans seed métier CK,
sous réserve que dorevia_ck_marketone_content ne soit pas installé.
Réserve conservée : thème CK, non marque blanche ; snippets encore éditorialisés CK.
```

| Nature | Verdict |
|--------|---------|
| QA isolation « thème seul » | ✅ **OK acté · 2026-06-14** |
| Instance cible CK Marketone | ✅ **Les deux modules** |
| Réutilisation thème seul (content non installé) | ✅ **Sans injection contenu CK** |
| Marque blanche / textes snippets neutres | ⚠️ **Hors périmètre V1** |
| Cycles thème/contenu totalement indépendants | ⚠️ **Réserve post-V1** (migrations historiques thème) |
| Blocant Phase 9 / clôture V1 instance | **Non** |

---

## 5. Verdict GO Odoo

| Champ | Valeur |
|-------|--------|
| **GO préparation reprise Odoo V1** | ☑ **Acté** (M8 · 2026-06-13) |
| **Recette QA CE** | ☑ **Validée MOA** · [`RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md`](./RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md) · M9 **OK CE avec réserve** §0bis |
| **Passe QA pré-Phase 1** | ☑ **OK réserves classées** · Codex 2026-06-13 · §0quater |
| **Recette QA Phase 1** | ☑ **OK QA · acté MOA** · revalidation 2026-06-13 · [`RECETTE_QA_PHASE1_HEADER_FOOTER_CK_V1.md`](./RECETTE_QA_PHASE1_HEADER_FOOTER_CK_V1.md) §6.0 |
| **Verdict MOA final Phase 1** | ☑ **OK acté** · 2026-06-13 |
| **GO exécution Odoo V1 — Phase 1** | ☑ **Acté · clôturé OK QA** |
| **Recette QA Phase 2** | ☑ **OK partiel** · 2026-06-13 · [`RECETTE_QA_PHASE2_HOME_SOBER_CK_V1.md`](./RECETTE_QA_PHASE2_HOME_SOBER_CK_V1.md) §6.0 · doc §6septies **opposable** |
| **GO exécution Odoo V1 — Phase 2** | ☑ **Acté · clôturé OK partiel QA** |
| **Q1 Phase 2 — Produits vedettes** | ☑ **Levée · réserve SSR actée** · **2026-06-13** · §5ter |
| **Phase 3** | ☑ **GO acté §5quater** · **2026-06-13** · Dev autorisé |
| **Palier autorisé** | **Phase 3** — Shop + catégorie principale BO |
| **Date GO exécution Phase 1** | **2026-06-13** |
| **Date GO exécution Phase 2** | **2026-06-13** |
| **Validé par** | MOA CK |

### Acte MOA — GO exécution §5 (2026-06-13)

```text
GO EXÉCUTION ODOO V1 — CK V1.2.x
Périmètre autorisé : Phase 1 uniquement — Header + footer BO
```

**Conditions d’exécution Phase 1** *(réserves QA · strictes)* :

```text
Mega-menu natif CE uniquement
Mega initial minimal : Épicerie créole + Packs & découvertes — URL BO réelles à confirmer
Masquer colonne Origines tant que attributs / données BO non prêts
Exclure /recettes et /a-propos du mega tant que pages non créées
Producteurs : lien simple seulement si cible CMS réelle existe
Pas de liens fictifs
Pas de mega-menu custom JS
Pas de reprise intégrale HTML
Pas de démarrage Phase 2 sans recette Phase 1
```

**Recette obligatoire après livraison Phase 1** :

| Contrôle | Attendu |
|----------|---------|
| Desktop | Navigation · rendu header/footer |
| Mobile **390 px** | Accordéon mega · pas d’overflow |
| Header | Boutique · Découvrir (mega) · Producteurs · Professionnels |
| Footer | 4 col · liens BO valides |
| Liens BO | Pas de 404 · pas de liens fictifs |
| Non-régression | `/shop` · `/professionnels` · panier |
| Verdict | **MOA/QA explicite** avant tout passage Phase 2 |

Matrice liens mega-menu Phase 1 : [`note_reference_header_mega_menu_decouverte_ck_v1.md`](./note_reference_header_mega_menu_decouverte_ck_v1.md) §2bis · recette §0quater.

### Historique prérequis §5

**Verdict passe QA pré-Phase 1 — Codex (2026-06-13)** :

```text
OK avec réserves classées — aucun bloquant technique nouveau pour Phase 1 limitée
Cohérence documentaire H1 : OK · contre-vérification mega-menu CE : OK
```

**Verdict recette QA CE — validé MOA (2026-06-13)** :

```text
OK avec réserves classées — dictionnaire CE suffisamment vérifié pour GO Phase 1 limité
Aucun bloquant technique identifié pour Phase 1 (header + footer BO)
M9 Newsletter : OK CE avec réserve — V1 possible · non bloquante Phase 1 · non obligatoire si lourd
```

---

## 5bis. Acte MOA — GO exécution Phase 2 (2026-06-13)

| Champ | Valeur |
|-------|--------|
| **Prérequis** | Phase 1 OK QA · [`RECETTE_QA_PHASE1_HEADER_FOOTER_CK_V1.md`](./RECETTE_QA_PHASE1_HEADER_FOOTER_CK_V1.md) §6.0 |
| **Verdict MOA Phase 1** | ☑ **OK acté** · 2026-06-13 |
| **GO exécution Phase 2** | ☑ **Acté** · ☐ Reporté |
| **Périmètre autorisé** | **Phase 2 uniquement** — Home sobre (`/`) |
| **Phases 3–10** | Suspendues |
| **Validé par** | MOA CK |

### Acte MOA — GO exécution §5bis (2026-06-13)

```text
GO EXÉCUTION ODOO V1 — CK V1.2.x
Périmètre autorisé : Phase 2 uniquement — Home sobre
Prérequis : Phase 1 OK QA · verdict MOA Phase 1 acté
```

**Périmètre Phase 2 — blocs autorisés** *(§2 · M6 · [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md))* :

| # | Bloc | Snippet / composant | Gate MOA |
|---|------|---------------------|----------|
| 2.1 | Hero | `s_ck_hero` | Copy CK · CTA `/shop` · signal Pro discret |
| 2.2 | Réassurance | `s_ck_reassurance` | **M5** — copy opérationnelle · promesses tenables |
| 2.3 | Produits vedettes — **5 CK réels en V1, cible 6 différée** | Grille SSR `.ck-featured-products__grid--stable` · `s_ck_featured_products` | 5 produits BO · prix TTC · **V1 = SSR, non Dynamic Products / carousel** |
| 2.4 | Catégories ×3 | `s_ck_category_links` | **M4 conditionnel** — uniquement si catégories BO prêtes · pas de liens fictifs |
| 2.5 | Bloc dual Pro / newsletter | `s_ck_dual_engage` ou Pro seul + subscribe natif | **M9** — colonne Pro **prioritaire** · newsletter **optionnelle** si simple · sinon différer |
| 2.6 | Bandeau Pro (signal B2B) | `s_ck_pro_banner` | Lien `/professionnels` · qualification sans friction |

**Exclus Phase 2** :

```text
Éditorial bas de page long · coffret / packs si produit absent
Modification header / footer / mega-menu (Phase 1 gelée)
Reprise intégrale prototype HTML · surcouche autonome
Phase 3+ sans recette MOA/QA Phase 2
```

**Conditions d’exécution Phase 2** *(strictes)* :

```text
Snippets CK existants first · Website Builder · dorevia_ck_theme
Vedettes V1 : grille SSR stable (§6quater–§6sexies RECETTE) — Dynamic Products / carousel INTERDIT sans recette dédiée
Pas de modification dorevia_ck_theme sans ticket dédié
Non-régression Phase 1 : header · footer · mega · routes · mobile 390 px
Pas de démarrage Phase 3 sans recette MOA/QA Phase 2 explicite + acceptation réserve SSR (§6septies)
Ordre mobile cible : hero → réassurance → produits → catégories (si M4) → dual Pro → footer
```

**Recette obligatoire après livraison Phase 2** :

| Contrôle | Attendu |
|----------|---------|
| Desktop `/` | Hero · réassurance · vedettes · blocs Pro visibles |
| Mobile **390 px** | Ordre blocs · pas d’overflow · CTA touch |
| Produits vedettes | **5 produits CK réels** · grille SSR stable · prix · liens fiche valides · cible 6 différée |
| Catégories ×3 | Présentes **si M4** · liens catégories 200 · absentes si BO non prêt |
| Signal Pro | Bandeau et/ou dual Pro · lien `/professionnels` 200 |
| Copy réassurance | **M5** — promesses sobres · pas de sur-promesse |
| Non-régression Phase 1 | Header 3 entrées · mega Épicerie · footer 4 col · pas Q1/Q2 |
| Verdict | **MOA/QA explicite** avant tout passage Phase 3 |

Ticket référence : [`ticket_moa_composition_cms_ck_01`](../ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md)

Recette post-traduction : [`recette_qa_composition_cms_ck_01.md`](../recette_qa_composition_cms_ck_01.md)

**Réserves classées maintenues** *(non bloquantes Phase 2 si déjà actées)* :

| # | Point | Statut |
|---|-------|--------|
| R1 | Producteurs absent nav | Gate CMS Phase 7 |
| R2 | Packs absent mega | 0 produit BO · URL 404 |
| R3 | Footer Découvrir = Contact seul | Phases 6–8 |
| R4 | Pas de mentions légales footer | Copy M5 |
| O1 | Démo Odoo corps `/contactus` | Phase 6 contact |

---

## 5ter. Acte MOA — Levée Q1 Phase 2 · Produits vedettes · réserve SSR

| Champ | Valeur |
|-------|--------|
| **Prérequis Dev** | Corrections §6bis → §6sexies · doc §6septies opposable · instance `dorevia_ck_marketone_01` |
| **Recette** | [`RECETTE_QA_PHASE2_HOME_SOBER_CK_V1.md`](./RECETTE_QA_PHASE2_HOME_SOBER_CK_V1.md) §6septies · §6quinquies (historique anomalie) |
| **Sélecteur recette** | `.ck-featured-products__grid--stable` |
| **Périmètre V1** | **5 produits CK réels** · cible 6 différée · grille SSR stable · **non carousel / non Dynamic Products** |
| **Verdict doc QA** | ☑ **OK opposable** |
| **Levée Q1** | ☑ **Actée** · **2026-06-13** |
| **Date recontrôle MOA** | **2026-06-13** |
| **Validé par** | **MOA CK** |

### Acte MOA signé — Q1 Phase 2 (2026-06-13)

Q1 est levée sur la home V1 actuelle, sous réserve acceptée :

**Le bloc Produits vedettes est validé en grille SSR stable, avec 5 produits CK réels.**

La MOA accepte que la V1 ne repose pas sur le carousel / Dynamic Products produits pour cette zone.

#### Réserve actée

- La cible 6 produits est différée.
- Le carousel / Dynamic Products produits reste exclu de la V1.
- Toute réintroduction d’un carousel ou Dynamic Products produits devra faire l’objet d’un ticket et d’une recette dédiée.

#### Conditions constatées

Validation sous réserve que le rendu desktop et mobile 390 px reste conforme :

- 5 cartes produits CK visibles ;
- titres et prix lisibles ;
- liens fiches produits valides ;
- pas de tremblement / layout shift ;
- pas d’overflow horizontal ;
- non-régression Phase 1 : header, mega-menu, footer.

#### Conséquence

```text
Q1 Phase 2 : LEVÉE (réserve SSR actée)
Phase 3 : OK partiel QA confirmé MOA · 2026-06-13
Dev Phase 4 : INTERDIT sans acte MOA explicite §5quinquies (ou équivalent)
```

### Recontrôle MOA — checklist (desktop 1280 px + mobile 390 px)

| # | Critère | Desktop | Mobile 390 |
|---|---------|:-------:|:----------:|
| R1 | Bloc `.ck-featured-products__grid--stable` présent | ☑ | ☑ |
| R2 | **5 cartes** produits CK réels visibles | ☑ | ☑ |
| R3 | Prix · titres lisibles · liens fiche `/shop/…` 200 | ☑ | ☑ |
| R4 | Aucun tremblement / layout shift au scroll (L1 §6quinquies) | ☑ | ☑ |
| R5 | Pas d’overflow horizontal | ☑ | ☑ |
| R6 | Non-régression Phase 1 (header · mega · footer) | ☑ | ☑ |

**Accès recette** : sélecteur DB → `dorevia_ck_marketone_01` → `/`  
*(éviter seul `/?db=…` sans session — risque redirect login)*

### Réserve technique acceptée par la MOA

```text
La stabilisation du bloc Produits vedettes repose sur une grille SSR (remplacement),
et non sur une correction du carousel / Dynamic Products Odoo natif.

Toute réintroduction d’un carousel ou dynamic snippet produits en V1 est interdite
sans ticket et recette dédiée.
```

| Point | Acceptation MOA |
|-------|-----------------|
| Grille SSR = traduction V1 acceptable (non carousel) | ☑ **Oui** |
| Carousel / Dynamic Products vedettes exclus V1 | ☑ **Acté** |

### Texte d’acte archivé (identique au signé)

```text
Q1 levée sur la home V1 actuelle, sous réserve acceptée :
le bloc Produits vedettes est validé en grille SSR stable, avec 5 produits CK réels.
Le carousel / Dynamic Products produits reste exclu de la V1 sans ticket et recette dédiée.
```

| Champ | Valeur |
|-------|--------|
| **Date acte levée Q1** | **2026-06-13** *(alignée chaîne documentaire §5 / §5bis)* |
| **Signataire MOA** | **MOA CK** |

---

## 5quater. Acte MOA — GO exécution Phase 3 (Shop) · **ACTÉ 2026-06-13**

| Champ | Valeur |
|-------|--------|
| **Prérequis** | ☑ Q1 levée §5ter · réserve SSR acceptée · recette Phase 2 OK partiel actée |
| **Décision MOA** | ☑ **Acté** |
| **GO exécution Phase 3** | ☑ **Acté** · **2026-06-13** |
| **Périmètre autorisé** | **Phase 3 uniquement** — Shop + catégorie principale BO |
| **Phases 4–10** | Suspendues |
| **Recette obligatoire** | [`RECETTE_QA_PHASE3_SHOP_CK_V1.md`](./RECETTE_QA_PHASE3_SHOP_CK_V1.md) |
| **Validé par** | **MOA CK** |
| **Date acte** | **2026-06-13** |

> **Dev Phase 3 : AUTORISÉ** (périmètre §5quater strict) · **Phase 4 : INTERDIT** sans recette MOA/QA Phase 3.

### Périmètre strict Phase 3

```text
Phase 3 uniquement — Shop + catégorie principale BO
```

| # | Livrable | Composant / route |
|---|----------|-------------------|
| 3.1 | Boutique `/shop` | `website_sale` natif · thème CK |
| 3.2 | Catégorie principale BO | `product.public.category` · ex. `/shop/category/epicerie-creole-1` |
| 3.3 | Grille produits · prix · liens fiches | Grille native Odoo |
| 3.4 | Tri natif | Si présent dans CE — pas de custom |

**Exclus Phase 3** :

```text
Filtres avancés (M3) · recherche custom · AJAX · catalogue parallèle
Modification checkout / panier · Phase 4+
Modification home Phase 2 (sauf non-régression)
Modification header / footer Phase 1
```

### Garde-fous Phase 3

```text
Shop natif Odoo / website_sale uniquement
Catégorie principale BO uniquement — liens réels · pas de liens fictifs
Pas de filtres avancés · pas de recherche custom · pas d’AJAX
Pas de catalogue parallèle
Pas de modification checkout / panier
Pas de modification home Phase 2 sauf correction de non-régression
Pas de modification header / footer Phase 1
Home : grille SSR vedettes §5ter conservée — carousel / Dynamic Products interdits
Pas de Phase 4 sans recette MOA/QA Phase 3 explicite
```

### Recette obligatoire Phase 3

Document : [`RECETTE_QA_PHASE3_SHOP_CK_V1.md`](./RECETTE_QA_PHASE3_SHOP_CK_V1.md)

| Contrôle | Attendu |
|----------|---------|
| `/shop` desktop | Grille · prix · liens fiches 200 |
| `/shop` mobile **390 px** | Pas d’overflow · CTA touch |
| Catégorie principale | Page 200 · produits listés · breadcrumb natif |
| Tri natif | Si présent — comportement CE standard |
| Liens | Aucun lien fictif · catégories BO réelles |
| Non-régression Phase 1 | Header · mega · footer |
| Non-régression Phase 2 | Home · vedettes SSR `.ck-featured-products__grid--stable` · bloc Pro |
| Verdict | **MOA/QA explicite** avant tout passage Phase 4 |

### Acte MOA signé — GO exécution §5quater (2026-06-13)

```text
GO EXÉCUTION ODOO V1 — CK V1.2.x
Périmètre autorisé : Phase 3 uniquement — Shop + catégorie principale BO
Prérequis : Q1 levée §5ter (2026-06-13) · réserve SSR vedettes actée · Phase 2 OK partiel QA acté
Garde-fous : shop natif website_sale · pas filtres avancés · pas AJAX · pas checkout custom
Pas de modification home Phase 2 · vedettes SSR §5ter conservées
Phases 4–10 : suspendues jusqu’à recette MOA/QA Phase 3
```

**Garde-fous home vedettes (maintenus)** :

```text
La home conserve la grille SSR stable .ck-featured-products__grid--stable — 5 produits CK réels
Carousel / Dynamic Products vedettes : exclus V1 sauf ticket + recette dédiée
```

| Champ | Valeur |
|-------|--------|
| **Date acte GO Phase 3** | **2026-06-13** |
| **Signataire MOA** | **MOA CK** |

**Conséquences actées** :

```text
Dev Phase 3 : AUTORISÉ (périmètre §5quater strict)
Phase 4 : INTERDIT sans recette MOA/QA Phase 3
```

### Exécution Dev Phase 3 · **2026-06-13**

| Élément | Détail |
|---------|--------|
| **Script** | [`scripts/ck_phase3_configure.py`](./scripts/ck_phase3_configure.py) · **module `dorevia_ck_theme` 19.0.1.1.0** |
| **Composition** | `s_ck_shop_intro` · `s_ck_reassurance_m5` · signal Pro · catégorie Épicerie créole BO |
| **View inherit** | `dorevia_ck_theme.products_ck_shop_compose` · `website_sale.products` |
| **Déploiement autre base** | `odoo -d MA_BASE -u dorevia_ck_theme --stop-after-init` |
| **QA automatisée** | `ck_phase3_desktop1280.mjs` · `ck_phase3_mobile390.mjs` |
| **Recette** | [`RECETTE_QA_PHASE3_SHOP_CK_V1.md`](./RECETTE_QA_PHASE3_SHOP_CK_V1.md) — **OK partiel confirmé MOA** |

### Verdict QA Phase 3 · **OK partiel maîtrisé — clôturé · 2026-06-13**

| Champ | Valeur |
|-------|--------|
| **Verdict** | **OK partiel maîtrisé** — clôturé QA |
| **Signataire** | **MOA CK** |
| **Gate portable** | [`scripts/ck_phase3_ci.sh`](./scripts/ck_phase3_ci.sh) · 14/14 tests · smoke curl OK |
| **Phase 6** | **✅ Clôturée OK MOA** |

```text
Instance conforme périmètre §5quater : shop natif + catégorie BO · home SSR / header-footer intacts
Gate M4 : Artisanat / Packs non exposés (404)
Contrat portable : dorevia_ck_theme 19.0.1.1.0 · ck_phase3_ci.sh
Playwright : recette UX hors gate · GitHub Actions différé
```

### Doctrine QA Phase 4+

```text
Triptyque obligatoire : (1) contrat Odoo portable · (2) smoke curl minimal · (3) Playwright séparé si UX
```

---

## 5quinquies. Acte MOA — GO exécution Phase 4 (Fiche produit) · **ACTÉ 2026-06-13**

| Champ | Valeur |
|-------|--------|
| **Prérequis** | ☑ Phase 3 clôturée OK partiel maîtrisé · gate portable OK · recette Phase 3 actée |
| **Décision MOA** | ☑ **Acté** |
| **GO exécution Phase 4** | ☑ **Acté** · **2026-06-13** |
| **Périmètre autorisé** | **Phase 4 uniquement** — Fiche produit native `website_sale` |
| **Phases 5–10** | Suspendues |
| **Recette obligatoire** | [`RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md`](./RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md) |
| **Validé par** | **MOA CK** |
| **Date acte** | **2026-06-13** |

> **Phase 4 : CLÔTURÉE OK partiel MOA** · **Phase 5 : INTERDIT** sans acte MOA explicite.

### Périmètre strict Phase 4

```text
Phase 4 uniquement — Fiche produit native Odoo / website_sale
```

| # | Livrable | Composant / route |
|---|----------|-------------------|
| 4.1 | Fiche produit | `/shop/{slug}-{id}` · template `website_sale.product` |
| 4.2 | Galerie / image | Galerie native CE |
| 4.3 | Titre · prix · qty · panier | Bloc achat natif · lien panier |
| 4.4 | Description enrichie simple | `website_description` · onglets CE |
| 4.5 | Origine · usage · conservation | Champs BO si disponibles |
| 4.6 | Signal B2B léger | Lien `/professionnels` |
| 4.7 | Lien producteur mini | **Conditionnel M1** — uniquement si cible CMS réelle |

**Exclus Phase 4** :

```text
Refonte panier / checkout
Cross-sell avancé · carousel produits associés · recette inline
Logique produit custom lourde
Modification home Phase 2 · shop Phase 3 · header/footer Phase 1
Phase 5+ sans recette MOA/QA Phase 4 explicite
```

### Garde-fous Phase 4

```text
Fiche produit website_sale native uniquement
Pas de refonte panier / checkout
Pas de cross-sell avancé · pas de carousel associés · pas de recette inline
Pas de logique produit custom lourde
Home Phase 2 : grille SSR §5ter conservée — inchangée
Shop Phase 3 : composition dorevia_ck_theme inchangée
Header / footer Phase 1 : inchangés
Lien producteur : différé si pas de page CMS cible réelle (M1 / Phase 7)
```

### Recette obligatoire Phase 4 — triptyque QA

Document : [`RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md`](./RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md)

| Niveau | Contrôle |
|--------|----------|
| **1. Contrat Odoo** | `--test-tags=dorevia_ck_theme_phase4` · produit publié · add-to-cart OK |
| **2. Smoke curl** | `ck_phase4_ci.sh` · fiche · `/shop/cart` · `/shop` · `/professionnels` |
| **3. Playwright UX** | Desktop · mobile 390 px · hors gate module |
| Non-régression | Phase 1 · 2 · 3 |
| Verdict | **MOA/QA explicite** avant tout passage Phase 5 |

### Acte MOA signé — GO exécution §5quinquies (2026-06-13)

```text
GO EXÉCUTION ODOO V1 — CK V1.2.x
Périmètre autorisé : Phase 4 uniquement — Fiche produit native website_sale
Prérequis : Phase 3 clôturée OK partiel maîtrisé · gate ck_phase3_ci.sh OK
Garde-fous : pas refonte panier/checkout · pas cross-sell · pas recette inline
Pas de modification home Phase 2 · shop Phase 3 · header/footer Phase 1
Phases 5–10 : suspendues jusqu’à recette MOA/QA Phase 4
```

| Champ | Valeur |
|-------|--------|
| **Date acte GO Phase 4** | **2026-06-13** |
| **Signataire MOA** | **MOA CK** |

### Exécution Dev Phase 4 · **2026-06-13**

| Élément | Détail |
|---------|--------|
| **Module** | `dorevia_ck_theme` **19.0.1.2.0** |
| **Composition** | `product_ck_compose` · chips catégorie · signal Pro · enrichissements BO |
| **Bootstrap BO** | `hooks.bootstrap_published_products` · descriptions site si vides |
| **Gate portable** | [`scripts/ck_phase4_ci.sh`](./scripts/ck_phase4_ci.sh) · 12 tests · smoke OK |
| **Recette** | [`RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md`](./RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md) — **OK partiel confirmé MOA** |

### Verdict MOA Phase 4 · **OK partiel — clôturé · 2026-06-13**

| Champ | Valeur |
|-------|--------|
| **Verdict** | **OK partiel** — clôturé MOA |
| **Signataire** | **MOA CK** |
| **Contrôle MOA** | Recette/gouvernance · tests/vues · HTTP fiche · Playwright desktop 1280 · mobile 390 |
| **Gate portable Dev** | [`scripts/ck_phase4_ci.sh`](./scripts/ck_phase4_ci.sh) · 12/12 tests · smoke curl OK (Dev) |
| **Phase 5** | **✅ Clôturée OK partiel MOA** (2026-06-13) |

```text
Fiche conforme §5quinquies : ck-product-page · add_to_cart · prix · qty · description enrichie · chip · signal Pro
Lien producteur : absent (CMS M1 différé) · mobile 390/390 sans overflow
Réserves non bloquantes : enrichissement BO bootstrap · contenu métier non final · portabilité CK_CI_PRODUCT_PATH documentée
```

### Verdict QA Phase 4 · **OK partiel — clôturé MOA · 2026-06-13**

```text
Gate portable Phase 4 : OK Dev (ck_phase4_ci.sh · 12/12 tests · smoke curl)
Contrôle MOA : recette · tests/vues · fiche live · Playwright desktop 1280 · mobile 390
Verdict MOA : OK partiel — clôturé 2026-06-13
Lien producteur : absent (404 CMS — conforme gate M1)
Phase 5 : suspendue — acte MOA explicite requis
```

---

## 5sexies. Acte MOA — GO exécution Phase 5 (Professionnels + CRM) · **ACTÉ 2026-06-13**

| Champ | Valeur |
|-------|--------|
| **Prérequis** | ☑ Phase 4 clôturée OK partiel MOA · recette Phase 4 actée · **2026-06-13** |
| **Décision MOA** | ☑ **Acté** |
| **GO exécution Phase 5** | ☑ **Acté** · **2026-06-13** |
| **Périmètre autorisé** | **Phase 5 uniquement** — Professionnels + CRM natif |
| **Phases 6–10** | Suspendues |
| **Recette obligatoire** | [`RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md`](./RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md) |
| **Référence instance** | [`COMPOSITION_PROFESSIONNELS_V1_2.md`](./COMPOSITION_PROFESSIONNELS_V1_2.md) |
| **Validé par** | **MOA CK** |
| **Date acte** | **2026-06-13** |

> **Phase 5 : CLÔTURÉE OK partiel MOA** · **Phase 6 : INTERDIT** sans acte MOA explicite.

### Périmètre strict Phase 5

```text
Phase 5 uniquement — Professionnels + CRM natif website_crm
Consolidation page /professionnels existante · pas refonte transversale
```

| # | Livrable | Composant / route |
|---|----------|-------------------|
| 5.1 | Page `/professionnels` | Page CMS existante · consolidation copy · structure maquette |
| 5.2 | Double cible B2B | Producteur · fournisseur · distributeur · boutique / CHR — distinction lisible |
| 5.3 | Doctrine B2B sobre | Prix B2C publics · conditions pro back-office · pas pricing pro public |
| 5.4 | Formulaire CRM natif | `website_crm` · `s_website_form` · modèle `crm.lead` |
| 5.5 | Qualification simple | Champ message / `description` lead · pas champ CRM custom |
| 5.6 | Note qualification | Demande qualifiée · pas commande B2B en ligne |

**Hors périmètre Phase 5 — différé** :

| # | Élément | Report |
|---|---------|--------|
| — | Bloc dual compact · newsletter (M9) | **Phase 9** — pas livré Phase 5 |

**Exclus Phase 5** :

```text
Portail B2B · espace connecté pro
Pricing pro public · pricelist exposée
Workflow commercial custom · automation CRM avancée
Champs CRM custom · logique qualification lourde
Newsletter · bloc dual M9 (Phase 9 — non livré Phase 5)
Modification home Phase 2 · shop Phase 3 · fiche Phase 4 · header/footer Phase 1
Phase 6+ sans recette MOA/QA Phase 5 explicite
```

### Garde-fous Phase 5

```text
Page CMS /professionnels — consolidation · pas template custom lourd
Formulaire website_crm natif uniquement — un seul formulaire · deux CTA contextuels
Qualification via description lead — pas de champ CRM custom V1
Wording B2B sobre · M5 — promesses tenables
Pas de portail · pas de pricing pro public · pas de workflow commercial custom
Signaux Pro existants (home · shop · fiche) : inchangés sauf non-régression
Header / footer Phase 1 : inchangés
```

### Recette obligatoire Phase 5 — triptyque QA (doctrine Phase 4+)

Document : [`RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md`](./RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md)

| Niveau | Contrôle |
|--------|----------|
| **1. Contrat Odoo** | `--test-tags=dorevia_ck_theme_phase5` · page Pro · formulaire CRM · soumission lead |
| **2. Smoke curl** | `ck_phase5_ci.sh` · `/professionnels` · non-régression Phases 1–4 |
| **3. Playwright UX** | Desktop 1280 · mobile 390 px · hors gate module |
| Soumission CRM | Lead `crm.lead` créé · qualification lisible dans description |
| Non-régression | Phase 1 · 2 · 3 · 4 |
| Verdict | **MOA/QA explicite** avant tout passage Phase 6 |

### Acte MOA signé — GO exécution §5sexies (2026-06-13)

```text
GO EXÉCUTION ODOO V1 — CK V1.2.x
Périmètre autorisé : Phase 5 uniquement — Professionnels + CRM natif website_crm
Prérequis : Phase 4 clôturée OK partiel MOA · recette Phase 4 actée
Garde-fous : pas portail B2B · pas pricing pro public · pas workflow commercial custom · pas champs CRM custom
Wording B2B sobre · qualification simple via message / description
Phases 6–10 : suspendues jusqu’à recette MOA/QA Phase 5
```

| Champ | Valeur |
|-------|--------|
| **Date acte GO Phase 5** | **2026-06-13** |
| **Signataire MOA** | **MOA CK** |

### Exécution Dev Phase 5 · **2026-06-13**

| Élément | Détail |
|---------|--------|
| **Module** | `dorevia_ck_theme` **19.0.1.3.0** |
| **Bootstrap portable** | `hooks.bootstrap_professionnels_page()` · page CMS `/professionnels` · `#ck-pro-form` |
| **Composition** | Double cible · doctrine B2B · formulaire `crm.lead` natif · classe `ck-pro-page` |
| **Gate portable** | [`scripts/ck_phase5_ci.sh`](./scripts/ck_phase5_ci.sh) · 11 tests · smoke OK |
| **Recette** | [`RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md`](./RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md) — **OK partiel confirmé MOA** |

### Verdict MOA Phase 5 · **OK partiel — clôturé · 2026-06-13**

| Champ | Valeur |
|-------|--------|
| **Verdict** | **OK partiel** — clôturé MOA |
| **Signataire** | **MOA CK** |
| **Contrôle MOA** | Playwright desktop 1280 · mobile 390 · HTML `/professionnels` · tests Dev inspectés |
| **Gate portable Dev** | [`scripts/ck_phase5_ci.sh`](./scripts/ck_phase5_ci.sh) · 11/11 tests · smoke curl OK (Dev) |
| **Phase 6** | **✅ Clôturée OK MOA** |

```text
Conforme §5sexies : ck-pro-page · #ck-pro-form · crm.lead · profils producteur/fournisseur/distributeur/boutique-CHR
Garde-fous : pas portail · pas tarif automatique · pas pricing pro public
Soumission CRM : test_crm_form_submission_creates_lead · lead créé
Réserves non bloquantes : copy M5 à affiner métier · M9 différé Phase 9 · instabilité parallèle localhost (env)
```

### Verdict QA Phase 5 · **OK partiel — clôturé MOA · 2026-06-13**

```text
Gate portable Phase 5 : OK Dev (ck_phase5_ci.sh · 11/11 tests · smoke curl)
Contrôle MOA : Playwright desktop 1280 · mobile 390/390 · HTML live · tests Dev
Verdict MOA : OK partiel — clôturé 2026-06-13
Soumission CRM : crm.lead via /website/form/crm.lead · description transmise
Phase 6 : clôturée OK MOA · 2026-06-13
```

---

## 5septies. Acte MOA — GO exécution Phase 6 (Contact + À propos) · **CLÔTURÉE OK MOA · 2026-06-13**

| Champ | Valeur |
|-------|--------|
| **Prérequis** | ☑ Phase 5 clôturée OK partiel MOA · recette Phase 5 actée · **2026-06-13** |
| **Décision MOA** | ☑ **Acté** |
| **GO exécution Phase 6** | ☑ **Acté** · **2026-06-13** |
| **Périmètre autorisé** | **Phase 6 uniquement** — Contact + À propos |
| **Phases 7–10** | Suspendues |
| **Recette obligatoire** | [`RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md`](./RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md) |
| **Références maquette** | [`artifact/contact.html`](./artifact/contact.html) · [`artifact/a-propos.html`](./artifact/a-propos.html) |
| **Validé par** | **MOA CK** |
| **Date acte** | **2026-06-13** |

> **Phase 6 : CLÔTURÉE OK MOA** · **Phase 7 : INTERDIT** sans acte MOA explicite.

### Périmètre strict Phase 6 (pressenti)

```text
Phase 6 uniquement — Contact natif + page À propos CMS simple
Wording client · non technique · promesses sobres M5
```

| # | Livrable | Composant / route |
|---|----------|-------------------|
| 6.1 | Contact | `/contactus` · formulaire website natif |
| 6.2 | Parcours contact | Question produit · général · renvoi Pro → `/professionnels` |
| 6.3 | Nettoyage contact | Retrait contenu démo Odoo corps page (O1 Phase 1) |
| 6.4 | Page À propos | `/a-propos` · page CMS · classe `ck-about-page` |
| 6.5 | Présentation CK | Mission · confiance · sélection · logistique — blocs sobres |
| 6.6 | Liens cohérents | Boutique `/shop` · Professionnels `/professionnels` · Contact `/contactus` |
| 6.7 | Signal Pro discret | Lien `/professionnels` · pas de CRM sur contact B2C |

**Hors périmètre Phase 6 — différé** :

| # | Élément | Report |
|---|---------|--------|
| — | Bloc dual · newsletter (M9) | **Phase 9** — pas livré Phase 6 |
| — | Liens recettes · fiche producteur | **Phases 7–8** — pages absentes |

**Exclus Phase 6** :

```text
Blog · recettes · fiche producteur · newsletter · portail
Modification home Phase 2 · shop Phase 3 · fiche Phase 4 · header/footer/mega-menu Phase 1
Phase 7+ sans recette MOA/QA Phase 6 explicite
```

### Garde-fous Phase 6

```text
/contactus : route native Odoo · formulaire standard · distinct de /professionnels CRM
/a-propos : page CMS simple · pas template custom lourd · bootstrap portable si retenu
Wording client · non technique · promesses tenables M5
Pas de lien mort vers /recettes · /producteur/… tant que pages absentes
Signaux Pro existants : inchangés sauf non-régression
Home · shop · fiche · header/footer : inchangés
```

### Points de vigilance MOA

```text
Éviter vocabulaire trop technique · promesses commerciales trop fortes
Contact B2C ≠ formulaire CRM Pro (déjà Phase 5)
Délai de réponse contact : formulation M5 tenable (pas engagement contractuel fort)
Mega-menu : pas d’ajout /a-propos tant que non validé MOA post-recette (option footer/mega Phase ultérieure)
```

### Recette obligatoire Phase 6 — triptyque QA (doctrine Phase 4+)

Document : [`RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md`](./RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md)

| Niveau | Contrôle (pressenti) |
|--------|----------------------|
| **1. Contrat Odoo** | `--test-tags=dorevia_ck_theme_phase6` · `/contactus` · `/a-propos` |
| **2. Smoke curl** | `ck_phase6_ci.sh` · contact · à-propos · non-régression Phases 1–5 |
| **3. Playwright UX** | Desktop 1280 · mobile 390 px · hors gate module |
| Distinction B2C/Pro | Contact ≠ CRM Pro · renvoi `/professionnels` lisible |
| Non-régression | Phase 1 · 2 · 3 · 4 · 5 |
| Verdict | **MOA/QA explicite** avant tout passage Phase 7 |

### Acte MOA signé — GO exécution §5septies (2026-06-13)

```text
GO EXÉCUTION ODOO V1 — CK V1.2.x
Périmètre autorisé : Phase 6 uniquement — Contact + À propos
Prérequis : Phase 5 clôturée OK partiel MOA · recette Phase 5 actée
Garde-fous : pas blog · pas recettes · pas fiche producteur · pas newsletter · pas portail
Pas de modification home · shop · fiche · header/footer hors non-régression
Phases 7–10 : suspendues jusqu’à recette MOA/QA Phase 6
```

| Champ | Valeur |
|-------|--------|
| **Date acte GO Phase 6** | **2026-06-13** |
| **Signataire MOA** | **MOA CK** |

### Exécution Dev Phase 6 · **2026-06-13**

| Élément | Détail |
|---------|--------|
| **Module** | `dorevia_ck_theme` **19.0.1.4.0** |
| **Bootstrap portable** | `bootstrap_contactus_page()` · `bootstrap_a_propos_page()` |
| **Composition** | `/contactus` · `ck-contact-page` · `mail.mail` · O1 démo retiré · `/a-propos` · `ck-about-page` |
| **Gate portable** | [`scripts/ck_phase6_ci.sh`](./scripts/ck_phase6_ci.sh) · 12 tests · smoke OK |
| **Recette** | [`RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md`](./RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md) — **OK MOA confirmé** |

### Verdict MOA Phase 6 · **OK — clôturé · 2026-06-13**

| Champ | Valeur |
|-------|--------|
| **Verdict** | **OK** — clôturé MOA |
| **Signataire** | **MOA CK** |
| **Contrôle MOA** | Docs · hooks/tests · gate · HTML live · Playwright desktop 1280 · mobile 390 |
| **Gate portable Dev** | [`scripts/ck_phase6_ci.sh`](./scripts/ck_phase6_ci.sh) · 12/12 tests · smoke curl OK |
| **Phase 7** | **Suspendue** — acte MOA explicite requis |

```text
Conforme §5septies : ck-contact-page · contactus_form · mail.mail · ck-about-page
Contact B2C distinct CRM Pro · O1 résolu (Ma société · Fake Buena Vista absents)
/a-propos : mission · sélection · logistique · liens /shop · /professionnels · /contactus
Mobile 390/390 sans overflow · non-régression Phases 1–5 OK
```

**Réserves non bloquantes** :

```text
Copy M5 à relire avant go-live (confiance · logistique)
CK_CI_TEST_HTTP_PORT=8075 — éviter deux gates parallèles sur le même port
/a-propos non exposée mega-menu — conforme gate actuel
```

### Verdict QA Phase 6 · **OK — clôturé MOA · 2026-06-13**

```text
Gate portable Phase 6 : OK Dev (ck_phase6_ci.sh · 12/12 tests · smoke curl)
Contrôle MOA : Playwright desktop 1280 · mobile 390/390 · HTML live · tests Dev
Verdict MOA : OK — clôturé 2026-06-13
Phase 7 : dossier §5octies préparé · Dev interdit sans acte MOA signé
```

---

## 5octies. Acte MOA — GO exécution Phase 7 (Fiche producteur CMS pilote · M1) · **ACTÉ 2026-06-13**

| Champ | Valeur |
|-------|--------|
| **Prérequis** | ☑ Phase 6 clôturée OK MOA · recette Phase 6 actée · **2026-06-13** |
| **Décision MOA** | ☑ **Acté** |
| **GO exécution Phase 7** | ☑ **Acté** · **2026-06-13** |
| **Périmètre autorisé** | **Phase 7 uniquement** — Fiche producteur CMS pilote · **M1** |
| **Phases 8–10** | Suspendues |
| **Recette obligatoire** | [`RECETTE_QA_PHASE7_FICHE_PRODUCTEUR_CK_V1.md`](./RECETTE_QA_PHASE7_FICHE_PRODUCTEUR_CK_V1.md) |
| **Référence maquette** | [`artifact/fiche-producteur.html`](./artifact/fiche-producteur.html) |
| **Validé par** | **MOA CK** |
| **Date acte** | **2026-06-13** |

> **Phase 7 : livrée Dev** · **Phase 8 : INTERDIT** sans recette MOA/QA Phase 7.

### Périmètre strict Phase 7 (pressenti)

```text
Phase 7 uniquement — 1 fiche producteur CMS pilote (M1)
Wording client · origine lisible · promesses sobres M5
```

| # | Livrable | Composant / route |
|---|----------|-------------------|
| 7.1 | Fiche pilote | `/producteur/atelier-hauts-goyaviers` · page CMS · classe `ck-producer-page` |
| 7.2 | Présentation | Nom · territoire · origine · tagline |
| 7.3 | Savoir-faire | Histoire · transformation · lien territoire — blocs texte CMS |
| 7.4 | Critères sélection CK | Liste statique · pourquoi CK sélectionne — pas scoring auto |
| 7.5 | Produits associés | Grille produits **si liens BO réels** (tag / catégorie) · sinon CMS manuel sobre |
| 7.6 | Signal logistique | Rôle CK · distinction B2B · **M5** tenable |
| 7.7 | CTA sortie | `/shop` · `/contactus` · `/professionnels` selon pertinence |

**Hors périmètre Phase 7 — différé** :

| # | Élément | Report |
|---|---------|--------|
| — | Lien mini fiche produit (Phase 4.3) | **Hors scope Phase 7** — pas modification fiche produit |
| — | Entrée nav **Producteurs** | **Option post-recette MOA** — header/footer inchangés Phase 7 |
| — | Lien recettes · usage/conseil | **Phase 8** — page `/recettes` absente |
| — | Sélection CK focus ×2 séparée | **Simplifiable** — fusion grille produits si besoin V1 |

**Exclus Phase 7** :

```text
Annuaire producteurs · portail producteur · espace connecté · workflow fournisseur
Scoring automatisé · promesse logistique excessive
Modification home · shop · fiche produit · contact · à propos · header/footer/mega-menu
Phase 8+ sans recette MOA/QA Phase 7 explicite
```

### Garde-fous Phase 7 · M1

```text
1 seule fiche pilote — pas annuaire · pas liste multi-producteurs
Page CMS simple · bootstrap portable si retenu — pas module producteur autonome
Produits associés : uniquement si convention BO explicite (tag / catégorie) ou cartes CMS manuelles
Pas de lien mort · pas de grille vide trompeuse
Wording M5 : pas sur-promesse logistique · pas discours marketplace
Home · shop · fiche · contact · à propos · header/footer : inchangés (non-régression)
```

### Points de vigilance MOA

```text
Capital BO : 0 tag producteur à ce stade — grille produits conditionnelle ou CMS manuel
Fournisseur Odoo natif (Option B) : hors scope V1 — CMS pilote uniquement (M1 acté)
Lien depuis fiche produit Phase 4 : différé — pas livré Phase 7 sans acte distinct
Mega-menu / nav Producteurs : pas d’ajout tant que non validé MOA post-recette
Copy producteur : contenu éditorial pilote — à valider métier avant go-live
```

### Recette obligatoire Phase 7 — triptyque QA (doctrine Phase 4+)

Document : [`RECETTE_QA_PHASE7_FICHE_PRODUCTEUR_CK_V1.md`](./RECETTE_QA_PHASE7_FICHE_PRODUCTEUR_CK_V1.md)

| Niveau | Contrôle (pressenti) |
|--------|----------------------|
| **1. Contrat Odoo** | `--test-tags=dorevia_ck_theme_phase7` · fiche producteur pilote |
| **2. Smoke curl** | `ck_phase7_ci.sh` · producteur · non-régression Phases 1–6 |
| **3. Playwright UX** | Desktop 1280 · mobile 390 px · hors gate module |
| M1 | 1 fiche · pas annuaire · pas portail |
| Non-régression | Phase 1 · 2 · 3 · 4 · 5 · 6 |
| Verdict | **MOA/QA explicite** avant tout passage Phase 8 |

### Acte MOA signé — GO exécution §5octies (2026-06-13)

```text
GO EXÉCUTION ODOO V1 — CK V1.2.x
Périmètre autorisé : Phase 7 uniquement — Fiche producteur CMS pilote (M1)
Prérequis : Phase 6 clôturée OK MOA · recette Phase 6 actée
Garde-fous : 1 fiche pilote · pas annuaire · pas portail · pas workflow fournisseur · pas scoring auto
Pas de modification home · shop · fiche produit · contact · à propos · header/footer hors non-régression
Phases 8–10 : suspendues jusqu’à recette MOA/QA Phase 7
```

| Champ | Valeur |
|-------|--------|
| **Date acte GO Phase 7** | **2026-06-13** |
| **Signataire MOA** | **MOA CK** |

### Exécution Dev Phase 7 · **2026-06-13**

| Élément | Détail |
|---------|--------|
| **Module** | `dorevia_ck_theme` **19.0.1.5.0** |
| **Bootstrap portable** | `bootstrap_producer_page()` · `/producteur/atelier-hauts-goyaviers` · `ck-producer-page` |
| **Composition** | Présentation · savoir-faire · critères CK · produits BO réels · CTA shop/contact/pro |
| **Gate portable** | [`scripts/ck_phase7_ci.sh`](./scripts/ck_phase7_ci.sh) · 12 tests · smoke OK |
| **Recette** | [`RECETTE_QA_PHASE7_FICHE_PRODUCTEUR_CK_V1.md`](./RECETTE_QA_PHASE7_FICHE_PRODUCTEUR_CK_V1.md) — **en attente verdict MOA** |

### Verdict MOA final Phase 7 · **CLÔTURÉE OK partiel MOA · 2026-06-14**

| Champ | Valeur |
|-------|--------|
| **Module** | `dorevia_ck_theme` **19.0.1.6.0** |
| **Verdict MOA (19.0.1.5.0)** | **KO** — fragment sans layout · **historique corrigé** |
| **Verdict MOA final** | **OK partiel MOA** |
| **Intégration page producteur** | **Validée** — layout · assets · `body.ck-theme` · desktop 1280/1280 · mobile 390/390 |
| **Réserve header/menu CK** | **Maintenue** — dette UX/UI transversale go-live / Phase 1 · **non bloquante Phase 7** |
| **Gate Dev** | **OK** — contenu fiche · triptyque · non-régression |
| **Phase 8** | **Suspendue** — acte MOA distinct requis |

```text
Phase 7 — OK partiel MOA.
Intégration website/CSS corrigée et validée.
Réserve header/menu maintenue comme dette UX/UI transversale go-live / Phase 1.
Phase 8 suspendue à acte MOA distinct.
```

> **Phase 8 : CLÔTURÉE OK partiel MOA** · **Phase 9 : CLÔTURÉE OK partiel MOA · 2026-06-14** · **Phase 10 suspendue** · **§4bis QA isolation OK acté**.

---

## 5nonies. Phase 8 (Recettes statiques / Savoirs · M2) · **CLÔTURÉE OK partiel MOA · 2026-06-14**

| Champ | Valeur |
|-------|--------|
| **Prérequis** | ☑ Phase 7 clôturée OK partiel MOA · **2026-06-14** |
| **Décision MOA GO exécution** | ☑ **Acté MOA · 2026-06-14** |
| **Verdict MOA clôture** | ☑ **OK partiel MOA · 2026-06-14** |
| **Périmètre autorisé** | **Phase 8 uniquement** — Page CMS `/recettes` · **M2** |
| **Module livré** | `dorevia_ck_theme` **19.0.1.7.0** |
| **Route livrée** | `/recettes` · classe `ck-recipes-page` |
| **Phases 9–10** | **Suspendues** — acte MOA distinct requis |
| **Recette obligatoire** | [`RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md`](./RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md) · triptyque OK · recontrôle MOA OK |
| **Composition** | [`COMPOSITION_RECETTES_V1_2.md`](./COMPOSITION_RECETTES_V1_2.md) |
| **Référence maquette** | [`artifact/recettes.html`](./artifact/recettes.html) |
| **Validé par** | MOA |
| **Date acte GO** | **2026-06-14** |
| **Date livraison Dev** | **2026-06-14** |
| **Date clôture MOA** | **2026-06-14** |

> **Phase 8 — OK partiel MOA.** Page `/recettes` conforme au périmètre M2 : CMS statique · 6 cartes · liens BO réels · pas de blog · pas de commentaires · layout Odoo complet.

### Périmètre strict Phase 8 (acté · livré)

```text
Phase 8 uniquement — 1 page CMS recettes statiques (M2)
Wording éditorial sobre · liens catalogue BO réels · pas sur-promesse
```

| # | Livrable | Composant / route | Statut |
|---|----------|-------------------|--------|
| 8.1 | Page recettes | `/recettes` · page CMS · classe `ck-recipes-page` | ✅ |
| 8.2 | Hero éditorial | Usages · transmission · cuisine créole | ✅ |
| 8.3 | Grille 6 cartes | Recettes · guides · conseils — CMS manuel statique | ✅ |
| 8.4 | Liens catalogue | Produits publiés · `/shop` · producteur pilote | ✅ |
| 8.5 | Intégration layout | `website.layout` · `_wrap_website_page_arch()` — dès bootstrap | ✅ |

**Hors périmètre Phase 8 — différé** :

| # | Élément | Report |
|---|---------|--------|
| — | Lien mega-menu `/recettes` | **Option post-recette MOA** — header inchangé Phase 8 |
| — | CTA à-propos · fiche producteur → recettes | **Option post-recette** ou acte distinct |
| — | Lien recette inline fiche produit | **Hors scope Phase 8** |
| — | Blog · commentaires · RSS | **Exclus M2** |

**Exclus Phase 8** :

```text
website_blog · moteur éditorial · contribution utilisateur · forum
Modification home · shop · fiche produit · contact · producteur · header/footer/mega-menu
Phase 9+ sans recette MOA/QA Phase 8 explicite
```

### Garde-fous Phase 8 · M2

```text
Page CMS statique unique — pas blog · pas multi-auteurs
Bootstrap portable — réutiliser _bootstrap_cms_page + website.layout (leçon Phase 7)
Liens cartes : BO réels uniquement · pas URLs maquette
Wording M5 : pas sur-promesse · contenu éditorial sobre
Home · shop · fiche · contact · à propos · producteur · header/footer : inchangés (non-régression)
Réserve header CK : dette transversale go-live — non bloquante Phase 8
```

### Recette obligatoire Phase 8 — triptyque QA

Document : [`RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md`](./RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md)

| Niveau | Contrôle | Résultat |
|--------|----------|----------|
| **1. Contrat Odoo** | `--test-tags=dorevia_ck_theme_phase8` | ✅ 15/15 |
| **2. Smoke curl** | `ck_phase8_ci.sh` · `/recettes` · layout · non-régression Phases 1–7 | ✅ |
| **3. Playwright UX** | Desktop 1280 · mobile 390 px · pas overflow | ✅ |
| M2 | CMS statique · pas blog | ✅ |
| Non-régression | Phases 1–7 | ✅ |
| Verdict | **OK partiel MOA · 2026-06-14** | ✅ |

### Verdict MOA clôture Phase 8 · **ACTÉ 2026-06-14**

```text
Phase 8 — OK partiel MOA.
Page /recettes conforme au périmètre M2 : CMS statique, 6 cartes, liens BO réels,
pas de blog, pas de commentaires, layout Odoo complet.
Réserve header/menu CK maintenue comme dette transversale go-live.
Phase 9 : GO §5decies acté · Dev livrée · clôture MOA en attente.
```

**Recontrôle MOA cache-bust** (`/recettes?qa_ts=1`) :

| Contrôle | Résultat |
|----------|----------|
| HTTP 200 | ✅ |
| doctype html | ✅ |
| `body.ck-theme` | ✅ |
| `web.assets_frontend` | ✅ |
| `ck-recipes-page` | ✅ |
| Header / footer | ✅ |
| H1 « Recettes & savoirs CK » | ✅ |
| 6 cartes statiques | ✅ |
| Pas blog / commentaires | ✅ |
| Desktop 1280/1280 | ✅ |
| Mobile 390/390 | ✅ |
| Menu mobile sans overflow | ✅ |

**Liens principaux contrôlés 200** : `/recettes` · `/shop/confiture-de-goyave-3` · `/shop` · `/producteur/atelier-hauts-goyaviers` · `/a-propos` · `/contactus`

**Réserve UX/UI header-menu** (identique Phase 7) :

```text
Header/menu encore très Odoo natif :
logo placeholder, offcanvas peu brandé CK, finition go-live insuffisante.
Dette UX/UI transversale Phase 1 / go-live, non bloquante Phase 8.
```

### Acte MOA — GO exécution §5nonies · **ACTÉ 2026-06-14**

```text
GO EXÉCUTION ODOO V1 — CK V1.2.x
Périmètre autorisé : Phase 8 uniquement — Recettes statiques / Savoirs (M2)
Prérequis : Phase 7 clôturée OK partiel MOA
Garde-fous : 1 page CMS · pas blog · pas commentaires · website.layout obligatoire
Pas de modification home · shop · fiche · contact · producteur · header/footer hors non-régression
Phases 9–10 : suspendues jusqu’à recette MOA/QA Phase 8
```

**Livraison Dev 19.0.1.7.0** :

| Élément | Détail |
|---------|--------|
| Bootstrap | `bootstrap_recipes_page()` · `build_recipes_page_arch()` · 6 cartes statiques |
| Migration | `19.0.1.7.0/post-migrate.py` |
| Tests | `test_ck_phase8_hooks.py` · `test_ck_phase8_compose.py` |
| Gate | [`ck_phase8_ci.sh`](./scripts/ck_phase8_ci.sh) |
| Fix transversal | `escape(page_name)` dans `_wrap_website_page_arch()` (titres avec `&`) |

**Réserve maintenue** : header/menu CK = dette transversale go-live / Phase 1 · **non bloquante Phase 8**.

---

## 5decies. Phase 9 (Newsletter M9 simple) · **CLÔTURÉE OK partiel MOA · 2026-06-14**

| Champ | Valeur |
|-------|--------|
| **Prérequis** | ☑ Phase 8 clôturée OK partiel MOA · **2026-06-14** |
| **Décision MOA GO exécution** | ☑ **Acté MOA · 2026-06-14** |
| **QA documentaire** | ☑ **OK documentaire · 2026-06-14** |
| **Verdict MOA clôture** | ☑ **OK partiel MOA · 2026-06-14** |
| **Périmètre autorisé** | **Phase 9 uniquement** — Newsletter M9 simple |
| **Modules livrés** | `dorevia_ck_theme` **19.0.1.10.0** · `dorevia_ck_marketone_content` **19.0.1.0.0** |
| **Phases 10** | **Suspendues** — acte MOA distinct requis |
| **Recette obligatoire** | [`RECETTE_QA_PHASE9_NEWSLETTER_CK_V1.md`](./RECETTE_QA_PHASE9_NEWSLETTER_CK_V1.md) · triptyque OK |
| **Référence copy / visuel** | [`note_reference_bloc_double_pro_newsletter_ck.md`](./note_reference_bloc_double_pro_newsletter_ck.md) |
| **CE M9** | [`RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md`](./RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md) §0bis |
| **Validé par** | MOA |
| **Date acte GO** | **2026-06-14** |
| **Date livraison Dev** | **2026-06-14** |

> **GO exécution Phase 9 acté MOA** · dual compact newsletter sur `/contactus` et `/professionnels` · mailing list BO `Newsletter CK` · snippet natif · home Phase 2 non modifiée.

### Périmètre strict Phase 9 (acté · livré)

```text
Phase 9 uniquement — Newsletter M9 simple
Inscription newsletter · mass_mailing · website_mass_mailing · RGPD · wording sobre
Pas tunnel marketing · pas automation avancée
```

| # | Livrable | Composant / route | Statut |
|---|----------|-------------------|--------|
| 9.1 | Modules CE | `mass_mailing` · `website_mass_mailing` | ✅ |
| 9.2 | Mailing list BO | `mailing.list` · `Newsletter CK` · `data-list-id` | ✅ |
| 9.3 | Contact — dual compact | `/contactus` · `ck-dual-engage--compact` | ✅ |
| 9.4 | Pro — dual compact | `/professionnels` · CTA `#ck-pro-form` | ✅ |
| 9.5 | Subscribe natif | `/website_mass_mailing/subscribe` | ✅ |
| 9.6 | RGPD | Consentement · désinscription mentionnée | ✅ |

**Capital Phase 2 (hors périmètre modification)** :

| Élément | Statut |
|---------|--------|
| Home `/` — bloc dual Pro/newsletter | **Déjà livré Phase 2** · recontrôle non-régression uniquement |
| `list_id` home Phase 2 | Existant · **non modifié** · recontrôle OK |
| `list_id` contact/pro Phase 9 | Mailing list BO `Newsletter CK` · id dynamique instance |

**Hors périmètre Phase 9 — différé / exclus** :

| # | Élément | Report |
|---|---------|--------|
| — | Modification **home** · **shop** · **fiche produit** · **producteur** · **recettes** | **Interdit Phase 9** (recontrôle OK) |
| — | Refonte header / footer / mega-menu | Dette go-live · Phase 1 |
| — | Footer global newsletter | **Différé** · hors V1 |
| — | Pop-up newsletter | **Exclu** · pas agressif |
| — | Automation · séquences · segmentation | **Exclus M9** |
| — | Snippet `s_ck_dual_engage` custom | **Optionnel** · privilégier composition native |

**Exclus Phase 9** :

```text
website_blog · moteur éditorial · contribution utilisateur
Campagne promotionnelle complexe · tunnel marketing
Modification pages interdites hors ajout bloc dual contact/pro
Phase 10+ sans recette MOA/QA Phase 9 explicite
```

### Garde-fous Phase 9 · M9

```text
Newsletter simple = subscribe + mailing list BO + RGPD — pas marketing automation
Snippet natif website_mass_mailing prioritaire — pas sur-ingénierie thème
Home dual Phase 2 : ne pas rouvrir — non-régression subscribe home incluse recette
Contact / Pro : pattern dual compact réutilisable (réf. note_reference_bloc_double_pro_newsletter_ck)
Contact / Pro : ne pas mélanger formulaire B2C · formulaire CRM Pro · newsletter — trois intentions lisibles
Wording M5/M9 : pas sur-promesse · pas promo agressive · ton éditorial CK
Gate M9 historique : si contact/pro non simple → différer variante · Pro seul conservé
Réserve header CK : dette transversale go-live — non bloquante Phase 9
```

### Recette obligatoire Phase 9 — triptyque QA

Document : [`RECETTE_QA_PHASE9_NEWSLETTER_CK_V1.md`](./RECETTE_QA_PHASE9_NEWSLETTER_CK_V1.md)

| Niveau | Contrôle | Résultat |
|--------|----------|----------|
| **1. Contrat Odoo** | `--test-tags=dorevia_ck_theme_phase9` | ✅ 17/17 |
| **2. Smoke curl** | [`ck_phase9_ci.sh`](./scripts/ck_phase9_ci.sh) | ✅ |
| **3. Playwright UX** | Desktop 1280 · mobile 390 px | ✅ |
| M9 | Subscribe simple · pas popup | ✅ |
| Non-régression | Phases 1–8 · home dual Phase 2 intact | ✅ |
| Verdict clôture | **MOA/QA explicite** avant Phase 10 | ☐ en attente |

**E-mail test recette** : `qa-phase9-newsletter@test.ck.local` · purge après test.

### Acte MOA — GO exécution §5decies · **ACTÉ 2026-06-14**

```text
GO EXÉCUTION ODOO V1 — CK V1.2.x
Périmètre autorisé : Phase 9 uniquement — Newsletter M9 simple
Prérequis : Phase 8 clôturée OK partiel MOA
Garde-fous : inscription simple · mass_mailing · RGPD · pas automation · pas popup agressive
Pas modification home · shop · fiche · producteur · recettes · header/footer hors non-régression
Emplacements livrés : dual compact contact + professionnels (+ recontrôle home Phase 2)
Phase 10 : suspendue jusqu’à recette MOA/QA Phase 9
```

**Livraison Dev 19.0.1.8.0** :

| Élément | Détail |
|---------|--------|
| Depends | `mass_mailing` · `website_mass_mailing` |
| Bootstrap | `bootstrap_newsletter_mailing_list()` · `build_*_page_arch()` |
| Pages | `/contactus` · `/professionnels` — dual compact `#ck-newsletter-subscribe` |
| Migration | `19.0.1.8.0/post-migrate.py` |
| Tests | `test_ck_phase9_hooks.py` · `test_ck_phase9_compose.py` |
| Gate | [`ck_phase9_ci.sh`](./scripts/ck_phase9_ci.sh) |

**Vigilances MOA maintenues** : subscribe test avec purge · reCAPTCHA non bloquant · RGPD · séparation B2C/Pro/newsletter.

### Verdict QA documentaire · **OK · 2026-06-14** (préparation)

```text
OK documentaire — dossier Phase 9 cohérent et opposable (préparation · 2026-06-14).
GO exécution acté · Dev livrée · triptyque QA OK · clôture MOA en attente.
```

**Points validés (QA documentaire)** :

| Point | Verdict |
|-------|---------|
| Phases 1–8 clôturées | ✅ |
| Phase 9 · GO §5decies · Dev livrée · triptyque OK | ✅ |
| Réserve architecture · généricité `dorevia_ck_theme` | ✅ **§4bis QA OK acté · 2026-06-14** |
| Périmètre M9 simple · mailing list BO · modules CE | ✅ |
| Home protégée · dual Phase 2 · recontrôle seulement | ✅ |
| Emplacements pressentis · contact + pro uniquement | ✅ |
| Exclusions automation · popup · refonte header/footer | ✅ |
| Phase 10 suspendue · recette cases vides (pas fausse validation) | ✅ |

**Points de vigilance avant GO Dev** :

| # | Point | Consigne |
|---|-------|----------|
| 1 | Test subscribe | Adresse e-mail test explicite · purge/nettoyage mailing list si besoin |
| 2 | reCAPTCHA | Vérifier au GO · **non bloquant Phase 9** si subscribe natif fonctionne sans surcouche |
| 3 | RGPD | Mention sobre mais réelle · désinscription visible · pas collecte opaque |
| 4 | Contact / Pro | Séparer B2C · CRM Pro · newsletter — trois intentions lisibles |

### Acte MOA — clôture Phase 9 · **ACTÉ 2026-06-14**

```text
Phase 9 — OK partiel MOA.
Newsletter M9 simple : dual compact sur /contactus et /professionnels,
mailing list BO Newsletter CK, subscribe natif, RGPD mentionné,
séparation Contact B2C / CRM Pro / Newsletter maintenue.
Home Phase 2 non modifiée · non-régression Phases 1–8 OK.
Réserve header/menu CK maintenue comme dette transversale go-live.
Architecture split thème/contenu validée — chantier non rouvert.
Phase 10 : suspendue — acte MOA distinct requis.
```

**Recontrôle MOA cache-bust** (`?qa_ts=1`) · gate `ck_phase9_ci.sh` · **2026-06-14** :

| Contrôle | `/contactus` | `/professionnels` |
|----------|--------------|-------------------|
| HTTP 200 | ✅ | ✅ |
| `ck-dual-engage--compact` | ✅ | ✅ |
| `#ck-newsletter-subscribe` | ✅ | ✅ |
| RGPD · « Désinscription possible » | ✅ | ✅ |
| Contact B2C · `contactus_form` · `mail.mail` | ✅ | — |
| CRM Pro · `#ck-pro-form` · `crm.lead` | — | ✅ |
| Pas popup newsletter | ✅ | ✅ |
| Home dual Phase 2 intact | ✅ (/) | — |
| Triptyque Odoo 17/17 | ✅ | ✅ |

**Doctrine architecture (actée · non rouverte)** :

```text
dorevia_ck_theme = socle thème / UI / snippets / assets
dorevia_ck_marketone_content = contenu métier CK + bootstraps éditoriaux
Réserve post-V1 migrations historiques thème : non bloquante · documentée
```

---

## 5undecies. Phase 10 (Recette globale go-live) · **DOSSIER PRÉPARÉ · 2026-06-14**

### Doctrine MOA · actée

```text
Phase 10 ≠ nouvelle phase de production / feature.
Phase 10 = recette finale go-live transversale, avant verdict MOA go-live V1.
Dev interdit sans acte MOA §5undecies exécution explicite.
```

| Champ | Valeur |
|-------|--------|
| **Prérequis** | ☑ Phases 1–9 clôturées OK partiel MOA · **2026-06-14** |
| **GO préparation dossier** | ☑ **Acté MOA · 2026-06-14** |
| **Dossier recette** | [`RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md`](./RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md) |
| **Verdict clôture Phase 9** | ☑ **OK partiel MOA · 2026-06-14** |
| **Nature Phase 10** | **Recette QA / MOA** — pas livraison fonctionnelle par défaut |
| **Focus prioritaire** | **Dette header / menu / branding CK** (grille §2 dossier recette) |
| **Exécution Dev** | ☑ **GO §5undecies exécution acté · livré 19.0.1.11.0 · 2026-06-14** |
| **Recette MOA écran** | 🔍 **En cours · §2 header P0 · recontrôle visuel 1280/390 requis post-Dev** |
| **Doctrine split §4bis** | **Non rouverte** |

### Périmètre recette go-live (checklist MOA)

```text
mobile 390 px (toutes pages traduites Phases 1–9)
header / menu / branding CK          ← PRIORITÉ dette go-live
footer / mentions légales
liens morts / routes / mapping BO
copy M5 (promesses réassurance tenables)
checkout / panier
newsletter (Phase 9 · non-régression)
formulaires (Contact B2C · CRM Pro · séparation)
assets / cache / cache-bust recette
non-régression pages Phases 1–9
```

| # | Axe recette | Référence / note |
|---|-------------|------------------|
| 10.1 | Composition CMS globale | [`recette_qa_composition_cms_ck_01.md`](../recette_qa_composition_cms_ck_01.md) · [`RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md`](./RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md) |
| 10.2 | Mobile 390 px | Dossier recette §3.1 |
| 10.3 | Header / menu / branding | **P0** · Dossier recette §2 · [`note_reference_header_mega_menu_decouverte_ck_v1.md`](./note_reference_header_mega_menu_decouverte_ck_v1.md) |
| 10.4 | Footer / mentions | Phase 1 · recette globale |
| 10.5 | Liens morts · routes | Mapping BO · pas de 404 critique |
| 10.6 | Copy M5 | Promesses réassurance · avant go-live |
| 10.7 | Checkout / panier | Phase 3+ · CE natif |
| 10.8 | Newsletter · formulaires | Phase 9 · Phase 5–6 · séparation parcours |
| 10.9 | Assets / cache | Cache-bust recette · SSR |
| 10.10 | Non-régression 1–9 | Gates phases · smoke curl |
| 10.11 | Verdict MOA go-live | Distinct du GO exécution §5 · acte final V1 |

### Verdict MOA sur retour Dev / gouvernance · **ACTÉ 2026-06-14**

```text
OK QA gouvernance.
Phase 9 reste clôturée OK partiel MOA.
Phase 10 s’ouvre comme recette finale / go-live — pas comme nouvelle feature.
Focus prioritaire : dette header-menu CK.
Réserve migrations historiques thème : acceptable post-V1 · documentée · non bloquante.
```

### Acte MOA — pré-contrôle technique §2 · **OK partiel · 2026-06-14**

```text
Pré-contrôle technique Phase 10 §2 : OK partiel (DOM conteneur Odoo).
Contrat HTML / header / assets / logo C-Kreyol : OK.
Nav header : Boutique · Découvrir · Professionnels · Contactez-nous — pas Producteurs (conforme gate).
Mega Épicerie créole : OK.
Contrôle visuel écran 1280 + 390 : non conclusif (instabilité navigateur hôte) — MOA écran requis.
Clôture §2 : en attente recontrôle visuel MOA.
GO exécution Dev §5undecies : acté · livraison header 19.0.1.11.0 · recontrôle écran requis.
```

### Acte MOA — GO exécution §5undecies ciblé header · **ACTÉ 2026-06-14**

```text
GO EXÉCUTION PHASE 10 — Corrections header / menu / branding CK V1.2.x
Périmètre autorisé : logo · header desktop 1280 · mega Découvrir (habillage) · mobile 390
Interdit : nouvelle page · refonte globale · checkout · split thème/contenu · Producteurs nav
         · modification fonctionnelle mega · automation newsletter · phases postérieures
Module : dorevia_ck_theme uniquement
Recette obligatoire : RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md §2
Validé par : MOA CK · 2026-06-14
```

**Livraison Dev `dorevia_ck_theme` 19.0.1.11.0** :

| Élément | Détail |
|---------|--------|
| QWeb | `views/website_header.xml` — classe `ck-header` sur `header#top` |
| SCSS | `static/src/scss/website_header.scss` — sticky · logo · nav · mega · offcanvas mobile |
| Tests | `test_ck_phase10_header_compose.py` · tag `dorevia_ck_theme_phase10` |
| Migration | `19.0.1.11.0/post-migrate.py` — no-op |
| Gate | [`ck_phase10_ci.sh`](./scripts/ck_phase10_ci.sh) |

**Verdict Dev post-gate · 2026-06-14** :

```text
Gate Phase 10 header : OK (upgrade · 3 tests Odoo · smoke 7 routes).
Contrat HTML : ck-header · C-Kreyol · nav Boutique/Découvrir/Professionnels/Contactez-nous · o_mega_menu · Épicerie créole.
Pas d'entrée Producteurs · pas Your Logo · non-régression marqueurs pages 1–9 OK.
Verdict visuel 1280/390 : non signé Dev — recontrôle MOA écran requis pour clôture §2.
```

### Acte MOA — séparation chantiers + séquence · **ACTÉ 2026-06-14**

```text
Séparation actée :
  Chantier A — dorevia_ck_theme + dorevia_ck_marketone_content · dorevia_ck_marketone_01 · Phase 10 go-live
  Chantier B — dorevia_ckreyol_marketone · ckr-marketone-01 · PR #62 (indépendant)

Verdict go-live global CK : NON SIGNÉ.

Priorité immédiate Chantier A : A1 recontrôle écran header §2.
Options verdict A1 : A1-OK · A1-GO Dev ciblé · A1-KO.
Tant que A1 non signé : pas de nouveau GO Dev header.

Séquence retenue :
  1. Recontrôle écran A1
  2. Décision A1
  3. Confirmation technique PR #62 (Chantier B)
  4. Décision B1 merge PR #62
  5. Proposition A7 mise sous Git modules CK (acte distinct)
  6. Recettes séparées A §3–§9 · B 6.3a/6.3b/SEO

Documents préparés :
  RECETTE_MOA_ECRAN_A1_HEADER_PHASE10.md
  PROPOSITION_A7_MISE_SOUS_GIT_MODULES_CK.md
Validé par : MOA CK · 2026-06-14
```

### Acte MOA — ouverture session A1 · **ACTÉ 2026-06-14**

```text
Chantier A — Phase 10 §2 header / menu / branding CK.
Pré-contrôle technique Dev : OK (ck-header · C-Kreyol · nav · mega · pas Producteurs nav).
Verdict A1 : NON SIGNÉ — session recontrôle écran ouverte.
Contrôles : desktop 1280 · mobile 390 · cohérence CK · mega · overflow · arbitrage Contactez-nous.
Options post-session : A1-OK · A1-GO Dev ciblé · A1-KO.
Tant que A1 non signé : aucun nouveau GO Dev header · aucun Dev header.
Document : RECETTE_MOA_ECRAN_A1_HEADER_PHASE10.md
Validé par : MOA CK · 2026-06-14
```

### Acte MOA — Chantier B · GO merge PR #62 (B1) · **ACTÉ · MERGÉ 2026-06-14**

```text
Chantier B — dorevia_ckreyol_marketone · ckr-marketone-01.
GO merge PR #62 acté sous réserve périmètre confirmé :
  Promotions · Kits · SEO portes shop · BO · warnings Odoo 19.
Merge : https://github.com/doreviateam/odoo19-addons-dorevia/pull/62 — MERGED · commit 388e515 · 19.0.19.0.1.
Ne vaut PAS clôture MOA lots 6.3a / 6.3b / SEO.
Suite : recettes navigateur RECETTE_MANUELLE_LOT6_3A_PROMO · LOT6_3B_PACK · SEO portes shop.
Indépendant Chantier A · pas de mélange avec Phase 10 CK.
Validé par : MOA CK · 2026-06-14
```

### Acte MOA — Chantier B · GO clôture navigateur · **ACTÉ 2026-06-14**

```text
Chantier B — dorevia_ckreyol_marketone · ckr-marketone-01 · 19.0.19.0.1.
GO clôture navigateur : 6.3a Promotions · 6.3b Kits & Coffrets · SEO portes/shop.
Recette : tests 39/39 OK · proxy HTTP 56/56 OK · aucun écart bloquant.
Arbitrages : N2 OK release 6.3 (chips cohabitants) · P4/P6/K6 acceptés non rejoués.
Rapport : dorevia_ckreyol_marketone/docs/recette/lots/RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md
Indépendant Chantier A · lot contenu légal local · pas de dev complémentaire.
Commit docs : en attente acte MOA dédié.
Validé par : MOA CK · 2026-06-14
```

### Acte MOA — A7 mise sous Git · **DOC VALIDÉE · GO A7 NON SIGNÉ · 2026-06-14**

```text
Proposition A7 acceptée comme base documentaire (PROPOSITION_A7_MISE_SOUS_GIT_MODULES_CK.md).
GO A7 explicite : NON SIGNÉ.
Traitement A7 : après verdict A1 (header stabilisé ou corrections A1 tranchées).
Aucun commit modules CK maquette sans acte MOA A7.
Validé par : MOA CK · 2026-06-14
```

### Acte MOA — recette écran Phase 10 · **ACTÉ 2026-06-14**

```text
Recette MOA écran Phase 10 ouverte — sans Dev.
Priorité §2 header / menu / branding CK.
GO exécution Dev §5undecies : NON SIGNÉ — interdit tant qu'aucune correction explicitement actée.
Gouvernance : pas refonte · pas nouvelle feature · split thème/contenu non rouvert.
Si corrections nécessaires post-recette → GO exécution §5undecies ciblé et limité.
Ensuite : checklist §9 · contrôles transversaux §3.
Validé par : MOA CK · 2026-06-14
```

### Acte MOA — GO préparation §5undecies · **ACTÉ 2026-06-14**

```text
GO PRÉPARATION PHASE 10 — Recette globale go-live CK V1.2.x
Dossier : RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md
Grille header/menu P0 · critères bloquants/non bloquants · modèle GO exécution §5undecies
Exécution Dev : INTERDITE
Exécution recette MOA : en attente
Validé par : MOA CK · 2026-06-14
```

### Acte MOA attendu — exécution recette Phase 10

```text
GO recette MOA Phase 10 (sans Dev) — parcours grille §2–§9 du dossier recette.
GO exécution Dev §5undecies : uniquement si correction header/menu ou autre dette
explicitement actée MOA (modèle §8 dossier recette).
Verdict go-live V1 : acte MOA final distinct après recette Phase 10.
```

---

## 6. Synthèse MOA

Nous validons une **V1 Odoo maîtrisée**, issue de la maquette CK V1.2.x, traduite **progressivement**.

```text
Maquette validée ≠ reprise intégrale HTML.
Reprise Odoo = traduction bloc par bloc, avec arbitrage MOA.
```

---

## 7. Documents liés

| Document | Rôle |
|----------|------|
| [`RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md`](./RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md) | Vérification CE instance · prérequis §5 |
| [`RECETTE_QA_PHASE1_HEADER_FOOTER_CK_V1.md`](./RECETTE_QA_PHASE1_HEADER_FOOTER_CK_V1.md) | Recette Phase 1 · prérequis §5bis |
| [`RECETTE_QA_PHASE2_HOME_SOBER_CK_V1.md`](./RECETTE_QA_PHASE2_HOME_SOBER_CK_V1.md) | Recette Phase 2 · Q1 §5ter |
| [`RECETTE_QA_PHASE3_SHOP_CK_V1.md`](./RECETTE_QA_PHASE3_SHOP_CK_V1.md) | Recette Phase 3 · clôturée |
| [`RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md`](./RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md) | Recette Phase 4 · clôturée |
| [`RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md`](./RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md) | Recette Phase 5 · clôturée |
| [`RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md`](./RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md) | Recette Phase 6 · clôturée |
| [`RECETTE_QA_PHASE7_FICHE_PRODUCTEUR_CK_V1.md`](./RECETTE_QA_PHASE7_FICHE_PRODUCTEUR_CK_V1.md) | Recette Phase 7 · §5octies · clôturée OK partiel MOA |
| [`RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md`](./RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md) | Recette Phase 8 · §5nonies · clôturée OK partiel MOA |
| [`RECETTE_QA_PHASE9_NEWSLETTER_CK_V1.md`](./RECETTE_QA_PHASE9_NEWSLETTER_CK_V1.md) | Recette Phase 9 · clôturée OK partiel MOA · 2026-06-14 |
| [`RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md`](./RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md) | Recette Phase 10 · dossier go-live · §5undecies |
| [`note_reference_bloc_double_pro_newsletter_ck.md`](./note_reference_bloc_double_pro_newsletter_ck.md) | Copy · emplacements dual Pro/newsletter · M9 |
| [`COMPOSITION_RECETTES_V1_2.md`](./COMPOSITION_RECETTES_V1_2.md) | Composition page `/recettes` · M2 |
| [`COMPOSITION_PROFESSIONNELS_V1_2.md`](./COMPOSITION_PROFESSIONNELS_V1_2.md) | Capital instance page Pro |
| [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) | Dictionnaire Maquette ↔ Odoo · intégration |
| [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) | Séquence · tickets · mapping par phase |
| [`ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md`](./ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md) | Arbitrage détaillé page × bloc |
| [`LIVRAISON_MOA_MAQUETTE_CK_V1_2_X.md`](./LIVRAISON_MOA_MAQUETTE_CK_V1_2_X.md) | Livraison maquette |
| [`note_05.md`](../../cadrage/note_05.md) | Doctrine · séquence opérationnelle |
| [`note_reference_header_mega_menu_decouverte_ck_v1.md`](./note_reference_header_mega_menu_decouverte_ck_v1.md) | Header · mega-menu Découvrir · CE natif |

---

*Décision MOA GO reprise Odoo V1 — Phases 1–9 clôturées OK partiel MOA · Phase 10 dossier recette préparé · 2026-06-14.*
