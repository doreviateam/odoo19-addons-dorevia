# Réponse MOA — Retour Dev principal sur Header C-Kréyòl V2.1

| Champ | Valeur |
| --- | --- |
| **Projet** | C-Kréyòl / CK Marketone |
| **Document concerné** | Cadrage Header V2.1 · [`note_07.md`](./note_07.md) |
| **Réponse à** | Retour Dev principal · [`note_07_retour_dev.md`](./note_07_retour_dev.md) |
| **Décision MOA** | **Arbitrages actés** — brief amendé · ticket H1 |
| **Statut** | **✅ Validé MOA · 2026-06-21** |
| **Contexte** | Post **Lot Nav-1** clôturé (PR #78 · GO merge QA) |

---

## 1. Accusé de réception

La MOA valide le retour Dev sur le cadrage Header C-Kréyòl V2.1 et **acte** les arbitrages de réconciliation avec Nav-1.

Le brief [`note_07.md`](./note_07.md) est amendé (§8 bis · §9 bis · §11 bis · §18.1 bis · §19 bis · URLs §12.2).

---

## 2. Position MOA générale

### GO cadrage Header V2.1

> Header C-Kréyòl V2.1 = header média-commerce premium, e-commerce d’abord, enrichi par l’origine identifiable et la culture créole.

Structure en trois strates **validée** :

```text
Strate 0 — Bandeau service (rassurer)
Strate 1 — Logo + recherche + compte + panier (vendre)
Strate 2 — Navigation (orienter) = Nav-1 figé
```

### Règle de non-régression Nav-1

> **La Strate 2 livrée par Nav-1 est la baseline figée pour H1.**
> H1 ne rouvre pas `nav_sync.py`, les menus commerce, le mega Découvrir ni le regroupement mobile **sans lot Nav-1 bis**.

---

## 3. Arbitrage 1 — Périmètre lot H1 (delta)

| Strate | Inclus H1 | Hors H1 |
| --- | --- | --- |
| **0** — Bandeau global Option A | ✅ | — |
| **1** — Marque C-Kréyòl · recherche · compte · panier | ✅ | — |
| **Mobile** — chrome ligne 1 | ✅ | Contenu drawer Nav-1 |
| **2** — Navigation | ❌ | **Nav-1 baseline** |

Ticket : [`TICKET_DEV_LOT_H1_HEADER_CK_V2_1.md`](../design/TICKET_DEV_LOT_H1_HEADER_CK_V2_1.md).

---

## 4. Arbitrage 2 — Navigation (baseline Nav-1)

| Sujet | Décision MOA actée |
| --- | --- |
| **Professionnels** | **Sous Découvrir** — pas top-level |
| Libellés | **Épicerie** · **Soin & Bien-être** |
| Découvrir | **Mega** natif CE (Nav-1) |
| Mobile | **Nos univers** accordéon |
| Contact | **`/contactus`** · sous Découvrir + footer |
| Recettes | **`/recettes`** |
| Producteurs hub | **`/producteurs`** → **H2** |

Desktop :

```text
Tous nos produits · Épicerie · Soin & Bien-être · Découvrir
```

Mobile :

```text
Tous nos produits · Nos univers · Découvrir
```

---

## 5. Arbitrage 3 — Marque C-Kréyòl

**GO** graphie **C-Kréyòl** dans le header public · recette typo caractère **ò** (1280 + 390 px).

---

## 6. Arbitrage 4 — Bandeau Strate 0

**Option A actée** — bandeau global header :

```text
Produits créoles sélectionnés · Origines identifiées · Livraison suivie
```

Coexistence home : ne pas dupliquer le même triptyque que la trust-bar S2 sur `/` (cf. `note_07` §9 bis).

---

## 7. Arbitrage 5 — Recherche centrale

**GO** H1 · placeholder `Rechercher un produit, une saveur...` · moteur **produits only** · résultats vides = backlog H1 bis.

---

## 8. Arbitrage 6 — Mobile chrome

**GO** `Menu · C-Kréyòl · Recherche · Panier` · compte dans le drawer · Contact via Découvrir + footer (Nav-1).

---

## 9. Verdict MOA

```text
GO cadrage Header C-Kréyòl V2.1 — amendé post-Nav-1
GO rédaction ticket Dev H1 (delta Strate 0/1 + mobile chrome)
Nav-1 = baseline navigation figée
H2 / Nav-2 / Nav-1 bis = lots ultérieurs distincts
Pas d’exécution H1 avant relecture ticket
```

---

*Réponse MOA · Header C-Kréyòl V2.1 · validé 2026-06-21.*
