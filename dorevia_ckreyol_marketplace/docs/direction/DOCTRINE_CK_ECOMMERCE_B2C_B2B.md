# Doctrine e-commerce C-Kreyol — B2C & B2B

**Statut :** Doctrine complémentaire **figée** — monde e-commerce uniquement  
**Date :** 2026-04-26  
**Périmètre :** Monde **e-commerce** C-Kreyol (double lecture commerciale)

**Pilotage :** [ADR-CKR-010](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-010). Cohérent avec la [vision média-commerce](VISION_CK_MEDIA_COMMERCE.md) ([ADR-CKR-009](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-009)) — la présente doctrine **précise** le sous-découpage **B2C / B2B** du monde e-commerce ; elle **n’élargit pas** le périmètre de livraison immédiat du MVP. [Note de cadrage Phase 1](NOTE_DE_CADRAGE.md), [modèle commercial ADR-004](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-004).

---

## 1. Intention

Le monde e-commerce de C-Kreyol ne s’adresse pas à un seul public.

Il doit servir deux réalités commerciales complémentaires :

1. **Le B2C**, à destination des particuliers ;
2. **Le B2B**, à destination des professionnels, revendeurs, partenaires distributeurs ou acheteurs en volume.

Cette distinction est structurante pour le positionnement, les prix, l’expérience utilisateur, les règles commerciales et l’exploitation Odoo.

---

## 2. Principe fondateur

> **Le e-commerce C-Kreyol est un espace marchand sanctuarisé, mais non monolithique.**
>
> **Il porte deux lectures commerciales : une lecture B2C avec prix public conseillé, et une lecture B2B avec prix partenaire distributeur.**

Le site doit donc permettre de présenter une même offre produit selon deux logiques :

- une logique **retail grand public** ;
- une logique **réseau partenaire / distribution**.

### 2.1 Catalogue commun, affichage commercial contextualisé

Le **catalogue CK** (produits, fiches, assortiment porté par Odoo) reste **commun** : une seule base d’articles pour tous les visiteurs.

En revanche, l’**affichage commercial** est **contextualisé** : ce que voit le visiteur — en particulier le **prix affiché**, les **remises** applicables et les **conditions de commande** (minimums, délais, modalités relevant du standard Odoo) — **dépend** :

- du **statut** du visiteur (anonyme, connecté, type de compte) ;
- de son **compte client** (partenaire Odoo) et des droits qui y sont attachés ;
- des **listes de prix** qui lui sont **associées** dans Odoo (et, le cas échéant, des règles commerciales natives alignées sur ces listes).

Ainsi, **un même produit** du catalogue peut être **montré** avec une lecture tarifaire et contractuelle **B2C** ou **B2B** selon le contexte, **sans dupliquer** le catalogue en silos parallèles.

---

## 3. Monde B2C — Prix public conseillé

Le B2C correspond au parcours des particuliers.

Il doit proposer :

- une expérience boutique claire, lisible et rassurante ;
- des prix publics cohérents avec le positionnement retail ;
- une mise en avant éditoriale sobre des produits, origines, usages et sélections ;
- une logique d’achat simple : découverte, ajout au panier, paiement, livraison ;
- une perception de confiance : qualité, origine, sérieux, disponibilité, service.

Le prix B2C de référence est le :

> **prix public conseillé**.

Ce prix doit être stable, compréhensible et cohérent avec la valeur perçue du produit.

---

## 4. Monde B2B — Prix partenaire distributeur

Le B2B correspond aux professionnels et partenaires distributeurs.

Il peut concerner notamment :

- épiceries fines ;
- commerces spécialisés ;
- restaurateurs ;
- traiteurs ;
- associations ;
- distributeurs ;
- revendeurs ;
- partenaires événementiels ;
- acheteurs en volume.

Le B2B doit permettre une logique commerciale différente :

- prix partenaire distributeur ;
- marges de revente ;
- volumes ;
- réassort ;
- conditions commerciales spécifiques ;
- éventuellement minimums de commande ;
- éventuellement accès conditionné par compte validé.

Le prix B2B de référence est le :

> **prix partenaire distributeur**.

Ce prix n’est pas destiné à concurrencer le prix public, mais à permettre au partenaire professionnel de revendre ou d’intégrer le produit dans son activité avec une marge cohérente.

---

## 5. Rôle d’Odoo

Odoo est adapté à cette double lecture commerciale et à l’**affichage contextualisé** décrit en **§2.1** (prix visibles, remises, conditions de commande pilotés par **compte** + **pricelists**).

La doctrine CK s’appuie sur les capacités natives ou standardisables d’Odoo, notamment :

- un **catalogue produit commun** ;
- des **listes de prix** différenciées et rattachées au bon **contexte** client / site / session ;
- des **comptes clients** identifiés et leurs **profils** ;
- des **conditions commerciales** par profil client (y compris règles de remise lorsqu’elles relèvent du standard) ;
- une **séparation** exploitable entre affichage **prix public** et **prix partenaire** pour un même `product.template` ;
- une exploitation commerciale **B2C** et **B2B** dans un **même** système.

Principe d’exploitation :

> **Un même produit peut exister dans le catalogue CK, mais être lu différemment selon le type de client : particulier ou partenaire distributeur.**

Alignement avec [ADR-CKR-001](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001) : **standard Odoo d’abord** pour listes de prix et segmentation ; spécifique seulement si le standard ne suffit pas.

---

## 6. Sanctuarisation du e-commerce

Cette doctrine B2C/B2B ne remet pas en cause le principe de **sanctuarisation** du monde e-commerce ([VISION_CK_MEDIA_COMMERCE.md](VISION_CK_MEDIA_COMMERCE.md) §6, [ADR-CKR-009](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-009)).

Le e-commerce reste protégé contre la pollution publicitaire, **quel que soit le public adressé**.

Rappel de principe :

> **La publicité finance l’audience CK, mais n’entre jamais dans l’acte d’achat.**

Cette règle vaut pour :

- le parcours B2C ;
- le parcours B2B ;
- les fiches produits ;
- le panier ;
- le checkout ;
- le compte client ;
- les pages de commande ;
- les espaces de réassort professionnel.

---

## 7. Articulation avec les trois mondes CK

La vision média-commerce CK distingue trois mondes :

1. e-commerce ;
2. éditorial ;
3. communautaire.

La présente doctrine précise uniquement le monde **e-commerce**.

Elle confirme que ce monde e-commerce contient lui-même **deux publics** :

| Public | Logique | Prix de référence | Objectif |
|---|---|---|---|
| B2C | Vente aux particuliers | Prix public conseillé | Achat direct, découverte, réachat |
| B2B | Vente aux professionnels / distributeurs | Prix partenaire distributeur | Distribution, volume, réassort, marge partenaire |

---

## 8. Implications produit et UX

À terme, cette doctrine pourra impliquer :

- une identification claire des clients B2B ;
- un accès aux prix partenaires uniquement pour les comptes autorisés ;
- une différenciation éventuelle des parcours de commande ;
- une documentation commerciale dédiée aux partenaires ;
- des conditions générales adaptées aux ventes professionnelles ;
- une logique de réassort simplifiée ;
- des seuils ou paliers de volume ;
- une présentation sobre mais lisible de l’offre professionnelle.

Ces implications ne constituent **pas** nécessairement un mandat de développement immédiat.

Elles servent d’**orientation** pour éviter de construire une boutique uniquement pensée pour le B2C.

---

## 9. Phrase canonique

> **C-Kreyol vend aux particuliers avec un prix public conseillé, et structure sa distribution professionnelle avec un prix partenaire distributeur.**
>
> **Le catalogue est commun ; l’affichage commercial — prix, remises, conditions — est celui du contexte Odoo du visiteur (compte, listes de prix).**
>
> **Odoo permet de faire cohabiter ces deux mondes commerciaux dans un même catalogue, sans remettre en cause la sanctuarisation du e-commerce.**

---

## 10. Décision

La vision e-commerce CK intègre officiellement une **double cible** :

- **B2C**, avec **prix public conseillé** ;
- **B2B**, avec **prix partenaire distributeur**.

Cette décision doit être prise en compte dans les futurs arbitrages liés :

- aux listes de prix ;
- aux comptes partenaires ;
- aux parcours UX ;
- aux règles de visibilité tarifaire ;
- aux conditions commerciales ;
- à la documentation projet ;
- aux futures spécifications Odoo.

---

## 11. Historique

| Date | Événement |
|---|---|
| 2026-04-26 | Formalisation de la doctrine e-commerce B2C/B2B : prix public conseillé pour les particuliers, prix partenaire distributeur pour les professionnels. |
| 2026-04-26 | Intégration dépôt `docs/direction/` ; [ADR-CKR-010](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-010) ; liens vision, note de cadrage, ADR-001 / 004 / 009. |
| 2026-04-26 | **§2.1** : catalogue **commun** ; **affichage commercial contextualisé** (prix, remises, conditions de commande selon statut, compte, pricelists Odoo). **§5** aligné. |
