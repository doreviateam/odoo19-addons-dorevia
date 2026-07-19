# Contrôle Garant S2-A — Navigation V3 canonique

**Verdict : PASS AVEC RÉSERVES**

| Référence | Valeur |
|---|---|
| Dépôt / worktree | `odoo19-addons-dorevia-s2-nav` |
| Branche | `refactor/s2-canonical-navigation-v3` |
| Commit contrôlé | `c39ce6329f06625efb218198c7aba01046bea010` |
| Head inchangé | confirmé avant et après contrôle |
| Module | `dorevia_ck_marketone_content` **19.0.1.96.0** |
| Thème (install test) | `dorevia_ck_theme` **19.0.1.129.0** |
| Date | 2026-07-19 |

**Recommandation :** autoriser la **recette QA** sur ce commit. Les réserves ne bloquent pas le chemin d’install/upgrade ni les wrappers V1/V2.2/mega ; elles portent sur une dette résiduelle de writers secondaires / helpers morts.

---

## 1. Autorité unique — conforme

| Contrôle | Résultat |
|---|---|
| `hooks.bootstrap_all_marketone_content` → `bootstrap_ck_catalogue_navigation` uniquement | OK (`hooks.py` ~1159–1164) |
| `bootstrap_ck_navigation` / `sync_ck_navigation_for_website` | Délégation stricte V3 + warning (`nav_sync.py` 479–498) |
| `bootstrap_ck_navigation_v1` / `sync_ck_navigation_v1_for_website` | Délégation stricte V3 + warning (`nav_sync.py` 505–523) — **plus aucune purge avant délégation** |
| Mega BO `CkMegaMenuVisualBlock` / `CkMegaMenuRayonVisual` | Appellent `bootstrap_ck_catalogue_navigation` |
| Migration `19.0.1.96.0` | Resync V3 uniquement |

Les migrations historiques qui appellent encore `bootstrap_ck_navigation` / `_v1` sont **sûres** : signatures publiques inchangées, corps = délégation V3.

---

## 2. Absence d’effets destructifs — conforme sur le chemin principal

- Ancienne purge V1 de `MANAGED_V22_ROOT_NAMES` (dont Épicerie) **supprimée** du wrapper.
- Cleanup V3 (`_cleanup_ck_catalogue_root_menus`, ~609–654) **préserve** les racines fixes et les catégories éligibles (par `ck_nav_category_id` ou nom) ; retire chrome mega/CSS sans unlink destructif.
- Épicerie éligible n’est plus supprimée avant upsert.

**Réserve R1 (Moyenne)** — writers secondaires encore autonomes :

- `sync_communaute_header` / `_sync_communaute` (`nav_sync.py` 315–355) **recrée** encore « Communauté » (CSS V2.2). Non appelé par hooks/upgrade courants, mais API publique encore utilisable (tests + migrations historiques). Un resync V3 ultérieur purge Communauté — pollution temporaire possible.
- `sync_shop_root_icon_header` (`nav_sync.py` 357+) peut réinjecter « Tous nos produits » (même logique).

---

## 3. Identité stable — conforme avec réserve mineure

- Matching prioritaire `ck_nav_category_id` puis fallback `name` (`_upsert_menu` 113–134).
- Champ `Many2one` `product.public.category`, `ondelete='set null'` (`website_menu.py` 12–17).
- Domaine upsert scopé `website_id` + `parent_id` → multi-site OK.
- Archivage / inéligibilité → unlink menu lié (cleanup).
- Anciens menus sans `ck_nav_category_id` : matching par nom puis rebind.

**Réserve R2 (Basse)** — pas de contrainte SQL d’unicité `(website_id, parent_id, ck_nav_category_id)` ; doublon manuel hors sync possible. Les racines fixes (Boutique / Producteurs / Professionnels) restent identifiées par `name` (attendu).

---

## 4. Idempotence — conforme

- `snapshot_ck_catalogue_navigation` compare name, url, sequence, category_id, mega, css, enfants.
- Correctif URL parent après enfants (`nav_sync.py` 183–186) traite bien le forçage Odoo `url='#'` — cause réelle de non-idempotence, pas un masquage.
- Tests : `test_catalogue_nav_idempotent`, `test_s2_structured_idempotence`, délégations V1/V2.2 même snapshot.

**Réserve R3 (Basse)** — snapshot sans `is_visible` ni id ORM menu (couverture fonctionnelle suffisante pour S2).

---

## 5. Doctrine BO — conforme (arbitrage MOA ratifié)

- Libellé = `category.name` au resync (test rename menu BO + rename catégorie).
- Séquence BO préservée (`preserve_existing_sequence=True` sur catégories / Producteurs / Pro).
- Boutique : séquence toujours forcée à 10 (préexistant ; hors doctrine « séquence rayons »).

---

## 6. Couverture fonctionnelle — auto vs QA

| Cas | Auto | QA |
|---|---|---|
| Structure type Épicerie + L2 | Oui (libellés synthétiques `Épicerie S2 Canon` / sucrée / salée) | Libellés réels seed |
| Producteurs / Professionnels conditionnel | Oui | Oui (page publiée/non) |
| Catégorie absente / archivée | Oui | Spot-check |
| Rename catégorie / séquence BO | Oui | Oui |
| Upgrade module 96.0 | Migration présente + bootstrap hooks | Upgrade local/préprod contrôlée |
| Multi-site | Oui (création 2ᵉ site) | Si multi-site réel |
| Header mobile (pas de « Nos univers », split liens) | Oui (purge + HttpCase split) | Recette visuelle mobile |
| Doubles exécutions / pas de mega V2.2 | Oui | Resync manuel ×2 |

**Réserve R4 (Basse)** — sur fresh-install, skips : seed MOA incomplet ; `test_v1_does_not_purge_epicerie_when_exposable` skip si Épicerie non exposable. Non bloquant (couvert par S2 synthétique + délégation snapshot).

---

## 7. Compatibilité / dette

- Signatures V1/V2.2 publiques conservées (délégation).
- Pas d’import circulaire détecté (`nav_sync` n’importe pas les modèles mega au top-level).
- Version `19.0.1.96.0` + `migrations/19.0.1.96.0/post-migrate.py` cohérentes.
- Tests adaptés au comportement V3 (pas affaiblis pour masquer une purge Épicerie) ; assertions Communauté/rayons V2.2 correctement retirées.

**Réserve R5 (Moyenne/Basse)** — code mort V2.2 encore présent (`_prune_unmanaged_root_menus`, `_sync_mega_rayon`, `_sync_producteurs`, …). `_prune_unmanaged_root_menus` pourrait supprimer Boutique/Professionnels **s’il était rappelé** (hors chemin runtime actuel). Dette à neutraliser/supprimer dans un ticket Dev ultérieur, pas un blocage S2-A.

---

## 8. Rejeu tests indépendants Garant

**Commande exacte :**
```bash
export CK_ADDONS_PATH=worktree:odoo19-addons-dorevia-s2-nav
docker compose -f docker-compose.yml -f docker-compose.local.yml run --rm --no-deps odoo \
  odoo -d ck_s2_garant_test \
  --db-filter='^ck_s2_garant_test$' \
  -i dorevia_ck_theme,dorevia_ck_marketone_content \
  --test-enable --stop-after-init --without-demo=all --log-level=test \
  --test-tags=/dorevia_ck_marketone_content:dorevia_ck_nav_s2,dorevia_ck_nav_catalogue,dorevia_ck_nav_v1,dorevia_ck_nav_communaute,dorevia_ck_nav_axe_b,dorevia_ck_marketone_nav_sync
```

| Élément | Valeur |
|---|---|
| SHA testé | `c39ce6329f06625efb218198c7aba01046bea010` |
| Versions | theme `19.0.1.129.0` · content `19.0.1.96.0` |
| Résultat | **0 failed, 0 error(s) of 55 tests** — exit 0 |
| Durée | ~90 s post-tests |
| Warnings | délégation V1/V2.2 (attendus) |
| Skips | 4 (seed/Épicerie absents sur fresh DB) |
| Base jetable | `ck_s2_garant_test` **DROP** confirmé (`db_destroyed=ck_s2_garant_test`) |
| Mount local | restauré sur `odoo19-addons-dorevia` |

---

## Constats par sévérité

### Moyenne
1. **R1** — `sync_communaute_header` / `sync_shop_root_icon_header` restent des writers non canoniques.
2. **R5** — helpers V2.2 morts mais potentiellement destructifs s’ils sont rappelés.

### Basse
3. **R2** — pas d’unicité SQL sur `ck_nav_category_id`.
4. **R3** — snapshot d’idempotence sans `is_visible`.
5. **R4** — libellés MOA littéraux / Épicerie seed à valider en QA.

### Info
- Warnings de dépréciation V1/V2.2 = preuve de délégation.
- Doctrine libellé `category.name` ratifiée MOA — alignée code/tests.

---

## Points QA (après PASS Garant)

1. Desktop + mobile : Boutique · Épicerie · Épicerie sucrée/salée · Producteurs · Professionnels ; accueil icône maison.
2. Aucun mega-menu V2.2 / Communauté / Espace pro / Nos producteurs.
3. Deux resync successives → même header (pas de doublon, séquences BO inchangées).
4. Rename catégorie en BO → libellé menu suit ; rename manuel menu seul → réaligné au resync.
5. Professionnels disparaît si page dépubliée.
6. Drawer / split mobile : liens catégorie réels (pas `#` sur le libellé parent).

---

## Suite

- **QA :** GO pour recette sur ce SHA.
- **Dev (hors S2-A, ticket dette) :** neutraliser `sync_communaute_header` / `sync_shop_root_icon_header` et retirer ou stubber les helpers V2.2 morts (`_prune_unmanaged_*`, `_sync_mega_*`, …).
- **Garant :** aucun amend / push / PR / déploiement effectué.
