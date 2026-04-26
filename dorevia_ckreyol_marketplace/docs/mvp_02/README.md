# MVP 02 — Documentation de chantier

Dossier de **cadrage et décisions** pour la vague **MVP 02** (évolution homepage et suites), distinct de **`docs/mvp_01/`** (specs portes catalogue, contrats d’URL, PV recette).

## Pilotage MVP2.1 — gel MOA (2026-04-24)

**Prompt de lancement** (à remettre au dev pour ouvrir la vague) : [`docs/prompting/prompt_lancement_mvp21.md`](../prompting/prompt_lancement_mvp21.md).

**Validations**

- Découpage des **5 chantiers** (tickets dans le tableau **Exécution & recette** ci-dessous) validé.
- Ordre des blocs homepage **gelé** : [1_HOMEPAGE.md](1_HOMEPAGE.md) (**Gel conception**).
- **Éditorial (§4 canon)** : **hors périmètre** évolution MVP2.1 — **V1** conservée ([PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md §9.3](../crea/PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md), bandeau sobre) ; rendu si `ckr_hpage_mvp1_tail_blocks = 1`.
- **Hero (chantier 1/5)** : recette visuelle **GO MOA** — ticket **`HERO-HOMEPAGE-V2` accepté** ; preuve [PV_RECETTE_HERO_HOMEPAGE_V2_CK.md](../crea/PV_RECETTE_HERO_HOMEPAGE_V2_CK.md) **§8** (2026-04-24) ; tests auto verts (`dorevia_ckr_hero`). *Réserve non bloquante* : crop tablette / mobile perfectible (piste d’amélioration future).
- **Explorer (chantier 2/5)** : implémentation **19.0.1.8.2** (grille **8+4**, micro-copy, visuel Origines ; base **19.0.1.8.1**) ; tests `dorevia_ckr_explorer` ; recette : [PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md](../crea/PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md) **§3 — GO (réserve mineure)**.
- **Sélection (chantier 3/5)** : logique **19.0.1.9.2+** (4 `product.template` sur le **site**, repli catalogue, visuels fiche/variante, règle §9.4 origines) ; visuels vitrine **19.0.1.9.7** ; par défaut **`ckr_hpage_mvp1_tail_blocks=0`** dans [ckr_homepage.xml](../../views/pages/ckr_homepage.xml) (**masque** Fournisseur + Éditorial ; **affiche** Cercle + Réassurance) ; tests `dorevia_ckr_selection` — [TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md](../crea/TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md) ; recette : **GO MOA avec réserves mineures (2026-04-24)** — [PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md).
- **Inscription (chantier 4/5)** : **Cercle C-Kreyol** — [TICKET_INSCRIPTION_HOMEPAGE_MVP21.md](../crea/TICKET_INSCRIPTION_HOMEPAGE_MVP21.md) ; recette : **GO MOA (2026-04-25)** — [PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md) ; *N/A V1* : composition split visuel / formulaire (bloc centré livré).
- **Réassurance (chantier 5/5)** : bloc confiance **4 repères**, statique, avant footer — [TICKET_REASSURANCE_HOMEPAGE_MVP21.md](../crea/TICKET_REASSURANCE_HOMEPAGE_MVP21.md) ; recette : **GO MOA (2026-04-25)** — [PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md) ; *réserve non bloquante* : rendu simple, évolution **Design System** plus tard.

**Clôture homepage MVP2.1 (MOA)** — **2026-04-25** : les **cinq chantiers** MVP2.1 homepage sont recettés ; la vague est **close côté MOA**. Suite : amélioration continue (Design System, contenu, conversion).

**Cadrage MVP2.2 boutique (MOA)** — **2026-04-25** : atelier **clos** pour le **cadrage** (UX, doctrine libellés, pré-spec **Incontournables** / `featured`) — canon **[2_SHOP.md](2_SHOP.md)** ; intégration **[SPEC_SHOP_PORTES.md](../mvp_01/SPEC_SHOP_PORTES.md)** **§4.6**. **Ticket dev** : **[TICKET_INCONTOURNABLES_SHOP_FEATURED_MVP22.md](../crea/TICKET_INCONTOURNABLES_SHOP_FEATURED_MVP22.md)** — chiffrage puis implémentation.

**Outillage d'exécution boutique (2026-04-26)** :

- [SHOP_EXEC_MATRIX.md](SHOP_EXEC_MATRIX.md) — matrice par contexte `/shop` (titre, hero, shortcuts, sidebar, fallback, recette) ;
- [SHOP_COMPONENT_CONTRACTS.md](SHOP_COMPONENT_CONTRACTS.md) — mapping **doc → code** et invariants d'orchestration ;
- [TICKET_SHOP_SIDEBAR_CATEGORIES.md](TICKET_SHOP_SIDEBAR_CATEGORIES.md) — fallback **`opt_wsale_categories`**, **`show_price_filter`**, démo 4 blocs, Odoo 19 / liens catégorie, offcanvas, **Prix** déplié par défaut (**10.24–10.28**) ;
- [SHOP_MAQUETTE_ECARTS.md](SHOP_MAQUETTE_ECARTS.md) — synthèse maquette vs livré (sidebar §2) ;
- [NOTE_TECH_TUILE_SHOP_FOOTER.md](NOTE_TECH_TUILE_SHOP_FOOTER.md) — pied tuile `/shop` (prix \| CTA, wrappers Odoo, cascade) ;
- [TICKET_SHOP_MVP22_VISIBLE_WAVE1.md](../crea/TICKET_SHOP_MVP22_VISIBLE_WAVE1.md) — ticket Vague 1 à utiliser avec les deux documents ci-dessus pour éviter l'empilement `hero + bandeaux + header natif`.

### Ordre de merge des PR (souhait MOA)

1. **Hero** — [TICKET_HERO_HOMEPAGE_V2.md](../crea/TICKET_HERO_HOMEPAGE_V2.md)  
2. **Explorer** — [TICKET_EXPLORER_HOMEPAGE_MVP2.md](../crea/TICKET_EXPLORER_HOMEPAGE_MVP2.md)  
3. **Sélection produits** — [TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md](../crea/TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md)  
4. **Inscription** — [TICKET_INSCRIPTION_HOMEPAGE_MVP21.md](../crea/TICKET_INSCRIPTION_HOMEPAGE_MVP21.md)  
5. **Réassurance** — [TICKET_REASSURANCE_HOMEPAGE_MVP21.md](../crea/TICKET_REASSURANCE_HOMEPAGE_MVP21.md)  

### Précisions MOA complémentaires

**Sélection produits** — Source **simple et maintenable** côté BO : **sélection explicite** (liste de produits ou paramétrage **snippet Website**). **Pas** de logique automatique complexe en MVP2.1.

**Inscription** — V1 livrable : **formulaire léger custom** ; pas d’espace membre ni automation avancée. **RGPD** : consentement explicite, lien **`/privacy`** (libellé **politique de confidentialité**), capacité de **désinscription**. **Pages légales module** : **`/privacy`** (politique structurée), **`/terms`** (mentions légales + hébergeur affiché + CGV) — voir README module § Pages légales ; **relecture juridique** recommandée avant ouverture publique (notamment si l’hébergeur réel ≠ bloc OVH par défaut). Le module **`mass_mailing`** n’est à **envisager** que s’il **simplifie** la mise en œuvre **sans** alourdir dépendances ou parcours.

**Réassurance** — **Livré MVP2.1** : **4 repères** statiques (ton sobre, preuve douce) — [PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md). Réf. ticket historique : 5 / 3 items ; aucune promesse **non maîtrisée**.

**Assets visuels** — Priorité à la banque locale **`docs/assets/`** (inventaire : [README du module](../../README.md), **Références visuelles MVP 02**). Usages typiques : **Hero**, **Explorer**, **Inscription** (visuel split), **fallback** si besoin. **Uniquement** images **réelles** (produits, producteurs, gestes métier) ; **pas** d’images touristiques ni **illustratives** ; **pas** d’assets **externes** en production **sans validation MOA**.

**Recette** — **Validation MOA à chaque PR** (pas uniquement en fin de sprint) ; compléter le **PV** du chantier concerné après chaque livraison.

## Fichiers

| Fichier | Description |
|---------|-------------|
| [DECISION_HERO_HOMEPAGE_V2.md](DECISION_HERO_HOMEPAGE_V2.md) | Décision MOA — hero immersif (Option B), QWeb + SCSS, ticket avant PR |
| [DECISION_EXPLORER_HOMEPAGE_MVP2.md](DECISION_EXPLORER_HOMEPAGE_MVP2.md) | Décision MOA — grille asymétrique Explorer, ordre des 5 portes, ticket avant PR |
| [DECISION_PRODUITS_HOMEPAGE_MVP21.md](DECISION_PRODUITS_HOMEPAGE_MVP21.md) | Décision MOA — sélection 4 produits dynamiques `website_sale`, prix, fiche produit, hors panier grille |
| [DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md](DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md) | Décision MOA — ordre **Produits → Éditorial → Inscription → Réassurance** (éditorial avant inscription) |
| [1_HOMEPAGE.md](1_HOMEPAGE.md) | Canon homepage MVP2.1 : §1 Hero … §6 Réassurance (Éditorial §4 explicite) |
| [2_SHOP.md](2_SHOP.md) | Canon boutique `/shop` MVP2.2 : UX, doctrine, **Incontournables** (`featured`) ; renvoi **[SPEC_SHOP_PORTES.md §4.6](../mvp_01/SPEC_SHOP_PORTES.md)** |
| [SHOP_EXEC_MATRIX.md](SHOP_EXEC_MATRIX.md) | Matrice d'exécution boutique : contextes `/shop`, hero, shortcuts, sidebar, fallback, recette |
| [SHOP_COMPONENT_CONTRACTS.md](SHOP_COMPONENT_CONTRACTS.md) | Contrat des composants boutique : mapping doc / code / invariants d'orchestration |
| [NOTE_TECH_TUILE_SHOP_FOOTER.md](NOTE_TECH_TUILE_SHOP_FOOTER.md) | Note dev : footer tuile produit `/shop` (QWeb, grille, neutralisation `website_sale`) |

**Exécution & recette** (dossier `docs/crea/`) :

| Fichier | Description |
|---------|-------------|
| [TICKET_HERO_HOMEPAGE_V2.md](../crea/TICKET_HERO_HOMEPAGE_V2.md) | Checklist pilotage, critères d’acceptation, hors périmètre |
| [PV_RECETTE_HERO_HOMEPAGE_V2_CK.md](../crea/PV_RECETTE_HERO_HOMEPAGE_V2_CK.md) | PV recette : **GO MOA** (2026-04-24, §8) |
| [TICKET_EXPLORER_HOMEPAGE_MVP2.md](../crea/TICKET_EXPLORER_HOMEPAGE_MVP2.md) | Grille Explorer + réordonnancement portes — checklist avant PR |
| [PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md](../crea/PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md) | PV recette : **GO MOA 2026-04-24** (réserve mineure §3) |
| [TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md](../crea/TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md) | Sélection produits dynamiques — checklist avant PR |
| [PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md) | PV recette : **GO MOA** (2026-04-24, réserves mineures) |
| [TICKET_INSCRIPTION_HOMEPAGE_MVP21.md](../crea/TICKET_INSCRIPTION_HOMEPAGE_MVP21.md) | Bloc newsletter / cercle — insertion éditorial → trust |
| [PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md) | PV recette : **GO MOA 2026-04-25** |
| [TICKET_REASSURANCE_HOMEPAGE_MVP21.md](../crea/TICKET_REASSURANCE_HOMEPAGE_MVP21.md) | Bloc confiance — évolution 3 vs 5 axes, copy sincère |
| [PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md) | PV recette : **GO MOA 2026-04-25** (réserve mineure Design System §4) |
| [TICKET_INCONTOURNABLES_SHOP_FEATURED_MVP22.md](../crea/TICKET_INCONTOURNABLES_SHOP_FEATURED_MVP22.md) | Boutique `/shop` — porte **Incontournables** (`featured`), 6 lots, critères d’acceptation |

## Liens utiles (hors MVP 02)

- Direction / ADR : `docs/direction/`
- Créa & tickets : `docs/crea/`
- Portes `/shop` & contrats URL : `docs/mvp_01/`
