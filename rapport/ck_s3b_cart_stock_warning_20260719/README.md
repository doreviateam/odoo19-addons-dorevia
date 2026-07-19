# Archive S3-B — Avertissement stock panier (2026-07-19)

**GO MOA de préparation à l’intégration** — preuves durables, sans chemins locaux ni secrets.

| Élément | Valeur |
|---|---|
| Branche | `refactor/s3-cart-stock-warning` |
| Commit fonctionnel scellé | `66973befa34924fd4c0e2c78c5b661ebb5f86bea` |
| Parent (runtime JS) | `e9fd4c6faefd124d9238b0057a950c12d898aa86` |
| Blob JS scellé | `121cd439c359b2dab3244db48e471905c9ab7a97` |
| Module | `dorevia_ck_marketone_content` **19.0.1.101.0** |
| Verdict QA navigateur | **GO QA AVEC RÉSERVES** |
| Dépôt | `doreviateam/odoo19-addons-dorevia` |
| Base `main` | `68abda898c962be5183a2ee92f1263bb87ec7ac0` |

Tout changement fonctionnel (JS, Python, i18n, manifeste) postérieur à `66973be` annule ce GO.

---

## Contenu

| Dossier / fichier | Contenu |
|---|---|
| `INDEX_SHA.md` | Chronologie des SHA et versions |
| `qa/` | Verdict QA navigateur + critères |
| `garant/` | Synthèse des contrôles Garant pré-QA |
| `captures/` | Toast FR/EN, multi-lignes, mobile 390×844, delete, A5 |
| `results/` | JSON QA expurgé + contexte produits |
| `hoot/` | Extrait Dev : 8/8 Hoot passés sur `66973be` |
| `backlog/RESERVES.md` | Réserves non bloquantes |
| `ENVIRONNEMENTS.md` | Conditions de test + destruction des bases jetables |
| `../ck_s3a_audit_panier_stock_20260719/` | Audit S3-A (préalable) |

---

## Interdictions encore en vigueur jusqu’au GO MOA de fusion

- Pas de merge `main`
- Pas de déploiement / préprod / prod
- Pas de correctif fonctionnel supplémentaire pendant l’intégration
