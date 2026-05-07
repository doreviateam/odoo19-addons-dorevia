# CK — État pré-ouverture commerciale

## 1. Synthèse

Le module `dorevia_ckreyol_marketplace` a atteint un niveau avancé sur le front e-commerce Odoo 19 CE: homepage, boutique, portes catalogue, fiches produit, header/footer, newsletter, demande compte pro et premiers jalons panier.  
L'ensemble n'est plus au stade maquette; c'est un socle installable, cohérent et exploitable en recette.

En revanche, la V1 marchande prête à l'ouverture publique n'est pas encore atteinte: des points structurants restent à consolider (données, ACL, canon URL, tunnel marchand réel, robustesse thème, conformité juridique).

## 2. Réalisé solide

- Homepage MVP2.1 livrée (hero, Explorer, sélection, newsletter, réassurance) avec validations directionnelles.
- Boutique `/shop` fortement intégrée à Odoo natif (filtres CK, chips commerciaux, catégories/origines/collections, tuiles produit).
- Fiches produit enrichies en conservant une base `website_sale` standard.
- Portes catalogue actives (`promotions`, `kits`, `origines`, `collections`, `incontournables`, `catégories`).
- Newsletter branchée sur `mass_mailing` (POST public CSRF, gestion duplicat/erreur).
- Demande compte pro MVP03 reliée à `website_crm` sans activation B2B automatique.
- Panier Palier A couvert sur invariants structurels.

## 3. Périmètre encore partiel

- Panier encore partiellement couvert en parcours réel (édition quantités, suppression, comportement multi-cas).
- Checkout/paiement/livraison essentiellement sur standard Odoo, sans couverture CK complète.
- B2B encore limité au flux "demande de compte pro" (pas de workflow partenaire complet).
- Favoris présents côté UI mais lot fonctionnel encore à stabiliser.
- Pages légales présentes, mais relecture juridique à finaliser avant ouverture.

## 4. Risques techniques identifiés

- Unicité slugs `unique(website_id, slug)` insuffisante quand `website_id IS NULL` (PostgreSQL).
- Ambiguïté ACL/record rules autour de l'exposition publique des collections.
- Fragilité potentielle sur XPaths liés au thème `theme_classic_store`.
- Documentation parfois contradictoire avec le code (routes canoniques, redirections, portes).

## 5. Risques fonctionnels marchands

- Absence de preuve bout-en-bout qu'un client peut acheter sans friction sur tous les cas clés.
- Risque de divergence UX/doc sur URLs marketing vs URLs effectivement servies.
- Risque de régression silencieuse sur `/shop` lors d'updates de thème ou d'Odoo.
- Risque de non-conformité perçue si juridique et communications légales ne sont pas consolidés.

## 6. Priorités avant ouverture publique

1. Corriger l'unicité slugs collections/origines (cas `website_id NULL`) + tests.
2. Trancher et documenter l'exposition publique des collections (ACL/rules).
3. Produire un canon URL unique et nettoyer les docs contradictoires.
4. Étendre les tests tunnel marchand réel (panier -> checkout -> paiement -> confirmation).
5. Vérifier systématiquement install/update/rendu (`/`, `/shop`, `/shop/cart`) sans erreur serveur.
6. Finaliser les vérifications juridiques minimales avant communication publique.

## 7. Décision

CK dispose d’un socle front e-commerce avancé et cohérent. Avant d’ouvrir une nouvelle phase, le projet entre dans une passe de consolidation : données, ACL, canon URL, panier réel, checkout, paiement/livraison, juridique et tests bout-en-bout.
