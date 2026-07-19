# Contrôles Garant — synthèse pré-QA S3-B

| Étape | SHA | Verdict | Notes |
|---|---|---|---|
| Après B2 i18n | `d01b24d` | **FAIL** | F1 chargement `.po` sans `#. odoo-python` ; F2 race swap temporaire `showWarning` ; F3–F5 couverture tests |
| Après F2 | `e9fd4c6` | **PASS AVEC RÉSERVES** | F1–F5 levés ; runtime JS scellé ; réserve Hoot non rejoués côté Garant |
| Après tests only | `66973be` | **PASS AVEC RÉSERVES** (Hoot) · **GO MOA ouverture QA** | Runtime byte-identique à `e9fd4c6` ; 8/8 Hoot exécutés côté Dev ; runner sans faux vert |

## Points gelés

- Pas de copie de `_changeQuantity` — héritage standard + patch permanent `wSaleUtils.showWarning`
- Capture `cartNotificationService` au `CartLine.setup()`
- Garde `assertShowWarningApi()` au chargement
- A5 (`sale.order` nouvel ajout) **hors périmètre** S3-B
