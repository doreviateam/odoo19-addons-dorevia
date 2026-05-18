# TICKET — Lot 2.1 Design system minimal « Artisanal Terroir »

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_LOT2_1_DESIGN_SYSTEM_MINIMAL` |
| **Lot** | 2.1 — Design system minimal (jalon avant Lot 4) |
| **Statut** | **GO avec réserves** — recette visuelle MOA 2026-05-18 |
| **Version livrée** | `19.0.3.1.0` |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | GO Lots 1, 2, 3 |
| **Version cible module** | `19.0.3.1.0` (proposition) |
| **Référence design** | Stitch — **inspiration uniquement**, pas source technique |

---

## Objectif

Adapter la direction **Artisanal Terroir** à `dorevia_ckreyol_marketone` de manière **réaliste, sobre et compatible** Odoo 19 CE : tokens SCSS, règles UI, ajustements QWeb minimaux.

```text
Critère GO Lot 2.1 :
L’enveloppe globale du site ne donne plus l’impression d’un thème Odoo natif :
header, footer, boutons, tokens, home et shop portent une identité C-Kreyol cohérente,
sans altérer website_sale ni introduire de logique métier.
```

**Formule marque** :

```text
C-Kreyol = épicerie fine créole, sobre, chaleureuse, crédible.
```

---

## Contexte

| Élément | État actuel |
|---------|-------------|
| Lot 1 | Socle installable (`19.0.1.0.0`) |
| Lot 2 | Home `marketone-root`, tokens terracotta / Playfair+Inter (`19.0.2.0.0`) |
| Lot 3 | `/shop` `marketone-shop`, `_shop.scss` (`19.0.3.0.0`) |
| Problème visible | Header/footer Odoo génériques (`Your Logo`, `Contact Us`, `Useful Links`, contacts fictifs, `Powered by odoo`) |
| Legacy | `dorevia_ckreyol_marketplace` — **ne pas porter** |

**Pourquoi ce jalon avant Lot 4** : stabiliser la grammaire visuelle globale avant la fiche produit ; éviter d’empiler des styles page par page sur une enveloppe encore « Odoo natif ».

---

## Doctrine

```text
Odoo vend. Marketone présente, clarifie, oriente.
```

| Le Lot 2.1 modifie | Le Lot 2.1 ne modifie pas |
|--------------------|---------------------------|
| Tokens, typo, radius, boutons scoped | Catalogue, filtres, tri, domaines |
| Header / footer présentation | Panier, checkout, paiement |
| Home / shop (styles existants) | Prix, stock, disponibilité |
| Liens navigation visuels | Moteur `website_sale` |

**Stitch** : référence design (intention, proportions, couleurs) — **interdit** : copie HTML/CSS, framework externe, thème custom complet.

---

## Direction « Artisanal Terroir »

| Dimension | Intention |
|-----------|-----------|
| Ton | Épicerie fine créole / tropicale, artisanale, retail-ready |
| À viser | Terroir, sélection, chaleur, confiance, simplicité d’achat, élégance accessible |
| À éviter | Marketplace brouillon, cliché tropical excessif, luxe froid, Odoo natif trop visible |

---

## Périmètre inclus

### 1. Tokens SCSS

Mettre à jour / remplacer les tokens actuels (Lots 2–3) selon § couleurs, typo, espacements, radius.

| Fichier | Action |
|---------|--------|
| `_tokens_colors.scss` | Palette Artisanal Terroir (§7) |
| `_tokens_typography.scss` | EB Garamond + Hanken Grotesk (§8–9) |
| `_tokens_spacing.scss` | Échelle simplifiée (§10) |
| `_tokens_radius.scss` | **Créer** si absent (§11) |

**Règle** : un token n’existe que s’il est utilisé dans le socle Marketone.

### 2. Composants SCSS

| Fichier | Action | Scope |
|---------|--------|-------|
| `_buttons.scss` | **Créer** — primaire / secondaire (§12) | `.marketone-root`, `.marketone-shop`, scope header/footer explicite |
| `_header.scss` | **Créer** — habillage léger (§13) | Header site |
| `_footer.scss` | **Créer** — footer Option A clair (§14) | Footer site |
| `_layout.scss` | Adapter | `.marketone-root` |
| `_home.scss` | Adapter nouveaux tokens | `.marketone-root` |
| `_shop.scss` | Adapter nouveaux tokens | `.marketone-shop` |

### 3. Polices (`website_layout.xml`)

Remplacer Playfair / Inter par :

```text
EB Garamond — titres éditoriaux
Hanken Grotesk — body, nav, prix, boutons, footer
```

- Google Fonts **provisoire** (comme Lot 2) — documenter dans ADR-017.
- Évolution possible : self-host Lot 2.2 (hors ce ticket).

### 4. QWeb minimal (header / footer)

| Fichier | Créer seulement si SCSS + BO insuffisants |
|---------|-------------------------------------------|
| `views/layout/header.xml` | Logo texte `C-Kreyol`, neutralisation libellés génériques |
| `views/layout/footer.xml` | Footer sobre C-Kreyol (contenu §14) |

**Approche recommandée** :

1. Tenter configuration BO (`website`, menus, footer blocks) + SCSS.
2. QWeb **minimal** (xpath `attributes`, `replace` ciblé sur blocs footer génériques) — pas de `replace` massif de `website.layout`.

**Header — à traiter**

- `Your Logo` → `C-Kreyol` (texte provisoire si pas d’image logo)
- Bouton `Contact Us` harmonisé palette
- Liens navigation cohérents
- **Conserver** : panier, recherche, connexion, lien `/shop`

**Footer — à traiter**

Remplacer / neutraliser :

- `Useful Links`, `About us`
- `info@yourcompany.example.com`, `+1 555-555-5556`
- `Copyright © Company name` → `© C-Kreyol`
- `Powered by odoo` — masquer si périmètre légal/licence Odoo le permet ; sinon ADR + réserve GO

**Contenu footer minimal (proposition MOA)**

```text
C-Kreyol
Épicerie fine créole — produits sélectionnés avec soin.

Boutique : Accueil · Boutique · Contact

Confiance :
- Commande simple en ligne
- Service client à votre écoute
- Paiement sécurisé

Contact : (à compléter)
```

**Style footer** : **Option A** — fond ivoire / `surface-container`, texte charbon, bordure supérieure sable. Option B (footer sombre) **reportée**.

### 5. Home (existant)

Adapter styles Lot 2 — **pas** de nouvelle section lourde.

| Élément | Contenu conservé |
|---------|------------------|
| Sur-titre | Épicerie fine créole |
| H1 | C-Kreyol |
| Accroche | Une sélection sobre et soignée… |
| CTA | Découvrir la boutique → `/shop` |
| Réassurance | 3 puces actuelles |

Styles : H1 EB Garamond, CTA `#884523`, fond `#fff8f5`, surfaces réassurance douces.

### 6. Shop (existant Lot 3)

Adapter `_shop.scss` aux nouveaux tokens :

- cartes, bordures sable, titres/prix lisibles, CTA harmonisés ;
- **aucune** nouvelle classe hors `marketone-shop` ;
- **aucune** logique catalogue.

### 7. Manifeste et assets

Ordre bundle proposé :

```text
_tokens_colors.scss
_tokens_typography.scss
_tokens_spacing.scss
_tokens_radius.scss
_layout.scss
_buttons.scss
_header.scss
_footer.scss
_home.scss
_shop.scss
marketone.scss
```

Mettre à jour `__manifest__.py` : version `19.0.3.1.0`, fichiers `data` si header/footer QWeb créés.

**Aucun JS.**

### 8. Tests

| Tag | Fichier |
|-----|---------|
| `dorevia_marketone_lot2_1` | `tests/test_marketone_lot2_1_design.py` (nom proposé) |

**Tests proposés** (HttpCase, `post_install`) — éviter fragilité DOM excessive :

1. `/` → 200
2. `/shop` → 200
3. Home contient `marketone-root`
4. Shop contient `marketone-shop`
5. Header ou body contient marque `C-Kreyol` (logo texte)
6. Footer **ne contient plus** (si QWeb appliqué) : `About us`, `Useful Links`, `info@yourcompany.example.com`, `+1 555-555-5556`
7. Modules interdits non installés (marketplace, theme_classic_store, wishlist, comparison)
8. Non-régression : `dorevia_marketone_smoke`, `dorevia_marketone_lot2`, `dorevia_marketone_lot3`

### 9. Documentation

| Document | Action |
|----------|--------|
| `cadrage/DECISIONS.md` | ADR-017 (après livraison) |
| `pilotage/ROADMAP.md` | Insérer Lot 2.1 avant Lot 4 |
| `recette/ENV_REFERENCE.md` | Commandes test `dorevia_marketone_lot2_1` |
| `docs/README.md` | Ligne ticket |

---

## Hors périmètre

| Exclusion |
|-----------|
| Mega-menu, menu mobile custom JS |
| Portes catalogue, chips, filtres métier, `_search_get_detail` |
| Fiche produit (`marketone-product`) — **Lot 4** |
| Panier / checkout — **Lot 5** |
| Badges « Organic », « Fair Trade », « New » sans données BO |
| Trust badges paiement/livraison avancés |
| JS, contrôleur, modèle |
| Thème tiers, dépendances optionnelles |
| Seed produit XML |
| Portage Stitch HTML/CSS brut |
| Portage legacy `ckr_*` |
| Refonte checkout |
| Palette Material-like complète (tokens fixed non utilisés) |

---

## Spécification tokens — couleurs (§7)

```scss
// Core — Artisanal Terroir
$marketone-primary: #884523;
$marketone-primary-container: #a65d39;
$marketone-secondary: #4c6547;
$marketone-secondary-container: #cbe8c2;

$marketone-bg: #fff8f5;
$marketone-bg-soft: #fbf2ed;
$marketone-surface: #ffffff;
$marketone-surface-container: #f5ece7;
$marketone-surface-container-high: #efe6e2;

$marketone-text: #1e1b18;
$marketone-text-muted: #54433c;
$marketone-text-inverse: #f8efea;

$marketone-border: #d9c2b8;
$marketone-outline: #86736b;

$marketone-error: #ba1a1a;
```

**Ne pas intégrer** : `primary-fixed`, `secondary-fixed`, `tertiary-fixed`, `inverse-primary`, `surface-container-lowest/highest`, etc.

**Compatibilité** : remapper les anciennes variables Lot 2 (`$marketone-primary: #a0522d`, etc.) — pas de double palette.

---

## Spécification tokens — typographie (§8–9)

```scss
$marketone-font-heading: "EB Garamond", Georgia, serif;
$marketone-font-body: "Hanken Grotesk", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;

$marketone-h1-mobile: 2rem;
$marketone-h1-desktop: 3rem;
$marketone-h2-mobile: 1.6rem;
$marketone-h2-desktop: 2rem;

$marketone-body: 1rem;
$marketone-body-lg: 1.125rem;
$marketone-label: 0.875rem;
$marketone-label-sm: 0.75rem;
```

**Usage** : EB Garamond → H1, H2, titres éditoriaux, noms produits carte si pertinent ; Hanken Grotesk → body, nav, boutons, prix, labels, footer.

---

## Spécification tokens — espacements (§10)

```scss
$marketone-space-xs: 0.5rem;
$marketone-space-sm: 1rem;
$marketone-space-md: 1.5rem;
$marketone-space-lg: 3rem;
$marketone-space-xl: 5rem;

$marketone-container-max: 1280px;
$marketone-gutter: 1.25rem;
```

Pas de grille custom — respecter Bootstrap / Odoo.

---

## Spécification tokens — radius (§11)

```scss
$marketone-radius-sm: 0.25rem;
$marketone-radius-md: 0.5rem;
$marketone-radius-lg: 0.75rem;
$marketone-radius-pill: 9999px;
```

| Usage | Radius |
|-------|--------|
| Boutons | pill ou md |
| Cartes produit | md |
| Blocs éditoriaux | lg |
| Inputs | sm ou md |

---

## Spécification boutons (§12)

Sous scope `.marketone-root`, `.marketone-shop`, et scope header/footer **explicite** (classe dédiée si nécessaire, ex. `.marketone-chrome`).

**Primaire** : fond `$marketone-primary`, texte blanc, radius pill, weight 600, hover `$marketone-primary-container`.

**Secondaire** : transparent, border `$marketone-border`, texte `$marketone-text`, hover fond `$marketone-bg-soft`.

**Interdit** :

```scss
.btn-primary { /* global non scopé */ }
```

sauf exception documentée dans ADR (objectif : zéro).

---

## Fichiers — matrice réelle (ne pas créer de vides)

| Fichier | Obligatoire Lot 2.1 |
|---------|---------------------|
| `_tokens_colors.scss` | Oui — mise à jour |
| `_tokens_typography.scss` | Oui — mise à jour |
| `_tokens_spacing.scss` | Oui — mise à jour |
| `_tokens_radius.scss` | Oui — création |
| `_buttons.scss` | Oui — création |
| `_header.scss` | Oui — création |
| `_footer.scss` | Oui — création |
| `_layout.scss`, `_home.scss`, `_shop.scss` | Oui — adaptation |
| `views/layout/website_layout.xml` | Oui — polices |
| `views/layout/header.xml` | **Si nécessaire** — justifier en PR |
| `views/layout/footer.xml` | **Si nécessaire** — justifier en PR |
| `marketone.scss` | Point d’entrée (peut rester commentaire) |

---

## Risques

| Risque | Mitigation |
|--------|------------|
| Surcharge globale `.btn` / `header` | Scope strict ; pas de règles hors classes Marketone |
| XPath footer fragile | Tests texte critique ; xpath ciblés |
| `Powered by odoo` non supprimable | GO avec réserve + ADR |
| Régression Lots 2–3 | Tests smoke + lot2 + lot3 obligatoires |
| Google Fonts / RGPD | ADR provisoire ; Lot 2.2 self-host optionnel |
| Logo image absent | Logo texte `C-Kreyol` — réserve acceptée |

---

## Critères GO / NO GO

### GO

- [ ] Enveloppe plus C-Kreyol, moins « Odoo natif »
- [ ] Header : marque `C-Kreyol`, panier / recherche / login / `/shop` OK
- [ ] Footer générique remplacé ou neutralisé
- [ ] Home et shop cohérents avec nouveaux tokens
- [ ] `/` et `/shop` → 200
- [ ] Tests smoke + lot2 + lot3 + lot2_1 verts
- [ ] Aucun module interdit, aucune dépendance ajoutée, aucun JS

### GO avec réserves

- [ ] Logo texte provisoire
- [ ] Contact footer « à compléter »
- [ ] Google Fonts provisoire
- [ ] `Powered by odoo` encore visible (contrainte licence)

### NO GO

- [ ] 500 sur `/` ou `/shop`
- [ ] Header casse panier / recherche / connexion
- [ ] Footer encore plein de contenus Odoo génériques
- [ ] Styles fuient vers checkout / BO
- [ ] Portes, mega-menu, JS, contrôleur, modèle
- [ ] Copie HTML Stitch ou thème parallèle

---

## Commandes de validation

```bash
# Depuis le repo addons (ou sandbox)
cd ../sandbox-odoo19 && docker compose exec odoo odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init \
  && docker compose restart odoo

# Tests (port 8071 si daemon actif sur 8069)
docker compose exec odoo odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_smoke,dorevia_marketone_lot2,dorevia_marketone_lot3,dorevia_marketone_lot2_1 \
  --http-port=8071

# HTTP
curl -sS -o /dev/null -w '%{http_code}\n' \
  -H 'X-Odoo-Database: ckr-marketone-01' http://localhost:18079/
curl -sS -o /dev/null -w '%{http_code}\n' \
  -H 'X-Odoo-Database: ckr-marketone-01' http://localhost:18079/shop
```

---

## Recette visuelle (humaine)

Base **`ckr-marketone-01`** — http://localhost:18079

| Route | Points d’attention |
|-------|-------------------|
| `/` | Header C-Kreyol, home ivoire/terracotta, footer sobre, pas de scroll horizontal mobile |
| `/shop` | Cohérence avec home, cartes lisibles, filtres/tri/pagination natifs OK |

Checklist :

- [ ] Plus de `Your Logo` dominant
- [ ] Plus de contacts fictifs Odoo
- [ ] Plus de `Useful Links` / `About us` génériques (si ticket exécuté)
- [ ] Panier, recherche, connexion accessibles

---

## ADR attendue (après exécution)

```text
ADR-017 — Adoption du design system minimal Artisanal Terroir
```

Contenu :

- Stitch = référence design, pas source technique ;
- tokens/principes utiles uniquement ;
- pas de framework externe ;
- Google Fonts provisoire, self-host possible Lot 2.2 ;
- header/footer minimaux ;
- `website_sale` souverain.

---

## Positionnement roadmap

```text
Lot 0 → Lot 1 → Lot 2 → Lot 3 → Lot 2.1 (ce ticket) → Lot 4 → Lot 5 → Lot 6
```

Le Lot 2.1 **réaligne** les livrables 2 et 3 sans changer leur périmètre fonctionnel.

**Lot 4** : débloqué pour préparation ticket — exécution après validation humaine du ticket Lot 4.

---

## Résultats automatises (2026-05-18)

| Commande | Résultat |
|----------|----------|
| `-u dorevia_ckreyol_marketone` | OK (v `19.0.3.1.0`) |
| Tests smoke + lot2 + lot2_1 + lot3 | **30/30** OK |

---

## Recette visuelle MOA (2026-05-18)

### Points validés

- Enveloppe globale ne fait plus Odoo natif
- Header sobre et cohérent C-Kreyol ; logo texte `C-Kreyol` accepté provisoirement
- Home propre, respirante, Artisanal Terroir ; CTA terracotta cohérent
- Footer C-Kreyol nettement meilleur que footer Odoo standard
- `/shop` cohérent visuellement avec la home
- Aucune dégradation visible majeure
- Panier, recherche, connexion et navigation accessibles

### Réserves acceptées

1. **`/shop` visuellement pauvre** sans produits en BO — prévoir **2 à 3 produits de recette en BO** pour valider les cartes (pas de seed XML module).
2. **Page Contact** (`/contactus`) reste Odoo native — ticket dédié futur « Contact minimal C-Kreyol » (hors Lot 2.1).
3. **Logo texte** `C-Kreyol` provisoire — wordmark à venir.
4. **Footer** : `Contact : à compléter` accepté en sandbox — à remplacer avant ouverture commerciale.

### Décision

```text
Décision : [x] GO avec réserves  [ ] GO  [ ] NO GO
Date : 2026-05-18
```

---

## Checklist validation humaine

```text
[x] Direction Artisanal Terroir validée
[x] Tokens couleur §7 acceptés
[x] Typographies EB Garamond + Hanken Grotesk acceptées
[x] Footer Option A (clair) validée
[x] Périmètre header/footer minimal accepté
[x] Hors périmètre (portes, Lot 4, JS) compris
[x] Réserve Google Fonts / logo texte / contact footer acceptées

Décision : [x] GO avec réserves  [ ] GO  [ ] NO GO
```

---

## Prochaine étape

Préparer / valider **`TICKET_MARKETONE_LOT4_PRODUCT`** — fiche produit (`marketone-product`), en conservant le niveau visuel Artisanal Terroir.
