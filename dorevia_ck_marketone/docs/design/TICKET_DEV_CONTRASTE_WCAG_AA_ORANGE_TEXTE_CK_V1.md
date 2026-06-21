# Ticket Dev — Contraste WCAG AA · orange terracotta utilisé comme texte · V1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` · C-Kreyol / CK |
| **Module** | `dorevia_ck_theme` — `static/src/scss/` |
| **Type** | Accessibilité (WCAG 2.1 AA) · présentation · périmètre étroit |
| **Priorité** | Moyenne (conformité a11y) — **SCSS uniquement** |
| **Statut** | À exécuter |

```text
Le terracotta $ck-primary (#d84315) en TEXTE petite taille sur fond clair est à
4.31:1 — juste sous le seuil AA (4.5). Fix : token texte plus foncé #bf360c (5.44:1).
Aucun impact sur les boutons / badges (où #d84315 reste, en fond).
```

---

## 1. Constat (mesures réelles)

Contrastes mesurés sur la palette CK (fond crème `#fffbf7`, blanc `#ffffff`, `bg-soft #f5f0e8`) :

| Paire | Ratio | AA (texte normal 4.5 / grand 3.0) |
|---|---|---|
| Texte `#1c1917` / fond, muted `#57534e`, vert `#2e7d4f` | 5–17:1 | ✅ |
| Badge « Nouveau ! » (texte `#1a1a1a` / ambre `#f9a825`) | 8.87:1 | ✅ |
| Blanc / CTA orange `#d84315` (bouton, gras) | 4.44:1 | ✅ (grand/gras, seuil 3.0) |
| **Orange `#d84315` comme texte normal / fond clair** | **4.31:1** | ⚠️ **échoue (seuil 4.5)** |

**Seul écart réel** : `$ck-primary` quand il sert de **couleur de texte/lien en taille corps** sur fond clair.

**Token de remplacement validé** : `#bf360c` (= `$ck-primary-hover`) → **5.44:1** fond crème · **5.60:1** blanc · **4.94:1** bg-soft → AA OK partout.

---

## 2. Correctif

### Étape 1 — Ajouter un token texte accessible
Fichier : `dorevia_ck_theme/static/src/scss/primary_variables.scss`, juste après `$ck-primary-hover` :
```scss
// Orange accessible pour TEXTE / lien petite taille — 5.44:1 sur fond crème (WCAG AA).
// $ck-primary (#d84315) reste réservé : fonds de bouton, badges, icônes, grand/gras texte.
$ck-primary-text: $ck-primary-hover;   // #bf360c
```

### Étape 2 — `color: $ck-primary` → `color: $ck-primary-text`
**Uniquement** sur les usages **texte par défaut, petite taille, fond clair** :

| Fichier | Ligne | Élément | Action |
|---|---|---|---|
| `static/src/scss/product_card.scss` | **99** | `.card-cta` (« Voir le produit », 12px) | ✅ remplacer |
| `static/src/scss/product_page.scss` | **674** | `a { … }` (lien bloc complément) | ✅ remplacer |
| `static/src/scss/product_page.scss` | **810** | `.ck-product-page__pro-gateway-link` (« Espace professionnel CK ») | ✅ remplacer |
| `static/src/scss/product_card.scss` | **178** | texte orange dans le bloc à bordure | ⚠️ remplacer **si** texte normal par défaut (laisser si label de bouton gras/grand) |
| `static/src/scss/website.scss` | **460** | à identifier le sélecteur sur place | ⚠️ remplacer **si** lien/texte normal par défaut |

### Étape 3 (optionnelle) — états `:hover` / `:focus`
Les `color: $ck-primary` sous `&:hover` / `&:focus-visible` sont aussi à 4.31:1 :
`product_card.scss` 124, 257, 341 · `product_page.scss` 190, 316, 507, 586 · `website_header.scss` 150, 202, 276 · `website_sale.scss` 115.
L'orange survol est un parti pris assumé. **Pour du strict AA même au survol**, les passer aussi en `$ck-primary-text` ; sinon laisser (décision MOA).

---

## 3. Ne PAS toucher (déjà conformes)

- **Fonds** : tous les `background-color: $ck-primary` (`btn-primary`, `badge-heart`, badges panier header `my_cart_quantity`/`my_wish_quantity`…). C'est du fond + texte blanc/foncé → OK.
- **Grand / gras** : `website_header.scss:69` `.ck-header__brand-accent` (logo) · `website.scss:726` `a.fw-bold` (éditorial) → seuil 3.0, passent.
- **Badge « Nouveau ! »** : déjà en texte foncé `#1a1a1a` sur ambre (8.87:1) — ne pas modifier.

---

## 4. Contraintes

- **SCSS uniquement** (`primary_variables.scss` + remplacements `color:` ciblés).
- Pas de changement de logique, de QWeb, de fond de bouton, de badge.
- Ne pas régresser : cards Home/Boutique, fiche produit Lot 1/Lot 2, header.

---

## 5. Recette / acceptation

| Critère | Attendu |
|---|---|
| Token `$ck-primary-text` | Présent (`#bf360c`) |
| Liens/texte orange petite taille | Couleur `#bf360c` → contraste ≥ 4.5:1 |
| Boutons / badges / logo | Inchangés (`#d84315` en fond, badge texte foncé) |
| Mesure post-fix | `#bf360c` sur fond clair ≥ 4.5:1 (vérif via DevTools / outil contraste) |
| Non-régression | Cards, fiche Lot 1/2, header OK · mobile 390 OK |

---

*Ticket contraste WCAG AA · orange texte → `$ck-primary-text` (#bf360c) · SCSS thème CK.*
