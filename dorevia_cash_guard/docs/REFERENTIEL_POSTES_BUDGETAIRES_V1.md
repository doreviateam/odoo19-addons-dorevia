# REFERENTIEL_POSTES_BUDGETAIRES_V1 — `dorevia_cash_guard`

Referentiel documentaire des 20 postes budgetaires standards V1.

Important :

- ce document fournit la nomenclature cible ;
- les comptes comptables restent des suggestions ;
- le mapping definitif doit etre valide manuellement dans chaque instance ;
- aucun seed XML automatique ne doit etre active sans mapping fiable prealablement valide.

---

## Format de reference

Colonnes :

- `code` : identifiant stable du poste ;
- `nom` : libelle metier ;
- `famille` : `entree` ou `sortie` ;
- `sens_cash_defaut` : `inflow` ou `outflow` ;
- `ordre` : ordre d'affichage recommande ;
- `description_metier` : usage metier attendu ;
- `comptes_comptables_suggeres` : exemples de comptes a confirmer localement.

---

## Nomenclature V1 (20 postes)

| code | nom | famille | sens_cash_defaut | ordre | description_metier | comptes_comptables_suggeres |
| --- | --- | --- | --- | ---: | --- | --- |
| CGB001 | Subventions publiques | entree | inflow | 10 | Subventions de collectivites et organismes publics | 74, 441, 467 |
| CGB002 | Subventions privees / mecenat | entree | inflow | 20 | Aides fondations et entreprises mecenes | 74, 758, 467 |
| CGB003 | Cotisations / adhesions | entree | inflow | 30 | Encaissements des cotisations membres | 756, 706, 411 |
| CGB004 | Dons / participations libres | entree | inflow | 40 | Dons ponctuels et contributions libres | 754, 758, 467 |
| CGB005 | Recettes d'activite | entree | inflow | 50 | Ventes, prestations, ateliers | 706, 707, 411 |
| CGB006 | Billetterie / evenements | entree | inflow | 60 | Recettes evenementielles et inscriptions | 706, 708, 411 |
| CGB007 | Remboursements recus | entree | inflow | 70 | Avoirs et remboursements entrants | 409, 467, 758 |
| CGB008 | Autres entrees | entree | inflow | 80 | Produits divers non classes | 758, 771, 467 |
| CGB009 | Salaires nets | sortie | outflow | 90 | Paiement des salaires nets | 421, 425, 512 |
| CGB010 | Charges sociales | sortie | outflow | 100 | Cotisations sociales et organismes | 431, 437, 438 |
| CGB011 | Prestations externes | sortie | outflow | 110 | Intervenants, consultants, sous-traitance | 611, 622, 401 |
| CGB012 | Fournisseurs / achats | sortie | outflow | 120 | Achats de biens et services | 601, 606, 607, 401 |
| CGB013 | Loyers / locaux | sortie | outflow | 130 | Loyers, charges locatives, salles | 613, 614, 401 |
| CGB014 | Energie / eau / telecom | sortie | outflow | 140 | Charges utilitaires courantes | 6061, 60611, 626, 401 |
| CGB015 | Assurances | sortie | outflow | 150 | Assurances RC, locaux, materiel | 616, 401 |
| CGB016 | Communication / marketing | sortie | outflow | 160 | Publicite, graphisme, impressions | 623, 626, 401 |
| CGB017 | Deplacements / transport | sortie | outflow | 170 | Frais de mission et transport | 625, 624, 401 |
| CGB018 | Impots / taxes / TVA | sortie | outflow | 180 | Fiscalite et taxes diverses | 445, 447, 635 |
| CGB019 | Remboursements / dettes / emprunts | sortie | outflow | 190 | Remboursements de dettes et prets | 164, 168, 512 |
| CGB020 | Autres sorties | sortie | outflow | 200 | Charges diverses non classees | 658, 671, 401 |

---

## Regles d'utilisation

- un poste utilise ne doit pas etre supprime ; il doit etre archive ;
- les comptes suggeres sont indicatifs et doivent etre adaptes au plan comptable local ;
- le mapping postes <-> comptes est de la responsabilite de l'instance ;
- le seed XML n'est active qu'apres validation manuelle explicite du mapping.
