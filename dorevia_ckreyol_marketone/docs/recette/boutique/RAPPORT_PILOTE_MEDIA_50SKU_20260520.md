# Rapport MOA — pilote média catalogue 50 SKU

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-20 |
| **Ticket** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) |
| **Signal amont** | [`REPONSE_MOA_GO_EXECUTION_PILOTE_MEDIA.md`](./REPONSE_MOA_GO_EXECUTION_PILOTE_MEDIA.md) |
| **Run** | `tools/ck_image_normalizer/reports/runs/pilote_20260520/` |
| **Recette** | `ck_shop_tile_v1.1` |
| **Volume** | 50 images |

---

## 1. Résultat automatique

| Statut moteur | Nombre | Taux |
|---------------|-------:|-----:|
| `OK` | 18 | 36 % |
| `OK_WITH_WARNINGS` | 3 | 6 % |
| `NEEDS_REVIEW` | 29 | 58 % |
| `REJECTED` | 0 | 0 % |

Synthèse :

```text
OK + OK_WITH_WARNINGS : 21 / 50 = 42 %
REJECTED              : 0 / 50 = 0 %
NEEDS_REVIEW          : 29 / 50 = 58 %
GO candidate auto     : non
```

---

## 2. Lecture MOA

Le pilote ne produit **aucun rejet**, ce qui est positif : le moteur ne détruit pas le lot.

En revanche, le volume `NEEDS_REVIEW` est trop élevé pour valider un flux opérateur simple :

```text
29 images à revoir humainement sur 50
```

Le résultat ne doit donc pas être interprété comme un échec technique, mais comme un signal clair :

```text
La recette fonctionne mieux sur certains types de sources que sur d’autres.
Le flux pilote nécessite une passe P4 de revue humaine avant décision.
```

---

## 3. Découpage du résultat

### Par origine du lot

| Lot | OK | OK_WITH_WARNINGS | NEEDS_REVIEW | OK + WARN |
|-----|---:|-----------------:|-------------:|----------:|
| Noyau historique 27 | 4 | 2 | 21 | 6 / 27 |
| Extension 23 | 14 | 1 | 8 | 15 / 23 |

Lecture :

- le **noyau historique 27** concentre l’essentiel de la revue humaine ;
- l’**extension 23** se comporte nettement mieux ;
- les sources de type lifestyle passent bien quand elles sont assumées comme telles.

### Par profil

| Profil | OK | OK_WITH_WARNINGS | NEEDS_REVIEW | OK + WARN |
|--------|---:|-----------------:|-------------:|----------:|
| `packshot` | 6 | 3 | 29 | 9 / 38 |
| `lifestyle` | 12 | 0 | 0 | 12 / 12 |

Lecture :

```text
Le problème principal n’est pas le lifestyle.
Le problème est le packshot plein cadre / hétérogène issu du noyau historique.
```

---

## 4. Seuils pilote

| Critère | Seuil pilote | Résultat | Verdict |
|---------|--------------|----------|---------|
| OK + OK_WITH_WARNINGS | ≥ 55 % | 42 % | KO |
| REJECTED | ≤ 15 % | 0 % | OK |
| NEEDS_REVIEW | ≤ 35 % et flux tenable | 58 % | KO |
| Reprises manuelles | À mesurer P4 | **7 M** (P4) · **7 récupérées après mini-batches** | Mesuré |
| Gain visuel grille | Revue humaine | **43/50 exploitables (86 %)** après mini-batches | OK avec réserves |

Verdict automatique (batch seul) :

```text
GO pilote exploitable auto : non
GO avec réserves : acté après P4 + mini-batches ciblés
```

→ Clôture consolidée : [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](./RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) · [`REPONSE_MOA_REINTEGRATION_2_MANIOC_SOURCES_DISTINCTES.md`](./REPONSE_MOA_REINTEGRATION_2_MANIOC_SOURCES_DISTINCTES.md)

---

## 5. Livrables générés

| Livrable | Emplacement |
|----------|-------------|
| Rapport JSON | `tools/ck_image_normalizer/reports/runs/pilote_20260520/reports/batch_20260520T120245Z.json` |
| Rapport CSV | `tools/ck_image_normalizer/reports/runs/pilote_20260520/reports/batch_20260520T120245Z.csv` |
| Previews | `tools/ck_image_normalizer/reports/runs/pilote_20260520/reports/previews/` |
| WebP | `tools/ck_image_normalizer/reports/runs/pilote_20260520/output/webp/` |
| JPEG fallback | `tools/ck_image_normalizer/reports/runs/pilote_20260520/output/jpeg/` |
| Suivi opérateur | `tools/ck_image_normalizer/reports/runs/pilote_20260520/pilote_operateur.csv` |
| Planche `NEEDS_REVIEW` | `tools/ck_image_normalizer/reports/runs/pilote_20260520/reports/contact_sheet_needs_review.jpg` |
| Planche `OK + WARN` | `tools/ck_image_normalizer/reports/runs/pilote_20260520/reports/contact_sheet_ok_warn.jpg` |
| Mini-batch lot M corrigé | `tools/ck_image_normalizer/reports/runs/pilote_20260520_lot_m_corrige/` |
| Mini-batch sources manioc distinctes | `tools/ck_image_normalizer/reports/runs/pilote_20260520_lot_manioc_sources/` |
| Arbitrage lot X | `tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_x_arbitrage_moa.csv` |

---

## 6. Décision MOA

P4, mini-batch lot M et mini-batch sources manioc clôturés (2026-05-20).

```text
GO pilote avec réserves — 43 / 50 exploitables (86 %) — lot X maintenu en demande fournisseur / exclusion temporaire — recette ck_shop_tile_v1.1 conservée comme candidate — CLI exploitable sous contrôle opérateur — aucune intégration Odoo autorisée sans ticket séparé.
```

→ [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](./RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) · [`RAPPORT_P4_PILOTE_MEDIA_50SKU_20260520.md`](./RAPPORT_P4_PILOTE_MEDIA_50SKU_20260520.md) · [`REPONSE_MOA_REINTEGRATION_2_MANIOC_SOURCES_DISTINCTES.md`](./REPONSE_MOA_REINTEGRATION_2_MANIOC_SOURCES_DISTINCTES.md)

---

## 7. Signal actuel

```text
Pilote média consolidé — GO avec réserves MOA — 43 / 50 exploitables (86 %) — lot X (7) maintenu en demande fournisseur / exclusion temporaire — pas de code Odoo.
```
