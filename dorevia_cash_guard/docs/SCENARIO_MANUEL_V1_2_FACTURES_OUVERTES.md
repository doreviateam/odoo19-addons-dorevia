# Scénario manuel — Cash Guard V1.2 (projection / factures ouvertes)

**Ticket** : `CG-V1.2-01-PROJECTED-BALANCE-FROM-OPEN-INVOICES`  
**Objectif** : valider la colonne **Projection** dans le suivi de trésorerie et son calcul depuis les factures **postées** avec résiduel, sans budget ni simulations.

---

## Prérequis

- Module `dorevia_cash_guard` installé ; droits utilisateur Cash Guard.
- Société avec journaux **Banque** et **Caisse**, et catégories comptables permettant de créer factures fournisseur et client.
- Environnement de recette : `http://localhost:18079`, base `tenant_o8`.

---

## Étapes

1. **Créer ou ouvrir un point de trésorerie** avec :
   - une **date de situation** comprise dans l’exercice affiché ;
   - **journaux de trésorerie** Banque + Caisse ;
   - une **périodicité** semaine (pour repérer facilement la ligne du mois concerné) ;
   - un **seuil d’alerte** et un solde constaté cohérent après **Actualiser**.

2. Noter le **Solde** (constaté) sur la ligne « Situation » et la **Projection** sur cette même ligne (sans facture ouverte : ils doivent être identiques au solde constaté sur cette maille).

3. **Créer une facture client validée**, non payée, avec une **date d’échéance dans une semaine future** (après la date de situation).

4. Cliquer **Actualiser** sur le point de trésorerie.

5. Vérifier dans **Suivi de trésorerie** :
   - une ligne dont la colonne **État** est **Prévisionnel**, correspondant à la semaine de l’échéance, affiche une **Projection** supérieure au **Solde** de cette ligne d’un montant égal au **résiduel** de la facture (en devise société) ;
   - le **Statut** des lignes utilise bien la **Projection** (pas uniquement le solde constaté si la facture suffit à changer le niveau de risque).

6. **Créer une facture fournisseur validée**, non payée, échéance sur une autre semaine.

7. **Actualiser** ; constater une **baisse** de la **Projection** sur la période contenant cette échéance (impact opposé au client).

8. **Enregistrer un paiement complet** sur l’une des factures.

9. **Actualiser** ; vérifier que la charge projetée liée à cette facture **disparaît** (puisque `amount_residual` devient nul).

10. Créer une **facture brouillon** (non validée) avec un montant élevé et une échéance proche.

11. **Actualiser** ; vérifier **aucun impact** sur la **Projection** (les brouillons sont exclus).

12. Créer une **facture client validée**, non payée, avec une **date d’échéance antérieure à la date de situation**.

13. **Actualiser** ; vérifier qu’elle impacte la **Projection** dès la ligne dont l’**État** est **Situation** ou la période contenant la date de situation.

14. Créer une **facture brouillon / à valider** avec une date d’échéance **antérieure** à la date de situation.

15. **Actualiser** ; vérifier qu’elle **n’impacte pas** la **Projection**.

---

## Résultat attendu

- La **Projection** reflète **uniquement** les pièces **postées** avec résiduel non nul, agrégées depuis `account.move`.
- Aucune ligne automatique n’apparaît dans l’onglet **Flux prévisionnels** pour représenter les factures (calcul agrégé uniquement).
- Une facture **validée échue non payée** est traitée comme **exigible à la date de situation**.
- Une facture **brouillon / à valider**, même échue, est **ignorée**.
