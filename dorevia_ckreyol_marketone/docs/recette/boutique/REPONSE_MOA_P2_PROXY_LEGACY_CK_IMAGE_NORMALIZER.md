# Réponse MOA — CK Image Normalizer — Batch P2 proxy legacy

| Champ | Valeur |
|-------|--------|
| **Statut** | **Décision MOA officielle** |
| **Date** | 2026-05-20 |
| **Ticket** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md) |
| **Analyse Dev** | [`ANALYSE_REJETS_P2_PROXY_CK_IMAGE_NORMALIZER.md`](./ANALYSE_REJETS_P2_PROXY_CK_IMAGE_NORMALIZER.md) |

---

Bonjour Dev,

Merci pour l'exécution du batch P2 proxy legacy sur les 21 images disponibles dans :

`/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketplace/docs/assets`

Nous prenons acte des résultats :

```text
Total        : 21 images
OK           : 13
OK_WARNINGS  : 1
REJECTED     : 7
OK rate      : 67 %
Rejected rate: 33 %
GO candidate : non
```

---

## Verdict MOA

Le batch proxy legacy est **utile mais non conclusif**.

Il ne permet pas un GO POC strict, car le taux `REJECTED` est trop élevé :

- seuil attendu : ≤ 10 % ;
- résultat proxy : 33 %.

Cependant, ce batch confirme que le moteur fonctionne techniquement :

- génération WebP / JPEG OK ;
- archive originaux OK ;
- rapports JSON / CSV OK ;
- previews avant / après OK ;
- mocks HTML grille source / normalisée / comparatif OK ;
- notation MOA G1–G6 prête ;
- taux OK de 67 % sur un lot legacy difficile.

---

## Décision MOA

**GO technique partiel — calibrage recette requis.**

Pas de GO POC final sur ce batch proxy.

Ce batch doit être utilisé comme **batch d'apprentissage**, afin de comprendre les rejets et d'améliorer la recette avant le lot officiel MOA.

> **Addendum MOA 2026-05-20** : l'échantillon officiel POC est **21 références** (banque catalogue disponible), et non 30. Le batch v1.1 sur ces 21 fichiers constitue le lot de décision.

---

## Demande d'analyse complémentaire

Merci d'analyser les 7 images `REJECTED`.

Pour chaque rejet, produire un tableau indiquant :

- nom du fichier ;
- profil déclaré : `packshot` ou `lifestyle` ;
- règle de rejet déclenchée ;
- métrique concernée ;
- cause probable ;
- décision recommandée :
  - rejet légitime ;
  - seuil trop strict ;
  - profil mal renseigné ;
  - image source non adaptée ;
  - cas à passer en `NEEDS_REVIEW` plutôt que `REJECTED`.

Point d'attention particulier :

> le moteur semble rejeter trop de cas plein cadre côté packshot.

Merci de vérifier si la règle liée au plein cadre, notamment `content_area_ratio > 0.95`, est trop stricte et s'il faudrait plutôt transformer certains rejets en `OK_WITH_WARNINGS` ou `NEEDS_REVIEW`.

**→ Livrable Dev** : [`ANALYSE_REJETS_P2_PROXY_CK_IMAGE_NORMALIZER.md`](./ANALYSE_REJETS_P2_PROXY_CK_IMAGE_NORMALIZER.md)

---

## Recette MOA à faire

Nous allons examiner :

- les previews avant / après ;
- la grille source ;
- la grille normalisée ;
- la grille comparative ;
- le CSV de notation G1–G6.

Le fond `#F8EEDB` baked-in reste un point central d'évaluation, notamment sur :

- la chaleur perçue ;
- la couture image / carte ;
- la cohérence entre produits ;
- l'absence d'effet artificiel.

---

## Suite envisagée

Après analyse des rejets, nous déciderons :

1. soit de recalibrer `ck_shop_tile_v1` ;
2. soit de conserver la recette actuelle et considérer que le lot proxy était volontairement trop difficile ;
3. soit de relancer un batch ciblé après ajustement ;
4. soit de valider les **21 refs** comme lot officiel et de trancher sur le batch v1.1 (révision MOA 2026-05-20 — plus d'attente d'un lot 30).

---

## Rappel

Pas de code Odoo à ce stade.

Le chantier reste au stade POC externe / recette image.

---

**Validé par** : MOA · **Date** : 2026-05-20
