# Note MOA — Cadrage CK-HOME-001B — Réserves visuelles home post-001A

| Champ | Valeur |
| --- | --- |
| Date | 2 juillet 2026 |
| Projet | C-Kréyòl Marketone — home |
| Destinataires | MOA, Produit, QA, Dev |
| Statut | **GO ticket Dev** — périmètre 001B-a + 001B-b validé MOA |
| Module | `dorevia_ck_marketone_content` (+ `dorevia_ck_theme` si correctif CSS vedettes) |
| Version contenu de référence | **19.0.1.75.0** (post CK-HOME-001A) |
| Base recette | `dorevia_ck_marketone_01` — http://localhost:18079 |
| Prérequis validés | Upgrade `-u dorevia_ck_marketone_content,dorevia_ck_theme` + restart Odoo (2 juil. 2026) · Home `200` · hero 001A présent |

---

## Objet

Ouvrir le **lot suivant home** après clôture **CK-HOME-001C** (hygiène) et **CK-HOME-001A** (hero).  
CK-HOME-001B ne vise **pas** une refonte globale : il borne les **réserves visuelles** encore ouvertes depuis la recette Home Maquette V1 (juin 2026), sans rouvrir hero, navigation, newsletter ni tunnel achat.

---

## Contexte — ce qui est stabilisé (ne pas rouvrir)

| Lot | Statut | Périmètre |
| --- | --- | --- |
| **CK-HOME-001C** | GO clôturé | Marque C-Kréyòl · newsletter FR · 4 cartes univers (Boissons) |
| **CK-HOME-001A** | GO clôturé | Hero repositionné · CTA `/producteurs` · CA6 mobile 390 px documenté |
| **Navigation Option C** | GO | Header catalogue · icône Boutique |
| **Tunnel achat** | Gel V1 | Shop → panier → checkout inchangé |

Références : [`NOTE_MOA_CLOTURE_CK_HOME_001C_20260702.md`](NOTE_MOA_CLOTURE_CK_HOME_001C_20260702.md) · [`NOTE_MOA_CLOTURE_CK_HOME_001A_20260702.md`](NOTE_MOA_CLOTURE_CK_HOME_001A_20260702.md) · [`NOTE_MOA_LIVRAISON_20260702.md`](NOTE_MOA_LIVRAISON_20260702.md)

---

## État actuel — inventaire blocs (post-upgrade 2 juil.)

Ordre observé sur `/` (sandbox recettée) :

```text
1. Hero 001A              → ck-hero--marketone-v1        ✅ stabilisé
2. Réassurance            → s_ck_reassurance             ✅ stable (baseline)
3. Nos coups de cœur      → ck-featured                  🔶 réserve E1
4. Acheter par univers    → section 4 cartes             ✅ stabilisé (001C)
5. Coffrets découverte    → ck-discovery                 🔶 réserve E2
6. Dual Pro / Newsletter  → ck-dual                      ✅ fonctionnel
7. Éditorial bas de page  → ck-home-editorial            🔶 copy à arbitrer (optionnel)
8. Footer                 → Phase 1                      ✅ hors périmètre court terme
```

Contrôle rapide post-upgrade :

| Contrôle | Résultat |
| --- | --- |
| HTTP `/` | `200` |
| Hero kicker / titre / CTA producteurs | Présents |
| Blocs `ck-featured`, `ck-discovery`, `ck-dual` | Présents |
| Version module | `19.0.1.75.0` |

---

## Gouvernance — renommage lot producteurs

L’ancienne intention « **CK-HOME-001B = bloc producteurs / transformateurs** » est **abandonnée** pour éviter toute confusion documentaire.

| Référence | Nouveau sens |
| --- | --- |
| **CK-HOME-001B** (ce cadrage) | Réserves visuelles home post-001A — vedettes · coffret · (promotions P2) |
| **Futur lot producteurs home** | **`CK-HOME-002`** ou **`CK-HOME-PRODUCERS-001`** — à cadrer séparément |

---

## Ticket Dev

**GO rédaction** — [`TICKET_DEV_HOME_VISUAL_CK_HOME_001B.md`](TICKET_DEV_HOME_VISUAL_CK_HOME_001B.md)

Périmètre ticket initial : **001B-a + 001B-b uniquement**. `/promotions` (001B-c) reste P2 hors ticket.

---

## Réserves héritées — source recette QA (juin 2026)

Extrait [`RECETTE_QA_RAPPROCHEMENT_HOME_MAQUETTE_V1.md`](../design/maquette_01.2/RECETTE_QA_RAPPROCHEMENT_HOME_MAQUETTE_V1.md) — toujours d’actualité pour les blocs **sous** le hero :

| ID | Bloc | Constat | Priorité MOA proposée |
| --- | --- | --- | --- |
| **E1** | Vedettes (`ck-featured`) | 5 produits · prix · liens OK — **images produit non visibles** (hauteur zone image `0px` en recette) | **P1 — candidat 001B-a** |
| **E2** | Coffrets (`ck-discovery`) | Bloc présent · CTA `/kits` OK — **fallback beige** au lieu d’un visuel coffret qualifié | **P1 — candidat 001B-b** |
| **E3** | `/promotions` | Route **404** · absent de la Home actuelle | **P2 — arbitrage MOA** (créer route vs retirer du périmètre Home) |
| **E4** | Polish global maquette | Écart de richesse visuelle cartes / rythmes verticaux | **Lot 6 / post-001B** — hors 001B strict |

---

## Proposition de découpage CK-HOME-001B

### Option recommandée — 2 sous-lots P1 + 1 arbitrage P2

| Sous-lot | Objectif | Fichiers probables | Hors scope |
| --- | --- | --- | --- |
| **001B-a — Vedettes visibles** | Rendre les images produit des cartes « Nos coups de cœur » visibles (hauteur stable, pas de placeholder) | `home_featured.py` · SCSS thème `.ck-featured` · tests `test_ck_home_lot2_*` | Changer la curation produits · refonte card shop |
| **001B-b — Visuel coffret** | Remplacer le fallback beige par une image coffret qualifiée (asset BO ou statique CK) | `home_discovery_pack.py` · asset `/web/image` ou `static/` | Comportement `/kits` · logique pack |
| **001B-c — Promotions (arbitrage)** | Créer `/promotions` (redirection shop filtré ?) **ou** retirer l’URL des critères Home | CMS page ou contrôleur · data XML | Mega-menu · SEO complet |

### Optionnel — harmonisation copy (non bloquant)

| Sujet | Constat | Décision MOA |
| --- | --- | --- |
| **Éditorial bas** | Titre actuel : *« C-Kréyòl, la boutique des saveurs créoles »* — ton encore **boutique-only** vs hero 001A | Inclure dans 001B ou reporter lot copy dédié ? |
| **Liens éditorial** | `/a-propos`, `/recettes` — routes à vérifier en recette | Contenu CMS hors Dev si pages absentes |

---

## Questions MOA (à trancher avant ticket Dev)

1. **Périmètre 001B** : valider **001B-a + 001B-b** seuls (recommandé) ou inclure **001B-c** et/ou copy éditorial ?
2. **E1 vedettes** : correctif **CSS/SSR minimal** (recommandé QA juin) ou refonte card alignée shop ?
3. **E2 coffret** : image fournie par MOA (shooting / asset maquette) ou placeholder CK temporaire acceptable ?
4. **E3 promotions** : créer la route (contenu ?) ou **clôturer** la réserve en retirant `/promotions` du périmètre Home ?
5. **Thème** : un correctif SCSS dans `dorevia_ck_theme` pour E1 est-il autorisé (acte séparé) ou content-only ?

---

## Critères d’acceptation proposés (brouillon)

### CA1 — Vedettes (si 001B-a retenu)

- Les cartes « Nos coups de cœur » affichent une **image produit visible** sur desktop 1280 et mobile 390 px.
- Prix, liens `/shop/...` et logique curation inchangés.
- Pas de régression tests `dorevia_ck_marketone_home_lot2`.

### CA2 — Coffret (si 001B-b retenu)

- Le bloc coffrets affiche un **visuel qualifié** (pas le fallback beige actuel).
- CTA vers `/kits` inchangé et fonctionnel.

### CA3 — Mobile 390 px

- Pas d’overflow horizontal sur la home complète (vedettes + coffret inclus).
- Recette documentée (capture ou métriques Playwright), sur le modèle CA6 de 001A.

### CA4 — Non-régression

- Hero 001A, section univers 001C, dual Pro/Newsletter, tunnel achat : **inchangés fonctionnellement**.

---

## Hors périmètre CK-HOME-001B

- Hero (001A), newsletter, marque, univers 4 cartes (001C)
- Navigation header, footer, SEO canonical tunnel
- Refonte `/producteurs`, communauté, blog, forum
- Lot 6 polish global (E4) — sauf décision MOA explicite d’élargir 001B
- Déploiement prod

---

## Recette QA envisagée

| Étape | Méthode |
| --- | --- |
| Post-upgrade | `-u dorevia_ck_marketone_content` (+ thème si SCSS) · restart container |
| Desktop 1280 | Capture hero + vedettes + coffret |
| Mobile 390 | `scrollWidth` / `clientWidth` · visibilité images vedettes |
| Tests auto | Tags `dorevia_ck_marketone_home_lot2`, `lot3`, smoke home |
| Référence maquette | [`RECETTE_QA_RAPPROCHEMENT_HOME_MAQUETTE_V1.md`](../design/maquette_01.2/RECETTE_QA_RAPPROCHEMENT_HOME_MAQUETTE_V1.md) |

Scripts réutilisables : `ck_lot2_*`, `ck_lot3_*`, `ck_lot4_*` dans `docs/design/maquette_01.2/scripts/`.

---

## Verdict MOA proposé (cadrage)

```text
CK-HOME-001A / 001C → clôturés GO
CK-HOME-001B → GO ticket Dev (001B-a vedettes + 001B-b coffret)
001B-c /promotions → P2 hors ticket initial
Bloc producteurs home → renommer CK-HOME-002 ou CK-HOME-PRODUCERS-001
```

---

*Note MOA — C-Kréyòl Marketone · Cadrage CK-HOME-001B — 2 juillet 2026*
