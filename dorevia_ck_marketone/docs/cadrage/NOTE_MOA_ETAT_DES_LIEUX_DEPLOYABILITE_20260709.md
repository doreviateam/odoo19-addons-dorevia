# Note MOA — État des lieux — Déployabilité et socle technique (9 juillet 2026)

| Champ | Valeur |
| --- | --- |
| Date | 9 juillet 2026 |
| Projet | C-Kréyòl Marketone — boutique en ligne Odoo 19 CE |
| Destinataires | MOA, Produit, QA, Exploitation |
| Statut | **GO technique — install fraîche validée, prêt pour enrichissement MOA et préparation prod** |
| URL locale (référence équipe) | http://localhost:18080 |
| Base locale (travail courant) | `ck_marketone_local` (clone enrichi) · base « vierge » recette : `ck_marketone` |
| Version thème | `dorevia_ck_theme` **19.0.1.120.0** |
| Version contenu | `dorevia_ck_marketone_content` **19.0.1.86.0** |
| Commit deploy | `12a546b` — `ck-marketone-deploy` `main` |
| Commit modules | `39203542` — `odoo19-addons-dorevia` `main` (PR #84 mergée) |

---

## Synthèse exécutive

Le chantier **déployabilité install fraîche** est **clos et recetté**. Une nouvelle machine (ou un nouveau serveur) peut installer C-Kréyòl Marketone **sans reprendre l’instance historique**, avec la même structure de fichiers qu’en production.

**Ce qui est garanti aujourd’hui :**

- Installation automatisée (`make install`) sur base neuve
- Contrôle qualité automatisé (`make verify`) — **6 points**, dont le hero homepage **réellement rendu** en navigateur
- Boutique pilote fonctionnelle (`/shop`, produits démo, branding C-Kréyòl)
- Socle Docker **aligné prod** (nginx, workers, TLS activable par configuration)

**Ce qui n’est pas encore fait** (décision MOA / calendrier) : mise en ligne publique (domaine, certificats HTTPS, secrets production, hébergement).

---

## 1. Contexte et objectif du chantier

### Problème initial

L’instance historique (sandbox, base enrichie manuellement) masquait des blocages sur **install fraîche** : erreurs XML à l’installation, homepage sans hero CK malgré un contrôle base « vert », page `/` globale en conflit avec la homepage site.

### Objectif MOA

| Attendu | Réalisé |
| --- | --- |
| Reproduire l’instance sur une machine neuve | ✅ |
| Même stack local / prod (fichiers identiques, `.env` différent) | ✅ |
| Séparer infra (deploy) et métier Odoo (modules) | ✅ |
| Valider le parcours acheteur pilote après install fraîche | ✅ |

### Gouvernance modules (rappel MOA §4bis)

| Module | Rôle |
| --- | --- |
| `dorevia_ck_theme` | Thème générique CK — tokens, SCSS, snippets, layout |
| `dorevia_ck_marketone_content` | Contenu métier optionnel — pages CMS, seed catalogue, newsletter |
| `dorevia_ck_marketone/` (dossier docs) | Documentation MOA, recettes, captures — **non installable** |

---

## 2. Architecture technique retenue

### Deux dépôts Git

```text
doreviateam/ck-marketone-deploy     →  Docker, scripts, nginx, Makefile, README
doreviateam/odoo19-addons-dorevia   →  modules Odoo dorevia_ck_* + docs MOA
```

Le fichier `.env` du dépôt deploy pointe vers le clone modules :

```bash
CK_ADDONS_PATH=../odoo19-addons-dorevia
```

### Modes d’exécution

| Mode | Variable | Comportement |
| --- | --- | --- |
| **Local (développement MOA)** | `CK_ENV=local` | Port direct `18080`, Mailpit, mode `--dev` |
| **Production** | `CK_ENV=prod` | nginx, workers Odoo, `proxy_mode=True` |
| **HTTPS (prod, quand prêt)** | `ODOO_TLS=on` | Redirect HTTP→HTTPS + terminaison TLS (certs requis) |

> En local, `ODOO_TLS=off` et `ODOO_PROXY_MODE=False` — **c’est normal et conforme** ; la prod activera les flags adaptés sans changer les fichiers.

### Schéma simplifié

```text
                    ┌─────────────────────────────────────┐
  Navigateur        │  CK_ENV=local : Odoo :18080         │
  ───────────────►  │  CK_ENV=prod  : nginx → Odoo        │
                    │              (+ TLS si ODOO_TLS=on) │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │  PostgreSQL + modules CK            │
                    │  dorevia_ck_theme                   │
                    │  dorevia_ck_marketone_content       │
                    └─────────────────────────────────────┘
```

---

## 3. Livrables du chantier (juillet 2026)

### 3.1 Socle de déploiement (`ck-marketone-deploy`)

| Livrable | Description |
| --- | --- |
| `docker-compose.yml` + overlays `local` / `prod` | Base db + Odoo ; prod ajoute nginx |
| `scripts/install.sh`, `verify.sh`, `backup.sh`, `restore.sh` | Parcours install, contrôle, sauvegarde |
| `scripts/fresh-install-test.sh` | Test CI local install fraîche |
| `odoo.conf.template` | Configuration Odoo générée (secrets hors Git) |
| `nginx/odoo.conf.template` | HTTP seul (défaut) |
| `nginx/odoo.conf.tls.template` | HTTPS + ACME (si `ODOO_TLS=on`) |
| `Makefile` | `make up`, `install`, `verify`, `test`, `prod-like` |
| `README.md`, `.env.example`, `REPOS.md` | Documentation équipe |

**Durcissements post-recette infra :**

- Healthcheck Odoo sans dépendance `curl` (Python)
- Proxy nginx Odoo 19 : `/websocket` (bus temps réel)
- `verify.sh` : contrôle **HTML rendu** sur `/` (plus de faux positif base seule)
- TLS activable par flag — nginx ne casse pas si certs absents

### 3.2 Modules Odoo (`odoo19-addons-dorevia` — PR #84)

| Correctif | Bénéfice MOA |
| --- | --- |
| Sidebar XML install fraîche | Plus d’erreur bloquante à l’installation |
| Homepage site-specific + suppression page `/` globale | Hero CK visible sur `/` en navigateur |
| Bootstrap hero réordonné (`post_init`) | Contenu home fiable sur base neuve |
| Migration `19.0.1.86.0` | Bases existantes realignées à la mise à jour |
| Tests `test_ck_homepage_binding` | Non-régression homepage + HTTP |

---

## 4. Recette QA — install fraîche (verdict vert)

Recette indépendante sur clone frais (juillet 2026), stack isolée, ports dédiés.

### Environnement de test

| Paramètre | Valeur |
| --- | --- |
| Deploy | `ck-marketone-deploy` @ `ebc62f0` puis `12a546b` |
| Modules | `odoo19-addons-dorevia` @ `fce23998` / `39203542` |
| URL QA | http://localhost:18480 |

### Résultats

| Contrôle | Résultat |
| --- | --- |
| `make install` | ✅ OK |
| `make verify` | ✅ **6/6** |
| Homepage `/` — hero CK, H1, CTA, 3 visuels | ✅ OK navigateur |
| Boutique `/shop` — produits pilote visibles | ✅ OK navigateur |
| Base — `GLOBAL_HOME_COUNT=0`, une page `/` site | ✅ OK |
| Conteneurs Docker | ✅ healthy |
| Logs — pas d’erreur bloquante | ✅ OK |

**Verdict QA :** verte — **merge PR #84 autorisé et effectué**.

### Les 6 points de `make verify`

1. Service Odoo répond
2. Modules CK installés (`dorevia_ck_theme` + `dorevia_ck_marketone_content`)
3. Boutique `/shop` accessible
4. Branding C-Kréyòl présent
5. **Homepage CK rendue** (hero `ck-hero--marketone-v1` ou CTA « Découvrir la boutique » dans le HTML)
6. Au moins 1 produit publié

---

## 5. État fonctionnel de la boutique pilote

### Parcours acheteur

```text
Home (hero CK) → Boutique /shop → Fiche produit → Panier → Checkout
```

Le tunnel de commande n’a pas été modifié par le chantier déployabilité.

### Contenu visible après install fraîche (exemples)

| Zone | Exemples |
| --- | --- |
| Home | Hero « C-Kréyòl — les saveurs créoles en Europe », CTA boutique / producteurs |
| Boutique | Galettes de manioc, Coffret découverte créole, … |
| Pages CMS | `/professionnels`, `/contactus`, `/a-propos`, `/recettes`, mentions légales |
| Navigation | Catalogue CK synchronisé (cf. notes NAV-003 à NAV-005) |

### Instance locale de travail MOA

L’équipe peut continuer à utiliser une base **enrichie** (`ck_marketone_local`) pour l’édition BO et les recettes visuelles. L’**install fraîche** reste le **référentiel de déployabilité** pour toute nouvelle machine ou serveur.

---

## 6. Points techniques documentés (non bloquants)

| Sujet | Explication MOA |
| --- | --- |
| `website.homepage_id` / `homepage_url` vide | Comportement Odoo 19 ; sans impact tant que `/` affiche le hero CK |
| Bootstraps idempotents | Éditions MOA en BO protégées par garde-fous anti-écrasement (pages CMS seed) |
| Mots de passe locaux (`admin` / `odoo`) | Acceptables en dev ; **à changer impérativement en prod** |
| `docs/design/.../node_modules` | Artefacts locaux maquette — non versionnés, sans impact deploy |

---

## 7. Conformité « règles de l’art » — lecture MOA

### Local (développement / recette MOA)

| Critère | Statut |
| --- | --- |
| Install reproductible | ✅ |
| Contrôles automatisés | ✅ |
| Secrets hors Git (`.env`) | ✅ |
| Séparation thème / contenu | ✅ |
| Alignement structure prod | ✅ |

### Production (préparée, non ouverte)

| Critère | Statut |
| --- | --- |
| nginx + workers | ✅ Socle prêt (`CK_ENV=prod`) |
| `proxy_mode` | ✅ Garde-fou si prod sans proxy |
| HTTPS activable | ✅ `ODOO_TLS=on` + README TLS |
| Secrets forts | ⏳ À faire jour J |
| Domaine + DNS + certs | ⏳ À planifier MOA |
| Sauvegardes planifiées | ⏳ Script `make backup` disponible ; planification à définir |

---

## 8. Commandes utiles (équipe / exploitation)

```bash
# Démarrage quotidien
make up
make verify

# Base neuve (recette ou nouveau poste)
make install

# Mise à jour modules après pull Git
make update

# Re-seed contenu CK (idempotent)
make bootstrap

# Test install fraîche (comme CI)
make test

# Sauvegarde
make backup
```

### Références Git à utiliser

```bash
# Deploy
git clone git@github.com:doreviateam/ck-marketone-deploy.git
cd ck-marketone-deploy && cp .env.example .env

# Modules
git clone git@github.com:doreviateam/odoo19-addons-dorevia.git ../odoo19-addons-dorevia

# .env
CK_ADDONS_PATH=../odoo19-addons-dorevia
```

---

## 9. Feuille de route — prochaines étapes MOA

### Court terme (sans mise en prod)

| Action | Responsable suggéré |
| --- | --- |
| Poursuivre enrichissement catalogue / pages CMS en local | MOA + Produit |
| Recettes visuelles et notes de clôture par lot | MOA + QA |
| Former les éditeurs BO (menus, vedettes, fiches produit) | MOA |

### Mise en production (quand le contenu et le calendrier le permettront)

| Étape | Détail |
| --- | --- |
| 1. Hébergement | VPS Docker, nom de domaine |
| 2. Secrets | `ODOO_ADMIN_PASSWORD`, `POSTGRES_PASSWORD` forts dans `.env` |
| 3. Configuration prod | `CK_ENV=prod`, `ODOO_PROXY_MODE=True`, `ODOO_DOMAIN=…` |
| 4. TLS | Émettre certs (Let's Encrypt webroot ou pré-prod auto-signé) → `ODOO_TLS=on` |
| 5. Deploy | `./scripts/render-config.sh` → `CK_ENV=prod make install` ou `update` |
| 6. Contrôle | `CK_ENV=prod make verify` + recette navigateur MOA |
| 7. Exploitation | Sauvegardes planifiées, procédure restauration testée |

---

## 10. Documents liés

| Document | Sujet |
| --- | --- |
| [`NOTE_MOA_LIVRAISON_20260702.md`](NOTE_MOA_LIVRAISON_20260702.md) | Navigation, home, polish (livraison précédente) |
| [`NOTE_MOA_CLOTURE_V1_BOUTIQUE_20260629.md`](NOTE_MOA_CLOTURE_V1_BOUTIQUE_20260629.md) | Gel boutique V1 |
| `ck-marketone-deploy/README.md` | Guide déploiement complet |
| `ck-marketone-deploy/REPOS.md` | Architecture deux dépôts |

---

## 11. Conclusion MOA

> **C-Kréyòl Marketone dispose d’un socle technique professionnel et d’modules validés en install fraîche.** La boutique pilote est exploitable en local pour le travail MOA. La mise en ligne publique est une **décision de calendrier et de contenu**, pas un blocage technique : l’infrastructure est prête à recevoir domaine, TLS et secrets production.

**Statut recommandé pour le comité MOA :** *chantier déployabilité — **clos*** · *enrichissement contenu / préparation go-live — **en cours***.

---

*Document rédigé le 9 juillet 2026 — équipe technique Dorevia / CK Marketone.*
