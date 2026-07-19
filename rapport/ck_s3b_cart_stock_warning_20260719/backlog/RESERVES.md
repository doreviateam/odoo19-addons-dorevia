# Réserves S3-B — backlog (non bloquantes pour intégration)

## R1 — Reproductibilité Hoot

Industrialiser l’environnement Hoot avec une image navigateur versionnée et épinglée, ou un Dockerfile reproductible.

- **Statut QA :** non bloquant
- **Pendant l’intégration :** ne pas ajouter ce Dockerfile ni modifier l’infra de test

## R2 — Formulation A5 (nouveau produit)

À l’ajout d’un produit absent du panier avec qty > stock, le message reste celui du cœur Odoo (`Vous souhaitez N produits…`), distinct du toast CK sur ligne existante.

- Quantité panier cohérente (plafonnée)
- **Statut QA :** réserve acceptée (mandat A5 hors périmètre)
- Voir aussi `../ck_s3a_audit_panier_stock_20260719/A5_HORS_PERIMETRE_S3B.md`

## R3 — UoM non unitaire

Aucune donnée produit adaptée en recette.

```text
uom_non_unit_test = not_applicable
```
