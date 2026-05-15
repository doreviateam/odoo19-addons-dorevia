# TICKET — Refondre le bloc newsletter homepage C-Kreyol

> **Implémentation livrée** — module `dorevia_ckreyol_marketplace` **[≥ 19.0.1.10.76](../../__manifest__.py)** :
> **`mass_mailing`** en dépendance ; liste **Newsletter C-Kreyol** (`data/ckr_mailing_list_newsletter.xml`, xmlid **`ckr_mailing_list_newsletter_ck`**) ;
> bloc QWeb **`ckr_snippet_circle`** (`views/snippets/ckr_circle.xml`) ; SCSS **`static/src/scss/components/_newsletter.scss`** ;
> **POST** **`/ckr/circle/subscribe`** ; redirections **`?cc_nl=`** : `ok` | `dup` | `invalid` | `err` .
> Nouvelles inscriptions → **`mailing.contact`** rattachés à cette liste. Le modèle **`ckr.circle.subscriber`** et la route **`/ckr/circle/unsubscribe/<token>`** restent pour l’historique.
> Ancien jeu de messages **`cc_cir`** abandonné pour ce bloc ; tests tag **`dorevia_ckr_circle`**.
>
> **GO MOA — rendu desktop** (2026-05) et gel UI : voir [PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md](PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md) § *GO visuel desktop & gel UI newsletter* ; recette finale (mobile, inscription, états, a11y) dans le même §.

---

## 1. Objectif

Refondre le bloc actuel d’inscription newsletter présent sur la homepage C-Kreyol.

Le bloc existant est aujourd’hui organisé comme une mini-page d’inscription centrée :

- label `REJOINDRE`
- titre `Rejoignez le cercle C-Kreyol`
- texte d’introduction
- champ email
- préférences optionnelles
- bouton pleine largeur
- texte court de consentement

Cette version doit être remplacée par un bloc newsletter plus sobre, horizontal, éditorial et mieux intégré à la homepage.

La nouvelle direction visuelle a été travaillée et confrontée à Stitch. Elle doit reprendre l’esprit suivant :

- bloc premium mais simple ;
- lecture rapide ;
- organisation horizontale sur desktop ;
- formulaire léger ;
- pas de logique de “club” ou de “cercle” en V1 ;
- pas de préférences optionnelles ;
- inscription email uniquement ;
- texte de réassurance clair sous le formulaire.

---

## 2. Intention produit

Le bloc newsletter doit être un appel discret à rester en relation avec C-Kreyol.

Il ne doit pas ressembler à une page d’adhésion ni à un formulaire communautaire complet.

L’intention est :

> Inviter le visiteur à recevoir les nouvelles, sélections et offres de C-Kreyol, sans perturber le parcours d’achat.

Le bloc doit rester compatible avec l’univers C-Kreyol :

- épicerie fine tropicale ;
- retail sobre ;
- éditorial calme ;
- non folklorique ;
- non agressif commercialement.

---

## 3. État actuel à remplacer

Le bloc actuel utilise notamment :

```text
REJOINDRE
Rejoignez le cercle C-Kreyol
Recevez des nouvelles du catalogue, des sélections saisonnières et des idées pour découvrir les saveurs créoles.
E-mail
Préférences (optionnel)
Offres / Recettes / Nouveautés
S’inscrire
En vous inscrivant, vous acceptez notre politique de confidentialité.
```

## Décision

Remplacer cette approche par un bloc newsletter simple.

À supprimer :

- le wording `REJOINDRE` ;
- le titre `Rejoignez le cercle C-Kreyol` ;
- la notion de “cercle” ;
- le bloc `Préférences (optionnel)` ;
- les cases à cocher `Offres`, `Recettes`, `Nouveautés` ;
- le formulaire vertical centré sur desktop ;
- le bouton pleine largeur sur desktop.

---

## 4. Nouveau contenu à intégrer

### Label

```text
NEWSLETTER
```

### Promesse principale

```text
Recevez nos sélections, découvertes et nouvelles de C-Kreyol
```

### Placeholder du champ email

```text
votre.adresse@email.com
```

### Bouton

```text
S’inscrire
```

### Texte de réassurance / RGPD

```text
Votre email est uniquement utilisé pour vous envoyer les nouvelles de C-Kreyol, nos sélections de produits et nos offres. Vous pouvez vous désabonner à tout moment via le lien présent dans chaque email.
```

---

## 5. Nouvelle structure UX attendue

Le bloc doit suivre cette organisation :

1. Label supérieur `NEWSLETTER`
2. Ligne principale :
   - promesse à gauche ;
   - champ email + bouton à droite.
3. Filet séparateur horizontal.
4. Texte de réassurance / RGPD sous le filet.

### Structure desktop indicative

```text
NEWSLETTER

Recevez nos sélections, découvertes et nouvelles de C-Kreyol        [votre.adresse@email.com][S’inscrire]

--------------------------------------------------------------------------------

Votre email est uniquement utilisé pour vous envoyer les nouvelles de C-Kreyol, nos sélections de produits et nos offres. Vous pouvez vous désabonner à tout moment via le lien présent dans chaque email.
```

---

## 6. Layout desktop attendu

Sur desktop, ne pas conserver le formulaire centré en colonne.

Le bloc doit être organisé en deux zones principales.

### Zone gauche

- label `NEWSLETTER`
- promesse principale

### Zone droite

- champ email
- bouton `S’inscrire`

### Règles desktop

- Le champ email et le bouton doivent être sur la même ligne.
- Le formulaire doit être placé à droite de la promesse.
- Le bouton ne doit pas être pleine largeur sur desktop.
- La promesse doit être le vrai point d’entrée visuel du bloc.
- Le formulaire doit être lisible, mais ne doit pas dominer le bloc.
- Le texte RGPD doit être sous le filet, pas collé au formulaire.
- L’ensemble doit rester aéré, mais moins “landing page” que l’existant.

---

## 7. Layout mobile attendu

Sur mobile, le bloc peut redevenir vertical.

Ordre attendu :

```text
NEWSLETTER

Recevez nos sélections, découvertes et nouvelles de C-Kreyol

[votre.adresse@email.com]

[S’inscrire]

--------------------------------------------------------------------------------

Votre email est uniquement utilisé pour vous envoyer les nouvelles de C-Kreyol, nos sélections de produits et nos offres. Vous pouvez vous désabonner à tout moment via le lien présent dans chaque email.
```

### Règles mobile

- Tout empiler en colonne.
- Champ email pleine largeur.
- Bouton pleine largeur sous le champ.
- Pas de préférences optionnelles.
- Texte RGPD lisible mais secondaire.
- Espacements confortables.
- Ne pas créer un bloc trop massif.

---

## 8. Direction visuelle attendue

La direction validée est celle d’un bloc sobre, horizontal, premium et éditorial.

À conserver de l’existant :

- fond crème / off-white ;
- typographie titre éditoriale / serif CK ;
- bouton brun / terracotta ;
- ambiance calme et premium ;
- respiration généreuse.

À modifier :

- passer d’une composition centrée verticale à une composition horizontale desktop ;
- remplacer l’approche “cercle / rejoindre” par une approche newsletter claire ;
- alléger la charge formulaire ;
- supprimer les préférences ;
- faire du texte RGPD une réassurance secondaire ;
- mieux intégrer le bloc dans le flux homepage.

---

## 9. Ajustements visuels précis

### Label `NEWSLETTER`

- Uppercase autorisé.
- Présence discrète.
- Éviter un letter-spacing trop luxueux ou trop distant.
- Le label doit introduire le bloc sans voler la vedette.

### Promesse principale

- Doit être plus forte que le texte RGPD.
- Typographie éditoriale CK.
- Taille suffisante pour être le point d’entrée du bloc.
- Ne pas rendre le texte trop gras ou trop promotionnel.

### Formulaire

- Champ email + bouton sur une seule ligne en desktop.
- Champ sobre avec bordure fine.
- Bouton plein brun / terracotta.
- Bouton lisible, sans letter-spacing excessif.
- Le formulaire doit être aligné visuellement avec la promesse.

### Filet séparateur

- Ajouter ou conserver un filet horizontal fin.
- Le filet doit séparer la ligne principale du texte RGPD.
- Trait doux, non dominant.

### Texte RGPD

- Sous le filet.
- Lisible, mais secondaire.
- Couleur légèrement atténuée possible.
- Ne doit pas concurrencer la promesse principale.

---

## 10. Fonctionnel Odoo

Utiliser autant que possible le mécanisme standard Odoo newsletter / mailing list.

### Liste cible

```text
Newsletter C-Kreyol
```

Si cette liste n’existe pas encore, signaler le besoin de création ou la créer selon les pratiques du module.

### Contraintes fonctionnelles

- Champ de type `email`.
- Validation email.
- Inscription uniquement sur action explicite.
- Pas de préférences en V1.
- Pas de popup.
- Pas d’inscription automatique.
- Pas de promesse de réduction.
- Pas de mécanique intrusive.

---

## 11. Messages attendus

### Email invalide

```text
Veuillez saisir une adresse email valide.
```

### Inscription réussie

```text
Merci, votre inscription a bien été prise en compte.
```

### Email déjà inscrit

```text
Cette adresse semble déjà inscrite à notre newsletter.
```

### Erreur technique

```text
L’inscription n’a pas pu être finalisée pour le moment. Vous pourrez réessayer dans quelques instants.
```

---

## 12. Accessibilité

Prévoir :

- un vrai label accessible pour le champ email ;
- un champ de type `email` ;
- un focus visible sur le champ ;
- un focus visible sur le bouton ;
- des contrastes suffisants ;
- des messages d’erreur compréhensibles sans dépendre uniquement de la couleur ;
- une navigation clavier correcte.

Le placeholder ne doit pas être le seul label fonctionnel.

---

## 13. Non-régression

Ne pas modifier :

- le hero ;
- les portes commerciales ;
- la sélection produits ;
- les blocs homepage existants hors remplacement du bloc newsletter ;
- le shop ;
- les filtres ;
- les chips ;
- les routes ;
- la doctrine catalogue ;
- les règles de canonicalisation.

Ne pas ajouter :

- popup ;
- JS tiers ;
- image lourde ;
- animation complexe ;
- tracking additionnel ;
- mécanique promotionnelle forcée.

---

## 14. Critères d’acceptation

### GO

La refonte est validée si :

- l’ancien bloc `Rejoignez le cercle C-Kreyol` est remplacé ;
- le nouveau label est `NEWSLETTER` ;
- la nouvelle promesse est intégrée ;
- les préférences `Offres / Recettes / Nouveautés` sont supprimées ;
- le rendu desktop est horizontal ;
- le champ email et le bouton sont alignés sur une même ligne en desktop ;
- le rendu mobile est empilé proprement ;
- le texte RGPD complet est présent sous le filet ;
- le bloc reste sobre, premium, éditorial et non agressif ;
- l’inscription fonctionne avec la liste `Newsletter C-Kreyol` ;
- les états succès / erreur sont gérés ;
- aucune régression n’est introduite sur la homepage ou le shop.

### NO GO

La refonte est refusée si :

- le bloc reste une mini-page d’inscription centrée sur desktop ;
- la notion de “cercle” est conservée ;
- les préférences optionnelles restent visibles ;
- le bouton reste pleine largeur sur desktop ;
- le RGPD domine visuellement la promesse ;
- une popup est ajoutée ;
- une promesse de réduction est ajoutée ;
- le formulaire casse sur mobile ;
- le bloc perturbe le parcours d’achat ;
- des éléments du shop sont modifiés sans lien direct.

---

## 15. Résumé exécutable

Refondre le bloc newsletter actuel de la homepage C-Kreyol.

Remplacer l’approche actuelle :

```text
REJOINDRE
Rejoignez le cercle C-Kreyol
Formulaire centré
Préférences optionnelles
Bouton pleine largeur
```

par un bloc newsletter horizontal desktop :

```text
NEWSLETTER

Recevez nos sélections, découvertes et nouvelles de C-Kreyol        [votre.adresse@email.com][S’inscrire]

--------------------------------------------------------------------------------

Votre email est uniquement utilisé pour vous envoyer les nouvelles de C-Kreyol, nos sélections de produits et nos offres. Vous pouvez vous désabonner à tout moment via le lien présent dans chaque email.
```

Objectif : un bloc plus léger, plus retail, plus intégré à la homepage, fidèle à la direction visuelle validée avec Stitch.
