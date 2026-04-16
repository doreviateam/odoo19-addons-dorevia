# dorevia_membership_roles

## Rôle du module

`dorevia_membership_roles` ajoute un **référentiel de rôles associatifs** dans l’univers **Membership** d’Odoo 19.

Il sépare explicitement :

- l’**adhésion** (module `membership`, statut, facturation, etc.) ;
- les **rôles fonctionnels** de la personne dans l’association (`membership.role`, champ `membership_role_ids` sur les contacts).

## Périmètre Lot 1 (livré)

- modèle `membership.role` (libellé, séquence, archivage, société optionnelle) ;
- attribution **multiple** sur `res.partner` via `membership_role_ids` (tags sur la fiche adhérent / contact) ;
- **portée société** : rôle global si `company_id` est vide, sinon limité à la société ;
- **domaine** sur le contact : rôles globaux + rôles de la société du contact ; si pas de société sur le contact → uniquement les globaux ;
- **rôles archivés** : non proposés pour de nouvelles sélections, mais toujours visibles s’ils étaient déjà attribués (`active_test: False` sur le champ) ;
- **menu** : *Membres* → *Configuration* → *Rôles de membre* (parent `membership.menu_marketing_config_association`) ;
- **sécurité** : lecture large (`base.group_user`), édition du référentiel (`account.group_account_invoice`) + règle multi-sociétés sur `membership.role` ;
- **données initiales** : 7 rôles en français (UTF-8), fichier de données en `noupdate` ;
- **i18n** : `i18n/fr.po` ; migrations optionnelles pour resynchroniser les libellés des rôles prédéfinis.

**Lot 2 — sous-lot A** (`19.0.2.0.1`) : vue **recherche** sur `membership.role` ; héritage de **`base.view_res_partner_filter`** (champ + filtres avec/sans rôle + groupement par rôle) ; bouton **Contacts** sur le formulaire rôle avec compteur.

**Lot 2 — B à E** : backlog — voir la spec §16.

Version actuelle du manifeste : voir `__manifest__.py`.

## Documentation fonctionnelle

- [SPEC V1 — Dorevia membership roles](../../Zedocs/odoo19/modules/dorevia_membership_role/SPEC_V1_DOREVIA_MEMBERSHIP_ROLES.md)

La spec inclut la **matrice de complétude** spec ↔ code, le **jalon Lot 2A** (§0.1–0.2), et les décisions d’architecture ; le gel Lot 2 **B à E** est explicité dans la spec.

## Dépendances

- `membership` (seule dépendance obligatoire).
