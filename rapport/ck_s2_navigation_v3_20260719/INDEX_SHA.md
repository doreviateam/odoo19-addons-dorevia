# Chronologie SHA / versions — S2 navigation V3

| Ordre | SHA | Version content | Rôle | Verdict |
|---|---|---|---|---|
| 1 | `c39ce6329f06625efb218198c7aba01046bea010` | 19.0.1.96.0 | Canonicalisation V3 unique autorité | Garant **PASS AVEC RÉSERVES** → QA **NO GO** (collision séquences) |
| 2 | `6afb44d36c6aab4ae905c6fcfcebca502b9bcfa9` | 19.0.1.97.0 | Réparation collisions (1ʳᵉ tentative) | Garant **NO GO** (cascade Producteurs→60 vs rayon BO=60) |
| 3 | `77197a3acecbb832e15c8552f1bdd20ea730d766` | 19.0.1.98.0 | Assignation atomique des séquences | Garant **GO** · QA desktop **GO** (réserve 390px) · mobile 390 **NO GO** (texte Boutique) |
| 4 | `58327b68faa80404a006df7417809bb3953790ea` | 19.0.1.99.0 | Icône Accueil (`ck-nav-shop-root` + `fa-home`) | Garant/QA mobile 390 **GO QA** |

**Commit fonctionnel scellé pour intégration :** `58327b6`  
**Thème testé (install) :** `dorevia_ck_theme` **19.0.1.129.0** (inchangé fonctionnellement pour S2)

Parents directs :

```text
4f6184f (origin/main à l’ouverture)
  └─ c39ce63  refactor V3
       └─ 6afb44d  fix séquences collision
            └─ 77197a3  fix assignation atomique
                 └─ 58327b6  fix icône Accueil   ← scellé
```
