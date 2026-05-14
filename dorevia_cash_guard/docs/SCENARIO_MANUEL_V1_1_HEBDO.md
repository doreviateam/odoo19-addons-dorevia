# Scénario manuel — Cash Guard V1.1 (suivi hebdomadaire)

## Contexte de recette

```text
URL : http://localhost:18079
Base : tenant_o8
Module : dorevia_cash_guard
```

*(Nom de base : **`tenant_o8`** avec la lettre **o**, pas `tenant_08` avec un zéro.)*

## Mise à jour du module et tests (Docker)

Exécuter les commandes depuis le répertoire qui contient **`docker-compose.yml`** (stack Odoo locale ; exemple typique : dossier **`sandbox-odoo19`** au même niveau que le dépôt addons, ou chemin équivalent sur ta machine). Sinon Docker répond *« no configuration file provided »*.

```bash
cd ~/sandbox-odoo19
docker compose exec odoo odoo -d tenant_o8 -u dorevia_cash_guard --stop-after-init
docker compose restart odoo
```

Tests :

```bash
cd ~/sandbox-odoo19
docker compose exec odoo odoo -d tenant_o8 -u dorevia_cash_guard --test-enable --stop-after-init --http-port=8071
```

## Prérequis

- Module `dorevia_cash_guard` en **19.0.3.0.0** ou supérieur, base à jour (`-u dorevia_cash_guard`).
- Utilisateur avec groupe **Utilisateur Cash Guard** ; actions manager si besoin (clôture, rouverture).

## Parcours minimal

1. Créer un **document de projection** : journal banque/caisse, **dates de début et de fin** de la période suivie, **périodicité** (semaine / mois / trimestre ; défaut : semaine), seuil d’alerte.
2. Enregistrer ; cliquer **Actualiser** : la synthèse affiche la **situation constatée** et la **projection** ; l’onglet **Suivi de trésorerie** liste les segments selon la périodicité (historique / situation / projeté).
3. Ajouter des **flux complémentaires** avec dates strictement **après** la date de situation pour alimenter les **périodes projetées** correspondantes ; actualiser à nouveau.
4. **Valider** puis, en manager, **Clôturer** : le cron « Recalcul des points ouverts » ne doit pas modifier les points **Clôturés** (uniquement brouillon / validé).

## Points de contrôle

- **Date de situation** calculée à chaque actualisation ; **périodicité** modifiable en brouillon et, après validation, selon les mêmes règles que les autres champs structurants (manager si besoin).
- Les lignes `dorevia.cash.guard.week` sont **lecture seule** pour les utilisateurs ; recalculées sans doublons à chaque actualisation (`guard_id` + `week_index`).
