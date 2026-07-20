# R-A2 — Mise sous contrôle Git de `dorevia_ck_preprod_guard`

**Date :** 2026-07-20  
**Branche :** `chore/track-preprod-guard`  
**Base :** `origin/main @ 756112092daae8e24a5828f1eec6f2815d4786b6`  
**Mandat :** intégration byte-identique, aucune évolution fonctionnelle.

---

## 1. Contexte

Le module `dorevia_ck_preprod_guard` (v`19.0.1.2.0`) était **installé en préproduction** et présent sur le disque hôte, mais **absent de tout dépôt Git** (`??` / 0 fichier suivi).  
S4-SAFE (`OPID S4SAFE_20260720_071946Z`) a préservé le module vivant et prouvé l’identité archive ↔ vivant.

**Avertissement :** ne pas exécuter `git clean` sur la préproduction avant fusion et mise à disposition de ce module depuis Git.

---

## 2. Références d’identité

| Élément | Valeur |
|---|---|
| Module vivant (hôte) | `/home/dorevia/ck-marketone-preprod/odoo19-addons-dorevia/dorevia_ck_preprod_guard` |
| Archive | `dorevia_ck_preprod_guard_S4SAFE_20260720_071946Z.tar.gz` |
| OPID | `S4SAFE_20260720_071946Z` |
| SHA-256 archive | `395c793913befd7a47234a9c29cf2402f784a5241a6adec5b7871070823f270c` |
| Fichiers | **8** |
| Version manifeste | **19.0.1.2.0** |

```text
live_module_vs_archive = identical
file_count             = 8
archive_checksum       = 395c793913befd7a47234a9c29cf2402f784a5241a6adec5b7871070823f270c
live_vs_git            = no_difference
archive_vs_git         = no_difference
```

### Checksums SHA-256 (identiques live / archive / Git)

| Fichier | Taille | SHA-256 |
|---|---|---|
| `__init__.py` | 1123 | `18df2cbe645a525971bc8e95152386e1fcc2d78486b88d7326d7a9b71323d9cb` |
| `__manifest__.py` | 823 | `5c2222f2d2fa38dee80c1d1c36a55e1647634ca4358ce4bb4f6b2d83ee5a2df6` |
| `guards.py` | 1909 | `21c5f757a71cd6182a1db701ada35dffb3f1b907cbb77f02561ac61e735c30ef` |
| `models/__init__.py` | 46 | `7fa4c37e9a4785f75e71d8b16fc15bcf45e7f26f5b50025e485f3aed3bf3f7a4` |
| `models/website.py` | 513 | `4f08cfbe7d1e2f0c7bbaa0b1ad061f04a8eb34587a3e53a5f70395d9ffbc98d9` |
| `runtime.py` | 1372 | `7b0a4ffe2bbc4d4947edc6ed5616e41946b72516037d8b15e4f5d34e9e0d1840` |
| `views/ck_soft_launch_auth_cta.xml` | 1335 | `f0acc162a4ec81e852b0328a3223ef6545a5c66510a95e0118e269aa3c52e81c` |
| `views/ck_soft_launch_p1.xml` | 2413 | `b6752c4433a0f81b4ded54e06a8d1d5029232eb4dfabd3d18086f9f6abb469d2` |

Commandes : `diff -r` live↔Git et archive↔Git → **aucune différence**.

---

## 3. Contrôle de contenu

Recherche secrets / clés / tokens / dumps / caches / chemins hôte :

**aucun finding.**  
Les constantes `EXPECTED_DOMAIN` / `EXPECTED_DATABASE` / `EXPECTED_ENV` sont le contrat fonctionnel du module (pas des secrets).

---

## 4. Comportement du `pre_init_hook`

Variables exigées à **l’installation** (logique AND) :

* `CK_SOFT_LAUNCH_ENV` = `preprod`
* `CK_SOFT_LAUNCH_DOMAIN` = `preprod-ck.doreviateam.com`
* `CK_SOFT_LAUNCH_DATABASE` = `ck_marketone_preprod`

| Chemin | `pre_init_hook` | Variables |
|---|---|---|
| **Installation** (`-i`) | **exécuté** — fail-closed si écart | **obligatoires** |
| **Mise à jour** (`-u`) | **non rejoué** (Odoo 19 constaté) | non requises pour l’upgrade |
| **Démarrage normal** | non concerné | non requises ; gardes runtime via `runtime.py` (domaine / base) |

Le conteneur préprod vivant ne définit actuellement pas ces trois variables : le module est **installé mais non réinstallable** sans configuration canonique (chantier **R-A3**).  
**On ne relâche pas le hook** dans R-A2.

---

## 5. Contrôles statiques

| Contrôle | Résultat |
|---|---|
| `python3 -m py_compile` (5 fichiers `.py`) | OK |
| Manifeste `19.0.1.2.0`, `pre_init_hook`, `auto_install=False` | OK |
| XML `views/*.xml` well-formed | OK |
| Import `guards` + `pre_init_hook` export | OK |
| Scan secrets / parasites | aucun |

---

## 6. Tests Odoo 19 jetables (local Docker, hors préprod)

### Installation positive

* Base jetable locale nommée `ck_marketone_preprod` (Postgres local `ck_project-db-1`, **pas** l’hôte préprod)
* Variables fournies temporairement au conteneur de test uniquement
* Résultat : `installed` · `19.0.1.2.0` · xmlids P4 présents (`ck_soft_launch_p1_hide_purchase`, CTA, auth)

### Tests négatifs (base `ck_ra2_neg1`, puis droppée)

| Cas | Exit | Erreur typique | État module |
|---|---|---|---|
| Variables absentes | 255 | `CK_SOFT_LAUNCH_ENV absent` (+ domain/db) | `uninstalled` |
| ENV incorrecte | 255 | `CK_SOFT_LAUNCH_ENV='production' ≠ 'preprod'` | `uninstalled` |
| DOMAIN incorrect | 255 | domain ≠ attendu | `uninstalled` |
| DATABASE incorrecte | 255 | database / runtime ≠ attendu | `uninstalled` |

Aucune installation partielle dangereuse.

### Test d’upgrade

```text
pre_init_hook_on_upgrade = not_executed
upgrade_result           = success
p4_guards_after_upgrade  = active   # 6 ir_model_data ; state=installed 19.0.1.2.0
```

Upgrade `-u dorevia_ck_preprod_guard` **sans** les trois variables : succès ; aucune trace de `pre_init_hook` / `GuardError` dans les logs.

---

## 7. Raison de l’intégration tardive

Le module a été déployé et itéré hors dépôt pour le soft-launch / P4, puis découvert hors Git lors de la revue S4.  
S4-SAFE a gelé le binaire vivant ; R-A2 le rend traçable **sans modifier une ligne**.

---

## 8. Risques résiduels / suite

* **R-A3** — déclarer les trois variables dans la configuration canonique du service préprod (réinstallabilité / reconstruction).
* Ne pas lancer `-i dorevia_ck_preprod_guard` en préprod tant que R-A3 n’est pas en place.
* `git clean` préprod reste dangereux jusqu’à fusion + déploiement du module depuis Git.
* Aucun GO de déploiement dans ce mandat.

---

## 9. Interdictions respectées

Aucun push, PR, merge, déploiement, modification préprod, assouplissement du hook, changement de version.
