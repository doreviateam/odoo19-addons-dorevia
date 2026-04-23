# Directions artistiques Phase 1 — C-Kreyol

**Statut** : **propositions** issues du [brief synthétique](BRIEF_SYNTHETIQUE_CK.md), **alignées** sur la [charte minimale Phase 1](CHARTE_GRAPHIQUE_PHASE1.md) **§3–§11** (**Direction A** gelée) ; reste à **décliner** les **états UI** (charte §3) et à **figer** le copy / visuel du [spec hero](SPEC_HERO_HOMEPAGE.md) sur **photos réelles**.

**Documents liés** : [BRIEF_SYNTHETIQUE_CK.md](BRIEF_SYNTHETIQUE_CK.md), [CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md), [DESIGN.md](DESIGN.md), [SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md), [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md), [ARCHITECTURE_DECISION_RECORD.md](ARCHITECTURE_DECISION_RECORD.md) (**ADR-CKR-002** / **ADR-CKR-003**).

**Note licences** : certaines familles citées (**Canela**, **Neue Montreal**, **Suisse International**, **Söhne**, **Editorial New**, etc.) sont **commerciales** ou **à licence** ; le choix final doit être **tranché** en Phase 1 avec des **alternatives libres** (ex. **Playfair Display** + **Inter**, **IBM Plex Sans**, **Source Sans 3**) si besoin de **coût / perf** maîtrisés.

---

## Synthèse

Trois directions distinctes répondent au positionnement visé : **sérieux** et **chaleureux**, **retail**, **non folklorique**, **non cheap**, **distinct d’un template e-commerce générique** et d’un **front Odoo standard**.

**Recommandation prioritaire** : **Direction A — « Épicerie fine tropicale »** (voir §5 et §6).

---

## Direction A : « Épicerie fine tropicale » *(recommandée)*

**Ton visuel** : raffiné, terreux, **éditorial**, chaleur sobre (minimalisme chaleureux).  
**Perception marque** : retail **spécialiste** sérieux, **sélection** curatée, **crédibilité artisanale**.

### Palette

| Rôle | Couleur | Hex (indicatif) |
|------|---------|-----------------|
| **Primaire** | Terracotta / argile cuite | `#A0522D` — chaleur sans cliché exotique |
| **Secondaire** | Vert sauge / feuillage sec | `#87A878` — nature, **origine** agricole |
| **Neutres** | Off-white chaud | `#F5F1E8` ; charbon | `#2C2C2C` |
| **Accent** | Ambre doré | `#D4A373` — évocation manioc caramélisé, fruits tropicaux (sans surcharge) |

### Typographie

- **Titres** : *Canela* ou **Playfair Display** — élégance éditoriale, crédibilité « univers produit » (vérifier **licence** pour Canela).
- **Corps** : **Suisse International** ou **Inter** — netteté retail, **lisibilité mobile** excellente.

### Direction photo / image

- **Textures macro** : farine, fibres de manioc, caramélisation, pulpe de fruit.
- **Nature morte contextuelle** : produits en **lumière naturelle**, bois, matières brutes.
- **Éviter** : palmiers, plages, esthétique « vacances aux Caraïbes ».
- **Mettre en avant** : la **transformation** (matière brute → produit fini).

### Intention hero

Visuel **plein cadre** sur un **détail produit** artisanal (ex. texture de biscuit, confiture) avec **blanc généreux**. Accroche type : *« L’artisanat agro transformé des Antilles, sélectionné pour vous »* — **sans folklore**, sans plage : la **matière** du produit.  
*(À aligner sur les titres candidats et les règles [SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md) §1 / §4.)*

### Navigation et footer

- **Menu** : horizontal, **aéré**, structuré par **catégories** (ex. Biscuits, Confiseries, Épicerie) ; survols discrets (**changement de teinte**, pas seulement soulignement).
- **Footer** : grille sobre — infos service, **origine** (récit court), newsletter ; **pas** de motifs décoratifs superflus.

---

## Direction B : « Laboratoire des saveurs »

**Ton visuel** : **scientifique** rencontrant l’**artisanal**, structuré, affirmé.  
**Perception marque** : **expert** curateur, **traçabilité**, culture alimentaire **moderne**.

### Palette

| Rôle | Couleur | Hex (indicatif) |
|------|---------|-----------------|
| **Primaire** | Indigo profond / bleu nuit | `#1A1A2E` — sérieux, profondeur |
| **Secondaire** | Jaune curcuma | `#E9C46A` — origine tropicale, épice |
| **Neutres** | Gris pierre | `#E5E5E5` ; blanc |
| **Accent** | Corail | `#E07A5F` — chaleur, touche humaine |

### Typographie

- **Titres** : **Neue Montreal** ou **Space Grotesk** — structure, léger côté **technique**, contemporain.
- **Corps** : **IBM Plex Sans** — rationnel, très lisible, adapté retail.

### Direction photo / image

- **Orientée process** : étapes de fabrication, gros plans ingrédients, détails packaging.
- **Compositions en grille** : produits disposés avec précision géométrique.
- **Fonds en aplats** (terracotta, sauge) pour unifier un catalogue hétérogène.
- **Éviter** : fouillis « rustique » ; viser un artisanal **ordonné**.

### Intention hero

**Split screen** : à gauche une **grille** de 3–4 produits phares (lumière uniforme), à droite une **affirmation typographique** forte. Ex. *« Des Antilles à votre table »* — **origine** claire et sobre ; insiste sur la **sélection retail**.  
*(Cohérent avec une des familles de titre de la [SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md) §3.1.)*

### Navigation et footer

- **Menu** type **méga-menu** avec miniatures de catégories, recherche mise en avant.
- **Footer** : quasi **utilitaire** — livraison, labels / certifications, données de traçabilité ; **signaux de confiance** plutôt que décoration.

---

## Direction C : « Maison créole contemporaine »

**Ton visuel** : modernisme chaleureux, **blanc généreux**, humaniste.  
**Perception marque** : premium **accessible**, patrimoine familial **reinterpreté**.

### Palette

| Rôle | Couleur | Hex (indicatif) |
|------|---------|-----------------|
| **Primaire** | Charbon chaud | `#3D3D3D` — sophistication sans froideur |
| **Secondaire** | Ocre / terre de Sienne | `#CC7722` — terre, tradition, manioc |
| **Neutres** | Crème | `#FAF7F0` ; gris chaud | `#8C8C8C` |
| **Accent** | Mousse tropicale | `#6B8E23` — végétation, croissance |

### Typographie

- **Titres** : **Editorial New** ou **Tiempos Headline** — humaniste, autorité chaleureuse.
- **Corps** : **Söhne** ou **Source Sans Pro** — convivial, optimisé retail (**Source Sans 3** en alternative libre).

### Direction photo / image

- **Lifestyle contextualisé** : produits en contexte **domestique**, mains, partage.
- **Lumière douce directionnelle** — cuisine le matin, pas flash studio.
- **Harmonie** : accessoires et fonds tirés de la palette.
- **Éviter** : stéréotypes « famille caraïbéenne » ; privilégier le plaisir **universel** de la table.

### Intention hero

Cadrage **cinématique** : mains qui cassent un biscuit, miettes et texture au premier plan. Accroche type : *« Le goût authentique des Antilles, façonné à la main »* — **métier** et **goût**, pas le tourisme.

### Navigation et footer

- **Menu** : catégories en **pilules** au scroll, en-tête **sticky** avec léger flou.
- **Footer** : plutôt **récit** — « Notre sélection », note **partenaire** (La Platine comme **partenaire**, pas comme **propriétaire** de la marque), newsletter avec **proposition de valeur** claire.

---

## Recommandation : prioriser la direction A

**Pourquoi la direction A « Épicerie fine tropicale » répond particulièrement au brief :**

| Critère | Lecture direction A |
|--------|----------------------|
| **Sérieux + retail** | Typo éditoriale + blanc structurant = marketplace **crédible** |
| **Non folklorique** | Terracotta / sauge évoquent le **terroir**, pas le **tourisme** |
| **Centré produit** | Macro photo célèbre le **processus de transformation** |
| **Distinct d’Odoo** | Couple typo + système de couleurs = rupture avec le **générique** |
| **Excellence mobile** | Fond off-white chaud + contrastes maîtrisés = **lisibilité** |
| **Intégration La Platine** | Textures **artisanales** adaptées aux spécialités manioc / confitures |
| **Évolutivité** | Système extensible à d’**autres lignes** que La Platine |

---

## Si vous hésitez entre directions

- **Time-to-market** prioritaire → **Direction A** (souvent la plus **implémentable** rapidement avec des choix **webfonts** simples).
- **Traçabilité / transparence** comme différenciateur fort → **Direction B**.
- **Lien émotionnel / patrimoine** comme priorité n°1 → **Direction C**.

---

## Prochaines étapes (opérationnel)

1. **Affiner si besoin** la palette **terracotta / sauge** (déjà **validée** en charte **§3–§4**) sur **photos produit réelles** (éclairage, packaging).
2. **Décliner** les **états UI** et **tokens** SCSS (à partir de la charte [CHARTE_GRAPHIQUE_PHASE1.md](CHARTE_GRAPHIQUE_PHASE1.md) **§3–§4**) — **Playfair Display** + **Inter** déjà **validés Phase 1**.
3. **Geler** titre / sous-texte / CTA / intention visuelle du hero dans [SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md) §3 / §7.
4. **Implémenter** le thème Odoo dans le respect [ADR-CKR-002](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-002) / [ADR-CKR-003](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-003).

---

## Historique du document

| Date | Changement |
|------|------------|
| 2026-04-21 | Création : **3 directions** (A épicerie fine tropicale, B laboratoire, C maison créole contemporaine), **recommandation A**, critères de choix, prochaines étapes ; liens brief, charte, spec, ADR. |
| 2026-04-21 | Alignement : **charte** restructurée (**§3–§11**) avec **Direction A** **gelée** ; statut et **prochaines étapes** mis à jour. |
