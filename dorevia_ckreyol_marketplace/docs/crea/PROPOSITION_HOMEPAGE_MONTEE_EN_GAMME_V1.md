# PROPOSITION — Montée en gamme créative de la homepage C-Kreyol (V1)

**Date** : 2026-04-23  
**Auteur** : créatif front-end (session IA)  
**Statut** : **implémentée V1** le 2026-04-23 — module `dorevia_ckreyol_marketplace` version **19.0.1.6.16** (lots A–C jusqu'à v.15, puis patch v.16 : retrait `ckr-hero__subtitle-accent`, Ticket 1 P1 clôturé — alignement gel `SPEC_HERO_HOMEPAGE.md` §7). Arbitrages gelés §9 appliqués intégralement ; plan d'exécution [PLAN_IMPL_HOMEPAGE_MONTEE_EN_GAMME_V1.md](PLAN_IMPL_HOMEPAGE_MONTEE_EN_GAMME_V1.md) exécuté en 3 lots (A fil rouge v.13, B Hero+Supplier+Selection v.14, C Editorial+Trust v.15). Recette MOA passante sur les lots A–C ; hero sobre conforme SPEC §7 en v.16. Sujets hors périmètre V1 déportés en tickets séparés : [TICKETS_HORS_PERIMETRE_V1.md](TICKETS_HORS_PERIMETRE_V1.md).  
**Portée** : présentation, rythme, photo, copy visuel — **aucune** modification d'architecture, de doctrine produit, ni de comportement JS.

**Documents de référence** :
- [WIREFRAME_HOMEPAGE.md](../WIREFRAME_HOMEPAGE.md) (blocs 1–8, variantes sobre / enrichie)
- [SPEC_HERO_HOMEPAGE.md](../SPEC_HERO_HOMEPAGE.md) (gel hero §7)
- [CHARTE_GRAPHIQUE_PHASE1.md](../CHARTE_GRAPHIQUE_PHASE1.md) (Direction A gelée §3–§11)
- [DIRECTIONS_ARTISTIQUES_PHASE1.md](../DIRECTIONS_ARTISTIQUES_PHASE1.md)
- [DESIGN.md](../DESIGN.md) §7
- [ARCHITECTURE_DECISION_RECORD.md](../ARCHITECTURE_DECISION_RECORD.md) (ADR-001, 002, 003, 005, 007, 008)
- [STRUCTURE_MENU_PRINCIPAL.md](../STRUCTURE_MENU_PRINCIPAL.md) §11

---

## 1. Intention de design globale (fil rouge)

Installer une **épicerie fine tropicale éditoriale**, pas une boutique en ligne de plus : la lecture doit donner la sensation d'ouvrir un **magazine retail** — images grandes et calmes, typo serif qui respire, filets discrets, couleurs terreuses utilisées avec parcimonie. Le visiteur doit comprendre en moins de 3 secondes qu'il est face à des **produits agro-transformés antillais choisis avec soin**, pas face à une marque folklorique ni à un template e-commerce.

### Trois invariants transverses

- **Respiration** : off-white `#F5F1E8` dominant partout, couleur utilisée en **ponctuation** (accent amber sur filets / hover, terracotta sur CTA primaire uniquement).
- **Rythme vertical unifié** : `$ckr-section-py-mobile` / `$ckr-section-py-desktop` partout, aucun modificateur d'exception. Un filet amber fin (`1px × 48px`, centré ou gauche selon section) en haut de chaque `.ckr-section-title` pour signer le rythme éditorial sans alourdir.
- **Photo au centre** : matière visible, packaging accessoire, zéro scène de vie. La photo doit **porter le message** — le texte l'accompagne, ne le répète pas.

---

## 2. Section par section — choix visuels concrets

### Bloc 2 — Hero (gelé au §7 de la SPEC, périmètre = mise en scène)

> **Arbitrage gelé 2026-04-23** (§9.1) : ratio **60/40 cible** desktop, **55/45 toléré** en implémentation pour affinage selon visuel et longueur de titre, **50/50 exclu**. Bloc texte ≥ 360 px de largeur minimum sur viewport 1280 px.

**Intention** : passer du hero « bandeau web » à un hero **éditorial calme**, où la matière produit et le titre cohabitent sans se disputer.

**Choix visuels** :
- Layout **asymétrique 60/40** desktop (image à droite sur 60 % du container, bloc texte à gauche sur 40 %, ancré bas) ; **image pleine largeur + texte dessous** en mobile (≤ 768 px).
- Image : macro biscuit manioc / confiture, cadrage serré, lumière latérale naturelle, **point de focus décalé** pour laisser un espace négatif propre au-dessus du titre.
- Titre Playfair Display, grand (`clamp(2rem, 5vw, 3.25rem)`), charcoal, interligne serré (1.1). Sous-texte Inter 400, charcoal à 80 % d'opacité, largeur max `42ch` pour un rythme de lecture retail.
- Filet amber `2px × 48px` au-dessus du titre (signature).
- CTA primaire terracotta plein, label **« Découvrir la boutique »** (gelé), hover : légère élévation (translateY -1px) + léger assombrissement du fond, pas d'ombre gadget. CTA secondaire **« Explorer le catalogue »** en lien souligné + icône chevron bas (ancre `#explorer-catalogue`).
- **Aucune animation d'entrée.** Rien qui bouge à l'ouverture.

**Variante mobile** : image en 16/10, texte dessous, CTA primaire pleine largeur, secondaire en lien texte dessous.

---

### Bloc 3 — Explorer (rail manuel, gelé au §3 du WIREFRAME)

**Intention** : cinq portes lisibles comme des **chapitres de catalogue**, pas comme des boutons. Chaque carte raconte une façon d'entrer dans l'offre.

**Choix visuels** :
- Carte format portrait doux (ratio ~4:5), fond `#FAF7EE` (off-white légèrement plus chaud que le fond de section) pour détacher le rail sans rupture.
- **Visuel haut de carte** occupant 60 % de la hauteur : macro matière par porte (pas d'icône abstraite).
  - **Promotions** : biscuit sortant d'une pile (mouvement suggéré, pas animé).
  - **Collections** : disposition calme à plat de 3 produits.
  - **Kits** : un coffret ouvert, intérieur visible.
  - **Catégories** : texture isolée (manioc râpé, grains, etc.).
  - **Origines** : détail d'étiquette de provenance lisible.
- Sous la photo : petit libellé **suréligne** en Inter uppercase 11 px, letter-spacing 0.08em, sauge `#87A878` (ex. « Porte 02 »), puis titre Playfair 22 px charcoal, puis une ligne courte Inter 14 px — **1 phrase max**, pas une description.
- Hover : le filet bas de la carte passe de transparent à amber (2 px) ; léger glissement vertical de la photo (scale 1.02, 300 ms ease-out). Focus : outline `2px` amber à 2 px d'offset — visible, propre, pas de bordure qui fait sauter le layout.
- Boutons prev/next : cercles de `44×44 px`, fond off-white, bordure charcoal à 15 % d'opacité, chevron charcoal ; en hover, fond terracotta 10 % + bordure terracotta. État disabled **supprimé** (le rail boucle — déjà implémenté en JS).
- Respect strict du `dir="ltr"` existant et du `tabindex="0"` du viewport.

---

### Bloc 4 — Mise en avant fournisseur / La Platine

> **Arbitrage gelé 2026-04-23** (§9.2) : **variante plane V1** retenue (deux colonnes alignées haut, **sans** chevauchement éditorial). Le chevauchement reste une option différée pour V1.1 si le bloc paraît trop plat après mise en ligne. Cohérent WIREFRAME §3 Bloc 4, SPEC §4 et ADR-003 : éviter d'inverser la hiérarchie visuelle C-Kreyol → La Platine.

**Intention** : faire exister **La Platine** comme **partenaire artisan crédible**, sans en faire la vitrine. Le visiteur doit comprendre « qui fabrique ce qu'on achète » — pas « bienvenue chez La Platine ».

**Choix visuels (V1 — variante plane)** :
- Mise en page **deux colonnes asymétrique 55/45** desktop : photo atelier / main / machine à gauche (pas de photo de foule, pas de portrait posé ; matière en train d'être transformée) ; à droite, bloc texte sur fond off-white **aligné haut avec la photo, sans décalage vertical**.
- Micro-accent de présence : filet amber `2px × 48px` au-dessus de la surtitre sauge, pour signer le bloc sans le gonfler.
- *(Variante chevauchement éditorial archivée — photo descendant 32 px sous le bloc texte — disponible si bloc perçu trop plat en V1.1.)*
- Surtitre sauge uppercase **« Premier fournisseur »** en micro-label (pas « PARTENAIRE » creux).
- Titre Playfair moyen (28–32 px), ex. : **« La Platine — manioc, biscuits et douceurs, au plus près de la matière »**. Paragraphe court Inter 15 px, 3–4 lignes max, sans chiffre non vérifiable.
- CTA tertiaire (lien + chevron) vers `/about` ou section À propos : **« Découvrir le fournisseur »**. **Pas** de CTA boutique ici pour ne pas doublonner le hero.
- Mobile : empilement photo → texte → lien ; chevauchement supprimé.

**Garde-fou** : typo C-Kreyol plus grande que tout nom/logo La Platine présent dans l'image. Si le packaging La Platine est dominant sur la photo, recadrer ou flouter très légèrement.

---

### Bloc 5 — Sélection produits (grille sincère, pas de carrousel)

> **Arbitrage gelé 2026-04-23** (§9.4) : ligne secondaire sous le titre produit = **origine**, **sous condition de couverture ≥ 80 %** de la sélection. Si la couverture est inférieure : **aucune** ligne secondaire, titre + prix + photo suffisent. **Jamais** de mixage origine / famille / usage d'une carte à l'autre dans la même grille.

**Intention** : une sélection **honnête et courte**, présentée comme une page d'ouverture de magazine — images grandes, prix discrets, pas de badges criards.

**Choix visuels** :
- Grille desktop `4 colonnes`, mobile `2 colonnes` (pas de single-column forcé sur mobile — deux produits côte à côte sont lisibles avec des photos carrées).
- Carte produit : photo carrée `1:1` fond off-white, titre Playfair 18 px, **ligne secondaire optionnelle** (origine) en Inter 12 px sauge sous le titre (ex. « Sainte-Anne, Guadeloupe »), prix Inter 14 px charcoal à droite du titre (pas en dessous — alignement horizontal titre/prix = lecture retail rapide).
- Ligne secondaire : rendue **uniquement** si la règle de couverture §9.4 est satisfaite ; en QWeb, `t-if` sur le champ origine avec fallback **silencieux** (pas d'espace réservé, pas de « — »).
- **Pas de bouton « Ajouter au panier »** en carte homepage : la carte entière est cliquable vers la fiche. Moins d'encombrement, parcours Odoo natif respecté.
- Badge unique admis si vraiment nécessaire : petit tag Inter 11 px uppercase terracotta sur fond off-white légèrement assombri, placé en haut gauche de la photo. **Un seul badge par produit maximum** — et de préférence aucun.
- Titre de section centré : suréligne sauge « Sélection » + filet amber + Playfair 28 px « Choisis ce mois-ci » + ligne courte Inter 15 px.
- Hover carte : photo scale 1.03 en 400 ms ease-out, titre passe de charcoal à terracotta. Rien d'autre.

**Arbitrage produit** : 4 ou 8 produits — **4 si le catalogue est petit**, 8 si stock confortable. Pas 6 (brouille la grille 4 colonnes).

---

### Bloc 6 — Éditorial (collection / saison / cadeau)

> **Arbitrage gelé 2026-04-23** (§9.3) : **variante sobre par défaut en V1** (bandeau simple, citation courte + lien discret). Le format pleine largeur passe en **V1.1** uniquement si les **trois conditions cumulées** sont réunies : contenu nommable, visuel paysage 21:9 produit pour ce bloc, phrase validée par le responsable marque. Tant qu'une condition manque : sobre.

**Intention** : casser le rythme grille avec un bloc narratif. C'est l'endroit du magazine où l'on raconte une histoire courte.

**Choix visuels (V1 — variante sobre)** :
- **Bandeau simple** dans le container : suréligne sauge uppercase (« Collection », « Saison », « Offrir »), une phrase Playfair 22 px sur une ligne (deux max. si long), lien souligné amber « En savoir plus » ou équivalent.
- Pas de visuel pleine largeur, pas de cartouche en overlay.
- Fond : off-white cohérent avec l'alternance de sections.

**Variante V1.1 — pleine largeur** *(activée seulement si §9.3 remplit les trois conditions)* :
- Format **pleine largeur** (break-out du container sur desktop ≥ 1200 px) : image paysage 21:9, texte superposé en bas à gauche dans un cartouche off-white à 92 % d'opacité, largeur max `520 px`.
- Cartouche : surtitre sauge uppercase (« Collection », « Saison », « Offrir »), titre Playfair 26 px, une phrase Inter 15 px, lien « Voir la collection » en souligné amber.
- Mobile : image 4:3, cartouche sous l'image (pas en overlay — illisible sur petits écrans).
- **Si contenu non-crédible** au lancement, ce bloc se replie proprement en **bandeau simple** : une ligne de citation + lien discret, sans photo pleine largeur (variante sobre du wireframe §5).

---

### Bloc 7 — Confiance (3 axes, sobre)

**Intention** : **rassurer sans vendre**. Trois blocs courts, pas d'icônes gadget.

**Choix visuels** :
- Grille 3 colonnes desktop, empilement mobile.
- Chaque bloc : petit pictogramme linéaire `24×24` charcoal (trait 1.5 px, style Phosphor/Feather — **pas** d'icône pleine ni colorée), titre Playfair 18 px, deux lignes Inter 14 px max.
- Fond de section légèrement différencié : off-white un cran plus chaud (`#F0EADA`) pour marquer la clôture de page sans rupture.
- **Pas de CTA.** Ce bloc ne vend pas, il rassure.
- Les 3 axes restent : Achat (paiement), Livraison (prudent, aligné ADR-005), Contact (humain). Formulations courtes et honnêtes, aucune promesse de délai chiffrée.

---

### Rythme global & respiration

- **Aucun modificateur** `ckr-section--tight-top` : tous les blocs respectent `$ckr-section-py-*`. Cohérent avec les changements récents.
- Fond alterné très léger pour marquer les respirations sans rupture : Hero / Selection / Confiance = `#F5F1E8` ; Explorer / Supplier / Editorial = off-white pur `#FAF7EE` (+1 point de chaleur). Jamais de fond sombre en Phase 1.
- Transitions de section : jamais d'onde / vague / diagonale. La respiration suffit.

---

## 3. Traduction technique front (synthétique)

### SCSS — ajouts réutilisables dans `tokens/` et `components/`

- `tokens/_colors.scss` : ajouter (si absent) `$ckr-bg-warm: #FAF7EE;` et `$ckr-bg-soft: #F0EADA;` pour les fonds alternés.
- `ckr_main.scss` : ajouter un modificateur générique `.ckr-section--bg-warm { background-color: $ckr-bg-warm; }` et `.ckr-section--bg-soft { background-color: $ckr-bg-soft; }` — appliqués au niveau QWeb, pas au niveau composant.
- Composant réutilisable `.ckr-section-title` : ajouter un pseudo `::before` filet amber optionnel via modificateur `.ckr-section-title--rule` (`1px × 48px`, `background: $ckr-accent`, `margin-bottom: $ckr-space-sm`). À appliquer section par section en QWeb.
- `components/_supplier.scss`, `_selection.scss`, `_editorial.scss`, `_trust.scss` : uniformiser les transitions (`transition: all 300ms ease-out`), les états hover et focus selon la grille décrite.
- Respecter mobile-first + breakpoint Bootstrap Odoo unique `768px` déjà utilisé — ne pas ajouter de seuil.

### QWeb — ajustements légers sur les snippets

- `ckr_hero.xml` : vérifier layout 60/40 desktop et présence du filet signature.
- `ckr_entries.xml` : ajouter suréligne « Porte 0x » par carte (ou nom de porte en petit label supérieur), déjà structurellement prêt.
- `ckr_supplier.xml` : composition 55/45 alignée haut, **sans décalage vertical** en V1 (arbitrage §9.2).
- `ckr_selection.xml` : placer titre + prix sur la même ligne flex (space-between).
- `ckr_trust.xml` : pas de CTA, icônes linéaires SVG inline.
- Toute section : appliquer `ckr-section--bg-warm` ou `--bg-soft` selon alternance.

### JS — rien de nouveau

Le carrousel Explorer est déjà en pas à pas manuel (prev/next + scroll natif + clavier). **Aucune logique JS à ajouter** pour cette montée en gamme. Toute animation proposée est CSS pure (`transition` sur hover/focus).

---

## 4. Accessibilité

- Contrastes vérifiés : charcoal sur off-white = AAA large, AA small. Terracotta `#A0522D` sur off-white = AA large (utilisé sur CTA et libellés, pas sur corps de texte). Sauge sur off-white = **limite AA large uniquement** : la réserver aux **suréligne** courts (uppercase, jamais < 11 px letter-spaced) ou à des éléments décoratifs, **jamais** au corps de paragraphe.
- Focus visible partout : outline amber `2px` avec offset `2px` sur tous les éléments interactifs (cartes Explorer, cartes produit, liens éditoriaux, CTA, boutons rail).
- Cartes produit et cartes Explorer cliquables **en entier** : un seul `<a>` englobant, `aria-label` explicite si le titre ne suffit pas.
- Hover effects **dupliqués en focus** (pas d'effet réservé à la souris).
- Aucune animation sur `prefers-reduced-motion: reduce` : wrap global dans la règle `@media (prefers-reduced-motion: reduce) { transition: none; transform: none; }` dans `ckr_main.scss`.
- Structure sémantique : chaque section en `<section>` avec `aria-labelledby` pointant sur le titre ; régions `role="region"` déjà présentes sur Explorer, à vérifier sur Selection et Editorial.

---

## 5. Fichiers touchés (liste précise)

- `views/snippets/ckr_hero.xml` — layout 60/40, filet signature, CTA secondaire
- `views/snippets/ckr_entries.xml` — suréligne par carte, ajustements mineurs
- `views/snippets/ckr_supplier.xml` — composition 55/45 alignée haut (variante plane V1, §9.2), hiérarchie typo
- `views/snippets/ckr_selection.xml` — grille 4/2, carte cliquable, ligne secondaire conditionnelle (§9.4)
- `views/snippets/ckr_editorial.xml` — variante sobre V1 (bandeau simple, sans visuel pleine largeur, §9.3)
- `views/snippets/ckr_trust.xml` — 3 axes, icônes linéaires
- `views/pages/ckr_homepage.xml` — alternance fonds `--bg-warm` / `--bg-soft`
- `static/src/scss/tokens/_colors.scss` — ajouts fonds alternés
- `static/src/scss/ckr_main.scss` — modificateurs sections + règle `prefers-reduced-motion`
- `static/src/scss/components/_hero.scss` — ajustements layout
- `static/src/scss/components/_entries.scss` — suréligne, hover card
- `static/src/scss/components/_supplier.scss` — composition plane V1, hiérarchie typo, alignement haut
- `static/src/scss/components/_selection.scss` — grille, carte
- `static/src/scss/components/_editorial.scss` — bandeau éditorial sobre V1
- `static/src/scss/components/_trust.scss` — icônes linéaires, layout
- `__manifest__.py` — bump version (cache busting)

**Aucune modification JS nécessaire.**

> *Note V1.1 : les variantes pleine largeur Editorial (§9.3) et chevauchement Supplier (§9.2) restent documentées dans les sections §2 correspondantes et pourront être activées sans refonte si leurs conditions d'activation sont réunies.*

---

## 6. Points à valider côté copy / photo

- **Hero** : le sous-texte gelé (« Biscuits, douceurs et épicerie des Antilles, sélectionnés avec soin… ») est parfait pour le cadrage 60/40 ; vérifier simplement qu'il tient sur 2–3 lignes en mobile 375 px.
- **Explorer** : rédiger les **5 micro-accroches** (une phrase courte par porte). À l'heure actuelle elles existent mais méritent un pass éditorial unifié — ton conseil : verbe d'action + matière (« Composer un coffret », « Traverser les territoires », « Suivre les arrivages », etc.).
- **Supplier** : titre + 3–4 lignes sur La Platine **sans chiffre non vérifiable** (pas de « 30 ans d'expérience » si non validé). Photo atelier / matière obligatoire, **pas de portrait posé**.
- **Selection** : arbitrer 4 vs 8 produits selon le catalogue réel disponible. Photos : fond off-white cohérent entre toutes les fiches — shooting uniforme ou retouche pour harmoniser.
- **Editorial** : valider **quel angle** (collection, saison, cadeau) est le plus crédible dès lancement. Si rien n'est mûr : variante bandeau simple.
- **Trust** : formulations **prudentes** sur la livraison (pas « Livraison rapide », mais « Livraison suivie depuis Nantes » ou équivalent aligné opérable).

---

## 7. Risques et non-régressions

- **Header / footer** : non touchés par cette proposition. Vérifier qu'aucun token de couleur ajouté ne casse un override existant.
- **Portail compte / boutique** : aucune modification sur `_portal.scss`, `_shop.scss`, `_product.scss`. Les fonds alternés sont scopés à la homepage via `.ckr-section--bg-*` appliqués en QWeb homepage uniquement.
- **Mobile** : tester la bonne tenue du layout **plane Supplier** et du **bandeau éditorial sobre** sur 375 px, 390 px et 768 px — cohérent avec les arbitrages V1 (§9.2, §9.3). Les variantes V1.1 (chevauchement Supplier, break-out Editorial) devront être retestées lors de leur activation éventuelle.
- **Contenus réels Odoo** : les cartes produit doivent tenir avec des titres longs (ex. « Confiture de goyave de la vallée de la Gosier, édition limitée »). Prévoir `line-clamp: 2` sur les titres de carte Selection et Explorer, `text-overflow: ellipsis` en repli.
- **Images manquantes** : prévoir un placeholder off-white avec filet amber discret plutôt qu'une image cassée.
- **`prefers-reduced-motion`** : tester que les hover dégradés restent lisibles (fallback = bordure au lieu de transform).
- **Cache assets** : bump manifeste obligatoire après chaque itération.

---

## 8. Conclusion

**Recommandé** — proposition alignée Direction A gelée, sans modification de doctrine produit ni d'architecture homepage. Elle est **réalisable par itérations**, section par section, sans dépendance bloquante entre blocs.

### Ordre d'implémentation suggéré (du plus d'impact perçu au moins visible)

**V1 (gelée 2026-04-23)** :

1. Rythme global + fonds alternés + filet signature sur `.ckr-section-title` (1 itération, impact immédiat sur toute la page).
2. Carte produit Selection (grande valeur retail) — avec règle §9.4 sur la ligne secondaire origine.
3. Carte Explorer (détaillage visuel).
4. Hero asymétrique 60/40 desktop (§9.1).
5. Supplier variante plane V1 (§9.2).
6. Editorial sobre V1 (§9.3).
7. Trust finalisation.

**V1.1 éventuelle — activations conditionnelles** :

- Supplier avec chevauchement discret si le bloc paraît trop plat après mise en ligne (§9.2).
- Editorial pleine largeur si les trois conditions §9.3 sont réunies (contenu nommable + visuel 21:9 dédié + phrase validée marque).

### Variante possible

Si le catalogue est trop court au lancement, basculer en **variante sobre** du wireframe (§5) : retirer l'Editorial, garder Selection en 4 produits, le reste inchangé. La proposition tient sans refonte.

### Déconseillé à intégrer dans cette passe

Ajout d'animations d'apparition au scroll, parallax, vidéos d'ambiance, overlays sombres. Tout cela casserait la Direction A et ouvrirait une dette visuelle.

---

## 9. Arbitrages gelés — 2026-04-23

Décisions validées faisant de cette proposition une **base de travail officielle** pour la montée en gamme créative de la homepage. Les sections concernées du §2 portent un bloc de renvoi vers cette §9.

### Synthèse

| # | Arbitrage | Décision gelée | Référence section |
|---|-----------|----------------|-------------------|
| 9.1 | Hero desktop — ratio de composition | **60/40 cible**, 55/45 toléré en impl., 50/50 exclu | §2 Bloc 2 |
| 9.2 | Supplier — niveau de présence visuelle | **Variante plane V1** ; chevauchement différé en V1.1 conditionnel | §2 Bloc 4 |
| 9.3 | Editorial — format V1 | **Variante sobre par défaut** ; pleine largeur en V1.1 sur 3 conditions cumulées | §2 Bloc 6 |
| 9.4 | Carte produit homepage — ligne secondaire | **Origine** si couverture ≥ 80 % de la sélection, sinon **rien** ; jamais mixé | §2 Bloc 5 |

---

### 9.1 Hero desktop — ratio de composition

**Décision** : **60/40 cible**, **55/45 toléré en implémentation** pour affinage selon le visuel retenu et la longueur du titre, **50/50 exclu**.

**Justification** :
- La Direction A gelée ([CHARTE_GRAPHIQUE_PHASE1.md](../CHARTE_GRAPHIQUE_PHASE1.md) §3–§11, [SPEC_HERO_HOMEPAGE.md](../SPEC_HERO_HOMEPAGE.md) §3.4 / §7) place la **matière** au centre du message hero. Une image qui dépasse la moitié de l'écran est cohérente avec ce choix : la photo **porte** le message, le texte l'accompagne.
- 50/50 glisse vers un pattern « template marketing » symétrique, contraire à [ADR-CKR-003](../ARCHITECTURE_DECISION_RECORD.md#adr-ckr-003) (le rendu standard Odoo n'est pas l'état final).
- 55/45 est une bande de tolérance saine pour les cas où le visuel est très dense ou le titre particulièrement long en mobile.

**Contrainte d'implémentation** : le bloc texte doit tenir un **minimum de 360 px de largeur** sur un viewport 1280 px pour préserver la hiérarchie titre / sous-texte / CTA et éviter un sous-texte cassé sur 4 lignes.

---

### 9.2 Bloc fournisseur — niveau de présence visuelle

**Décision** : **variante plane retenue pour V1** (deux colonnes 55/45, photo et texte **alignés haut**, **sans** chevauchement vertical). Un micro-accent de présence (filet amber `2px × 48px` au-dessus de la surtitre sauge) suffit à signer le bloc. Le chevauchement éditorial est **versé en option V1.1** si le bloc paraît trop plat après mise en ligne.

**Justification** :
- [WIREFRAME_HOMEPAGE.md](../WIREFRAME_HOMEPAGE.md) §3 Bloc 4 et [SPEC_HERO_HOMEPAGE.md](../SPEC_HERO_HOMEPAGE.md) §4 sont fermes : La Platine **ne doit pas** absorber C-Kreyol ni inverser la hiérarchie visuelle.
- Le chevauchement est un effet « magazine » qui donne du **poids éditorial** à un bloc — donc exactement ce qu'on veut **éviter** pour garder Supplier en position clairement secondaire par rapport à Hero et Selection.
- La variante plane sert mieux l'intention « ancrage sincère sans vitrine fournisseur » et simplifie le SCSS et le responsive (aucune logique mobile pour désactiver un chevauchement).

**Option V1.1** : si après mise en ligne le bloc est perçu trop plat, on a deux leviers gradués avant le chevauchement complet :
1. Renforcement du micro-accent (filet plus long, suréligne sauge plus appuyée).
2. Chevauchement réintroduit (photo descendant 32 px sous le bloc texte).

---

### 9.3 Bloc éditorial — variante V1

**Décision** : **variante sobre par défaut en V1** (bandeau simple : suréligne sauge + phrase Playfair + lien souligné amber, sans visuel pleine largeur). Le format **pleine largeur** passe en V1.1 **uniquement** si les **trois conditions cumulées** sont réunies :

1. Une collection / saison / offre cadeau effectivement **active et nommable** (pas un concept flou).
2. Une photo paysage **21:9 produite ou recadrée pour ce bloc** (pas une image du hero recyclée).
3. Une phrase d'accroche **validée** par le responsable marque.

Tant qu'une condition manque : la variante sobre reste en place.

**Justification** :
- [WIREFRAME_HOMEPAGE.md](../WIREFRAME_HOMEPAGE.md) §3 Bloc 6 et §9 imposent explicitement : « si Offrir / Recettes ne sont pas nourris crédiblement, **réduire** ou **retirer** ce bloc ».
- Un bloc pleine largeur **mal nourri** produit l'inverse de l'intention : au lieu d'un magazine, le visiteur perçoit un bandeau publicitaire creux — plus gros risque de dégradation visuelle de toute la page.
- La variante sobre reste **gracieuse** dans le rythme de la page et permet une bascule non-régressive vers la version riche dès que le contenu et le visuel sont prêts ensemble.

---

### 9.4 Carte produit homepage — ligne secondaire

**Décision** : la ligne secondaire sous le titre produit affiche **l'origine**, **sous condition de couverture ≥ 80 %** des produits de la sélection. En dessous de ce seuil : **aucune** ligne secondaire (titre + photo + prix suffisent). **Jamais** de mixage origine / famille / usage d'une carte à l'autre dans la même grille.

**Justification** :
- [DESIGN.md](../DESIGN.md) §5 (principes retail) et [SPEC_HERO_HOMEPAGE.md](../SPEC_HERO_HOMEPAGE.md) §1 placent **l'origine** comme repère commercial fort, visible dès le hero et **prolongé** sur les cartes — cohérence maximale.
- Une grille où quelques cartes affichent l'origine et les autres autre chose (ou rien) crée une **incohérence perçue** plus coûteuse que l'absence d'info : le visiteur retail lit la grille comme un tout.
- **Famille / type de produit** est déjà redondant avec le titre (« Confiture de goyave » → famille = confiture). **Usage** est trop subjectif pour une homepage. L'origine reste le seul champ retail-pertinent ici.

**Règle d'implémentation** :
- En QWeb : un seul champ (`origine`), rendu conditionnellement via `t-if` avec **fallback silencieux** (aucun espace réservé, aucun tiret).
- Le seuil de 80 % est évalué **sur la sélection affichée** (pas sur le catalogue global).
- Si la sélection est curatée manuellement, privilégier un **filtrage amont** sur la couverture origine (option à valider côté édito) pour atteindre 100 % et stabiliser le rendu.

**Évolution** : si la qualité des données origine se dégrade ou s'améliore, l'arbitrage reste stable (seuil fixe) ; seul le rendu effectif varie.

---

## Historique du document

| Date | Changement |
|------|------------|
| 2026-04-23 | Création : proposition V1 de montée en gamme créative de la homepage — fil rouge, section par section (blocs 2 à 7), traduction SCSS / QWeb, accessibilité, fichiers touchés, arbitrages copy/photo, risques, ordre d'implémentation. Aligné Direction A gelée, ADR-007, ADR-008, rail Explorer manuel. |
| 2026-04-23 | **Passage en base de travail officielle** — §9 **Arbitrages gelés** ajouté : (9.1) hero 60/40 cible / 55/45 toléré / 50/50 exclu ; (9.2) Supplier variante plane V1, chevauchement différé en V1.1 conditionnel ; (9.3) Editorial variante sobre par défaut, pleine largeur en V1.1 sur 3 conditions cumulées ; (9.4) carte produit ligne secondaire = origine si couverture ≥ 80 %, sinon rien, jamais mixé. Blocs de renvoi ajoutés dans §2 Hero / Supplier / Selection / Editorial. |
| 2026-04-23 | **Passe de cohérence V1** — statut document mis à jour (base de travail officielle V1) ; §3 QWeb Supplier réaligné (plane V1, sans décalage) ; §5 fichiers touchés Supplier et Editorial réalignés sur les arbitrages V1 + note V1.1 ; §7 risques mobile réaligné sur les layouts V1 ; §8 ordre d'implémentation séparé en V1 gelée + V1.1 conditionnelle. |
| 2026-04-23 | **Implémentée V1** — 3 lots appliqués en patches conservateurs sur `dorevia_ckreyol_marketplace` : **Lot A** (`v.12 → v.13`) fil rouge transverse — modificateur `.ckr-section-title__eyebrow--rule` dans `ckr_main.scss`, garde `prefers-reduced-motion` scopée au périmètre `.ckr-root` / `.ckr-page`, application du `--rule` sur Supplier + Selection + Editorial + Trust (Explorer hors périmètre) ; **Lot B** (`v.13 → v.14`) Hero `grid-template-columns: 4fr 6fr` (§9.1 60/40), Supplier `align-items: start` + filet amber 2 px local (§9.2 plane V1), Selection nouveau wrapper `__head` flex baseline + ellipsis h3 2 lignes + `white-space: nowrap` prix + `:focus-visible` amber (§9.4 garde-fou responsive) ; **Lot C** (`v.14 → v.15`) refonte complète Editorial en bandeau sobre centré (§9.3 — suppression des 2 tuiles overlay sombre, nouveau `.ckr-editorial__bandeau` / `__eyebrow` / `__line` / `__link`, pas de `<h2>`), Trust icônes linéaires charcoal 32×32 transparent (abandon pilule amber). Recette MOA passante. Points validés en arbitrage final : (1) Editorial sans `<h2>` accepté en V1 — outline strict h1 → h2×4, AA respecté, bandeau traité comme transition ; (2) lien unique `/collections` accepté — `/recettes` reste accessible via footer, URL directe, page publiée. Sujets hors périmètre déportés en [TICKETS_HORS_PERIMETRE_V1.md](TICKETS_HORS_PERIMETRE_V1.md). |
| 2026-04-23 | **Post-V1 — Ticket 1 (P1) clôturé, Option A** — retrait du `<span class="ckr-hero__subtitle-accent">` dans `views/snippets/ckr_hero.xml` et du bloc SCSS `.ckr-hero__subtitle-accent` dans `static/src/scss/components/_hero.scss` ; hero plus sobre et respirant, conformité stricte au gel `SPEC_HERO_HOMEPAGE.md` §7 (SPEC non amendée). Bump module **19.0.1.6.15 → 19.0.1.6.16**. |
