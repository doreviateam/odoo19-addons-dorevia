# Conditions de test et destruction des environnements jetables

## Conditions communes

- Worktree isolé branche `refactor/s2-canonical-navigation-v3`
- Mount addons via `CK_ADDONS_PATH` pointant vers ce worktree
- Bases PostgreSQL **jetables** (jamais `ck_marketone_local` / préprod)
- `--db-filter` explicite pour éviter le filtre local forçant une autre DB
- `--without-demo=all` · `--stop-after-init` pour les suites automatisées
- Aucun push / déploiement pendant les recettes

## Commande type (suite navigation S2)

```bash
export CK_ADDONS_PATH=<worktree-s2>
docker compose -f docker-compose.yml -f docker-compose.local.yml run --rm --no-deps odoo \
  odoo -d ck_s2_nav_test --db-filter='^ck_s2_nav_test$' \
  -i dorevia_ck_theme,dorevia_ck_marketone_content \
  --test-enable --stop-after-init --without-demo=all --log-level=test \
  --test-tags=/dorevia_ck_marketone_content:dorevia_ck_nav_s2,dorevia_ck_nav_catalogue,dorevia_ck_nav_v1,dorevia_ck_nav_communaute,dorevia_ck_nav_axe_b,dorevia_ck_marketone_nav_sync
```

Tags utiles : `dorevia_ck_nav_s2` (idempotence + collisions), `dorevia_ck_nav_catalogue`.

## Contre-recette mobile 390×844 (GO final)

| Paramètre | Valeur |
|---|---|
| SHA | `58327b68faa80404a006df7417809bb3953790ea` |
| Viewport | `390 × 844` |
| Navigateur | Chromium (API Playwright) |
| Upgrade | `19.0.1.98.0` → `19.0.1.99.0` + double resync |
| Verdict | **GO QA** |

## Bases / instances détruites (confirmé)

| Nom / usage | Destruction |
|---|---|
| `ck_s2_nav_test` (+ variantes Dev) | DROP après suites |
| `ck_s2_garant_test` | DROP confirmé (`db_destroyed`) |
| `ck_s2_home_icon_test` | DROP après correctif icône |
| `ck_s2_qa_20260719` (+ compose QA éphémère) | Instance + volumes supprimés |
| Instances mobile QA `58327b6` / `77197a3` | Conteneurs + volumes supprimés ; preuves conservées dans cette archive |

Artefacts éphémères hors dépôt (vidéos tmp, overrides compose) : **non archivés** volontairement.
