# TICKET — Page produit merchandising MVP2.4

**ID** : `PRODUCT-PAGE-MERCH-MVP24`  
**Date d’ouverture** : 2026-04-28  
**Priorité** : **P2** (enrichissement contenu/merchandising, hors refonte)  
**Statut** : **Prêt pour dev** (orientation MOA validée)  
**Module** : `dorevia_ckreyol_marketplace`  
**Périmètre** : enrichissement éditorial et merchandising léger de la fiche produit, compatible Odoo natif.

**Références** :  
- [TICKET_PRODUCT_PAGE_MVP23.md](TICKET_PRODUCT_PAGE_MVP23.md)  
- [PV_RECETTE_PRODUCT_PAGE_MVP23.md](PV_RECETTE_PRODUCT_PAGE_MVP23.md)

---

## Contexte

La structure MVP2.3 de la fiche produit est validée (grammaire de page en place, invariants respectés).  
Le besoin restant est un enrichissement de la perception de richesse et de crédibilité, sans réouvrir la refonte MVP2.3.

---

## Objectif

Améliorer la qualité perçue des fiches produit via le contenu, les médias et un merchandising simple, en privilégiant les capacités natives Odoo et la maintenabilité.

---

## Doctrine (opposable)

1. **Exploiter d’abord le natif Odoo** (champs, médias, comportements standards).
2. **Enrichir le contenu avant le template**.
3. **Ne pas afficher de sections vides**.
4. **Pas de logique de recommandation complexe** si Odoo ne la fournit pas simplement.
5. **Ne pas toucher** aux routes catalogue, moteur shop, checkout, ni aux invariants MVP2.3.

Tout besoin hors doctrine = nouvel arbitrage MOA.

---

## Périmètre exécutable

### 1) Réassurance (micro-copy)

- Remplacer le libellé `Conditions générales` par **`Achat en confiance`**.
- Conserver le bloc existant (pas de nouveau composant lourd).
- Garder un ton chaleureux, court, factuel.

### 2) Sections produit (alimentation contenu)

Sections attendues quand données présentes :

- description ;
- ingrédients ;
- conservation ;
- conseils de dégustation ;
- spécifications.

Règle stricte :

- afficher uniquement les sections réellement alimentées (aucune section vide/décorative).

### 3) Galerie média

- Enrichir la galerie quand les médias existent.
- Cible recommandée : **3 visuels / produit** quand possible :
  1. packshot ;
  2. détail / texture ;
  3. usage.
- Ne pas casser le fallback 1 média.

### 4) Bloc recommandations

- Afficher `Vous aimerez aussi` **uniquement** si les produits recommandés sont disponibles de manière fiable.
- Si données absentes/instables, masquer proprement le bloc.
- Aucune logique custom complexe de scoring/cross-sell.

### 5) Recette ciblée

- Contrôle sur un échantillon de fiches représentatives :
  - fiche **bonne** (riche) ;
  - fiche **moyenne** ;
  - fiche **pauvre**.

---

## Hors périmètre (non négociable)

- Refonte structurelle de la page produit (déjà traitée MVP2.3) ;
- évolution routes catalogue / moteur shop ;
- modifications checkout/panier ;
- moteur de recommandation avancé custom ;
- refonte UI globale du thème ;
- changement des invariants MVP2.3.

---

## Livrables attendus

| Livrable | Détail |
|----------|--------|
| **QWeb léger** | Ajustements mineurs de libellés/conditions d’affichage sans complexifier le template. |
| **Contenu produit** | Plan d’alimentation minimal des sections (description, ingrédients, conservation, conseils, specs). |
| **Médias** | Règle opérationnelle 1→3 visuels quand possible, sans rupture fallback. |
| **Merchandising simple** | Affichage recommandations uniquement si données fiables, sinon masquage propre. |
| **Recette** | Vérification sur 3 fiches types (bonne, moyenne, pauvre), desktop + mobile essentiel. |

---

## Critères d’acceptation (GO / GO avec réserves / NO GO)

- [ ] Libellé réassurance remplacé par `Achat en confiance` ;
- [ ] Sections produit affichées seulement si alimentées ;
- [ ] Aucune section vide visible ;
- [ ] Galerie enrichie quand médias disponibles ;
- [ ] Fallback 1 média inchangé et stable ;
- [ ] Objectif 3 visuels suivi quand possible (sans blocage si indisponible) ;
- [ ] Bloc `Vous aimerez aussi` affiché seulement si recommandations fiables ;
- [ ] Aucun impact sur shop/checkout/routes ;
- [ ] Aucun impact sur invariants MVP2.3 ;
- [ ] Rendu desktop/mobile essentiel lisible sur fiches bonne/moyenne/pauvre.

---

## Plan d’exécution recommandé

1. **Lot A — micro-copy et règles d’affichage** : réassurance + masquage sections vides.
2. **Lot B — alimentation contenu** : description/ingrédients/conservation/conseils/specs.
3. **Lot C — médias** : enrichissement progressif jusqu’à 3 visuels quand possible.
4. **Lot D — merchandising simple** : recommandations si fiables, sinon masquage.
5. **Lot E — QA** : échantillon 3 fiches + desktop/mobile essentiel.

---

## Dépendances / hypothèses

- L’équipe contenu peut alimenter les champs produits de base.
- Les assets médias existent ou peuvent être produits progressivement.
- Le comportement Odoo natif de recommandations reste la base d’affichage.

---

## Preuve de recette attendue

Recette à consigner dans un PV dédié MVP2.4 merchandising (à créer au lancement exécution).

---

## Prêt pour dev — checklist

1. [x] Orientation MOA validée (vague distincte contenu/merchandising).
2. [x] Doctrine et hors périmètre explicitement figés.
3. [x] Exigence de simplicité/maintenabilité/compatibilité Odoo actée.
4. [ ] Implémentation réalisée.
5. [ ] Recette exécutée sur fiches bonne/moyenne/pauvre.
6. [ ] Décision finale MOA (GO / GO avec réserves / NO GO).

---

## Historique

| Date | Changement |
|------|------------|
| 2026-04-28 | Création du ticket MVP2.4 merchandising à partir de la décision MOA post-validation MVP2.3 ; périmètre limité à l’enrichissement contenu/médias/recommandations simples, sans refonte. |
