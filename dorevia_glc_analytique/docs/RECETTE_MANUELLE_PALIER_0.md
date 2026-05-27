# Recette manuelle — dorevia_glc_analytique · Palier 0

**Module :** `dorevia_glc_analytique`  
**Version cible :** `19.0.1.0.0` (Palier 0)  
**Rôle testeur :** gestionnaire GLC, comptable ou MOA  
**Références :** [README module](../README.md), [PALIERS.md](./PALIERS.md), [REGLES_AFFECTATION.md](./REGLES_AFFECTATION.md), [spec V1.1](./README.md)

Ce document est le **guide d'exécution Palier 0** : installation du socle analytique, nomenclature, droits, applicabilités non bloquantes.

**Hors périmètre de cette recette :** contrôles d'anomalies (Palier 1), ventilation salariale, registre bénévole, rapport CA, clôture analytique.

**Statut document :** gelé pour exécution recette MOA sur `glc-rgl-test-import` (Palier 0).

---

## Contexte de recette

```text
URL  : http://localhost:18079
Base : glc-rgl-test-import
Module : dorevia_glc_analytique
Version : 19.0.1.0.0
```

Adapter l'URL si l'instance de recette diffère.

---

## Menus concernés

| Menu | Rôle |
|---|---|
| **Comptabilité → Pilotage GLC → Activités GLC** | Liste des 7 comptes du plan Activités |
| **Comptabilité → Pilotage GLC → Financements GLC** | Liste des 4 comptes du plan Financements |
| **Comptabilité → Configuration → Plans analytiques** | Vérification des plans et applicabilités Odoo 19 |
| **Comptabilité → Fournisseurs / Clients → Factures** | Test distribution analytique sur pièces |
| **Paramètres → Utilisateurs** | Attribution des groupes GLC |

---

## Mise à jour du module (Docker)

Depuis le répertoire contenant `docker-compose.yml` (ex. `~/sandbox-odoo19`) :

> **Note :** le nom du **service Docker** (`odoo` ci-dessous) dépend de votre `docker-compose.yml`.  
> Vérifier avec `docker compose config --services` ou la clé `services:` du fichier.  
> Remplacer `odoo` par le nom réel (ex. `web`, `odoo19`) dans toutes les commandes.  
> Si le conteneur tourne déjà : `docker compose exec <service> …` ; sinon : `docker compose run --rm <service> …`.

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytique --stop-after-init --no-http

docker compose restart odoo
```

Tests automatisés (optionnel) :

```bash
docker compose run --rm odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytique \
  --test-enable --test-tags=/dorevia_glc_analytique --stop-after-init --no-http
```

---

## Avant de commencer

| # | Contrôle | ☐ |
|---|---|---|
| A1 | Module `dorevia_glc_analytique` installé, état **Installé** (Apps) | ☐ |
| A2 | Dépendances `account` et `analytic` actives | ☐ |
| A3 | Utilisateur de test avec groupe **Gestionnaire GLC** (ou **Utilisateur GLC**) | ☐ |
| A4 | Groupe **Comptabilité analytique** actif (implicite via Utilisateur GLC) | ☐ |
| A5 | Société GLC sélectionnée dans l'environnement Odoo | ☐ |

**Utilisateur recommandé pour la recette complète :** compte avec **Gestionnaire GLC** (ex. Administrator en recette).

---

## Palier 0 — parcours nominal

Exécuter **dans l'ordre**. Pour chaque pas : **Action** → **Contrôles** → cocher **OK** ou noter l'écart.

### 1. Installation et module

| Pas | Action | Contrôles | OK | Observations |
|---|---|---|---|---|
| P0.1 | Apps → rechercher « GLC Analytique » ou `dorevia_glc_analytique` | Module **Dorevia GLC Analytique** visible, état **Installé**, version **19.0.1.0.0** | ☐ | |
| P0.2 | Vérifier qu'aucune erreur bloquante n'apparaît au chargement Comptabilité | Pas d'erreur client / traceback au menu Comptabilité | ☐ | |

### 2. Menus Pilotage GLC

| Pas | Action | Contrôles | OK | Observations |
|---|---|---|---|---|
| P0.3 | Ouvrir **Comptabilité → Pilotage GLC** | Sous-menus **Activités GLC** et **Financements GLC** visibles | ☐ | |
| P0.4 | Ouvrir **Activités GLC** | **7** comptes listés | ☐ | |
| P0.5 | Ouvrir **Financements GLC** | **4** comptes listés | ☐ | |

### 3. Nomenclature — codes et plans

| Pas | Action | Contrôles | OK | Observations |
|---|---|---|---|---|
| P0.6 | Dans **Activités GLC**, vérifier les codes | Présents : `STRUCTURE`, `BAR`, `PRESTATIONS`, `RESIDENCES`, `MISSIONS`, `PRIVATISATIONS`, `LOCATION_RADIO` | ☐ | |
| P0.7 | Dans **Financements GLC**, vérifier les codes | Présents : `ADHESIONS`, `DONS`, `SUBVENTIONS`, `RESSOURCES_PROPRES` | ☐ | |
| P0.8 | **Configuration → Plans analytiques** | Plans **GLC - Activités** et **GLC - Financements** existent | ☐ | |
| P0.9 | Ouvrir le plan **GLC - Activités** | 7 comptes rattachés ; description cohérente | ☐ | |
| P0.10 | Ouvrir le plan **GLC - Financements** | 4 comptes rattachés ; description cohérente | ☐ | |

### 4. Extension fiche compte analytique

**Palier 0 — 4 champs livrés** sur `account.analytic.account` (onglet **Pilotage GLC**) :

| Libellé interface | Champ technique |
|---|---|
| Type GLC | `glc_activity_type` |
| Ordre rapport GLC | `glc_display_sequence` |
| Actif rapport GLC | `glc_report_active` |
| Commentaire de pilotage | `glc_pilotage_comment` |

Pas de modèle « Activité » parallèle — source de vérité = compte analytique Odoo standard.

| Pas | Action | Contrôles | OK | Observations |
|---|---|---|---|---|
| P0.11 | Ouvrir le compte **BAR** (Activités GLC) | Onglet **Pilotage GLC** visible | ☐ | |
| P0.12 | Vérifier les **3 premiers champs** Palier 0 | **Type GLC** = Mixte ; **Ordre rapport GLC** renseigné ; **Actif rapport GLC** coché | ☐ | |
| P0.13 | Saisir un **Commentaire de pilotage** (`glc_pilotage_comment`) test, enregistrer | 4ᵉ champ Palier 0 ; commentaire persisté après rechargement fiche | ☐ | |
| P0.14 | Ouvrir **ADHESIONS** (Financements GLC) | **Type GLC** = Financement | ☐ | |

### 5. Applicabilités Odoo 19 (non bloquantes)

> Doctrine Palier 0 : les plans sont **visibles** mais **non obligatoires** à la validation. Aucun blocage si la distribution est vide.

| Pas | Action | Contrôles | OK | Observations |
|---|---|---|---|---|
| P0.15 | Plan **GLC - Activités** → onglet applicabilité | Facture client : **Optional** ; Facture fournisseur : **Optional** | ☐ | |
| P0.16 | Plan **GLC - Financements** → onglet applicabilité | Facture client : **Optional** ; Facture fournisseur : **Unavailable** (masqué) | ☐ | |
| P0.17 | Créer une **facture fournisseur** brouillon, ligne de charge | Champ distribution analytique : plan **GLC - Activités** proposé ; **GLC - Financements** absent | ☐ | |
| P0.18 | **Valider** la facture fournisseur **sans** analytique | Validation **acceptée** (pas de blocage Palier 0) | ☐ | |
| P0.19 | Créer une **facture client** brouillon, ligne de produit | Les **deux** plans GLC apparaissent dans la distribution | ☐ | |
| P0.20 | Affecter `BAR` + `RESSOURCES_PROPRES`, valider | Validation acceptée ; analytique enregistrée sur la ligne | ☐ | |
| P0.21 | Créer une **facture client**, valider **sans** analytique | Validation **acceptée** (non bloquant en Palier 0) | ☐ | |

### 6. Droits et sécurité

| Pas | Action | Contrôles | OK | Observations |
|---|---|---|---|---|
| P0.22 | Utilisateur avec **Gestionnaire GLC** uniquement | Menus Pilotage GLC + onglet Pilotage GLC accessibles | ☐ | |
| P0.23 | Utilisateur **sans** groupe GLC (session test séparée) | Menu **Pilotage GLC** absent ou inaccessible | ☐ | |
| P0.24 | Vérifier l'implication des groupes | **Gestionnaire GLC** → inclut **Utilisateur GLC** → inclut **Comptabilité analytique** | ☐ | |

### 7. Non-régression et périmètre

| Pas | Action | Contrôles | OK | Observations |
|---|---|---|---|---|
| P0.25 | Parcourir Apps : aucun sous-module GLC salaire / bénévolat / rapport | Pas de menu Ventilation salariale, Registre bénévole, Rapport CA | ☐ | |
| P0.26 | Vérifier qu'il n'existe pas de modèle « Activité GLC » séparé | Source de vérité = **comptes analytiques Odoo** standard | ☐ | |
| P0.27 | Comptabilité générale existante (journal, facture antérieure) | Pas de régression visible sur les écrans comptables standard | ☐ | |

---

## Cas limites

### L1 — Utilisateur GLC sans droits comptables étendus

**Action :** utilisateur avec **Utilisateur GLC** seulement (pas Comptable).

**Contrôle :** accès lecture Pilotage GLC ; pas d'erreur sur ouverture des listes de comptes.

| OK | Observations |
|---|---|
| ☐ | |

### L2 — Double installation / mise à jour

**Action :** relancer `-u dorevia_glc_analytique` sur la base.

**Contrôle :** pas de doublon de plans ou comptes ; codes GLC toujours uniques (11 comptes).

| OK | Observations |
|---|---|
| ☐ | |

### L3 — Compte analytique désactivé

**Action :** sur un compte test, décocher **Actif rapport GLC** ou archiver le compte.

**Contrôle :** compte toujours utilisable en compta si actif Odoo ; flag GLC indépendant du statut `active` Odoo (documenter le comportement observé).

| OK | Observations |
|---|---|
| ☐ | |

---

## Grille de conformité nomenclature

À compléter lors de la recette (cocher chaque ligne trouvée).

### Plan GLC - Activités

| Code | Nom attendu | Type GLC | ☐ |
|---|---|---|---|
| `STRUCTURE` | Structure & Administration | Charge | ☐ |
| `BAR` | Bar, Restauration & Cuisine | Mixte | ☐ |
| `PRESTATIONS` | Prestations & Animations | Mixte | ☐ |
| `RESIDENCES` | Résidences artistiques | Charge subventionnée | ☐ |
| `MISSIONS` | Déplacements & Missions | Charge | ☐ |
| `PRIVATISATIONS` | Privatisation d'espace | Mixte | ☐ |
| `LOCATION_RADIO` | Location Radio Grand Lieu | Recette | ☐ |

### Plan GLC - Financements

| Code | Nom attendu | Type GLC | ☐ |
|---|---|---|---|
| `ADHESIONS` | Adhésions | Financement | ☐ |
| `DONS` | Dons | Financement | ☐ |
| `SUBVENTIONS` | Subventions | Financement | ☐ |
| `RESSOURCES_PROPRES` | Ressources propres | Financement | ☐ |

---

## Verdict recette Palier 0

| Verdict | Condition |
|---|---|
| **GO MOA Palier 0** | P0.1 à P0.27 OK · nomenclature 11/11 · applicabilités non bloquantes confirmées · hors périmètre Palier 1+ absent |
| **GO avec réserves** | Écarts mineurs documentés (libellés, ordre colonnes) sans impact fonctionnel |
| **NO GO** | Plans ou comptes manquants · validation bloquée sans analytique · menus Palier 1+ présents · doublons nomenclature |

**Verdict :** ☑ **GO MOA Palier 0** · ☐ GO avec réserves · ☐ NO GO

**Testeur :** MOA GLC **Date :** 2026-05-27

**Commentaire MOA :**

```text
Recette exécutée sur glc-rgl-test-import (http://localhost:18079).
Mise à jour module + redémarrage Odoo OK. Tests auto : 7/7.
Recette fonctionnelle backend : P0.1–P0.27 OK. Nomenclature 11/11.
Applicabilités conformes (optional / unavailable). Validations sans
analytique acceptées ; double axe BAR + RESSOURCES_PROPRES persisté.
Droits, menus et hors périmètre Palier 1+ conformes.
```

---

## Clôture recette — `glc-rgl-test-import` (2026-05-27)

| Contrôle | Résultat |
|---|---|
| Mise à jour module Docker | OK |
| Redémarrage Odoo | OK |
| Tests automatisés (`/dorevia_glc_analytique`) | **7 tests, 0 échec, 0 erreur** |
| Recette fonctionnelle P0.1–P0.27 | **Tous OK** |
| Nomenclature 11 comptes | **11/11 conformes** |
| Applicabilités Activités | `optional` client / fournisseur |
| Applicabilités Financements | `optional` client · `unavailable` fournisseur |
| Facture fournisseur sans analytique | Validée (non bloquant) |
| Facture client sans analytique | Validée (non bloquant) |
| Facture client `BAR` + `RESSOURCES_PROPRES` | Validée, distribution persistée |
| Droits / groupes / menus | Conformes |
| Absence modèle `glc.activity` | Confirmé |
| Absence menus Palier 1+ | Confirmé |
| URL Odoo / base | Joignable, pas d'erreur relevée |

### Données de test créées en base (recette)

À conserver ou nettoyer selon politique de la base de recette :

| Objet | Identifiant |
|---|---|
| Partenaire | `Recette GLC Palier 0` |
| Utilisateurs | 2 utilisateurs de recette (droits GLC) |
| Factures | Factures fournisseur / client de test |

Script de recette temporaire : `/private/tmp/glc_p0_recette.py` (hors dépôt).

### Suite immédiate

- Palier 0 **validé MOA** — socle prêt pour usage et Phase 0 migration métier.
- Prochain ticket : **Palier 1** (rapport anomalies, durcissement applicabilités).

## Après validation Palier 0

1. Compléter [MATRICE_MIGRATION.md](./MATRICE_MIGRATION.md) (Phase 0 métier — anciens 9 comptes).
2. Ouvrir le ticket **Palier 1** : rapport anomalies, durcissement progressif des applicabilités.
3. Ne pas attendre Palier 0 pour **discipline de saisie** manuelle (cf. [REGLES_AFFECTATION.md](./REGLES_AFFECTATION.md)) — les contrôles automatisés viendront au Palier 1.
