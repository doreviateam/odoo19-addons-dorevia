# TICKET — CK Image Normalizer — Pilote média catalogue (cadrage post-POC)

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA` |
| **Univers** | **Boutique** — qualité média catalogue `/shop` |
| **Type** | **Cadrage + pilote CLI externe** — hors module Odoo |
| **Statut** | **Clôturé MOA** (2026-05-20) · **GO pilote avec réserves confirmé** · **43/50 (86 %)** · lot X hors flux |
| **Ticket amont** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md) — **clôturé GO avec réserves** |
| **Outil** | `tools/ck_image_normalizer/` |
| **Recette candidate** | `ck_shop_tile_v1.1` |
| **Module Odoo** | **Aucun changement** dans `dorevia_ckreyol_marketone` |
| **ADR** | **ADR-033** (suite post-POC) |
| **Effort indicatif** | **1–2 j/h cadrage** (ce ticket) · **2–4 j/h exécution pilote** · **4–8 h MOA opérateur** (estimation) |

---

## Contexte — état acté MOA

```text
POC CLI externe clôturé
Verdict : GO POC avec réserves
Recette candidate : ck_shop_tile_v1.1
Lot officiel POC : 21 références
Aucun code Odoo touché
Aucune industrialisation lancée
```

Le POC a prouvé la **valeur du moteur** sur un lot contrôlé. Il ne déclenche **pas** une intégration Odoo ni un traitement massif catalogue.

**Décision MOA (2026-05-20)** :

```text
GO pilote média catalogue — volume initial 50 SKU
Recette : ck_shop_tile_v1.1
Périmètre : tuiles commerce /shop uniquement
Aucun code Odoo · Aucun remplacement image_1920 · Aucune industrialisation automatique
```

→ [`REPONSE_MOA_GO_PILOTE_MEDIA.md`](../../recette/boutique/REPONSE_MOA_GO_PILOTE_MEDIA.md) · [`REPONSE_MOA_GO_EXECUTION_PILOTE_MEDIA.md`](../../recette/boutique/REPONSE_MOA_GO_EXECUTION_PILOTE_MEDIA.md) · [`RAPPORT_PILOTE_MEDIA_50SKU_20260520.md`](../../recette/boutique/RAPPORT_PILOTE_MEDIA_50SKU_20260520.md)

**Résultat batch pilote (2026-05-20)** :

```text
OK 18 · OK_WITH_WARNINGS 3 · NEEDS_REVIEW 29 · REJECTED 0
```

**P4 complété (2026-05-20)** — E:3 · R:12 · M:7 · X:7 · **36/50 exploitable (72 %)** · ~0,88 min/revue

**Verdict final MOA (2026-05-20)** :

```text
Pilote média clôturé — GO avec réserves confirmé — 43/50 exploitables (86 %) — recette ck_shop_tile_v1.1 conservée — lot X 7/50 exclusion temporaire — pas de GO exploitation automatique — P6 V1.5 en attente signal MOA
```

→ [`REPONSE_MOA_CLOTURE_PILOTE_MEDIA_CATALOGUE.md`](../../recette/boutique/REPONSE_MOA_CLOTURE_PILOTE_MEDIA_CATALOGUE.md)

**Progression pilote** :

```text
Batch seul : 21/50 (42 %) → P4 : 36/50 (72 %) → lot M : 41/50 (82 %) → manioc : 43/50 (86 %)
```

**Verdict intermédiaire P4/P5** :

→ [`RAPPORT_P4_PILOTE_MEDIA_50SKU_20260520.md`](../../recette/boutique/RAPPORT_P4_PILOTE_MEDIA_50SKU_20260520.md) · [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](../../recette/boutique/RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) — **P5 clôturé**

---

## Objectif

Passer de :

> une recette candidate validée en POC (21 refs)

à :

> un **flux média catalogue exploitable** pour C-Kreyol / Marketone

…de manière **prudente**, **mesurée** et **sans brûler les étapes**.

Ce ticket **cadre** le pilote et définit les règles opérateur. Il **n’autorise pas** le code Odoo ni l’industrialisation automatique.

---

## Hors périmètre (interdit)

| Élément | Statut |
|---------|--------|
| Implémentation Odoo (V1.5) | ❌ Ticket séparé · **après** pilote |
| Champ `image_shop_tile` / QWeb / cron | ❌ Cadrage futur uniquement |
| Remplacement `product.template.image_1920` | ❌ Interdit |
| Traitement massif catalogue complet | ❌ Sans nouveau GO MOA explicite |
| Hero, fiche, culture, blog | ❌ Hors périmètre |
| IA / segmentation / `rembg` | ❌ Interdit |
| Recette `v1.2` sans arbitrage MOA | ❌ Pilote d’abord sur v1.1 |

---

## Décisions MOA retenues (héritées POC)

| # | Décision |
|---|----------|
| **D1** | Recette candidate **`ck_shop_tile_v1.1`** |
| **D2** | Fond **`#F8EEDB` baked-in** accepté |
| **D3** | **`NEEDS_REVIEW`** = sas opérateur obligatoire |
| **D4** | **`OK`** / **`OK_WITH_WARNINGS`** utilisables après contrôle |
| **D5** | **`REJECTED`** = non utilisable sans reprise source |
| **D6** | Périmètre strict : **tuiles commerce `/shop` uniquement** |
| **D7** | Originaux conservés · pas de remplacement `image_1920` |
| **D8** | Pas de traitement massif · pas d’industrialisation auto sans GO MOA post-pilote |
| **D9** | **GO pilote média** — 50 SKU · extension catalogue +23 |
| **D10** | **GO pilote avec réserves** (P4) — 72 % exploitable · sas `NEEDS_REVIEW` indispensable · pas d’exploitation auto |
| **D11** | **P5 clôturé** (2026-05-20) — CLI exploitable sous contrôle opérateur · lots M/X formalisés · **aucune intégration Odoo** sans ticket V1.5 |
| **D12** | **Bilan définitif pilote** — **43 / 50 (86 %)** exploitable · 7 / 50 hors flux (lot X) · 0 REJECTED · recette v1.1 conservée |
| **D13** | **Règle catalogue** — un SKU = une source distincte · pas de duplication · `REGLE_CATALOGUE_IMAGES_SOURCE.md` |
| **D14** | **Clôture définitive pilote MOA** (2026-05-20) — GO avec réserves confirmé · **43/50 (86 %)** · pas d’exploitation auto · P6 V1.5 **sur signal MOA explicite uniquement** |

---

## 1. Périmètre proposé du pilote

### 1.1 Volume SKU

| Option | SKU | Décision MOA |
|--------|-----|--------------|
| **Lot initial** | **50** | **Retenu** — mesure prudente temps opérateur + taux statuts |
| Extension | **75** | Si préparation fluide · second lot ou extension même pilote |
| Plafond ticket | **100** | Hors scope immédiat |

**Volume actif** : **50 SKU**.

### 1.2 Composition du lot (cible indicative)

| Catégorie | Part cible | Objectif |
|-----------|------------|----------|
| Packshots fond clair (fournisseur) | **40–50 %** | ROI principal — replace bg |
| Packshots hétérogènes / mal cadrés | **15–20 %** | Robustesse trim / padding |
| Sachets, bocaux, bouteilles | **15 %** | Formes variées |
| Lifestyle simples | **10–15 %** | Profil conservateur |
| Cas difficiles connus (plein cadre, artefacts) | **5–10 %** | Taux `NEEDS_REVIEW` réaliste |

**Équilibre packshot / lifestyle proposé** : **~70 % packshot · ~30 % lifestyle** (à ajuster selon catalogue réel).

### 1.3 Règles de sélection MOA

| Règle | Détail |
|-------|--------|
| **Inclure** | Produits **vendables** et **publiés sur le site** (ou candidats publication proche) |
| **Prioriser** | Familles visuellement hétérogènes aujourd’hui sur `/shop` |
| **Inclure volontairement** | 5–10 refs « difficiles » (plein cadre, fond complexe, exports fournisseur bruts) |
| **Exclure** | Produits sans image utilisable · doublons visuels · hors univers boutique |
| **Exclure** | Images déjà retouchées « finales » sans intérêt de test |
| **Source** | Fichiers **master** fournisseur ou export BO **`image_1920`** (copie locale — **pas** de modification BO pour le pilote) |

### 1.4 Exclusions explicites

- Kits / packs sans visuel unitaire clair (sauf cas MOA volontaire)
- Visuels hero homepage non utilisés en tuile `/shop`
- Banque recette `marketplace/docs/assets` déjà couverte par le POC (sauf 2 reprises manuelles signalées)

---

## 2. Flux opérateur

### 2.1 Par statut moteur

| Statut | Action opérateur | Publication tuile dérivée |
|--------|------------------|----------------------------|
| **`OK`** | Contrôle rapide preview (G1, G4, G6) | Utilisable si OK visuel |
| **`OK_WITH_WARNINGS`** | Vérification ciblée · noter la réserve | Utilisable avec réserve documentée |
| **`NEEDS_REVIEW`** | **Revue humaine obligatoire** G1–G6 · décision E/R/M/X | Uniquement après décision explicite |
| **`REJECTED`** | Reprise source fournisseur **ou** exclusion | **Non** utilisable tel quel |

### 2.2 Décisions humaines sur `NEEDS_REVIEW`

| Code | Signification | Suite |
|------|---------------|-------|
| **E** | Exploitable | Retenir tuile normalisée |
| **R** | Acceptable avec réserve | Retenir · tracer la réserve |
| **M** | Reprise manuelle | Retoucher source · relancer CLI sur le fichier |
| **X** | Exclure | Demander nouvelle source fournisseur |

### 2.3 Suivi opérateur (à produire pendant le pilote)

| Métrique | Objectif mesure |
|----------|-----------------|
| Temps moyen / image | Par statut (OK vs NEEDS_REVIEW vs REJECTED) |
| Temps total lot | Budget opérationnel catalogue |
| Taux reprise manuelle | Acceptabilité flux |
| Taux demande fournisseur | Qualité amont à renforcer |

**Outil de suivi proposé** : colonnes additionnelles dans manifest / feuille `pilote_operateur.csv` (temps_min, decision_moa, action, notes).

### 2.4 Reprises connues POC (rappel)

| Fichier POC | Action attendue pilote |
|-------------|---------------------|
| `homepage_manioc_pates_mayotte_la_platine.png` | Reprise manuelle · **ne pas** valider auto |
| `stitch_guava_jam_jar.png` | Reprise manuelle recommandée |

Si ces SKU figurent dans le lot pilote : traiter comme **cas témoin reprise**, pas comme baseline automatique.

---

## 3. Livrables pilote

| # | Livrable | Responsable | Critère d’acceptation |
|---|----------|-------------|----------------------|
| **L1** | Liste SKU pilote + `manifest.pilote.csv` | MOA + Dev | 50–100 lignes · profils renseignés · SKU identifiés |
| **L2** | Batch CLI `ck_shop_tile_v1.1` | Dev | Rapport JSON/CSV · run horodaté dans `reports/runs/pilote_*/` |
| **L3** | Previews avant/après | Dev | `reports/previews/` |
| **L4** | Grille comparative HTML | Dev | Desktop 4 col. + mobile 2 col. |
| **L5** | Synthèse statuts | Dev | OK / WARN / REVIEW / REJECTED · taux · comparaison POC |
| **L6** | Liste reprises manuelles | MOA | Fichiers `M` · effort estimé |
| **L7** | Liste demandes fournisseur | MOA | Fichiers `X` ou `REJECTED` · brief qualité |
| **L8** | Feuille suivi opérateur | MOA | Temps · décisions · réserves |
| **L9** | Rapport décision pilote | Dev + MOA | GO / GO réserves / NO GO / v1.2 ? / V1.5 ? |

### Commande batch (inchangée POC)

```bash
cd tools/ck_image_normalizer
source .venv/bin/activate
python -m ck_image_normalizer run \
  --input input/pilote \
  --manifest manifest.pilote.csv \
  --recipe recipes/ck_shop_tile_v1.1.yaml \
  --output-dir reports/runs/pilote_YYYYMMDD
```

---

## 4. Critères GO / NO-GO pilote

### 4.1 GO pilote média si

| Critère | Seuil proposé (à valider MOA) |
|---------|-------------------------------|
| `OK` + `OK_WITH_WARNINGS` | ≥ **55 %** du lot pilote |
| `REJECTED` | ≤ **15 %** |
| `NEEDS_REVIEW` | ≤ **35 %** **et** flux opérateur tenable |
| Temps opérateur moyen | ≤ **3 min/image** sur `NEEDS_REVIEW` (hypothèse — à mesurer) |
| Gain visuel grille | MOA valide net vs sources actuelles `/shop` |
| Reprises manuelles | ≤ **20 %** du lot · effort acceptable |

### 4.2 GO avec réserves si

- Gain visuel net mais taux `NEEDS_REVIEW` élevé (**20–35 %**) ;
- Reprises manuelles localisées et prévisibles ;
- Recette v1.1 suffisante · pas de `v1.2` urgente ;
- Charte qualité source amont à renforcer (process, pas algo).

### 4.3 NO-GO / pause si

- `REJECTED` > **20 %** sur packshots fond clair ;
- Temps opérateur prohibitive (> **5 min/image** en médiane sur REVIEW) ;
- Dégradation texture systématique ;
- MOA rejette le fond baked-in sur volume réel *(peu probable — validé POC)* ;
- Sources catalogue trop hétérogènes sans budget reprise photo.

### 4.4 Questions de décision post-pilote

Le pilote doit permettre de trancher :

| Question | Sortie attendue |
|----------|-----------------|
| Moteur utile à l’échelle catalogue ? | Oui / Oui avec réserves / Non |
| Taux `NEEDS_REVIEW` opérable ? | Oui / Non · seuil acceptable |
| Reprises manuelles acceptables ? | Oui / Non · volume max |
| `ck_shop_tile_v1.1` suffit ? | Oui / Non → `v1.2` |
| V1.5 Odoo lite mérite cadrage ? | Oui / Non / Plus tard |

---

## 5. V1.5 Odoo lite — articulation (cadrage seulement)

**Ne pas implémenter** dans ce ticket.

Hypothèses futures à cadrer **après** synthèse pilote :

| Hypothèse | Principe |
|-----------|----------|
| Champ dédié | `image_shop_tile` (ou équivalent) |
| Fallback | Image standard si tuile absente |
| Usage | Tuile `/shop` uniquement |
| Master | `image_1920` conservé |
| BO | Minimal — pas de studio complet |
| Batch | Pas de cron massif sans GO MOA |
| Écriture | Pas de remplacement automatique de l’original |

**Ticket futur proposé** : `TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_CADRAGE.md` — ouvert **uniquement** si pilote → GO ou GO avec réserves.

**Séquence figée** :

```text
POC (clôturé) → Pilote média (ce ticket) → Décision produit → Cadrage V1.5 → Implémentation V1.5 (ticket séparé)
```

---

## 6. Risques

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Lot pilote trop « facile » | Sous-estime `NEEDS_REVIEW` réel | Règles sélection MOA · cas difficiles volontaires |
| Lot pilote trop dur | NO-GO injustifié | Équilibre 70/30 packshot/lifestyle · plafond 100 SKU |
| Temps opérateur sous-estimé | Coût caché catalogue | Feuille suivi L8 · mesure avant V1.5 |
| Tentation branchement Odoo | Scope creep | Garde-fous ticket · 0 ligne module |
| Sources fournisseur faibles | Taux REJECTED élevé | Liste demandes L7 · charte amont |
| Confusion POC / pilote | Rejouer 21 refs inutilement | Exclure banque POC sauf reprises ciblées |

---

## 7. Plan d’exécution

| Phase | Action | Responsable | Statut |
|-------|--------|-------------|--------|
| **P0** | Validation cadrage pilote | MOA | ✅ **Validé MOA** (2026-05-20) |
| **P0-dev** | Préparation structure pilote | Dev | ✅ **Livré** (2026-05-20) |
| **P1** | Sélection **50 SKU** + export images | MOA | ✅ **Livré** (2026-05-20) |
| **P2** | `manifest.pilote.csv` + `input/pilote/` | MOA | ✅ **Livré** — 50/50 · 38 packshot · 12 lifestyle |
| **P3** | Exécution batch v1.1 | Dev/MOA | ✅ **Livré** — run `pilote_20260520` |
| **P4** | Revue **29 NEEDS_REVIEW** (E/R/M/X) + temps opérateur | MOA | ✅ **Clôturé** (2026-05-20) · [`RAPPORT_P4`](../../recette/boutique/RAPPORT_P4_PILOTE_MEDIA_50SKU_20260520.md) |
| **P5** | Rapport décision pilote + synthèse GO réserves | Dev + MOA | ✅ **Clôturé** (2026-05-20) · [`RECETTE_MANUELLE_PILOTE`](../../recette/boutique/RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) |
| **P6** | Cadrage V1.5 Odoo lite | MOA + Dev | ✅ **Validé MOA** (2026-05-20) |
| **P7** | Implémentation V1.5 lite | Dev | 🔄 **Ouvert** · [`TICKET_V1_5_IMPLEMENTATION`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md) |

**Estimation** :

| Phase | Effort |
|-------|--------|
| P0 cadrage | **1–2 j/h Dev** (ce document) |
| P1–P2 préparation lot | **2–4 h MOA** + **0.5 j/h Dev** |
| P3 exécution technique | **1–2 j/h Dev** |
| P4 revue opérateur | **4–8 h MOA** (selon volume) |
| P5 synthèse | **0.5–1 j/h Dev** + **2 h MOA** |

---

### Livrables préparation Dev (P0-dev) — ✅

| Livrable | Chemin |
|----------|--------|
| Dossier pilote | `tools/ck_image_normalizer/input/pilote/` |
| Procédure MOA | `tools/ck_image_normalizer/input/pilote/README.md` |
| Template manifest | `tools/ck_image_normalizer/manifest.pilote.template.csv` |
| Template suivi opérateur | `tools/ck_image_normalizer/pilote_operateur.template.csv` |

---

### Livrables run pilote (P3) — ✅

| Livrable | Chemin |
|----------|--------|
| Run | `tools/ck_image_normalizer/reports/runs/pilote_20260520/` |
| Rapport CSV | `…/reports/batch_20260520T120245Z.csv` |
| Suivi opérateur P4 | `…/pilote_operateur.csv` |
| Planches revue | `…/reports/contact_sheet_needs_review.jpg` · `contact_sheet_ok_warn.jpg` |
| Rapport MOA | [`RAPPORT_PILOTE_MEDIA_50SKU_20260520.md`](../../recette/boutique/RAPPORT_PILOTE_MEDIA_50SKU_20260520.md) |

---

## 8. Suite post-pilote

| Qui | Action | Statut |
|-----|--------|--------|
| **MOA** | Contrôle visuel 5 previews OK lot M | ✅ Validé (2026-05-20) |
| **MOA + Dev** | Mini-batch 2 manioc sources distinctes | ✅ Clôturé (2026-05-20) |
| **MOA** | Lot **X** (7) — demande fournisseur / exclusion | ✅ Arbitré — hors flux pilote |
| **MOA** | Fournir sources lot **X** (7) — charte fournisseur | ☐ En attente (hors périmètre pilote) |
| **MOA / Dev** | Ticket **P6 — cadrage V1.5 Odoo lite** | ✅ **Cadrage livré** · [`TICKET_V1_5_CADRAGE`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_CADRAGE.md) |
| **MOA** | Valider cadrage P6 | ✅ Validé (2026-05-20) |
| **Dev** | Ticket **P7 implémentation V1.5 lite** | 🔄 **Ouvert** · [`TICKET_V1_5_IMPLEMENTATION`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md) |

**Verdict final acté** :

```text
Pilote média CK Image Normalizer clôturé — GO avec réserves confirmé — 43/50 exploitables — P6 cadrage V1.5 livré — P7 implémentation en attente validation MOA P6.
```

→ [`REPONSE_MOA_CLOTURE_PILOTE_MEDIA_CATALOGUE.md`](../../recette/boutique/REPONSE_MOA_CLOTURE_PILOTE_MEDIA_CATALOGUE.md)

**Garde-fou Dev** : aucune action technique sans signal MOA explicite.

---

## Références

| Document | Rôle |
|----------|------|
| [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md) | POC clôturé |
| [`REPONSE_MOA_GO_EXECUTION_PILOTE_MEDIA.md`](../../recette/boutique/REPONSE_MOA_GO_EXECUTION_PILOTE_MEDIA.md) | GO exécution · 50 SKU |
| [`REPONSE_MOA_CLOTURE_PILOTE_MEDIA_CATALOGUE.md`](../../recette/boutique/REPONSE_MOA_CLOTURE_PILOTE_MEDIA_CATALOGUE.md) | **Clôture définitive MOA** — GO confirmé · 43/50 |
| [`RAPPORT_P4_PILOTE_MEDIA_50SKU_20260520.md`](../../recette/boutique/RAPPORT_P4_PILOTE_MEDIA_50SKU_20260520.md) | P4 revue opérateur |
| [`RAPPORT_PILOTE_MEDIA_50SKU_20260520.md`](../../recette/boutique/RAPPORT_PILOTE_MEDIA_50SKU_20260520.md) | Résultat batch automatique |
| `…/lot_m_reprise_manuelle.csv` · `…/lot_x_demande_fournisseur.csv` | Lots opérationnels post-P5 |
| [`RAPPORT_P4_LOTS_M_X_QUALITE_SOURCE.md`](../../recette/boutique/RAPPORT_P4_LOTS_M_X_QUALITE_SOURCE.md) | Préparation lots M/X · qualité source |
| [`RAPPORT_MINI_BATCH_LOT_M_CORRIGE_20260520.md`](../../recette/boutique/RAPPORT_MINI_BATCH_LOT_M_CORRIGE_20260520.md) | Mini-batch lot M — 5 OK · 2 REJECTED |
| [`MAPPING_CATALOGUE_EXTENSION_23_PRODUITS.md`](../../cadrage/MAPPING_CATALOGUE_EXTENSION_23_PRODUITS.md) | Extension catalogue 27→50 |
| [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_POC.md`](../../recette/boutique/RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_POC.md) | Flux opérateur POC |
| [`NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md`](../../cadrage/NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md) | Cadrage initial |
| [`cadrage/DECISIONS.md`](../../cadrage/DECISIONS.md) — ADR-033 | Arbitrages MOA |
| [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_CADRAGE.md`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_CADRAGE.md) | P6 cadrage — **validé MOA** |
| [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md) | **P7 implémentation** — ouvert |
| [`tools/ck_image_normalizer/README.md`](../../../../tools/ck_image_normalizer/README.md) | CLI opérateur |

---

## Historique

| Date | Auteur | Action |
|------|--------|--------|
| 2026-05-20 | MOA | **P6 validé · GO P7** · [`TICKET_V1_5_IMPLEMENTATION`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md) |
| 2026-05-20 | MOA | **GO réintégration lot M** — 5 images validées · bilan **41/50 (82 %)** · [`REPONSE_MOA_LOT_M`](../../recette/boutique/REPONSE_MOA_REINTEGRATION_5_LOT_M_CORRIGE.md) · [`REGLE_CATALOGUE`](../../cadrage/REGLE_CATALOGUE_IMAGES_SOURCE.md) |
| 2026-05-20 | MOA | **Lot X arbitré** — exclusion temporaire flux image · `lot_x_arbitrage_moa.csv` |
| 2026-05-20 | Dev | **Mini-batch lot M** — 5 OK · 2 REJECTED manioc · [`RAPPORT_MINI_BATCH`](../../recette/boutique/RAPPORT_MINI_BATCH_LOT_M_CORRIGE_20260520.md) |
| 2026-05-20 | MOA | **Lots M/X préparés** — [`RAPPORT_P4_LOTS_M_X`](../../recette/boutique/RAPPORT_P4_LOTS_M_X_QUALITE_SOURCE.md) |
| 2026-05-20 | Dev | **P5 clôturé** — [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](../../recette/boutique/RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) |
| 2026-05-20 | MOA | **P4 clôturé** — GO pilote avec réserves · 72 % exploitable |
| 2026-05-20 | MOA | **GO exécution** · batch 50 · run `pilote_20260520` |
