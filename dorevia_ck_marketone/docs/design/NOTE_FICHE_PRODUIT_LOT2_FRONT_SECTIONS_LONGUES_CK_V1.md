# Note de livraison — Lot 2 front fiche produit CK (sections longues)

**Projet** : C-Kreyol — Odoo 19  
**Modules** : `dorevia_ck_theme` **19.0.1.35.6** · `dorevia_ck_marketone_content` **19.0.1.25.28**  
**Date** : juin 2026  
**Statut** : livré Dev — validation visuelle MOA sur captures desktop 1280px / mobile 390px

---

## Objectif

Reprendre l’UX des sections longues sous la zone achat Lot 1 : rendu plus chaleureux, lisible et orienté expérience d’achat, sans modifier le parser ni le BO.

---

## Champ éditorial source

| Usage | Champ |
|-------|--------|
| Sections longues | `website_description` |
| Accroche zone achat | `description_ecommerce` |
| Notes commerciales Odoo | `description_sale` — **hors contenu front MOA** |
| Origine géographique | Attribut produit « Origines » (section `origin_producer` si non couverte) |

---

## Gabarit HTML recommandé (`website_description`)

```html
<div class="ck-product-enrich">
  <h3>Origine &amp; usage</h3>
  <p>Texte de présentation du produit, de son univers et de son usage principal.</p>
  <p><strong>Usage :</strong> idées de consommation ou d’utilisation.</p>

  <h3>Conservation</h3>
  <p>Avant ouverture : consigne de conservation. Après ouverture : consigne après ouverture.</p>

  <h3>Ingrédients &amp; allergènes</h3>
  <p>Liste des ingrédients et allergènes éventuels.</p>
</div>
```

---

## Sections supportées (parser inchangé)

| Clé | Titre front |
|-----|-------------|
| `origin_usage` | Origine & usage |
| `usage` | Conseils d’usage |
| `conservation` | Conservation |
| `ingredients` | Ingrédients & allergènes |
| `origin_producer` | Origine & producteur |
| `nutrition` | Valeurs nutritionnelles |

---

## Livrable front

### Templates (`dorevia_ck_theme`)

- Zone `ck-product-page__details` sous `#product_detail`
- Grille Bootstrap `col-lg-8` centrée (largeur lecture ~720px)
- En-tête éditorial : eyebrow « Découvrir » + titre « À propos de ce produit »
- Classes par section : `ck-product-page__section--{key}`
- Conservation : panneaux `ck-product-page__section-split` / `section-panel`

### SCSS (`product_page.scss`)

- Fond dégradé léger, séparateurs discrets
- Typographie plus aérée (`$ck-text-base`, interlignage 1.65)
- Styles par type de section (usage, conservation, ingrédients, origine producteur)
- Responsive mobile sans padding excessif

---

## Contraintes respectées

| Contrainte | Statut |
|------------|--------|
| Aucun nouveau champ | ✅ |
| Aucun changement BO | ✅ |
| Aucun changement parser | ✅ |
| Lot 1 zone haute intact | ✅ |
| Cards Home / Boutique intactes | ✅ |
| `description_sale` non hypothèse UX | ✅ (fallback technique inchangé) |
| Logique origine produit inchangée | ✅ |

---

## Dettes / réserves

- **Fallback `description_sale`** : toujours actif techniquement si `website_description` vide — ticket séparé Option B prévu.
- **Validation visuelle MOA** : ajustements fins (espacements, titres, séparateurs) possibles sans refonte structurelle.
- **Captures** : à produire côté MOA sur instance `dorevia_ck_marketone_01` (desktop 1280px, mobile 390px).

---

## Tests

Tag Odoo : `dorevia_ck_product_page_lot2_front`

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --http-port=8079 --no-http \
  --test-enable --stop-after-init \
  --test-tags dorevia_ck_product_page_lot2_front,dorevia_ck_product_page_lot2,dorevia_ck_theme_phase4
```

---

## Documents liés

- `CARTOGRAPHIE_CHAMPS_PRODUIT_CK_V1.md`
- `NOTE_CLARIFICATION_PARSER_WEBSITE_DESCRIPTION_CK_V1.md`
- `NOTE_BO_PRODUIT_ONGLET_VENTES_CK_V1.md`
