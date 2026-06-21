# Ticket Dev — Polish bloc achat fiche produit CK (zone haute Lot 1) · V1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` · C-Kreyol / CK |
| **Module** | `dorevia_ck_theme` (SCSS) — `static/src/scss/product_page.scss` |
| **Type** | Polish UI / présentation · périmètre étroit |
| **Priorité** | Moyenne (qualité perçue) — **présentation uniquement** |
| **Périmètre** | Fiche produit front — **bloc achat** (zone haute Lot 1) |
| **Statut** | À exécuter |

```text
Objectif : remonter le bloc achat au standard « boutique CK premium » sans refonte —
3 ajustements CSS ciblés. Aucune logique prix / panier / variantes touchée.
```

---

## 1. Contexte

La zone haute Lot 1 est **validée fonctionnellement** (achat, favori, réassurance OK). Mais le **rendu visuel du bloc achat** reste en deçà du reste du site (effet « Odoo e-commerce repeint » plutôt que boutique CK). Ce ticket corrige la présentation, sans rouvrir le chantier ni toucher la logique.

> C'est un polish CSS du **Lot 1**, qui était marqué « ne pas toucher » dans le ticket Lot 2 — d'où ce ticket dédié.

---

## 2. Constat (capture bloc achat)

1. **Sélecteur de quantité pleine largeur** — la boîte « − 1 + » s'étire sur toute la colonne avec un grand vide central → effet cassé/inachevé. **Point principal.**
2. **Eyebrow catégories** (« Épicerie  Coups de cœur ») — rendu en texte muet collé, sans style chip visible ni séparateur → flotte, on ne sait pas si c'est cliquable.
3. **Trop de filets gris horizontaux** entre prix / quantité / réassurance → effet « formulaire administratif », rythme haché.

---

## 3. Corrections demandées (priorisées)

### 3.1 Quantité compacte (priorité)
- La quantité ne doit **plus s'étirer** : largeur compacte (~120–140 px), contrôles `−` / valeur / `+` serrés, alignée à gauche.
- La rangée quantité + favori + comparer doit respirer (gap), sans bloc étiré.

Sélecteur : `.ck-product-layout__buy .css_quantity.input-group` (+ `.form-control.quantity`).
```scss
.ck-product-layout__buy {
    .css_quantity.input-group {
        width: auto;
        max-width: 140px;
        flex: 0 0 auto;        // ne pas étirer dans le flex de la rangée
    }
    .form-control.quantity { text-align: center; }
}
```

### 3.2 Eyebrow catégories lisible
- Donner aux chips un vrai look « tag » (petite pilule discrète) **ou** un séparateur `·` clair — cohérent avec les chips de la fiche / cards.

Sélecteur : `.ck-product-purchase__chips .ck-chip`.
```scss
.ck-product-purchase__chips {
    display: flex; gap: 6px; margin-bottom: 6px;
    .ck-chip {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 999px;
        background: $ck-bg-soft;
        color: $ck-text-muted;
        font-size: 12px;
        font-weight: $ck-font-weight-semibold;
        text-decoration: none;
        &:hover { color: $ck-primary; }
    }
}
```

### 3.3 Alléger les filets
- Réduire le nombre de `border-top` dans le bloc achat (actuellement plusieurs : prix / quantité / réassurance). **Garder un seul filet discret** (au-dessus de la réassurance), rythmer le reste par l'espacement vertical.

Concerné : les multiples `border-top: 1px solid …` de `product_page.scss` (bloc achat). Conserver celui de la réassurance, retirer/atténuer les intermédiaires.

### 3.4 Mobile 390 px — actions secondaires icône seule (retour MOA — bloquant)

**Constat MOA (390 px) :** favori avec **libellé tronqué**, comparer **sur 2 lignes**, rangée surchargée, actions secondaires qui dégradent le CTA.

**Cause racine identifiée :** la structure mobile est déjà bonne (grille `#o_wsale_cta_wrapper` : quantité col 1, favori/comparer à droite, CTA pleine largeur en ligne 2). Le bug vient du **masquage du libellé** ciblé sur `span.d-lg-none` / `> span.d-inline.ms-2` (≈ lignes 376‑379) qui **ne correspondent plus au markup Odoo 19** des boutons `.o_add_wishlist_dyn` / `.o_add_compare_dyn` → le texte n'est pas masqué et, sur un bouton de 42 px en `overflow:hidden`, il est tronqué/passe à la ligne.

**Cible mobile :**
```text
[ − 1 + ]   [♡] [⇄]
[ Ajouter au panier ]
```

**Correction (robuste, markup‑agnostique)** — remplacer le ciblage fragile par un masquage de tout texte, en restaurant l'icône :
```scss
@media (max-width: 991.98px) {
    .o_add_wishlist_dyn,
    .o_add_compare_dyn {
        font-size: 0 !important;                 // collapse TOUT texte/label (y c. nœuds texte nus)
        > .fa, > .oi, > i { font-size: 1rem !important; }   // restaure l'icône seule
        // (retire / remplace le ciblage span.d-lg-none / span.d-inline.ms-2 devenu inopérant)
    }
}
```
Conserver : boutons carrés 42 px, `overflow:hidden`, `white-space:nowrap`, `aria-label`/`title` (accessibilité), quantité compacte ligne 1, **CTA panier pleine largeur en ligne 2**.

**Ne pas régresser le desktop** : sur ≥ 992 px, le rendu actuel (icônes carrées sans texte) reste inchangé.

---

## 4. Style cible

Esprit CK existant : fond clair chaud, titres serif, accent orange, **sobre et premium**. Utiliser les tokens existants (`$ck-border`, `$ck-bg-soft`, `$ck-text-muted`, `$ck-primary`). Pas de dégradés ni d'ombres lourdes.

---

## 5. Contraintes

Ne pas :
- modifier la logique prix / quantité / panier / variantes ;
- modifier le QWeb au-delà d'éventuels ajustements de classe mineurs (idéalement **SCSS seul**) ;
- toucher au Lot 2 sections longues, aux cards Home/Boutique, au favori, à la réassurance (contenu) ;
- refondre la zone haute.

Peut :
- ajuster `product_page.scss` (et, si nécessaire, une classe de wrapper sur la rangée quantité).

---

## 6. Recette / tests

- **Captures** desktop 1280 px + mobile 390 px (Confiture de goyave).
- Quantité compacte, alignée, fonctionnelle (− / + / saisie).
- Eyebrow lisible (chips ou séparateur).
- Filets allégés, rythme aéré.
- **Non-régression** : ajout panier OK, favori OK, variantes (Manio) OK, Lot 2 sections longues intactes, cards Home/Boutique intactes, **mobile 390 sans overflow** (script Playwright existant).
- Tests front existants `dorevia_ck_theme_phase4` verts.

---

## 7. Critères d'acceptation MOA

| Critère | Attendu |
|---|---|
| Quantité | Compacte (~120–140px), serrée, alignée gauche — plus de boîte pleine largeur |
| Eyebrow | Chips lisibles ou séparateur clair |
| Filets | Un seul filet discret, rythme par l'espacement |
| Logique achat/prix/variantes | Inchangée |
| Lot 2 / cards / favori | Non régressés |
| **Mobile 390 — favori/comparer** | **Icône seule, aucun libellé texte** |
| **Mobile 390 — texte** | **Aucun texte tronqué** |
| **Mobile 390 — boutons** | **Aucun bouton sur 2 lignes** |
| **Mobile 390 — overflow** | **Aucun overflow horizontal** |
| **Mobile 390 — CTA** | **« Ajouter au panier » pleine largeur, prioritaire, sous la rangée** |
| **Mobile 390 — quantité** | **Compacte et utilisable** |
| Desktop ≥ 992px | Rendu actuel non régressé |
| Validation | Captures desktop 1280 + mobile 390 (Playwright) |

---

*Ticket polish bloc achat fiche produit CK · présentation uniquement · SCSS `product_page.scss`.*
