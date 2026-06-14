# Séquence reprise Odoo — document historique · pré-pause maquette

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Statut document** | **Historique · pré-pause maquette** — ne pas utiliser comme séquence active |
| **Date** | 2026-06-13 |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Composition Pro** | [`COMPOSITION_PROFESSIONNELS_V1_2.md`](./COMPOSITION_PROFESSIONNELS_V1_2.md) |
| **Composition Header** | [`COMPOSITION_HEADER_V1_2.md`](./COMPOSITION_HEADER_V1_2.md) |

```text
DOCUMENT HISTORIQUE — SÉQUENCE PRÉ-PAUSE MAQUETTE
Séquence active : SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md
Gouvernance active : decision_moa_go_reprise_odoo_v1.md (GO exécution §5 acté · Phase 1 autorisée)
```

> **Renvoi obligatoire** — pour toute reprise Odoo V1, utiliser exclusivement :
>
> * [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) — séquence 10 phases · Phase 1 OK QA
> * [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) — dictionnaire Maquette ↔ Odoo
> * [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) — gouvernance · GO exécution §5 · Phase 1

---

## 1. Contexte historique — phase préparatoire Odoo (avant pause maquette)

Avant la pause maquette V1.2.x, une phase Odoo préparatoire avait été validée pour éviter les 404 sur les liens Header → Professionnels :

| # | Élément | Statut | Référence |
|---|---------|--------|-----------|
| 1 | `/professionnels` | ✅ Composé | [`COMPOSITION_PROFESSIONNELS_V1_2.md`](./COMPOSITION_PROFESSIONNELS_V1_2.md) |
| 2 | Header marchand | ✅ Partiel | [`COMPOSITION_HEADER_V1_2.md`](./COMPOSITION_HEADER_V1_2.md) |

**Motif** : la page `/professionnels` est une dépendance fonctionnelle du Header. Si le Header est composé avant la page cible, les liens **Professionnels** pointent vers une **404**.

Ce capital est **conservé** — cf. Phase 0 de [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md).

---

## 2. Ancienne séquence (obsolète — ne pas exécuter)

```text
Phase Odoo préparatoire (validée · conservée en instance)
1. ✅ /professionnels
2. ✅ Header marchand

Phase maquette Lot 1 — ✅ livré · validé
3. ✅ Accueil · Fiche produit · Professionnels maquette

Phase maquette Lot 2 — ✅ livré · validé
4. ✅ Shop · Catégorie / collection

Phase maquette Lot 3+ — ✅ livré · validé
5. ✅ À propos · Producteur · Recettes · Contact

Phase arbitrage + décisions MOA — ✅ acté
6. ✅ M1–M9 · GO préparation · séquence V1 préparée

Phase Odoo reprise — ⏸ suspendue (GO exécution §5 non acté)
7. ☐ Traduction bloc par bloc — voir SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md
```

---

## 3. Périmètre `/professionnels` (référence conservée)

| Élément | Attendu |
|---------|---------|
| Type | Page CMS Odoo native · Website Builder |
| Portail B2B | ❌ pas de portail B2B custom |
| Tarification B2B | ❌ pas de logique tarifaire B2B publique |
| Développement métier | ❌ pas de dev métier |
| Contenu | Qualification commerciale |
| Double cible | Producteurs / transformateurs créoles · boutiques / distributeurs / restaurants / hôtels / revendeurs |
| Formulaire | `website_crm` natif si disponible |
| Objectif | Demande qualifiée — pas commande B2B |

Référence ticket : [`ticket_moa_composition_cms_ck_01`](../ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) §2.3

---

## 4. Garde-fous maintenus

```text
Odoo 19 CE · Website Builder · snippets first · dorevia_ck_theme
Pas de surcouche autonome · pas de catalogue parallèle
Pas de panier / checkout custom · pas de logique B2B custom V1
Pas de reprise intégrale du prototype HTML
```

---

## 5. Documents liés

| Document | Rôle |
|----------|------|
| [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) | **Séquence active** · 10 phases |
| [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) | **Gouvernance active** · M1–M9 · §5 |
| [`decision_moa_pause_odoo_iteration_maquette_v1_2_x.md`](./decision_moa_pause_odoo_iteration_maquette_v1_2_x.md) | Décision pause maquette (historique) |
| [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](./CADRAGE_MAQUETTE_CK_V1_2_X.md) | Cadrage maquette V1.2.x |
| [`recette_qa_maquette_v1_2_x.md`](./recette_qa_maquette_v1_2_x.md) | Recette QA vision complète |

---

*Document historique · pré-pause maquette · renvoi vers SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md · 2026-06-13.*
