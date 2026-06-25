# Note — Clôture livraison Navigation « Communauté »

| Champ | Valeur |
|---|---|
| Projet | `dorevia_ck_marketone` |
| Statut | **Clôturé — GO** |
| Date | 2026-06-25 |
| Responsable | Dev · validation QA |
| Version | `dorevia_ck_marketone_content` **19.0.1.40.0** |
| Recette faisant foi | [RECETTE_QA_NAV_COMMUNAUTE_20260625.md](./maquette_01.2/RECETTE_QA_NAV_COMMUNAUTE_20260625.md) |
| Remplace | — |
| Remplacé par | — |

---

## Synthèse

Remplacement de l'entrée header **« Coups de cœur »** par **« Communauté »** (`href="#"`), sans impact sur la section Home « Nos coups de cœur », les cards produit ni les catégories boutique.

| Cycle | Verdict | Module |
|---|---|---|
| 19.0.1.39.0 | NO GO | bootstrap complet sur catalogue dégradé → menus rayons supprimés |
| **19.0.1.40.0** | **GO** | sync chirurgical + garde-fou catalogue + migration réparation |

**Recette finale** : 31/31 tests · 7/7 produits publiés · menu complet · routes HTTP 200.

---

## Livrables techniques

| Élément | Fichier / API |
|---|---|
| Entrée N3 Communauté | `nav_v22_config.py` · `nav_sync._sync_communaute()` |
| Sync chirurgical (sans resync rayons) | `nav_sync.sync_communaute_header()` |
| Garde-fou catalogue seed MOA | `catalog_seed_guard.py` |
| Rendu `href="#"` | `models/website_menu._clean_url()` |
| Migrations | `19.0.1.39.0` (corrigée) · `19.0.1.40.0` (réparation) |
| Tests non-régression | tag `dorevia_ck_nav_communaute` (3) + header/nav (31 total) |

---

## Protocole Axe C

| Action | Statut |
|---|---|
| **2** — retirer « Coups de cœur » du header | **Clôturée** (ce ticket) |
| 1, 3–10 | **Ouvertes** — arbitrages MOA-1/2/3 · ticket Dev `ck_is_featured` |

Référence état BO : [PROTOCOLE_QA_AXE_C_SECURISATION_BO_20260624.md](./maquette_01.2/PROTOCOLE_QA_AXE_C_SECURISATION_BO_20260624.md).

---

## Observations hors périmètre (backlog)

| ID | Observation | Piste |
|---|---|---|
| **OBS-1** | « Communauté » sans `fr_FR` dans `website_menu` | BO ou prochaine livraison i18n nav |
| **OBS-2** | Menu « Maison & Bien-être » vs catégorie BO « Soin & Bien-être » | Axe C action 9 — MOA |
| **OBS-3** | Catégorie « Coups de cœur » en base, 3 produits assignés (delta vs pré-39.0) | MOA-1 à arbitrer |

Ces points **ne remettent pas en cause** le GO.

---

## Upgrade sandbox

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 \
  -u dorevia_ck_marketone_content --stop-after-init --no-http
docker restart sandbox-odoo19-odoo-1
```

Tests ciblés :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 \
  --test-enable --stop-after-init --http-port=8079 \
  --test-tags="dorevia_ck_nav_communaute,dorevia_ck_header_v22,dorevia_ck_marketone_nav_sync"
```
