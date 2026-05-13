# PV de recette - Navigation Cash / Projection

## Synthese

| Element | Valeur |
| --- | --- |
| Recette | Navigation Cash apres reorganisation des menus |
| Date d'execution | 2026-05-13 |
| Base Odoo | `tenant_o8` |
| Branche / commit | `feature/shop-mvp22-visible-wave1` — navigation menus **21368ad** ; **GO** recette ; preuves versionnées dans le même dépôt (voir captures ci-dessous) |
| Modules controles | `dorevia_cash_flow`, `dorevia_cash_guard`, `base_account_budget` |
| Versions attendues | Cash Flow `19.0.2.2.0`, Cash Guard `19.0.5.3.9` |
| Verdict | **GO** |

## Pre-requis verifies

| Controle | Resultat |
| --- | --- |
| Mise a jour `dorevia_cash_guard,dorevia_cash_flow` | OK - commande `-u dorevia_cash_guard,dorevia_cash_flow` executee sans erreur bloquante |
| Backend Odoo recharge | OK - conteneur Odoo redemarre |
| Version `dorevia_cash_flow` installee | OK - `19.0.2.2.0` |
| Version `dorevia_cash_guard` installee | OK - `19.0.5.3.9` |
| Droits utilisateur Cash Guard | OK - utilisateur `admin` membre du groupe `Utilisateur Cash Guard` |
| Projection de reference disponible | OK - `Projection 1`, id `1409`, active, periodique semaine, date de situation `2026-05-13`, 13 mailles hebdomadaires |

## Controles de navigation

| Point de controle | Resultat |
| --- | --- |
| Menu principal `Comptabilite > Projection > Tresorerie` | OK - dossier `Projection`, sous-dossier `Tresorerie` visibles cote utilisateur |
| Ordre des entrees sous `Tresorerie` | OK - `Accueil graphique` en sequence 10, `Projections de tresorerie` en sequence 20 |
| `Accueil graphique` | OK - ouverture directe de la trajectoire de reference, sans selection manuelle obligatoire |
| Bandeau de lecture | OK - titre `Accueil graphique`, mention trajectoire de reference, message de lecture non modifiable et boutons atelier |
| Donnees affichees | OK - projection `Projection 1`, date de situation `2026-05-13`, seuil d'alerte `1 800,00 EUR`, point bas affiche |
| Lecture graphique | OK - legende presente : constate en trait plein, projete en pointille, ligne date de situation, ligne seuil d'alerte |
| Atelier Cash Guard | OK - `Projections de tresorerie` ouvre la liste atelier Cash Guard avec `Projection 1` |
| Entrees Analyse secondaires | OK - `Analyse > Gestion > Trajectoire (Analyse)` et `Analyse > Gestion > Trajectoire - choix projection (Analyse)` visibles |
| `Trajectoire (Analyse)` | OK - ouvre la meme trajectoire avec controles d'audit `Changer de projection` et `Liste des points` |
| `Trajectoire - choix projection (Analyse)` | OK - ouvre l'assistant secondaire de choix de projection |

## Interpretation utilisateur

La navigation est comprehensible selon le cadrage demande :

> Je lis la situation dans **Accueil graphique**.  
> Je travaille les hypotheses dans **Projections de tresorerie**.  
> J'utilise Analyse pour audit / diagnostic.

## Details observes

Captures conservees :

- `docs/cash/captures/recette_navigation_cash_accueil_graphique_20260513.png`
- `docs/cash/captures/recette_navigation_cash_atelier_projection_20260513.png`

### Accueil graphique

Parcours controle : **Comptabilite > Projection > Tresorerie > Accueil graphique**.

Resultat observe :

- titre : `Accueil graphique` ;
- sous-titre : trajectoire de `reference` ;
- projection resolue automatiquement : `Projection 1` ;
- date de situation : `2026-05-13` ;
- seuil d'alerte : `1 800,00 EUR` ;
- point bas affiche : `0,00 EUR (2026-01-07)` ;
- controles atelier : `Ouvrir la projection`, `Actualiser la projection`, `Toutes les projections` ;
- raccourcis audit : `Audit - autre projection`, `Vue Analyse (plein ecran)` ;
- pas de passage obligatoire par l'assistant de selection.

### Atelier Cash Guard

Parcours controle : **Comptabilite > Projection > Tresorerie > Projections de tresorerie**.

Resultat observe :

- ouverture de la vue liste `Projections de tresorerie` ;
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

La nouvelle organisation est coherente cote utilisateur : le parcours nominal de lecture est bien **Projection > Tresorerie > Accueil graphique**, l'atelier de travail reste **Projections de tresorerie**, et les entrees **Analyse** sont correctement positionnees comme outils d'audit / diagnostic.

## Traçabilité dépôt

Les captures listées dans **Captures conservées** sont conservées sous **`docs/cash/captures/`** et versionnées avec ce PV comme **preuves de recette** (ne pas supprimer ni renommer sans mettre à jour ce document).
