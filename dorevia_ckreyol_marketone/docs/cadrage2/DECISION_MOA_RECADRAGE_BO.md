# Décision MOA CK — Recadrage BO prioritaire

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-08 |
| **Module** | `dorevia_ckreyol_marketone` |
| **Statut** | **Validé MOA** |
| **Suite** | [`PROPOSITION_LOT_RECADRAGE_BO_PRODUIT.md`](./PROPOSITION_LOT_RECADRAGE_BO_PRODUIT.md) |

---

Après analyse du module `dorevia_ckreyol_marketone`, la MOA confirme que le projet ne doit **pas** être considéré comme un e-commerce externe déguisé.

Le socle boutique repose bien sur les briques Odoo natives, notamment `website_sale` : catalogue, panier, wishlist et checkout. Le front actuel est donc conservé, sous réserve de corrections, de non-régressions et de maintien des tests existants. Le retour d’analyse confirme que le problème principal n’est pas l’architecture e-commerce, mais la sémantique et l’UX du back-office produit.

---

## Constat MOA

La fiche produit expose aujourd’hui certains champs spécifiques CK avec une sémantique trop technique, notamment le bloc **« Tuile commerce /shop »**.

Ce bloc, placé à proximité de l’image produit standard, peut donner à un utilisateur back-office l’impression d’un système parallèle au standard Odoo, alors que l’objectif est au contraire de rester dans une logique Odoo claire, maintenable et métier.

Le sujet prioritaire est donc le **recadrage du back-office produit**, sans refonte du front.

---

## Décision

À partir de ce recadrage :

- gel des nouveaux lots UX front, hors correction ou régression ;
- prochain lot limité au recadrage BO produit ;
- retrait du bloc **« Tuile commerce /shop »** de la zone image principale ;
- restructuration de la fiche produit en espaces lisibles :
  - **Publication site** ;
  - **Catalogue CK** ;
  - **Qualité image / contenu** ;
  - **Technique** ;
- masquage des champs techniques visibles par défaut, notamment :
  - run CLI ;
  - version recette ;
  - date de traitement batch ;
  - traces/debug techniques ;
- renommage des libellés visibles en langage métier Odoo/MOA ;
- conservation temporaire de `image_shop_tile` comme dérivé média contrôlé, avec fallback vers `image_1920` ;
- aucun changement front tant que ce recadrage BO n’est pas livré et validé ;
- arbitrage Blog / Forum traité séparément, selon le besoin métier réel, et non par automatisme au nom du standard Odoo.

---

## Objectif

Rendre CK pleinement **odoo-iste côté back-office**, sans casser le front existant, qui est déjà fonctionnel, intégré à `website_sale` et couvert par les tests.

Le livrable attendu est donc un lot de **recadrage BO propre, limité et vérifiable**, sans refonte front et sans ajout fonctionnel e-commerce.

---

## Attendu Dev

Le retour Dev porte sur :

1. la proposition de restructuration de la fiche produit ;
2. la liste des champs à conserver, masquer, renommer ou déplacer ;
3. les impacts XML / vues / groupes de sécurité ;
4. les tests de non-régression associés ;
5. la confirmation qu’aucune logique front nouvelle n’est ajoutée dans ce lot.

→ Voir [`PROPOSITION_LOT_RECADRAGE_BO_PRODUIT.md`](./PROPOSITION_LOT_RECADRAGE_BO_PRODUIT.md).
