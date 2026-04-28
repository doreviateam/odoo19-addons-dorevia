# MVP2.3 — Page produit

**Statut du document** : cadrage **UX / structure / doctrine d’implémentation** pour la fiche produit C-Kreyol en continuité de la logique MVP2.x (raffinement, compatibilité Odoo, non-régression).  
**Références amont** : cohérence de ton et de sincérité avec [PLATEFORME_MARQUE_CK_V1.md](../crea/PLATEFORME_MARQUE_CK_V1.md) et [ARCHITECTURE_DECISION_RECORD.md](../direction/ARCHITECTURE_DECISION_RECORD.md) (notamment ADR-CKR-002 et ADR-CKR-005).

**Documents d’exécution associés** :

- **Ticket d’exécution** : [TICKET_PRODUCT_PAGE_MVP23.md](../crea/TICKET_PRODUCT_PAGE_MVP23.md)
- **PV de recette** : [PV_RECETTE_PRODUCT_PAGE_MVP23.md](../crea/PV_RECETTE_PRODUCT_PAGE_MVP23.md)

> Toute évolution qui touche aux routes catalogue, au domaine métier produit ou au moteur de filtrage du shop sort du périmètre de ce document et doit être traitée dans les contrats `mvp_01` / boutique.

---

## 0. Intentions et écarts à corriger (analyse)

La fiche produit actuelle repose sur une base saine (deux colonnes, média principal, prix, achat, sections basses), mais plusieurs points nuisent à la lisibilité et à la compréhension :

- l’origine apparaît comme une option interactive au lieu d’une information éditoriale ;
- la hiérarchie titre / promesse / prix / description manque de rythme ;
- les médias additionnels sont sous-exploités ;
- le bloc réassurance est utile mais insuffisamment structuré ;
- les informations basses sont trop proches d’un bloc technique brut.

La cible MVP2.3 n’est pas une refonte totale : c’est un **durcissement de grammaire** pour obtenir une fiche plus claire, plus crédible et plus convertissante.

---

## 1. Objectif de la vague

Définir une fiche produit C-Kreyol qui combine :

- chaleur éditoriale ;
- efficacité e-commerce ;
- lisibilité immédiate ;
- sobriété visuelle ;
- maintenabilité Odoo.

La page doit aider l’utilisateur à répondre rapidement à quatre questions :

1. Quel est ce produit ?
2. D’où vient-il ?
3. Pourquoi est-il intéressant ?
4. Puis-je acheter en confiance ?

---

## 2. Invariants d’orchestration (bloquants)

Ces invariants s’appliquent à toute implémentation :

1. **Deux colonnes conservées** sur desktop :
   - gauche = médias ;
   - droite = information et achat.
2. **Un seul flux d’action principal** dans le bloc droit :
   - quantité + ajout panier prioritaires ;
   - wishlist / comparaison restent secondaires.
3. **Origine non interactive** :
   - jamais rendue comme case à cocher ;
   - toujours traitée en information produit.
4. **Progressivité du détail** :
   - haut de page court et orienté décision ;
   - détail étendu en sections basses.
5. **Compatibilité native d’abord** :
   - pas de composant custom fragile quand Odoo couvre le besoin ;
   - pas de rupture de comportements standard produit.

---

## 3. Structure cible de la page

Organisation cible :

1. Bloc haut en deux colonnes (média / achat).
2. Zone de confiance et d’informations transactionnelles dans la colonne droite.
3. Sections basses de détail produit.
4. Recommandations en pied si source disponible.

Principe directeur : **raffiner la fiche existante**, pas réinventer l’architecture.

---

## 4. Colonne gauche — Galerie média produit

### 4.1 Image principale

L’image principale reste prioritaire, grande, immédiatement lisible.

### 4.2 Médias additionnels

Quand plusieurs médias existent en back-office :

- afficher des miniatures sous l’image principale (orientation préférée) ;
- permettre un changement d’image simple, sans interaction lourde ;
- garder un rendu propre lorsqu’un seul média est disponible ;
- éviter les widgets complexes non nécessaires.

Types de médias attendus (quand disponibles) :

- packshot ;
- détail produit / étiquette ;
- ambiance ;
- suggestion d’usage ;
- visuel origine / terroir.

---

## 5. Colonne droite — Information et conversion

### 5.1 Ordre de lecture cible

Ordre recommandé du haut vers le bas :

1. Origine (badge ou ligne info non interactive)
2. Titre produit
3. Phrase de promesse courte
4. Prix
5. Description courte
6. Zone d’achat (quantité + CTA)
7. Actions secondaires (wishlist / comparaison)
8. Réassurance

### 5.2 Règles par bloc

- **Origine** : libellé clair, discret, non cliquable comme option.
- **Titre** : élément dominant du bloc droit.
- **Promesse** : phrase courte sous le titre (bénéfice immédiat).
- **Prix** : visible rapidement, sans effet visuel agressif.
- **Description courte** : 2–4 lignes max, orientée usage / désirabilité.
- **Achat** : CTA “Ajouter au panier” clairement prioritaire.
- **Secondaires** : présence possible, poids visuel inférieur.

---

## 6. Bloc réassurance (colonne droite)

Le bloc réassurance doit être court, stable et lisible.

Exemples de contenus (à adapter à la vérité opérationnelle) :

- expédition sous délai maîtrisé ;
- paiement sécurisé ;
- support client ;
- politique satisfaction.

Règles :

- pas de promesse non tenue ;
- pas de surcharge graphique ;
- formulation sobre et crédible.

---

## 7. Sections basses — Détail produit

Les sections basses doivent éviter l’effet “mur de texte technique”.

Sections recommandées :

- description complète ;
- ingrédients / composition ;
- conservation ;
- conseils d’utilisation / dégustation ;
- informations techniques.

Rendu autorisé :

- sections simples ;
- ou accordéons légers si comportement stable.

---

## 8. Recommandations en bas de page

Section affichée uniquement si la donnée est disponible et fiable.

Libellé type : `Vous aimerez aussi`.

Peut valoriser :

- produits de même famille ;
- produits complémentaires ;
- produits de même origine ;
- produits de même collection.

Doctrine :

- exploiter le natif Odoo si simple ;
- sinon reporter la sophistication en V2.

---

## 9. Périmètre V1 exécutable

Inclus dans la vague :

- conservation de la structure deux colonnes ;
- galerie média simple avec miniatures ;
- conversion de l’origine en information non interactive ;
- hiérarchie claire titre / promesse / prix / description ;
- clarification de la zone quantité + ajout panier ;
- allègement visuel des actions secondaires ;
- création ou rationalisation d’un bloc réassurance ;
- organisation lisible des sections basses ;
- non-régression des comportements Odoo.

---

## 10. Hors périmètre V1

Exclus de cette passe :

- refonte globale header / architecture site ;
- changement des URLs catalogue ;
- redesign lourd du tunnel panier / checkout ;
- moteur d’avis avancé ;
- cross-sell complexe non natif ;
- composants front trop custom ou difficiles à maintenir ;
- refonte mobile lourde hors ajustements essentiels.

---

## 11. Arbitrages MOA à valider avant ticket dev

1. **Galerie** : miniatures sous l’image (préféré) vs latérales.
2. **Recommandations** : incluses V1 si natif exploitable, sinon report.
3. **Sections basses** : sections ouvertes vs accordéons.
4. **Promesse courte** : source de donnée (champ dédié, description courte, éditorial).
5. **Réassurance** : contenu statique site vs paramétrable.

---

## 12. Critères d’acceptation (GO / NO GO)

La livraison est conforme si :

- la lecture de la fiche est plus claire à structure constante ;
- l’origine n’est jamais présentée comme option interactive ;
- la hiérarchie du bloc droit est immédiatement compréhensible ;
- la zone d’achat est identifiable sans effort ;
- le bloc réassurance est lisible et non envahissant ;
- la galerie gère correctement les cas 1 média et multi-médias ;
- les sections basses structurent le détail sans lourdeur ;
- aucune régression Odoo produit n’est observée.

---

## 13. Recette minimale attendue

Recette fonctionnelle à mener après livraison :

- produit avec un seul média ;
- produit avec plusieurs médias ;
- produit avec et sans origine renseignée ;
- produit avec et sans description courte ;
- vérification CTA ajout panier + quantité ;
- vérification affichage wishlist/comparaison selon configuration ;
- vérification responsive essentiel (desktop / mobile).

Traçabilité attendue :

- ticket d’exécution dédié ;
- PV de recette MVP2.3 page produit.

---

## 14. Doctrine de conduite

La page produit est améliorée par **raffinement progressif**.

La priorité n’est pas de produire un écran spectaculaire, mais une fiche :

- claire ;
- crédible ;
- rassurante ;
- désirable ;
- maintenable.

Principe de mise en oeuvre :

> Odoo d’abord, C-Kreyol par-dessus, sans sur-ingénierie.

---

## 15. Statut et suite

Statut actuel : cadrage MOA consolidé (version amendée dans la logique MVP2.x).

Prochaine étape :

1. valider les arbitrages §11 ;
2. produire le ticket d’exécution page produit ;
3. implémenter avec non-régression ;
4. recetter puis geler la vague si critères §12 atteints.

---

## 16. Historique

| Date | Événement |
|------|-----------|
| *(version initiale)* | Cadrage UX page produit (intention, structure, périmètre, critères). |
| 2026-04-28 | Amendement structurel “logique MVP2.x” : invariants bloquants, périmètre exécutable, doctrine de non-régression, recette minimale et trajectoire ticket/PV. |