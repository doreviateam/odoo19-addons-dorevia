# Séquence reprise Odoo V1 — CK V1.2.x

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Décisions MOA** | [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) — M1–M9 + **H1** actés |
| **Arbitrage** | [`ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md`](./ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md) |
| **Maquette source** | [`artifact/`](./artifact/) |
| **Instance cible** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Guide intégration** | [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) |
| **Recette QA CE** | [`RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md`](./RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md) |
| **Date** | 2026-06-13 |
| **Statut** | **Phases 1–8 clôturées · Phase 9 GO §5decies acté · Dev livrée · recette QA remplie** |

```text
Phases 1–6 : clôturées
Phase 7 : CLÔTURÉE OK partiel MOA · 2026-06-14
Phase 8 : CLÔTURÉE OK partiel MOA · 2026-06-14
Phase 9 : GO §5decies ACTÉ · Dev livrée · gate OK
Phase 10+ : SUSPENDUES
```

> Traduction **bloc par bloc · par paliers** · recette MOA/QA à chaque phase · pas de reprise intégrale du prototype HTML.

---

## 0bis. GO par palier (MOA · 2026-06-13)

| Palier | Statut GO | Condition passage |
|--------|-----------|-------------------|
| **Phase 1** | ✅ **OK QA acté MOA** | Clôturée 2026-06-13 |
| **Phase 2** | ✅ **OK partiel QA** | Recette MOA 2026-06-13 · §6.0 |
| **Phase 3** | ✅ **Clôturée · gate OK** | [`RECETTE_QA_PHASE3_SHOP_CK_V1.md`](./RECETTE_QA_PHASE3_SHOP_CK_V1.md) · [`ck_phase3_ci.sh`](./scripts/ck_phase3_ci.sh) |
| **Phase 4** | ✅ **Clôturée OK partiel MOA** | [`RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md`](./RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md) |
| **Phase 5** | ✅ **Clôturée OK partiel MOA** | [`RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md`](./RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md) |
| **Phase 6** | ✅ **Clôturée OK MOA** | [`RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md`](./RECETTE_QA_PHASE6_CONTACT_A_PROPOS_CK_V1.md) |
| **Phase 7** | ✅ **Clôturée OK partiel MOA** | [`RECETTE_QA_PHASE7_FICHE_PRODUCTEUR_CK_V1.md`](./RECETTE_QA_PHASE7_FICHE_PRODUCTEUR_CK_V1.md) |
| **Phase 8** | ✅ **Clôturée OK partiel MOA** | [`RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md`](./RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md) · [`ck_phase8_ci.sh`](./scripts/ck_phase8_ci.sh) |
| **Phase 9** | ⏸ **GO acté · Dev livrée · triptyque OK** | [`RECETTE_QA_PHASE9_NEWSLETTER_CK_V1.md`](./RECETTE_QA_PHASE9_NEWSLETTER_CK_V1.md) · [`ck_phase9_ci.sh`](./scripts/ck_phase9_ci.sh) · clôture MOA en attente |

**Recette Phase 1** (avant GO Phase 2) :

- Desktop 1280 px · mobile 390 px
- Navigation header · footer · menu Pro
- Liens BO valides · pas de 404
- Non-régression `/shop` · `/professionnels` · panier
- Verdict MOA/QA explicite

Dictionnaire bloc par bloc : [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md)

---

## 0. Règles de traduction (M7)

Pour chaque bloc, choisir **un seul** levier Odoo :

| Levier | Usage |
|--------|--------|
| Odoo standard | Shop · fiche · panier · contact |
| Snippet natif | `s_title` · `s_features` · Dynamic Products |
| Snippet CK thème | `s_ck_hero` · `s_ck_reassurance` · `s_ck_pro_banner` · `s_ck_dual_engage` (à créer si retenu) |
| Page CMS | À propos · producteur · recettes |
| Configuration BO | Menu · footer · catégories |
| Champ produit | Description · attributs origine |
| Catégorie / attribut | Collections · origines |
| **Réserve / différé** | Filtres avancés · blog · annuaire |

---

## 1. Capital instance conservé (Phase 0)

Ne pas annuler — consolider à la reprise :

| Élément | Statut instance | Action reprise |
|---------|-----------------|----------------|
| `/professionnels` | ✅ Composé | Consolidation · recette CRM |
| Menu Professionnels | ✅ | Vérifier liens |
| Header marchand | ✅ Partiel | Aligner maquette V1.2.x |
| Hero `s_ck_hero` | ✅ Amorce | Réaligner copy · visuels |
| Routes `/shop` | ✅ | Non-régression |

Références : [`COMPOSITION_PROFESSIONNELS_V1_2.md`](./COMPOSITION_PROFESSIONNELS_V1_2.md) · [`COMPOSITION_HEADER_V1_2.md`](./COMPOSITION_HEADER_V1_2.md)

---

## 2. Séquence d’exécution V1 — par paliers

### Phase 1 — Transversal · configuration BO · **LIVRÉ DEV (2026-06-13)**

| # | Bloc | Maquette | Odoo | Snippet / composant | M | Complexité | Statut |
|---|------|----------|------|---------------------|---|------------|--------|
| 1.1 | Header — **3 entrées** Phase 1 | Toutes pages | Configuration BO | Boutique · Découvrir · Pro | **H1** · M6 | Faible | ✅ **OK QA** |
| 1.1b | Mega-menu **Découvrir** | Maquette nav | `is_mega_menu` + `mega_menu_content` | Épicerie créole | **H1** · M4 | Faible | ✅ Livré · Packs différé (0 produit) |
| 1.1c | Entrée **Producteurs** | Maquette nav | Lien simple | — | **H1** · M1 | — | ⏸ Phase 7 · pas CMS |
| 1.1d | **Professionnels** lien direct | Maquette nav | `/professionnels` | Lien menu BO | **H1** | Faible | ✅ Livré |
| 1.2 | Footer 4 col | Toutes pages | Menus footer BO | `website.footer_custom` | M6 | Faible | ✅ Livré |
| 1.3 | Copy réassurance | Accueil · shop | Texte BO | `s_ck_reassurance` | **M5** | Faible | Préparer copy · valider avant go-live |
| 1.4 | Signal Pro menu | Toutes pages | Page CMS | `/professionnels` · menu BO | M6 | Faible | QA CE OK · consolidation |

**Gate Phase 1 → 2** : recette MOA/QA Phase 1 validée · cf. §0bis.

**Gate liens mega-menu Phase 1** (QA Codex · matrice §2bis note H1) :

```text
Mega initial : **Épicerie créole uniquement** (URL BO confirmée) — **Packs & découvertes différé** (0 produit)
Exclure : /recettes · /a-propos · Manioc · Incontournables · Nouveautés tant que BO absent
Producteurs : lien simple uniquement si cible CMS réelle
```

---

### Phase 2 — Home sobre · **OK PARTIEL QA**

| # | Bloc | Maquette | Odoo | Snippet / composant | M | Complexité |
|---|------|----------|------|---------------------|---|------------|
| 2.1 | Hero | `index.html` | Snippet CK | `s_ck_hero` | M6 | Faible |
| 2.2 | Réassurance | `index.html` | Snippet CK | `s_ck_reassurance` | M5 · M6 | Faible |
| 2.3 | Produits vedettes | `index.html` | Grille SSR stable | `.ck-featured-products__grid--stable` · 5 cartes SSR · **pas Dynamic Products / carousel** | M6 | Faible |
| 2.4 | Catégories ×3 | `index.html` | Catégories e-commerce | `s_ck_category_links` | **M4** | Moyenne — **si BO prêtes** |
| 2.5 | Bloc dual Pro | `index.html` | Snippet CK / CMS | `s_ck_dual_engage` ou Pro seul | **M9** | Moyenne |
| 2.6 | Newsletter | `index.html` | Mass mailing | Subscribe natif | **M9** | Moyenne — **si simple · sinon différer** |

**Exclu V1 home** : éditorial long · coffret si produit absent.

Ordre mobile : hero → réassurance → produits → catégories (si M4) → dual Pro → footer.

---

### Phase 3 — Commerce natif · **✅ CLÔTURÉE OK partiel maîtrisé · gate portable OK · 2026-06-13**

| # | Bloc | Maquette | Odoo | Snippet / composant | M | Complexité |
|---|------|----------|------|---------------------|---|------------|
| 3.1 | Shop `/shop` | `shop.html` | `website_sale` natif | Grille native · thème CK | M6 · M3 | Faible |
| 3.2 | Catégorie principale | `categorie.html` | `product.public.category` | Header catégorie CMS optionnel | M6 | Faible |
| 3.3 | Attributs origine | Shop · fiche | Attributs produit BO | Tags / attributs | M6 | Moyenne |
| 3.4 | Filtres visuels shop | `shop.html` | — | **Différé** | **M3** | — |

**Gate M3** : pas de filtres AJAX · pas de search custom.

---

### Phase 4 — Fiche produit · **✅ CLÔTURÉE OK partiel MOA · 2026-06-13**

| # | Bloc | Maquette | Odoo | Snippet / composant | M | Complexité | Statut |
|---|------|----------|------|---------------------|---|------------|--------|
| 4.1 | Galerie + achat | `fiche-produit.html` | `website_sale` natif | Fiche native · `ck-product-page` | M6 | Faible | ✅ |
| 4.2 | Origine & usage · conservation | `fiche-produit.html` | Champ produit BO | Description · bootstrap BO | M6 | Faible | ✅ bootstrap |
| 4.3 | Bloc producteur mini | `fiche-produit.html` | Lien CMS | → fiche producteur M1 **si cible réelle** | **M1** | Faible | ⏸ différé M1 |
| 4.4 | Signal B2B | `fiche-produit.html` | Snippet CK / lien | `/professionnels` · `ck-product-pro-signal` | M6 | Faible | ✅ |
| 4.5 | Associations · recette inline | `fiche-produit.html` | — | **Différé** | M2 · M6 | — | 🚫 |

**Gate QA Phase 4** (triptyque — cf. recette) :

```text
1. test-tags dorevia_ck_theme_phase4
2. ck_phase4_ci.sh (smoke curl)
3. Playwright UX séparé (hors gate)
```

**Garde-fous** : pas panier/checkout custom · pas cross-sell · home/shop/header intacts.

**Dev Phase 4 : CLÔTURÉ** · gate [`ck_phase4_ci.sh`](./scripts/ck_phase4_ci.sh) · verdict MOA OK partiel **2026-06-13**.

---

### Phase 5 — B2B · Professionnels · **✅ CLÔTURÉE OK partiel MOA · 2026-06-13**

| # | Bloc | Maquette | Odoo | Snippet / composant | M | Complexité | Statut |
|---|------|----------|------|---------------------|---|------------|--------|
| 5.1 | Page `/professionnels` | `professionnels.html` | Page CMS bootstrap | `hooks.bootstrap_professionnels_page` · `ck-pro-page` | M6 | Faible | ✅ |
| 5.2 | Double cible B2B | `professionnels.html` | Page CMS | Producteur · fournisseur · distributeur · boutique / CHR | M6 | Faible | ✅ |
| 5.3 | Formulaire CRM | `professionnels.html` | `website_crm` | `#ck-pro-form` · `crm.lead` | M6 | Faible | ✅ soumission OK |
| 5.4 | Doctrine · qualification | `professionnels.html` | Texte CMS | Wording sobre · note qualification | M5 · M6 | Faible | ✅ |
| 5.5 | Bloc dual compact (M9) | `professionnels.html` | — | **Différé Phase 9** | M9 | — | ⏸ Phase 9 |

**Gate QA Phase 5** (triptyque — cf. recette) :

```text
1. test-tags dorevia_ck_theme_phase5
2. ck_phase5_ci.sh (smoke curl)
3. Playwright UX séparé (hors gate)
```

**Garde-fous** :

```text
Pas portail B2B · pas pricing pro public · pas workflow commercial custom
Pas champ CRM custom · qualification via description lead
Home Phase 2 · shop Phase 3 · fiche Phase 4 · header/footer Phase 1 : inchangés
```

**Dev Phase 5 : CLÔTURÉ** · gate [`ck_phase5_ci.sh`](./scripts/ck_phase5_ci.sh) · verdict MOA OK partiel **2026-06-13**.

---

### Phase 6 — Contact + À propos · **✅ CLÔTURÉE OK MOA · 2026-06-13**

| # | Bloc | Maquette | Odoo | Snippet / composant | M | Complexité | Statut |
|---|------|----------|------|---------------------|---|------------|--------|
| 6.1 | Contact `/contactus` | `contact.html` | Odoo standard | `ck-contact-page` · `mail.mail` · retrait O1 | M6 | Faible | ✅ |
| 6.2 | Parcours contact | `contact.html` | Page CMS | Question produit · général · renvoi Pro | M6 | Faible | ✅ |
| 6.3 | À propos `/a-propos` | `a-propos.html` | Page CMS bootstrap | `ck-about-page` · blocs texte · `s_features` | M6 | Faible | ✅ |
| 6.4 | Présentation CK | `a-propos.html` | Page CMS | Mission · confiance · sélection · logistique | M5 · M6 | Faible | ✅ |
| 6.5 | Liens cohérents | `a-propos.html` · `contact.html` | Liens CMS | `/shop` · `/professionnels` · `/contactus` | M6 | Faible | ✅ |
| 6.6 | Bloc dual contact (M9) | `contact.html` | — | **Différé Phase 9** | M9 | — | ⏸ Phase 9 |

**Gate QA Phase 6** (triptyque — cf. recette) :

```text
1. test-tags dorevia_ck_theme_phase6
2. ck_phase6_ci.sh (smoke curl)
3. Playwright UX séparé (hors gate)
```

**Dev Phase 6 : CLÔTURÉ** · gate [`ck_phase6_ci.sh`](./scripts/ck_phase6_ci.sh) · verdict MOA OK **2026-06-13**.

---

### Phase 7 — Fiche producteur CMS pilote (M1) · **✅ CLÔTURÉE OK partiel MOA · 2026-06-14**

| # | Bloc | Maquette | Odoo | Snippet / composant | M | Complexité | Statut |
|---|------|----------|------|---------------------|---|------------|--------|
| 7.1 | Fiche pilote | `fiche-producteur.html` | Page CMS bootstrap | `/producteur/atelier-hauts-goyaviers` · `ck-producer-page` | **M1** | Moyenne | ✅ |
| 7.2 | Présentation · savoir-faire | `fiche-producteur.html` | Page CMS | Blocs texte | M1 | Faible | ✅ |
| 7.3 | Critères sélection CK | `fiche-producteur.html` | Texte CMS statique | Liste statique | M1 | Faible | ✅ |
| 7.4 | Produits associés | `fiche-producteur.html` | `website_sale` / CMS | Liens BO réels publiés | M1 | Moyenne | ✅ |
| 7.5 | Signal logistique · CTA | `fiche-producteur.html` | Snippet CK + liens CMS | M5 · `/shop` · `/contactus` · `/professionnels` | M5 · M1 | Faible | ✅ |
| 7.6 | Lien fiche produit (4.3) | `fiche-produit.html` | — | **Hors scope Phase 7** | M1 | — | ⏸ Différé |
| 7.7 | Nav Producteurs | Header | — | **Option post-recette MOA** | H1 · M1 | — | ⏸ Non acté |

**Gate QA Phase 7** (triptyque — cf. recette) :

```text
1. test-tags dorevia_ck_theme_phase7 (à créer à l'exécution Dev)
2. ck_phase7_ci.sh (à créer à l'exécution Dev)
3. Playwright UX séparé (hors gate)
```

**Garde-fous M1** :

```text
1 fiche pilote · pas annuaire · pas portail · pas workflow fournisseur · pas scoring auto
Pas modification home · shop · fiche produit · contact · à propos · header/footer
Wording M5 · pas sur-promesse logistique
```

**Dev Phase 7 : CLÔTURÉ** · gate [`ck_phase7_ci.sh`](./scripts/ck_phase7_ci.sh) · **OK partiel MOA 2026-06-14** · réserve header transversale.

---

### Phase 8 — Recettes statiques (M2) · **CLÔTURÉE OK partiel MOA · 2026-06-14**

| # | Bloc | Maquette | Odoo | Snippet / composant | M | Complexité |
|---|------|----------|------|---------------------|---|------------|
| 8.1 | Page `/recettes` | `recettes.html` | Page CMS · `ck-recipes-page` | Hero · grille 6 cartes · `website.layout` | **M2** | Moyenne |

**Garde-fou M2** : pas blog · pas commentaires · pas contribution utilisateur.

**Docs** : [`COMPOSITION_RECETTES_V1_2.md`](./COMPOSITION_RECETTES_V1_2.md) · [`RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md`](./RECETTE_QA_PHASE8_RECETTES_STATIQUES_CK_V1.md) · [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) §5nonies.

**Dev Phase 8 : CLÔTURÉ** · gate [`ck_phase8_ci.sh`](./scripts/ck_phase8_ci.sh) · **OK partiel MOA 2026-06-14** · réserve header transversale.

---

### Phase 9 — Newsletter M9 simple · **GO ACTÉ · Dev livrée · 2026-06-14**

| # | Bloc | Maquette | Odoo | Snippet / composant | M | Statut |
|---|------|----------|------|---------------------|---|--------|
| 9.1 | Mailing list BO | — | `mailing.list` · `Newsletter CK` | Bootstrap hooks | **M9** | ✅ |
| 9.2 | Contact — dual compact | `contact.html` | `/contactus` | `s_newsletter_subscribe_form` | **M9** | ✅ |
| 9.3 | Pro — dual compact | `professionnels.html` | `/professionnels` | `#ck-pro-form` | **M9** | ✅ |
| 9.4 | Subscribe · RGPD | — | `/website_mass_mailing/subscribe` | Snippet natif | **M9** | ✅ |

### Phase 10 — Recette globale go-live · **DOSSIER PRÉPARÉ**

> **Doctrine MOA · 2026-06-14** : Phase 10 = recette finale go-live · **pas nouvelle feature**. Dev interdit sans acte MOA §5undecies exécution. Focus P0 : **header / menu / branding CK**.

| # | Action | Document |
|---|--------|----------|
| 10.0 | **Dossier recette Phase 10** | [`RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md`](./RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md) |
| 10.1 | Recette composition CMS | [`recette_qa_composition_cms_ck_01.md`](../recette_qa_composition_cms_ck_01.md) |
| 10.2 | Mobile 390 px | Dossier recette §3.1 · toutes pages Phases 1–9 |
| 10.3 | **Header / menu / branding** | **P0** · Dossier recette §2 |
| 10.4 | Footer / mentions | Dossier recette §3.2 |
| 10.5 | Liens morts · routes | Dossier recette §3.3 |
| 10.6 | Copy M5 | Dossier recette §3.4 |
| 10.7 | Checkout / panier | Dossier recette §3.5 |
| 10.8 | Newsletter · formulaires | Dossier recette §3.6–3.7 |
| 10.9 | Assets / cache | Dossier recette §3.8 |
| 10.10 | Non-régression Phases 1–9 | Gates · Dossier recette §3.9 |
| 10.11 | Verdict MOA go-live | Dossier recette §9 · acte final distinct |

**Dev Phase 9 : CLÔTURÉE OK partiel MOA** · **2026-06-14**.

---

## 3. Matrice décisions → phases

| Décision | Impact séquence |
|----------|-----------------|
| M1 | Phase 7 · lien Phase 4.3 |
| M2 | Phase 8 |
| M3 | Phase 3.4 exclue |
| M4 | Phase 2.4 conditionnelle |
| M5 | Gate Phase 1.3 · Phase 10.3 |
| M6 | Périmètre entier §2 decision |
| M7 | Méthode §0 |
| M8 | Ce document = préparation · exécution §5 |
| M9 | Phases 2.5–2.6 · 5.5 · 6.6 · 9 |
| **H1** | Phases 1.1–1.1d · header + mega Découvrir |

---

## 4. Hors scope V1 — rappel

```text
Reprise intégrale prototype HTML
Filtres AJAX · search custom · catalogue parallèle
Annuaire producteurs · portail · espace connecté
Blog · forum · communauté
Cross-sell avancé · associations fiche
Checkout pro · pricing B2B public
Automation marketing · tunnel newsletter complexe
```

---

## 5. Prochaine étape

| # | Action | Responsable | Statut |
|---|--------|-------------|--------|
| 1 | Dictionnaire CE validé MOA | MOA | ✅ |
| 2 | Acter §5 GO exécution Phase 1 | MOA | ✅ **Acté 2026-06-13** |
| 3 | Exécuter Phase 1 — header + footer BO | Dev | ✅ **Livré 2026-06-13** |
| 4 | Recette MOA/QA Phase 1 | MOA / QA | ✅ **OK QA** · §6.0 |
| 5 | Acter GO MOA Phase 2 | MOA | ✅ **Acté 2026-06-13** · §5bis |
| 6 | Exécuter Phase 2 — Home sobre | Dev | ✅ **Livré 2026-06-13** |
| 7 | Recette MOA/QA Phase 2 | MOA / QA | ✅ **OK partiel** · §6.0 |
| 8 | Contrôle visuel MOA Q1 (vedettes) | MOA | ❌ **Non levée** · 2026-06-13 |
| 8bis | Correction Dev Q1 — vedettes DOM | Dev | ✅ §6bis |
| 8ter | Correction Dev Q1 — produit test QA | Dev | ✅ §6ter |
| 9 | Recontrôle MOA Q1 | MOA | ▶ En attente |
| 10 | Levée Q1 + acte GO Phase 3 | MOA | ✅ **2026-06-13** · §5ter |
| 11 | Exécution Phase 3 Dev | Dev | ✅ **Clôturée OK partiel maîtrisé** · gate OK |
| 12 | Recette MOA/QA Phase 3 | MOA / QA | ✅ **Clôturée** |
| 13 | Préparation acte GO Phase 4 | MOA / Dev | ✅ **§5quinquies acté** |
| 14 | Exécution Phase 4 Dev | Dev | ✅ **Clôturée OK partiel MOA** |
| 15 | Recette MOA/QA Phase 4 | MOA / QA | ✅ **OK partiel MOA** · 2026-06-13 |
| 16 | Préparation dossier Phase 5 | MOA / Dev | ✅ **§5sexies acté** |
| 17 | Exécution Phase 5 Dev | Dev | ✅ **Clôturée OK partiel MOA** |
| 18 | Recette MOA/QA Phase 5 | MOA / QA | ✅ **OK partiel MOA** · 2026-06-13 |
| 19 | Préparation dossier Phase 6 | MOA / Dev | ✅ **§5septies acté** · 2026-06-13 |
| 20 | Exécution Phase 6 Dev | Dev | ✅ **Clôturée OK MOA** |
| 21 | Recette MOA/QA Phase 6 | MOA / QA | ✅ **OK MOA** · 2026-06-13 |
| 22 | Préparation dossier Phase 7 | MOA / Dev | ✅ **§5octies acté** · 2026-06-13 |
| 23 | Exécution Phase 7 Dev | Dev | ✅ **Livrée** · gate OK |
| — | Recette MOA/QA Phase 7 | MOA / QA | ✅ **OK partiel MOA** · 2026-06-14 |
| 24 | Préparation dossier Phase 8 | MOA / Dev | ✅ **§5nonies acté** · 2026-06-14 |
| 25 | Exécution Phase 8 Dev | Dev | ✅ **Livrée** · `19.0.1.7.0` · gate OK |
| — | Recette MOA/QA Phase 8 | MOA / QA | ✅ **OK partiel MOA** · 2026-06-14 |
| 26 | Préparation dossier Phase 9 | MOA / Dev | ✅ **§5decies · QA documentaire OK** · 2026-06-14 |
| 27 | Acte GO Phase 9 | MOA | ✅ **2026-06-14** |
| 28 | Exécution Phase 9 Dev | Dev | ✅ **Livrée** · `19.0.1.8.0` · gate OK |
| — | Recette MOA/QA Phase 9 | MOA / QA | ☐ **Triptyque OK · clôture en attente** |

---

*Séquence reprise Odoo V1 CK V1.2.x — Phases 1–8 clôturées · Phase 9 Dev livrée · clôture MOA en attente · 2026-06-14.*
