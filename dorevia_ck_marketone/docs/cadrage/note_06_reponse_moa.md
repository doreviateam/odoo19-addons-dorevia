# Réponse MOA — Retour Dev principal sur Brief Navigation CK V2

| Champ | Valeur |
| --- | --- |
| **Projet** | C-Kreyol / CK Marketone |
| **Document concerné** | Brief MOA Navigation CK V2 · [`note_06.md`](./note_06.md) |
| **Réponse à** | Retour Dev principal · [`note_06_retour_dev.md`](./note_06_retour_dev.md) |
| **Décision MOA** | Arbitrages intégrés — poursuite vers version amendée du brief |
| **Statut** | Réponse MOA intégrée · prêt ticket Dev Lot Nav-1 |
| **Date** | 2026-06-21 |

---

## 1. Accusé de réception

La MOA prend acte du retour Dev principal sur le brief Navigation CK V2.

Le retour est jugé pertinent : il ne remet pas en cause la doctrine produit **Acheter · Apprendre · Contribuer**, mais met en évidence plusieurs arbitrages stratégiques restés implicites dans le brief initial.

La MOA confirme que ces points doivent être tranchés avant transformation du brief en ticket Dev exécutable.

---

## 2. Position MOA générale

La MOA confirme la doctrine cible :

> Acheter les produits du monde créole.
> Apprendre sur les produits, les usages, les cultures et les territoires.
> Contribuer aux savoirs, recettes, récits et pratiques autour de ces produits.

La MOA confirme également la distinction suivante :

* **Apprendre** = intention produit ;
* **Découvrir** = libellé de navigation.

Cette distinction reste structurante et ne doit pas être modifiée côté MOE sans nouvel arbitrage MOA.

---

## 3. Arbitrage 1 — Pivot de navigation

### Décision MOA

La MOA assume le **pivot de navigation**.

La Navigation CK V2 n’est pas considérée comme un simple renommage du header V1.2 existant. Elle constitue une évolution volontaire de l’architecture de navigation, afin d’aligner le header avec la stratégie produit CK :

> Acheter · Apprendre · Contribuer.

L’écart avec le header actuellement livré n’est donc pas une anomalie, mais un pivot maîtrisé à intégrer dans le cadrage du Lot Navigation.

### Conséquence

Le header existant :

> Boutique · Découvrir · Professionnels

doit être considéré comme la structure de phase initiale.

La cible Navigation V2 devient :

> Tous nos produits · Épicerie · Boissons · Soin · Artisanat · Découvrir

---

## 4. Arbitrage 2 — Place de « Professionnels »

### Décision MOA

L’entrée **Professionnels** ne doit plus être une entrée top-level du menu principal.

Elle doit être relocalisée dans **Découvrir**.

La MOA ne souhaite pas supprimer le parcours Professionnels. Elle souhaite le repositionner dans l’espace d’écosystème, d’attachement et de relation CK.

### Justification

Le menu principal doit rester prioritairement marchand et orienté catalogue B2C.

L’espace **Découvrir** porte les dimensions :

* apprendre ;
* comprendre ;
* relation producteurs / territoires ;
* communauté ;
* contribution ;
* écosystème professionnel.

### Sous-menu Découvrir cible amendé

Ordre cible proposé :

> Producteurs & territoires
> Histoires de produits
> Recettes & usages
> Le blog CK
> Professionnels
> Communauté
> Contribuer

La MOA considère que cette relocalisation évite la régression fonctionnelle signalée par le Dev : l’entrée Professionnels reste accessible, mais elle ne concurrence plus les catégories marchandes dans le menu principal.

---

## 5. Arbitrage 3 — Taxonomie catalogue

### Décision MOA

La MOA valide la taxonomie commerciale racine suivante :

> Épicerie · Boissons · Soin · Artisanat

Cette taxonomie est considérée comme suffisamment claire, large et durable pour porter le menu principal CK.

### Demande MOE associée

La MOA accepte néanmoins la recommandation Dev de produire un tableau de correspondance opérationnel :

| Entrée menu | Catégorie Odoo cible | URL / slug | Statut | Produit publié minimum |
| --- | --- | --- | --- | --- |
| Tous nos produits | Catalogue complet | `/shop` | Existant / à confirmer | Oui |
| Épicerie | Catégorie racine Épicerie | À confirmer | À confirmer / créer si besoin | Oui |
| Boissons | Catégorie racine Boissons | À confirmer | À confirmer / créer si besoin | Oui |
| Soin | Catégorie racine Soin | À confirmer | À confirmer / créer si besoin | Oui |
| Artisanat | Catégorie racine Artisanat | À confirmer | À confirmer / créer si besoin | Oui |

La taxonomie est donc validée stratégiquement, mais doit être sécurisée techniquement côté BO Odoo.

---

## 6. Règle de visibilité des liens

La MOA valide la règle Dev suivante :

> Un lien ne doit apparaître en navigation que si la cible existe, est publiée et ne génère pas de 404.

Cela vaut pour :

* les catégories produits ;
* les pages CMS ;
* les entrées du sous-menu Découvrir ;
* les éventuelles pages teaser.

Si une cible n’est pas prête, l’entrée doit être masquée ou différée, sauf décision MOA explicite de publier une page teaser.

---

## 7. Découvrir — clarification de rôle

La MOA confirme que **Découvrir** ne doit plus porter une logique « Acheter par univers » si les univers marchands sont déjà remontés au top-level.

La logique cible est donc :

### Menu principal

> Acheter / catalogue

### Découvrir

> Apprendre / relation / culture / communauté / contribution / professionnels

Conséquence :

> Le mega-menu Découvrir ne doit pas dupliquer les entrées commerce principales.

---

## 8. Home S4 — position MOA

La MOA prend acte du risque d’incohérence entre le nouveau header et la section Home S4 actuellement structurée autour de trois univers.

Décision MOA à ce stade :

> Le Lot Navigation ne doit pas modifier la Home S4.

La cohérence header ↔ Home S4 ↔ catégories BO devra être contrôlée, mais toute modification de la Home S4 devra faire l’objet d’un arbitrage MOA séparé ou d’un ticket distinct.

Objectif : ne pas mélanger le chantier Navigation avec une reprise de la Home.

---

## 9. Phase 1 — Livrable attendu Lot Nav-1

Le Lot Nav-1 devra porter uniquement sur la navigation.

Périmètre attendu :

* mise en place du menu principal cible ;
* relocalisation de Professionnels dans Découvrir ;
* création / synchronisation des menus nécessaires ;
* respect des règles de visibilité des liens ;
* vérification des catégories BO nécessaires ;
* adaptation des tests header existants ;
* recette desktop et mobile 390 px ;
* non-régression recherche, compte, panier, accès boutique et accès professionnels.

Hors périmètre Lot Nav-1 :

* refonte Home S4 ;
* refonte fiche produit ;
* forum complet ;
* système de contribution utilisateur ;
* modération ;
* compte contributeur ;
* marketplace ;
* refonte panier / checkout.

---

## 10. Critères de validation complémentaires

La MOA ajoute les critères suivants au brief amendé :

1. le pivot de navigation est explicitement assumé ;
2. Professionnels est relocalisé dans Découvrir ;
3. la taxonomie racine Épicerie / Boissons / Soin / Artisanat est validée ;
4. chaque entrée navigation doit pointer vers une cible existante et publiée ;
5. Découvrir ne doit pas dupliquer les entrées commerce principales ;
6. le Lot Nav-1 ne modifie pas la Home S4 ;
7. la cohérence header ↔ catégories BO ↔ pages publiées doit être vérifiée ;
8. la recette mobile 390 px est obligatoire ;
9. les tests header existants doivent être mis à jour en cohérence avec la cible Navigation V2.

---

## 11. Verdict MOA

> **RETOUR DEV ACCEPTÉ — ARBITRAGES MOA INTÉGRÉS — BRIEF AMENDÉ · PRÊT TICKET DEV LOT NAV-1**

La MOA demande la production d’une version amendée du brief Navigation CK V2 intégrant les arbitrages ci-dessus.

Après validation de cette version amendée, un ticket Dev Lot Nav-1 pourra être rédigé sur un périmètre strictement borné.

**Intégration** : arbitrages repris dans [`note_06.md`](./note_06.md) (révision 2026-06-21).

**Exécution Dev** : [`TICKET_DEV_LOT_NAV1_NAVIGATION_CK_V2.md`](../design/TICKET_DEV_LOT_NAV1_NAVIGATION_CK_V2.md).
