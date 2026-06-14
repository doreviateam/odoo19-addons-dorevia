# Livraison — Maquette CK V1.2 · Boutique élégante

| Champ | Valeur |
|-------|--------|
| **GO MOA** | [`go_moa_maquette_01_2.md`](./go_moa_maquette_01_2.md) |
| **Brief** | [`brief_01_2.md`](./brief_01_2.md) |
| **Ticket Dev** | [`ticket_dev_maquette_01_2_open_design.md`](./ticket_dev_maquette_01_2_open_design.md) |
| **Date livraison Dev** | 2026-06-13 |
| **Artefact Open Design** | `/Users/doreviateam/open-design/.od/projects/ck-marketone-maquette-v1_2/index.html` |
| **Artefact repo** | [`artifact/index.html`](./artifact/index.html) |
| **Statut** | **Livré Dev · recetté QA · GO traduction Odoo** ([`arbitrage_moa_maquette_01_2.md`](./arbitrage_moa_maquette_01_2.md)) |

---

## Synthèse

Évolution **home uniquement** de la V1.1.1 vers une logique **boutique élégante** (doctrine note_05) :

| Changement V1.2 vs V1.1.1 home | Détail |
|--------------------------------|--------|
| Hero | **Raccourci** — moins de hauteur · promesse + 2 CTA |
| Réassurance | **Remontée** — immédiatement sous le hero (4 preuves) |
| Produits | **6 cartes** · prix visibles · CTA « Voir » · produits CK crédibles |
| Catégories | **Cartes actionnables** · routes `/shop/category/…` explicites |
| Coffrets | **Bloc dédié** · coffret découverte mis en avant |
| Pro | **Bandeau home** · CTA `/professionnels` |
| Éditorial | **Bas de page** — après blocs marchands |
| Footer | **CK propre** — sans placeholder Odoo |
| Périmètre | **Home seule** — pas de refonte /shop ni fiche produit dans V1.2 |

**Home Odoo non modifiée** pendant cette livraison.

---

## Prévisualisation

```bash
# Option 1 — Python
cd /Users/doreviateam/open-design/.od/projects/ck-marketone-maquette-v1_2
python3 -m http.server 8766

# Option 2 — artefact repo
cd odoo19-addons-dorevia/dorevia_ck_marketone/docs/design/maquette_01.2/artifact
python3 -m http.server 8766
```

URL : `http://127.0.0.1:8766/index.html`

**Mobile** : responsive natif CSS · tester viewport 390px · ordre DOM = hero → preuves → produits → catégories → coffrets → pro → éditorial → footer.

---

## Livrables

| # | Fichier | Statut |
|---|---------|--------|
| 1 | `index.html` (desktop + responsive mobile) | ✅ |
| 2 | `LIVRAISON_V1_2.md` | ✅ |
| 3 | [`TABLEAU_TRADUCTION_ODOO_V1_2.md`](./TABLEAU_TRADUCTION_ODOO_V1_2.md) | ✅ |

---

## Écarts / réserves à arbitrer MOA

| # | Sujet | Statut |
|---|-------|--------|
| 1 | **Univers Artisanat** | Non mis en avant — en attente arbitrage MOA (cf. brief §9.A) |
| 2 | **Routes produits** | URLs fictives plausibles (`/shop/slug-id`) — mapping catalogue BO à créer |
| 3 | **`/professionnels`** | Lien maquette · page Odoo à composer (travail parallèle autorisé) |
| 4 | **Typo Fraunces/DM Sans** | Google Fonts maquette — arbitrage prod Odoo maintenu |
| 5 | **Visuels produits** | Aplats placeholder — photos catalogue à intégrer en prod |

---

## Prochaine étape

Recette QA : [`recette_qa_maquette_01_2.md`](./recette_qa_maquette_01_2.md)

Verdict attendu :

```text
OK MAQUETTE CK V1.2 — BOUTIQUE ÉLÉGANTE
```

ou OK PARTIEL / KO — corrections à reprendre.

---

*Livraison Dev maquette CK V1.2 — Move 3 · 2026-06-13.*
