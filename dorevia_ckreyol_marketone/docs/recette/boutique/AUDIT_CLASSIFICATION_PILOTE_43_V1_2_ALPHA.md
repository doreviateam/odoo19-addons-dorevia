# Audit classification packshot / lifestyle / NEEDS_REVIEW — pilote 43 — V1.2-alpha

| Champ | Valeur |
|-------|--------|
| **Phase** | P8-1 — pré-audit Dev · à valider MOA |
| **Date** | 2026-05-20 |
| **Outil** | `tools/ck_image_normalizer/audit_classification_v12_alpha.py` |
| **Sources scannées** | 43 / 43 (lot pilote MOA validé) · 0 manquante |
| **Méthode** | Exécution flood-fill alpha v1.2 + mesure ratio opaque + indicateurs périphériques |
| **CSV résultat** | `AUDIT_CLASSIFICATION_PILOTE_43_V1_2_ALPHA.csv` |
| **Décision** | Aucune décision auto-appliquée — proposition à valider MOA |

---

## Méthode

Chaque source PNG est passée dans la pipeline alpha v1.2 (flood-fill depuis les 4 coins) puis on mesure :

| Indicateur | Définition | Signification |
|------------|------------|---------------|
| **opaque_ratio** | % de pixels avec alpha ≥ 32 après détourage | Cible packshot fond uni : **25–50 %** · lifestyle : > 65 % |
| **corner_luminance** | Luminance moyenne 4 coins source | Clair : ≥ 200 · sombre/complexe : < 180 |
| **periphery_entropy** | Variance normalisée des 4 patchs périphériques | Uniforme : ≤ 0.22 · complexe : > 0.30 |
| **corner_uniformity** | Distance couleur max entre les 4 coins | Indicatif, non bloquant |

### Règles de classification proposées (Dev)

```text
packshot_alpha  → opaque 0.20–0.55  ET  luminance ≥ 200  ET  entropie ≤ 0.22
lifestyle       → opaque > 0.65     OU  luminance < 180  OU  entropie > 0.30
needs_review    → autres cas intermédiaires
```

---

## Résultat synthétique

| Classe | Nombre | % | Action V1.5 / V1.2-alpha |
|--------|--------|---|--------------------------|
| **packshot_alpha** | **6** | 14 % | Candidat re-export v1.2-alpha · arbitrage MOA confirmation |
| **lifestyle** | 34 | 79 % | Conserver v1.1 (rendu actuel acceptable) |
| **needs_review** | 3 | 7 % | Arbitrage MOA · v1.1 par défaut si non tranché |

**Catalogue effectivement éligible alpha** : 6/43 (≈ 14 %) automatiquement + jusqu'à 3 supplémentaires si MOA bascule les NEEDS_REVIEW.

---

## Détail — packshots éligibles alpha (6) — proposition Dev

| ID | Produit | opaque | luminance | entropie |
|----|---------|--------|-----------|----------|
| **7** | Maniocookies salés La Platine | 25 % | 255 | 0.00 |
| **155** | Shrub agrumes créole | 26 % | 250 | 0.00 |
| **163** | Mix beignets manioc | 25 % | 255 | 0.00 |
| **187** | Marinade jerk authentique | 26 % | 250 | 0.00 |
| **CK-MO-031** | Marinade jerk citron vert | 26 % | 250 | 0.00 |
| **CK-MO-033** | Palettes coco vanille | 25 % | 255 | 0.00 |

Profil typique : fond blanc / quasi-blanc uniforme, produit central net, opaque ~25 % cohérent avec un packshot studio.

---

## Détail — NEEDS_REVIEW (3) — arbitrage MOA

| ID | Produit | opaque | luminance | Note |
|----|---------|--------|-----------|------|
| **8** | Crackers manioc Sainte-Anne | 61 % | ≥ 200 | Sachet transparent → opaque artificiellement élevé ; le POC précédent (§ RAPPORT_POC) a démontré **rendu alpha EXCELLENT** — basculement `packshot_alpha` recommandé MOA |
| **183** | Chips banane plantain salées | 61 % | ≥ 200 | Profil identique sachet transparent — à vérifier visuellement |
| **CK-MO-034** | Chips patate douce créole | 61 % | ≥ 200 | Profil identique — à vérifier visuellement |

**Recommandation Dev** : ces 3 produits ont probablement un sachet plastique transparent qui gonfle le ratio opaque. Le détourage alpha sera propre — basculement vers `packshot_alpha` proposé sous réserve revue MOA visuelle.

Si MOA valide ces 3 reclassifications : **9/43 packshots alpha** (21 % du pilote).

---

## Détail — lifestyle (34) — conservés v1.1

Liste complète dans le CSV `AUDIT_CLASSIFICATION_PILOTE_43_V1_2_ALPHA.csv`.

Profils typiques détectés :

- Scènes cuisine ensoleillées (Confiture banane, Colombo, Bouillon)
- Plans de travail noir/bois (Pâtes manioc, Sauce piment, Jus goyave)
- Compositions épices/condiments (Mélange épices, Tapenade, Rougail)
- Pots/bouteilles sur fond contrasté (Miel, Sirop, Confitures)
- Coffrets/assortiments (Coffret gourmand, Assortiment apéritif)

**Rendu v1.1 actuel** : zone photo `#F8EEDB` baked. Sur lifestyle, le rendu est jugé acceptable (la scène remplit la zone).

---

## Cas particuliers identifiés (informationnel)

| Produit | Phénomène | Recommandation Dev |
|---------|-----------|--------------------|
| Pâtes de manioc Mayotte (#9) | Plan de travail blanc/gris non uniforme | lifestyle v1.1 — confirmé par POC (halos en alpha) |
| Colombo des Antilles (#154) | Scène cuisine — étiqueté packshot dans manifest mais lifestyle réel | lifestyle v1.1 — confirmé par POC |
| Crackers manioc (#8) | Sachet plastique transparent | NEEDS_REVIEW → probable packshot_alpha (POC OK) |

---

## Prochaine étape — validation MOA

Merci de :

1. Ouvrir `AUDIT_CLASSIFICATION_PILOTE_43_V1_2_ALPHA.csv` ;
2. Vérifier la colonne `audit_class` sur les 43 lignes ;
3. **Confirmer ou ajuster** la classe pour chaque ligne (notamment NEEDS_REVIEW) ;
4. **Renvoyer le CSV validé** au Dev (ou indiquer les changements ligne par ligne) ;
5. Ensuite seulement, P8-3 re-export sur la liste validée.

**Aucun re-export ne sera lancé sans validation MOA explicite de cette classification.**

---

## Garde-fous respectés (P8-1)

- ✅ Aucune modification `image_1920`
- ✅ Aucun re-export effectué (lecture des sources seule)
- ✅ Aucune modification Odoo
- ✅ Pas d'IA / pas de rembg
- ✅ Pas de cron
- ✅ Lot X exclu de l'audit (43 lignes uniquement)

---

## Références

| Document | Rôle |
|----------|------|
| [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_2_ALPHA_P8.md`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_2_ALPHA_P8.md) | Ticket P8 |
| [`RAPPORT_POC_V1_2_ALPHA_3_PACKSHOTS.md`](./RAPPORT_POC_V1_2_ALPHA_3_PACKSHOTS.md) | POC fondateur 3 cibles |
| `tools/ck_image_normalizer/audit_classification_v12_alpha.py` | Script audit reproductible |
| `AUDIT_CLASSIFICATION_PILOTE_43_V1_2_ALPHA.csv` | Tableau audit complet |
