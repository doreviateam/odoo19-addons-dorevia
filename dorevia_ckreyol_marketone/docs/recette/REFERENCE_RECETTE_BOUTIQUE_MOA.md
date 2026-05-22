# Référence recette boutique MOA — `/shop` et périmètre associé

| Champ | Valeur |
|-------|--------|
| **Rôle** | **Document maître** — invariants GO MOA + checklist anti-régression |
| **Version module de référence** | **`19.0.15.11.1`** (UX-4 Lot 1 — wishlist toggle GO avec réserve) |
| **Base** | `ckr-marketone-01` · http://localhost:18079 |
| **Dernière mise à jour doc** | 2026-05-22 (UX-4 Lot 1 — critères B7–B10) |
| **Statut** | **Actif** — à mettre à jour à chaque GO MOA boutique |

> Ce document **ne remplace pas** les recettes détaillées par ticket.  
> Il liste ce qui **doit rester vrai** après chaque évolution touchant la boutique.

---

## Comment s'en servir

### Principe

| Couche | Document | Quand |
|--------|----------|-------|
| **Référence (ce doc)** | Invariants + passage régression rapide | **À chaque livraison** touchant `/shop`, header boutique, panier, wishlist, fiche depuis grille |
| **Recette ticket** | Delta du changement (ex. wishlist, UX-1) | Pendant le développement et la validation du ticket |
| **Rapport daté** | `RAPPORT_*_YYYYMMDD.md` | Archive exécution — **ne pas** utiliser comme spec active |

### Workflow MOA / recette (5 étapes)

```text
1. AVANT merge / GO ticket
   → Lire § « Matrice par type de ticket » : quelles sections rejouer ?

2. PENDANT recette ticket
   → Exécuter la recette détaillée du ticket (lien en fin de doc)
   → Puis cocher la checklist § B (régression) — desktop + mobile 375 px

3. TESTS AUTO (obligatoire avant GO)
   → Lancer la commande § « Tests automatisés »
   → Tous verts ou écarts documentés

4. VERDICT
   → GO ticket **seulement si** recette ticket OK **et** § B sans régression bloquante
   → Toute régression = NO GO ou GO avec réserve explicite + ticket correctif

5. APRÈS GO MOA
   → Si nouvel invariant validé : mettre à jour ce document + bump version référence
   → Rapport daté dans le dossier recette concerné (ux/, boutique/, racine recette/)
```

### Workflow développeur

1. **Cadrage** — vérifier si le ticket touche une zone § A (invariant) ; si oui, prévoir non-régression.
2. **Implémentation** — ne pas modifier un invariant sans décision MOA (ADR / ticket).
3. **Avant PR** — tests auto § commandes + smoke `/shop` 200.
4. **Description PR** — indiquer : « Régression référence boutique : sections Bx rejouées ».

### Workflow nouveau ticket (template)

En tête de chaque nouvelle recette manuelle boutique, ajouter :

```markdown
**Régression obligatoire :** [REFERENCE_RECETTE_BOUTIQUE_MOA.md](./REFERENCE_RECETTE_BOUTIQUE_MOA.md)
Sections à rejouer : B__ · B__ · …
```

### Matrice — sections à rejouer selon le ticket

| Type de changement | Sections référence | Recette ticket typique |
|--------------------|-------------------|------------------------|
| Tuile / image grille | **B4** · B6 · B1 (smoke) | [`RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md`](boutique/RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md) |
| Haut grille / compteur / chips | **B2** · B3 · B1 | [`RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md`](ux/RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md) · [`RECETTE_MANUELLE_SHOP_GRID_TITLE.md`](boutique/RECETTE_MANUELLE_SHOP_GRID_TITLE.md) |
| Sidebar / filtres | **B3** · B1 | [`RECETTE_MANUELLE_SHOP_UX2_SIDEBAR.md`](ux/RECETTE_MANUELLE_SHOP_UX2_SIDEBAR.md) · [`RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md`](boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md) |
| Wishlist / header icônes | **B5** · B4 · B1 · **B7** | [`RECETTE_VISUELLE_WISHLIST_STANDARD.md`](RECETTE_VISUELLE_WISHLIST_STANDARD.md) |
| UX-4 shop-in-place (toggle / panier / preview) | **B7–B10** · zones impactées | [`ux/RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md`](ux/RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md) |
| Fiche produit (depuis boutique) | B1 · B5 (si wishlist) | [`RECETTE_MANUELLE_LOT4.md`](lots/RECETTE_MANUELLE_LOT4.md) |
| Panier / checkout | B1 (smoke URL) | [`RECETTE_MANUELLE_LOT5.md`](lots/RECETTE_MANUELLE_LOT5.md) |
| **Tout ticket `/shop`** | **B1** minimum + zones impactées | Ce document § B |

---

## § A — Invariants GO MOA (ne pas casser sans nouvelle décision)

### A1 — Environnement et périmètre module

| ID | Invariant |
|----|-----------|
| E1 | Modules **non installés** : `dorevia_ckreyol_marketplace`, `theme_classic_store`, `website_sale_comparison` |
| E2 | Module **installé** : `website_sale_wishlist` (standard Odoo, dépendance Marketone ≥ `15.10.0`) |
| E3 | Upgrade `-u dorevia_ckreyol_marketone` + **restart** conteneur avant recette visuelle |

### A2 — Sidebar `/shop`

| ID | Invariant | Source GO |
|----|-----------|-----------|
| S1 | Ordre fixe : **Catégories → Collections → Origines → Fourchette de prix** | ADR-030 · Lot B · `19.0.15.10.1` |
| S2 | Libellé **Origines** (pluriel) | [`RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md`](boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md) |
| S3 | **13** catégories principales · facettes C4 (liste contextuelle, pas catalogue complet au clic) | `19.0.10.9.0` |
| S4 | **Une seule** entrée **La Réunion** (dédoublonnage origine) | `19.0.13.1.0` |
| S5 | Desktop : accordéons ouverts par défaut · label + case cliquables (UX-2) | `19.0.14.0.0` |
| S6 | **Pas** de « Clear Filters » dans la sidebar (reset = barre chips uniquement) | UX-1 |

### A3 — Haut grille (UX-1 + grid title)

| ID | Invariant | Source GO |
|----|-----------|-----------|
| G1 | Ligne 1 : **compteur gauche** · **recherche centrée** · **tri droite** (même ligne) | `19.0.15.8.5` |
| G2 | Ligne 2 (si filtres) : **Effacer les filtres** à gauche · puis chips | UX-1 U6 |
| G3 | Compteur pluriel : **`{n} produits disponibles`** · singulier : **`1 produit disponible`** | UX-1 R2 |
| G4 | 0 résultat **avec filtres** : compteur **`Aucun produit trouvé`** | `19.0.15.9.4` |
| G5 | 0 résultat **sans filtre** : **`Aucun produit disponible`** | `19.0.15.9.3` |
| G6 | État vide central filtré : **`Aucun produit ne correspond à cette sélection`** + CTA **Effacer les filtres** | `19.0.15.9.4` |
| G7 | Chips : ordre **Catégories → Collections → Origines → Prix** (miroir sidebar) | UX-1 |
| G8 | Chips collection/catégorie/origine : **`(n)`** optionnel si fiable · **jamais** sur chip prix | UX-1 R3 |
| G9 | **R1** : sans filtre prix explicite, `remove_url` chips **sans** `min_price` / `max_price` | UX-1 |
| G10 | Portes catalogue (`marketone_mode=origin`, etc.) : **pas de chip porte** · titre porte dédié | UX-1 U7 |

### A4 — Tuiles produit `/shop` (conversion)

| ID | Invariant | Source GO |
|----|-----------|-----------|
| T1 | Photo pleine bord à bord · pas d’effet « image dans l’image » | Conversion tile GO |
| T2 | Structure : titre 2 lignes · **Voir** gauche · **prix** droite · **pas** de description courte grille | Conversion tile |
| T3 | Panier au **survol** zone photo (bas droite) · add-to-cart Odoo standard | Conversion tile |
| T4 | CTA **Voir** et **prix** visuellement prioritaires vs wishlist | Conversion tile + wishlist |

### A5 — Wishlist (standard Odoo + cosmétique CK)

| ID | Invariant | Source GO |
|----|-----------|-----------|
| W1 | **Un seul** bouton wishlist par card (overlay coin **haut droit** image) | `15.10.0` |
| W2 | Cœur repos : contour discret · hover **#C4715A** · retenu terracotta persistant | Wishlist recette |
| W3 | **Pas** de logique métier CK (JS / modèle custom) · standard Odoo | Doctrine ticket |
| W4 | Fiche produit : wishlist **secondaire** vs achat | Wishlist recette |
| W5 | Comportement connecté / non connecté : **standard Odoo documenté** (pas de règle CK imposée) | § Vigilance wishlist |

### A7 — UX-4 Shop-in-place (boutique continue)

| ID | Invariant | Source / Lot |
|----|-----------|--------------|
| U1 | CTA **premier niveau** carte : pas de navigation forcée (wishlist · panier · Voir preview) | UX-4 doctrine |
| U2 | Toggle wishlist depuis `/shop` : add **et** remove AJAX sans quitter la page | Lot 1 · **B7** |
| U3 | Panier depuis grille : mode `stay` · `/shop/cart/update_json` — pas de réimplémentation | Lot 2 · **B8** |
| U4 | CTA **Voir** : preview non modale in-page (pas popup) | Lot 3 · **B9** |
| U5 | Photo + titre grille : liens secondaires fiche produit (**gel MOA Lot 3**) | UX-4 arbitrage |
| U6 | Fiche produit · panier · wishlist pages : destinations **secondaires** volontaires | UX-4 · **B10** |
| U7 | Extension légère standard Odoo — pas de modèle / logique métier CK wishlist-panier | UX-4 doctrine |

### A6 — Header boutique

| ID | Invariant |
|----|-----------|
| H1 | Navigation CK intacte · panier · compte · recherche |
| H2 | Lien wishlist `o_wsale_my_wish` harmonisé visuellement (taille / hover) si présent |

---

## § B — Checklist régression rapide (15–25 min MOA)

Cocher à **chaque GO** ticket touchant la boutique. Desktop **+** mobile **375 px**.

### B1 — Smoke URLs (2 min)

| ☐ | URL | Attendu |
|---|-----|---------|
| ☐ | `/shop` | 200 · grille · sidebar |
| ☐ | `/shop/cart` | 200 |
| ☐ | `/shop/wishlist` | 200 |
| ☐ | 1 fiche produit depuis grille | 200 · CTA achat visible |

### B2 — Haut grille (5 min)

| ☐ | Contrôle |
|---|----------|
| ☐ | `/shop` sans filtre : compteur « N produits disponibles » · recherche centrée · tri droite |
| ☐ | 1 filtre sidebar : chips ligne 2 · « Effacer les filtres » |
| ☐ | Combo restrictive → 0 résultat : « Aucun produit trouvé » + message central « cette sélection » |
| ☐ | Croix chip : pas de `min_price`/`max_price` si prix non filtré |

### B3 — Sidebar (3 min)

| ☐ | Contrôle |
|---|----------|
| ☐ | Ordre : **Catégories → Collections → Origines → Prix** |
| ☐ | Clic label case OK · C4 catégories (liste contextuelle avec 1 filtre actif) |
| ☐ | Pas de reset sidebar |

### B4 — Cards (5 min)

| ☐ | Contrôle |
|---|----------|
| ☐ | Photo pleine · titre 2 lignes · Voir + prix |
| ☐ | Cœur haut droit · discret · hover terracotta |
| ☐ | Panier au survol photo |
| ☐ | Pas de doublon wishlist |

### B5 — Wishlist (5 min — si ticket ou régression header/cards)

| ☐ | Contrôle |
|---|----------|
| ☐ | Ajout / retrait depuis card |
| ☐ | Page `/shop/wishlist` liste ou vide |
| ☐ | Header icône cohérente |
| ☐ | (Optionnel) constats P1–P7 connecté / non connecté |

### B6 — Mobile (3 min)

| ☐ | Contrôle |
|---|----------|
| ☐ | Pas de débordement horizontal `/shop` |
| ☐ | Offcanvas filtres : même ordre rubriques |
| ☐ | Cœur wishlist cliquable |

### B7 — UX-4 Wishlist toggle in-place (Lot 1+)

| ☐ | Contrôle |
|---|----------|
| ☐ | 1er clic cœur card : ajout · **URL reste `/shop`** |
| ☐ | 2e clic même cœur : retrait · compteur header cohérent |
| ☐ | Cœur retenu terracotta · feedback carte discret |
| ☐ | Pas de bouton wishlist `disabled` en grille |

### B8 — UX-4 Panier in-place (Lot 2+)

| ☐ | Contrôle |
|---|----------|
| ☐ | Clic panier survol : ajout · **URL reste `/shop`** |
| ☐ | État carte « Ajouté au panier » visible |
| ☐ | Lien secondaire « Voir le panier » · compteur header +1 |

### B9 — UX-4 Preview « Voir » in-place (Lot 3+)

| ☐ | Contrôle |
|---|----------|
| ☐ | Clic **Voir** : preview s’ouvre · **pas** navigation fiche |
| ☐ | Pas de popup modale · panneau / bloc intégré |
| ☐ | Lien « Voir la fiche complète » fonctionnel |

### B10 — UX-4 Destinations secondaires

| ☐ | Contrôle |
|---|----------|
| ☐ | Photo + titre → fiche produit (liens secondaires) |
| ☐ | Header panier → `/shop/cart` (volontaire) |
| ☐ | Header wishlist → `/shop/wishlist` (volontaire) |
| ☐ | Lien « Voir le panier » / « Voir la fiche complète » explicites sur carte ou preview |

---

## § C — Tests automatisés (avant GO)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_shop_in_place,dorevia_marketone_shop_regression,dorevia_marketone_shop_filter_state,dorevia_marketone_shop_sidebar,dorevia_marketone_shop_sidebar_collections,dorevia_marketone_shop_wishlist,dorevia_marketone_lot3_shop,dorevia_marketone_smoke \
  --http-port=8073
```

**Attendu :** 0 failed. En cas d’échec : corriger ou documenter réserve MOA.

---

## § D — Mise à jour de cette référence

| Événement | Action |
|-----------|--------|
| **GO MOA** nouveau comportement boutique | Ajouter invariant § A · ligne checklist § B si pertinent · bump version référence |
| **Changement MOA** (ex. ordre sidebar) | Modifier § A · mettre à jour ADR · archiver ancienne règle dans rapport daté |
| **Ticket hors boutique** (Culture, BO seul) | Ne pas modifier ce doc |
| **Recette ticket détaillée** | Reste dans son fichier · lien depuis § E |

**Responsable suggéré :** exécuteur recette MOA + validation tech (même personne ou binôme).

---

## § E — Index des recettes détaillées (specs par ticket)

| Sujet | Document | Statut |
|-------|----------|--------|
| **Référence anti-régression** | **Ce document** | Actif |
| UX-1 état filtres / chips | [`ux/RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md`](ux/RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md) | GO `9.4` |
| Haut grille compteur | [`boutique/RECETTE_MANUELLE_SHOP_GRID_TITLE.md`](boutique/RECETTE_MANUELLE_SHOP_GRID_TITLE.md) | GO |
| Tuile conversion | [`boutique/RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md`](boutique/RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md) | GO |
| Sidebar UX-2 | [`ux/RECETTE_MANUELLE_SHOP_UX2_SIDEBAR.md`](ux/RECETTE_MANUELLE_SHOP_UX2_SIDEBAR.md) | GO |
| Ordre sidebar | [`boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md`](boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_ORDRE.md) | GO |
| Collections sidebar | [`boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_COLLECTIONS.md`](boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_COLLECTIONS.md) | GO |
| Catégories sidebar | [`boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES.md`](boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_CATEGORIES.md) | GO |
| Facettes C4 | [`boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md`](boutique/RECETTE_MANUELLE_SHOP_SIDEBAR_FACETTES_CONTEXTUELLES.md) | GO |
| Wishlist standard | [`RECETTE_VISUELLE_WISHLIST_STANDARD.md`](RECETTE_VISUELLE_WISHLIST_STANDARD.md) | GO MOA `10.2` (réserves) |
| UX-4 shop-in-place | [`ux/RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md`](ux/RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md) | Lot 1 **GO réserve** `11.1` |
| Fiche produit | [`lots/RECETTE_MANUELLE_LOT4.md`](lots/RECETTE_MANUELLE_LOT4.md) | GO |
| Panier / checkout | [`lots/RECETTE_MANUELLE_LOT5.md`](lots/RECETTE_MANUELLE_LOT5.md) | — |
| Environnement | [`reference/ENV_REFERENCE.md`](reference/ENV_REFERENCE.md) | Réf. technique |
| Plan lots historique | [`lots/RECETTE_MANUELLE.md`](lots/RECETTE_MANUELLE.md) | **Obsolète** — prefer ce document pour `/shop` |

---

## § F — Grille verdict régression (par exécution)

| Date | Ticket / version | Exécuteur | B1–B6 | B7–B10 | Tests auto | Régression ? | Verdict |
|------|------------------|-----------|-------|--------|------------|--------------|---------|
| 2026-05-22 | Wishlist + sidebar `19.0.15.10.3` | MOA | ☑ | — | ☑ 75/75 | Non | **GO** (R2 clôturée) |
| 2026-05-22 | UX-4 Lot 1 `19.0.15.11.1` | MOA | ☑ | ☑ B7 | ☑ 79/79 | Non | **GO avec réserve documentaire** |

**Commentaire :** B6 corrigé `10.2` · R2 accordéon Collections validé MOA `10.3`. UX-4 Lot 1 validé visiteur public `11.1` — réserve connecté documentaire (comme wishlist P3–P6).
