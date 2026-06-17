# Ticket — Conflit seuil vedettes lot2 vs mode curation · V1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` · C-Kreyol / CK |
| **Module** | `dorevia_ck_marketone_content` |
| **Type** | Dette test · périmètre étroit |
| **Priorité** | Moyenne (non bloquant merge campagne PR-1→4) |
| **Statut** | **Clôturé** — option B implémentée (2026-06-17) |
| **Origine** | Note recette PR-4 (2026-06-17) |
| **Lié à** | [`SYNTHESE_CAMPAGNE_DURCISSEMENT_SECTION3_PR1_PR4_V1.md`](./SYNTHESE_CAMPAGNE_DURCISSEMENT_SECTION3_PR1_PR4_V1.md) · dette « Lot2 seuil » |

```text
Indépendant du pricing H1. Conflit de doctrine de seuil entre le mode curation
(catégorie « Coups de cœur » peuplée) et la sélection automatique des tests lot2.
```

---

## 1. Symptôme

Sur `dorevia_ck_marketone_01`, les tests `test_ck_home_lot2_*` échouent en **mode curation** : la curation expose **3 vedettes** alors que la sélection automatique attend le seuil `MIN_FEATURED_PRODUCTS = 5`.

---

## 2. Analyse

Deux chemins coexistent dans `home_featured.py` :

- **Curation** — `get_curated_featured_variants` : produits rangés dans « Coups de cœur », nombre = contenu de la catégorie (ici 3). Pas de plancher à 5.
- **Repli auto** — `get_ready_featured_variants` : sélection automatique, soumise au plancher `MIN_FEATURED_PRODUCTS = 5`.

`bootstrap_home_featured_products` privilégie la curation si elle existe ; le repli auto (et son seuil de 5) **ne s'applique alors plus**. Les tests lot2 supposent le chemin auto et son seuil → ils deviennent caducs dès qu'une catégorie « Coups de cœur » peuplée est présente sur la base.

C'est donc un **conflit de prémisse de test**, pas un défaut de code produit.

---

## 3. Doctrine

> En mode curation, `get_ready_featured_variants` et le seuil `MIN_FEATURED_PRODUCTS = 5` ne s'appliquent plus. Les tests lot2 doivent expliciter le mode qu'ils testent.

**Aucun changement du seuil `MIN_FEATURED_PRODUCTS` sans arbitrage MOA** (impacte le rendu live du mode auto).

---

## 4. Options de correction (test uniquement)

| Option | Principe | Avantage | Limite |
|--------|----------|----------|--------|
| **A — Skip si curation peuplée** | Taguer / `skipTest` les tests lot2 si une catégorie « Coups de cœur » peuplée existe sur la base. | Minimal, sûr. | Couverture auto non jouée sur bases curées. |
| **B — Forcer le chemin auto** | Dans `setUpClass`, neutraliser la curation (catégorie vide / non référencée) puis appeler explicitement la sélection auto. | Teste réellement le mode auto + seuil 5. | `setUpClass` plus lourd ; doit restaurer l'état. |

Recommandation : **B** si l'on veut conserver la couverture du mode auto ; **A** si l'on considère la curation comme le mode nominal de l'instance (et le mode auto couvert ailleurs).

---

## 5. Hors scope

- Modification de `MIN_FEATURED_PRODUCTS` (arbitrage MOA requis).
- Modification du comportement produit `bootstrap_home_featured_products`.
- Tout lien avec le pricing H1 (PR-4) — sans rapport.

---

## 6. Critère de clôture

- Tests `test_ck_home_lot2_*` verts sur `dorevia_ck_marketone_01` (base curée) **et** sur une base sans curation. ✅ **11/11** (2026-06-17)
- Doctrine §3 référencée dans le test (commentaire) pour éviter la régression de prémisse. ✅ `ck_home_lot2_utils.py`
- Correctif annexe bootstrap : retrait effectif de la section vedettes quand `featured_arch` est vide (`home_featured.py`).

---

*Ticket lot2 · seuil vedettes vs curation · périmètre test étroit · 2026-06-17.*
