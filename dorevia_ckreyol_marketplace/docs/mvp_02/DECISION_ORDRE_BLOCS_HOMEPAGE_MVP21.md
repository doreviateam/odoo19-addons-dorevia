# Décision — Ordre des blocs bas de page Homepage MVP2.1

**Statut** : actée (MOA) ; **gel conception** — l’ordre des blocs **ne se rouvre pas** en implémentation sans **ticket MOA** de révision.  
**Date** : 2026-04-24.  
**Périmètre** : enchaînement **après la zone Produits** (fournisseur + sélection) jusqu’au **bloc confiance**, dans le document canonique [1_HOMEPAGE.md](1_HOMEPAGE.md) et, à terme, dans [`ckr_homepage.xml`](../../views/pages/ckr_homepage.xml).

## Décision

**L’éditorial précède l’inscription (newsletter / cercle).**

Séquence retenue :

1. **Produits** (Blocs wireframe 4–5 : fournisseur + sélection)  
2. **Éditorial** (bandeau « Collection » — V1)  
3. **Inscription** (cercle C-Kreyol — `ckr_snippet_circle`)  
4. **Réassurance** (bloc confiance — `ckr_snippet_trust`)

## Synthèse (gel)

```text
Décision MOA :
Éditorial avant Inscription.

Ordre : Produits → Éditorial → Inscription → Réassurance.
```

## Justification

Enchaînement **Produits → Éditorial → Inscription** : le visiteur voit l’**offre**, comprend l’**univers** (sélection, thème, origine), puis peut **s’engager** (newsletter) — sans inverser cette logique.

## État implémentation (MVP2.1 — 2026-04-25)

Dans [`views/pages/ckr_homepage.xml`](../../views/pages/ckr_homepage.xml), l’ordre **effectif** est :

`ckr_snippet_hero` → `ckr_snippet_entries` → *(si `ckr_hpage_mvp1_tail_blocks`)* `ckr_snippet_supplier` → `ckr_snippet_selection` → *(si flag)* `ckr_snippet_editorial` → **`ckr_snippet_circle`** → **`ckr_snippet_trust`**.

Le drapeau **`ckr_hpage_mvp1_tail_blocks`** (défaut `0`) **masque** uniquement **Fournisseur** et **Éditorial** ; **Inscription** et **Réassurance** sont **toujours** rendus.

## Références

| Document | Rôle |
|----------|------|
| [1_HOMEPAGE.md](1_HOMEPAGE.md) | §4 Éditorial, §5 Inscription, §6 Réassurance |
| [TICKET_INSCRIPTION_HOMEPAGE_MVP21.md](../crea/TICKET_INSCRIPTION_HOMEPAGE_MVP21.md) | Exécution snippet Inscription + PV recette |
| [TICKET_REASSURANCE_HOMEPAGE_MVP21.md](../crea/TICKET_REASSURANCE_HOMEPAGE_MVP21.md) | Évolution bloc confiance (3 vs 5 items) + PV recette |
| [WIREFRAME_HOMEPAGE.md](../direction/WIREFRAME_HOMEPAGE.md) | Blocs 6–7 |
| [PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md](../crea/PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md) | §9.3 éditorial V1 |

## Historique

| Date | Événement |
|------|-----------|
| 2026-04-24 | Actée — Éditorial avant Inscription ; [1_HOMEPAGE.md](1_HOMEPAGE.md) renuméroté §4–6. |
| 2026-04-24 | **Validation MOA** — structure canonique §1–6 et ordre Produits → Éditorial → Inscription → Réassurance **gelés** côté conception ; suite = tickets d’impl. dédiés uniquement ; repère `ckr_homepage.xml` validé pour le futur snippet Inscription. |
| 2026-04-24 | **Ticket Inscription** — [TICKET_INSCRIPTION_HOMEPAGE_MVP21.md](../crea/TICKET_INSCRIPTION_HOMEPAGE_MVP21.md) + [PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md) ; références § mises à jour. |
| 2026-04-24 | **Ticket Réassurance** — [TICKET_REASSURANCE_HOMEPAGE_MVP21.md](../crea/TICKET_REASSURANCE_HOMEPAGE_MVP21.md) + [PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md). |
| 2026-04-25 | **Clôture homepage MVP2.1 (MOA)** — chaînage cercle + réassurance ; PV Inscription et Réassurance **GO** ; alignement de la présente section sur [`ckr_homepage.xml`](../../views/pages/ckr_homepage.xml). |
