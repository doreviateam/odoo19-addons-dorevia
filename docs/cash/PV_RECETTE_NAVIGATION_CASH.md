# PV de recette - Navigation Cash / Projection

## Synthese

| Element | Valeur |
| --- | --- |
| Recette | Navigation Cash apres reorganisation des menus |
| Date d'execution | 2026-05-13 |
| Base Odoo | `tenant_o8` |
| Branche / commit | `feature/shop-mvp22-visible-wave1` — navigation menus ; **GO** recette initiale 2026-05-13 ; **Note** : captures du 2026-05-13 = ancienne hiérarchie (**Projection > Trésorerie > Projections de trésorerie > Accueil graphique**) ; libellés et chemins **Comptabilité > Projection de trésorerie** (**Cash Flow** + **Cash Guards**) documentés à partir des versions indiquées ci-dessous |
| Modules controles | `dorevia_cash_flow`, `dorevia_cash_guard`, `base_account_budget` |
| Versions attendues | Cash Flow `19.0.2.3.17`, Cash Guard `19.0.5.6.2` |
| Verdict | **GO** |

## Pre-requis verifies

| Controle | Resultat |
| --- | --- |
| Mise a jour `dorevia_cash_guard,dorevia_cash_flow` | OK - commande `-u dorevia_cash_guard,dorevia_cash_flow` executee sans erreur bloquante |
| Backend Odoo recharge | OK - conteneur Odoo redemarre |
| Version `dorevia_cash_flow` installee | OK - `19.0.2.3.17` (attendu) |
| Version `dorevia_cash_guard` installee | OK - `19.0.5.6.2` (attendu) |
| Droits utilisateur Cash Guard | OK - utilisateur `admin` membre du groupe `Utilisateur Cash Guard` |
| Projection de reference disponible | OK - `Projection 1`, id `1409`, active, periodique semaine, date de situation `2026-05-13`, 13 mailles hebdomadaires |

## Controles de navigation

| Point de controle | Resultat |
| --- | --- |
| Menu principal `Comptabilite > Projection de tresorerie` | OK - racine **Projection de tresorerie** visible sous **Comptabilite** |
| Ordre des entrees sous `Projection de tresorerie` | OK - **Cash Flow** (sequence 10) puis **Cash Guards** / liste (20), puis **Budgets** (25) |
| `Cash Flow` | OK - ouverture directe de la trajectoire de reference, sans selection manuelle obligatoire |
| Bandeau de lecture | OK - encadre **Cash Flow**, mention trajectoire de reference, message de lecture non modifiable et boutons atelier |
| Donnees affichees | OK - projection `Projection 1`, date de situation `2026-05-13`, seuil d'alerte `1 800,00 EUR`, point bas affiche |
| Lecture graphique | OK - legende presente : constate en trait plein, projete en pointille, ligne date de situation, ligne seuil d'alerte |
| Atelier Cash Guard | OK - **Cash Guards** (liste) ouvre l'atelier avec `Projection 1` |
| Entrees Analyse secondaires | OK - `Analyse > Gestion > Trajectoire (Analyse)` et `Analyse > Gestion > Trajectoire - choix projection (Analyse)` visibles |
| `Trajectoire (Analyse)` | OK - ouvre la meme trajectoire avec controles d'audit `Changer de projection` et `Liste des points` |
| `Trajectoire - choix projection (Analyse)` | OK - ouvre l'assistant secondaire de choix de projection |

## Interpretation utilisateur

La navigation est comprehensible selon le cadrage demande :

> Je lis la situation dans **Cash Flow** (sous **Projection de tresorerie**).  
> Je travaille les hypotheses dans **Cash Guards** (liste, meme rubrique).  
> Je gere les budgets sous **Comptabilite > Projection de tresorerie > Budgets**.  
> J'utilise Analyse pour audit / diagnostic.

## Details observes

Captures conservees :

- `docs/cash/captures/recette_navigation_cash_accueil_graphique_20260513.png`
- `docs/cash/captures/recette_navigation_cash_atelier_projection_20260513.png`

### Cash Flow

Parcours controle : **Comptabilite > Projection de tresorerie > Cash Flow**.

Resultat observe :

- titre principal encadre : `Projection de trésorerie` ;
- ligne de contexte : `Trajectoire de référence · Situation : … · Seuil : … · Point bas : …` (formulation métier, sans jargon technique) ;
- projection resolue automatiquement : `Projection 1` ;
- controles atelier : `Actualiser`, `Ouvrir l'atelier`, `Toutes les projections` ;
- raccourcis audit : `Vue analyse`, `Audit / autre projection` ;
- pas de passage obligatoire par l'assistant de selection.

### Atelier Cash Guard

Parcours controle : **Comptabilite > Projection de tresorerie > Cash Guards**.

Resultat observe :

- ouverture de la vue liste **Cash Guards** (action liste Cash Guard) ;
- document `Projection 1` visible ;
- donnees principales visibles : periodicite `Semaine`, date de situation `13 mai`, seuil `1 800,00`, solde constate `1 740,67`, projection finale `1 840,67`, point bas `1 640,67`, statut `Tension`.

### Analyse

Parcours controle : **Comptabilite > Analyse > Gestion**.

Resultat observe :

- `Trajectoire (Analyse)` reste disponible comme raccourci secondaire ;
- `Trajectoire - choix projection (Analyse)` reste disponible comme parcours d'audit avec selection manuelle ;
- le libelle `(Analyse)` rend le statut secondaire explicite.

## Verdict

**GO**.

La nouvelle organisation est coherente cote utilisateur : le parcours nominal de lecture est **Comptabilite > Projection de tresorerie > Cash Flow** (trajectoire de reference systeme ; heuristique transitoire tant que `is_system_reference` n'est pas livre), l'atelier est **Cash Guards** sous la meme rubrique, **Budgets** est **Comptabilite > Projection de tresorerie > Budgets**, et les entrees **Analyse** restent des raccourcis d'audit / diagnostic.

## Traçabilité dépôt

Les captures listées dans **Captures conservées** sont conservées sous **`docs/cash/captures/`** et versionnées avec ce PV comme **preuves de recette** (ne pas supprimer ni renommer sans mettre à jour ce document).
