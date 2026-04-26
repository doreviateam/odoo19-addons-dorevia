# Prompt de lancement — MVP2.1 Homepage C-Kreyol

Tu interviens sur le module Odoo **`dorevia_ckreyol_marketplace`** pour lancer l’exécution **MVP2.1 — Homepage**.

Le cadrage global est **gelé** côté MOA.  
**Ne pas rouvrir** l’ordre des blocs ni le périmètre structurel sans **ticket MOA** de révision.

## Statut (2026-04-25)

**Vague homepage MVP2.1 — clôturée côté MOA.** Les cinq chantiers sont **recettés** ; suite : amélioration continue — voir [README MVP 02](../mvp_02/README.md). Ce prompt reste une **référence historique** d’exécution.

## Objectif MVP2.1

Faire évoluer la homepage C-Kreyol en **5 chantiers d’implémentation**, dans l’ordre suivant :

1. **Hero immersif**
2. **Explorer — grille asymétrique**
3. **Sélection produits dynamique**
4. **Inscription / cercle C-Kreyol**
5. **Réassurance / confiance**

Le bloc **Éditorial** reste conservé en **V1** et **hors périmètre MVP2.1**, sauf demande explicite.

## Documents de référence

Lire en priorité :

- [`docs/mvp_02/README.md`](../mvp_02/README.md) — **Pilotage MVP2.1** (ordre merge, précisions MOA, assets, recette par PR).
- [`docs/mvp_02/1_HOMEPAGE.md`](../mvp_02/1_HOMEPAGE.md) — canon homepage §1–6, **gel conception**.
- [`docs/mvp_02/DECISION_HERO_HOMEPAGE_V2.md`](../mvp_02/DECISION_HERO_HOMEPAGE_V2.md).
- [`docs/mvp_02/DECISION_EXPLORER_HOMEPAGE_MVP2.md`](../mvp_02/DECISION_EXPLORER_HOMEPAGE_MVP2.md).
- [`docs/mvp_02/DECISION_PRODUITS_HOMEPAGE_MVP21.md`](../mvp_02/DECISION_PRODUITS_HOMEPAGE_MVP21.md).
- [`docs/mvp_02/DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md`](../mvp_02/DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md).
- [`docs/crea/PLATEFORME_MARQUE_CK_V1.md`](../crea/PLATEFORME_MARQUE_CK_V1.md).
- [`docs/crea/CADRAGE_DESIGN_CREATION_CK_V1.md`](../crea/CADRAGE_DESIGN_CREATION_CK_V1.md).
- [`docs/mvp_01/SPEC_SHOP_PORTES.md`](../mvp_01/SPEC_SHOP_PORTES.md).

## Ordre de merge validé

| # | Chantier | Ticket |
|---|-----------|--------|
| 1 | Hero | [`HERO-HOMEPAGE-V2`](../crea/TICKET_HERO_HOMEPAGE_V2.md) |
| 2 | Explorer | [`EXPLORER-HOMEPAGE-MVP2`](../crea/TICKET_EXPLORER_HOMEPAGE_MVP2.md) |
| 3 | Sélection produits | [`SELECTION-PRODUITS-HOMEPAGE-MVP21`](../crea/TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md) |
| 4 | Inscription | [`INSCRIPTION-HOMEPAGE-MVP21`](../crea/TICKET_INSCRIPTION_HOMEPAGE_MVP21.md) |
| 5 | Réassurance | [`REASSURANCE-HOMEPAGE-MVP21`](../crea/TICKET_REASSURANCE_HOMEPAGE_MVP21.md) |

**Une PR par chantier.** **Recette MOA à chaque PR** (PV dédié).

## Règles générales

- Respecter **Odoo 19 CE**.
- **QWeb + SCSS** uniquement sauf besoin justifié.
- Ne **pas** créer de moteur e-commerce parallèle.
- **Ne pas modifier** l’ordre des blocs homepage.
- Utiliser les **assets locaux** dans `docs/assets/` en priorité.
- **Pas d’image externe** en production sans validation MOA.
- Pas de **sur-promesse** logistique ([ADR-CKR-005](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)).
- Pas de **faux prix**, pas de **données hardcodées** si Odoo peut fournir la donnée.

## Assets

Banque d’images locale : **`docs/assets/`** (inventaire : [README du module](../../README.md), **Références visuelles MVP 02**).

Règles :

- images **réelles** : produits, producteurs, gestes, ateliers ;
- pas d’images touristiques ;
- pas d’illustrations ;
- cohérence CK : **chaud, sobre, crédible**.

## Points MOA déjà tranchés

### Hero

Hero **immersif** avec **image produit en fond**, **overlay léger**, **texte à gauche**, **deux CTA** (`/shop`, `/origines`).

### Explorer

**Grille asymétrique** de **5 portes** :

1. Promotions
2. Kits
3. Catégories
4. Collections
5. Origines

### Produits

**4 produits dynamiques** issus de **`website_sale`**, avec **prix dynamique** et **accès fiche produit**.  
**Pas d’ajout panier direct** en MVP2.1. Sélection **explicite / maintenable** côté BO (liste produits ou snippet Website).

### Inscription

**Formulaire léger custom** par défaut.  
Lien politique de confidentialité : **`/privacy`**.  
Libellé exact du lien : **politique de confidentialité**.  
**Avant prod.** : pages **`/privacy`** et **`/terms`** publiées par le module (politique RGPD structurée ; mentions légales avec **hébergeur** sur la page — vérifier cohérence avec l’infra réelle). Relecture juridique recommandée.

### Réassurance

**Cible 5 items**.  
Fallback accepté en **3 axes enrichis** si la lisibilité l’exige.

## Attendu

- **Démarrer** par le ticket **`HERO-HOMEPAGE-V2`**.
- **Ne pas enchaîner** sur le ticket suivant avant **validation MOA** de la PR précédente, sauf **accord explicite**.

## Historique

| Date | Événement |
|------|-----------|
| 2026-04-24 | Création — lancement MVP2.1 (5 chantiers, gel conception, `/privacy`, assets locaux, recette à chaque PR). |
| 2026-04-25 | **Clôture MOA** — homepage MVP2.1 recettée (PV Inscription + Réassurance ; pilotage [README MVP 02](../mvp_02/README.md)). |
| 2026-04-25 | **Correctifs post-audit** — contrôleur cercle (`sub.search`) ; `/privacy` + `/terms` + tests `dorevia_ckr_circle` ; hébergeur LCEN sur `/terms` — détail [README module](../../README.md) § Pages légales. |
