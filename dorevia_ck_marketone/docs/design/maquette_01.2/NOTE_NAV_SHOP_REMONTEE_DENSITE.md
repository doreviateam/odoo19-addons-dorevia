# Note — Nav-Shop · règle de remontée et densité 7+

| Champ | Valeur |
| --- | --- |
| **Lot** | Nav-Shop · catégories e-commerce dynamiques |
| **Ticket** | [`TICKET_DEV_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md`](../TICKET_DEV_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md) |
| **Module** | `dorevia_ck_marketone_content` · `nav_sync.py` |

---

## 1. Règle de remontée (header)

Une entrée **racine** (`product.public.category` · `parent_id = False`) apparaît dans le header si et seulement si :

```text
≥ 1 product.template publié site
  (sale_ok · is_published · website_published)
  rattaché à cette catégorie ou à l’un de ses descendants (child_of)
```

**Ordre d’affichage** : `sequence`, puis `name` (BO).

**Libellé menu** : nom exact de la catégorie BO (plus d’alias Nav-1 type « Soin & Bien-être »).

**Niveau 2** (enfant direct) : même règle de visibilité.

- **Desktop** : dropdown sous la racine · lien parent **navigable** (`ck-nav-universe-split` + URL depuis `ck_nav_category_id`, car Odoo force `url=#` dès qu’il y a des `child_id`) · entrée **« Toute {racine} »** en tête de dropdown (fallback overflow).
- **Mobile** : **Nos univers > {racine} > {L2}** — L2 rendus depuis le BO via `ck_nav_category_id` (pas de `website.menu` niveau 3, contrainte Odoo).
- **Overflow `…`** : JS `ck_nav_shop_header.js` — clic/survol L2 sans fermeture du menu parent.

**Entrées épinglées** (exclues du overflow Odoo via `o_no_autohide_item`) : **Tous nos produits** · **Découvrir**.

**Niveau 3+** : jamais injecté dans `website.menu` header — accès via fil d’Ariane, page catégorie `/shop`, ou recherche.

**Hors périmètre catalogue** (inchangés Nav-1) :

- `Tous nos produits` → `/shop` si ≥ 1 produit publié global ;
- `Découvrir` → mega éditorial (`DECOUVRIR_LINK_SPECS`) ;
- `Nos univers` → regroupement mobile uniquement (masqué desktop CSS).

**Sync** : `bootstrap_ck_navigation()` / `sync_ck_navigation_for_website()` — point d’entrée recette et cron.

---

## 2. Densité desktop 1280 px

| Nombre de racines éligibles | Statut lot |
| --- | --- |
| **4–6** | Recette exécutée sur instance seed (5–6 racines selon catalogue) |
| **7–8** | **Documenté** — pas de masquage silencieux |

### Comportement attendu à 7+ racines

Sans arbitrage MOA, le header affiche **toutes** les racines éligibles. Solutions autorisées si tenue visuelle insuffisante :

1. **Deux lignes nav** (si rendu propre, sans casser le chrome H1) ;
2. **Regroupement temporaire** documenté et validé MOA ;
3. **Limitation technique** documentée — accès catalogue conservé via `/shop` et recherche H1.

**Interdit** sans arbitrage MOA :

- masquer des catégories éligibles ;
- tronquer des libellés sans indication ;
- modifier le bandeau H1, la recherche centrale ou le panier pour « faire tenir » le menu.

### Instance seed (référence)

Racines typiques visibles après sync : **Épicerie · Maison & bien-être · Artisanat & Culture · Coups de cœur · Boissons** (+ **Tous nos produits · Découvrir**).  
**Packs & découvertes** masquée tant qu’aucun produit publié dans son sous-arbre.

---

## 3. MOA — prochaine décision si densité critique

Si le catalogue dépasse **6 racines éligibles** et que la tenue 1280 px se dégrade (chevauchement logo / chrome droit), remonter une **demande d’arbitrage MOA** avec capture 1280 px et liste des racines concernées — conforme ticket §7–§8.
