# Recette QA — Phase 2 · Home sobre · CK V1.2.x

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Conteneur** | `sandbox-odoo19-odoo-1` |
| **GO MOA** | [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) §5bis · **Q1 levée §5ter (2026-06-13)** |
| **Séquence** | [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) Phase 2 |
| **Script Dev** | [`scripts/ck_phase2_configure.py`](./scripts/ck_phase2_configure.py) |
| **Date livraison Dev** | 2026-06-13 |
| **Date recette MOA/QA** | 2026-06-13 |
| **Date acte MOA Q1** | **2026-06-13** |
| **Statut** | **✅ Q1 levée (réserve SSR actée) · Phase 3 après acte §5quater** |

```text
Q1 Phase 2 : LEVÉE (2026-06-13) — grille SSR stable · 5 produits CK réels
Réserve SSR actée · carousel / Dynamic Products exclus V1
Phase 3 : envisageable — acte GO distinct §5quater · Dev Phase 3 interdit sans acte
```

> Header HTTP `X-Odoo-Database: dorevia_ck_marketone_01` requis.  
> Après exécution du script : **redémarrer Odoo** (cache HTML `website.page` · 3600 s).

---

## 1. Périmètre livré

| # | Bloc | Snippet / composant | Statut Dev |
|---|------|---------------------|------------|
| 2.1 | Hero | `s_ck_hero` | ✅ Conservé · copy CK existante |
| 2.2 | Réassurance | `s_ck_reassurance` | ✅ Copy M5 ajustée |
| 2.3 | Produits vedettes — **5 produits CK réels en V1, cible 6 différée** | `s_ck_featured_products` + grille SSR `.ck-featured-products__grid--stable` | ✅ 5 produits CK · rendu serveur · **pas Dynamic Products / carousel V1** |
| 2.4 | Catégories | `s_ck_category_links` | ✅ **2 liens BO 200** (gate M4) |
| 2.5 | Dual Pro / newsletter | Bloc CMS 2 col + `s_newsletter_subscribe_form` | ✅ Pro prioritaire · list_id=1 |
| 2.6 | Bandeau Pro | `s_ck_pro_banner` | ✅ Lien `/professionnels` |

**Exclus respectés** : pas d’éditorial long · pas de coffret/packs · header/footer/mega **non modifiés** · `dorevia_ck_theme` **non modifié**.

---

## 2. Ordre des blocs

### Desktop `/`

```text
Hero → Réassurance → Produits vedettes → Catégories → Dual Pro/newsletter → Bandeau Pro → Footer (Phase 1)
```

### Mobile 390 px (Playwright · pré-recette Dev)

| # | Critère | Attendu | Résultat Dev |
|---|---------|---------|--------------|
| M1 | `scrollWidth = 390` · pas d’overflow | 390/390 | ✅ |
| M2 | Ordre blocs | hero → réassurance → vedettes → catégories → dual → pro | ✅ |
| M3 | Produits vedettes | **5 cartes** CK réelles · liens `/shop/…` 200 | ✅ |
| M4 | Catégories | 2 pills · liens 200 | ✅ |
| M5 | Signal Pro | CTA `/professionnels` | ✅ |
| M6 | Non-régression Phase 1 | Header · footer | ✅ |

---

## 3. Contrôles desktop (pré-recette Dev · 2026-06-13)

| Contrôle | Attendu | Résultat |
|----------|---------|----------|
| `/` HTTP 200 | Page home composée | ✅ |
| Hero | `s_ck_hero` · CTA `/shop` | ✅ |
| Réassurance M5 | 4 items · promesses sobres | ✅ |
| Vedettes | Grille SSR `.ck-featured-products__grid--stable` · **5 cartes** HTML source | ✅ |
| Produits BO | **5 publiés** CK réels · liens fiche valides | ✅ |
| Catégories M4 | Épicerie créole · Maison & bien-être → 200 | ✅ |
| Dual Pro | Colonne Pro + CTA `/professionnels` | ✅ |
| Newsletter M9 | Subscribe natif · `data-list-id="1"` | ✅ |
| Bandeau Pro | `s_ck_pro_banner` | ✅ |

---

## 4. Non-régression Phase 1

| Contrôle | Attendu | Résultat |
|----------|---------|----------|
| Header nav | Boutique · Découvrir · Professionnels | ✅ |
| Mega Découvrir | Épicerie créole seule | ✅ |
| Footer 4 col | C-Kreyol · Boutique · Découvrir/Contact · CK | ✅ |
| Q1 téléphone fictif header/drawer | 0 occurrence | ✅ |
| Q2 mention Odoo | Absente | ✅ |
| `/shop` · `/shop/cart` · `/professionnels` | 200 | ✅ |

---

## 5. Réserves classées (non bloquantes si actées MOA)

| # | Point | Statut |
|---|-------|--------|
| R-M4 | Catégories ×3 : **2/3 seulement** — Artisanat (0 produit · 404) · Packs (404) exclus | Gate M4 |
| R-M9 | Newsletter : subscribe natif · recette RGPD / double opt-in à compléter avant go-live | M9 |
| R1–R4 | Producteurs nav · Packs mega · footer Découvrir · mentions légales | Phase 1 / 6–8 |
| O1 | Démo Odoo corps `/contactus` | Phase 6 |

---

## 6. Verdict QA — historique

### 6.0 · Recette MOA — 2026-06-13 · **OK partiel**

| Champ | Valeur |
|-------|--------|
| **Responsable QA** | MOA CK |
| **Verdict Phase 2** | ☐ OK · ☑ **OK partiel** · ☐ KO |
| **Recommandation** | **Phase 2 acceptée avec réserves** · GO Phase 3 **conditionnel** |
| **GO Phase 3** | ☐ Autorisé · ☑ **En attente acte §5quater** — Q1 ✅ levée |

**Gate Q1 — contrôle visuel MOA en cours** *(desktop + mobile 390 px)* :

| Point | Attendu |
|-------|---------|
| Cartes vedettes | **5 visibles** (catalogue BO actuel · cible 6 différée) |
| Rendu | Propre · intégration home OK |
| Overflow | Aucun (390 px) |
| Liens produits | Cohérents · fiches 200 |
| Prix / titres | Lisibles |
| Non-régression Phase 1 | Header · mega · footer inchangés |

```text
Si conforme → MOA confirme levée Q1 → acte GO Phase 3 dans decision_moa_go_reprise_odoo_v1.md
Phase 3 Dev : NE PAS DÉMARRER avant acte MOA explicite
```

| Contrôle | Verdict |
|----------|---------|
| Home publiée `/` · page générique dépubliée | ✅ OK |
| Ordre blocs serveur | ✅ OK |
| Copy M5 réassurance | ✅ OK |
| Catégories M4 (2 liens 200) | ✅ OK |
| Exclusion Artisanat / Packs | ✅ OK |
| Non-régression Phase 1 | ✅ OK |
| Routes HTTP | ✅ OK |
| **Q1** Vedettes dynamiques | ✅ **Levée** · acte MOA §5ter · **2026-06-13** · réserve SSR |

**Verdict contrôle visuel MOA Q1 — relance (2026-06-13)** :

```text
Q1 — Produits vedettes dynamiques : NON LEVÉE
Motif 1 : contrôle visuel navigateur intégré non fiabilisé (blocage/timeout)
Motif 2 : flux dynamique incluait « Recette QA CK — Produit test » en vedettes
Motif 3 : instabilité ponctuelle port localhost:18079 (refus connexion intermittents)
Conséquence : Phase 3 suspendue
```

**Constats MOA positifs (relance)** : `s_ck_featured_products` + `s_dynamic_snippet_products` présents · `/website/snippet/filters` → 6 produits (avant correction) · liens 200 · overflow OK.

**Réserves actées** :

| # | Point | Statut |
|---|-------|--------|
| **Q1** | Vedettes grille SSR · 5 produits CK | ✅ **Levée §5ter** · réserve SSR actée |
| **Q1b** | Catalogue BO : **5 produits publiés** en V1 · **6e produit différé** jusqu’à disponibilité catalogue | Gate catalogue · non bloquant levée Q1 |
| **Q2** | Newsletter M9 go-live | Classée |

---

### 6ter. Correction Dev Q1 — produit test QA (2026-06-13)

| Action | Détail |
|--------|--------|
| Dépublier `Recette QA CK — Produit test` | `product.template` id 2 · `website_published=False` |
| Ajuster vedettes | `data-number-of-records="5"` (catalogue BO réel) |
| Script | [`scripts/ck_q1_cleanup_test_product.py`](./scripts/ck_q1_cleanup_test_product.py) |
| Restart Odoo | `docker restart sandbox-odoo19-odoo-1` · flush cache HTML |

**Produits vedettes attendus (5)** :

| Produit | URL |
|---------|-----|
| Savon vétiver | `/shop/savon-vetiver-7` |
| Manio Crackers sucré | `/shop/manio-crackers-sucre-6` |
| Manio Crackers salé | `/shop/manio-crackers-sale-5` |
| Galettes de manioc | `/shop/galettes-de-manioc-4` |
| Confiture de goyave | `/shop/confiture-de-goyave-3` |

**Exclus** : `Recette QA CK — Produit test` · tout produit non publié BO.

**Pré-recette Dev post-§6ter** *(Playwright · `?db=dorevia_ck_marketone_01`)* :

| Viewport | Cartes | Produit test absent | Overflow |
|----------|--------|---------------------|----------|
| Desktop 1280 px | **5** | ✅ | — |
| Mobile 390 px | **5** | ✅ | 390/390 |

> **Note port 18079** : en cas de refus connexion, attendre ~15 s post-`docker restart` puis réessayer. Conteneur `sandbox-odoo19-odoo-1` répond en interne sur `:8069`.

---

### 6quater. Correction Dev Q1 — rendu serveur vedettes SSR (2026-06-13)

| Champ | Valeur |
|-------|--------|
| **Diagnostic post-§6ter** | Catalogue OK · endpoint `/website/snippet/filters` → 5 produits CK · mais **0 carte visible** côté navigateur MOA — le dynamic snippet ne remplit `.dynamic_snippet_template` qu’après hydratation JS ; HTML source servi = grille vide |
| **Cause racine** | Dépendance au RPC frontend `website_sale.dynamic_snippet_products` · contenu absent du HTML initial · échec silencieux si session/DB/assets |
| **Action** | Remplacement du bloc `s_dynamic_snippet_products` par **grille SSR** pré-rendue dans `arch_db` view 1001 · cartes visibles **sans JavaScript** |
| **Script** | [`scripts/ck_q1_ssr_featured.py`](./scripts/ck_q1_ssr_featured.py) |
| **Post-action** | `docker restart sandbox-odoo19-odoo-1` |

**Structure DOM post-SSR** :

| Élément | Sélecteur | Attendu |
|---------|-----------|---------|
| Titre | `.s_ck_featured_products h2` | « Produits vedettes » |
| Grille SSR | `.ck-featured-products__grid--stable` | Présent · **5 cartes** dans le HTML source |
| Cartes | `.o_carousel_product_card` | **5** |
| Dynamic JS | `.s_dynamic_snippet_products` | **Absent** (volontaire) |

**Pré-recette Dev post-§6quater** *(curl + Playwright · DB `dorevia_ck_marketone_01`)* :

| Contrôle | Résultat |
|----------|----------|
| HTML source `curl /` | **5** × `o_carousel_product_card` · pas de `s_dynamic_snippet_products` |
| Desktop 1280 px · 500 ms | **5 cartes** · **5 liens** `/shop/…` |
| Mobile 390 px | **5 cartes** · overflow 390/390 |
| MOA-like (sélecteur DB → `/`) | **5 cartes** · titre visible |

**Accès recette MOA** : préférer **sélecteur de base** puis `/` — l’URL seule `/?db=…` peut rediriger vers `/web/login` sans session.

> **Recontrôle MOA Q1 requis** — gate Phase 3.

---

### 6quinquies. Anomalie MOA Q1 — layout shift carousel · Produits vedettes (2026-06-13)

**Verdict MOA recontrôle post-§6quater** :

```text
Q1 — NON LEVÉE
Motif : instabilité de layout au défilement du bloc Produits vedettes (layout shift carousel)
```

#### Formulation anomalie (Dev / MOA)

```text
Anomalie Q1 — Produits vedettes / carousel

Lors du défilement du carousel « Produits vedettes », la home présente un comportement
visuel instable : la page « tremble » ou saute légèrement au fur et à mesure du passage
des produits.

Le problème ne semble pas être uniquement un problème de données catalogue : les produits
existent, mais le rendu dynamique du bloc provoque une instabilité visuelle côté navigateur.

Effet observé :
- micro-sauts verticaux ou horizontaux pendant le défilement ;
- impression que la page se recalcule / se repositionne ;
- lecture inconfortable ;
- bloc produits non perçu comme stable ou maîtrisé.

Impact QA :
Q1 non levée.
Le bloc Produits vedettes ne peut pas être validé tant que le carousel provoque ce tremblement.

Attendu :
- carousel stable ;
- hauteur du bloc figée ou maîtrisée ;
- cartes produits de dimensions homogènes ;
- images avec ratio/dimensions constantes ;
- aucune variation de hauteur au changement de slide ;
- aucun scroll horizontal ou recalcul visible de layout ;
- comportement stable desktop et mobile 390 px.
```

**Version courte** :

```text
Le carousel « Produits vedettes » provoque un tremblement / saut de layout pendant son
défilement. Le bloc n’est pas visuellement stable : la hauteur ou le positionnement semble
se recalculer à chaque transition. Q1 non levée tant que le carousel n’est pas stabilisé.
```

**Vocabulaire QA** : *layout shift carousel* · *instabilité de layout au changement de slide* · CLS (Cumulative Layout Shift) sur le bloc vedettes.

#### Contexte technique Dev (post-§6quater)

| Point | État instance `dorevia_ck_marketone_01` |
|-------|----------------------------------------|
| Implémentation actuelle | Grille **SSR statique** (sélecteur recette : `.ck-featured-products__grid--stable`) — **pas de carousel Bootstrap** · pas de `s_dynamic_snippet_products` |
| Classe carte | `o_carousel_product_card` = nommage natif Odoo · **ne signifie pas** qu’un carousel JS est actif |
| Données | 5 produits CK réels · cartes présentes HTML source |

> Si le MOA observe encore un **défilement carousel** : vérifier cache navigateur / redémarrage Odoo post-§6quater · ou recette sur une version antérieure (dynamic snippet carousel).

#### Critères de levée Q1 (complément §6.0)

| # | Critère | Desktop | Mobile 390 px |
|---|---------|---------|---------------|
| L1 | Aucun tremblement / saut layout au défilement | ☐ | ☐ |
| L2 | Hauteur bloc stable (pas de recalcul visible) | ☐ | ☐ |
| L3 | Cartes homogènes · images ratio constant | ☐ | ☐ |
| L4 | Pas de scroll horizontal parasite | ☐ | ☐ |
| L5 | 5 cartes produits CK réels visibles | ☐ | ☐ |

**Suite Dev** : stabiliser le bloc vedettes (grille fixe ou carousel maîtrisé) · ticket CSS/layout si nécessaire · **sans modifier `dorevia_ck_theme` hors ticket dédié**.

---

### 6sexies. Correction Dev Q1 — stabilisation layout vedettes (2026-06-13)

| Champ | Valeur |
|-------|--------|
| **Diagnostic** | Tremblement / layout shift au défilement — causé par `content-visibility: auto` natif Odoo sur `.oe_product_cart` + options hover (`img_hover_zoom_out_light`, `actions_onhover`) |
| **Action CSS** | `dorevia_ck_theme/static/src/scss/website.scss` — bloc `.ck-featured-products__grid` : hauteur figée, ratio image 1:1, désactivation transforms/transitions, boutons toujours visibles |
| **Action HTML** | Scripts SSR : retrait classes instables · ajout `ck-featured-products__grid--stable` · colonnes `align-items-stretch` |
| **Scripts** | [`ck_q1_ssr_featured.py`](./scripts/ck_q1_ssr_featured.py) · [`ck_phase2_configure.py`](./scripts/ck_phase2_configure.py) |
| **Module** | `odoo -u dorevia_ck_theme` + `docker restart sandbox-odoo19-odoo-1` |

**Pré-recette Dev post-§6sexies** :

| Contrôle | Desktop 1280 | Mobile 390 |
|----------|--------------|------------|
| Cartes visibles | **5** | **5** |
| Hauteur grille stable (scroll + hover) | ✅ | ✅ |
| Cartes hauteur homogène | 475 px × 5 | 460 px × 5 |
| Images ratio constant | 373 px | 358 px |
| Overflow horizontal | — | 390/390 |
| Classes instables absentes | pas `img_hover_zoom` · pas `actions_onhover` | idem |
| Carousel JS | absent | absent |

**Script vérif layout** : [`scripts/ck_q1_layout_shift.mjs`](./scripts/ck_q1_layout_shift.mjs) · [`scripts/ck_q1_hover_stability.mjs`](./scripts/ck_q1_hover_stability.mjs)

> **Recontrôle MOA Q1** — parcourir la home lentement (desktop + mobile 390 px) · confirmer absence de tremblement sur le bloc vedettes.

---

### 6septies. Verdict QA Q1 — stabilisation acceptée avec réserve de preuve (2026-06-13)

**Formulation QA recommandée (Dev / MOA)** :

```text
Q1 — Stabilisation acceptée avec réserve de preuve

Le tremblement n’est plus observable, mais il a disparu parce que le comportement initial
a été contourné par suppression / remplacement du carousel dynamique.

La correction stabilise visuellement la home, mais elle ne démontre pas que le carousel
Odoo initial est corrigé.

Conclusion :
- le problème utilisateur immédiat est neutralisé ;
- le risque de tremblement sur ce bloc home est levé dans la solution actuelle ;
- la cause carousel / dynamic snippet n’est pas corrigée en tant que composant réutilisable ;
- toute réintroduction future d’un carousel ou dynamic snippet produits devra repasser
  en recette dédiée.
```

**Version courte** :

```text
Q1 levable sur la home actuelle, car le bloc Produits vedettes est stable.
Mais réserve technique : correction par remplacement du carousel, non par correction du carousel.
```

**Ce qu’il ne faut pas écrire** : « bug carousel corrigé » · « Dynamic Products stabilisé ».

**Ce qu’il faut écrire** : grille SSR stable · risque layout shift neutralisé sur la home V1 · carousel produits **hors périmètre validé**.

#### Gouvernance V1

```text
Phase 3 peut être envisagée uniquement si la MOA accepte que la V1 utilise une grille SSR
stable à la place du carousel.

Le carousel produits / Dynamic Products vedettes reste exclu / interdit en V1 tant qu’il
n’a pas fait l’objet d’une recette spécifique.
```

| Décision MOA | Condition |
|--------------|-----------|
| **Levée Q1 home** | Bloc vedettes stable desktop + mobile 390 px (critères L1–L5 §6quinquies) |
| **Acceptation réserve SSR** | Acte explicite : grille SSR = traduction V1 acceptable (non carousel) |
| **GO Phase 3** | Levée Q1 + acceptation réserve SSR + acte dans `decision_moa_go_reprise_odoo_v1.md` |
| **Carousel / Dynamic Products** | Interdit en V1 sans ticket + recette dédiée |

**Sélecteur DOM officiel recette** : `.ck-featured-products__grid--stable`  
*(classe interne `.ck-featured-products__ssr` — conteneur legacy · ne pas utiliser seule pour le verdict QA)*

**Formulation acte MOA proposée** :

```text
Q1 levée sur la home V1 actuelle, sous réserve acceptée :
le bloc Produits vedettes est validé en grille SSR stable, avec 5 produits CK réels.
Le carousel / Dynamic Products produits reste exclu de la V1 sans ticket et recette dédiée.
```

**Acte à signer** : [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) **§5ter** ✅ acté **2026-06-13** · **§5quater** (GO Phase 3 · en attente).

---

### 6bis. Correction Dev Q1 — vedettes absentes DOM (2026-06-13)

| Champ | Valeur |
|-------|--------|
| **Diagnostic** | Bloc vedettes **absent de `arch_db`** view 1001 — suppression probable sauvegarde Website Builder (contenu imbriqué `oe_structure`) |
| **Action** | Recomposition [`scripts/ck_phase2_configure.py`](./scripts/ck_phase2_configure.py) — **sections sœurs** dans `#wrap` : |
| | 1. `s_ck_featured_products` (titre « Produits vedettes ») |
| | 2. `s_dynamic_snippet_products` (filtre « Nouveaux produits » · 6 enregistrements) |
| **Post-action** | `docker restart sandbox-odoo19-odoo-1` (cache HTML 3600 s) |

**Pré-recette Dev post-correction** *(Playwright · URL MOA `?db=dorevia_ck_marketone_01`)* :

| Viewport | Cartes | Liens fiche | `.s_ck_featured_products` DOM |
|----------|--------|-------------|-------------------------------|
| Desktop 1280 px | **6** | **6** | ✅ |
| Mobile 390 px | **6** | **6** · 390/390 | ✅ |

> **Recontrôle MOA requis** sur [http://localhost:18079/?db=dorevia_ck_marketone_01](http://localhost:18079/?db=dorevia_ck_marketone_01) après redémarrage Odoo.

---

### 6.1 · Contre-vérification Auto — Playwright (2026-06-13) · avant correction Q1

> Première passe Auto — **non reproductible** après perte arch · conservée historique.

| Viewport | Cartes | Note |
|----------|--------|------|
| Desktop / Mobile | 6 | Avant perte bloc en base |

---

### 6.2 · Pré-recette Dev initiale — Auto (2026-06-13)

| Champ | Valeur |
|-------|--------|
| **Verdict initial Dev** | Livré |
| **Suite** | MOA Q1 non levée → correction §6bis |

---

## 7. Prochaine étape

```text
1. ✅ Recette MOA Phase 2 — OK partiel acté
2. ✅ Q1 levée — acte MOA §5ter · 2026-06-13 · réserve SSR actée
3. ✅ Corrections Dev §6bis → §6sexies
4. ▶ Acte MOA §5quater — **préparé** · signature requise avant Dev Phase 3
5. 🚫 Dev Phase 3 — INTERDIT tant que §5quater non acté
6. 🚫 Carousel / Dynamic Products vedettes — interdit V1 sans recette dédiée
```

---

## 8. Documents liés

| Document | Rôle |
|----------|------|
| [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) | §5bis · **§5ter Q1 levée** · §5quater préparé |
| [`RECETTE_QA_PHASE3_SHOP_CK_V1.md`](./RECETTE_QA_PHASE3_SHOP_CK_V1.md) | Recette Phase 3 · §5quater |
| [`RECETTE_QA_PHASE1_HEADER_FOOTER_CK_V1.md`](./RECETTE_QA_PHASE1_HEADER_FOOTER_CK_V1.md) | Non-régression |
| [`note_reference_bloc_double_pro_newsletter_ck.md`](./note_reference_bloc_double_pro_newsletter_ck.md) | Copy dual Pro |
| [`recette_qa_composition_cms_ck_01.md`](../recette_qa_composition_cms_ck_01.md) | Recette historique CMS CK 01 |

---

*Recette QA Phase 2 — Q1 levée §5ter (2026-06-13) · réserve SSR actée · GO Phase 3 §5quater en attente.*
