# TICKET — Page produit MVP2.3

**ID** : `PRODUCT-PAGE-MVP23`  
**Date d’ouverture** : 2026-04-28  
**Priorité** : **P1** (conversion et lisibilité fiche produit)  
**Statut** : **Prêt pour dev** (cadrage MOA validé, exécution à lancer)  
**Module** : `dorevia_ckreyol_marketplace`  
**Périmètre** : page fiche produit Odoo e-commerce (template produit, styles associés, non-régression fonctionnelle).

**Document source (opposable)** : [3_PRODUCT_PAGE.md](../mvp_02/3_PRODUCT_PAGE.md)

---

## Contexte

Le cadrage MOA de la fiche produit est validé en **MVP2.3** : objectif de raffinement progressif, sans refonte globale, avec priorité à la compatibilité native Odoo et à la non-régression.

Ce ticket exécute le cadrage **sans rouvrir les arbitrages MOA** déjà posés.

---

## Objectif

Livrer une fiche produit plus lisible, plus crédible et plus efficace commercialement, tout en conservant la structure standard Odoo :

- deux colonnes desktop (médias à gauche, information/achat à droite) ;
- hiérarchie claire du bloc droit ;
- origine affichée comme information non interactive ;
- zone d’achat immédiatement identifiable ;
- détail produit mieux structuré en sections basses.

---

## Invariants bloquants (à respecter strictement)

Conformes au document [3_PRODUCT_PAGE.md](../mvp_02/3_PRODUCT_PAGE.md) :

1. **Deux colonnes conservées** en desktop.
2. **Un flux d’action principal unique** : quantité + ajout panier.
3. **Origine non interactive** : jamais rendue comme option sélectionnable dans cette vague ; toute navigation future par origine relève d’un ticket séparé.
4. **Progressivité du détail** : haut de fiche décisionnel, détail en bas.
5. **Compatibilité native d’abord** : pas de sur-ingénierie front.

Tout écart à ces invariants = **hors ticket** (nouvel arbitrage MOA requis).

---

## Périmètre exécutable

### 1) Colonne gauche — médias

- Conserver une image principale prioritaire.
- Activer une galerie simple quand plusieurs médias existent.
- Afficher des miniatures sous l’image principale (orientation MOA retenue dans le cadrage).
- Assurer un rendu propre en cas de média unique.

### 2) Colonne droite — information et conversion

Ordre de lecture à implémenter :

1. Origine (badge ou ligne info non interactive)
2. Titre produit
3. Phrase courte de promesse
4. Prix
5. Description courte
6. Zone d’achat (quantité + CTA)
7. Actions secondaires (wishlist / comparaison si disponibles)
8. Bloc réassurance

Règle de fallback :

- Si aucune source propre n’est disponible pour la phrase courte de promesse, le bloc est masqué (pas de génération artificielle).

### 3) Zone d’achat

- CTA `Ajouter au panier` clairement prioritaire.
- Actions secondaires visuellement plus discrètes.
- Lisibilité immédiate sans alourdir le bloc.

### 4) Bloc réassurance

- Bloc court, lisible, non envahissant.
- Contenu aligné à la réalité opérationnelle (pas de promesse non tenue).

### 5) Sections basses

- Structurer le détail produit (description, composition, conservation, usage, infos techniques).
- Rendu en sections simples ou accordéons légers selon faisabilité stable.
- Les sections ne doivent apparaître que si les données correspondantes existent (ou si Odoo fournit déjà un contenu fiable) ; ne pas créer de sections vides.

### 6) Recommandations bas de page

- Activer uniquement si la donnée est disponible nativement/exploitable simplement.
- Ne pas introduire de logique complexe dédiée en MVP2.3.

---

## Hors périmètre (non négociable)

- Refonte globale header / architecture site ;
- changements d’URL catalogue ;
- refonte checkout/panier ;
- moteur d’avis avancé ;
- cross-sell complexe non natif ;
- composants custom lourds ;
- refonte mobile lourde hors ajustements essentiels.

---

## Livrables techniques attendus

| Livrable | Détail |
|----------|--------|
| **QWeb** | Ajustements template fiche produit pour hiérarchie bloc droit, origine non interactive, galerie simple, sections basses lisibles. |
| **SCSS** | Ajustements de rythme visuel (espaces, hiérarchie, poids CTA/secondaires, bloc réassurance) sans rupture Design System. |
| **Intégration** | Non-régression des comportements Odoo natifs (prix, variante, quantité, ajout panier, wishlist/comparaison si modules actifs). |
| **Recette** | PV dédié : [PV_RECETTE_PRODUCT_PAGE_MVP23.md](PV_RECETTE_PRODUCT_PAGE_MVP23.md). |

---

## Critères d’acceptation (GO / NO GO)

- [ ] Structure deux colonnes conservée (desktop) ;
- [ ] Origine affichée en information non interactive ;
- [ ] Hiérarchie du bloc droit claire (titre/promesse/prix/desc/achat) ;
- [ ] Zone d’achat immédiatement identifiable ;
- [ ] CTA panier prioritaire vs actions secondaires ;
- [ ] Bloc réassurance lisible et sobre ;
- [ ] Galerie correcte en cas 1 média et multi-médias ;
- [ ] Sections basses plus lisibles que l’état initial ;
- [ ] Aucune régression fonctionnelle Odoo sur la fiche produit ;
- [ ] Rendu cohérent avec la direction visuelle C-Kreyol.

---

## Plan d’exécution recommandé

1. **Lot A — structure/ordre bloc droit** : origine, promesse, hiérarchie visuelle, zone achat.
2. **Lot B — galerie médias** : miniatures + fallback 1 média.
3. **Lot C — réassurance + sections basses** : lisibilité et progressivité du détail.
4. **Lot D — QA non-régression** : parcours achat standard, responsive essentiel, modules optionnels.

---

## Dépendances / hypothèses

- Les données produit (origine, description courte, médias) sont renseignées côté BO de façon minimale.
- Les modules optionnels (wishlist/comparaison) peuvent varier selon environnement : le rendu doit rester propre dans les deux cas.
- Aucune évolution du domaine métier catalogue n’est introduite dans ce ticket.

---

## Preuve de recette

PV à compléter après livraison : [PV_RECETTE_PRODUCT_PAGE_MVP23.md](PV_RECETTE_PRODUCT_PAGE_MVP23.md).

---

## 0. Prêt pour dev — checklist

1. [x] Cadrage source validé : [3_PRODUCT_PAGE.md](../mvp_02/3_PRODUCT_PAGE.md) (MVP2.3).
2. [x] Invariants bloquants repris dans le ticket.
3. [x] Hors périmètre explicitement figé.
4. [x] Critères GO / NO GO définis.
5. [ ] Implémentation dev réalisée.
6. [ ] PV de recette rempli et signé MOA.

---

## Historique

| Date | Changement |
|------|------------|
| 2026-04-28 | Création ticket exécutable MVP2.3 à partir du cadrage `3_PRODUCT_PAGE.md` ; doctrine non-régression et périmètre strict page produit. |
