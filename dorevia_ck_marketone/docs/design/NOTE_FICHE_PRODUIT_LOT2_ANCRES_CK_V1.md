# NOTE DE LIVRAISON — Fiche produit CK · Lot 2 front (Option A ancres)

**Projet** : C-Kreyol — Odoo 19  
**Date** : 2026-06-18  
**Modules** :

| Module | Version |
|--------|---------|
| `dorevia_ck_theme` | `19.0.1.36.2` |
| `dorevia_ck_marketone_content` | `19.0.1.25.32` |

**Instance recette** : `dorevia_ck_marketone_01` · http://localhost:18079  
**Produit témoin** : Confiture de goyave (`/shop/confiture-de-goyave-3`)

---

## 1. Verdict MOA

| Niveau | Statut |
|--------|--------|
| Structure UX (Zone 0 + zone longue) | **GO** |
| Option A — empilement + ancres | **GO** |
| Habillage CSS zone longue V1 | **GO** |
| Galerie produit desktop | **GO** |
| Mobile 390 px (recette automatisée) | **GO** |

**Verdict global Lot 2 fiche produit CK : validé MOA** (2026-06-18).

Retour MOA confirmé :

- Zone haute achat conservée
- Onglets remplacés par empilement + ancres
- Bandeau discret · sections dans le flux
- Découvrir / Composition / Conservation / Détails cohérents
- Galerie : pot visible en entier
- Passerelle Pro discrète
- Pas de retour aux grandes sections documentaires

---

## 2. Doctrine retenue

```text
Zone 0 = achat immédiat
Zone longue = complément, réassurance, légal — visible dans le flux
```

La fiche n’est plus une page documentaire verticale. Les anciens blocs « À propos » / « Spécifications » / grand encart Pro ont été remplacés par une zone longue compacte, navigable par ancres HTML.

---

## 3. Parcours de livraison (synthèse)

| Étape | Décision / livrable |
|-------|---------------------|
| Lot 2 initial | Onglets Bootstrap sous zone achat |
| Retour MOA structure | **Option A** : ancres + empilement (onglets retirés) |
| Retour MOA visuel | Polish CSS zone longue (chaleur CK, séparateurs adoucis) |
| Correctif technique | Droits public `dorevia.ck.card.uom` (403 visiteur anonyme) |
| Correctif SCSS | Compilation Sass (`min()` interdit) |
| Correctif galerie | `object-fit: contain` vs `cover` natif Odoo |

---

## 4. Structure fonctionnelle

### Zone 0 — inchangée

Bloc achat : image, titre, chips catégorie, métadonnées card, accroche, prix, quantité, CTA panier, rassurance courte.

### Zone longue — Option A

**Bandeau d’ancres** (affiché si ≥ 2 blocs) :

```text
Découvrir · Composition · Conservation · Détails
```

Liens HTML natifs · pas de `tablist` · pas de contenu masqué · smooth scroll CSS (`scroll-behavior: smooth`) · pas de sticky V1.

**Blocs empilés** :

| Ancre | Contenu |
|-------|---------|
| `#ck-section-discover` | Origine & usage · Conseils d’usage · Origine & producteur |
| `#ck-section-composition` | Ingrédients · Allergènes · Nutrition (si alimenté) |
| `#ck-section-conservation` | Avant / Après ouverture · note livraison |
| `#ck-section-details` | Specs factuelles (remplace « Spécifications » natif) |

**Passerelle Pro** : discrète sous la zone longue — *« Vous commandez pour un commerce ou un restaurant ? Espace professionnel CK »*.

### Gestion des sections vides

| Cas | Comportement |
|-----|--------------|
| 4 blocs alimentés | Bandeau 4 liens |
| 3 blocs | Bandeau 3 liens, pas de lien mort |
| 1 bloc | Bandeau masqué |
| Aucun contenu parser | Pas de zone longue, pas d’erreur |
| Composition vide | Bloc absent (pas de placeholder) |

---

## 5. Fichiers livrés

### Contenu (`dorevia_ck_marketone_content`)

| Fichier | Rôle |
|---------|------|
| `product_page_tabs.py` | Regroupement sections parser → blocs + `anchor_id` / `nav_label` |
| `product_page_details.py` | Parser `website_description` (inchangé fonctionnellement) |
| `models/product_template.py` | `get_ck_product_page_tabs()` · `get_ck_shop_card_metadata_line()` |
| `views/website_sale_product_page.xml` | Injection données + masquage `product_full_description` |
| `security/ir.model.access.csv` | Lecture publique `dorevia.ck.card.uom` |
| `hooks.py` | Seed goyave : section Ingrédients & allergènes |
| `migrations/19.0.1.25.31/post-migrate.py` | Reprise ingrédients confiture goyave |
| `tests/test_ck_product_page_tabs.py` | Unitaires blocs / ancres |
| `tests/test_ck_product_page_lot2_front.py` | HTTP zone longue + ancres |

### Thème (`dorevia_ck_theme`)

| Fichier | Rôle |
|---------|------|
| `views/website_sale_product_page.xml` | QWeb zone longue · bandeau ancres · masquage specs natives |
| `static/src/scss/product_page.scss` | Zone 0 · zone longue · galerie · ancres |
| `views/website_sale_product_compose.xml` | Composition page (Pro retiré du compose) |
| `__manifest__.py` | Dépendance `website_sale_comparison` |

---

## 6. Habillage CSS (zone longue)

- Conteneur `complement` : dégradé crème, transition douce vers le footer
- Carte `long-zone` : surface blanche, bordure adoucie, ombre légère (`col-lg-8`)
- Bandeau ancres : repère éditorial, hover rouge CK, séparateurs discrets
- Titres blocs : Fraunces · sous-titres en petites caps
- Encart usage : vert CK poli (dégradé + bordure)
- Composition : fond rassurant `$ck-bg-soft`
- Conservation : panneaux Avant / Après harmonisés
- Détails : lignes alternées (fini l’effet tableau brut)
- Origine producteur : pastille compacte

---

## 7. Galerie produit (zone 0)

**Problème** : Odoo natif impose `object-fit: cover` + `aspect-ratio` fixe → photo rognée.

**Correction** : surcharge CK sur `#o-carousel-product` :

- `object-fit: contain !important`
- `aspect-ratio: auto`
- `max-height: 400px` desktop (onglets/ancres remontés sans rogner le produit)

---

## 8. Hors périmètre respecté

```text
Pas de nouveau champ BO
Pas de modification parser / description_sale
Pas de régression panier · checkout · footer
Pas de régression cards Home / Boutique
Pas de retour aux onglets
Pas de sticky bandeau V1
Pas de parser Markdown complexe
Markdown brut neutralisé (*Usage :* → Usage :)
```

Blocs natifs masqués quand zone longue active : `product_full_spec`, accordéon specs, documents redondants.

---

## 9. Tests

**Tags** : `dorevia_ck_product_page_tabs` · `dorevia_ck_product_page_lot2_front` · `dorevia_ck_theme_phase4`

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --test-enable --stop-after-init \
  --http-port=8071 -u dorevia_ck_marketone_content \
  --test-tags dorevia_ck_product_page_tabs,dorevia_ck_product_page_lot2_front,dorevia_ck_theme_phase4
```

**Résultat attendu** : 0 échec (38 tests Lot 2 + phase4).

---

## 10. Déploiement

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 \
  -u dorevia_ck_theme,dorevia_ck_marketone_content \
  --stop-after-init

docker restart sandbox-odoo19-odoo-1
```

Hard refresh navigateur après upgrade assets (`Cmd+Shift+R`).

---

## 11. Recette mobile 390 px

### Script automatisé

```bash
cd dorevia_ck_marketone/docs/design/maquette_01.2/scripts
CK_SCREENSHOT=1 node ck_lot2_product_mobile390.mjs
```

Produit témoin : `/shop/confiture-de-goyave-3` · viewport **390×844** · base `localhost:18079`.

### Résultat recette (2026-06-18)

| Critère MOA | Résultat |
|-------------|----------|
| Aucun overflow horizontal | **OK** — `scrollWidth = clientWidth = 390` |
| Bandeau ancres lisible (1–2 lignes) | **OK** — hauteur ~45 px · 4 liens sur une ligne |
| Sections empilées | **OK** — 4 blocs `#ck-section-*` |
| Conservation colonne unique | **OK** — `grid-template-columns: 1fr` |
| CTA achat utilisable | **OK** — `#add_to_cart` présent · visible après scroll vertical (empilement mobile Lot 1 : galerie puis bloc achat) |
| Footer sans rupture | **OK** — footer présent |

Captures : `docs/design/maquette_01.2/captures/lot2_product_mobile390/`

- `01_zone_haute.png`
- `02_bandeau_ancres.png`
- `03_conservation.png`
- `04_footer.png`

---

## 12. Recette manuelle MOA (desktop)

| # | Scénario | Attendu |
|---|----------|---------|
| 1 | Desktop 1280 px — confiture goyave | Zone 0 compacte · photo entière dans le cadre · bandeau ancres · 4 blocs visibles |
| 2 | Clic « Composition » | Scroll vers `#ck-section-composition` |
| 3 | Mobile 390 px | Pas d’overflow horizontal · ancres sur 1–2 lignes · conservation en colonne |
| 4 | Visiteur non connecté | Pas de 403 · fiche 200 |
| 5 | Produit sans `website_description` | Pas de zone longue · zone 0 intacte |
| 6 | `/shop` et `/` | Cards Home / Boutique inchangées |

---

## 13. Documents associés

- `NOTE_FICHE_PRODUIT_ZONE0_ONGLETS_CK_V1.md` — historique intermédiaire (onglets, obsolète structure)
- `NOTE_CLARIFICATION_PARSER_WEBSITE_DESCRIPTION_CK_V1.md` — source contenu parser
- `CARTOGRAPHIE_CHAMPS_PRODUIT_CK_V1.md` — champs produit CK

---

## 14. Formulation synthétique Dev

```text
Zone 0 = achat immédiat.
Zone longue = complément en flux, navigation par ancres.
Même contenu parser, même logique métier — présentation Option A validée MOA.
```
