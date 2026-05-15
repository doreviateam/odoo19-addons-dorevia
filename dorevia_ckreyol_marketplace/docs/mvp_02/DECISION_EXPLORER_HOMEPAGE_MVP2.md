# Décision — Explorer Homepage MVP2 (grille asymétrique)

**Statut** : actée (MOA).  
**Date** : 2026-04-24.  
**Périmètre** : bloc **Explorer** (cinq portes catalogue — `ckr_entries` / `#explorer-catalogue`).

## Arbitrage structurel

**Option retenue** : **grille asymétrique MVP2**.

- **Vérité actuelle (V1)** : **rail horizontal manuel** (prev / next, **sans autoplay**) — `views/snippets/ckr_entries.xml`, [WIREFRAME_HOMEPAGE.md — Bloc 3](../direction/WIREFRAME_HOMEPAGE.md).
- **Cible MVP2** : **grille asymétrique** pour le bloc Explorer, avec hiérarchie visuelle (Promotions dominante, Kits secondaire fort, trois autres portes en cartes simples) — détail [1_HOMEPAGE.md §2](1_HOMEPAGE.md).

**Condition d’exécution** : **ticket dédié** + **PR** après checklist pilotage ([TICKET_EXPLORER_HOMEPAGE_MVP2.md](../crea/TICKET_EXPLORER_HOMEPAGE_MVP2.md)).

## Ordre des portes **retenu** (MVP2 — cible post-implémentation)

L’ordre **affiché** après livraison doit être :

1. **Promotions** → `/promotions`  
2. **Kits** → `/kits`  
3. **Catégories** → `/categories`  
4. **Collections** → `/collections`  
5. **Origines** → `/origines`  

> **Écart avec V1** : jusqu’à la PR, le snippet conserve l’ordre **Promotions → Collections → Kits → Catégories → Origines**. La PR MVP2 **réordonne** le DOM pour respecter la liste ci-dessus.

## Impacts

- **QWeb** : restructuration du bloc (grille, spans, suppression ou adaptation du conteneur « carousel » / boutons nav si inutiles en grille).
- **SCSS** : mise en page asymétrique, responsive, états hover/focus.
- **Accessibilité** : révision des rôles ARIA (`carrousel` / `region`) si le pattern n’est plus un rail scrollable.
- **Documentation** : après merge, aligner [WIREFRAME_HOMEPAGE.md](../direction/WIREFRAME_HOMEPAGE.md) Bloc 3 (et tout extrait de spec qui décrit explicitement le rail comme **seule** forme) pour refléter la **grille MVP2** — **même PR ou commit doc immédiat** (zéro dérive).

## Justification

Montée en **partition** et **hiérarchie visuelle** perçues (cadrage design & appétence), sans changer les **URL** ni la doctrine des portes ([ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007), [SPEC_SHOP_PORTES.md](../mvp_01/SPEC_SHOP_PORTES.md)).

## Références

| Document | Rôle |
|----------|------|
| [1_HOMEPAGE.md](1_HOMEPAGE.md) | Contenu cible §2 (poids des cartes, contraintes) |
| [TICKET_EXPLORER_HOMEPAGE_MVP2.md](../crea/TICKET_EXPLORER_HOMEPAGE_MVP2.md) | Exécution — checklist avant PR |
| [PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md](../crea/PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md) | PV recette : **GO MOA 2026-04-24** (réserve mineure §3) |
| [DECISION_HERO_HOMEPAGE_V2.md](DECISION_HERO_HOMEPAGE_V2.md) | Hero MVP2 (chantier parallèle ou même vague — coordonner les PR) |
| [TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md](../crea/TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md) | Ticket mère partition / appétence |

## Historique

| Date | Événement |
|------|-----------|
| 2026-04-24 | Création + pilotage — grille asymétrique MVP2 ; ordre Promotions → Kits → Catégories → Collections → Origines ; [TICKET_EXPLORER_HOMEPAGE_MVP2.md](../crea/TICKET_EXPLORER_HOMEPAGE_MVP2.md) + [PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md](../crea/PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md) ; [1_HOMEPAGE.md](1_HOMEPAGE.md) §2 aligné. |
| 2026-04-24 | **Ticket Explorer** réécrit (fiche MOA / dev complète) ; conservation checklist §0, routes MVP1, ancre `#explorer-catalogue`. |
| 2026-04-24 | **Livraison code** : module `19.0.1.8.0` — `ckr_entries.xml` grille asymétrique, `_entries.scss`, retrait `ckr_entries_carousel.js` ; CTA hero secondaire `/origines` ; tests `dorevia_ckr_explorer`. |
| 2026-04-24 | **19.0.1.8.1** : correctif `__manifest__.py` (description RST, coupure `non-` en fin de ligne) ; visuels portes (copies `docs/assets` mvp02 → `static/src/img/explorer_porte_*.png`) ; README tableau mapping. |
| 2026-04-24 | **19.0.1.8.2** : grille desktop **8+4** (Promo/Kits), hiérarchie visuelle (hauteurs média, typo) ; micro-copy e-commerce (snippet) ; visuel **Origines** (épices / terroir, hors carte postale). |
| 2026-04-24 | **Recette MOA** : **GO** — [PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md](../crea/PV_RECETTE_EXPLORER_HOMEPAGE_MVP2_CK.md) §3 (réserve : « coups de cœur » Collections). Chantier **3/5** déblocable. |
