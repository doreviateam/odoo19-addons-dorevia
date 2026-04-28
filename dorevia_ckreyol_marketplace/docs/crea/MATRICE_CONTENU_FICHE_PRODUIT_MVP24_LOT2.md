# Matrice de contenu — Fiche produit (MVP2.4 Lot 2)

**Référence ticket** : [TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24_LOT2.md](TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24_LOT2.md)  
**Charte associée** : [CHARTE_EDITORIALE_FICHE_PRODUIT_MVP24_LOT2.md](CHARTE_EDITORIALE_FICHE_PRODUIT_MVP24_LOT2.md)  
**Date** : 2026-04-28  
**Statut** : version opérationnelle v1

---

## 1) Objectif

Cette matrice permet de piloter l’enrichissement des fiches produit de façon progressive, sans refonte technique :

- identifier ce qui est **obligatoire** pour publier ;
- distinguer ce qui est **recommandé** pour monter en qualité ;
- tracer ce qui est **manquant** ;
- appliquer la règle stricte : **pas de section vide affichée**.

---

## 2) Règles de classification des fiches

- **Fiche pauvre** : minimum publiable atteint, plusieurs champs recommandés absents.
- **Fiche moyenne** : obligatoires complets, partie des recommandés renseignée.
- **Fiche riche** : obligatoires + recommandés majoritairement complets, médias alignés standard.

---

## 3) Matrice champs par fiche

| Bloc | Champ / donnée | Niveau | Source Odoo | Statut fiche (OK/NA/MANQUANT) | Action si manquant |
|------|----------------|--------|-------------|-------------------------------|--------------------|
| Identité | Nom produit clair | Obligatoire | `name` / `ck_product_name` |  | Corriger intitulé BO |
| Promesse | Promesse courte crédible | Obligatoire | `description_sale` (1re ligne utile) |  | Rédiger phrase courte |
| Vente | Prix affiché | Obligatoire | Pricelist Odoo |  | Vérifier config prix |
| Achat | Quantité + ajout panier | Obligatoire | Natif Odoo |  | Vérifier variante/stock |
| Origine | Origine informative (si renseignée) | Recommandé | attribut Origine / profil origin |  | Renseigner origine fiable |
| Description | Description utile (3-6 lignes) | Obligatoire | `description_sale` / contenu éditorial |  | Enrichir contenu utile |
| Bénéfices / usages | Usages concrets (2-4 points) | Recommandé | contenu éditorial |  | Ajouter usages réalistes |
| Ingrédients | Liste ingrédients | Recommandé | contenu fiche |  | Compléter section |
| Conservation | Consignes de conservation | Recommandé | contenu fiche |  | Compléter section |
| Conseils | Conseils de dégustation | Recommandé | contenu fiche |  | Compléter section |
| Spécifications | Données techniques fiables | Recommandé | attributs / champs produits |  | Structurer attributs |
| Média 1 | Packshot principal | Obligatoire | image produit |  | Ajouter visuel packshot |
| Média 2 | Détail / texture | Recommandé | galerie images |  | Ajouter visuel texture |
| Média 3 | Usage / dégustation | Recommandé | galerie images |  | Ajouter visuel usage |
| Média 4 | Origine / ambiance (si dispo) | Optionnel | galerie images |  | Ajouter si asset existe |
| Reco | Produits recommandés fiables | Recommandé | liens produits Odoo |  | Créer liens simples |

---

## 4) Règle “pas de section vide”

Application obligatoire :

- une section n’apparaît que si sa donnée existe ;
- aucune section décorative vide ;
- aucun texte artificiel généré pour remplir.

Conséquence recette :

- absence de donnée = `NA — donnée absente` ;
- ce n’est pas un KO dev tant que le fallback d’affichage est propre.

---

## 5) Grille d’audit rapide par fiche

| ID fiche | Niveau cible (pauvre/moyenne/riche) | % obligatoires OK | % recommandés OK | Sections vides visibles (oui/non) | Médias (1/2/3+) | Reco fiables (oui/non) | Décision |
|---------|--------------------------------------|-------------------|------------------|-----------------------------------|-----------------|------------------------|----------|
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |

---

## 6) Seuils de décision opérationnels

- **Publier (minimum)** : 100% obligatoires OK, 0 section vide.
- **Passer “moyenne”** : minimum + au moins 50% recommandés OK.
- **Passer “riche”** : minimum + au moins 80% recommandés OK + standard médias respecté.

---

## 7) Historique

| Date | Changement |
|------|------------|
| 2026-04-28 | Création de la matrice de contenu Lot 2 MVP2.4 (obligatoire/recommandé/manquant, pas de section vide). |
