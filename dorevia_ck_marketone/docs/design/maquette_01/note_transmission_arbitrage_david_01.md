# Note de transmission — arbitrage David (grille traduction Odoo v1)

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Destinataire** | David |
| **Document source** | [`grille_traduction_odoo_v1.md`](./grille_traduction_odoo_v1.md) |
| **Références** | Maquette V1.1 validée QA · `design_01.md` v1.1 · `revue_dev_traduisibilite_odoo.md` |
| **Date** | 2026-06-12 |
| **Statut** | **Remplacée** par [`note_transmission_arbitrage_david_01_v1_1.md`](./note_transmission_arbitrage_david_01_v1_1.md) — arbitrages §10 actés MOA |

---

## Objet

La maquette CK V1.1 est validée QA/MOA. La grille de traduction Odoo v1 est validée comme **document d’analyse MOA** — pas comme ticket de développement.

Cette note demande à David de trancher les **8 arbitrages §10** avant toute implémentation Odoo.

```text
Recommandation grille ≠ Décision David
```

Les formulations « Recommandation grille » ci-dessous sont des propositions MOA/Dev. Seules les réponses de David font foi.

---

## Contexte validé (hors arbitrage)

| Point | Statut |
|-------|--------|
| Nature du document | Grille d’analyse MOA, pas ordre de développement |
| Verrou Odoo | **Maintenu** jusqu’à décision explicite de David |
| Séquence | Thème + natif d’abord ; extensions seulement après limite Odoo démontrée |
| Catégories e-commerce phase 1 | `product.public.category` hiérarchiques |
| Répartition ~55 / 35 / 10 | Estimation indicative de complexité, non engagement de charge ou de périmètre |
| Front autonome / catalogue parallèle | Interdit |
| Maquette V1.1 | **Validée QA — stable**, pas de refonte demandée |
| Évolution maquette | Micro-ajustement **textes Pro** possible **après** arbitrage David — pas prérequis maintenant |

```text
Maquette V1.1 = stable.
Textes Pro = ajustables après arbitrage.
Architecture Odoo = toujours verrouillée.
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

## Arbitrages §10 — à trancher

### 1. Packs `non_detailed`

**Enjeu** : un pack = une ligne panier (doctrine existante) ou détail des composants ?

| | |
|---|---|
| **Recommandation grille** | Aligner sur la doctrine pack existante : **1 produit Odoo = 1 ligne panier** (`non_detailed`). |
| **Décision David** | ☐ Validé · ☐ Autre : _______________ |

---

### 2. Origines

**Enjeu** : filtre et affichage des origines (Martinique, Guadeloupe, etc.) — attribut natif ou modèle dédié ?

| | |
|---|---|
| **Recommandation grille** | **Attribut produit en phase 1**, sauf limite fonctionnelle démontrée. |
| **Décision David** | ☐ Attribut · ☐ Modèle dédié · ☐ Reporter |

---

### 3. Collections

**Enjeu** : filtres « collections » sur `/shop` — réutiliser le natif ou créer un modèle custom ?

| | |
|---|---|
| **Recommandation grille** | **Catégories / tags d’abord**, modèle dédié uniquement si besoin métier démontré. |
| **Décision David** | ☐ Catégories / tags · ☐ Modèle dédié · ☐ Reporter |

---

### 4. Filtre prix

**Enjeu** : slider / fourchette de prix sur `/shop` — faisable en natif CE ou extension nécessaire ?

| | |
|---|---|
| **Recommandation grille** | **Simplifier ou reporter** si la traduction Odoo CE impose une extension prématurée. |
| **Décision David** | ☐ Natif / simplifié phase 1 · ☐ Reporter · ☐ Extension acceptée |

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
| **Décision David — CMS/CRM** | ☐ A · ☐ B · ☐ C · ☐ Autre : _______________ |
| **Décision David — UX double cible** | ☐ A · ☐ B · ☐ C · ☐ D · ☐ E · ☐ Combinaison recommandée MOA |

---

### 6. Typographie production

**Enjeu** : Fraunces + DM Sans (maquette) — conserver en production ou réévaluer avant build thème ?

| | |
|---|---|
| **Recommandation grille** | Réévaluer avant build `dorevia_ck_theme` (self-host, licence, perf). |
| **Décision David** | ☐ Conserver maquette · ☐ Réévaluer · ☐ Autre : _______________ |

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
| **Décision David** | ☐ Doctrine validée telle quelle · ☐ Micro-évolution textuelle post-arbitrage · ☐ Ajustements : _______________ |

---

### 8. Verrou Odoo

**Enjeu** : autoriser ou non le démarrage technique (base dev, `dorevia_ck_theme`, QWeb/SCSS).

| | |
|---|---|
| **État actuel** | Verrou **maintenu** — aucune base, aucun thème, aucun QWeb/SCSS. |
| **Décision David** | ☐ Maintenir le verrou · ☐ Lever explicitement le verrou |

---

## Décisions attendues de David

```text
David valide-t-il la grille comme base de traduction Odoo ?
David tranche-t-il les arbitrages §10 ?
David maintient-il ou lève-t-il explicitement le verrou Odoo ?
```

| Question | Réponse David |
|----------|---------------|
| Grille v1 validée comme base de traduction Odoo ? | ☐ Oui · ☐ Non · ☐ Sous réserve : _______________ |
| Arbitrages §10 tranchés ? | ☐ Oui (tous) · ☐ Partiellement · ☐ Non |
| Verrou Odoo | ☐ Maintenu · ☐ Levé explicitement |

---

## Rappel impératif

```text
Aucun développement Odoo ne démarre tant que la levée du verrou Odoo
n’est pas explicitement décidée par David.
```

Même validation de la grille et tranchage des arbitrages §10 : **pas de base dev, pas de `dorevia_ck_theme`, pas de QWeb/SCSS** sans GO explicite sur le point 8.

---

## Suite après retour David

1. Intégrer les décisions dans la grille v1 (ou version v1.1).
2. Si verrou levé → ticket `dorevia_ck_theme` (tokens + layout uniquement).
3. Extensions uniquement si limite Odoo démontrée post-thème et conforme aux arbitrages.

---

*Document de transmission — synthèse orientée décision. Détail complet : [`grille_traduction_odoo_v1.md`](./grille_traduction_odoo_v1.md).*
