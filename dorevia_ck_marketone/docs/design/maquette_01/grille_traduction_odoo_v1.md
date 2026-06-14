# Grille de traduction Odoo — v1 (analyse MOA)

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Statut** | Grille d’analyse MOA — **pas ticket de développement** |
| **Suite de** | `grille_traduction_odoo_brouillon.md` (passe QA/MOA positive) |
| **Références** | `design_01.md` v1.1 · Maquette V1.1 · `revue_dev_traduisibilite_odoo.md` · `recette_qa_maquette_01.md` |
| **Arbitrages §10** | **Tranchés MOA** — cf. [`note_transmission_arbitrage_david_01_v1_1.md`](./note_transmission_arbitrage_david_01_v1_1.md) |
| **Verrou Odoo** | **Levé ticket 01 uniquement** — exécution encadrée autorisée MOA |
| **Squelette thème** | **Validé QA statique** — recette fonctionnelle suspendue à instance Odoo 19 CE |
| **Date** | 2026-06-12 |

### Statut courant (lecture prioritaire)

```text
Architecture Odoo : verrou levé uniquement pour le ticket 01 dorevia_ck_theme ;
GO général CK non donné ; extensions hors ticket 01 interdites.
Squelette dorevia_ck_theme : validé QA statique (recette_qa_dorevia_ck_theme_01_squelette.md).
Recette fonctionnelle : suspendue — instance Odoo 19 CE requise.
```

Les formulations « Architecture Odoo = toujours verrouillée » ou « verrou maintenu »
ci-dessous, lorsqu’elles apparaissent hors §14, relèvent du **contexte historique**
(avant addendum GO ticket 01 — cf. note transmission § addendum).

---

## 1. Objet de la grille

Ce document traduit la **maquette CK V1.1** en décisions d’implémentation Odoo **futures** :

```text
Thème        → dorevia_ck_theme (visuel, layout, tokens)
Template     → website_sale / website natif (comportement, données)
Extension    → uniquement si Odoo standard + thème insuffisent (arbitrage MOA)
Interdit     → front autonome, catalogue/panier/checkout parallèles
```

**Nature du document** : grille d’analyse et d’arbitrage pour David — **pas** un ordre de développement.

La validation QA de la maquette **ne constitue pas** un GO développement Odoo.

### Évolution maquette — lecture MOA

```text
Maquette V1.1.1 = stable (validée QA — adaptation Pro MOA)
Textes Pro = alignés arbitrages MOA §10
Architecture Odoo : verrou levé uniquement pour le ticket 01 dorevia_ck_theme ;
GO général CK non donné ; extensions hors ticket 01 interdites.
```

Les précisions matrice fournisseur/distributeur, entrée Pro double cible et distinction prix B2C / conditions B2B **ne rouvrent pas** le chantier UX global. Une **micro-évolution textuelle** de l’entrée Pro peut être envisagée **après** arbitrage David — point d’arbitrage, pas correction maquette obligatoire maintenant.

**Exemples d’ajustements possibles post-arbitrage** (illustration, non engagement) :

```text
Vous êtes producteur ou transformateur créole ?
Proposez vos produits et structurez votre offre avec CK.

Vous êtes boutique, restaurant, hôtel ou distributeur ?
Référencez des produits créoles et approvisionnez votre point de vente.

Les prix affichés publiquement correspondent au canal B2C CK.
Les partenaires professionnels qualifiés peuvent bénéficier de conditions commerciales personnalisées via Odoo.
```

---

## 2. Doctrine MOA confirmée

### Référentiel technique projet

```text
Odoo 19 CE · snippets first · pas de surcouche autonome
```

```text
Odoo = source de vérité métier
website_sale = moteur boutique B2C phase 1
Thème = habillage Odoo (tokens, layout, snippets) — pas front parallèle
Maquette V1.1.1 = référence UX validée (QA V1.1.1 + revue Dev favorable avec réserves)
dorevia_ckreyol_marketone = mémoire d’analyse, pas reprise automatique
```

Note d’approche thème (validée MOA) : [`note_approche_technique_dorevia_ck_theme_01.md`](../note_approche_technique_dorevia_ck_theme_01.md)

Ticket cadrage thème 1 (**validé MOA — exécution encadrée**) : [`ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md`](../ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md)

```text
Ticket thème 1 : tokens + layout + snippets — pas activation pricelists / portail / parcours B2B
```

### Doctrine brick & mortar (MOA)

> CK valorise les producteurs et transformateurs créoles, tout en soutenant les distributeurs physiques — boutiques, épiceries, restaurants, hôtels, concept stores et revendeurs — qui souhaitent référencer et proposer ces produits à leurs propres clients.

> L’entrée professionnelle phase 1 est une **porte de qualification commerciale**, non un **portail B2B transactionnel**.

CK ne court-circuite pas les distributeurs physiques.

### Matrice fournisseur / distributeur (doctrine complémentaire MOA)

CK est une plateforme d’**intermédiation commerciale et logistique** entre deux mondes réels.

| Pôle | Archétype | Profil | Besoins |
|------|-----------|--------|---------|
| **Offre** | **La Platine** | Producteurs / transformateurs créoles — artisans, producteurs à offre différenciante | Débouchés commerciaux · canal fiable et valorisant · mise en marché · catalogue · vente B2B/B2C · logistique · montée en production progressive |
| **Demande** | **Kemet Exotique** | Commerces physiques spécialisés — boutiques, épiceries, restaurants, hôtels, concept stores, distributeurs | Clientèle existante · produits authentiques et différenciants · régularité d’approvisionnement · conditions B2B claires (prix, minimums, délais, colisage, disponibilité) · catalogue digital fiable pour découvrir, sélectionner et commander |

**Positionnement CK** : opérateur commercial, logistique et digital entre ces deux pôles.

> **CK connecte des producteurs créoles comme La Platine à des commerces spécialisés comme Kemet Exotique, avec un catalogue structuré, une logistique maîtrisée et une expérience d’achat professionnelle.**

**Conséquence d’architecture** : le B2C reste une vitrine marchande et un canal de vente directe ; le cœur économique peut s’appuyer fortement sur la chaîne :

```text
Producteurs / transformateurs créoles
→ CK
→ boutiques spécialisées / épiceries / restaurants / distributeurs
→ consommateurs finaux
```

### Boussole stratégique MOA

> **CK connecte les fournisseurs créoles aux distributeurs européens, tout en opérant un canal e-commerce B2C de vente directe.**

```text
Fournisseurs créoles
        ↓
        CK
   ↙         ↘
B2C direct   Distributeurs européens
             ↓
        Consommateurs finaux
```

| Face CK | Rôle phase 1 |
|---------|--------------|
| **B2B structurante** | Fournisseurs créoles → CK → distributeurs européens (qualification commerciale) |
| **B2C directe** | CK → consommateurs finaux (`website_sale`, prix publics canal B2C) |

Ne modifie pas la séquence ni le verrou Odoo.

### Doctrine prix B2C / B2B (MOA)

Les prix affichés publiquement sur CK, hors identification utilisateur, correspondent aux **prix de vente que CK conseille et pratique pour son canal B2C**.

Un partenaire B2B qualifié pourra avoir ses propres conditions commerciales grâce aux **fonctionnalités standard Odoo de listes de prix**.

```text
Visiteur non identifié / client B2C
→ prix public CK

Partenaire B2B identifié / qualifié
→ liste de prix Odoo associée au partenaire
→ prix de vente personnalisé
```

**Formulation phase 1 :**

```text
Pas d’exposition publique des prix B2B en phase 1.
Les prix publics affichés correspondent au canal B2C CK.
Les conditions commerciales B2B sont gérables en back-office Odoo via les listes de prix, pour les partenaires qualifiés.
L’exposition d’un parcours B2B transactionnel complet reste hors phase 1.
```

| Élément | Phase 1 |
|---------|---------|
| Prix publics site | Prix B2C CK |
| Partenaires B2B qualifiés | Prix personnalisés via `product.pricelist` Odoo (back-office) |
| Portail B2B transactionnel complet | Hors phase 1 |
| Workflow devis / commande pro complet | Hors phase 1 |
| Qualification commerciale | Page Pro + formulaire |
| Listes de prix Odoo | Mécanisme cible pour les conditions B2B |

```text
Prix publics B2C affichés sur le site ≠ conditions commerciales B2B personnalisées via listes de prix Odoo.
```

### Répartition indicative phase 1

| Couche | Part indicative | Rôle |
|--------|-----------------|------|
| Thème `dorevia_ck_theme` | ~55 % | Identité, tokens, header/footer, tuiles, sidebar visuelle, responsive |
| Templates natifs Odoo | ~35 % | `/shop`, fiche, tri, pagination, buy box, recherche |
| Extensions | ~10 % max | Origines, collections, filtre prix — **si** arbitrage MOA |
| Front autonome | 0 % | Interdit |

```text
Estimation indicative de complexité, non engagement de charge ou de périmètre.
```

### Décision MOA — catégories e-commerce

```text
Phase 1 → product.public.category hiérarchiques
```

Arborescence cible (maquette V1.1) :

```text
Boutique
├── Épicerie créole
│   ├── Farines · Galettes · Biscuits
│   ├── Confitures
│   └── Sauces & piments · Épices & condiments
├── Boissons
│   ├── Jus & nectars · Sirops · Infusions
├── Coffrets & packs
│   ├── Découverte · Cadeaux · Professionnels
└── Maison & bien-être
    ├── Savons artisanaux · Huiles · Soins naturels
```

---

## 3. Entrée pro — qualification des deux familles de partenaires

L’entrée professionnelle phase 1 ne doit **pas** être réduite à un simple achat en volume. Elle prépare la **qualification commerciale** des deux familles de relations (cf. matrice §2).

### Famille 1 — Fournisseurs / producteurs (La Platine)

- proposer ses produits ;
- être référencé dans le catalogue CK ;
- structurer son offre ;
- signaler un besoin de mise en marché, catalogue ou logistique.

### Famille 2 — Distributeurs / brick & mortar (Kemet Exotique)

- référencer des produits créoles dans son point de vente ;
- approvisionner boutique, restaurant, hôtel ou revendeur ;
- demander un accès professionnel ;
- conditions B2B claires — **hors transaction en ligne phase 1**.

Distributeurs visés : boutiques, épiceries fines, concept stores, restaurants, hôtels, revendeurs spécialisés, points de vente locaux ou européens.

### Ce que couvre l’entrée pro phase 1 (signal)

| Famille | Signaux portés |
|---------|----------------|
| Fournisseurs | Référencement offre · structuration catalogue · contact commercial producteur |
| Distributeurs | Référencement en point de vente · approvisionnement · qualification type de professionnel |

**Hors phase 1** : portail B2B transactionnel complet, workflow devis / commande pro complet, exposition publique des prix B2B.

**En phase 1** : qualification commerciale ; conditions B2B des partenaires qualifiés gérables en back-office via `product.pricelist` Odoo standard.

**Traduction Odoo phase 1 envisageable** (simple, sans portail transactionnel) :

```text
page CMS d’intention
formulaire de contact / qualification
qualification CRM de la nature de la demande (pas classification définitive du partenaire)
catégorisation progressive des contacts fournisseurs et clients professionnels
listes de prix Odoo pour partenaires qualifiés (back-office, hors exposition publique)
portail B2B transactionnel et workflows commande pro complets → phase ultérieure
```

### Intentions UX (contenu à porter)

```text
Vous êtes producteur ou transformateur créole ?
Proposer vos produits, être référencé, structurer votre offre avec CK.

Vous êtes distributeur, restaurateur ou boutique spécialisée ?
Référencer des produits créoles dans votre point de vente.
Approvisionnement pour boutiques, restaurants, hôtels et revendeurs.
Demander un accès professionnel.
```

### Arbitrage entrée pro — à trancher David (§10)

**Couche technique (CMS vs CRM) :**

| Option | Description |
|--------|-------------|
| **A** | Page CMS d’intention seule |
| **B** | `website_crm` / formulaire CRM seul |
| **C** | Page CMS + formulaire simple raccordable CRM |

**UX double cible fournisseur / distributeur :**

| Option | Description |
|--------|-------------|
| **A** | Page Pro unique avec deux blocs : « Je suis producteur / transformateur » · « Je suis distributeur / boutique / restaurant » |
| **B** | Deux CTA distincts : « Proposer vos produits » · « Référencer des produits créoles » |
| **C** | Formulaire unique avec champ de qualification de la demande (cf. nuance ci-dessous) |
| **D** | Deux formulaires séparés plus tard |
| **E** | Autre option David |

**Nuance MOA — nature de la demande, pas classification définitive**

Un même `res.partner` Odoo peut être client, fournisseur, ou les deux. Le champ formulaire qualifie la **demande**, pas le rôle définitif du partenaire.

```text
Formulaire Pro → lead CRM (website_crm) → qualification commerciale
→ création ou rapprochement partenaire
→ rôles client / fournisseur déterminés ensuite selon les flux réels
```

**Libellé recommandé** : « Nature de la demande professionnelle » ou « Type de relation souhaitée avec CK ».

**Valeurs possibles** : proposer une offre / être référencé fournisseur · référencer des produits / approvisionner un point de vente · demander des conditions commerciales · partenariat / autre.

**Recommandation MOA probable (non décision)** :

```text
Phase 1 :
page Pro unique + deux blocs + deux CTA distincts
+ formulaire unique (nature de la demande)
+ couche technique option C (CMS + website_crm)
```

`website_crm` pertinent phase 1 pour capture et qualification commerciale. Qualifie les deux cibles sans portail B2B transactionnel complet.

**Recommandation Dev (non décision)** : alignée — lead CRM suffisant ; rôles partenaire et pricelists en back-office Odoo post-qualification.

---

## 4. Grille par zone — Accueil

| Zone maquette | Couche | Traduction Odoo probable | Phase 1 | Note |
|---------------|--------|--------------------------|---------|------|
| Header | Thème + template | `website.layout` | Natif + thème | Panier = `sale_get_order()` |
| Hero + CTA boutique | Thème / snippet | Snippet ou QWeb bloc | Thème | — |
| CTA Professionnels | Thème + page CMS | Lien page « Accès pro » | Signal | §3 brick & mortar |
| Pills univers | Template + thème | `product.public.category` parentes | **Natif** | MOA validé |
| Produits vedettes | Snippet + thème | Snippet manuel ou sélection produits | Thème | Dynamique = phase 2+ |
| Réassurance | Thème / snippet | Snippet statique | Thème | — |
| Tokens | Thème | SCSS `dorevia_ck_theme` | Thème | Typo prod §10 |

**Verdict** : thème + snippets + catégories natives — **pas d’extension**.

---

## 5. Grille par zone — Entrée pro & formulaire

| Zone | Couche | Traduction Odoo | Phase 1 | Arbitrage |
|------|--------|-----------------|---------|-----------|
| Lien header « Professionnels » | Thème + CMS | Page `/professionnels` | Signal | §10 CMS vs CRM |
| Bandeau `/shop` pro | Snippet | Bloc brick & mortar | Signal | Texte MOA §10 |
| Page intention pro | CMS | Contenu référencement + approvisionnement | Signal | Rédaction MOA |
| Formulaire demande pro | Template + CRM | `website.form` ou lead `website_crm` | Signal | §10 |
| Prix publics site | Template natif | Pricelist B2C / défaut | **Natif** | Canal B2C CK — §2 |
| Portail B2B transactionnel | — | — | **Hors phase 1** | Interdit |
| Pricelists B2B partenaires | Métier Odoo | `product.pricelist` back-office | **Natif Odoo** | Partenaires qualifiés — hors exposition publique |

### Champs formulaire pro envisagés

| Champ | Usage |
|-------|-------|
| **Nature de la demande professionnelle** | Type de relation souhaitée avec CK — **pas** classification définitive du partenaire |
| Valeurs indicatives | Proposer offre / référencé fournisseur · Référencer produits / approvisionner · Conditions commerciales · Partenariat / autre |
| Type de professionnel | Producteur, transformateur · boutique, restaurant, hôtel, épicerie fine, distributeur… |
| Nom établissement / structure | Qualification |
| Pays / zone | Offre (fournisseur) ou distribution (distributeur) |
| Type de point de vente | Physique, mixte… (distributeurs) |
| Besoin | Référencement offre · Structuration catalogue · Approvisionnement · Contact commercial |
| Coordonnées | Email, téléphone |

### Parcours Odoo cible (phase 1 — qualification)

```text
website_crm / website.form → crm.lead
Qualification commerciale (nature de la demande)
Création ou rapprochement res.partner
Rôles client / fournisseur déterminés ensuite selon flux réels (un partenaire peut être les deux)
Rattachement product.pricelist partenaire qualifié (back-office Odoo)
```

---

## 6. Grille par zone — Page `/shop`

| Zone maquette | Couche | Traduction Odoo | Phase 1 | Arbitrage / recommandation |
|---------------|--------|-----------------|---------|---------------------------|
| Titre + promesse | Template + thème | `website_sale.products` | Natif | — |
| Catégories sidebar | Template + thème | `product.public.category` hiérarchiques | **Natif** | MOA validé |
| Filtre origines | Template ou extension | `product.attribute` « Origine » **ou** modèle dédié | À trancher | Dev : attribut phase 1 |
| Filtre collections | Template ou extension | Catégories secondaires / **tags** **ou** modèle custom | À trancher | **MOA : catégories/tags d’abord** |
| Filtre prix | Template ou extension | CE limité | À trancher | **Risque extension prématurée** — voir §8 |
| Tri | Template natif | `?order=` | Natif | — |
| Grille + carte « Voir » | Thème + template | Tuiles `website_sale` | Natif | Quick-add non retenu |
| Badge pack | Template | 1 produit Odoo | Template | Doctrine `non_detailed` §10 |
| Pagination | Template natif | Pager Odoo | Natif | — |
| Drawer filtres mobile | Thème | Offcanvas + liens URL | Thème | Pas JS catalogue |
| Bandeau pro | Snippet | Brick & mortar | Signal | — |

**Verdict `/shop`** : **majoritairement natif + thème**. Extensions limitées aux arbitrages §10.

---

## 7. Grille par zone — Fiche produit

| Zone | Couche | Traduction Odoo | Phase 1 |
|------|--------|-----------------|---------|
| Fil d’Ariane, galerie, buy box | Template natif + thème | `website_sale.product` | Natif |
| Chips origine / catégorie | Template + thème | Attribut + `public_categ_ids` | Natif à moyen |
| Usage éditorial | Template | `description_sale` | Natif |
| Réassurance | Thème / snippet | Bloc statique | Thème |
| Produits liés | Template natif | `alternative_product_ids` | Natif |
| Pack | Template | 1 ligne si `non_detailed` | §10 |

**Verdict fiche** : **100 % natif + thème** en phase 1.

---

## 8. Risques d’extension prématurée (MOA / Dev)

| Point | Risque | Recommandation grille |
|-------|--------|----------------------|
| **Filtre prix** | Traduction CE incertaine → tentation d’extension custom | **Simplifier ou reporter** plutôt qu’extension trop tôt |
| **Collections** | Reprise modèle `marketone.shop.collection` sans besoin démontré | **Catégories / tags d’abord** — modèle dédié seulement si besoin métier prouvé |
| **Origines** | Modèle dédié comme ancien Marketone | **`product.attribute` d’abord** |
| **Portail B2B** | Dérive ERP bis | **Interdit phase 1** |
| **Entrée pro** | Réduction à l’achat en volume ou confusion portail transactionnel | Qualifier **deux familles** (fournisseur + distributeur) — pas portail phase 1 |

```text
Séquence saine : thème + natif d’abord → extensions seulement après limite Odoo démontrée et arbitrage MOA.
```

---

## 9. Tableau de synthèse — Thème / Template / Extension

| Composant | Thème | Template natif | Extension | Statut |
|-----------|:-----:|:--------------:|:---------:|--------|
| Tokens SCSS | ● | | | Palette V1 — typo §10 |
| Header / footer | ● | ○ | | Thème |
| Hero + réassurance accueil | ● | ○ | | Snippet |
| Catégories hiérarchiques | ○ | ● | | **MOA validé** |
| Tuile + « Voir » | ● | ● | | Natif |
| Sidebar filtres (visuel) | ● | ○ | | Thème |
| Filtre origines | ○ | ○ | | **MOA** — attribut phase 1 |
| Filtre collections | ○ | ○ | | **MOA** — catégories / tags |
| Filtre prix | ○ | | | **MOA** — natif / simplifié ; report si extension |
| Tri / pagination | ○ | ● | | Natif |
| Fiche produit | ● | ● | | Natif |
| Entrée pro + bandeaux | ● | ○ | | Signal brick & mortar |
| Page + formulaire pro | ○ | ● | ○ | **MOA** — CMS + website_crm |
| Prix publics B2C | ○ | ● | | Natif — canal B2C CK |
| Pricelists B2B back-office | | ○ | | Natif Odoo — partenaires qualifiés |
| Portail B2B transactionnel | | | | **Hors phase 1** |
| Packs | ○ | ● | ○ | **MOA** — `non_detailed` validé |

Légende : ● = principale · ○ = contribution

---

## 10. Arbitrages §10 — décisions MOA

> Source arbitrage : [`note_transmission_arbitrage_david_01_v1_1.md`](./note_transmission_arbitrage_david_01_v1_1.md)

```text
Décisions MOA §10 complétées ≠ GO Dev général CK.
État historique avant addendum : le verrou Odoo restait maintenu.
Statut courant : verrou levé ticket 01 uniquement — squelette validé QA statique ;
recette fonctionnelle suspendée à instance Odoo 19 CE.
```

| # | Sujet | Décision MOA | Impact Dev immédiat |
|---|-------|--------------|---------------------|
| 1 | **Packs `non_detailed`** | ✅ 1 produit Odoo = 1 ligne panier — pas de détail composants phase 1 | Aucun |
| 2 | **Origines** | ✅ Attribut produit phase 1 — pas de modèle dédié sans limite démontrée | Aucun |
| 3 | **Collections** | ✅ Catégories / tags d’abord — modèle dédié exclu phase 1 | Aucun |
| 4 | **Filtre prix** | ✅ Natif / simplifié ; report si extension prématurée — extension non acceptée à ce stade | Aucun |
| 5 | **Entrée pro** | ✅ CMS + `website_crm` · page Pro unique · deux blocs · deux CTA · formulaire (nature demande) | Aucun |
| 6 | **Typo production** | ✅ Réévaluer avant build `dorevia_ck_theme` | Aucun |
| 7 | **Textes brick & mortar** | ✅ Doctrine validée · micro-évolution textuelle autorisée post-arbitrage | Aucun |
| 8 | **Verrou Odoo** | ✅ **Levé ticket 01** (2026-06-12) — maintenu hors ticket 01 | Exécution encadrée ticket 01 autorisée |

---

## 11. Interdits (inchangés)

```text
Catalogue / panier / checkout parallèles
Front React/Vue/SPA
Portail B2B transactionnel complet phase 1
Exposition publique des prix B2B phase 1
Workflow devis / commande pro complet phase 1
Reprise automatique dorevia_ckreyol_marketone
Développement Odoo hors ticket 01 validé MOA
```

---

## 12. Séquence après arbitrage MOA §10

```text
1. Arbitrages §10 actés MOA
2. Maquette V1.1.1 validée QA (adaptation Pro MOA)
3. ✅ Validation MOA note approche thème (snippets first)
4. ✅ Squelette validé QA statique — [`recette_qa_dorevia_ck_theme_01_squelette.md`](../recette_qa_dorevia_ck_theme_01_squelette.md)
5. ⏳ Base dev + website_sale (réserve opérationnelle instance)
6. ⏳ Recette QA fonctionnelle ticket 01
```

---

## 13. Synthèse MOA

> … Les arbitrages §10 sont tranchés côté MOA. Le verrou Odoo est **levé pour le ticket thème 01 uniquement** — exécution encadrée autorisée ; hors périmètre ticket 01, ticket séparé et validation MOA/QA requis.

---

## 14. Statut document

| Verdict QA/MOA sur brouillon | Statut v1 |
|------------------------------|-----------|
| Grille validable comme analyse MOA | **Oui** |
| Ticket de développement | **Oui — ticket 01 validé MOA** |
| Verrou Odoo | **Levé ticket 01 uniquement** |
| Arbitrages §10 | **Tranchés MOA** (note v1.1) |
| Maquette | **V1.1.1 validée QA** |
| Approche thème | [`note_approche_technique_dorevia_ck_theme_01.md`](../note_approche_technique_dorevia_ck_theme_01.md) — **validée MOA** |
| Ticket cadrage thème 1 | [`ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md`](../ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md) — **validé MOA · squelette validé QA statique** |
| Recette squelette | [`recette_qa_dorevia_ck_theme_01_squelette.md`](../recette_qa_dorevia_ck_theme_01_squelette.md) — **OK statique · fonctionnel suspendu** |
| En attente | **Recette QA fonctionnelle ticket 01** — [`REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md`](../REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md) |
