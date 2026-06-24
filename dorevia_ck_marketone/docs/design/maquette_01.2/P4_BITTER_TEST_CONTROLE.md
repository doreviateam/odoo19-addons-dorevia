# P4 — Bitter validée (wordmark logo)

| Champ | Valeur |
| --- | --- |
| Date | 2026-06-23 |
| Déclencheur | Arbitrage MOA suite à `P4_PISTES_TYPO_LOGO_CK.md` — Bitter retenue comme direction typographique |
| Périmètre | Wordmark logo uniquement (`.ck-header__brand`) — **implémenté et conservé** |
| Modules | `dorevia_ck_theme` **19.0.1.48.0** |
| Statut | **Implémentation retenue** — GO MOA posé le 2026-06-23 (cf. [`ACTE_MOA_GO_LOGO_BITTER_V1.md`](ACTE_MOA_GO_LOGO_BITTER_V1.md)). Réserve inchangée : visuels rayon mega-menu = placeholders BO (cf. `P4_HYBRIDE_HEADER_ENSEIGNE_CK.md` §2) |

---

## 1. Ce qui a été fait

- Ajout des fichiers `bitter-latin.woff2` / `bitter-latin-ext.woff2` (`static/src/fonts/`), téléchargés depuis Google Fonts, licence **SIL OFL 1.1** vérifiée sur `google/fonts/ofl/bitter/OFL.txt` — même procédure d'auto-hébergement que Fraunces/DM Sans (`website_fonts.scss`).
- Nouveau token **`$ck-font-logo: "Bitter", $ck-font-display;`** dans `ck_tokens.scss`, séparé de `$ck-font-display` (Fraunces).
- `.ck-header__brand` (le wordmark, et seulement lui) utilise désormais `$ck-font-logo`.

### Ce qui n'a volontairement pas changé

Conformément à « mettre à jour le token/logo concerné sans bouleverser tout le système typo » :

| Élément | Police | Vérifié |
| --- | --- | --- |
| H1 (`Boutique C-Kreyol`) | Fraunces — inchangé | `getComputedStyle` confirmé |
| Titres mega-menu (`Origines & producteurs`, etc.) | Fraunces — inchangé | `getComputedStyle` confirmé |
| Carte visuelle mega-menu (`Épicerie créole`, etc.) | Fraunces — inchangé | `getComputedStyle` confirmé |
| Baseline (`épicerie créole`) | DM Sans — inchangé (jamais sur Fraunces) | — |
| Navigation N3, recherche, boutons | DM Sans — inchangé | — |

Couleurs, contraste noir/terracotta, accent sous le wordmark, taille du wordmark : **strictement inchangés** (déjà validés, non remis en cause par ce test).

---

## 2. Captures

| Vue | Avant (Fraunces, référence) | Après (Bitter, ce test) |
| --- | --- | --- |
| Desktop initial | `captures/recette_header_v22/p4_final/desktop_initial.png` | `captures/recette_header_v22/p4_bitter/desktop_initial.png` |
| Mega Épicerie | `captures/recette_header_v22/p4_final/mega_epicerie.png` | `captures/recette_header_v22/p4_bitter/mega_epicerie.png` |
| Mega Boissons | `captures/recette_header_v22/p4_final/mega_boissons.png` | `captures/recette_header_v22/p4_bitter/mega_boissons.png` |
| Mobile fermé | `captures/recette_header_v22/p4_final/mobile_ferme.png` | `captures/recette_header_v22/p4_bitter/mobile_ferme.png` |

La colonne « Avant » réutilise les captures déjà validées de la recette P4 précédente (état strictement identique hors logo) — pas de recapture artificielle d'un état qui n'a pas changé.

---

## 3. Lecture du résultat

- Le wordmark gagne en présence et en ancrage ("épicerie/boutique") sans devenir décoratif, conforme à l'appréciation portée en phase de pistes.
- Lisible aux deux gabarits ; l'accent terracotta et le trait restent correctement positionnés (ancrage déjà corrigé en amont, indépendant de la police).
- **Point structurel nouveau, à votre lecture** : le header affiche désormais 3 familles de police au lieu de 2 — Bitter (logo seul), Fraunces (H1, titres mega-menu, carte éditoriale), DM Sans (UI, navigation, baseline). C'est un choix de "logotype distinct de l'éditorial", courant en branding, mais c'est précisément l'équilibre que vous avez indiqué vouloir vérifier avant le GO final.

---

## 4. GO MOA — posé

Lecture du rendu global P4 effectuée côté MOA (scope, rôles Fraunces/DM Sans/Bitter, desktop, mobile, trait, cohérence des 3 familles). **GO MOA posé le 2026-06-23** : Bitter validée comme police définitive du wordmark C-Kréyòl. Détail des points validés : [`ACTE_MOA_GO_LOGO_BITTER_V1.md`](ACTE_MOA_GO_LOGO_BITTER_V1.md).

---

## 5. Statut

```text
Bitter validée et implémentée — police définitive du wordmark C-Kréyòl.
Scope strictement limité au wordmark, système typo H1 / mega-menu / UI inchangé (vérifié).
GO MOA posé le 2026-06-23.
Réserve inchangée : visuels rayon mega-menu = placeholders BO, brief définitif à cadrer.
```
