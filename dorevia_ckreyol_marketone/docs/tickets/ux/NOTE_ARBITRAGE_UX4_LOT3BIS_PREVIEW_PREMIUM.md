# Note d’arbitrage MOA — UX-4 Lot 3bis · Finition visuelle premium preview

| Champ | Valeur |
|-------|--------|
| **Statut** | **Validé MOA** — **GO arbitrage** (2026-05-22) |
| **Date** | 2026-05-22 |
| **Prérequis** | Lot 3 **GO fonctionnel figé** · version réf. **`19.0.15.13.2`** |
| **Ticket** | [`TICKET_MARKETONE_UX4_SHOP_IN_PLACE.md`](TICKET_MARKETONE_UX4_SHOP_IN_PLACE.md) |
| **Arbitrage Lot 3 (fonctionnel)** | [`NOTE_ARBITRAGE_UX4_LOT3_PREVIEW_VOIR.md`](NOTE_ARBITRAGE_UX4_LOT3_PREVIEW_VOIR.md) |
| **Recette cible** | § **V3bis** [`RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md`](../recette/ux/RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md) |
| **Version cible** | **`19.0.15.13.3`** |
| **Branche autorisée (post-note)** | `feat/marketone-ux4-lot3bis-preview-premium` |
| **PR cible** | `[CK][UX-4] Lot 3bis — Finition visuelle preview premium` |

---

## 1. Contexte et doctrine

### 1.1 — Lot 3 fonctionnel figé

Le Lot 3 est **validé fonctionnellement** sur **`19.0.15.13.2`** :

- preview in-page sans sortie de `/shop` ;
- fermeture recettée (G3.9 · L3.F · L3.M) ;
- panier / wishlist depuis preview ;
- photo / titre tuile inchangés ;
- mobile 390 px ;
- réserve **L3.V1** documentée.

**Le Lot 3bis ne rouvre pas le Lot 3 fonctionnel.**

### 1.2 — Motif MOA

Retour visuel post-recette : la preview est **techniquement conforme** mais **qualitativement insuffisante** pour l’univers C-Kreyol — ressenti « panneau technique » plutôt que « maison de sélection ».

### 1.3 — Objectif Lot 3bis

Améliorer la **qualité perçue** de la preview : mini-fiche courte **premium**, cohérente palette pastel CK, **sans changement de comportement**.

---

## 2. Périmètre validé MOA

### 2.1 — In (autorisé)

| Zone | Détail |
|------|--------|
| **SCSS** | Fichier principal `_shop_product_preview.scss` · tokens CK existants |
| **QWeb léger** | Wrappers · libellés · structure visuelle meta (chips) · simplification header |
| **Recette** | Section **V3bis** · captures visuelles · smoke non-régression fonctionnelle |
| **Version** | Bump patch **`19.0.15.13.3`** |

### 2.2 — Out (interdit — gel MOA)

| Hors scope | Motif |
|------------|--------|
| Modification **JS** (interactions preview / panier / wishlist) | Risque régression G3.6–G3.9 — **exception V3bis.12** § 10 |
| Modification **routes** / contrôleurs | Lot 3 figé |
| Changement comportement **panier / wishlist** | Lot 1–2 figés |
| Changement **photo / titre** tuile grille | Gel MOA Lot 3 |
| Changement **fallback** variante / configurable | L3.V1 |
| **Deep-link** preview · **configurateur** · modal | Arbitrage Lot 3 |
| Extension fonctionnelle contenu preview | Scope creep |
| Nouvelles couleurs hors tokens CK | Doctrine charte |

---

## 3. Arbitrages MOA figés

### 3.1 — Titre header preview

| Avant | Après MOA |
|-------|-------------|
| `Aperçu produit` | **`Découvrir le produit`** |

**Motif :** ton éditorial · cohérent « maison de sélection » · moins technique.

**Application :** header offcanvas desktop · toolbar mobile inline (libellé contextuel).

---

### 3.2 — Fermeture desktop

| Surface | Décision MOA |
|---------|-------------|
| **Desktop** | **Croix seule** — zone cliquable confortable (≥ 44×44 px) · `aria-label="Fermer l'aperçu"` conservé |
| **Desktop** | **Supprimer** le bouton texte `Fermer` redondant (ajouté en reprise G3.9) |
| **Mobile** | Conserver **Fermer** texte discret dans la toolbar inline |

**Vigilance :** la simplification visuelle **ne doit pas** dégrader G3.9.

**Non-régression fermeture obligatoire :**

- croix desktop ;
- ESC ;
- re-clic **Voir** ;
- **Fermer** mobile ;
- console sans erreur JS bloquante.

> **Implémentation :** QWeb + SCSS uniquement — **ne pas modifier** `marketone_shop_preview.js` sauf arbitrage MOA explicite.

---

### 3.3 — Image preview

| Option | Décision MOA |
|--------|-------------|
| **Cover** (plein cadre) | ❌ Rejeté |
| **Contain cadré** | ✅ **Retenu** |

**Motif :** catalogue hétérogène (packshot · lifestyle · détourés · alimentaire) — le `contain` dans un **cadre pastel maîtrisé** limite la masse visuelle sans couper les produits.

**Direction technique (SCSS) :**

- bloc média avec fond `$ck-bg-image-tile` ;
- padding interne 12–16 px ;
- `object-fit: contain` ;
- `max-height` / ratio contrôlé (ex. ~4:5 ou carré) ;
- radius 14 px aligné tuiles.

---

## 4. Direction DA validée

| Élément | Cible MOA |
|---------|-----------|
| Panneau offcanvas / inline | Fond **`$ck-bg-card-body`** · header **`$ck-bg-cream`** — pas blanc Bootstrap brut |
| Bordures / ombres | **`$ck-border-soft`** · ombre chaude légère (réf. tuiles UX-3) |
| Image | Cadre visuel · contain · respiration |
| Typo titre produit | Hiérarchie éditoriale · prix terracotta **`$ck-terracotta`** |
| Origines / Collections | **Chips ou labels pastel** (réf. UX-1 / `$ck-bg-green-mist` · `$ck-sauge-border`) |
| CTA panier | Plus **respirant** · pleine largeur recommandée |
| Wishlist | Mieux **intégrée** (alignement style overlay tuile) |
| Lien « Voir la fiche complète » | **Lien secondaire premium** — séparateur · marge · pas concurrence visuelle avec CTA panier |
| Respiration | Espacements verticaux généreux (`gap` 1.25–1.5 rem · padding body offcanvas) |
| Ressenti global | **Maison de sélection** — pas panneau admin / technique |

**Palette :** tokens existants [`_tokens_colors.scss`](../../static/src/scss/_tokens_colors.scss) uniquement.

---

## 5. Fichiers impactés (estimation)

| Fichier | Rôle |
|---------|------|
| `static/src/scss/_shop_product_preview.scss` | **Principal** — styles preview + offcanvas |
| `views/pages/shop_product_preview.xml` | Libellés · wrappers meta · suppression bouton Fermer desktop |
| `__manifest__.py` | Version `13.3` |
| `docs/recette/ux/RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md` | § V3bis |
| `docs/tickets/ux/TICKET_MARKETONE_UX4_SHOP_IN_PLACE.md` | Référence Lot 3bis |

| `static/src/interactions/marketone_shop_preview.js` | **V3bis.12** — retrait naturel clic / scroll hors preview |

---

## 6. Risques et mitigations

| Risque | Niveau | Mitigation |
|--------|--------|------------|
| Régression **G3.9** fermeture | Moyen | Ne pas toucher JS · classes `.marketone-shop-preview-offcanvas__close` et `.marketone-shop-preview__close` conservées · recette L3.F / L3.M |
| Régression panier / wishlist | Faible | Classes handlers inchangées · SCSS conteneurs only |
| Image lifestyle « petite » en contain | Faible | Cadre + fond tile · recette packshot + lifestyle |
| Mobile 390 px débordement | Moyen | Recette V3bis + L3.M · pas de largeurs fixes |
| Scope creep mini-fiche | Élevé | Checklist § 2.2 · pas de merge sans MOA visuel |
| Remise en cause GO Lot 3 | Élevé | Lot 3bis isolé · version patch · doctrine § 1 |

---

## 7. Recette MOA Lot 3bis

### 7.1 — Recette visuelle V3bis

Voir [`RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md`](../recette/ux/RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md) § **Lot 3bis — V3bis**.

### 7.2 — Non-régression fonctionnelle (smoke obligatoire)

| Critère | Référence |
|---------|-----------|
| Fermeture preview | **G3.9** · **L3.F** · **L3.M** |
| Panier / wishlist / fiche | **G3.6–G3.8** |
| URL `/shop` | **G3.1** |
| Mobile 390 px | **G3.3** · **L3.M1** |
| Console | **L3.F11** · **L3.M6** |

### 7.3 — Captures attendues

| ID | Sujet |
|----|-------|
| C-V3bis-1 | Desktop — preview ouverte |
| C-V3bis-2 | Desktop — preview fermée |
| C-V3bis-3 | Mobile 390 px — preview ouverte |
| C-V3bis-4 | Mobile 390 px — preview fermée |
| C-V3bis-5 | Produit **packshot** |
| C-V3bis-6 | Produit **lifestyle** (si disponible) |

---

## 8. Méthode et règles de merge

| Étape | Règle |
|-------|-------|
| 1 | Note arbitrage MOA (ce document) — **validée** |
| 2 | Recette § V3bis — **à jour** |
| 3 | Branche `feat/marketone-ux4-lot3bis-preview-premium` |
| 4 | PR `[CK][UX-4] Lot 3bis — Finition visuelle preview premium` |
| 5 | Recette MOA desktop + mobile |
| 6 | **Pas de merge** sans validation visuelle MOA |

**Estimation :** ~½ journée · diff cible **< 200 lignes** · SCSS-majoritaire.

---

## 9. Verdict arbitrage

| Verdict | Condition |
|---------|-----------|
| **GO MOA Lot 3bis** | Arbitrage validé · recette V3bis définie · branche autorisée |
| **GO visuel Lot 3bis** | V3bis OK · smoke fonctionnel OK · captures MOA |
| **NO GO** | Régression G3.6–G3.9 · scope creep · remise en cause Lot 3 |

**Verdict MOA (2026-05-22) :** **GO arbitrage Lot 3bis** — passe visuelle complémentaire · **GO fonctionnel Lot 3 inchangé** sur `19.0.15.13.2`.

**Réserve maintenue :** **L3.V1** — hors périmètre 3bis.

---

## 10. Micro-arbitrage MOA — Retrait naturel preview (V3bis.12)

| Champ | Valeur |
|-------|--------|
| **Statut** | **Validé Dev** — en attente recette MOA (2026-05-22) |
| **Contexte** | GO visuel Lot 3bis `13.3` avec réserve R1 · **GO final suspendu** |
| **Version cible** | **`19.0.15.13.4`** |

### 10.1 — Problème MOA

La preview desktop peut rester ouverte comme un **tiroir permanent** alors que l’utilisateur reprend la navigation boutique (grille, filtres, scroll).

### 10.2 — Solution retenue (la plus légère)

| Déclencheur | Comportement | Modal ? |
|-------------|--------------|---------|
| **Clic hors preview** | Fermeture via `_closeAll()` | Non — pas de backdrop |
| **Scroll hors preview** | Fermeture si scroll page / grille | Non |
| **Clic dans preview** | Maintien ouvert | — |
| **Scroll dans preview** | Maintien ouvert (contenu long) | — |
| **Clic CTA Voir** | Logique existante (toggle / bascule produit) | — |

**Implémentation :** reprise **ciblée** de `marketone_shop_preview.js` uniquement.

| Listener | Phase | Rôle |
|----------|-------|------|
| `click` capture | capture | Bouton **Fermer** mobile (existant G3.9) |
| `click` | bubble | Clic hors `#marketone_shop_preview_offcanvas` · hors `.marketone-shop-preview` · hors `.marketone-shop-card-cta` |
| `scroll` | capture | Scroll hors panneau / preview inline |
| `keydown` Escape | — | Inchangé G3.9 |

**Zones exemptées du retrait :**

- offcanvas desktop (`#marketone_shop_preview_offcanvas`) ;
- fragment inline (`.marketone-shop-preview`) ;
- CTA **Voir** (`.marketone-shop-card-cta`) — évite conflit avec toggle / bascule produit.

### 10.3 — Exception périmètre « zéro JS »

| Avant arbitrage | Après V3bis.12 |
|-----------------|----------------|
| Lot 3bis = SCSS + QWeb uniquement | **Exception documentée** : JS limité à la **fermeture naturelle** |

**Hors scope de l’exception :** panier · wishlist · routes · photo/titre · fallback · deep-link · configurateur · modal/backdrop.

### 10.4 — Non-régression obligatoire

| Critère | Référence |
|---------|-----------|
| Fermeture explicite | **G3.9** · croix · ESC · re-clic Voir · Fermer mobile |
| Preview non modale | `data-bs-backdrop=false` · pas de trap focus |
| URL `/shop` | **G3.1** |
| Panier / wishlist preview | **G3.6–G3.7** inchangés |

### 10.5 — Recette MOA

§ **V3bis.12** · **V3bis.12-D1–D6** · **V3bis.12-M1–M6** dans [`RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md`](../recette/ux/RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md).

### 10.6 — Verdict micro-arbitrage

| Verdict | Condition |
|---------|-----------|
| **GO technique V3bis.12** | Implémentation légère · exception JS documentée · smoke G3.9 préservé |
| **GO final Lot 3bis** | V3bis.12 recetté MOA · pas de régression |

---

## 11. Historique

| Date | Événement |
|------|-----------|
| 2026-05-22 | Retour MOA visuel post-GO Lot 3 `13.2` |
| 2026-05-22 | Proposition Dev Lot 3bis — approche validée MOA |
| 2026-05-22 | Arbitrages figés : titre · fermeture · contain · direction DA |
| 2026-05-22 | **GO note arbitrage** — branche autorisée post-documentation |
| 2026-05-22 | GO visuel `13.3` avec réserve R1 mobile |
| 2026-05-22 | Micro-arbitrage **V3bis.12** retrait naturel · exception JS documentée · cible `13.4` |
