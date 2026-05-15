# Backlog d’enrichissement fiches — MVP2.4 Lot 2

**Référence ticket** : [TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24_LOT2.md](TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24_LOT2.md)  
**Références de méthode** :  
- [CHARTE_EDITORIALE_FICHE_PRODUIT_MVP24_LOT2.md](CHARTE_EDITORIALE_FICHE_PRODUIT_MVP24_LOT2.md)  
- [MATRICE_CONTENU_FICHE_PRODUIT_MVP24_LOT2.md](MATRICE_CONTENU_FICHE_PRODUIT_MVP24_LOT2.md)  
- [STANDARDS_MEDIAS_FICHE_PRODUIT_MVP24_LOT2.md](STANDARDS_MEDIAS_FICHE_PRODUIT_MVP24_LOT2.md)  
- [REGLES_RECOMMANDATIONS_SIMPLIFIEES_MVP24_LOT2.md](REGLES_RECOMMANDATIONS_SIMPLIFIEES_MVP24_LOT2.md)  
**Date** : 2026-04-28  
**Statut** : version opérationnelle v1

---

## 1) Objectif backlog

Organiser l’enrichissement catalogue de façon progressive et pilotable, sans refonte technique, en traitant d’abord les fiches les plus pauvres.

---

## 2) Segmentation des fiches

## 2.1 Fiches pauvres

Critères :

- obligatoires incomplets ;
- 1 média ou média faible ;
- contenu utile insuffisant.

Objectif :

- atteindre le minimum publiable (obligatoires complets + pas de section vide).

## 2.2 Fiches moyennes

Critères :

- obligatoires complets ;
- recommandés partiels ;
- cohérence éditoriale variable.

Objectif :

- stabiliser la qualité et monter vers un niveau homogène.

## 2.3 Fiches riches

Critères :

- obligatoires + recommandés majoritairement complets ;
- médias conformes standard ;
- recommandations pertinentes.

Objectif :

- maintenir la qualité, corriger les écarts mineurs, servir de référence.

---

## 3) Priorisation progressive

Ordre recommandé :

1. **Vague A — pauvres critiques**  
   - forte visibilité / fort potentiel business.

2. **Vague B — moyennes à potentiel**  
   - produits déjà vendants mais incomplets.

3. **Vague C — riches à optimiser**  
   - finitions qualité, cohérence catalogue.

Critères de priorité :

- impact business ;
- volume de trafic/vente ;
- effort d’enrichissement ;
- disponibilité des assets.

---

## 4) Format de backlog (tableau opérationnel)

| ID fiche | Nom produit | Niveau actuel (pauvre/moyenne/riche) | Priorité (P1/P2/P3) | Contenu manquant | Média manquant | Reco manquante | Lot cible | Responsable | Échéance | Statut |
|---------|-------------|----------------------------------------|---------------------|------------------|----------------|----------------|----------|-------------|---------|--------|
| 2 | Manio Crackers sucrée | pauvre | P1 | promesse à valoriser, description complète, ingrédients/composition, conservation, conseils, spécifications | détail/texture, usage/dégustation, origine/ambiance si asset fiable | recommandations fiables même famille/complément/origine/collection | Vague A | Contenu + Merch | S+1 | À lancer |
| 7 | Kit colombo | pauvre | P1 | promesse courte, description utile, sections basses complètes | packshot à valider + médias complémentaires | alternatives/optionnels non renseignés | Vague A | Contenu + Merch | S+1 | À lancer |
| 33 | Crêpes | pauvre | P2 | promesse, description utile, sections basses | packshot + détail + usage | alternatives/optionnels non renseignés | Vague A | Contenu + Merch | S+2 | À qualifier |
| 34 | Bière | pauvre | P2 | promesse, description utile, sections basses | packshot + détail + usage | alternatives/optionnels non renseignés | Vague A | Contenu + Merch | S+2 | À qualifier |
| 35 | Sucre de canne | pauvre | P2 | promesse, description utile, sections basses | packshot + détail + usage | alternatives/optionnels non renseignés | Vague A | Contenu + Merch | S+2 | À qualifier |
| 36 | Chips | pauvre | P2 | promesse, description utile, sections basses | packshot + détail + usage | alternatives/optionnels non renseignés | Vague A | Contenu + Merch | S+2 | À qualifier |

---

## 5) Définition de “Done” par fiche

Une fiche est considérée enrichie quand :

- tous les champs obligatoires sont OK ;
- pas de section vide visible ;
- niveau média cible atteint pour sa catégorie ;
- recommandations cohérentes (ou fallback propre) ;
- validation MOA effectuée.

---

## 5.b Focus Vague A — Manio Crackers sucrée

Actions contenu :

- remplacer la promesse descriptive par une phrase courte plus désirable, sans surpromesse ;
- rédiger une description complète de 3 à 6 lignes ;
- renseigner ingrédients/composition depuis l’étiquette ou la source BO ;
- renseigner conservation et conseils de dégustation si la donnée est vérifiée ;
- structurer poids, origine, famille et collection dans les attributs si disponibles.

Actions médias :

- conserver le packshot existant si qualité suffisante ;
- ajouter un gros plan texture crackers ;
- ajouter une photo d’usage : crackers avec confiture, café, chocolat chaud ou jus local ;
- ajouter un visuel d’ambiance/origine seulement si l’asset est fiable et utile.

Actions merchandising :

- relier 1 à 4 produits recommandés publiés et cohérents ;
- masquer `Vous aimerez aussi` si aucun lien fiable n’est disponible ;
- compléter `Achat en confiance` uniquement avec les garanties réellement tenues.

---

## 6) Cadence et pilotage

Cadence recommandée :

- revue backlog hebdomadaire ;
- lotissement par vagues courtes ;
- suivi simple des indicateurs.

KPIs minimaux :

- % fiches pauvres restantes ;
- % fiches avec minimum publiable atteint ;
- % fiches avec standard média atteint ;
- % fiches avec recommandations fiables.

---

## 7) Gestion des NA

Quand une donnée manque :

- marquer `NA — donnée absente` ;
- créer une action backlog dédiée ;
- ne pas classer en KO dev.

---

## 8) Historique

| Date | Changement |
|------|------------|
| 2026-04-28 | Création du backlog d’enrichissement Lot 2 MVP2.4 (segmentation pauvre/moyenne/riche, priorisation progressive). |
| 2026-04-28 | Pré-remplissage du backlog à partir de l’audit `tenant_o7` (6 fiches publiées classées en pauvres, priorisées Vague A). |
| 2026-04-28 | Ajout du plan d’action détaillé pour la fiche pilote Manio Crackers sucrée. |
