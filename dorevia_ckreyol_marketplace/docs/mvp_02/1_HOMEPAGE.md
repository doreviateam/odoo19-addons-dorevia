# MVP2.1 — Homepage

**Décision hero structurelle** : [DECISION_HERO_HOMEPAGE_V2.md](DECISION_HERO_HOMEPAGE_V2.md) (Option B, hero immersif, ticket avant PR).  
**Ticket d’exécution** : [TICKET_HERO_HOMEPAGE_V2.md](../crea/TICKET_HERO_HOMEPAGE_V2.md) — **PV recette** : [PV_RECETTE_HERO_HOMEPAGE_V2_CK.md](../crea/PV_RECETTE_HERO_HOMEPAGE_V2_CK.md).

**Décision Explorer MVP2** : [DECISION_EXPLORER_HOMEPAGE_MVP2.md](DECISION_EXPLORER_HOMEPAGE_MVP2.md) (grille asymétrique, ordre portes, ticket avant PR).  
**Ticket d’exécution** : [TICKET_EXPLORER_HOMEPAGE_MVP2.md](../crea/TICKET_EXPLORER_HOMEPAGE_MVP2.md) — **PV recette** : [PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md](../crea/PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md) (**GO MOA 2026-04-24**, réserve mineure §3).

**Décision Sélection produits MVP2.1** : [DECISION_PRODUITS_HOMEPAGE_MVP21.md](DECISION_PRODUITS_HOMEPAGE_MVP21.md) (4 produits dynamiques `website_sale`, prix, fiche produit, hors panier grille).  
**Ticket d’exécution** : [TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md](../crea/TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md) — **PV recette** : [PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md).

**Décision ordre bas de page MVP2.1** : [DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md](DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md) (**Éditorial avant Inscription** — séquence Produits → Éditorial → Inscription → Réassurance).  
**Ticket d’exécution — Inscription** : [TICKET_INSCRIPTION_HOMEPAGE_MVP21.md](../crea/TICKET_INSCRIPTION_HOMEPAGE_MVP21.md) — **PV recette** : [PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md) (**GO MOA 2026-04-25**).  
**Ticket d’exécution — Réassurance** : [TICKET_REASSURANCE_HOMEPAGE_MVP21.md](../crea/TICKET_REASSURANCE_HOMEPAGE_MVP21.md) — **PV recette** : [PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md) (**GO MOA 2026-04-25**, réserve mineure Design System).

**Gel conception** : la **structure canonique** §1–6 (Hero → Explorer → Produits → Éditorial → Inscription → Réassurance) et l’**ordre** Produits → Éditorial → Inscription → Réassurance sont **validés MOA** (2026-04-24). **Implémentations MVP2.1 livrées** — **ne pas rouvrir** l’ordre des blocs sans **ticket MOA explicite** de révision.

**Clôture homepage MVP2.1 (MOA)** — **2026-04-25** : les cinq chantiers homepage sont **recettés** ; pilotage : [README MVP 02](README.md). Suite : amélioration continue (Design System, contenu, conversion).

**Drapeau QWeb `ckr_hpage_mvp1_tail_blocks`** (valeur **`0`** par défaut dans [`ckr_homepage.xml`](../../views/pages/ckr_homepage.xml)) : **masque** uniquement **Fournisseur** (§3 bis) et **Éditorial** (§4). **Inscription** (newsletter) et **Réassurance** (§6) sont **toujours** rendus. Mettre **`1`** pour réafficher le **bas de page V1** complet (fournisseur + éditorial), **sans** retirer newsletter ni confiance.

**Pilotage PR** : **ordre de merge** des cinq chantiers, précisions MOA (sélection BO, inscription, réassurance, assets `docs/assets/`, **recette à chaque PR**) — [README MVP 02](README.md) section **Pilotage MVP2.1**.

## Sections

### 1. Hero

## Contenu
Titre :
Retrouvez les saveurs et savoir-faire créoles.

Texte :
C-Kreyol sélectionne avec soin des produits issus de territoires où la culture créole est vivante, auprès de producteurs et créateurs de confiance.

CTA principal :
Découvrir la sélection → /shop

CTA secondaire :
Explorer les origines → /origines

## Rendu attendu
- image de fond produit (candidats versionnés : `docs/assets/mvp02_reference_*.png` — inventaire dans [README du module](../../README.md), sous-tableau **Références visuelles MVP 02**)
- texte aligné à gauche
- overlay léger (lisibilité)
- 2 boutons visibles

## Contraintes
- pas de blur fort
- pas d’illustration
- pas de style startup

### 2. Explorer (portes)

**Arbitrage MOA** : [DECISION_EXPLORER_HOMEPAGE_MVP2.md](DECISION_EXPLORER_HOMEPAGE_MVP2.md) — **grille asymétrique MVP2** (livrée module ≥ **19.0.1.8.2**) ; **ticket** : [TICKET_EXPLORER_HOMEPAGE_MVP2.md](../crea/TICKET_EXPLORER_HOMEPAGE_MVP2.md).

#### Rôle
Orienter le visiteur vers les **cinq modes de lecture catalogue** ([ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007), [SPEC_SHOP_PORTES.md](../mvp_01/SPEC_SHOP_PORTES.md)).

#### Implémentation (MVP2 livré module ≥ 19.0.1.8.2)

- `views/snippets/ckr_entries.xml` : **grille asymétrique** ; `#explorer-catalogue` ; **sans** carrousel / prev-next.
- Ordre **affiché** : **Promotions → Kits → Catégories → Collections → Origines** ([DECISION_EXPLORER_HOMEPAGE_MVP2.md](DECISION_EXPLORER_HOMEPAGE_MVP2.md)).

#### MVP2 — ordre retenu + poids visuel grille

| # | Porte | `href` | Poids grille |
|---|--------|--------|----------------|
| 1 | Promotions | `/promotions` | **Dominante** |
| 2 | Kits | `/kits` | **Secondaire fort** |
| 3 | Catégories | `/categories` | Carte simple |
| 4 | Collections | `/collections` | Carte simple |
| 5 | Origines | `/origines` | Carte simple |

*(Détail contrats d’URL / comportements : `docs/mvp_01/` — inchangés par cette décision.)*

#### Rendu attendu (cible MVP2)

- Grille **asymétrique** desktop ; **mobile** et **spans** précisés en maquette ou spec d’impl. (cf. ticket §0).
- Carte entière cliquable ; hover/focus sobres ; **pas d’autoplay**.

#### Contraintes

- Pas de visuels abstraits décoratifs ; pas de faux packaging ; textes lisibles sur images si utilisées.
- **Cohérence routes** avec `mvp_01` ; **Explorer ≠ menu** ([STRUCTURE_MENU_PRINCIPAL.md §11](../direction/STRUCTURE_MENU_PRINCIPAL.md)).
- **Copy** : [PLATEFORME_MARQUE_CK_V1.md](../crea/PLATEFORME_MARQUE_CK_V1.md) ; cohérence avec le CTA hero secondaire « Explorer les origines » (Origines en #5 — rôle de **porte**, pas nécessairement « premier plan visuel »).

#### Checklist avant PR (renvoi ticket)

Voir **[TICKET_EXPLORER_HOMEPAGE_MVP2.md](../crea/TICKET_EXPLORER_HOMEPAGE_MVP2.md) §0** (maquette, DOM, copy, assets, a11y, wireframe, manifest, PV, instance).

### 3. Produits

*(Vertical « après Explorer » : **mise en avant fournisseur** puis **sélection produits** — [WIREFRAME_HOMEPAGE.md](../direction/WIREFRAME_HOMEPAGE.md) Blocs 4 et 5 ; sincérité offre [ADR-CKR-005](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005).)*

**Arbitrage MOA (sélection — Bloc 5)** : [DECISION_PRODUITS_HOMEPAGE_MVP21.md](DECISION_PRODUITS_HOMEPAGE_MVP21.md) — **ticket avant PR** : [TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md](../crea/TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md).

#### Rôle

- **Fournisseur (Bloc 4)** : ancrer l’offre dans le **réel** ; hiérarchie **C-Kreyol** → partenaire (doctrine wireframe) — `views/snippets/ckr_supplier.xml`.
- **Sélection (Bloc 5)** : preuve d’**offre réelle** branchée sur **`website_sale`** ; grille sobre, sans sur-promesse ([DESIGN.md §5.1](../direction/DESIGN.md)).

#### Chaînage & implémentation (MVP2.1)

- **Ordre cible (WIREFRAME)** : [`views/pages/ckr_homepage.xml`](../../views/pages/ckr_homepage.xml) — après Explorer : Fournisseur → Sélection ; puis Éditorial ; puis **Inscription newsletter** ; puis Réassurance.
- **Ordre avec `ckr_hpage_mvp1_tail_blocks = 0` (défaut)** : **Hero** → **Explorer** → **Sélection** → **Inscription** → **Réassurance** (Fournisseur + Éditorial **non** rendus).
- **Fournisseur** (V1) — `ckr_supplier.xml` (La Platine, CTA **En savoir plus** → `/a-propos`) : rendu seulement si `ckr_hpage_mvp1_tail_blocks` vaut `1`.
- **Sélection** (module ≥ **19.0.1.9.2**, fiches vitrine 4/4 + affectation accueil si emplacements vides en **19.0.1.9.5** ; **visuels produit** banque `docs/assets/` → `static/src/img/selection/` + migration **19.0.1.9.7** ; tests repli en **19.0.1.9.4**) — `ckr_selection.xml` : **4** emplacements **Site web** ; résolution = jusqu’à **4** produits **avec** binaire image modèle **ou** variante (sinon l’emplacement est ignoré et complété par le catalogue jusqu’à 4) ; pas de visuel « placeholder » Odoo en grille. **Titre** accueil : *Notre sélection du moment* ; **prix** `_get_combination_info` ; **CTA** fiche ; **pas** d’ajout panier. **Aucun** produit publié avec image : message d’aide. **Origine** : couverture ≥ 80 % (§9.4). **Conflit** `website.homepage` : [README module](../../README.md) § Sélection.
- **Pas de carrousel** sur ce bloc ([WIREFRAME §2](../direction/WIREFRAME_HOMEPAGE.md)).

#### Comportement

- Clic **carte** ou **CTA** → **fiche produit** ; cohérence parcours e-commerce standard Odoo.
- **Pas** de redirection **forcée** des cartes vers `/shop` seul ; un lien de **section** vers le catalogue reste **optionnel** (distinct des cartes).

#### Hors périmètre MVP2.1 (gel)

- Pas d’**ajout panier direct** sur la grille ; pas d’AJAX / panier inline ; pas de **prix statique** ; pas de grille **8** produits ; pas de surcharge UX — détail [DECISION_PRODUITS_HOMEPAGE_MVP21.md](DECISION_PRODUITS_HOMEPAGE_MVP21.md).

#### Contraintes

- [ADR-CKR-005](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005) ; **Copy** [PLATEFORME_MARQUE_CK_V1.md](../crea/PLATEFORME_MARQUE_CK_V1.md).

#### Checklist avant PR (renvoi ticket)

Voir **[TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md](../crea/TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md) §0**.

#### Recette

- **MVP2.1** : [PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md).
- **Phase A (historique)** : [PV_RECETTE_PHASE_A_HOMEPAGE_CK.md](../crea/PV_RECETTE_PHASE_A_HOMEPAGE_CK.md) §6.4.

### 4. Éditorial

**Arbitrage MOA (ordre)** : [DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md](DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md) — après **Produits**, **avant** Inscription et Réassurance.

#### Rôle

Prolonger l’univers **C-Kreyol** au-delà du catalogue produit ([WIREFRAME_HOMEPAGE.md](../direction/WIREFRAME_HOMEPAGE.md) Bloc 6).

#### V1 — implémentation actuelle

- Chaînage : [`ckr_homepage.xml`](../../views/pages/ckr_homepage.xml) — après `ckr_snippet_selection` (et après **Fournisseur** si actif) : **`ckr_snippet_editorial`** rendu seulement si `ckr_hpage_mvp1_tail_blocks` vaut `1`.
- Fichier **`views/snippets/ckr_editorial.xml`** : bandeau sobre (gel [PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md §9.3](../crea/PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md)) — eyebrow **« Collection »**, phrase d’accroche, lien **`/collections`**.

#### MVP2.1 — cible

- Bloc éditorial **sobre** ;
- Mise en avant d’une **sélection**, d’un **thème** ou d’une **origine** ;
- Lien vers **Collections** ou contenu associé (selon contenu réel).

#### Contraintes

- Pas de **sur-promesse** ; pas de **storytelling artificiel** ;
- Cohérence [PLATEFORME_MARQUE_CK_V1.md](../crea/PLATEFORME_MARQUE_CK_V1.md) ; [ADR-CKR-005](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005) si promesses visibles.

---

### 5. Inscription

*(Cible **newsletter homepage** — **après** le §4 Éditorial et **avant** le §6 Réassurance ; [DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md](DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md).)*

**Refonte courante (≥ 19.0.1.10.69)** : [TICKET_REFONTE_BLOC_NEWSLETTER_HOMEPAGE_CK.md](../crea/TICKET_REFONTE_BLOC_NEWSLETTER_HOMEPAGE_CK.md) — bloc horizontal desktop, **`mass_mailing`**, liste **Newsletter C-Kreyol**, retours **`?cc_nl=`**.  
**Historique MVP2.1** — **PV recette** : [PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md) (**GO MOA 2026-04-25**) ; ticket livraison initiale [TICKET_INSCRIPTION_HOMEPAGE_MVP21.md](../crea/TICKET_INSCRIPTION_HOMEPAGE_MVP21.md).

**Chaînage** : **`ckr_snippet_circle`** (fichier `views/snippets/ckr_circle.xml`, id template conservé pour compatibilité) **après** `ckr_snippet_editorial` (si rendu) et **avant** `ckr_snippet_trust` — [`ckr_homepage.xml`](../../views/pages/ckr_homepage.xml).

#### Rôle

Inviter le visiteur à **rester en relation** avec C-Kreyol (nouvelles, sélections, offres) **sans** bruit commercial ni parcours type « adhésion » — voir intention produit du **ticket de refonte**.

#### Implémentation actuelle (2026-05)

- **Snippet** : `views/snippets/ckr_circle.xml` — classes **`ckr-newsletter`** ; label **NEWSLETTER** ; promesse éditoriale ; filet horizontal puis texte RGPD complet ; champ e-mail + CTA **S’inscrire** ; **pas** de préférences optionnelles ; **pas** de wording « cercle ».
- **SCSS** : `static/src/scss/components/_newsletter.scss`.
- **POST** **`/ckr/circle/subscribe`** — `controllers/ckr_circle.py` : **`mailing.contact`** sur **`mailing.list` « Newsletter C-Kreyol »** ; redirections **`cc_nl`** : `ok` \| `dup` \| `invalid` \| `err`.
- **Legacy** : modèle **`ckr.circle.subscriber`** et **`/ckr/circle/unsubscribe/<token>`** pour inscriptions historiques ; pages **`/privacy`** / **`/terms`** inchangées pour le site.

#### Chronologie MVP2.1 (référence — contenu à l’époque « cercle »)

Le ticket [TICKET_INSCRIPTION_HOMEPAGE_MVP21.md](../crea/TICKET_INSCRIPTION_HOMEPAGE_MVP21.md) et le **PV** documentent la **première livraison** (bloc centré, préférences, lien `/privacy` dans le formulaire, retours **`cc_cir`**). Ce périmètre est **remplacé** par la refonte pour le **comportement et le copy** courants — la **position** dans la page reste conforme au **DECISION**.

#### Rendu attendu

- Section **après** le §4 **Éditorial** (si affichée) et **avant** le §6 — ordre gelé inchangé.
- **Desktop** : promesse à gauche, **e-mail + bouton sur une ligne** à droite (bouton pas pleine largeur) ; **mobile** : colonne, bouton pleine largeur.

#### Contraintes

- Pas de **pop-up** ; pas de **réduction** promise ; pas de **fausse urgence** ; pas de **tracking** additionnel intrusive (ticket refonte §13).
- **RGPD** : texte de réassurance dans le bloc + pages **`/privacy`** et **`/terms`** ; désinscription gérée côté e-mails (**mass mailing**) ; validation juridique avant prod. publique recommandée.

#### Recette

- **Initiale MVP2.1** : [PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md) — complété § refonte **2026-05**.
- **Critères refonte** : [TICKET_REFONTE_BLOC_NEWSLETTER_HOMEPAGE_CK.md](../crea/TICKET_REFONTE_BLOC_NEWSLETTER_HOMEPAGE_CK.md) § critères d’acceptation (GO).
- **GO visuel desktop & gel UI newsletter** : même PV, § dédié (2026-05) ; recette finale responsive / Odoo / états / accessibilité à confirmer sur instance.

---

### 6. Réassurance

*(Aligné wireframe [Bloc 7 — Bloc confiance](../direction/WIREFRAME_HOMEPAGE.md) ; implémenté par `ckr_snippet_trust` — voir V1.)*

**Ticket d’exécution** : [TICKET_REASSURANCE_HOMEPAGE_MVP21.md](../crea/TICKET_REASSURANCE_HOMEPAGE_MVP21.md) — **PV recette** : [PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md) (**GO MOA 2026-04-25**, réserve Design System).

#### Rôle

Rassurer avant l’achat, sans discours générique ni **surpromesse** ([ADR-CKR-005](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)).

#### V1 — implémentation historique (pré-MVP2.1 clôture)

- Ancienne mouture : **3** axes (Achat / Livraison / Contact) — remplacée par la livraison MVP2.1 ci-dessous.

#### MVP2.1 — implémentation livrée (2026-04-25)

- Fichier : `views/snippets/ckr_trust.xml` — appel **dernier** bloc du `wrap` dans [`ckr_homepage.xml`](../../views/pages/ckr_homepage.xml) (**après** `ckr_snippet_circle`, **avant** le footer site). **Toujours** rendu (indépendant de `ckr_hpage_mvp1_tail_blocks`).
- **Structure** : en-tête **« En pratique »** / titre **« Quelques repères »** ; grille **`ckr-trust__grid`** — **4** repères, icônes Font Awesome sobres :
  1. **Produits sélectionnés avec soin** — producteurs et partenaires de confiance (`fa-leaf`).
  2. **Expédition depuis la France** — préparation et envoi depuis la métropole (`fa-truck`).
  3. **Paiement sécurisé** — transactions protégées (`fa-lock`).
  4. **Support disponible** — joignabilité (`fa-envelope-o`).
- Fond : `ckr-section--soft` ; grille responsive 1 / 2 / 4 colonnes — `static/src/scss/components/_trust.scss`.
- **Recette** : [PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md) (**GO MOA** ; réserve mineure Design System).

#### Cible rédactionnelle historique (ticket — 5 intentions)

Référence de travail initiale dans [TICKET_REASSURANCE_HOMEPAGE_MVP21.md](../crea/TICKET_REASSURANCE_HOMEPAGE_MVP21.md) ; **livré** : **4** repères (arbitrage chantier, lisibilité / sincérité).

#### Rendu attendu

- Section **après** le §5 **Inscription** — **toujours** avant le footer.
- **Desktop et mobile** : texte court ; pas de surpromesse ; *réserve* : finition Design System ultérieure.

#### Contraintes

- Pas de **faux badges** de confiance ; pas de **promesse excessive** ; pas de « **livraison rapide** » si non garantie — copy actuelle **prudente** ([`ckr_trust.xml`](../../views/snippets/ckr_trust.xml)).
- Pas de **surcharge** visuelle.

#### Checklist avant PR (renvoi ticket)

Voir **[TICKET_REASSURANCE_HOMEPAGE_MVP21.md](../crea/TICKET_REASSURANCE_HOMEPAGE_MVP21.md) §0**.

#### Recette

- **MVP2.1** : [PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md).
- **Phase A (historique)** : [PV_RECETTE_PHASE_A_HOMEPAGE_CK.md](../crea/PV_RECETTE_PHASE_A_HOMEPAGE_CK.md) si sections transverses utiles.