# S3-B — A5 hors périmètre (observation QA)

**Décision MOA S3-B :** ne pas overrider `sale.order` pour l’ajout d’un nouveau produit sans ligne existante.

En Odoo 19, cette branche génère encore son propre message inline côté cœur.
Après S3-B2, le chemin « ligne existante » utilise le message CK i18n ; le chemin « nouvelle ligne » peut différer.

À documenter en recette QA et remonter à la MOA après observation du rendu réel — **aucune extension `sale.order` dans S3-B**.
