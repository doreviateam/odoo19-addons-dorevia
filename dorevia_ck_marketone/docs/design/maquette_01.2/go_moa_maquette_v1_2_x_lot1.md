# GO MOA — Maquette CK V1.2.x · Lot 1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Move** | **Move 4** — Production maquette V1.2.x · Lot 1 |
| **Validateur MOA** | MOA CK |
| **Date** | 2026-06-13 |
| **Décision cadre** | [`decision_moa_pause_odoo_iteration_maquette_v1_2_x.md`](./decision_moa_pause_odoo_iteration_maquette_v1_2_x.md) |
| **Cadrage** | [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](./CADRAGE_MAQUETTE_CK_V1_2_X.md) |
| **Brief base accueil** | [`brief_01_2.md`](./brief_01_2.md) |

```text
GO PRODUCTION MAQUETTE V1.2.x — LOT 1
ODOO EN PAUSE — AUCUNE TRADUCTION ODOO À CE STADE
```

---

## 1. Décision MOA

```text
GO cadrage validé.
```

Priorité **Lot 1** :

1. **Accueil enrichie** V1.2.x ;
2. **Fiche produit type enrichie** ;
3. **Page Professionnels** maquette.

**Objectif** : matérialiser la **promesse CK**, la **valeur produit** et la **double cible B2C/B2B** avant d’étendre au shop complet.

---

## 2. Motif du lot

| Page | Rôle dans la vision CK |
|------|------------------------|
| **Accueil** | Promesse · collections · réassurance · B2C/B2B |
| **Fiche produit** | Valeur CK : origine · usage · recette · producteur · conservation · association · signal pro |
| **Professionnels** | Double cible producteurs / distributeurs — le B2B ne reste pas un simple bouton home |

**Lot 2** (différé) : Shop · Catégorie — dépendent des choix fiche produit et collections commerciales.

---

## 3. Périmètre Lot 1

### IN

| # | Livrable maquette | Fichier artifact (cible) |
|---|-------------------|---------------------------|
| 1 | Accueil enrichie | `artifact/index.html` (évolution V1.2) |
| 2 | Fiche produit type | `artifact/fiche-produit.html` (ou équivalent) |
| 3 | Page Professionnels | `artifact/professionnels.html` (alignée vision · pas copie Odoo) |

Enrichissements transverses Lot 1 :

* visuels réels ou quasi-réels (hero · produits · coffret) ;
* copy MOA complet (promesse · réassurance · B2C/B2B · producteurs) ;
* polish mobile 390 px ;
* routes plausibles ;
* **classes d’arbitrage** par bloc (§4 décision cadre).

### OUT

```text
Shop complet · page catégorie · à propos · recettes/savoirs · contact
Traduction Odoo · reprise home Odoo · dev module · catalogue custom
```

Odoo `/professionnels` + header **conservés** — la maquette Pro est une **cible d’expérience**, pas une copie de l’instance.

---

## 4. Livrables attendus Dev

| # | Livrable | Document |
|---|----------|----------|
| 1 | Artifact HTML Lot 1 mis à jour | `artifact/` |
| 2 | Cadrage complété | [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](./CADRAGE_MAQUETTE_CK_V1_2_X.md) |
| 3 | Première lecture classes d’arbitrage | Cadrage §2 · §10 + [`TABLEAU_TRADUCTION_ODOO_V1_2_1.md`](./TABLEAU_TRADUCTION_ODOO_V1_2_1.md) |
| 4 | Note livraison Lot 1 | `LIVRAISON_V1_2_X_LOT1.md` (à créer) |

---

## 5. Garde-fous

```text
Matérialiser largement → arbitrer à la traduction Odoo
Réserve documentée ≠ obligation Dev Odoo immédiate
Odoo 19 CE · snippets first · pas de surcouche autonome (lecture traduisibilité)
```

---

## 6. Lot 2 — planifié (non lancé)

```text
1. Boutique / Shop
2. Catégorie ou collection type
```

Extension ultérieure selon verdict Lot 1 : à propos · recettes/savoirs · contact.

---

## 7. Suite

```text
1. ✅ GO MOA Lot 1 — ce document
2. ✅ Production artifact HTML Lot 1 — [`LIVRAISON_V1_2_X_LOT1.md`](./LIVRAISON_V1_2_X_LOT1.md)
3. ☐ Recette QA maquette Lot 1
4. ☐ Verdict MOA Lot 1 · classes d’arbitrage
5. ☐ GO Lot 2 ou reprise Odoo — post-arbitrage
```

---

*GO MOA — maquette CK V1.2.x Lot 1 · accueil · fiche produit · professionnels · 2026-06-13.*
