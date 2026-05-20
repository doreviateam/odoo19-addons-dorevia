# Rapport P4 — revue opérateur MOA — pilote média 50 SKU

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-20 |
| **Run** | `tools/ck_image_normalizer/reports/runs/pilote_20260520/` |
| **Recette** | `ck_shop_tile_v1.1` |
| **Fichier opérateur** | `tools/ck_image_normalizer/reports/runs/pilote_20260520/pilote_operateur.csv` |
| **Périmètre** | Revue des 29 `NEEDS_REVIEW` uniquement |
| **Garde-fous** | Aucun code Odoo · aucun remplacement `image_1920` · aucune modification des sources |

---

## 1. Synthèse P4

Les 29 lignes `NEEDS_REVIEW` ont été revues et renseignées dans `pilote_operateur.csv`.

| Décision | Sens | Nombre |
|----------|------|-------:|
| `E` | Exploitable tel quel | 3 |
| `R` | Exploitable avec réserve | 12 |
| `M` | Reprise manuelle nécessaire | 7 |
| `X` | À exclure / redemander fournisseur | 7 |

Synthèse opérateur :

```text
NEEDS_REVIEW revus : 29 / 29
Exploitables après revue (E + R) : 15 / 29
Non exploitables sans action (M + X) : 14 / 29
Temps moyen de revue : 0,88 min / image
Temps total estimé : 25,6 min
```

---

## 2. Lecture cumulée du pilote

Résultat moteur initial :

| Statut moteur | Nombre |
|---------------|-------:|
| `OK` | 18 |
| `OK_WITH_WARNINGS` | 3 |
| `NEEDS_REVIEW` | 29 |
| `REJECTED` | 0 |

Après revue P4 :

| Catégorie exploitable | Nombre |
|-----------------------|-------:|
| `OK` moteur | 18 |
| `OK_WITH_WARNINGS` moteur | 3 |
| `NEEDS_REVIEW` validés `E` | 3 |
| `NEEDS_REVIEW` validés `R` | 12 |
| **Total exploitable / exploitable avec réserve** | **36 / 50** |

Taux exploitable après revue :

```text
36 / 50 = 72 %
```

Images non exploitables sans action :

```text
M + X = 14 / 50 = 28 %
```

---

## 3. Causes principales de réserve (`R`)

Les réserves ne bloquent pas forcément l’usage en tuile, mais doivent être tracées.

Causes observées :

- produit lisible mais petit dans une scène lifestyle ;
- étiquette peu lisible en taille mobile ;
- scène attractive mais un peu dense ;
- couture fond / carte acceptable mais perfectible ;
- identification du SKU correcte, sans être parfaitement packshot.

Exemples typiques :

- confitures en scène ;
- sauces en ambiance ;
- trio ou assortiment lisible mais dense ;
- pot de miel identifiable mais étiquette faible.

---

## 4. Causes principales de reprise manuelle (`M`)

Les reprises manuelles concernent surtout les sources techniquement récupérables mais pas publiables telles quelles.

Causes observées :

- produit trop latéralisé ou partiellement coupé ;
- détourage / zone vide très visible ;
- source plein cadre difficile ;
- scène trop éditoriale alors que le SKU doit rester identifiable ;
- packshot historique nécessitant recadrage ou source dédiée.

Exemples :

- pâtes / semoule manioc avec détourage visible ;
- biscuits trop cadrés sur un bord ;
- coffret latéralisé ;
- scènes d’ingrédients sans produit clairement dominant.

---

## 5. Causes principales de demande fournisseur (`X`)

Les cas `X` ne relèvent pas d’un simple ajustement de recette.

Causes observées :

- visuel générique sans produit principal identifiable ;
- image lifestyle non adaptée à une tuile SKU ;
- incohérence entre nom du produit et visuel source ;
- produit attendu absent ou impossible à reconnaître.

Exemples :

- rayon de bouteilles générique ;
- portrait / ambiance non produit ;
- image de miel pour un SKU sirop ;
- image de pâtes manioc pour farine ou flocons.

---

## 6. Recommandation MOA

Recommandation :

```text
GO avec réserves — flux opérateur viable, mais pas de GO exploitation automatique.
```

Justification :

- le moteur ne rejette aucune image automatiquement ;
- après revue humaine, **72 %** du lot devient exploitable ou exploitable avec réserve ;
- après mini-batches ciblés lot M + sources manioc distinctes, le bilan consolidé monte à **43 / 50 exploitables (86 %)** ;
- le temps moyen de revue reste raisonnable ;
- les échecs sont majoritairement liés à la qualité ou à l’inadéquation des sources, pas uniquement à la recette ;
- les `X` montrent qu’une charte source fournisseur est nécessaire.

Limite :

```text
La recette ck_shop_tile_v1.1 ne doit pas être utilisée en publication automatique.
Le sas NEEDS_REVIEW reste obligatoire.
```

---

## 7. Décision proposée

```text
P4 complété — pilote_operateur.csv renseigné — synthèse E/R/M/X disponible
```

**Verdict MOA (2026-05-20)** :

```text
GO avec réserves — flux opérateur viable, pas de GO exploitation automatique.
```

→ Clôture officielle P5 : [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](./RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md)

Décision opérationnelle :

```text
GO avec réserves pour poursuivre le pilote média catalogue.
Pas de remplacement image_1920.
Pas d’industrialisation.
Préparer une charte source fournisseur + reprise manuelle ciblée des 7 M.
Redemander une source correcte pour les 7 X.
```

---

## 8. Suite conseillée

1. Valider MOA les 36 images exploitables ou exploitables avec réserve.
2. Isoler les 7 `M` dans un lot de reprise manuelle.
3. Isoler les 7 `X` dans une demande source fournisseur.
4. Ne pas modifier la recette `ck_shop_tile_v1.1` tant que les problèmes source ne sont pas séparés des problèmes moteur.
5. Relancer un mini-batch uniquement sur les reprises `M` après correction.

---

## 9. Addendum consolidé mini-batches

Décisions ultérieures du 2026-05-20 :

- mini-batch lot M corrigé : **5 / 7** images récupérées et validées visuellement ;
- mini-batch sources manioc distinctes : **2 / 2** SKU manioc réintégrés ;
- lot X : **7 / 50** maintenus en demande fournisseur / exclusion temporaire.

Bilan consolidé :

```text
43 / 50 exploitables ou exploitables avec réserve
Taux exploitable : 86 %
Reste hors flux : 7 / 50 = 14 %
```

Référence : [`REPONSE_MOA_REINTEGRATION_2_MANIOC_SOURCES_DISTINCTES.md`](./REPONSE_MOA_REINTEGRATION_2_MANIOC_SOURCES_DISTINCTES.md)
