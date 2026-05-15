# TICKET — Hero Homepage V2 (immersif)

**ID** : `HERO-HOMEPAGE-V2`  
**Date d’ouverture** : 2026-04-24  
**Priorité** : **P1** (bloc au-dessus de la ligne de flottaison ; impact identité perçue).  
**Statut** : **Clôturé — GO MOA** (`HERO-HOMEPAGE-V2` accepté ; recette **`19.0.1.7.11`**, correctif chargement RST **`19.0.1.7.12`**)  
**Exécution : clos** — voir [PV_RECETTE_HERO_HOMEPAGE_V2_CK.md](PV_RECETTE_HERO_HOMEPAGE_V2_CK.md) §8 ; checklists §0 soldées (2026-04-25).  
**Module** : `dorevia_ckreyol_marketplace`  
**Périmètre** : **bloc Hero uniquement** (snippet / template / SCSS hero — pas le reste de la homepage sauf non-régression layout).

**Décision MOA** : [DECISION_HERO_HOMEPAGE_V2.md](../mvp_02/DECISION_HERO_HOMEPAGE_V2.md) (**Option B** — hero immersif).

**Rattachement** : [TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md](TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md) (appétence / partition) ; coordonner les PR avec **Explorer MVP2** / **sélection produits** si mêmes fichiers assets ou conflits Git sur `ckr_homepage.xml`.

---

## Contexte

Décision MOA validée : **hero immersif (Option B)** — voir [DECISION_HERO_HOMEPAGE_V2.md](../mvp_02/DECISION_HERO_HOMEPAGE_V2.md).  
Cadrage contenu et contraintes visuelles : [1_HOMEPAGE.md](../mvp_02/1_HOMEPAGE.md) §1.

---

## Objectif

Remplacer le hero actuel par un **hero immersif** avec **image produit en fond**, afin de poser immédiatement le **positionnement C-Kreyol** (offre réelle, ton sobre et alimentaire).

---

## Périmètre

### Structure

- Section hero **pleine largeur** ;
- **Image de fond** produit (candidats versionnés : `docs/assets/mvp02_reference_*.png` — inventaire [README du module](../../README.md), **Références visuelles MVP 02** ; intégration finale `static/` ou média BO selon convention du module) ;
- **Overlay léger** pour lisibilité ;
- Texte **aligné à gauche** ;
- **2 CTA** visibles.

### Contenu (gel pour ce ticket)

| Élément | Texte / cible |
|---------|----------------|
| **Titre** | Retrouvez les saveurs et savoir-faire créoles. |
| **Texte** | C-Kreyol sélectionne avec soin des produits issus de territoires où la culture créole est vivante, auprès de producteurs et créateurs de confiance. |
| **CTA principal** | Découvrir la sélection → `/shop` |
| **CTA secondaire** | Explorer les origines → `/origines` (cible doctrinale) — **implémentation MVP2.1** : `/shop?ckr_mode=origin` tant que la porte `/origines` front n'est pas livrée par le ticket `EXPLORER-HOMEPAGE-MVP2` (arbitrage MOA 2026-04-24 : *filtre /shop équivalent* plutôt que lien mort). **Bascule** vers `/origines` à opérer dans la PR Explorer MVP2. |

### Contraintes (MOA)

- Pas de **blur fort** ; pas d’**illustration** ; pas de **style startup** ;
- **Produits visibles** (pas « lavés » par l’overlay) ;
- Ton **sobre**, **crédible**, **alimentaire**.

### Technique (attendu)

- **Modification QWeb** autorisée (périmètre hero) ;
- **Adaptation SCSS** autorisée ;
- **Responsive** desktop / mobile ;
- **Pas de régression** sur header / navigation ni sur les blocs sous le hero (Explorer, etc.).

---

## Hors périmètre

- Animation **complexe** ; **A/B testing** ;
- **Refonte globale** de la homepage (autres blocs, ordre des sections) ;
- Rail **Explorer**, **sélection produits**, **inscription**, **trust** : tickets dédiés.

---

## Critères d’acceptation

- [x] Hero **visible au chargement** sans scroll (above the fold — essentiel lisible sans scroll forcé sur mobile) ;
- [x] **Texte lisible** sur l’image (contraste / overlay) ;
- [x] **CTA cliquables** ; ordre de tabulation et **focus** cohérents ;
- [x] Rendu **cohérent** desktop / mobile / tablette (acceptable) ;
- [x] **Image produit identifiable** (pas effet « maquette » ou « startup ») ;
- [x] **Performance** : image optimisée pour la prod. ;
- [x] **Doctrine** : alignement [PLATEFORME_MARQUE_CK_V1.md](PLATEFORME_MARQUE_CK_V1.md) / [ADR-CKR-005](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005) / [ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007) (CTA boutique & origines).

---

## Recette

- **PV** : [PV_RECETTE_HERO_HOMEPAGE_V2_CK.md](PV_RECETTE_HERO_HOMEPAGE_V2_CK.md) — **verdict final §8** : **GO MOA** (2026-04-24), build **`19.0.1.7.11`** ; **réserve non bloquante** : crop tablette / mobile perfectible ; **feu vert** chantier **2/5** [EXPLORER-HOMEPAGE-MVP2](TICKET_EXPLORER_HOMEPAGE_MVP2.md).
- Validation **visuelle MOA** ;
- Vérification **responsive** ;
- Cohérence avec la **direction CK** (assets + ton) — renvois [BRIEF_VISUEL_HERO_PHASE1.md](../direction/BRIEF_VISUEL_HERO_PHASE1.md), [SPEC_HERO_HOMEPAGE.md](../direction/SPEC_HERO_HOMEPAGE.md) **§7** (mise à jour **dans la PR** code ou commit doc **immédiatement après** merge).

---

## 0. Prêt pour dev — checklist pilotage *(soldée — clos 2026-04-24 / doc 2026-04-25)*

1. [x] **Branche** — intégration hero V2 livrée (versions manifest § statut).
2. [x] **Copy figée** — alignée [1_HOMEPAGE.md](../mvp_02/1_HOMEPAGE.md) §1 ; **GO MOA**.
3. [x] **Image de fond** — asset MVP02 / `static/` ; overlay immersif validé.
4. [x] **CTA** — `/shop` ; `/origines` (parcours portes) ; a11y recettée.
5. [x] **SPEC** — [SPEC_HERO_HOMEPAGE.md](../direction/SPEC_HERO_HOMEPAGE.md) suivi en phase livraison.
6. [x] **`__manifest__.py`** — bumps appliqués (`19.0.1.7.11` +).
7. [x] **Recette** — [PV_RECETTE_HERO_HOMEPAGE_V2_CK.md](PV_RECETTE_HERO_HOMEPAGE_V2_CK.md) **GO MOA** §8.
8. [x] **Instance / relecteur** — recette MOA complétée.

---

## Livrables techniques (synthèse)

| Livrable | Détail |
|----------|--------|
| **QWeb** | Markup hero immersif (fond, overlay, titre, texte, 2 CTA). |
| **SCSS** | Pleine largeur, fond, overlay, alignements, responsive. |
| **A11y** | Contraste, `focus-visible`, structure titres. |

---

## Historique

| Date | Changement |
|------|------------|
| 2026-04-24 | Création — checklist §0 ; critères ; lien décision MVP02 + PV. |
| 2026-04-24 | **Réécriture** — structure Contexte / Objectif / Périmètre (structure, contenu, contraintes, technique) ; hors périmètre ; critères d’acceptation alignés MOA ; recette ; périmètre hero seul (homepage §2–6 gelés ailleurs). |
| 2026-04-24 | **Tests auto + PV pré-rempli** — `tests/test_ckr_hero_homepage.py` (tag `dorevia_ckr_hero`, 5 tests HTTP sur homepage : section immersive, CTA primaire `/shop`, CTA secondaire transitoire `/shop?ckr_mode=origin`, copy titre, non-régression ancre `#explorer-catalogue`) ; enregistré dans `tests/__init__.py`. `PV_RECETTE_HERO_HOMEPAGE_V2_CK.md` pré-rempli (livraison technique §2, grille critères annotée Auto/MOA §4, tests auto §6, arbitrages §7) — captures et verdict en attente recette MOA. Exécution ciblée : `odoo -d <base> --test-enable --stop-after-init --test-tags=dorevia_ckr_hero`. |
| 2026-04-24 15:47 | **Exécution tests auto sandbox** — `sandbox-odoo19-odoo-1` / `tenant_o7`, port test `8169` (port 8069 occupé par service live). **5/5 tests verts, 0 failure, 0 error** ; 867 queries, 33.93s. PV §6 mis à jour avec le log. Verdict technique auto **GO**. Conteneur redémarré. En attente recette visuelle MOA desktop + mobile pour feu vert Explorer MVP2. |
| 2026-04-24 | **Recette visuelle MOA — NO-GO lisibilité** ; itération SCSS `19.0.1.7.1` : overlay gauche renforcé (radial + linéaires), léger assombrissement du fond (`brightness(0.94)`), H1 crème + ombres portées, sous-titre renforcé, **CTA secondaire** surchargé dans le scope hero (le style global `.ckr-btn--secondary` est charcoal, illisible sur fond sombre). QWeb et image inchangés. PV §1/§2/en-tête mis à jour ; **re-passer** recette visuelle avant feu vert Explorer. |
| 2026-04-24 | **Recette visuelle MOA — NO-GO ton** (hero trop sombre, perte appétence CK). Itération SCSS **`19.0.1.7.2`** : pas d’overlay noir global ni `brightness` sur l’image ; voile pleine largeur **très léger** (tons charte) ; **panneau crème local** `::before` sur `.ckr-hero__content` + typo `$ckr-text` / `$ckr-text-muted` ; CTA secondaire = style global. QWeb et asset inchangés. PV + SPEC §7 alignés. |
| 2026-04-24 | **Revue direction** — abandon effet « carte » ; **`19.0.1.7.3`** : overlay **dégradé gauche → droite** (semi-transparent chaud), texte clair intégré image, overlay **mobile** diagonal / fade précoce, secondaire contour clair. QWeb + image inchangés. |
| 2026-04-24 | **Correctif critique `19.0.1.7.4`** : (1) overlay G→D réellement présent dans `_hero.scss` (fichier était resté sur voile trop léger — capture MOA illisible). (2) **H1 noir** : la règle globale `ckr_main.scss` `.ckr-root… h1 { color: $ckr-text }` (spécificité + ordre après `_hero.scss`) écrasait `.ckr-hero__title` — exclusion **`h1:not(.ckr-hero__title)`** pour le scope `.ckr-page` / `.ckr-root`. |
| 2026-04-24 | **Recette visuelle MOA desktop** : **GO sous réserve validation mobile** — points validés (immersif, overlay G→D, texte intégré, CTA, image appétente). PV §1 + §8 + en-tête ; clôture ticket / feu vert Explorer **après** GO mobile. |
| 2026-04-24 | **Ajustement mobile pre-GO final** — `19.0.1.7.5` : fond sombre semi-transparent **local** (alpha 0,88) derrière zone texte + CTA uniquement (`::before` sur `.ckr-hero__content`, max-width 767px) ; degrade mobile plein ecran legerement adouci ; manifest bump. |
| 2026-04-24 | **Hotfix `19.0.1.7.6`** : compilation SCSS — `max-width: min(36rem, 100%)` provoquait *Incompatible units: '%' and 'rem'* (Dart Sass) ; remplacé par `unquote("min(36rem, 100%)")` (cf. `_header.scss`). |
| 2026-04-24 | **`19.0.1.7.7`** — mobile : lisibilité sans « bloc noir » — fond `.ckr-hero__content` `rgba(18,14,10,0.58)` + `backdrop-filter` / `-webkit-backdrop-filter` 2px ; overlay mobile dégradé vertical ; marges/padding/rayon 18px ; CTA colonne ; SPEC §7 + PV alignés. |
| 2026-04-24 | **`19.0.1.7.8`** — correctif recette MOA : `backdrop-filter` invisible / bloc trop dense — `ckr_main` : `.ckr-hero--immersive.ckr-root { background: transparent }` ; hero mobile `overflow: visible` ; voile mobile sur `::before` + blur ~12px + overlay allégé ; bump `19.0.1.7.8`. |
| 2026-04-24 | **`19.0.1.7.9`** — écart vs référence visuelle : abandon carte mobile + blur ; mobile = dégradé **intégré** sur `.ckr-hero__overlay` (principe desktop), texte direct sur image, `text-shadow` renforcé ; SPEC §7 + PV. |
| 2026-04-24 | **`19.0.1.7.10`** — **version finale attendue pour GO mobile** (snippet MOA) : overlay G→D net (noir 0.65→0.05), pas de carte ni blur, contenu sans fond (`margin: 5rem 1rem 2rem`, `padding: 2rem 1.5rem`), titre `clamp(2rem,9vw,2.8rem)` + `text-shadow` simple, sous-titre `rgba(255,255,255,0.92)`, CTA colonne `margin-top: 1.5rem`, secondaire contour 1px blanc / fond transparent. |
| 2026-04-24 | **`19.0.1.7.11`** — alignement **desktop / tablette** sur le principe mobile (cohérence cross-device) : overlay G→D unique (desktop 0.6→0 sur 85%, mobile 0.65→0.05 sur 100%), suppression du voile vertical additionnel desktop, typo simplifiée (color `#fff` / `rgba(255,255,255,0.92)` + `text-shadow` sobre), CTA secondaire mutualisé contour 1px blanc / transparent toutes tailles. QWeb et asset inchangés. |
| 2026-04-24 | **Livraison code** — `views/snippets/ckr_hero.xml` refondu en hero immersif (fond + overlay double + contenu gauche + 2 CTA), `static/src/scss/components/_hero.scss` réécrit (variante `.ckr-hero--immersive` + legacy split conservé en fallback), asset `static/src/img/hero_v2_immersive.png` issu de `docs/assets/mvp02_reference_coffret_gourmand_bois.png` (produit-centré, bois, chaud, sobre — hors familles touristiques), `__manifest__.py` bumpé `19.0.1.6.17` → `19.0.1.7.0` + description MVP2.1 1/5 consignée. **Arbitrage CTA2** : pointage transitoire vers `/shop?ckr_mode=origin` (porte Origines MVP1 opérationnelle) jusqu'à livraison de `/origines` front par le ticket Explorer MVP2. Recette MOA à ouvrir via [PV_RECETTE_HERO_HOMEPAGE_V2_CK.md](PV_RECETTE_HERO_HOMEPAGE_V2_CK.md). Mise à jour `SPEC_HERO_HOMEPAGE.md` §7/§8 restant à faire dans la même PR ou commit doc immédiat. |
| 2026-04-24 | **Clôture recette — GO MOA** : **`HERO-HOMEPAGE-V2` accepté** (desktop + mobile OK, tablette acceptable ; principe immersif cohérent ; pas carte / pas blur ; CTA lisibles ; tests auto verts). PV [§8](PV_RECETTE_HERO_HOMEPAGE_V2_CK.md). **Réserve non bloquante** : crop tablette/mobile perfectible. **Feu vert** lancement chantier **2/5** [EXPLORER-HOMEPAGE-MVP2](TICKET_EXPLORER_HOMEPAGE_MVP2.md). Statut ticket → **Clôturé — GO MOA** ; critères d’acceptation cochés. |
| 2026-04-24 | **`19.0.1.7.12`** — `__manifest__.py` : suppression des warnings docutils au chargement du module (*Unknown target name* : la description RST ne doit pas couper un identifiant **avant** un `_` en fin de ligne — références fantômes `decision_ordre`, `cadrage_fonctionnel`, `spec_impl`, `ckr_collection`). |
| 2026-04-25 | **Documentation** — **Exécution : clos** explicite dans l’en-tête ; checklist §0 **soldée** (alignement homepage MVP2.1 close MOA). |
