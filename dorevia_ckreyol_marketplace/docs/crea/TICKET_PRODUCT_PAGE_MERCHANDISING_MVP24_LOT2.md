# TICKET — Page produit merchandising MVP2.4 Lot 2

**ID** : `PRODUCT-PAGE-MERCH-MVP24-LOT2`  
**Date d’ouverture** : 2026-04-28  
**Priorité** : **P2** (méthode durable d’enrichissement catalogue)  
**Statut** : **Prêt pour cadrage exécution**  
**Module** : `dorevia_ckreyol_marketplace`  
**Périmètre** : chantier contenu/merchandising durable sur fiches produit, sans refonte technique.

**Références** :  
- [TICKET_PRODUCT_PAGE_MVP23.md](TICKET_PRODUCT_PAGE_MVP23.md)  
- [PV_RECETTE_PRODUCT_PAGE_MVP23.md](PV_RECETTE_PRODUCT_PAGE_MVP23.md)  
- [TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24.md](TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24.md)  
- [PV_RECETTE_PRODUCT_PAGE_MERCHANDISING_MVP24.md](PV_RECETTE_PRODUCT_PAGE_MERCHANDISING_MVP24.md)

---

## Contexte

Le template produit MVP2.3 et le Lot 1 MVP2.4 sont posés.  
Le besoin du Lot 2 est d’installer une méthode durable d’enrichissement éditorial et merchandising, pilotable et maintenable, sans rouvrir l’architecture technique.

---

## Objectif

Industrialiser l’enrichissement des fiches produit via :

- une charte éditoriale claire ;
- une matrice de contenu opérationnelle ;
- des standards médias homogènes ;
- des règles simples de recommandations ;
- un backlog d’enrichissement progressif.

---

## Invariants bloquants (non négociables)

1. **Ne pas rouvrir** le template MVP2.3.
2. **Ne pas rouvrir** le Lot 1 MVP2.4.
3. **Aucune refonte technique** (routes shop, moteur catalogue, checkout, logique complexe custom).
4. **Compatibilité Odoo d’abord** (natif et maintenable).
5. **Pas de section vide** visible côté fiche.

---

## Périmètre exécutable Lot 2

## 1) Charte éditoriale fiche produit

Produire une charte opposable avec exemples concrets :

- **Promesse courte** : claire, spécifique, non marketing creux.
- **Description utile** : aide à l’achat (composition, goût, usage, bénéfice client).
- **Bénéfices / usages** : exprimés sans surpromesse.
- **Ton C-Kreyol** : chaleureux, authentique, lisible.
- **Sincérité des informations** : aucune allégation non vérifiable.

Livrable attendu : guide éditorial court + exemples “à faire / à éviter”.

## 2) Matrice de contenu par fiche

Définir une matrice simple par statut de fiche :

- **Champs obligatoires** (minimum publiable).
- **Champs recommandés** (qualité cible).
- **Données manquantes** (liste d’écarts à traiter).
- **Règle globale** : pas de section vide côté front.

Livrable attendu : tableau d’audit exploitable par contenu/merch.

## 3) Standards médias

Définir et diffuser un standard minimum :

- **Packshot** ;
- **Détail / texture** ;
- **Usage / dégustation** ;
- **Origine / ambiance** (si disponible).

Contraintes de qualité :

- qualité visuelle minimale ;
- ratio homogène ;
- poids raisonnable ;
- cohérence visuelle catalogue.

Livrable attendu : fiche standard média + checklist d’acceptation.

## 4) Règles simples de recommandations

Formaliser des règles éditoriales/merch compatibles Odoo :

- même famille ;
- complémentarité ;
- même origine ;
- même collection.

Règle stricte :

- pas de logique de scoring complexe non native Odoo.

Livrable attendu : règles de mapping recommandation + exemples de cas.

## 5) Backlog d’enrichissement

Organiser le rattrapage catalogue en 3 classes :

- fiches **pauvres** ;
- fiches **moyennes** ;
- fiches **riches**.

Priorisation :

- progression par vagues (pauvres en premier) ;
- impact business + faisabilité ;
- suivi du taux de complétion.

Livrable attendu : backlog priorisé, loti et pilotable.

---

## Hors périmètre (strict)

- Refonte UI/template produit ;
- changements routes catalogue/shop ;
- modification checkout/panier ;
- algorithme recommandation avancé custom ;
- développement de nouveaux composants lourds.

---

## Critères d’acceptation (GO / NO GO)

- [ ] Charte éditoriale produite et validée MOA ;
- [ ] Matrice de contenu publiée (obligatoire/recommandé/manquant) ;
- [ ] Règle “pas de section vide” opérationnelle en exécution contenu ;
- [ ] Standards médias validés (format/qualité/ratio/poids) ;
- [ ] Règles simples de recommandation définies sans complexité technique ;
- [ ] Backlog d’enrichissement priorisé (pauvre/moyenne/riche) ;
- [ ] Aucune régression MVP2.3 / MVP2.4 Lot 1.

---

## Plan d’exécution recommandé

1. **Cadre éditorial** : charte + exemples.  
2. **Audit catalogue** : matrice par fiche + gaps.  
3. **Cadre média** : standards + checklist.  
4. **Cadre recommandation** : règles simples documentées.  
5. **Backlog** : priorisation et planning d’enrichissement.  
6. **Recette** : contrôle sur 3 fiches représentatives.

---

## Preuve de recette

PV associé : [PV_RECETTE_PRODUCT_PAGE_MERCHANDISING_MVP24_LOT2.md](PV_RECETTE_PRODUCT_PAGE_MERCHANDISING_MVP24_LOT2.md)

---

## Prêt pour exécution — checklist

1. [x] Doctrine de continuité MVP2.3 / Lot 1 actée.
2. [x] Invariants et hors périmètre figés.
3. [x] Axes Lot 2 structurés (charte/matrice/médias/reco/backlog).
4. [ ] Artefacts produits (documents opérationnels).
5. [ ] Recette Lot 2 exécutée.
6. [ ] Décision finale MOA.

---

## Historique

| Date | Changement |
|------|------------|
| 2026-04-28 | Création ticket Lot 2 MVP2.4 orienté méthode durable d’enrichissement contenu/merchandising, sans refonte technique. |
