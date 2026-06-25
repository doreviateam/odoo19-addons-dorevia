# Recette QA — Axe B · Libellés navigation & badges · Verdict QA

| Champ | Valeur |
|---|---|
| Projet | `dorevia_ck_marketone` |
| Version | `dorevia_ck_marketone_content` 19.0.1.41.0 |
| Date recette | 2026-06-25 |
| Rédacteur | QA expert Odoo |
| Base | `dorevia_ck_marketone_01` |
| Référence Dev | [RECETTE_QA_AXE_B_LIBELLES_NAV_BADGES_20260625.md](./RECETTE_QA_AXE_B_LIBELLES_NAV_BADGES_20260625.md) |

---

## Verdict

**GO — livraison 19.0.1.41.0 recevable.**

Tous les contrôles automatisés et SQL passent. La grille manuelle desktop/mobile ne peut pas être complétée par recette automatisée (rendu JS) — les contrôles de données confirment la conformité. Une recette visuelle complémentaire est recommandée avant publication en production.

---

## Résultats

### Version et tests automatisés

| Contrôle | Attendu | Constaté | OK |
|---|---|---|---|
| Version module | 19.0.1.41.0 | 19.0.1.41.0 | ✅ |
| Tests `dorevia_ck_nav_axe_b` | au vert | ✅ | ✅ |
| Tests `dorevia_ck_nav_communaute` | au vert | ✅ | ✅ |
| Tests `dorevia_ck_header_v22` | au vert | ✅ | ✅ |
| Tests `dorevia_ck_marketone_nav_sync` | au vert | ✅ | ✅ |
| **Total** | 34/34 | **34/34** | ✅ |

---

### Libellé navigation — « Maison & Bien-être » → « Soin & Bien-être »

```sql
-- Résultat constaté
SELECT id, name->>'en_US', url FROM website_menu
WHERE parent_id = 4 AND name::text ILIKE '%bien%';
-- → id=603 · "Soin & Bien-être" · /shop/category/soin-bien-etre-2
```

| Contrôle | Attendu | Constaté | OK |
|---|---|---|---|
| Entrée « Soin & Bien-être » présente | ✅ | id=603, url=`/shop/category/soin-bien-etre-2` | ✅ |
| Entrée « Maison & Bien-être » absente (menu entier) | 0 occurrence | **0** | ✅ |
| URL catégorie conservée | `/shop/category/soin-bien-etre-2` | `/shop/category/soin-bien-etre-2` | ✅ |
| HTTP `/shop/category/soin-bien-etre-2` | 200 | 200 | ✅ |
| « Maison & Bien-être » absent du HTML Home | 0 occurrence | **0** | ✅ |
| Position dans le menu N2 | après Boissons, avant Artisanat | ✅ (sequence 30) | ✅ |

---

### Ruban — « New! » → « Nouveau ! »

```sql
-- Résultat constaté
SELECT id, name->>'fr_FR', name->>'en_US' FROM product_ribbon
WHERE name::text ILIKE '%nouveau%' OR name::text ILIKE '%new%';
-- → id=4 · "Nouveau !" · "Nouveau !"
```

| Contrôle | Attendu | Constaté | OK |
|---|---|---|---|
| Ruban « Nouveau ! » présent | fr + en = "Nouveau !" | id=4, fr="Nouveau !", en="Nouveau !" | ✅ |
| Aucun ruban « New! » restant | 0 | 0 | ✅ |
| Confiture de goyave — ruban | Nouveau ! | Nouveau ! | ✅ |
| Chapeau Panama — ruban | Nouveau ! | Nouveau ! | ✅ |

---

### Non-régression

| # | Contrôle | Attendu | Constaté | OK |
|---|---|---|---|---|
| 11 | Home section « Nos coups de cœur » | Inchangée | Présente (mentions HTML confirmées) | ✅ |
| 12 | Produits Home vedettes (`ck_is_featured`) | Même sélection | Confiture · Manio Crackers · Savon · Chapeau (4/4) | ✅ |
| 13 | Filmstrip `/shop` | Soin & Bien-être | Non vérifiable via curl (JS) — données DB conformes | ⚠️ Visuel |
| 14 | Routes principales | HTTP 200 | `/odoo/shop` · `/` · `/odoo/shop/cart` · `/shop/category/soin-bien-etre-2` : 200 | ✅ |
| 15 | Catalogue seed | 7 publiés | **7** | ✅ |
| — | Entrée Communauté | Présente, href=# | id=598, url=# | ✅ |
| — | « Coups de cœur » absent du header | 0 | 0 | ✅ |
| — | Menu N2 complet | 8 entrées | 8 (Tous · Épicerie · Boissons · Soin · Artisanat · Communauté · Producteurs · Pro) | ✅ |

---

### Grille manuelle — état

Les contrôles 1–10 de la grille Dev (desktop 1280 / mobile 390) nécessitent une recette visuelle dans le navigateur. Les données DB confirment la conformité ; la vérification visuelle est recommandée avant mise en production.

| # | Contrôle | Données DB | Recette visuelle |
|---|---|---|---|
| 1–2 | Header N3 : Soin visible, Maison absent | ✅ DB | À confirmer visuellement |
| 3 | Lien → `/shop/category/soin-bien-etre-2` · 200 | ✅ | À confirmer visuellement |
| 4–5 | Communauté présente, Coups de cœur absent | ✅ DB | À confirmer visuellement |
| 6 | Mega-menu Soin & Bien-être, titre fallback | ✅ config | À confirmer visuellement |
| 7 | Badge « Nouveau ! » sur cards | ✅ DB (2 produits) | À confirmer visuellement |
| 8–10 | Mobile 390 : drawer, libellés, badges | ✅ DB | À confirmer visuellement |

---

## Observations

### OBS-1 — Ruban id=5 « Coup de cœur » sans traduction fr_FR

Le ruban id=5 (`en_US = "Coup de cœur"`, `fr_FR = NULL`) est assigné à Pâte de manioc et Manio Crackers. Cette situation est **antérieure à ce ticket** et n'a pas été introduite par la livraison 19.0.1.41.0.

En interface française, le ruban s'affichera en fallback `en_US` = "Coup de cœur". Impact limité mais cohérence à compléter lors d'une prochaine passe BO.

### OBS-2 — Entrées menu sans fr_FR (état général)

La majorité des entrées `website_menu` n'ont pas de traduction `fr_FR` (Tous nos produits, Épicerie, Soin & Bien-être, Artisanat, Communauté…). Situation identique aux tickets précédents — le fallback `en_US` assure l'affichage. Ce sujet reste ouvert dans le protocole Axe C (traductions à compléter en BO).

---

## Clôtures

| Référence | Sujet | Statut |
|---|---|---|
| OBS-2 RECETTE_QA_NAV_COMMUNAUTE | « Maison & Bien-être » reconstruit sans correction | ✅ **Soldé** |
| Action 9 · PROTOCOLE_QA_AXE_C | Corriger label menu « Maison & Bien-être » → « Soin & Bien-être » | ✅ **Soldé** |

---

## Réponse à la note Dev

> *« Note : le changement n'est pas encore commité. Indiquez-moi si vous souhaitez un commit + push. »*

La décision commit / push relève de l'Architecte, pas du QA. La recette QA confirme que la livraison est recevable. La suite du workflow (commit, PR, merge) est à déclencher par l'Architecte sur validation de ce verdict.

---

> *Recette réalisée sur `dorevia_ck_marketone_01` · `dorevia_ck_marketone_content` 19.0.1.41.0 · 2026-06-25.*
