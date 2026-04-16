# `dorevia_vault_connector` — V3 bornée (Odoo 19)

## Rôle

Module **connecteur source** minimal : à la validation d’un **document comptable posté** (`account.move`) ou d’un **paiement validé** (`account.payment`), construction d’un **payload JSON** stable et envoi en **POST HTTP** vers une URL configurable. L’état d’envoi est stocké sur la pièce ou le paiement ; un **rejeu manuel** est prévu après échec.

Ce module **ne** remplace **pas** Vault ni Lynki : il prépare la chaîne **Odoo local → cible HTTP** (adaptateur, mock, ou futur socle Dorevia).

## Périmètre actuellement implémenté

- Inclus :
  - documents comptables : `out_invoice`, `in_invoice`, `out_refund`, `in_refund`
  - paiements : `account.payment` `inbound` et `outbound` en état `in_process` ou `paid`
  - hook sur `action_post`, rejeu manuel, champs techniques, paramètres, client HTTP (`urllib`), vue pièce + vue paiement.
- Exclus : rapprochement bancaire, stock, retry avancé, queue, multi-flux cash côté lecture produit — voir [SPEC_V1_DOREVIA_VAULT_CONNECTOR_ODOO19.md](../SPEC_V1_DOREVIA_VAULT_CONNECTOR_ODOO19.md) et [SPEC_V2_DOREVIA_VAULT_CONNECTOR_ODOO19_VENTE_ACHAT_AVOIR.md](../../Zedocs/odoo19/modules/dorevia-vault-connector/SPEC_V2_DOREVIA_VAULT_CONNECTOR_ODOO19_VENTE_ACHAT_AVOIR.md).

## Dépendances Odoo

- `base`
- `account`

## Installation

1. Ajouter le répertoire parent `odoo19-addons-dorevia` au **addons_path** de votre instance Odoo 19.
2. Mettre à jour la liste des applications, installer **« Dorevia — connecteur Vault (V1) »**.

Après mise à jour du code du module (nouveaux champs ou vues paiement), **mettre à jour le module** pour recréer les colonnes et recharger le registre :

```bash
# Exemple : instance locale
odoo-bin -c odoo.conf -d VOTRE_BASE -u dorevia_vault_connector --stop-after-init
# puis redémarrer le serveur Odoo normalement
```

### Erreur Owl : `account.payment` / `dorevia_vault_status` field is undefined

Cela signifie que la **vue** du formulaire paiement référence les champs Vault alors que le **modèle Python** chargé par le serveur ne les expose pas (registre incomplet ou base pas à jour).

1. Vérifier que le répertoire addons contient bien tout le module (notamment `models/vault_connector_account_payment.py`).
2. Lancer **`-u dorevia_vault_connector`** sur la base concernée, puis redémarrer Odoo.
3. Vider le cache navigateur ou forcer un rechargement si une ancienne définition de vue reste en session.

## Configuration

**Paramètres →** section **Dorevia Vault** (ou équivalent selon la vue) :

| Clé (stockage `ir.config_parameter`) | Rôle |
|--------------------------------------|------|
| `dorevia_vault_connector.enabled` | `True` pour activer l’envoi |
| `dorevia_vault_connector.target_url` | URL du POST JSON (ex. `http://127.0.0.1:8091/ingest`) |
| `dorevia_vault_connector.token` | Optionnel, envoyé en `Authorization: Bearer …` |
| `dorevia_vault_connector.timeout_seconds` | Délai max. de la requête |
| `dorevia_vault_connector.tenant` | Identifiant tenant dans le payload |

## Comportement

1. Lors du **post** d’un document ou d’un paiement éligible, si le connecteur est actif et l’URL renseignée, un envoi est tenté **après** `super().action_post()` — une erreur réseau ou applicative côté connecteur **ne bloque pas** la validation comptable (statut `failed` + message).
2. Champs sur la pièce ou le paiement : statut (`todo` / `sent` / `failed`), date du dernier essai, message d’erreur, référence distante si la réponse JSON en contient une (`id`, `ref`, `reference`).
3. Bouton **Réessayer l’envoi Vault** pour les objets éligibles en `failed` ou `todo` (rééligibilité requise).

Types actuellement couverts :

- `out_invoice` : vente
- `in_invoice` : achat
- `out_refund` : avoir client
- `in_refund` : avoir fournisseur
- `account.payment` inbound : encaissement reconnu
- `account.payment` outbound : décaissement reconnu

## Démo locale (récepteur mock)

Procédure détaillée : [RECETTE_LOCALE_V1_DOREVIA_VAULT_CONNECTOR_ODOO19.md](../RECETTE_LOCALE_V1_DOREVIA_VAULT_CONNECTOR_ODOO19.md).

En résumé, depuis la **racine du workspace** `dorevia-saas` :

```bash
python3 scripts/mock_vault_receiver.py
```

Configurer l’URL cible sur `http://127.0.0.1:8091/ingest`, poster une facture client, contrôler le terminal du récepteur et le fichier NDJSON (par défaut `/tmp/dorevia_vault_connector_payloads.ndjson`).

## Documentation liée

| Document | Contenu |
|----------|---------|
| [SPEC_V1_DOREVIA_VAULT_CONNECTOR_ODOO19.md](../SPEC_V1_DOREVIA_VAULT_CONNECTOR_ODOO19.md) | Spec fonctionnelle V1 |
| [PLAN_IMPLEMENTATION_V1_DOREVIA_VAULT_CONNECTOR_ODOO19.md](../PLAN_IMPLEMENTATION_V1_DOREVIA_VAULT_CONNECTOR_ODOO19.md) | Plan d’implémentation |
| [BACKLOG_IMPL_V1_DOREVIA_VAULT_CONNECTOR.md](../BACKLOG_IMPL_V1_DOREVIA_VAULT_CONNECTOR.md) | Backlog ultra-court (étape 8 = recette) |
| [../README.md](../README.md) | Contexte répertoire addons Dorevia |

## Fichiers utiles dans le module

- `models/account_move.py` — documents comptables, `action_post`, rejeu
- `models/vault_connector_account_payment.py` — extension `account.payment` (nom de fichier distinct du module standard `account_payment`)
- `models/res_config_settings.py` — exposition des paramètres
- `services/payload_builder.py` — charge utile document / paiement
- `services/vault_client.py` — envoi HTTP
- `views/` — pièce comptable + paiement + écran de configuration
