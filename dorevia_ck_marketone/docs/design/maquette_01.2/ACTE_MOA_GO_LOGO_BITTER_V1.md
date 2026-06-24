# Acte MOA — GO Logo Bitter (wordmark C-Kréyòl)

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-23 |
| **Périmètre** | Police du wordmark logo `.ck-header__brand` — Header CK V2.2 / P4 |
| **Instance recette** | `dorevia_ck_marketone_01` · `http://localhost:18079` |
| **Module thème** | `dorevia_ck_theme` `19.0.1.48.0` |
| **Référence technique** | [`P4_BITTER_TEST_CONTROLE.md`](P4_BITTER_TEST_CONTROLE.md) · [`P4_PISTES_TYPO_LOGO_CK.md`](P4_PISTES_TYPO_LOGO_CK.md) (5 pistes comparées en amont) |

---

## Périmètre

Validation de la police **Bitter** comme typographie définitive du wordmark "C-Kréyòl", à l'exclusion de toute autre zone du header (H1, titres mega-menu, carte visuelle éditoriale, UI/navigation).

---

## Décision MOA validée

**Bitter est validée comme police du wordmark C-Kréyòl.**

Remplace Fraunces sur le seul élément `.ck-header__brand`, via le token dédié `$ck-font-logo` (`ck_tokens.scss`).

---

## Points validés

- Scope correct : Bitter appliquée uniquement à `.ck-header__brand`, rien d'autre.
- Fraunces reste la police éditoriale (H1, titres mega-menu, cartes visuelles).
- DM Sans reste la police UI/navigation/baseline.
- Rendu desktop : gain d'ancrage et de présence, sans excès décoratif.
- Rendu mobile : lisible, compact, équilibré.
- Trait d'accent terracotta sous le wordmark : correctement positionné (ancrage déjà corrigé en amont, indépendant de la police).
- Coexistence de 3 familles de police dans le header jugée non dispersée — chaque police a un rôle clair et distinct (logotype / éditorial / UI).

---

## Couverture de vérification

- Licence Bitter : SIL OFL 1.1, vérifiée directement sur `google/fonts/ofl/bitter/OFL.txt`.
- Auto-hébergement : fichiers `bitter-latin.woff2` / `bitter-latin-ext.woff2` ajoutés à `static/src/fonts/`, même procédure que Fraunces/DM Sans (pas de CDN Google Fonts).
- Non-régression du système typo hors logo : vérifiée par `getComputedStyle` (H1, titres mega-menu, carte visuelle — tous confirmés Fraunces, inchangés).
- Couleurs, contraste noir/terracotta, taille et accent du wordmark : inchangés (déjà validés en amont, non remis en cause par ce test).

---

## Verdict MOA

```text
GO MOA — Logo Bitter validé comme police définitive du wordmark C-Kréyòl.
```

Le test contrôlé `P4_BITTER_TEST_CONTROLE.md` passe du statut "test" au statut **implémentation retenue**.

---

## Réserve inchangée (hors périmètre de cet acte)

Les visuels éditoriaux de mega-menu (Épicerie, Boissons — `ck.mega.menu.rayon.visual`) restent des **placeholders BO de démonstration**, non concernés par ce GO. Réserve documentée dans [`P4_HYBRIDE_HEADER_ENSEIGNE_CK.md`](P4_HYBRIDE_HEADER_ENSEIGNE_CK.md) §2, toujours active : un brief contenu/visuel définitif par rayon reste à cadrer avant clôture complète du chantier P4.

---

## Suite

Chantier P4 logo clos. Reste ouvert pour clôture P4 globale : brief visuels rayon définitifs (placeholders → contenu validé).
