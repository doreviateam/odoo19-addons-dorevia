# ticket_dev_maquette_01_2_open_design — Production maquette CK V1.2 · Boutique élégante

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Type** | Ticket Dev / maquettage — évolution home V1.2 |
| **Suite de** | Maquette V1.1.1 · [`ticket_dev_maquette_01_open_design.md`](../ticket_dev_maquette_01_open_design.md) |
| **Doctrine** | [`note_05.md`](../../cadrage/note_05.md) — **actée MOA** |
| **Brief opérationnel** | [`brief_01_2.md`](./brief_01_2.md) |
| **Recette QA** | [`recette_qa_maquette_01_2.md`](./recette_qa_maquette_01_2.md) |
| **GO MOA** | [`go_moa_maquette_01_2.md`](./go_moa_maquette_01_2.md) — **GO OFFICIEL confirmé** |
| **Date** | 2026-06-13 |
| **Statut** | **Livré Dev — en attente recette QA** |

```text
GO OFFICIEL MOA — PRODUCTION MAQUETTE CK V1.2 — BOUTIQUE ÉLÉGANTE
HOME ODOO : EN PAUSE — cf. go_moa_maquette_01_2.md
```

---

## 1. Objet du ticket

Produire la **maquette CK V1.2 — Home boutique élégante**, évolution marchande de la V1.1.1, conforme au brief [`brief_01_2.md`](./brief_01_2.md) et à la doctrine [`note_05.md`](../../cadrage/note_05.md).

```text
Nous ne maquettisons pas dans Odoo.
Nous maquettisons pour Odoo.
```

Ce ticket **ne déclenche aucune modification** de la home Odoo sur l’instance `dorevia_ck_marketone_01`.

---

## 2. Contexte

Une première traduction Odoo a validé le socle technique :

```text
OK socle technique · OK faisabilité CMS · KO traduction cible commerciale complète
```

La V1.2 corrige l’écart **commercial** — pas l’architecture Odoo.

Référentiel technique maintenu :

```text
Odoo 19 CE · Website Builder · snippets first · pas de surcouche autonome
```

Base esthétique : maquette **V1.1.1** · [`design_01.md`](../design_01.md) v1.1.

---

## 3. Rôles

```text
David   = porteur de vision / décision MOA / arbitrage final
Loulou  = cadrage MOA / doctrine / formalisation / critères
Dev     = exécution et pilotage opérationnel Open Design (ou outil maquette)
QA      = recette maquette — recette_qa_maquette_01_2.md
```

Le Dev **ne modifie pas** la composition home Odoo dans ce ticket.

---

## 4. Périmètre

### Inclus

```text
Home CK V1.2 — desktop + mobile (ou comportement mobile documenté)
Structure des 9 blocs — cf. brief_01_2 §5
Tableau traduction Odoo par bloc — cf. brief_01_2 §5
Produits indicatifs crédibles CK — cf. brief_01_2 §9.B
```

### Exclus

```text
Modification home Odoo / Website Builder
Module dorevia_ck_theme · QWeb · SCSS
Front autonome · catalogue parallèle
Panier / checkout custom · logique B2B custom
Refonte /shop ou fiche produit (hors scope V1.2 — home uniquement)
```

### Parallèle Odoo autorisé (hors ticket Dev maquette)

Sur instance `dorevia_ck_marketone_01`, **sans toucher à la home** :

* page `/professionnels` ;
* menu Professionnels ;
* configuration Dynamic Products ;
* revalidation mobile post-overflow.

---

## 5. Objectif de la mission

Produire une home V1.2 qui traduise la doctrine :

> CK doit être une boutique claire, désirable et rassurante, capable de déclencher l’achat rapidement, tout en conservant une identité soignée.

Renforcer par rapport à V1.1.1 / home Odoo actuelle :

* visibilité **produit** et **prix** plus tôt ;
* **réassurance** haute (≥ 3 preuves) ;
* **catégories** actionnables (routes Odoo plausibles) ;
* **coffrets / sélections** ;
* **entrée Pro** claire (`/professionnels`) ;
* header et footer **sans placeholder** Odoo.

---

## 6. Hiérarchie cible — home V1.2

Ordre desktop — cf. [`note_05.md`](../../cadrage/note_05.md) §4 · [`brief_01_2.md`](./brief_01_2.md) §5 :

1. Header marchand
2. Hero court
3. Réassurance immédiate
4. Produits mis en avant (prix visibles)
5. Catégories / univers actionnables
6. Packs / coffrets
7. Espace professionnel
8. Éditorial / SEO (bas)
9. Footer CK

**Mobile** — ordre strict : hero → preuves → produits → catégories → pro → éditorial → footer.

---

## 7. Contraintes de traduisibilité Odoo

Chaque bloc doit être mappable vers :

* snippet natif Odoo Website Builder, ou
* snippet CK Marketone existant (`s_ck_hero`, `s_ck_reassurance`, `s_ck_category_links`, `s_ck_featured_products`, `s_ck_pro_banner`, …).

Correspondance indicative : [`brief_01_2.md`](./brief_01_2.md) §5.

Interdit :

```text
front autonome · catalogue parallèle · panier custom · B2B custom · maquette non traduisible Builder
```

---

## 8. Compléments QA intégrés au brief

Le Dev doit respecter les compléments §9 du brief :

* **Artisanat** : ne pas surdimensionner — arbitrage MOA en cours ;
* **Produits indicatifs** : liste crédible CK (confiture goyave, crackers, savon vétiver, coffret, …) ;
* **CTA produit** : privilégier `Voir` / `Découvrir` — pas `Ajouter au panier` sans arbitrage ;
* **Réassurance** : promesses tenables opérationnellement ;
* **Liens** : aucun CTA principal vers 404 ;
* **Premier écran desktop** : réassurance ou début produits visible ;
* **Footer** : sans placeholder Odoo · mention Odoo = réserve si non masquable.

---

## 9. Livrables attendus

```text
Maquette CK V1.2 — Home boutique élégante
```

| # | Livrable | Détail |
|---|----------|--------|
| 1 | Maquette desktop | Home complète · 9 blocs |
| 2 | Maquette mobile | **Obligatoire** — ou responsive vérifiable |
| 3 | Tableau traduction Odoo | [`TABLEAU_TRADUCTION_ODOO_V1_2.md`](./TABLEAU_TRADUCTION_ODOO_V1_2.md) |
| 4 | Textes principaux | Promesse · CTAs · preuves · entrées catégories |
| 5 | Note livraison | [`LIVRAISON_V1_2.md`](./LIVRAISON_V1_2.md) — choix · écarts · points à arbitrer |

Formats acceptés : artefact Open Design · HTML exportable · captures · zip · markdown.

---

## 10. Critères d’acceptation (pré-recette Dev)

Le ticket Dev est **livré** si :

```text
□ Home V1.2 desktop produite
□ Maquette mobile obligatoire — ou responsive explicitement vérifiable
□ TABLEAU_TRADUCTION_ODOO_V1_2.md complété
□ Conformité structure brief_01_2 §5
□ Produits + prix visibles tôt (desktop · mobile)
□ ≥ 3 preuves haut de page
□ Catégories avec routes Odoo plausibles
□ CTA Pro sans 404
□ Footer sans placeholder Odoo
□ Tableau traduction Odoo par bloc
□ Aucune modification home Odoo effectuée
```

La **validation MOA/QA** intervient via [`recette_qa_maquette_01_2.md`](./recette_qa_maquette_01_2.md).

---

## 11. Verdict QA attendu (post-livraison)

```text
OK MAQUETTE CK V1.2 — BOUTIQUE ÉLÉGANTE
```

ou

```text
KO MAQUETTE V1.2 — corrections à reprendre
```

ou

```text
OK PARTIEL MAQUETTE V1.2 — réserves à lever avant traduction Odoo
```

---

## 12. Suite après verdict OK

Reprise composition Odoo — cf. [`brief_01_2.md`](./brief_01_2.md) §11 · [`ticket_moa_composition_cms_ck_01`](../ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) §0.3 :

```text
1. Reprise home Website Builder — bloc par bloc
2. Recette composition — recette_qa_composition_cms_ck_01.md
3. Verdict — OK ou KO composition CMS CK 01
```

---

## 13. Retour attendu du Dev

```text
1. Livrables produits (chemins / URLs)
2. Direction visuelle retenue vs V1.1.1
3. Tableau traduction Odoo par bloc
4. Points conformes au brief
5. Points d’écart ou d’attention
6. Points à arbitrer MOA (ex. Artisanat)
7. Limites de la maquette
8. Confirmation : home Odoo non modifiée
```

---

## 14. Rappel gouvernance

```text
GO maquette V1.2 ≠ GO développement Odoo home
GO maquette V1.2 ≠ GO général CK
Home Odoo en pause jusqu’à verdict QA maquette V1.2
Extension hors brief = constat limite + arbitrage MOA + ticket séparé
```

---

## 15. Synthèse

> Produire la maquette CK V1.2 — Home boutique élégante — via Open Design (ou outil maquette), à partir de `brief_01_2.md` et `note_05.md`, sans modifier la home Odoo, avec traduisibilité Website Builder et recette QA `recette_qa_maquette_01_2.md`.

---

*Ticket Dev maquette CK V1.2 — GO OFFICIEL MOA · cf. go_moa_maquette_01_2.md · home Odoo en pause.*
