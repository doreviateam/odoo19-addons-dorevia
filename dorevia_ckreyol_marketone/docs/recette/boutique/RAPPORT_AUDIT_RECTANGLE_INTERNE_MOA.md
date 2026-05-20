# Audit MOA — effet rectangle interne / image dans l'image

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-20 |
| **Périmètre** | 43 tuiles `image_shop_tile` pilote |
| **Référence OK MOA** | **Colombo des Antilles** — image pleine lifestyle bord à bord (référence tuile /shop MOA 2026-05-20) |
| **Exemple NON OK MOA** | Colombo en v1.1 normalisé — rectangle interne, marges baked-in visibles |
| **Source audit** | `AUDIT_P8_5_VISUAL_OCCUPANCY.csv` + revue visuelle MOA |

---

## Doctrine visuelle retenue

| Type | Comportement attendu |
|------|---------------------|
| **Lifestyle** | image pleine, bord à bord dans la zone photo |
| **Packshot alpha** | produit détouré sur fond conteneur, sans carré interne |
| **Packshot / pseudo-lifestyle v1.1** | aucun effet de rectangle interne |
| **Fond conteneur** | proche du blanc, discret |
| **Interdit** | visuel flottant au centre d'une zone plus grande |

**Référence comportementale** : Confiture ananas vanille (`product_id=182`, hors flux pilote 43 — comportement visuel cible).

---

## Synthèse

| Catégorie | Nb | Action Dev proposée |
|-----------|---:|---------------------|
| **A — NON OK confirmé (rectangle interne)** | **8** | gouvernance source / fallback / retrait dérivé |
| **B — Surveillance post-Lot A (alpha)** | **3** | maintien avec réserve — revue visuelle |
| **C — OK comportement cible** | **32** | aucune action |

> Note : l'audit automatique `bbox_area_ratio` seul **sous-estime** certains cas (ex. Colombo : métrique OK mais rendu MOA NON OK). La revue visuelle prime.

---

## A — NON OK confirmé — effet rectangle interne

### A1 · Lot B déjà identifié (5) — `NEEDS_REVIEW_SOURCE` en base

| Produit | ID | Recette | bbox | Proposition Dev |
|---------|---:|---------|-----:|-----------------|
| Biscuits banane confiture | 471 | v1.1 | 0.29 | **Recadrage source** — priorité haute ; fallback `image_1920` si gênant en grille |
| Biscuits coco vanille | 156 | v1.1 | 0.33 | **Recadrage source** — priorité haute ; fallback temporaire recommandé |
| Pâtes de manioc Mayotte | 9 | v1.1 | 0.34 | **Recadrage source** — maintien v1.1 + statut actuel |
| Coffret biscuits et douceurs | 188 | v1.1 | 0.35 | **Recadrage source** — maintien v1.1 + statut actuel |
| Semoule manioc fine Mayotte | 184 | v1.1 | 0.42 | **Recadrage source** — maintien v1.1 + statut actuel |

### A2 · Pseudo-packshot v1.1 — nouveau signal MOA (3)

| Produit | ID | Recette | bbox | Problème | Proposition Dev |
|---------|---:|---------|-----:|----------|-----------------|
| **Colombo des Antilles** | **154** | v1.1 | 0.61* | Pochette posée, marges baked-in visibles, effet carré interne | **Retrait temporaire `image_shop_tile`** + **recadrage source** ; fallback `image_1920` en attendant |
| Pochette curry des Antilles | 469 | v1.1 | 0.61* | Même profil source que Colombo (pochette fond clair) | **Recadrage source** ; fallback `image_1920` si rendu identique à Colombo |
| Palets manioc croustillants La Platine | 178 | v1.1 | 0.59* | Sachet sur fond clair, risque rectangle interne | **Maintien avec réserve** ; recadrage source si confirmé visuellement |

\* bbox élevé mais rendu visuel NON OK — limite de la métrique automatique.

---

## B — Surveillance alpha post-Lot A (3)

Lot A exécuté (`content_fill_ratio=0.84`). Revue visuelle recommandée :

| Produit | ID | Recette | bbox post-Lot A | Proposition Dev |
|---------|---:|---------|----------------:|-----------------|
| Maniocookies salés La Platine | 7 | v1.2-alpha | ~0.32 | **Maintien avec réserve** — OK si présence suffisante post-Lot A |
| Mix beignets manioc | 163 | v1.2-alpha | ~0.32 | **Maintien avec réserve** — idem |
| Palettes coco vanille | 472 | v1.2-alpha | ~0.32 | **Maintien avec réserve** — idem |

Si la présence reste faible : re-export alpha ciblé (`fill=0.88`) **ou** fallback v1.1 — pas de bascule alpha sur lifestyle.

---

## C — OK comportement cible (32)

Comportement aligné référence Confiture ananas vanille (image pleine, zone photo unique).

Exemples représentatifs :

| Produit | ID | Recette | bbox |
|---------|---:|---------|-----:|
| Confiture papaye muscovado | 478 | v1.1 | 0.52 |
| Confiture goyave rose | 468 | v1.1 | 0.61 |
| Confiture fruits de la passion | 185 | v1.1 | 0.61 |
| Confiture banane flambée | 153 | v1.1 | 0.61 |
| Crackers manioc Sainte-Anne | 8 | v1.2-alpha | 0.53 |
| Chips banane plantain salées | 183 | v1.2-alpha | 0.53 |
| … | … | … | … |

*(liste complète : produits `recommendation=OK` dans `AUDIT_P8_5_VISUAL_OCCUPANCY.csv`, hors A2 si confirmés visuellement)*

---

## Plan d'action proposé (sans refonte)

| Priorité | Action | Produits | Garde-fous |
|----------|--------|----------|------------|
| **P1** | Retrait temporaire `image_shop_tile` | Colombo (154) | fallback `image_1920` immédiat ; flag inchangé |
| **P2** | Fallback `image_1920` temporaire | Biscuits coco (156), Biscuits banane (471) | cas les plus gênants visuellement |
| **P3** | Gouvernance source documentée | Lot B (5) + Colombo + Pochette curry | pas d'alpha forcé ; pas de retraitement massif |
| **P4** | Revue visuelle post-Lot A | 3 packshots alpha | ajustement fill ciblé si MOA le valide |

---

## Garde-fous maintenus

- `image_1920` inchangé
- pas d'alpha sur lifestyle
- pas de détourage IA / rembg
- pas de cron / pas de traitement massif
- rollback via `marketone.shop_tile_enabled`

---

## Décision MOA (2026-05-20)

- **GO P1** — retrait `image_shop_tile` Colombo (154)
- **GO P2** — fallback temporaire Biscuits coco (156) + Biscuits banane (471)
- Autres cas : gouvernance source, pas d'action immédiate
- Packshots alpha Lot A : maintien avec réserve

**Exécution Dev** : `RAPPORT_P1_P2_FALLBACK_RECTANGLE_EXECUTION.md`

**Signal Dev** :

```text
P1 + P2 exécutés — Colombo + Biscuits coco + Biscuits banane en fallback image_1920 — 40 tuiles dérivées restantes — garde-fous maintenus.
```
