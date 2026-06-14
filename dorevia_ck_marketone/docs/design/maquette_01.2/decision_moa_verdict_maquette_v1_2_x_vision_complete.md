# Décision MOA — Verdict maquette CK V1.2.x · Vision complète matérialisée

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Statut** | **Livraison MOA** · [`LIVRAISON_MOA_MAQUETTE_CK_V1_2_X.md`](./LIVRAISON_MOA_MAQUETTE_CK_V1_2_X.md) |
| **Date** | 2026-06-13 |
| **Recette globale** | [`recette_qa_maquette_v1_2_x.md`](./recette_qa_maquette_v1_2_x.md) |
| **Cadrage** | [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](./CADRAGE_MAQUETTE_CK_V1_2_X.md) |
| **Décision pause Odoo** | [`decision_moa_pause_odoo_iteration_maquette_v1_2_x.md`](./decision_moa_pause_odoo_iteration_maquette_v1_2_x.md) |

```text
OK MAQUETTE CK V1.2.x — VISION COMPLÈTE MATÉRIALISÉE
ODOO EN PAUSE — PROCHAINE ÉTAPE = ARBITRAGE PÉRIMÈTRE V1 TRADUISIBLE
```

> Phrase de référence MOA : *La vision complète est matérialisée ; Odoo reste en pause ; la prochaine étape est l’arbitrage du périmètre V1 traduisible — pas la reprise automatique de tout le prototype.*

---

## 1. Verdict QA MOA

La MOA valide le verdict QA global :

```text
OK MAQUETTE CK V1.2.x LOT 1 + LOT 2 + LOT 3+
— vision complète matérialisée (9 pages)
```

Contrôles MOA exécutés sur le rendu réel :

| Contrôle | Résultat |
|----------|----------|
| Desktop 1280 px | OK — 9 pages sans overflow horizontal |
| Mobile 390 px | OK — 9 pages · `scrollWidth = 390` |
| Images | OK — pas d’image cassée détectée |
| Liens `.html` locaux | OK — aucun lien manquant |
| Footer | OK — colonne « Fiche producteur » cohérente |
| Parcours producteur | OK — Fiche produit → Fiche producteur → Shop / Recettes / Pro |

---

## 2. État acté des lots

| Lot | Pages | Verdict |
|-----|-------|---------|
| **Lot 1** | Accueil · Fiche produit · Professionnels | OK |
| **Lot 2** | Shop · Catégorie | OK |
| **Lot 3+** | À propos · **Fiche producteur** · Recettes · Contact | OK |

**9 pages artifact** recettées — dont `fiche-producteur.html` comme 9e page de la vision.

---

## 3. Lecture MOA — points forts

* **Fiche producteur** : bon ajout — donne du fond sans transformer CK en annuaire ou portail.
* **Équilibre vente / confiance** : producteur · origine · savoir-faire · produits · usage · achat.
* **Vision CK** : expérience commerciale + logistique + éditoriale + relation producteur.

---

## 4. Réserves acceptées (non bloquantes)

| Réserve | Arbitrage attendu |
|---------|-------------------|
| Promesses logistiques | Confirmer opérationnellement avant publication Odoo |
| Routes Odoo cibles | Mapper `/shop`, catégories, produits, `/legal` à la traduction |
| **Fiche producteur** | Trancher **page CMS producteur** vs **données fournisseur Odoo natives** |
| Visuels Unsplash | Remplacer par assets réels avant recette finale Odoo |

Aucune réserve bloquante identifiée après Lot 1.1.

---

## 5. Hors scope V1 — ne pas ouvrir

```text
Annuaire multi-producteurs
Portail producteur
Espace connecté
Page « Partenaires » générique
Blog complexe · forum · communauté
Workflow custom · automation CRM au-delà du natif
Reprise automatique de l’intégralité du prototype HTML
```

---

## 6. Décision MOA

```text
La matérialisation maquette V1.2.x est terminée et validée.
Odoo reste EN PAUSE.
Aucune traduction Odoo n’est déclenchée par ce verdict.
```

La maquette devient la **référence cible** pour arbitrer ce qui entre en V1 Odoo traduisible.

---

## 7. Clôture phase maquette

| Élément | Statut |
|---------|--------|
| 9 pages artifact HTML | ✅ |
| Recette QA globale (1280 + 390 px) | ✅ |
| Verdict MOA Lot 1 + 2 + 3+ | ✅ |
| Fiche producteur type | ✅ |
| Cadrage + décision verdict | ✅ |
| Document arbitrage V1 traduisible | ✅ — [`ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md`](./ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md) · QA MOA OK |
| Décisions M1–M9 · GO exécution | ☐ §5 — [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) · M1–M9 ✅ |
| Séquence reprise V1 | ✅ préparation — [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) |
| Reprise Odoo | ⏸ En pause — GO distinct |

```text
Phase maquette V1.2.x = close.
Document d’arbitrage V1 préparé — décisions MOA et GO Odoo restent distincts.
```

---

## 9. Prochaine étape MOA

Voir [`LIVRAISON_MOA_MAQUETTE_CK_V1_2_X.md`](./LIVRAISON_MOA_MAQUETTE_CK_V1_2_X.md) · §10.

| # | Action | Document |
|---|--------|----------|
| 1 | Acter M1–M9 | [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) |
| 2 | GO reprise Odoo §5 | même document |

---

## 10. Discours MOA (externe / interne)

```text
La vision CK V1.2.x est matérialisée sur 9 pages maquette :
promesse, catalogue, fiche produit, producteur, Pro, confiance, éditorial, contact.

Odoo reste en pause.
La prochaine étape n’est pas de tout traduire,
mais d’arbitrer le périmètre V1 prioritaire traduisible dans Odoo 19 CE.
```

---

*Décision MOA verdict maquette CK V1.2.x · vision complète · 2026-06-13.*
