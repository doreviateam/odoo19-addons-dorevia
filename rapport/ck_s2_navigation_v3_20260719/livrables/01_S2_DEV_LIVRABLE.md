# S2-A Dev — Navigation V3 canonique et idempotente

**Branche :** `refactor/s2-canonical-navigation-v3`  
**Worktree :** `worktree:odoo19-addons-dorevia-s2-nav`  
**Base :** `origin/main` @ `4f6184f`  
**Module :** `dorevia_ck_marketone_content` → `19.0.1.96.0`  
**Statut :** commit local uniquement — **pas de push / PR / déploiement**

---

## 1. Diagnostic des trois implémentations

| Impl | Entrée historique | Effet avant S2 | Après S2 |
|---|---|---|---|
| **V3** `bootstrap_ck_catalogue_navigation` | `hooks.py` install/upgrade + migrations récentes | Boutique + catégories exposables + Producteurs + Pro | **Unique autorité** |
| **V2.2** `bootstrap_ck_navigation` | migrations + modèles mega BO | Megas / purge rayons N3 | **Délègue à V3** (+ warning log) |
| **V1** `bootstrap_ck_navigation_v1` | migration `19.0.1.72.0` | Purgeait `MANAGED_V22` dont **Épicerie** | **Délègue à V3** (+ warning log) |

Point d’entrée réellement exécuté à l’install/upgrade module : toujours `hooks.bootstrap_all_marketone_content` → `bootstrap_ck_catalogue_navigation`.

---

## 2. Fonctions supprimées / neutralisées / conservées

### Neutralisées (délégation V3)
- `bootstrap_ck_navigation` / `sync_ck_navigation_for_website`
- `bootstrap_ck_navigation_v1` / `sync_ck_navigation_v1_for_website`
- `CkMegaMenuVisualBlock._ck_refresh_navigation` → appelle V3
- `CkMegaMenuRayonVisual._ck_refresh_navigation` → appelle V3

### Canoniques (conservées / renforcées)
- `bootstrap_ck_catalogue_navigation`
- `sync_ck_catalogue_navigation_for_website`
- `_upsert_menu` : matching prioritaire `ck_nav_category_id`, puis `name`
- `_cleanup_ck_catalogue_root_menus` : ne détruit plus Épicerie éligible
- `snapshot_ck_catalogue_navigation` : état structuré pour idempotence

### Conservées pour compat / tests / mega HTML (non utilisées par le sync runtime)
- Helpers V2.2 (`_sync_mega_rayon`, `build_*_mega`, `sync_communaute_header`, …)
- Constantes `nav_v22_config` encore référencées

---

## 3. Changements clés

1. Identité stable menu ↔ catégorie via `ck_nav_category_id`.
2. Cleanup V3 sans purge aveugle des libellés V2.2 encore catalogue-éligibles.
3. Réécriture URL parent après création d’enfants (contre le forçage Odoo `url='#'`).
4. Migration `19.0.1.96.0` : resync V3 post-upgrade.
5. Suites de tests adaptées + `test_ck_nav_s2_canonical_v3.py`.

---

## 4. Arbitrages fonctionnels (MOA)

| Sujet | Doctrine retenue Dev | Besoin GO MOA ? |
|---|---|---|
| Libellé menu catégorie | Suit `category.name` au resync (édition BO du seul `name` menu réalignée) | Confirmer |
| Séquence BO | Conservée (`preserve_existing_sequence`) | Non (déjà acté CK-NAV-003b) |
| « Soin & Bien-être » / rayons V2.2 | Uniquement si catégorie exposable — plus d’injection mega | Non |
| Communauté / Espace pro / Nos producteurs | Absents après sync V3 | Non |

---

## 5. Tests

**Commande (worktree S2, DB jetable) :**
```bash
export CK_ADDONS_PATH=worktree:odoo19-addons-dorevia-s2-nav
# Important : dbfilter du odoo.conf local force sinon ck_marketone_local
docker compose -f docker-compose.yml -f docker-compose.local.yml run --rm --no-deps odoo \
  odoo -d ck_s2_nav_test --db-filter='^ck_s2_nav_test$' \
  -i dorevia_ck_theme,dorevia_ck_marketone_content \
  --test-enable --stop-after-init --without-demo=all --log-level=test \
  --test-tags=/dorevia_ck_marketone_content:dorevia_ck_nav_s2,dorevia_ck_nav_catalogue,dorevia_ck_nav_v1,dorevia_ck_nav_communaute,dorevia_ck_nav_axe_b,dorevia_ck_marketone_nav_sync
```

**Résultat :** `0 failed, 0 error(s) of 55 tests` (exit 0).

Couverture S2 : 1ʳᵉ création, idempotence structurée, pas de doublons, séquences BO, un root/entrée, liens catégories, absence résidus V1/V2.2, rename catégorie, catégorie archivée, délégation V1/V2.2, bootstrap multi-alias, header mobile (groupe « Nos univers »), multi-site si possible, split desktop/mobile.

---

## 6. Interdictions respectées

- Pas de déploiement / préprod
- Pas de merge `main`
- Pas de push
- Travail hors dépôt local verrouillé (worktree isolé)
- Mount local restauré sur `../odoo19-addons-dorevia` après les tests
