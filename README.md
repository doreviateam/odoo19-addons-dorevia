# odoo19-addons-dorevia

**Dépôt GitHub** : [doreviateam/odoo19-addons-dorevia](https://github.com/doreviateam/odoo19-addons-dorevia)

## Objet

Ce répertoire contient les modules Odoo Dorevia retenus pour la **source Odoo 19 locale de démonstration** utilisée dans la chaîne :

**Odoo local → Vault → Lynki**

Il ne s’agit pas d’un dépôt générique d’addons Odoo.  
Il s’agit d’un **sous-ensemble volontairement réduit** de modules `dorevia_*`, reconstruits proprement pour **Odoo 19**, afin d’alimenter une démonstration locale crédible de Dorevia SaaS.

## Documentation canonique (Zedocs)

Les **cadrages, specs, plans, recettes et notes de sandbox** vivent dans le dépôt sous **[`Zedocs/`](../Zedocs/README.md)** (arborescence thématique : vision, Odoo 19, chaîne ingestion, cockpit).

**Convention** : pour tout nouveau module ou jalon documenté, ajouter ou mettre à jour les fichiers dans `Zedocs/` (de préférence sous `Zedocs/odoo19/modules/<nom-kebab>/` pour un module Odoo), puis **pointer depuis ce README** (section modules ou références) vers l’entrée Zedocs — éviter de dupliquer la même spec à la racine de `odoo19-addons-dorevia/`.

## Principe

La règle suivie dans ce répertoire est simple :

> **on ne migre pas le lab Odoo ; on reconstruit un sous-ensemble Dorevia Odoo utile à la chaîne source locale.**

Autrement dit :

- on ne copie pas mécaniquement les modules du lab historique ;
- on ne retient que les modules utiles à la V1 source locale ;
- on réécrit proprement les modules retenus pour Odoo 19 ;
- on garde une frontière nette entre :
  - la **source Odoo locale** ;
  - le **socle de confiance Vault** ;
  - la **surface produit Lynki**.

## Version cible

- **Odoo cible** : `19.0`
- **Rôle du répertoire** : fournir le socle Dorevia minimal côté Odoo pour une démonstration locale
- **Périmètre** : source métier locale, pas produit SaaS complet

## Modules retenus au départ

### Socle minimal V1

Les modules retenus en priorité pour la V1 source locale sont :

- `dorevia_vault_connector` — [spec V1](../Zedocs/odoo19/modules/dorevia-vault-connector/SPEC_V1_DOREVIA_VAULT_CONNECTOR_ODOO19.md), [spec V2 vente/achat/avoir](../Zedocs/odoo19/modules/dorevia-vault-connector/SPEC_V2_DOREVIA_VAULT_CONNECTOR_ODOO19_VENTE_ACHAT_AVOIR.md), [backlog V2](../Zedocs/odoo19/modules/dorevia-vault-connector/BACKLOG_IMPL_V2_DOREVIA_VAULT_CONNECTOR_VENTE_ACHAT_AVOIR.md), [plan](../Zedocs/odoo19/modules/dorevia-vault-connector/PLAN_IMPLEMENTATION_V1_DOREVIA_VAULT_CONNECTOR_ODOO19.md), [recette](../Zedocs/odoo19/modules/dorevia-vault-connector/RECETTE_LOCALE_V1_DOREVIA_VAULT_CONNECTOR_ODOO19.md)
- `dorevia_posted_lock` — [module](./dorevia_posted_lock/README.md), [cadrage](../Zedocs/odoo19/modules/dorevia-posted-lock/CADRAGE_V1_DOREVIA_POSTED_LOCK_ODOO19.md), [spec](../Zedocs/odoo19/modules/dorevia-posted-lock/SPEC_V1_DOREVIA_POSTED_LOCK_ODOO19.md), [plan](../Zedocs/odoo19/modules/dorevia-posted-lock/PLAN_IMPLEMENTATION_V1_DOREVIA_POSTED_LOCK_ODOO19.md), [backlog](../Zedocs/odoo19/modules/dorevia-posted-lock/BACKLOG_IMPL_V1_DOREVIA_POSTED_LOCK.md), [recette](../Zedocs/odoo19/modules/dorevia-posted-lock/RECETTE_LOCALE_V1_DOREVIA_POSTED_LOCK_ODOO19.md)
- `dorevia_membership_roles` — [module](./dorevia_membership_roles/README.md), [spec V1](../Zedocs/odoo19/modules/dorevia_membership_role/SPEC_V1_DOREVIA_MEMBERSHIP_ROLES.md)

### Modules utiles mais non bloquants

Ces modules ne sont pas inclus automatiquement dans la première passe.  
Ils peuvent être ajoutés ensuite si un besoin concret apparaît :

- `dorevia_pos_lna_is_private_ip_guard` — [README](./dorevia_pos_lna_is_private_ip_guard/README.md) — correctif crash JS POS (`isPrivateIp` / LNA) sur certaines images Odoo 19
- `dorevia_core`
- `dorevia_res_config_dms_shim`
- `dorevia_session_guard`
- `dorevia_helloasso_connector` comme socle HelloAsso minimal, si l'on veut ouvrir un premier périmètre API sans embarquer les modules métier `members`, `payment` ou `billetterie`

### Modules HelloAsso versionnés mais non activés dans le socle local

Les modules suivants sont maintenant présents dans ce répertoire pour être versionnés et relus depuis le workspace, mais ils ne font pas partie du **socle local activé par défaut** :

- `dorevia_helloasso_members`
- `dorevia_helloasso_payment`
- `dorevia_helloasso_billetterie`

Architecture transverse des lots (rôles, dépendances, découplage visé) : [ARCHITECTURE_LOTS_HELLOASSO_ODOO19.md](../Zedocs/odoo19/modules/helloasso-dorevia/ARCHITECTURE_LOTS_HELLOASSO_ODOO19.md).

Ils restent dépendants d'un arbitrage explicite sur leur périmètre et leurs dépendances avant activation dans le sandbox Odoo 19.

## Modules explicitement hors périmètre V1

Ne font pas partie du socle initial de ce répertoire pour la V1 source locale :

- `dorevia_vault_connector_hr_payroll`
- `dorevia_adapter_odoo18`
- `dorevia_billing_core`
- `dorevia_helloasso_members`
- `dorevia_helloasso_payment`
- `dorevia_helloasso_billetterie`
- `dorevia_sale_reports`
- `dorevia_sale_report_fix`
- `dorevia_sale_proforma_report_fix`
- `dorevia_report_pdf_layout_fix`
- `dorevia_dlp_connector` (différé, utile plus tard si besoin explicite)

Le statut de conservation de ce sandbox est fixé dans [STATUT_SANDBOX_ODOO19_LOCAL.md](../Zedocs/odoo19/socle/STATUT_SANDBOX_ODOO19_LOCAL.md).

## Rôle dans l’architecture

Ce répertoire couvre uniquement la partie **source Odoo locale**.

La lecture d’ensemble reste :

- **Odoo local** : produit ou porte la donnée métier source
- **Modules Dorevia Odoo** : préparent, sécurisent ou exposent cette donnée
- **Vault** : expose un contrat de confiance et des statuts lisibles
- **Lynki** : compose la lecture, le pilotage et la restitution

## Règle de croissance

Tout nouveau module ajouté ici doit répondre à une question simple :

> **aide-t-il directement la chaîne Odoo local → Vault → Lynki pour une source locale de démonstration crédible ?**

Si la réponse est non, il n’entre pas dans ce répertoire.

## Références

- [Architecture des lots HelloAsso (Zedocs)](../Zedocs/odoo19/modules/helloasso-dorevia/ARCHITECTURE_LOTS_HELLOASSO_ODOO19.md)
- [Recette seed de démonstration Odoo 19 pour Lynki](../Zedocs/odoo19/socle/RECETTE_SEED_DEMO_ODOO19_POUR_LYNKI.md)
- [Index Zedocs](../Zedocs/README.md)
- [BIG_PICTURE_DOREVIA_SAAS.md](../Zedocs/vision/BIG_PICTURE_DOREVIA_SAAS.md)
- [ROLE_DETAILLE_LYNKI_DANS_DOREVIA_SAAS.md](../Zedocs/vision/ROLE_DETAILLE_LYNKI_DANS_DOREVIA_SAAS.md)
- [SELECTION_MODULES_DOREVIA_POUR_SOURCE_ODOO19_LOCALE.md](../Zedocs/odoo19/socle/SELECTION_MODULES_DOREVIA_POUR_SOURCE_ODOO19_LOCALE.md)
