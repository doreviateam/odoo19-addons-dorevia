# GO OFFICIEL MOA — Production maquette CK V1.2 · Boutique élégante

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Move** | **Move 3** — Production maquette CK V1.2 |
| **Décision** | **GO MOA confirmé** |
| **Validateur MOA** | MOA CK |
| **Verdict QA document** | **OK** — document propre · clair · opposable (2026-06-13) |
| **Date** | 2026-06-13 |
| **Documents de référence** | [`note_05.md`](../../cadrage/note_05.md) · [`brief_01_2.md`](./brief_01_2.md) · [`ticket_dev_maquette_01_2_open_design.md`](./ticket_dev_maquette_01_2_open_design.md) · [`recette_qa_maquette_01_2.md`](./recette_qa_maquette_01_2.md) · [`arbitrage_moa_maquette_01_2.md`](./arbitrage_moa_maquette_01_2.md) |

```text
GO OFFICIEL — PRODUCTION MAQUETTE CK V1.2 · BOUTIQUE ÉLÉGANTE
HOME ODOO : REPRISE AUTORISÉE — GO traduction post-arbitrage MOA 2026-06-13
```

---

## 1. Décision MOA

La MOA acte le **GO** pour la production de la maquette V1.2, sur la base des documents suivants :

| Document | Rôle |
|----------|------|
| [`note_05.md`](../../cadrage/note_05.md) | Doctrine MOA / décision de réorientation |
| [`brief_01_2.md`](./brief_01_2.md) | Commande opérationnelle maquette V1.2 |
| [`ticket_dev_maquette_01_2_open_design.md`](./ticket_dev_maquette_01_2_open_design.md) | Périmètre d’exécution Dev / maquettage |
| [`recette_qa_maquette_01_2.md`](./recette_qa_maquette_01_2.md) | Grille de recette QA post-livraison |

---

## 2. Objectif

Produire une nouvelle version de la home CK orientée :

```text
Boutique élégante
```

La cible n’est **pas** une vitrine premium contemplative.
La cible est une boutique **claire, désirable et rassurante**, capable de déclencher l’achat rapidement, tout en conservant une identité soignée.

La maquette doit renforcer :

* la visibilité immédiate des produits ;
* la présence des prix ;
* les preuves de confiance ;
* les catégories actionnables ;
* les packs / coffrets ;
* l’entrée professionnelle ;
* la traduisibilité réaliste dans Odoo Website Builder.

---

## 3. Périmètre autorisé

Le périmètre du GO porte **uniquement** sur :

```text
Maquette CK V1.2 — Home desktop + mobile obligatoire
```

La **maquette mobile est obligatoire** pour une home e-commerce. À défaut : déclinaison responsive **explicitement vérifiable** (captures ou artefact mobile distinct).

Doctrine technique maintenue :

```text
Odoo 19 CE
Website Builder
snippets first
pas de surcouche autonome
pas de catalogue parallèle
pas de panier / checkout custom
pas de logique B2B custom
```

---

## 4. Home Odoo — reprise autorisée

La **home Odoo reprend** selon la maquette V1.2 recettée et l’arbitrage MOA acté — cf. [`arbitrage_moa_maquette_01_2.md`](./arbitrage_moa_maquette_01_2.md).

```text
GO TRADUCTION ODOO — MAQUETTE CK V1.2
AVEC RÉSERVES MOA ACCEPTÉES
```

Travaux Odoo **prioritaires en parallèle** :

* page `/professionnels` — **obligatoire avant mise en ligne publique** ;
* menu Professionnels ;
* configuration Dynamic Products ;
* revalidation mobile / overflow ;
* mapping routes BO (fiches produits · catégories · logo · `/legal`).

Référence instance : [`REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md`](../REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md)

---

## 5. Livrables attendus

| # | Livrable | Fichier / format |
|---|----------|------------------|
| 1 | Maquette V1.2 desktop | Artefact Open Design · HTML · captures |
| 2 | Maquette V1.2 mobile | **Obligatoire** — ou responsive vérifiable |
| 3 | Note de livraison | [`LIVRAISON_V1_2.md`](./LIVRAISON_V1_2.md) |
| 4 | Tableau traduction Odoo par bloc | [`TABLEAU_TRADUCTION_ODOO_V1_2.md`](./TABLEAU_TRADUCTION_ODOO_V1_2.md) — **fichier dédié obligatoire** |
| 5 | Réserves ou arbitrages | Section dédiée dans `LIVRAISON_V1_2.md` ou liste séparée |

> Le tableau Odoo ne doit **pas** être noyé dans `LIVRAISON_V1_2.md` seul — il vit dans [`TABLEAU_TRADUCTION_ODOO_V1_2.md`](./TABLEAU_TRADUCTION_ODOO_V1_2.md) (grille pré-positionnée · à compléter à la livraison).

---

## 6. Recette attendue

La maquette sera recettée avec :

[`recette_qa_maquette_01_2.md`](./recette_qa_maquette_01_2.md)

Verdicts possibles :

```text
OK MAQUETTE CK V1.2 — BOUTIQUE ÉLÉGANTE
```

ou

```text
OK PARTIEL MAQUETTE V1.2 — réserves à lever avant traduction Odoo
```

ou

```text
KO MAQUETTE V1.2 — corrections à reprendre
```

---

## 7. Principe de travail

> *Culture MOA — rappel projet, hors critères opposables du GO.*

Le projet CK est conduit par **itérations courtes**.

L’objectif n’est pas de produire une version parfaite du premier coup, mais de faire progresser :

* la qualité commerciale ;
* la qualité perçue ;
* la traduisibilité Odoo.

Principe MOA retenu :

> Nous ne perdons jamais : nous apprenons, nous capitalisons, puis nous améliorons.

---

## 8. Suite opérationnelle

```text
1. ✅ Production maquette V1.2 — livrée Dev
2. ✅ Recette QA — [`recette_qa_maquette_01_2.md`](./recette_qa_maquette_01_2.md)
3. ✅ Verdict MOA/QA — OK PARTIEL · arbitrage acté
4. ☐ Reprise composition home Odoo — bloc par bloc — [`arbitrage_moa_maquette_01_2.md`](./arbitrage_moa_maquette_01_2.md)
5. ☐ Recette composition CMS — [`recette_qa_composition_cms_ck_01.md`](../recette_qa_composition_cms_ck_01.md)
```

---

## 9. GO traduction Odoo (2026-06-13)

Arbitrage MOA : [`arbitrage_moa_maquette_01_2.md`](./arbitrage_moa_maquette_01_2.md)

```text
GO TRADUCTION ODOO — MAQUETTE CK V1.2
AVEC RÉSERVES MOA ACCEPTÉES
```

Périmètre : header · hero · réassurance · produits · catégories · coffret · Pro · éditorial · footer · revalidation desktop + mobile.

---

*GO OFFICIEL MOA — Move 3 · maquette CK V1.2 Boutique élégante · 2026-06-13.*
