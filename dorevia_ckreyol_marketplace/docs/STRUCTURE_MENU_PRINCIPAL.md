# STRUCTURE_MENU_PRINCIPAL — C-Kreyol

Ce document décrit la **structure cible du menu principal** du front-end **C-Kreyol** en **Phase 1**.

Il complète :

- [DESIGN.md](DESIGN.md)
- [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md) (alignement homepage ↔ menu)
- [NOTE_DE_CADRAGE.md](NOTE_DE_CADRAGE.md)
- [ARCHITECTURE_DECISION_RECORD.md](ARCHITECTURE_DECISION_RECORD.md) (notamment [ADR-CKR-003](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-003))

Le menu principal est un **élément obligatoirement personnalisé** en Phase 1. Il ne doit pas reprendre le rendu standard Odoo comme base finale.

---

## 1. Rôle du menu principal

Le menu principal doit :

- porter l’**identité** de **C-Kreyol** ;
- permettre un accès **clair et rapide** aux grandes entrées du canal ;
- soutenir une logique **retail** et non une simple exposition technique du catalogue ;
- rester **lisible sur mobile** ;
- éviter la surcharge et la profondeur excessive en Phase 1.

Le menu ne doit pas chercher à refléter toute la profondeur future du projet. Il doit d’abord servir une **exploration simple, crédible et commerciale** de l’offre.

---

## 2. Principes de construction

### 2.1 Principes directeurs

- **Peu d’entrées de niveau 1**
- intitulés **simples**
- hiérarchie **courte**
- équilibre entre :
  - **accès catalogue**
  - **entrées éditoriales**
  - **confiance**
  - **accès utilitaires**

### 2.2 Ce que le menu doit exprimer

Le menu doit faire percevoir que **C-Kreyol** est :

- un **canal retail digital** ;
- une **marque propre** ;
- un site de vente de **produits agro transformés antillais** ;
- un canal **sérieux**, non un simple catalogue ERP.

### 2.3 Ce que le menu ne doit pas devenir

- une arborescence trop profonde de type « grand agrégateur » ;
- une liste technique de catégories sans intention commerciale ;
- une copie du standard Odoo ;
- un empilement de rubriques concurrentes.

### 2.4 Intitulés de niveau 1

Les intitulés du **niveau 1** doivent rester **courts**, **concrets** et **immédiatement compréhensibles** sans effort d’interprétation.

---

## 3. Hypothèse de structure Phase 1

### 3.1 Niveau 1 — proposition de base

Proposition de structure principale :

1. **Boutique**
2. **Collections**
3. **Offrir**
4. **Recettes**
5. **À propos**
6. **Contact**

À compléter / arbitrer :

- faut-il une entrée explicite **Nouveautés** ?
- faut-il une entrée explicite **Origines** ou **Territoires** dès la Phase 1 ?
- faut-il un accès **Pro / B2B** visible dès la Phase 1 ou non ?

### 3.2 Logique de chaque entrée

#### Boutique

Entrée principale vers l’**offre produit** sur une logique **taxonomique / catalogue** :

- **catégories** de produits (grandes familles) ;
- **toutes les références** ou accès structuré **familles → produits** ;
- point d’entrée **principal** du **catalogue e-commerce** tel qu’attendu par le client.

**Distinction avec Collections** : ici on structure l’**inventaire** et la **navigation par rayon** ; ce n’est pas le seul lieu des **sélections** portées par la mise en marché (voir ci-dessous).

#### Collections

Entrée **retail / éditoriale** sur une logique **non strictement taxonomique** :

- **best sellers** (sincères) ;
- **nouveautés** réelles ;
- **sélections** saisonnières ;
- **univers d’usage** ;
- **sélections** par occasion.

**Distinction avec Boutique** : **Collections** ne remplace pas le **catalogue structuré** ; elle regroupe des **sélections** et des **angles** de découverte **sans dupliquer** la seule arborescence « grandes familles » de la **Boutique**. Si la frontière paraît floue en implémentation, trancher explicitement ce qui relève de **/shop** (familles) vs pages **collections** éditoriales.

#### Offrir

Entrée dédiée à la logique **cadeau**.

Peut inclure :

- idées cadeaux ;
- coffrets ;
- sélections par budget ;
- attentions / occasions.

**Vigilance** : le libellé **Offrir** n’est **pertinent** en Phase 1 que si le canal peut montrer un **mini-univers crédible** (quelques idées cadeaux, une sélection simple, coffrets ou attentions **réellement** disponibles). Sinon l’entrée **décrédibilise** le retail — arbitrer : fusion avec **Collections**, contenu minimal **avant** ouverture, ou **repousser** l’entrée.

#### Recettes

Entrée **éditoriale** reliant produits et usages.

Objectif :

- enrichir l’expérience ;
- soutenir l’exploration ;
- crédibiliser la logique retail.

**Vigilance** : l’entrée suppose une **charge éditoriale** (contenus recettes reliés aux produits). Si la capacité n’est pas là à l’ouverture : **assumer** un calendrier éditorial minimal, **retirer** l’entrée du menu jusqu’à preuve de contenu, ou **remplacer provisoirement** par une entrée plus simple (ex. **Blog** / **Inspirations**) — **à trancher** avant gel.

#### À propos

Entrée de confiance / marque.

Peut porter :

- vision C-Kreyol ;
- ancrage Nantes / Antilles ;
- premier fournisseur ;
- qualité / sérieux du canal.

#### Contact

Entrée utilitaire de confiance.

Doit rester simple et accessible.

---

## 4. Structure alternative possible

### Option A — menu très sobre

- Boutique
- Collections
- À propos
- Contact

### Option B — menu retail enrichi

- Boutique
- Collections
- Offrir
- Recettes
- À propos
- Contact

### Option C — ouverture précoce à la logique B2B

- Boutique
- Collections
- Offrir
- Recettes
- Pro
- À propos
- Contact

**Lecture** : l’**option C** expose **Pro / B2B** très tôt dans le menu principal ; pour la Phase 1, le cœur de l’expérience reste plutôt le **retail B2C** — le **B2B** peut exister plus **discrètement** (footer, **À propos**, espace séparé ultérieur), cf. [DESIGN.md §3.2–3.3](DESIGN.md).

### Décision Phase 1 (niveau 1)

**Option B — menu retail enrichi**, avec **vigilance** particulière sur la **réalité éditoriale** des entrées **Offrir** et **Recettes**.

**Hypothèse recommandée à ce stade** : **Option B**, sous réserve de **confirmation** de la capacité à alimenter **Offrir** et **Recettes** de manière **crédible** dès la Phase 1.  
Si cette capacité fait **défaut** à l’ouverture, **Option A** reste une **version transitoire** acceptable (sans renoncer à l’ambition **retail** à moyen terme).

**Point de vigilance** : un menu **retail riche** sans **contenus minimaux** derrière **Offrir** et **Recettes** **dégrade la confiance** — l’arbitrage final dépend autant du **goût** que de la question : *peut-on nourrir ces entrées sans faire faux ?*

---

## 5. Sous-navigation / mégamenu

### 5.1 Position de principe

La Phase 1 doit rester prudente sur le mégamenu.

Un mégamenu n’est acceptable que si :

- la lisibilité reste forte ;
- le catalogue le justifie réellement ;
- la version mobile reste simple.

### 5.2 Hypothèse recommandée

- **desktop** : menu principal clair, sous-entrées limitées ;
- **mobile** : navigation courte, repliable, sans surcharge.

---

## 6. Utilitaires hors menu principal

Les éléments suivants ne doivent pas nécessairement surcharger le menu de niveau 1 :

- compte client
- panier
- recherche
- icônes sociales
- langue
- accès pro
- livraison / FAQ

Ils peuvent être placés :

- en header secondaire ;
- dans des zones utilitaires ;
- dans le footer.

---

## 7. Exigences mobile

Le menu mobile doit :

- être accessible facilement au pouce ;
- s’ouvrir rapidement ;
- éviter les sous-niveaux excessifs ;
- permettre d’atteindre :
  - boutique,
  - panier,
  - compte,
  - contact,
  - pages de confiance,

  sans friction majeure.

Le menu mobile est un **élément critique de la Phase 1**.

---

## 8. Éléments à éviter

- plus de rubriques que nécessaire ;
- vocabulaire flou ou trop « marketing » ;
- catégories trop techniques ;
- duplication entre menu, homepage et footer ;
- profondeur excessive ;
- rendu visuel « standard Odoo ».

---

## 9. Questions ouvertes

La **structure de principe** **Option B** est posée en **§4** et **§10**. Restent notamment à **trancher** avant gel :

- **Nouveautés** : entrée de **niveau 1** dédiée ou intégration sous **Boutique** / **Collections** ?
- **Origines / Territoires** : entrée de **niveau 1** en Phase 1 ou traitement par **pages** / **collections** ?
- **Pro / B2B** : confirmer le repli **hors menu principal** (footer, **À propos**, lien discret) jusqu’à maturité du canal.
- **Calendrier éditorial minimal** pour **Offrir** et **Recettes** ; faute de quoi **révision** du menu (repli **Option A** transitoire, cf. §4).

---

## 10. Décision cible à formaliser

**Décision cible Phase 1** :  
Le menu principal de **C-Kreyol** retient une structure **retail enrichie** de **niveau 1** :

- **Boutique**
- **Collections**
- **Offrir**
- **Recettes**
- **À propos**
- **Contact**

Cette structure pourra être **révisée** si la **charge éditoriale** réelle ne permet pas de soutenir de manière **crédible** les entrées **Offrir** et **Recettes** au moment de l’ouverture (cf. §3.2 et §4).

Le menu principal devra en tout état de cause :

- rester **court** ;
- soutenir la logique **retail** ;
- **distinguer** le canal du standard Odoo ([ADR-CKR-003](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-003)) ;
- être **parfaitement utilisable** sur **mobile** (§7).

---

## 11. Complément Phase 2 — Section « Explorer » sur la homepage *(distinct du menu)*

La **Phase 2** introduit sur la **homepage** un bloc **Explorer / Par où commencer** qui ne remplace **pas** la décision **Option B** ci-dessus : le menu reste la **navigation générale du site**.

* **Menu (§10)** : Boutique, Collections, Offrir, Recettes, À propos, Contact — rubriques **canal** (commerce + éditorial + relation).
* **Explorer** : **cinq portes d’exploration catalogue** — libellés front au **pluriel** **Promotions**, **Collections**, **Kits**, **Catégories**, **Origines** (ordre d’affichage). Pour la porte 3, **règle de bi-lexique** [ADR-CKR-008](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) : libellé **visiteur** = **Kits** (univers alimentaire C-Kreyol : kit colombo, kit apéritif…) ; **grille back-office / source de vérité** = **Pack** (module OCA **`product_pack`**, case *« Est un pack ? »* = booléen `pack_ok`, onglet *Pack*). URL visible **`/kits`** ; conventions internes en **Pack** — [ADR-CKR-006 / 008](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-006), [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md) Bloc 3. **Mise en page** des cartes sur l’accueil (rail horizontal **manuel**, sans autoplay, boutons précédent/suivant) : même référence **WIREFRAME** — sous-section *Présentation front (implémentation)*.

En particulier, **Offrir** et **Recettes** ne sont **pas** des cartes **Explorer** ; ils restent accessibles via le **header** (et le **bloc éditorial** homepage si contenu disponible). **Promotions**, **Origines** et **Kits** *(front, porte **Pack** en back-office)* sont portés par Explorer (pages dédiées ou `/shop` selon arbitrages métier / paramétrage Odoo).

---

## Historique du document

| Date | Changement |
|------|------------|
| 2026-04-21 | Création : rôle du menu, principes, proposition de base (6 entrées), options A/B/C, mégamenu, utilitaires, mobile, questions, décision **[à compléter]**. |
| 2026-04-21 | **Option B** posée comme **décision Phase 1** (§4, §10) avec repli **Option A** si charge éditoriale insuffisante ; distinctions **Boutique** / **Collections** ; vigences **Offrir** / **Recettes** ; **§2.4** intitulés niveau 1 ; lecture **option C** vs B2C. |
| 2026-04-21 | Lien vers **[WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md)** dans l’en-tête (cohérence menu / homepage). |
| 2026-04-21 | **§11** : complément — section **Explorer** homepage **≠** menu Option B ; renvois **ADR-006/008** + **WIREFRAME** Bloc 3. |
| 2026-04-21 | **§11** : porte **Kits → Packs** (et référence doctrine interne « composition » retirée) — alignement sur la logique pack Odoo / OCA **`product_pack`** (vérification back-office : case *« Est un pack ? »*, onglet *Pack*). |
| 2026-04-21 | **§11** : formalisation de la **règle de bi-lexique** [ADR-CKR-008](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-008) — libellé **visiteur** repassé à **Kits** (univers alimentaire), **grille back-office / source de vérité** conservée sur **Pack** (`pack_ok`, `product_pack`). URL visible **`/kits`** ; conventions internes SPEC / CONTRAT_URL / paramètre CK maintenues en **Pack**. |
| 2026-04-23 | **§11** : renvoi **WIREFRAME** — sous-section *Présentation front* (rail Explorer **manuel**, prev/next, sans autoplay). |
