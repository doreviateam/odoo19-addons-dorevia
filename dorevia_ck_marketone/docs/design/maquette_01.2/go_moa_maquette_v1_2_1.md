# GO MOA — Maquette CK V1.2.1 · Enrichissement avant traduction Odoo home

> **Élargi** par [`decision_moa_pause_odoo_iteration_maquette_v1_2_x.md`](./decision_moa_pause_odoo_iteration_maquette_v1_2_x.md) — vision V1.2.x multi-pages · matérialisation concepts §6.

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Move** | **Move 3 bis** — Enrichissement maquette V1.2 → V1.2.1 |
| **Validateur MOA** | MOA CK |
| **Date** | 2026-06-13 |
| **Brief** | [`brief_maquette_ck_v1_2_1.md`](./brief_maquette_ck_v1_2_1.md) |
| **Base** | Maquette V1.2 livrée · [`LIVRAISON_V1_2.md`](./LIVRAISON_V1_2.md) · arbitrage [`arbitrage_moa_maquette_01_2.md`](./arbitrage_moa_maquette_01_2.md) |

```text
GO MAQUETTE V1.2.1 — ENRICHISSEMENT AVANT TRADUCTION ODOO HOME
HOME ODOO (Hero · réassurance · produits…) : EN PAUSE
```

---

## 1. Décision MOA

La MOA acte la ligne suivante :

| Principe | Décision |
|----------|----------|
| Maquette HTML | **Référence commerciale, visuelle et éditoriale** |
| Odoo | **Exécution progressive** bloc par bloc — jamais en avance sur la maquette |
| Travail Odoo déjà fait | **`/professionnels` + header** — **valide** · ne doit pas inverser la logique |
| Home Odoo V1.2 | **En pause** tant que V1.2.1 n’est pas **prête à traduction** |

```text
La maquette = la spec · Odoo = la copie fidèle
```

---

## 2. Objectif V1.2.1

Pousser la maquette **aussi loin que possible** en gardant une **intégration Odoo réaliste** :

1. **Visuels** réels ou quasi-réels ;
2. **Copy MOA** complet — prêt snippets ;
3. **Polish mobile** + **traduisibilité Odoo** documentée.

V1.2.1 **ne repart pas de zéro** : elle enrichit la structure V1.2 déjà validée (ordre des blocs · doctrine boutique élégante).

---

## 3. Périmètre autorisé

```text
Maquette HTML V1.2.1 — Home desktop + mobile obligatoire
Open Design · artifact repo · copy · visuels · polish responsive
Tableau traduction V1.2.1 — bloc → snippet → route → réserve
```

### Hors périmètre

```text
Hero / réassurance / produits / catégories / coffret / Pro / éditorial / footer — composition Odoo home
Refonte /shop · fiche produit · panier / checkout custom
Front autonome · catalogue parallèle · logique B2B custom
Modification dorevia_ck_theme (sauf bug bloquant documenté)
```

### Odoo — peut continuer (non conflictuel)

```text
Page /professionnels — déjà composée · maintenance légère si besoin
Header / menus — déjà alignés V1.2 · pas de refonte
Données BO · config Dynamic Products · non-régression /shop
```

---

## 4. Garde-fou traduisibilité

> Tout effet ou bloc **non traduisible proprement** dans Odoo Website Builder doit être documenté comme **réserve**, pas comme obligation de développement immédiat.

---

## 5. Livrables attendus

| # | Livrable | Fichier |
|---|----------|---------|
| 1 | Brief V1.2.1 | [`brief_maquette_ck_v1_2_1.md`](./brief_maquette_ck_v1_2_1.md) |
| 2 | Maquette HTML V1.2.1 | [`artifact/index.html`](./artifact/index.html) · Open Design |
| 3 | Note livraison | `LIVRAISON_V1_2_1.md` |
| 4 | Tableau traduction Odoo | [`TABLEAU_TRADUCTION_ODOO_V1_2_1.md`](./TABLEAU_TRADUCTION_ODOO_V1_2_1.md) |
| 5 | Recette QA | `recette_qa_maquette_v1_2_1.md` |

---

## 6. Verdict attendu post-recette

```text
OK MAQUETTE CK V1.2.1 — PRÊTE TRADUCTION ODOO
```

ou

```text
OK PARTIEL MAQUETTE V1.2.1 — réserves documentées
```

Verdict **OK** ou **OK PARTIEL levé** → reprise home Odoo (Hero → …) selon [`go_reprise_odoo_v1_2.md`](./go_reprise_odoo_v1_2.md).

---

## 7. Suite opérationnelle

```text
1. ✅ Décision MOA V1.2.1 — ce document
2. ☐ Validation brief — brief_maquette_ck_v1_2_1.md
3. ☐ Production artifact HTML V1.2.1
4. ☐ Recette QA maquette V1.2.1
5. ☐ Verdict MOA — prête traduction ?
6. ☐ Reprise Odoo home — Hero · réassurance · produits…
```

---

*GO MOA — maquette CK V1.2.1 · enrichissement avant traduction Odoo home · 2026-06-13.*
