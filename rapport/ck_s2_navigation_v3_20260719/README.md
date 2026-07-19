# Archive S2 — Navigation V3 canonique (2026-07-19)

**GO MOA de préparation à l’intégration** — preuves durables, sans chemins locaux ni secrets.

| Élément | Valeur |
|---|---|
| Branche | `refactor/s2-canonical-navigation-v3` |
| Commit fonctionnel scellé | `58327b68faa80404a006df7417809bb3953790ea` |
| Parent | `77197a3acecbb832e15c8552f1bdd20ea730d766` |
| Module | `dorevia_ck_marketone_content` **19.0.1.99.0** |
| Verdict final QA | **GO QA** (mobile 390×844) |
| Dépôt | `doreviateam/odoo19-addons-dorevia` |

Tout changement fonctionnel postérieur à `58327b6` annule ce GO.

---

## Contenu

| Dossier / fichier | Contenu |
|---|---|
| `INDEX_SHA.md` | Chronologie des SHA et versions testés |
| `livrables/` | Livrables Dev (canonicalisation, séquences, icône Accueil) |
| `garant/` | Verdicts Garant (PASS réserves, GO atomique, GO final icône) |
| `qa/` | NO GO séquences, GO desktop ciblé, NO GO puis GO mobile 390 |
| `captures/` | Header / drawer / sous-catégories (GO) + preuves NO GO historiques |
| `results/` | JSON expurgés (GO + NO GO mobile) |
| `backlog/RESERVES_R1_R5.md` | Réserves hors périmètre d’intégration |
| `ENVIRONNEMENTS.md` | Conditions de test + destruction des bases jetables |

---

## Interdictions encore en vigueur jusqu’au GO MOA de fusion

- Pas de merge `main`
- Pas de déploiement / préprod / prod
- Pas de correctif fonctionnel supplémentaire (R1/R5 inclus)
