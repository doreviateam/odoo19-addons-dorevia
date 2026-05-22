# Rapport recette — Wishlist + régression boutique

| Champ | Valeur |
|-------|--------|
| Recettes | `REFERENCE_RECETTE_BOUTIQUE_MOA.md` § B1–B6 + `RECETTE_VISUELLE_WISHLIST_STANDARD.md` |
| Version cible | **`19.0.15.10.3`** |
| Base | `ckr-marketone-01` |
| URL | http://localhost:18079 |
| Date | 2026-05-22 |
| Exécuteur | MOA / Codex |

## Verdict

**GO MOA — wishlist standard + régression boutique** (réserves mineures documentées).

| Volet | Verdict |
|-------|---------|
| Wishlist standard Odoo + cosmétique CK | **GO** |
| Référence boutique § B1–B6 | **GO** (B6 corrigé en `10.2`) |
| Tests automatisés | **75 tests, 0 failed** |

**Réserves non bloquantes :**
- Scénarios utilisateur connecté / fusion session (P3–P6) non exécutés — documentaire, hors scope cosmétique.

### Historique

- **Passe 1 (`10.1`)** : NO GO B6 — Collections absente offcanvas mobile.
- **Passe 2 (`10.2`)** : GO B6 ciblé — ordre offcanvas conforme.
- **Passe 3 (`10.3`)** : GO R2 — titre Collections aligné accordéon natif.

## Préparation environnement

| Étape | Résultat |
|-------|----------|
| Conteneur `sandbox-odoo19-odoo-1` | Démarré |
| Upgrade `-u dorevia_ckreyol_marketone` | OK |
| Restart Odoo | OK |
| Smokes HTTP `/shop`, `/shop/cart`, `/shop/wishlist` | 200 OK |

Note technique : warning Odoo `@class` toujours observé sur la vue collections sidebar. Non bloquant pour l'exécution, mais toujours présent.

## Tests automatisés

Commande exécutée :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_shop_wishlist,dorevia_marketone_shop_regression,dorevia_marketone_shop_filter_state,dorevia_marketone_shop_sidebar,dorevia_marketone_shop_sidebar_collections,dorevia_marketone_smoke,dorevia_marketone_lot3_shop \
  --http-port=8073
```

Résultat : **74 tests, 0 failed, 0 error(s)**.

## Référence boutique § B1–B6

| Section | Contrôle | Verdict | Notes |
|---------|----------|---------|-------|
| B1 | `/shop`, `/shop/cart`, `/shop/wishlist`, fiche produit | OK | HTTP 200 et pages chargées |
| B2 | Compteur, chips, état vide filtré, remove URL sans prix implicite | OK | `50 produits disponibles`, `Aucun produit trouvé`, reset présent, pas de `min_price/max_price` implicite |
| B3 | Sidebar desktop | OK | Ordre desktop conforme : Catégories → Collections → Origines → Prix |
| B4 | Cards | OK | Photo, `Voir`, prix, coeur haut droit, pas de doublon wishlist |
| B5 | Wishlist | OK | Ajout, page pleine, retrait, état vide, compteur 0 → 1 → 0 |
| B6 | Mobile | **OK** (passe 2) | Ordre offcanvas : Catégories → Collections → Origines → Prix · pas de débordement |

## Recette wishlist

| Contrôle | Verdict | Notes |
|----------|---------|-------|
| Header wishlist | OK | Icône visible, compteur cohérent |
| Card repos | OK | Coeur discret coin haut droit |
| Ajout depuis card | OK | Ajout public sans login, compteur passe à 1 |
| Page wishlist pleine | OK | Produit listé |
| Retrait wishlist | OK | Produit supprimé, compteur revient à 0 |
| Fiche produit | OK | Wishlist secondaire à côté du CTA achat |
| Mobile | OK pour wishlist | Coeur visible et grille sans débordement |
| Connecté / fusion session | Non exécuté | Compte test MOA non fourni |

## Anomalie bloquante

| ID | Zone | Attendu | Observé | Gravité |
|----|------|---------|---------|---------|
| R1 | Mobile offcanvas filtres | Catégories → Collections → Origines → Fourchette de prix | ~~Catégories → Origines → Fourchette de prix~~ **Corrigé `10.2`** | ~~Bloquant~~ **Clos** |
| R2 | Offcanvas — alignement titre Collections | Aligné accordéon natif (`o_wsale_offcanvas_title`) | **Corrigé `10.3`** | **Clos** |

## Captures

### Desktop conforme

![Shop desktop](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/capture_boutique_wishlist_regression_shop_desktop_20260522.png)

### Filtre actif et chips

![Filtre actif](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/capture_boutique_wishlist_regression_filter_chip_20260522.png)

### État vide filtré

![État vide filtré](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/capture_boutique_wishlist_regression_empty_filtered_20260522.png)

### Wishlist pleine

![Wishlist pleine](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/capture_boutique_wishlist_regression_wishlist_full_20260522.png)

### Mobile offcanvas KO (passe 1)

![Mobile offcanvas KO](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/capture_boutique_wishlist_regression_mobile_filters_20260522.png)

### Mobile offcanvas R2 (`10.3` — GO cosmétique)

![R2 offcanvas OK](/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/recette/capture_boutique_wishlist_regression_mobile_filters_r2_ok_20260522.png)

## Conclusion

**GO MOA** — activation `website_sale_wishlist` validée · régression boutique levée (`10.2`) · réserve cosmétique R2 clôturée (`10.3`).

**Réserve documentaire restante :** connecté / fusion session (P3–P6) — à traiter ultérieurement si compte test MOA fourni.

---

## Correctif Dev (`19.0.15.10.2`)

| Élément | Détail |
|---------|--------|
| Cause | Injection Collections offcanvas via héritage catégories — non rendue dans `o_wsale_offcanvas` |
| Fix | Template `marketone_shop_sidebar_collections_offcanvas_after_categories` — injection après accordéon Catégories |
| Test | `test_shop_offcanvas_collections_after_categories` |
| Statut | **GO MOA B6** — re-recette mobile 390 px validée |

## Correctif cosmétique R2 (`19.0.15.10.3`)

| Élément | Détail |
|---------|--------|
| Réserve | Titre « Collections » offcanvas moins aligné que les accordéons natifs |
| Fix | Structure `accordion-item` + `o_wsale_offcanvas_title` (identique Catégories / Origines) |
| Test | `test_shop_offcanvas_collections_after_categories` enrichi |
| Statut | **GO MOA R2** — contrôle mobile 390 px validé MOA |

## Re-recette R2 (passe 3 — `10.3`)

| Contrôle | Résultat |
|----------|----------|
| Upgrade + restart | OK |
| Mobile 390 px — offcanvas Filtres | Rendu accordéon identique Catégories / Origines |
| Chevron Collections | Présent |
| Ordre rubriques | Catégories → Collections → Origines → Fourchette de prix |
| Débordement / CSS / console | OK |

## Re-recette B6 (passe 2)

| Contrôle | Résultat |
|----------|----------|
| Tests auto | **75 tests, 0 failed, 0 error(s)** |
| `test_shop_offcanvas_collections_after_categories` | OK |
| Mobile 390 px — offcanvas Filtres | Catégories → Collections → Origines → Fourchette de prix |
| Débordement / CSS / console | OK |
