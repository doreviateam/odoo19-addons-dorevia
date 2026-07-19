# Conditions de test et destruction des environnements jetables

## Conditions communes

- Worktree isolé branche `refactor/s3-cart-stock-warning`
- Mount addons en lecture seule vers ce worktree
- Bases PostgreSQL **jetables** (jamais base partagée / préprod)
- `--db-filter` explicite
- Aucun push / déploiement pendant la recette QA
- Aucune modification de code pendant la recette QA

## QA navigateur (GO AVEC RÉSERVES)

| Paramètre | Valeur |
|---|---|
| SHA | `66973befa34924fd4c0e2c78c5b661ebb5f86bea` |
| Version | `19.0.1.101.0` |
| Conteneur | `ck_s3b_qa_odoo` (éphémère) |
| Base | `ck_s3b_qa1` |
| Navigateur | Chromium (Playwright) |
| Viewport desktop | `1280 × 800` |
| Viewport mobile | `390 × 844` |
| Langues | `fr_FR` / `en_US` (cookie `frontend_lang`) |
| Produits | A stock 2 · B stock 3 · C stock 1 |

## Contrat vérifié

```text
dépassement stock
  → POST /shop/cart/update
  → payload.warning
  → CartLine._changeQuantity
  → wSaleUtils.showWarning (patch CK permanent)
  → cartNotificationService.add → toast CK (.toast.show)
  → #data_warning = 0
```

## Bases / instances détruites (confirmé)

| Nom / usage | Destruction |
|---|---|
| Conteneur `ck_s3b_qa_odoo` | `docker rm` après verdict |
| Base `ck_s3b_qa1` | `DROP DATABASE` confirmé |
| Port local `18081` | down après cleanup |
| Bases Hoot Dev (`ck_s3b_hoot*`) | jetables Dev (hors archive) |
