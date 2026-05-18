# Banque visuelle — réutilisation `dorevia_ckreyol_marketplace/docs/assets`

| Champ | Valeur |
|-------|--------|
| **Chemin source** | `../dorevia_ckreyol_marketplace/docs/assets/` (depuis ce module) |
| **Inventaire détaillé** | [`dorevia_ckreyol_marketplace/README.md`](../../../dorevia_ckreyol_marketplace/README.md) — § Références visuelles |
| **Statut Marketone** | Référence autorisée — **pas de copie mécanique** dans le module sans décision MOA |

---

## Règles d'usage Marketone

| Règle | Application |
|-------|-------------|
| Inspiration, pas portage legacy | Les PNG servent recette, cadrage et futurs lots — **pas** de reprise des blocs marketplace (Explorer, hero rotateur, portes). |
| Pas de seed XML | Images importées **manuellement en BO** pour produits de recette (2–3 fiches). |
| Artisanal Terroir prioritaire | Direction visuelle = tokens Lot 2.1 ; assets marketplace **complètent**, ne remplacent pas le design system. |
| ADR-018 / ADR-019 | Pas de densité média type 750g ; pas de logique marketplace Caribshopper ; fiche **non encyclopédique**. |
| Fichiers `stitch_*` | **Inspiration design** (Stitch) — interdit de copier HTML/CSS ; alignement conceptuel Artisanal Terroir uniquement. |
| Scènes « ambiance » | `mvp02_reference_tropical_panier_fleurs_plage.png` — éditorial / territoire **plus tard**, pas packshot produit par défaut. |

---

## Inventaire synthétique (21 PNG)

### Packshots produit — priorité recette BO (`/shop`, fiche Lot 4)

Idéaux pour **2 à 3 produits de recette** (upload BO) :

| Fichier | Usage recommandé |
|---------|------------------|
| `homepage_maniocookies_sale_la_platine.png` | Carte boutique / fiche — produit réel, fond clair |
| `homepage_manioc_crackers_sale_ste_anne.png` | Idem |
| `homepage_manioc_pates_mayotte_la_platine.png` | Idem |
| `exemple_produit_manioc_crackers_la_platine.png` | Référence **fiche produit** (packaging lisible, hiérarchie titre/prix) |

### Moodboards MVP02 — lots éditoriaux / portes (après socle)

| Fichier | Usage |
|---------|--------|
| `mvp02_reference_confitures_tropicaux_panier.png` | Ambiance confitures, sélection |
| `mvp02_reference_coffret_gourmand_bois.png` | Coffret / offrir |
| `mvp02_reference_epicerie_verre_etagere.png` | Épicerie fine |
| `mvp02_reference_epices_curry_piments.png` | Épices / territoire |
| `mvp02_reference_miel_pot_mains.png` | Artisanat / chaleur |
| `mvp02_reference_tropical_panier_fleurs_plage.png` | **Éditorial territoire** — pas tuile produit seule |
| `hero_reference_direction_a_biscuits_confiture.png` | Macro / matière — inspiration hero future |

### Exports Stitch — inspiration design (hors intégration directe)

`stitch_hero_ambiance_food.png`, `stitch_hero_pantry_shelf.png`, `stitch_caribbean_kitchen.png`, `stitch_caribbean_spread.png`, `stitch_curry_powder_pouch.png`, `stitch_guava_jam_jar.png`, `stitch_jerk_marinade_bottle.png`, `stitch_scotch_bonnet_sauce.png`, `stitch_tropical_spread.png`

→ Référence MOA / tickets créa ; **ne pas** servir de bannières lourdes au Lot 4.

---

## Procédure recette — produits BO (`ckr-marketone-01`)

1. Ouvrir le dossier source :

   ```text
   odoo19-addons-dorevia/dorevia_ckreyol_marketplace/docs/assets/
   ```

2. Créer **2 à 3** `product.template` publiés sur le site.

3. Pour chaque fiche : **eCommerce** → image = un des packshots `homepage_*` ou `exemple_produit_*` (redimensionnement Odoo accepté).

4. Vérifier `/shop` (cartes `marketone-shop`) et, après Lot 4, fiche `marketone-product`.

5. **Ne pas** committer ces binaires dans `dorevia_ckreyol_marketone/static/` sauf décision MOA explicite (poids repo, doublon avec marketplace).

---

## Liens doctrine

| Document | Lien |
|----------|------|
| ADR-018 | Trois dimensions — socle e-commerce d'abord |
| ADR-019 | Inspirations 750g / Caribshopper |
| ADR-020 | Exploitation banque assets marketplace |
| `ENV_REFERENCE.md` | Commandes tests et base recette |
| `TICKET_MARKETONE_LOT4_PRODUCT.md` | Recette fiche — images BO |
