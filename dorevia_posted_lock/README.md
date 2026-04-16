# dorevia_posted_lock

## Rôle

`dorevia_posted_lock` renforce la crédibilité comptable de la source Odoo locale.

Dans sa V1 Odoo 19, le module porte une règle volontairement minimale :

> une **facture client** (`out_invoice`) déjà **postée** ne peut pas revenir en
> brouillon via `button_draft`.

Sur le formulaire, le bouton **Remettre en brouillon** est piloté par le champ
calculé standard `show_reset_to_draft_button` : ce module le force à **faux**
pour les `out_invoice` **postées**, afin de masquer le bouton (en plus du blocage
`UserError` si l’action est quand même invoquée).

## Périmètre V1

- modèle : `account.move`
- type : `out_invoice`
- état : `posted`
- UI : `show_reset_to_draft_button` forcé à `False`
- action bloquée : `button_draft` → `UserError` (filet RPC / hors UI)

## Hors périmètre V1

- autres types de pièces
- blocage `write` / `unlink`
- groupes de bypass
- logique de verrouillage plus large

## Dépendances

- `account`

## Références

Documentation détaillée dans **Zedocs** (chemins relatifs depuis ce fichier) :

- [CADRAGE_V1_DOREVIA_POSTED_LOCK_ODOO19.md](../../Zedocs/odoo19/modules/dorevia-posted-lock/CADRAGE_V1_DOREVIA_POSTED_LOCK_ODOO19.md)
- [SPEC_V1_DOREVIA_POSTED_LOCK_ODOO19.md](../../Zedocs/odoo19/modules/dorevia-posted-lock/SPEC_V1_DOREVIA_POSTED_LOCK_ODOO19.md)
- [PLAN_IMPLEMENTATION_V1_DOREVIA_POSTED_LOCK_ODOO19.md](../../Zedocs/odoo19/modules/dorevia-posted-lock/PLAN_IMPLEMENTATION_V1_DOREVIA_POSTED_LOCK_ODOO19.md)
- [BACKLOG_IMPL_V1_DOREVIA_POSTED_LOCK.md](../../Zedocs/odoo19/modules/dorevia-posted-lock/BACKLOG_IMPL_V1_DOREVIA_POSTED_LOCK.md)
- [RECETTE_LOCALE_V1_DOREVIA_POSTED_LOCK_ODOO19.md](../../Zedocs/odoo19/modules/dorevia-posted-lock/RECETTE_LOCALE_V1_DOREVIA_POSTED_LOCK_ODOO19.md)
