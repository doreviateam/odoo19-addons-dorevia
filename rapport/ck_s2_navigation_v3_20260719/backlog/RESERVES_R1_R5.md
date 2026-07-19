# Réserves techniques — backlog (hors fusion S2)

Ces points sont **explicitement hors périmètre** de la branche d’intégration.
Ils ne doivent pas être corrigés opportunément sur `refactor/s2-canonical-navigation-v3`.

## R1 — Writers secondaires (sévérité moyenne)

- `sync_communaute_header` / `_sync_communaute` peuvent encore créer « Communauté » (CSS V2.2).
- `sync_shop_root_icon_header` peut réinjecter « Tous nos produits ».
- Non appelés par les hooks/upgrade courants ; API encore publique (tests / migrations historiques).
- Un resync V3 ultérieur restaure l’état canonique — pollution temporaire possible.

## R5 — Helpers V2.2 morts (sévérité moyenne/basse)

- Code encore présent dans `nav_sync.py` : `_prune_unmanaged_root_menus`, `_sync_mega_rayon`, `_sync_producteurs`, etc.
- `_prune_unmanaged_root_menus` pourrait supprimer Boutique/Professionnels **s’il était rappelé** (hors chemin runtime actuel).
- Dette : neutraliser / stubber / supprimer dans un ticket Dev ultérieur.

## Autres réserves basses (à conserver)

| Id | Sujet |
|---|---|
| R2 | Pas de contrainte SQL d’unicité sur `(website_id, parent_id, ck_nav_category_id)` |
| R3 | Snapshot d’idempotence ne couvre pas encore `is_visible` |
| R4 | Sur fresh-install, certains tests skip si seed Épicerie MOA absent (non bloquant) |

## Ticket backlog suggéré

> S2-dette — Neutraliser writers R1 (`sync_communaute_header`, `sync_shop_root_icon_header`) et retirer/stubber helpers V2.2 morts (R5) ; évaluer contrainte SQL `ck_nav_category_id` (R2) et extension snapshot `is_visible` (R3).
