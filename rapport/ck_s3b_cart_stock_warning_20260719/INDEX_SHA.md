# Chronologie SHA / versions — S3-B panier stock warning

| Ordre | SHA | Version content | Rôle | Verdict |
|---|---|---|---|---|
| 0 | `68abda898c962be5183a2ee92f1263bb87ec7ac0` | (main) | Base d’ouverture S3-B | — |
| 1 | `b8d3109…` | — | Archive audit S3-A | docs |
| 2 | `1539510…` | 19.0.1.100.0* | B1 : réduction override JS | Dev |
| 3 | `d01b24d…` | — | B2 : message stock i18n | Dev → Garant FAIL (F1 i18n / F2 race) |
| 4 | `8599b27…` | — | F1/F4 : `#. odoo-python` + tests FR | Dev |
| 5 | `e9fd4c6faefd124d9238b0057a950c12d898aa86` | **19.0.1.101.0** | F2 : patch permanent `showWarning` | Garant **PASS AVEC RÉSERVES** (Hoot non rejoués) |
| 6 | `66973befa34924fd4c0e2c78c5b661ebb5f86bea` | **19.0.1.101.0** | Tests Hoot + HttpCase uniquement (runtime inchangé) | Garant **PASS** · QA **GO AVEC RÉSERVES** |

\* versions intermédiaires : voir commits ; scellé d’intégration = `101.0` sur `66973be`.

**Commit fonctionnel scellé pour intégration :** `66973be`  
**Runtime JS byte-identique à :** `e9fd4c6` (blob `121cd439c359b2dab3244db48e471905c9ab7a97`)

Parents directs :

```text
68abda8 (origin/main à l’ouverture)
  └─ b8d3109  docs audit S3-A
       └─ 1539510  refactor JS B1
            └─ d01b24d  i18n B2
                 └─ 8599b27  fix odoo-python
                      └─ e9fd4c6  patch permanent showWarning   ← runtime
                           └─ 66973be  tests Hoot                ← scellé
```
