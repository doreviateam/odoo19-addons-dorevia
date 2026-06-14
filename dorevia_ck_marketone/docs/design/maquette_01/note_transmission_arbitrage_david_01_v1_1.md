# Note de transmission — arbitrage MOA §10 (v1.1)

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Destinataire** | David / arbitrage MOA interne |
| **Document source** | [`grille_traduction_odoo_v1.md`](./grille_traduction_odoo_v1.md) |
| **Références** | Maquette V1.1 validée QA · `design_01.md` v1.1 · `revue_dev_traduisibilite_odoo.md` |
| **Date** | 2026-06-12 |
| **Statut** | **Arbitrages §10 complétés côté MOA** — voir encadré statut courant ci-dessous |
| **Remplace** | [`note_transmission_arbitrage_david_01.md`](./note_transmission_arbitrage_david_01.md) (v1) |
| **Grille alignée** | [`grille_traduction_odoo_v1.md`](./grille_traduction_odoo_v1.md) §10 mis à jour |

### État courant après addendum (lecture prioritaire)

```text
État courant après addendum : le verrou Odoo est levé uniquement pour le ticket 01
dorevia_ck_theme. Le GO général CK n’est pas donné. La recette fonctionnelle du
squelette reste suspendée à la mise à disposition d’une instance Odoo 19 CE.
```

Références : addendum § fin de document · [`recette_qa_dorevia_ck_theme_01_squelette.md`](../recette_qa_dorevia_ck_theme_01_squelette.md).

Les mentions « verrou maintenu » ou « Architecture Odoo = toujours verrouillée »
dans le corps du document = **état historique avant addendum**, sauf addendum et suite.

---

## Objet

La maquette CK V1.1 est validée QA/MOA. La grille de traduction Odoo v1 est validée comme **document d’analyse MOA** — pas comme ticket de développement.

Cette note formalise les **8 arbitrages §10 côté MOA** avant toute implémentation Odoo.

```text
Recommandation grille ≠ Décision MOA
```

Les formulations « Recommandation grille » ci-dessous sont des propositions MOA/Dev. Les décisions MOA ci-dessous font foi pour la suite du cadrage.

---

## Contexte validé (hors arbitrage)

| Point | Statut |
|-------|--------|
| Nature du document | Grille d’analyse MOA, pas ordre de développement |
| Verrou Odoo | **Maintenu** *(état historique avant addendum)* — jusqu’à décision explicite MOA de levée du verrou |
| Séquence | Thème + natif d’abord ; extensions seulement après limite Odoo démontrée |
| Catégories e-commerce phase 1 | `product.public.category` hiérarchiques |
| Répartition ~55 / 35 / 10 | Estimation indicative de complexité, non engagement de charge ou de périmètre |
| Front autonome / catalogue parallèle | Interdit |
| Maquette V1.1 | **Validée QA — stable**, pas de refonte demandée |
| Évolution maquette | Micro-ajustement **textes Pro** possible **après** arbitrage David — pas prérequis maintenant |

```text
Maquette V1.1 = stable.
Textes Pro = ajustables après arbitrage.
Architecture Odoo = toujours verrouillée. (État historique avant addendum.)
```

### Doctrine brick & mortar (validée MOA)

> CK valorise les producteurs et transformateurs créoles, tout en soutenant les distributeurs physiques — boutiques, épiceries, restaurants, hôtels, concept stores et revendeurs — qui souhaitent référencer et proposer ces produits à leurs propres clients.

> L’entrée professionnelle phase 1 est une **porte de qualification commerciale**, non un **portail B2B transactionnel**.

### Matrice fournisseur / distributeur (doctrine complémentaire MOA)

CK = plateforme d’intermédiation commerciale et logistique entre deux pôles :

| Pôle | Archétype | Rôle |
|------|-----------|------|
| Offre | **La Platine** | Producteurs / transformateurs créoles |
| Demande | **Kemet Exotique** | Commerces physiques spécialisés (brick & mortar) |

> **CK connecte des producteurs créoles comme La Platine à des commerces spécialisés comme Kemet Exotique, avec un catalogue structuré, une logistique maîtrisée et une expérience d’achat professionnelle.**

Chaîne économique cible :

```text
Producteurs / transformateurs créoles → CK → boutiques / épiceries / restaurants / distributeurs → consommateurs finaux
```

Le B2C reste vitrine et vente directe ; l’entrée pro phase 1 qualifie **deux familles** — fournisseurs **et** distributeurs.

### Boussole stratégique MOA (lecture David)

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

**Deux faces complémentaires de CK :**

| Face | Chaîne |
|------|--------|
| **B2B structurante** | Fournisseurs créoles → CK → distributeurs européens |
| **B2C directe** | CK → consommateurs finaux |

Cette formulation ne modifie pas la séquence documentaire ni le verrou Odoo.

### Doctrine prix B2C / B2B (validée MOA)

```text
Visiteur non identifié / client B2C → prix public CK
Partenaire B2B identifié / qualifié → liste de prix Odoo → prix personnalisé
```

```text
Pas d’exposition publique des prix B2B en phase 1.
Les prix publics affichés correspondent au canal B2C CK.
Les conditions commerciales B2B sont gérables en back-office Odoo via les listes de prix, pour les partenaires qualifiés.
L’exposition d’un parcours B2B transactionnel complet reste hors phase 1.
```

```text
Prix publics B2C affichés sur le site ≠ conditions commerciales B2B personnalisées via listes de prix Odoo.
```


---

## Synthèse des décisions MOA §10

| # | Sujet | Décision MOA | Impact Dev immédiat |
|---|-------|--------------|---------------------|
| 1 | Packs | `non_detailed` validé : 1 produit Odoo = 1 ligne panier | Aucun |
| 2 | Origines | Attribut produit en phase 1 | Aucun |
| 3 | Collections | Catégories / tags d’abord | Aucun |
| 4 | Filtre prix | Natif / simplifié ; report si extension nécessaire | Aucun |
| 5 | Entrée Pro | Page CMS + formulaire CRM, double cible fournisseur / distributeur | Aucun |
| 6 | Typographie | Réévaluation avant build thème | Aucun |
| 7 | Textes brick & mortar | Doctrine validée, micro-évolution textuelle possible | Aucun |
| 8 | Verrou Odoo | **Maintenu** *(état historique avant addendum)* | **Aucune action Dev** *(au moment de l’arbitrage §10)* |

```text
Décisions MOA §10 complétées ≠ GO Dev.
Le verrou Odoo reste maintenu. (État historique avant addendum.)
```

## Arbitrages §10 — décisions MOA

### 1. Packs `non_detailed`

**Enjeu** : un pack = une ligne panier (doctrine existante) ou détail des composants ?

| | |
|---|---|
| **Recommandation grille** | Aligner sur la doctrine pack existante : **1 produit Odoo = 1 ligne panier** (`non_detailed`). |
| **Décision MOA** | ✅ Validé — pack = **1 produit Odoo = 1 ligne panier** (`non_detailed`). Pas de détail des composants en phase 1. |

---

### 2. Origines

**Enjeu** : filtre et affichage des origines (Martinique, Guadeloupe, etc.) — attribut natif ou modèle dédié ?

| | |
|---|---|
| **Recommandation grille** | **Attribut produit en phase 1**, sauf limite fonctionnelle démontrée. |
| **Décision MOA** | ✅ **Attribut produit en phase 1**. Pas de modèle dédié tant qu’une limite Odoo n’est pas démontrée. |

---

### 3. Collections

**Enjeu** : filtres « collections » sur `/shop` — réutiliser le natif ou créer un modèle custom ?

| | |
|---|---|
| **Recommandation grille** | **Catégories / tags d’abord**, modèle dédié uniquement si besoin métier démontré. |
| **Décision MOA** | ✅ **Catégories / tags d’abord**. Modèle dédié exclu en phase 1, sauf besoin métier démontré plus tard. |

---

### 4. Filtre prix

**Enjeu** : slider / fourchette de prix sur `/shop` — faisable en natif CE ou extension nécessaire ?

| | |
|---|---|
| **Recommandation grille** | **Simplifier ou reporter** si la traduction Odoo CE impose une extension prématurée. |
| **Décision MOA** | ✅ **Natif / simplifié phase 1**. Si le filtre prix impose une extension prématurée, il est reporté. Extension non acceptée à ce stade. |

---

### 5. Entrée pro — CMS vs `website_crm` + UX double cible

**Enjeu** : porter le signal « Professionnels » pour **deux familles** — fournisseurs (La Platine) et distributeurs (Kemet Exotique) — sans réduire l’entrée pro à un achat en volume.

**Couche technique — CMS vs CRM :**

| Option | Description |
|--------|-------------|
| A | Page CMS d’intention seule |
| B | `website_crm` / formulaire CRM seul |
| C | Page CMS + formulaire simple raccordable CRM |

**UX double cible — à trancher explicitement :**

| Option | Description |
|--------|-------------|
| A | Page Pro unique avec deux blocs : « Je suis producteur / transformateur » · « Je suis distributeur / boutique / restaurant » |
| B | Deux CTA distincts : « Proposer vos produits » · « Référencer des produits créoles » |
| C | Formulaire unique avec champ de qualification de la demande (voir nuance ci-dessous) |
| D | Deux formulaires séparés plus tard |
| E | Autre option David |

**Nuance MOA — champ formulaire (non classification définitive du partenaire)**

Le champ ne doit **pas** figer le partenaire dans un rôle unique. Dans Odoo, un même `res.partner` peut être client, fournisseur, ou les deux, selon les flux réels avec CK.

```text
Formulaire Pro → lead CRM (website_crm) → qualification commerciale
→ création ou rapprochement du partenaire
→ rôles client / fournisseur déterminés ensuite dans Odoo selon les flux réels
```

**Libellé recommandé** : « Nature de la demande professionnelle » ou « Type de relation souhaitée avec CK ».

**Valeurs possibles** :

```text
Proposer une offre / être référencé comme fournisseur
Référencer des produits créoles / approvisionner un point de vente
Demander des conditions commerciales
Partenariat / autre demande professionnelle
```

`website_crm` est **pertinent en phase 1** comme outil de capture et qualification commerciale.

| | |
|---|---|
| **Recommandation grille** | **Phase 1** : page Pro unique + deux blocs clairs + deux CTA distincts + formulaire unique (nature de la demande, pas classification définitive) + couche technique **option C** (CMS + `website_crm`). Pas de portail B2B transactionnel complet. Conditions B2B via listes de prix Odoo back-office — pas d’exposition publique des prix B2B. |
| **Décision MOA — CMS/CRM** | ✅ **Option C** — page CMS + formulaire simple raccordable CRM (`website_crm`). |
| **Décision MOA — UX double cible** | ✅ **Combinaison recommandée MOA** : page Pro unique + deux blocs + deux CTA + formulaire unique avec champ de qualification. Pas de deux formulaires séparés en phase 1. |

---

### 6. Typographie production

**Enjeu** : Fraunces + DM Sans (maquette) — conserver en production ou réévaluer avant build thème ?

| | |
|---|---|
| **Recommandation grille** | Réévaluer avant build `dorevia_ck_theme` (self-host, licence, perf). |
| **Décision MOA** | ✅ **Réévaluer avant build** `dorevia_ck_theme` : licence, self-host, performance et cohérence Odoo. |

---

### 7. Texte brick & mortar / matrice fournisseur-distributeur

**Enjeu** : formulations définitives page pro, bandeaux `/shop` et accueil — incluant les deux archétypes (La Platine, Kemet Exotique), la phrase de synthèse CK et la nuance prix B2C / conditions B2B.

**Pas de correction maquette obligatoire maintenant** — micro-évolution textuelle éventuelle après arbitrage (maquette V1.1 reste stable).

**Exemples illustratifs post-arbitrage** (non engagement) :

```text
Vous êtes producteur ou transformateur créole ?
Proposez vos produits et structurez votre offre avec CK.

Vous êtes boutique, restaurant, hôtel ou distributeur ?
Référencez des produits créoles et approvisionnez votre point de vente.

Les prix affichés publiquement correspondent au canal B2C CK.
Les partenaires professionnels qualifiés peuvent bénéficier de conditions commerciales personnalisées via Odoo.
```

| | |
|---|---|
| **Recommandation grille** | S’appuyer sur la doctrine et la matrice validées (ci-dessus) ; rédaction MOA à finaliser après arbitrage. |
| **Décision MOA** | ✅ Doctrine validée. Micro-évolution textuelle autorisée après arbitrage, sans refonte maquette et sans impact Dev immédiat. |

---

### 8. Verrou Odoo *(état historique avant addendum)*

**Enjeu** : autoriser ou non le démarrage technique (base dev, `dorevia_ck_theme`, QWeb/SCSS).

| | |
|---|---|
| **État actuel** *(au moment de l’arbitrage §10)* | Verrou **maintenu** — aucune base, aucun thème, aucun QWeb/SCSS. |
| **Décision MOA** *(§10 initial)* | ✅ **Maintenir le verrou Odoo**. Aucun démarrage technique, aucune base dev, aucun `dorevia_ck_theme`, aucun QWeb/SCSS. |

> **Statut courant** : levée du verrou **ticket 01 uniquement** — cf. addendum en fin de document.

---

## Décisions MOA actées

```text
La grille v1 est-elle validée comme base de traduction Odoo ?
Les arbitrages §10 sont-ils tranchés côté MOA ?
Le verrou Odoo est-il maintenu ou levé explicitement ?
```

| Question | Décision MOA |
|----------|--------------|
| Grille v1 validée comme base de traduction Odoo ? | ✅ Oui, comme base de cadrage / traduction, pas comme ticket Dev. |
| Arbitrages §10 tranchés ? | ✅ Oui, côté MOA, selon décisions ci-dessus. |
| Verrou Odoo | ✅ Maintenu *(décision §10 initiale — état historique avant addendum)*. |

---

## Rappel impératif *(état historique avant addendum)*

```text
Aucun développement Odoo ne démarre tant que la levée du verrou Odoo
n’est pas explicitement décidée côté MOA.
```

Même après validation de la grille et tranchage des arbitrages §10 : **pas de base dev, pas de `dorevia_ck_theme`, pas de QWeb/SCSS** sans GO explicite ultérieur de levée du verrou Odoo.

> **Statut courant** : GO encadré ticket 01 acté · squelette validé QA statique · recette fonctionnelle suspendée à instance — cf. addendum ci-dessous.

---

## Addendum — GO exécution encadré ticket 01 (2026-06-12)

Décision MOA ultérieure au §8 ci-dessus :

| Question | Décision MOA |
|----------|--------------|
| Ticket `dorevia_ck_theme_01` validé ? | ✅ Oui — cadrage d’exécution |
| Verrou Odoo | ✅ **Levé ticket 01 uniquement** |
| Exécution | ✅ Autorisée — périmètre strict ticket 01 |
| GO général CK | ❌ Non |
| Squelette thème | ✅ Validé QA statique · recette fonctionnelle suspendée à instance |
| Instance Odoo | Réserve opérationnelle — prochaine étape recette fonctionnelle |

Détail : [`ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md`](../ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md) §0.

---

## Suite après arbitrage MOA

1. ~~Intégrer les décisions MOA §10 dans la grille~~ — fait dans `grille_traduction_odoo_v1.md` §10.
2. ~~Adaptation maquette Pro MOA~~ — **QA validée V1.1.1** · [`recette_qa_maquette_01_1.md`](./recette_qa_maquette_01_1.md).
3. ~~Validation MOA~~ : [`note_approche_technique_dorevia_ck_theme_01.md`](../note_approche_technique_dorevia_ck_theme_01.md) — **validée MOA** · snippets first · pas de surcouche autonome.
4. ~~Validation MOA ticket 01~~ — **validé MOA** · GO exécution encadré · [`ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md`](../ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md).
5. ~~Levée verrou Odoo ticket 01~~ — **faite** — verrou maintenu hors ticket 01.
6. ~~Squelette `dorevia_ck_theme`~~ — **validé QA statique** · [`recette_qa_dorevia_ck_theme_01_squelette.md`](../recette_qa_dorevia_ck_theme_01_squelette.md).
7. **Prochaine étape** : instance Odoo 19 CE + installation module + recette QA fonctionnelle.
8. Extensions uniquement si limite Odoo démontrée — ticket séparé + arbitrage MOA.

---

*Document d’arbitrage MOA — synthèse orientée décision. Détail complet : [`grille_traduction_odoo_v1.md`](./grille_traduction_odoo_v1.md).*
