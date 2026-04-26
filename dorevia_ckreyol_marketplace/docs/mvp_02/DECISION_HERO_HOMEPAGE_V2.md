# Décision — Hero Homepage V2

**Statut** : actée (MOA).  
**Date** : 2026-04-24.  
**Périmètre** : bloc **Hero** homepage uniquement (les §2–6 de [1_HOMEPAGE.md](1_HOMEPAGE.md) sont cadrés ailleurs — **ne pas** les traiter dans le périmètre de ce chantier).

## Arbitrage

**Option B** retenue.

## Nature

Évolution **structurelle** du hero (au-delà d’un polish SCSS ou d’un simple renouvellement de médias dans le gabarit actuel).

## Objectif

Passer à un hero **immersif** : image de fond produit, overlay léger, texte aligné à gauche, **deux CTA**.

## Impacts

- **Modification QWeb** : autorisée (périmètre hero).
- **Adaptation SCSS** : autorisée.
- Sortie du seul **polish visuel** ciblé (type lot Phase A « cartes sélection » sans toucher au hero).
- **Ticket dédié** obligatoire **avant** ouverture de PR dev (périmètre, critères d’acceptation, recette, bump manifest si bundle front).

## Justification

Alignement avec la **direction artistique CK** validée (références **Stitch** + **assets** sous `docs/assets/`).

## Cadrage existant à réconcilier en implémentation

- **Copy / gel hero** : toute nouvelle copy hero doit être **reflétée** dans [SPEC_HERO_HOMEPAGE.md](../direction/SPEC_HERO_HOMEPAGE.md) (amendement §7 + historique) une fois le texte figé pour le build cible.
- **Doctrine boutique** : CTA vers `/shop` et `/origines` restent cohérents avec [ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007) et la porte Origines (spec / contrat dans `docs/mvp_01/`).
- **Fichier de travail MVP2** : proposition de contenu et contraintes visuelles — [1_HOMEPAGE.md](1_HOMEPAGE.md).

## Références

| Document | Rôle |
|----------|------|
| [1_HOMEPAGE.md](1_HOMEPAGE.md) | Contenu cible hero + contraintes rendu |
| [SPEC_HERO_HOMEPAGE.md](../direction/SPEC_HERO_HOMEPAGE.md) | Source de vérité copy / structure hero à jour après implémentation |
| [WIREFRAME_HOMEPAGE.md](../direction/WIREFRAME_HOMEPAGE.md) | Cohérence globale homepage (hors périmètre hero si inchangé) |
| [TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md](../crea/TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md) | Contexte appétence / partition ; ticket mère non clos sur le fond |
| [TICKET_HERO_HOMEPAGE_V2.md](../crea/TICKET_HERO_HOMEPAGE_V2.md) | Ticket d’exécution — checklist avant PR, critères d’acceptation |
| [PV_RECETTE_HERO_HOMEPAGE_V2_CK.md](../crea/PV_RECETTE_HERO_HOMEPAGE_V2_CK.md) | Trame de recette MOA après livraison |

## Historique

| Date | Événement |
|------|-----------|
| 2026-04-24 | Création — décision **Option B** ; hero immersif ; QWeb + SCSS ; ticket avant PR. |
| 2026-04-24 | Pilotage : création **TICKET_HERO_HOMEPAGE_V2** + **PV_RECETTE_HERO_HOMEPAGE_V2_CK** ; **§8** ajouté dans [SPEC_HERO_HOMEPAGE.md](../direction/SPEC_HERO_HOMEPAGE.md). |
| 2026-04-24 | **Ticket hero** réaligné (structure MOA complète) ; périmètre décision : hero seul, §2–6 cadrés hors ce chantier. |
| 2026-04-24 | **Livraison code MVP2.1 1/5** — snippet `ckr_hero.xml` + `_hero.scss` refondus (variante immersive `.ckr-hero--immersive`, legacy split conservé), asset `hero_v2_immersive.png` (produit coffret gourmand sur bois), manifest 19.0.1.7.0, CTA2 pointé transitoirement `/shop?ckr_mode=origin` en attendant `/origines` livré par Explorer MVP2 — voir [TICKET_HERO_HOMEPAGE_V2.md](../crea/TICKET_HERO_HOMEPAGE_V2.md) historique. |
| 2026-04-24 | **Recette MOA** — desktop **GO sous réserve mobile** (`19.0.1.7.4`, PV [§1/§8](../crea/PV_RECETTE_HERO_HOMEPAGE_V2_CK.md)) ; décision hero inchangée, clôture chantier 1/5 conditionnée au **GO mobile** (ou dérogation MOA pilotage). |
