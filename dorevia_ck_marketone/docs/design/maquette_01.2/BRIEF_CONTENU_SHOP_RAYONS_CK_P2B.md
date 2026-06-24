# Brief contenu — Shop CK P2B · pages rayon editorialisees

| Champ | Valeur |
| --- | --- |
| Date | 2026-06-23 |
| Objet | Preparer les contenus necessaires pour transformer les pages `/shop` et `/shop/category/...` en vrais rayons boutique editorialises. |
| Statut | Brief MOA a completer avant implementation Dev P2B |
| Reference | Benchmark grammaire e-commerce : BienManger, page categorie editorialisee |
| Dependances | Assets photo, textes courts, sous-familles alimentees, produits associes |
| Hors perimetre | Refonte moteur Odoo, contenu saisonnier invente, categories vides, notation produit factice |

---

## 0. Source taxonomique de reference

Le P2B ne doit pas creer une deuxieme taxonomie de sous-familles.

Les sous-familles affichees dans les pages rayon doivent rester alignees avec la taxonomie Header CK V2.2 deja figee MOA et implementee dans :

```text
dorevia_ck_marketone_content/nav_v22_config.py
```

Decision MOA :

```text
Header mega-menu et pages rayon doivent partager le meme decoupage fonctionnel.
P2B ajoute une couche editoriale et merchandising,
mais ne renomme pas les familles sans arbitrage global.
```

Si une evolution de taxonomie devient souhaitable, elle devra etre traitee comme une evolution transverse :

- mise a jour du brief P2B ;
- mise a jour de `nav_v22_config.py` ;
- verification des mega-menus header ;
- verification des pages rayon ;
- recette de coherence navigation.

---

## 1. Objectif

Le P2A a densifie les cards produit et allege le CTA panier.

Le P2B doit traiter le vrai ecart avec une boutique mature :

```text
ne plus afficher seulement une grille de produits,
mais construire une page de rayon avec contexte, sous-familles, preuves et selections.
```

Chaque page rayon prioritaire doit pouvoir repondre a quatre questions :

1. Quel univers suis-je en train d'explorer ?
2. Quelles sous-familles utiles puis-je parcourir ?
3. Pourquoi ces produits sont-ils credibles / identifies / selectionnes ?
4. Quels produits ou selections sont mis en avant maintenant ?

---

## 2. Pages prioritaires

Ordre recommande :

| Priorite | Page | Raison | Statut (2026-06-23) |
| --- | --- | --- | --- |
| P1 | `/shop` | Porte d'entree generale de la boutique. | Actif |
| P1 | `/shop/category/epicerie-...` | Rayon le plus structurant pour CK. | **Actif — seul rayon pilote P2B** |
| Differe | `/shop/category/boissons-...` | Rayon lisible et marchand, bon terrain pour sous-familles. | Differe — 1 seul produit publie au total |
| Differe | `/shop/category/maison-bien-etre-...` | Rayon differenciant, besoin d'explication et de confiance. | Differe — 1 seul produit publie au total |
| Differe | `/shop/category/artisanat-...` | A activer seulement si contenu suffisant. | Differe — 1 seul produit publie au total |

### 2.1 Arbitrage MOA du 2026-06-23 — recentrage sur Epicerie

Audit catalogue effectue le 2026-06-23 (cf. migration `19.0.1.35.0` et verification live) :

```text
Epicerie    : 3 familles resolues, 4 produits publies -> seuil §6 atteint
Boissons    : 1 famille resolue,  1 produit publie    -> sous le seuil
Soin & Bien-etre (categorie reelle ; le brief disait "Maison & Bien-etre") :
              1 famille resolue,  1 produit publie    -> sous le seuil
Artisanat   : 0 famille resolue,  1 produit publie    -> sous le seuil
```

Verification faite produit par produit : ce n'est pas un probleme de produits non publies
(tous les produits existants sont deja publies), c'est un catalogue reellement incomplet
pour ces 3 rayons — aucun stock cache a activer.

Decision MOA : **P2B est recentre sur Epicerie seul** jusqu'a ce qu'un vrai catalogue existe
pour Boissons / Soin & Bien-etre / Artisanat. Ces 3 rayons restent en grille simple (etat
actuel), sans traitement editorial complet, conformement a la regle §6 :
*"Si ces conditions ne sont pas remplies : conserver une version allegee, ne pas afficher
une profondeur artificielle."*

A noter pour une prochaine iteration : la categorie reelle en base s'appelle
**"Soin & Bien-etre"**, pas "Maison & Bien-etre" comme ecrit en §5.4/§9.4 — a harmoniser
(renommage categorie ou correction du brief) avant toute production de contenu sur ce rayon.

---

## 3. Structure cible d'une page rayon

Chaque page rayon doit suivre cette grammaire :

```text
1. Header de rayon editorialise
2. Sous-familles / chemins de navigation
3. Preuves CK contextualisees
4. Mise(s) en avant commerciale(s) ou saisonniere(s)
5. Transition vers grille produits
6. Grille produits + filtres
```

La structure doit rester compacte. L'objectif n'est pas de creer une landing page longue avant les produits.

---

## 4. Contenus a fournir par rayon

### 4.1 Image lifestyle ou visuel de rayon

Pour chaque rayon prioritaire :

| Champ | Attendu |
| --- | --- |
| Type | Photo lifestyle, scene produit, texture alimentaire ou composition naturelle. |
| Role | Installer l'univers du rayon. |
| Format souhaite | Paysage large, exploitable en bandeau compact. |
| Qualite | Lumineux, lisible, non generique, compatible CK. |
| Interdit | Image sombre, stock trop neutre, visuel qui ne montre pas le produit ou l'usage. |

Fallback autorise :

```text
Si aucune image qualifiee n'existe, utiliser une surface editoriale sobre,
mais ne pas simuler un hero lifestyle avec un placeholder faible.
```

### 4.2 Phrase editoriale courte

Longueur recommandee :

```text
120 a 180 caracteres maximum.
```

Role :

- expliquer le rayon ;
- donner envie ;
- rester marchand ;
- eviter le discours institutionnel.

Exemples de ton :

```text
Epicerie :
Saveurs creoles, condiments, douceurs et essentiels du quotidien selectionnes pour leur origine et leur savoir-faire.

Boissons :
Jus, nectars, infusions et boissons creoles pour retrouver les parfums des iles a chaque moment de la journee.

Maison & Bien-etre :
Soins, savons, senteurs et objets utiles pour faire entrer les matieres et gestes creoles dans le quotidien.
```

### 4.3 Sous-familles utiles

Pour chaque rayon, fournir 3 a 6 sous-familles maximum.

Regle :

```text
Une sous-famille ne doit etre affichee que si elle mene a du contenu reel.
```

Sous-familles de reference :

#### Epicerie

- Biscuits & crackers
- Confitures & douceurs
- Farines & manioc
- Sauces & condiments
- Chocolat & cacao
- Cafe & infusions

#### Boissons

- Jus & nectars
- Sirops creoles
- Boissons locales
- Boissons fraiches si activees
- Aperitifs & boissons festives
- Preparations a boire

#### Maison & Bien-etre

- Savons & soins solides
- Huiles & baumes
- Senteurs & bougies
- Maison & decoration
- Accessoires bien-etre
- Rituels creoles

#### Artisanat

- Objets decoratifs
- Arts de la table
- Textile & accessoires
- Bijoux & creations
- Papeterie & affiches
- Creations artisanales

### 4.4 Mise en avant commerciale ou saisonniere

Pour chaque rayon prioritaire, fournir 1 a 3 tuiles maximum.

Types possibles :

- nouveaute rayon ;
- selection saison ;
- produit ou famille a pousser ;
- origine a valoriser ;
- producteur a mettre en avant ;
- coffret ou idee cadeau.

Format attendu :

| Champ | Exemple |
| --- | --- |
| Titre | `Le manioc a l'honneur` |
| Texte court | `Farines, galettes et crackers autour d'un essentiel creole.` |
| Lien | Categorie, tag, produit ou page producteur |
| Image | Optionnelle mais recommandee |

Regle :

```text
Pas de tuile saisonniere sans contenu reel derriere.
```

### 4.5 Preuves CK contextualisees

Preuves reutilisables :

- Origines identifiees ;
- Produits selectionnes ;
- Expedition depuis Nantes ;
- Livraison suivie ;
- Producteurs et partenaires visibles.

Sur les pages rayon, ces preuves doivent etre courtes et proches du contexte d'achat.

Exemple :

```text
Origines identifiees
Chaque produit est rattache a une origine, un producteur ou un partenaire connu lorsque l'information est disponible.
```

---

## 5. Fiche brief par rayon

### 5.1 Boutique generale `/shop`

| Champ | A remplir |
| --- | --- |
| Titre | Boutique C-Kreyol |
| Phrase courte | A definir |
| Image / visuel | A fournir ou fallback sobre |
| Sous-familles | Epicerie · Boissons · Maison & Bien-etre · Artisanat · Coups de coeur |
| Mise en avant 1 | A definir |
| Mise en avant 2 | A definir |
| Mise en avant 3 | A definir |
| Preuves | Produits selectionnes · Origines identifiees · Expedition depuis Nantes · Livraison suivie |

### 5.2 Epicerie

| Champ | A remplir |
| --- | --- |
| Titre | Epicerie creole |
| Phrase courte | A definir |
| Image / visuel | A fournir |
| Sous-familles | Biscuits & crackers · Confitures & douceurs · Farines & manioc · Sauces & condiments · Chocolat & cacao · Cafe & infusions |
| Mise en avant 1 | A definir |
| Mise en avant 2 | A definir |
| Mise en avant 3 | A definir |
| Producteur / origine a valoriser | A definir |

### 5.3 Boissons

| Champ | A remplir |
| --- | --- |
| Titre | Boissons creoles |
| Phrase courte | A definir |
| Image / visuel | A fournir |
| Sous-familles | Jus & nectars · Sirops creoles · Boissons locales · Boissons fraiches si activees · Aperitifs & boissons festives · Preparations a boire |
| Mise en avant 1 | A definir |
| Mise en avant 2 | A definir |
| Mise en avant 3 | A definir |
| Producteur / origine a valoriser | A definir |

### 5.4 Maison & Bien-etre

| Champ | A remplir |
| --- | --- |
| Titre | Maison & Bien-etre |
| Phrase courte | A definir |
| Image / visuel | A fournir |
| Sous-familles | Savons & soins solides · Huiles & baumes · Senteurs & bougies · Maison & decoration · Accessoires bien-etre · Rituels creoles |
| Mise en avant 1 | A definir |
| Mise en avant 2 | A definir |
| Mise en avant 3 | A definir |
| Producteur / origine a valoriser | A definir |

### 5.5 Artisanat

| Champ | A remplir |
| --- | --- |
| Titre | Artisanat |
| Phrase courte | A definir |
| Image / visuel | A fournir si rayon active |
| Sous-familles | Objets decoratifs · Arts de la table · Textile & accessoires · Bijoux & creations · Papeterie & affiches · Creations artisanales |
| Mise en avant 1 | A definir |
| Mise en avant 2 | A definir |
| Mise en avant 3 | A definir |
| Condition | Activer uniquement si contenu suffisant |

---

## 6. Regles de publication

Une page rayon peut recevoir le traitement editorial complet si elle dispose au minimum de :

- 1 titre valide ;
- 1 phrase courte validee ;
- 3 sous-familles ou chemins utiles alimentes ;
- 1 preuve CK contextualisee ;
- 1 image qualifiee ou fallback sobre assume ;
- au moins 4 produits publies ou publiables dans le rayon.

Si ces conditions ne sont pas remplies :

```text
Conserver une version allegee.
Ne pas afficher une profondeur artificielle.
```

---

## 7. Attendus Dev apres brief contenu

Une fois le brief rempli, le Dev pourra :

- creer la structure de bloc rayon ;
- brancher les donnees categories/sous-categories ;
- afficher les mises en avant si disponibles ;
- masquer automatiquement les elements incomplets ;
- generer les captures de recette ;
- documenter les fallbacks.

---

## 8. Verdict MOA

Le P2B n'est pas un simple polish visuel.

C'est le lot qui doit permettre a CK de passer de :

```text
page shop propre
```

a :

```text
rayon boutique editorialise, organise et marchand
```

Il doit etre lance avec un brief contenu minimal par rayon pour eviter de fabriquer une vitrine vide.

---

## 9. Proposition MOA V0 a arbitrer

Cette section propose une premiere base de contenu pour lancer la reflexion.

Statut :

```text
Proposition MOA V0
A relire, ajuster et valider avant transmission Dev P2B.
```

### 9.1 Boutique generale `/shop`

| Champ | Proposition V0 |
| --- | --- |
| Titre | Boutique C-Kreyol |
| Phrase courte | Epicerie creole, boissons, bien-etre et creations selectionnes avec des origines identifiees et une expedition depuis Nantes. |
| Image / visuel | Composition large : produits CK varies sur table claire, touches creoles, matieres naturelles, sans surcharge. |
| Sous-familles | Epicerie · Boissons · Maison & Bien-etre · Artisanat · Coups de coeur |
| Mise en avant 1 | `Les essentiels creoles` — Condiments, douceurs, manioc et boissons pour composer une premiere selection CK. |
| Mise en avant 2 | `Origines identifiees` — Decouvrir les produits rattaches a une ile, un producteur ou un partenaire connu. |
| Mise en avant 3 | `Coups de coeur CK` — La selection courte des produits a mettre en avant maintenant. |
| Preuves | Produits selectionnes · Origines identifiees · Expedition depuis Nantes · Livraison suivie |

Intention :

```text
La boutique generale doit servir de porte d'entree claire.
Elle doit orienter vers les rayons sans devenir une page institutionnelle.
```

### 9.2 Epicerie

| Champ | Proposition V0 |
| --- | --- |
| Titre | Epicerie creole |
| Phrase courte | Confitures, manioc, condiments, cacao, cafes et douceurs creoles selectionnes pour leur gout, leur origine et leur usage au quotidien. |
| Image / visuel | Table epicerie : pot de confiture, manioc/farine, crackers, cacao/cafe, cuillere ou tissu naturel. |
| Sous-familles | Biscuits & crackers · Confitures & douceurs · Farines & manioc · Sauces & condiments · Chocolat & cacao · Cafe & infusions |
| Mise en avant 1 | `Le manioc a l'honneur` — Farines, galettes, crackers et produits autour d'un essentiel creole. |
| Mise en avant 2 | `Douceurs des iles` — Confitures, cacao, cafe et notes sucrees pour le petit-dejeuner ou le cadeau. |
| Mise en avant 3 | `Pour relever la cuisine` — Sauces, condiments et saveurs pour retrouver les gestes creoles. |
| Producteur / origine a valoriser | La Platine ou Sweet Manihot si fiches et produits associes sont qualifies. |

Intention :

```text
Epicerie est le rayon prioritaire P2B.
C'est le meilleur candidat pour montrer l'effet "rayon mature" en premier.
```

### 9.3 Boissons

| Champ | Proposition V0 |
| --- | --- |
| Titre | Boissons creoles |
| Phrase courte | Jus, nectars, sirops et boissons locales pour retrouver les parfums des iles, du quotidien aux moments de partage. |
| Image / visuel | Verres lumineux, bouteille/jus, fruits tropicaux, table claire, ambiance fraiche et naturelle. |
| Sous-familles | Jus & nectars · Sirops creoles · Boissons locales · Boissons fraiches si activees · Aperitifs & boissons festives · Preparations a boire |
| Mise en avant 1 | `Jus & nectars` — Des boissons fruites pour le quotidien et les moments conviviaux. |
| Mise en avant 2 | `Sirops creoles` — A servir frais, en cuisine ou en boisson maison. |
| Mise en avant 3 | `Boissons festives` — A activer uniquement si produits et perimetre legal sont valides. |
| Producteur / origine a valoriser | A definir selon marques/produits disponibles. |

Intention :

```text
Boissons doit rester frais, simple et marchand.
Ne pas forcer les boissons festives si le contenu ou les contraintes legales ne sont pas prets.
```

### 9.4 Maison & Bien-etre

| Champ | Proposition V0 |
| --- | --- |
| Titre | Maison & Bien-etre |
| Phrase courte | Savons, baumes, senteurs et accessoires pour faire entrer les matieres, parfums et gestes creoles dans le quotidien. |
| Image / visuel | Savon, bougie/senteur, textile clair, feuille ou matiere vegetale, salle de bain ou coin maison lumineux. |
| Sous-familles | Savons & soins solides · Huiles & baumes · Senteurs & bougies · Maison & decoration · Accessoires bien-etre · Rituels creoles |
| Mise en avant 1 | `Rituels du quotidien` — Savons, soins solides et gestes simples pour la routine. |
| Mise en avant 2 | `Senteurs & maison` — Bougies, parfums et objets pour l'ambiance. |
| Mise en avant 3 | `Matieres naturelles` — A activer seulement si les produits permettent de soutenir cette promesse. |
| Producteur / origine a valoriser | A definir selon artisans/marques qualifies. |

Intention :

```text
Maison & Bien-etre doit rassurer.
Eviter un discours cosmétique trop medical ou des promesses produit non verifiees.
```

### 9.5 Artisanat

| Champ | Proposition V0 |
| --- | --- |
| Titre | Artisanat |
| Phrase courte | Objets, accessoires et creations en petites series pour offrir, decorer et faire vivre les savoir-faire creoles. |
| Image / visuel | Detail de creation, objet sur table, main/artisan si disponible, ambiance cadeau ou decoration. |
| Sous-familles | Objets decoratifs · Arts de la table · Textile & accessoires · Bijoux & creations · Papeterie & affiches · Creations artisanales |
| Mise en avant 1 | `Creations a offrir` — A activer si plusieurs produits cadeau sont disponibles. |
| Mise en avant 2 | `Objets pour la maison` — A activer si objets decoratifs / arts de la table alimentes. |
| Mise en avant 3 | `Petites series` — A activer uniquement si la promesse est vraie cote stock/fournisseurs. |
| Condition | Traitement editorial complet uniquement si au moins 3 familles sont alimentees. |

Intention :

```text
Artisanat reste conditionnel.
Ne pas afficher un grand rayon editorialise si le contenu ne tient pas encore la promesse.
```

### 9.6 Priorite de production conseillee

```text
Mise a jour 2026-06-23 : cf. §2.1 — P2B recentre sur Epicerie seul.
Boissons / Soin & Bien-etre / Artisanat differes jusqu'a catalogue suffisant.
```

Ordre de travail actif :

1. `/shop` general : porte d'entree.
2. `Epicerie` : rayon pilote P2B — **seule priorite active**.

Differe (a reprendre uniquement quand le catalogue le permet, cf. §2.1) :

3. `Boissons`
4. `Soin & Bien-etre`
5. `Artisanat`

### 9.7 Images a produire ou selectionner

Besoin minimal pour lancer P2B proprement :

| Page | Asset minimal |
| --- | --- |
| `/shop` | 1 composition multi-produits CK |
| Epicerie | 1 photo rayon epicerie |
| Boissons | 1 photo boissons |
| Maison & Bien-etre | 1 photo soins/senteurs/maison |
| Artisanat | 1 photo creation artisanale, seulement si rayon active |

Regle :

```text
Mieux vaut un fallback sobre qu'une image faible.
Le visuel doit soutenir le rayon, pas faire decor generique.
```
