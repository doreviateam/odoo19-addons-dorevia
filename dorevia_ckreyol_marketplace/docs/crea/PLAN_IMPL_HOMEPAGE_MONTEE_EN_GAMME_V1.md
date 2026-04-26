# PLAN D'IMPLÉMENTATION — Montée en gamme V1 homepage C-Kreyol

**Date** : 2026-04-23  
**Auteur** : implémentation front (session IA)  
**Statut** : **plan exécuté intégralement — V1 implémentée** (module `dorevia_ckreyol_marketplace` version **19.0.1.6.16**). Lots A + B + C appliqués (jusqu'à v.15), recette MOA passante ; **post-V1** patch v.16 : Ticket 1 clôturé — retrait `__subtitle-accent`, alignement Hero / gel `SPEC_HERO_HOMEPAGE.md` §7. Sujets reportés (hors Ticket 1 résolu) → [TICKETS_HORS_PERIMETRE_V1.md](TICKETS_HORS_PERIMETRE_V1.md).  
**Portée** : traduction opérationnelle du document créatif gelé, strictement V1, sans V1.1, sans changement d'architecture ni de logique métier.

**Document de référence (gelé)** :
- [PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md](PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md) — §9 Arbitrages gelés le 2026-04-23.

**Cadre doctrinal** :
- [ARCHITECTURE_DECISION_RECORD.md](../direction/ARCHITECTURE_DECISION_RECORD.md) (ADR-001, 002, 003, 005, 007, 008)
- [WIREFRAME_HOMEPAGE.md](../direction/WIREFRAME_HOMEPAGE.md)
- [SPEC_HERO_HOMEPAGE.md](../direction/SPEC_HERO_HOMEPAGE.md) (gel §7)
- [CHARTE_GRAPHIQUE_PHASE1.md](../direction/CHARTE_GRAPHIQUE_PHASE1.md) (Direction A gelée §3–§11)
- [DESIGN.md](../direction/DESIGN.md) §7

---

## 1. Compréhension

Appliquer la montée en gamme créative gelée sur la homepage existante, **sans** toucher à l'architecture (même ordre des blocs, mêmes snippets, mêmes routes), **sans** JS supplémentaire, **sans** V1.1.

### Traduction opérationnelle des arbitrages §9

| Arbitrage gelé | Traduction V1 |
|----------------|---------------|
| **§9.1** Hero 60/40 cible, 55/45 toléré, 50/50 exclu | `_hero.scss` : `grid-template-columns: 4fr 6fr` desktop (le content reste à gauche, le visuel à droite) |
| **§9.2** Supplier variante plane V1, sans chevauchement | `_supplier.scss` : `align-items: start` + filet amber 2 px sur eyebrow via modificateur `--rule` |
| **§9.3** Editorial variante sobre V1, pas de pleine largeur | Refonte complète `ckr_editorial.xml` + `_editorial.scss` en bandeau sobre centré |
| **§9.4** Carte produit ligne secondaire origine si couverture ≥ 80 % | Rendu statique V1 + commentaire QWeb documentant la règle pour la bascule V1.x sur donnée réelle |

### Fil rouge transverse
- Filet amber `1px × 48px` appliqué sur les eyebrows de section via modificateur `.ckr-section-title__eyebrow--rule`.
- Garde globale `prefers-reduced-motion` : toutes transitions / transformations désactivées.

### Ce qui n'est PAS touché
- Copy hero (gel SPEC §7).
- Structure et routes Explorer (ADR-007 / ADR-008).
- Assemblage `ckr_homepage.xml`.
- JS carrousel Explorer.
- Header, footer, portail, boutique, fiche produit.

---

## 2. Ajustements validés par le MOA (2026-04-23)

### 2.1 Selection — pas de `t-if` factice

Aucun `t-if="True"` en dur. En V1 statique, l'origine est **rendue explicitement** en contenu de carte. La classe `.ckr-selection__card__origin` sert de **point d'extension stable** pour la bascule V1.x sur donnée réelle. Règle §9.4 documentée par commentaire QWeb au-dessus de la ligne.

### 2.2 Explorer — suréligne « Porte 0x » exclue de V1

Tranchée par le MOA : **hors périmètre V1**. Rationnel : le §9 n'en fait pas un invariant, les cinq cartes sont déjà denses, on préfère itérer au vu de la V1 en situation réelle. Conséquence : `ckr_entries.xml` et `_entries.scss` **ne sont pas modifiés** dans ce ticket.

### 2.3 Selection responsive — garde-fou explicite

Titre + prix sur la même ligne sur toutes tailles d'écran ; le **prix ne se casse jamais**, le **titre absorbe toute contrainte de largeur** via ellipsis à 2 lignes. Pas de `flex-wrap` de secours (troncature propre plutôt que casse d'alignement).

### 2.4 Supplier — changement QWeb minimal confirmé

**Une seule classe** (`--rule`) ajoutée sur l'eyebrow existant. Aucun wrapper, aucune restructuration DOM. Le passage en plane est géré exclusivement en SCSS.

### 2.5 Lots — séparation nette validée

- **Lot A** : fil rouge transverse
- **Lot B** : Hero + Supplier + Selection
- **Lot C** : Editorial + Trust

### 2.6 Versionning — bump conservateur patch

Convention interne non connue avec certitude → bump **patch** par lot : `.12 → .13 → .14 → .15`. Le MOA validera si un saut mineur est préférable lors du Lot C.

---

## 3. Fichiers touchés — liste finale

### QWeb
- `views/snippets/ckr_supplier.xml` — ajout classe `--rule` sur l'eyebrow (1 ligne).
- `views/snippets/ckr_selection.xml` — wrap `<div class="__head">` autour de `h3` + `__price` + commentaire §9.4 + classe `--rule` sur titre de section.
- `views/snippets/ckr_editorial.xml` — **refonte complète** en bandeau sobre.
- `views/snippets/ckr_trust.xml` — classe `--rule` sur l'eyebrow (1 ligne).

### SCSS
- `static/src/scss/ckr_main.scss` — modificateur `.ckr-section-title__eyebrow--rule` + garde `prefers-reduced-motion`.
- `static/src/scss/components/_hero.scss` — grid 4fr/6fr desktop.
- `static/src/scss/components/_supplier.scss` — `align-items: start` + filet 2 px Supplier.
- `static/src/scss/components/_selection.scss` — garde-fou titre/prix + `:focus-visible` + transitions harmonisées.
- `static/src/scss/components/_editorial.scss` — réécriture bandeau sobre.
- `static/src/scss/components/_trust.scss` — icônes linéaires charcoal, suppression pilule.

### Manifeste
- `__manifest__.py` — bump version par lot (`.12 → .13 → .14 → .15`).

### Documents (après chaque lot)
- Entrée d'historique dans `docs/crea/PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md`.
- Éventuellement : entrée d'historique dans `docs/direction/WIREFRAME_HOMEPAGE.md` et `docs/direction/DESIGN.md` après Lot C (refonte Editorial → variante sobre = état V1).

### Fichiers NON touchés (confirmé)
- `views/snippets/ckr_hero.xml` (copy gelé SPEC §7)
- `views/snippets/ckr_entries.xml` (ajustement §2.2 : exclu V1)
- `views/pages/ckr_homepage.xml`
- `static/src/scss/components/_entries.scss`
- `static/src/scss/tokens/*.scss`
- `static/src/js/*.js`
- Tous les fichiers `views/layout/`, `views/portal/`, `views/auth/`, `views/pages/*` sauf homepage.

---

## 4. Séquencement — 3 lots

### Lot A — Fil rouge transverse
**Portée** : tokens / règles génériques + application visuelle du fil rouge sur toutes les sections.

**Actions** :
1. Ajout du modificateur `.ckr-section-title__eyebrow--rule` dans `ckr_main.scss`.
2. Ajout de la garde globale `@media (prefers-reduced-motion: reduce)` dans `ckr_main.scss`.
3. Application de la classe `--rule` sur les eyebrows : Supplier, Selection, Editorial, Trust.
4. Bump `__manifest__.py` → `19.0.1.6.13`.
5. `./odoo-bin -u dorevia_ckreyol_marketplace -d <db>` + hard-reload assets.
6. Smoke test visuel du fil rouge sur toutes les sections de la homepage.

**Critère de sortie** : le filet amber 1 px × 48 px signe les quatre sections concernées, aucune régression visuelle ailleurs.

---

### Lot B — Hero + Supplier + Selection (§9.1, §9.2, §9.4)
**Portée** : les trois blocs où l'arbitrage porte sur la composition ou la hiérarchie interne.

**Actions** :
1. `_hero.scss` : `grid-template-columns: 4fr 6fr` desktop (≥ 992 px).
2. `_supplier.scss` : `align-items: start` + filet amber 2 px sur eyebrow Supplier.
3. `_selection.scss` : garde-fou titre/prix (`flex-wrap: nowrap`, `min-width: 0` titre, `white-space: nowrap` prix, ellipsis 2 lignes), `:focus-visible` amber, transitions harmonisées.
4. `ckr_selection.xml` : wrap `<div class="ckr-selection__card__head">` autour de `h3` + `__price` + commentaire §9.4.
5. Bump `__manifest__.py` → `19.0.1.6.14`.
6. `-u` + hard-reload.
7. Smoke test desktop 1280 / 992 + mobile 375 / 390 / 768.

**Critère de sortie** : ratio hero 60/40 validable à l'œil en ≥ 992 px ; Supplier photo et texte alignés haut ; Selection titre + prix sur une ligne baseline, pas de casse même avec titre long.

---

### Lot C — Editorial + Trust (§9.3 + finition icônes)
**Portée** : le bloc à refondre + la finition icônes.

**Actions** :
1. `ckr_editorial.xml` : **refonte complète** en bandeau sobre (suréligne + phrase Playfair + lien amber, sans image de fond, sans overlay sombre).
2. `_editorial.scss` : **réécriture** (suppression de la logique dark-tile, ajout du bandeau centré).
3. `_trust.scss` : icônes linéaires charcoal, suppression de la pilule de fond.
4. Bump `__manifest__.py` → `19.0.1.6.15`.
5. `-u` + hard-reload.
6. Recette complète (voir §8).

**Critère de sortie** : Editorial est un bandeau sobre conforme §9.3 ; Trust utilise des icônes linéaires charcoal ; recette §8 passante.

---

### Ordre des lots — justification

- **A → B → C** va du moins risqué (règles génériques) au plus structurel (refonte Editorial).
- Chaque lot est **livrable et recettable indépendamment** : un rollback de C ne casse ni B ni A.
- Le lot C contient le seul changement structurel significatif (refonte Editorial) → isolé en fin de chaîne, plus facile à reverter si besoin.

---

## 5. Patchs QWeb

### 5.1 `views/snippets/ckr_supplier.xml` (Lot A)

```xml
<!-- AVANT -->
<span class="ckr-section-title__eyebrow">Origines reelles</span>

<!-- APRES -->
<span class="ckr-section-title__eyebrow ckr-section-title__eyebrow--rule">Origines reelles</span>
```

### 5.2 `views/snippets/ckr_trust.xml` (Lot A)

```xml
<!-- AVANT -->
<header class="ckr-section-title">
    <span class="ckr-section-title__eyebrow">Engagements</span>
    <h2>Acheter en confiance</h2>
</header>

<!-- APRES -->
<header class="ckr-section-title">
    <span class="ckr-section-title__eyebrow ckr-section-title__eyebrow--rule">Engagements</span>
    <h2>Acheter en confiance</h2>
</header>
```

### 5.3 `views/snippets/ckr_selection.xml` (Lots A + B)

```xml
<header class="ckr-section-title">
    <span class="ckr-section-title__eyebrow ckr-section-title__eyebrow--rule">Selection</span>
    <h2>Quelques produits reperes</h2>
</header>

<div class="ckr-selection__grid">

    <a href="/shop" class="ckr-selection__card">
        <div class="ckr-selection__card__img">
            <img src="/dorevia_ckreyol_marketplace/static/src/img/packshot_maniocookies.png"
                 alt="Maniocookies - biscuits au manioc"/>
        </div>
        <div class="ckr-selection__card__head">
            <h3>Maniocookies</h3>
            <span class="ckr-selection__card__price">Voir en boutique</span>
        </div>
        <!--
            V1 : origine rendue en statique (placeholder homepage).
            V1.x (bascule donnee reelle) : remplacer ce <p> par un rendu
            conditionnel t-if="product.x_ckr_origin" + verification de
            couverture globale >= 80 % sur la selection (regle §9.4 du
            document gele), pilotee au niveau du template parent ou du
            controleur qui resout la selection. Si couverture < 80 %,
            masquer la ligne sur TOUTES les cartes - jamais de melange.
        -->
        <p class="ckr-selection__card__origin">Guadeloupe</p>
    </a>

    <!-- Idem pour les 3 autres cartes avec la meme structure __head + commentaire + __origin en statique -->

</div>
```

### 5.4 `views/snippets/ckr_editorial.xml` (Lot C — refonte)

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <!-- ========================================================== -->
    <!-- Snippet : Bloc 6 - Bloc editorial (variante SOBRE V1)      -->
    <!-- Gel §9.3 du 2026-04-23 - PROPOSITION_HOMEPAGE_MONTEE_EN_    -->
    <!-- GAMME_V1.md. La variante pleine largeur reste documentee    -->
    <!-- pour V1.1 sous 3 conditions cumulees :                      -->
    <!--   - contenu nommable (collection / saison / cadeau actif)   -->
    <!--   - visuel paysage 21:9 dedie produit ou recadre            -->
    <!--   - phrase d accroche validee par le responsable marque     -->
    <!-- ========================================================== -->

    <template id="ckr_snippet_editorial" name="C-Kreyol: Bloc editorial (sobre V1)">
        <section class="ckr-section ckr-editorial ckr-root">
            <div class="ckr-container">

                <div class="ckr-editorial__bandeau">
                    <span class="ckr-editorial__eyebrow">Collection</span>
                    <p class="ckr-editorial__line">
                        Des selections courtes, par saison ou par usage —
                        pour decouvrir l offre sans la parcourir en entier.
                    </p>
                    <a href="/collections" class="ckr-editorial__link">
                        Voir les collections &#8594;
                    </a>
                </div>

            </div>
        </section>
    </template>

</odoo>
```

---

## 6. Patchs SCSS

### 6.1 `static/src/scss/ckr_main.scss` (Lot A)

Ajout à la fin du fichier (après la section `.ckr-section-title--center`) :

```scss
// --- Filet amber sur l eyebrow de section (fil rouge V1 - §9 PROPOSITION_
// HOMEPAGE_MONTEE_EN_GAMME_V1.md) -----------------------------------------
.ckr-section-title__eyebrow--rule {
    position: relative;
    display: inline-block;
    padding-top: calc(#{$ckr-space-sm} + 2px);

    &::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 48px;
        height: 1px;
        background-color: $ckr-accent;
    }
}

// Centrage du filet dans un .ckr-section-title--center
.ckr-section-title--center .ckr-section-title__eyebrow--rule::before {
    left: 50%;
    transform: translateX(-50%);
}

// --- Garde prefers-reduced-motion : desactive toutes les transitions
// et transformations sur les racines C-Kreyol. Respecte strictement
// le contrat WCAG 2.1 SC 2.3.3 et la doctrine §4 accessibilite.
@media (prefers-reduced-motion: reduce) {
    .ckr-root *,
    .ckr-page * {
        transition-duration: 0.01ms !important;
        animation-duration: 0.01ms !important;
        transform: none !important;
    }
}
```

### 6.2 `static/src/scss/components/_hero.scss` (Lot B — §9.1)

```scss
&__inner {
    // ... existant inchange jusqu a @media

    @media (min-width: 992px) {
        grid-template-columns: 4fr 6fr;   // 60/40 cible §9.1 (remplace 1.05fr 1fr)
        align-items: center;
        gap: $ckr-space-3xl;
    }
}
```

**Note §9.1** : en cas de contenu long à l'impl. réelle, tolérance gelée 55/45 = `grid-template-columns: 4.5fr 5.5fr` (ou `9fr 11fr`). 50/50 exclu doctrinalement.

### 6.3 `static/src/scss/components/_supplier.scss` (Lot B — §9.2)

```scss
.ckr-supplier {
    background-color: $ckr-bg-soft;

    &__inner {
        display: grid;
        grid-template-columns: 1fr;
        gap: $ckr-space-xl;
        align-items: start;   // <-- change : plane V1 §9.2 (etait center)

        @media (min-width: 992px) {
            grid-template-columns: 1fr 1.1fr;
            gap: $ckr-space-3xl;
            align-items: start;
        }
    }

    // ... __visual inchange

    &__content {
        // Micro-accent de presence §9.2 : filet amber 2 px au-dessus de l eyebrow.
        // Un cran plus appuye que le filet 1 px des autres sections pour signer
        // le bloc sans le gonfler, cohérent avec l intention "partenaire artisan
        // credible sans vitrine".
        .ckr-section-title__eyebrow--rule {
            &::before {
                height: 2px;
            }
        }

        h2 {
            margin-top: 0;
            margin-bottom: $ckr-space-md;
        }

        p {
            line-height: 1.6;
            margin-bottom: $ckr-space-md;
        }

        strong {
            color: $ckr-primary;
            font-weight: $ckr-weight-semibold;
        }
    }
}
```

### 6.4 `static/src/scss/components/_selection.scss` (Lot B — §9.4 + garde-fou)

```scss
.ckr-selection {
    &__grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: $ckr-space-md;

        @media (min-width: 768px) {
            grid-template-columns: repeat(4, 1fr);
            gap: $ckr-space-lg;
        }
    }

    &__card {
        display: flex;
        flex-direction: column;
        gap: $ckr-space-sm;
        background-color: $ckr-bg;
        border: 1px solid $ckr-border;
        border-radius: $ckr-radius-md;
        padding: $ckr-space-md;
        text-decoration: none;
        color: $ckr-text;
        transition: border-color $ckr-transition-fast,
                    box-shadow $ckr-transition-base,
                    transform $ckr-transition-fast;

        &:hover {
            border-color: $ckr-accent;
            box-shadow: $ckr-shadow-sm;
            transform: translateY(-2px);
            color: $ckr-text;
            text-decoration: none;
        }

        // Focus visible clavier : duplique le hover + outline amber.
        &:focus-visible {
            outline: 2px solid $ckr-accent;
            outline-offset: 2px;
            border-color: $ckr-accent;
            box-shadow: $ckr-shadow-sm;
            transform: translateY(-2px);
            text-decoration: none;
        }

        &__img {
            width: 100%;
            aspect-ratio: unquote("1 / 1");
            background-color: $ckr-bg-soft;
            border-radius: $ckr-radius-sm;
            overflow: hidden;

            img {
                width: 100%;
                height: 100%;
                object-fit: cover;
                display: block;
            }
        }

        // Garde-fou titre / prix (§3 ajustement MOA 2026-04-23) :
        // titre + prix sur UNE seule ligne baseline, le prix ne casse jamais,
        // le titre absorbe la contrainte de largeur via ellipsis 2 lignes.
        &__head {
            display: flex;
            flex-wrap: nowrap;
            justify-content: space-between;
            align-items: baseline;
            gap: $ckr-space-sm;
            min-width: 0;
        }

        h3 {
            margin: 0;
            min-width: 0;   // cle pour que text-overflow fonctionne dans un flex child
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            flex: 1 1 auto;
            font-family: $ckr-font-serif;
            font-size: 1.05rem;
            font-weight: $ckr-weight-semibold;
            color: $ckr-text;
        }

        &__origin {
            font-size: 0.8rem;
            letter-spacing: 0.02em;
            color: $ckr-secondary;
            margin: 0;
        }

        &__price {
            font-family: $ckr-font-sans;
            font-weight: $ckr-weight-semibold;
            color: $ckr-primary;
            margin: 0;
            white-space: nowrap;   // le prix n est jamais cesure
            flex: 0 0 auto;        // ne retrecit pas
        }
    }

    &__cta {
        text-align: center;
        margin-top: $ckr-space-xl;
    }
}
```

### 6.5 `static/src/scss/components/_editorial.scss` (Lot C — §9.3, réécriture)

```scss
// ============================================================================
// C-Kreyol - Bloc 6 : Bloc editorial (variante SOBRE V1)
// Gel §9.3 du 2026-04-23 - PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md
//
// Bandeau centre : surÉligne sauge + phrase Playfair + lien souligne amber.
// Pas d image de fond, pas d overlay sombre, pas de tuiles multiples.
//
// La variante pleine largeur (ex-dark-overlay grid) est archivee et reste
// documentee pour V1.1 sous 3 conditions cumulees (contenu nommable,
// visuel 21:9 dedie, phrase validee marque).
// ============================================================================

.ckr-editorial {
    background-color: $ckr-bg;

    &__bandeau {
        max-width: 720px;
        margin: 0 auto;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: $ckr-space-sm;
    }

    &__eyebrow {
        font-family: $ckr-font-sans;
        font-size: 0.85rem;
        font-weight: $ckr-weight-medium;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: $ckr-secondary;
        position: relative;
        padding-top: calc(#{$ckr-space-sm} + 2px);

        &::before {
            content: "";
            position: absolute;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 48px;
            height: 1px;
            background-color: $ckr-accent;
        }
    }

    &__line {
        font-family: $ckr-font-serif;
        font-size: unquote("clamp(1.15rem, 2vw, 1.5rem)");
        line-height: 1.4;
        color: $ckr-text;
        margin: 0;
        max-width: 42ch;
    }

    &__link {
        font-family: $ckr-font-sans;
        font-size: 0.95rem;
        font-weight: $ckr-weight-medium;
        color: $ckr-primary;
        text-decoration: underline;
        text-decoration-color: $ckr-accent;
        text-underline-offset: 4px;
        transition: color $ckr-transition-fast,
                    text-decoration-color $ckr-transition-fast;

        &:hover,
        &:focus-visible {
            color: $ckr-primary-dark;
            text-decoration-color: $ckr-primary-dark;
        }

        &:focus-visible {
            outline: 2px solid $ckr-accent;
            outline-offset: 3px;
            border-radius: 2px;
        }
    }
}
```

### 6.6 `static/src/scss/components/_trust.scss` (Lot C)

```scss
.ckr-trust {
    background-color: $ckr-bg;

    &__grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: $ckr-space-xl;

        @media (min-width: 768px) {
            grid-template-columns: repeat(3, 1fr);
        }
    }

    &__item {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: $ckr-space-sm;

        // Icone lineaire charcoal (§9 fil rouge V1) - remplace la pilule
        // ambree qui passait "icon-badge" au lieu de "sobre Direction A".
        &__icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            background-color: transparent;
            color: $ckr-text;
            font-size: 1.35rem;
            margin-bottom: $ckr-space-sm;
            border-radius: 0;
        }

        h3 {
            font-family: $ckr-font-serif;
            font-size: 1.25rem;
            font-weight: $ckr-weight-semibold;
            margin: 0;
            color: $ckr-text;
        }

        p {
            margin: 0;
            line-height: 1.55;
            color: $ckr-text-muted;
            font-size: 0.95rem;
        }
    }
}
```

---

## 7. Accessibilité et responsive

### Accessibilité
- **Contrastes** maintenus : charcoal sur off-white (AAA), terracotta sur off-white (AA large), sauge réservée aux éléments courts (eyebrows, origine).
- **Focus visible** (`:focus-visible`) ajouté sur `.ckr-selection__card` et `.ckr-editorial__link` avec outline amber 2 px offset 2 px.
- **Hover = focus** : toutes les transitions visuelles se dupliquent en focus-visible.
- **`prefers-reduced-motion`** : garde globale dans `ckr_main.scss` coupe toutes les transitions et transformations pour les visiteurs concernés.
- **Sémantique** inchangée : cartes Explorer et Selection restent des `<a>` englobants ; Editorial passe d'une grille de 2 `<a>` à 1 bandeau avec 1 seul lien (simplification saine).

### Responsive
- **Hero** 60/40 : ne s'applique qu'à ≥ 992 px (breakpoint Bootstrap existant) ; mobile reste empilé.
- **Supplier** plane : `align-items: start` aux deux breakpoints ; aucune logique mobile à changer.
- **Editorial** bandeau : flex-column centré sur toutes tailles, `max-width: 720px` + container → pas de casse attendue.
- **Selection** `__head` flex : comportement garanti en mobile 320 → 768 px avec le garde-fou §6.4 (`nowrap` + ellipsis + `nowrap` prix).
- **Trust** icônes 32 × 32 charcoal : aucune régression mobile.

---

## 8. Recette et critères d'acceptation

### Recette visuelle par lot

**Après Lot A** :
- [ ] Filet amber 1 px × 48 px visible au-dessus des eyebrows de Supplier / Selection / Editorial / Trust.
- [ ] Aucun filet parasite sur Hero (pas de `--rule` appliqué) ou sur Explorer (hors périmètre V1).
- [ ] `prefers-reduced-motion` forcé dans DevTools → plus aucune transition.

**Après Lot B** :
- [ ] Hero desktop ≥ 1200 px : bloc texte à gauche ≈ 40 % largeur, visuel à droite ≈ 60 %.
- [ ] Hero mobile 375 px : texte au-dessus du visuel, CTAs empilés.
- [ ] Supplier : photo et texte alignés **en haut** (baseline des eyebrows). Filet amber 2 px visible au-dessus de l'eyebrow Supplier. **Aucun chevauchement**.
- [ ] Selection desktop : grille 4 col, titre + prix sur une ligne baseline, origine sous le bloc head.
- [ ] Selection mobile 375 px avec titre long : pas de casse, prix reste sur la même ligne, titre tronque à 2 lignes.
- [ ] Hover / focus Selection : translateY + bordure amber, outline visible au Tab.

**Après Lot C** :
- [ ] Editorial : **bandeau centré sobre** (suréligne + phrase Playfair + lien amber), **sans image de fond**, **sans overlay sombre**.
- [ ] Inspection DOM : `.ckr-editorial__tile` n'existe plus, `.ckr-editorial__bandeau` présent.
- [ ] Trust : icônes linéaires charcoal 32 × 32, **sans pilule ambrée**.

### Recette technique
- [ ] `./odoo-bin -u dorevia_ckreyol_marketplace -d <db>` passe sans erreur.
- [ ] Hard-reload assets (Ctrl+Shift+R) applique les changements à chaque lot.
- [ ] Inspection : `.ckr-hero__inner { grid-template-columns: 4fr 6fr }` en desktop après Lot B.
- [ ] Inspection : `.ckr-supplier__inner { align-items: start }` après Lot B.
- [ ] Inspection : `.ckr-editorial__bandeau` existe après Lot C.

### Recette accessibilité
- [ ] Navigation clavier complète : Tab progresse de Hero CTA → CTA secondaire → rail Explorer (prev/next/flèches) → Supplier CTA → cartes Selection → lien Editorial → Trust (sans interactif).
- [ ] Focus visible à chaque étape, outline amber sur Selection et Editorial.
- [ ] Lighthouse accessibilité ≥ 95 sur la homepage (valeur actuelle à mesurer pour comparaison).

### Recette non-régression
- [ ] Portail `/my`, fiche produit, `/shop`, routes dérivées `/collections`, `/kits`, `/promotions`, `/categories`, `/origines` : inchangés.
- [ ] Tests `dorevia_ckr_collections` (tag existant) : passent toujours.
- [ ] Header + drawer mobile identiques.
- [ ] Footer identique.

### Tests mobiles
- [ ] 375 px (iPhone SE), 390 px (iPhone 12/13), 768 px (breakpoint desktop) — pris en charge par le garde-fou §6.4.
- [ ] Orientation paysage mobile : pas de régression.

---

## 9. Versionning

Convention interne non connue avec certitude → bump **patch** par lot pour rester conservateur :

| Lot | Version avant | Version après | Justification |
|-----|---------------|---------------|---------------|
| A | 19.0.1.6.12 | **19.0.1.6.13** | Fil rouge + garde motion |
| B | 19.0.1.6.13 | **19.0.1.6.14** | Hero + Supplier + Selection |
| C | 19.0.1.6.14 | **19.0.1.6.15** | Editorial (refonte) + Trust |
| post-V1 (Ticket 1) | 19.0.1.6.15 | **19.0.1.6.16** | Alignement Hero / SPEC §7 — retrait `__subtitle-accent` (QWeb + SCSS) |

**Arbitrage possible MOA** : si la convention interne prévoit un saut mineur pour les montées en gamme visibles utilisateur, le Lot C peut basculer en `19.0.1.7.0`. À confirmer avant exécution du Lot C.

---

## 10. Hors périmètre — tickets séparés

- **Sous-titre hero `__subtitle-accent`** : **résolu en v.16** — Ticket 1 clôturé, retrait de `__subtitle-accent` pour alignement Hero / SPEC §7 (sans amendement du gel).
- **Chemin du document gelé dans les `prompt_*.md`** : les prompts vivent sous **`docs/prompting/`** ; la proposition homepage V1 gelée est **`docs/crea/PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md`** (pas de chemin fantôme type ancien `phase_2` / nom de fichier erroné). Vérifier la cohérence dans `docs/prompting/prompt_creative.md`, `docs/prompting/prompt_dev.md`, `docs/prompting/prompt_ticket.md`.
- **Explorer suréligne « Porte 0x »** : exclue de V1 ; à réévaluer en V1.1 / V2 si besoin de lisibilité éditoriale renforcée apparaît au vu de la V1 en situation.
- **Alternance des fonds de section** (`--bg-warm` / `--bg-soft`) évoquée dans la proposition créative : non incluse en V1 (les fonds actuels suffisent à marquer la respiration). À réévaluer après Lot C si l'ensemble paraît trop uniforme.

---

## 11. Conclusion — V1 implémentée

**Plan exécuté intégralement le 2026-04-23.** Les 3 lots ont été appliqués en séquence avec bumps conservateurs successifs, chaque passage étant validé par recette MOA avant bascule suivante :

1. **Lot A** (`19.0.1.6.12` → `19.0.1.6.13`) — fil rouge transverse (filet amber `__eyebrow--rule` + garde `prefers-reduced-motion` scopée `.ckr-root` / `.ckr-page`). Validé MOA.
2. **Lot B** (`.13` → `.14`) — Hero 60/40 (`grid-template-columns: 4fr 6fr`), Supplier plane V1 (`align-items: start` + filet local 2 px), Selection garde-fou responsive (`__head` flex baseline + ellipsis h3 2 lignes + prix `white-space: nowrap` + `:focus-visible` amber). Validé MOA.
3. **Lot C** (`.14` → `.15`) — Editorial refonte complète en bandeau sobre (suppression des 2 tuiles overlay sombre, nouveau `.ckr-editorial__bandeau` sans `<h2>`, filet amber local centré, lien unique amber `/collections`), Trust icônes linéaires charcoal 32×32 transparent. Validé MOA.
4. **Recette finale MOA passante.** Arbitrages additionnels levés : (a) absence de `<h2>` Editorial acceptée (outline `h1 → h2×4`, AA respecté, bandeau = transition) ; (b) lien unique `/collections` accepté (`/recettes` reste accessible via footer).
5. **Entrée d'historique V1 portée** dans `PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md` avec statut mis à jour et récapitulatif des 3 lots.
6. **Sujets hors périmètre V1** déportés en tickets séparés : voir [TICKETS_HORS_PERIMETRE_V1.md](TICKETS_HORS_PERIMETRE_V1.md).
7. **Patch post-V1 `19.0.1.6.16`** : Ticket 1 clôturé — retrait `__subtitle-accent`, conformité stricte au gel `SPEC_HERO_HOMEPAGE.md` §7 (détail §10 + tableau §9).

Le plan a respecté intégralement :
- les arbitrages gelés §9.1 à §9.4 de la proposition ;
- les 6 ajustements validés par le MOA (pas de `t-if` factice, Explorer suréligne exclue, garde-fou Selection explicite, Supplier QWeb minimal, lots séparés A/B/C, bump patch conservateur) ;
- les contraintes d'exécution (standard Odoo d'abord, périmètre V1 strict, pas de JS, pas de framework tiers, pas de V1.1, bump + `-u` à chaque lot).

---

## Historique du document

| Date | Changement |
|------|------------|
| 2026-04-23 | Création : plan d'implémentation V1 à partir du document créatif gelé. 3 lots (A fil rouge, B Hero + Supplier + Selection, C Editorial + Trust). 6 ajustements MOA intégrés (selection sans t-if factice, Explorer suréligne exclue, garde-fou selection, supplier QWeb minimal, séquencement A/B/C, bump conservateur). Patchs QWeb et SCSS détaillés par fichier. Recette par lot + non-régression. Statut GO Lot A. |
| 2026-04-23 | **Plan exécuté intégralement.** Lots A+B+C appliqués sur le module `dorevia_ckreyol_marketplace` en 3 bumps patches successifs (`.12 → .13 → .14 → .15`), chacun validé par recette MOA avant bascule suivante. Recette finale passante. Arbitrages finaux MOA levés : absence de `<h2>` Editorial acceptée (outline `h1 → h2×4` conforme AA), lien unique `/collections` accepté (`/recettes` reste accessible via footer). Statut document passé à « V1 implémentée ». Conclusion §11 refondue en retour d'exécution. Sujets hors périmètre V1 déportés dans `TICKETS_HORS_PERIMETRE_V1.md`. |
| 2026-04-23 | **Alignement post-V1.** Puce §10 `__subtitle-accent` : mention « à arbitrer » remplacée par résolution factuelle (v.16, Ticket 1 clôturé). Statut en-tête et tableau §9 versionnement mis à jour (`19.0.1.6.16`, ligne post-V1). |
