# Recette QA — Navigation « Communauté » · 19.0.1.39.0 → 19.0.1.40.0

| Champ | Valeur |
|---|---|
| Projet | `dorevia_ck_marketone` |
| Ticket | Navigation « Communauté » — remplacement de « Coups de cœur » dans le header |
| Version livrée | `dorevia_ck_marketone_content` 19.0.1.40.0 (correctif de 19.0.1.39.0) |
| Date recette | 2026-06-25 |
| Rédacteur | QA expert Odoo |
| Base | `dorevia_ck_marketone_01` |
| Méthode | Requêtes SQL directes · HTTP authentifié · Tests Odoo par tag |

---

## Historique du cycle de recette

| Version | Verdict | Motif |
|---|---|---|
| 19.0.1.39.0 | **NO GO** | Régression 1 : 6 produits dépubliés · Régression 2 : 3 entrées menu supprimées |
| 19.0.1.40.0 | **GO** | Régressions corrigées · 31/31 tests au vert · état catalogue et navigation conformes |

---

## Périmètre de la livraison

Le ticket couvre uniquement :
- Suppression de l'entrée « Coups de cœur » du menu header racine (N2)
- Création d'une entrée « Communauté » placeholder (`href="#"`) à la même position
- Garde-fou `catalog_seed_guard.py` : 7 produits seed republiés si dépubliés
- Sync chirurgical `sync_communaute_header()` : opère sur l'entrée menu uniquement, sans bootstrap complet

**Hors périmètre confirmé :**
- Home section « Nos coups de cœur » → inchangée
- Cards produit et catégories boutique → inchangées
- Mega-menus internes aux rayons (liens « Coups de cœur » N3) → conservés, hors ticket
- Catégorie BO `product_public_category` id=24 → toujours en base, non exposée au header

---

## Résultats de recette — 19.0.1.40.0

### 1. Versions modules

| Module | Version attendue | Version constatée | OK |
|---|---|---|---|
| `dorevia_ck_marketone_content` | 19.0.1.40.0 | 19.0.1.40.0 | ✅ |
| `dorevia_ck_theme` | 19.0.1.56.0 | 19.0.1.56.0 | ✅ |

---

### 2. Tests automatisés

```
Tags : dorevia_ck_nav_communaute · dorevia_ck_header_v22 · dorevia_ck_marketone_nav_sync
```

| Résultat | Valeur |
|---|---|
| Tests exécutés | 31 |
| Réussis | **31** |
| Échecs | 0 |
| Erreurs | 0 |

Couverture confirmée :
- `sync_communaute` ne dépublie pas le catalogue seed
- `ensure_moa_seed_catalog_published` restaure 7 produits si dépubliés
- Boissons / Maison & Bien-être / Artisanat présents après guard + bootstrap

---

### 3. Catalogue produits

| Contrôle | Attendu | Constaté | OK |
|---|---|---|---|
| Produits publiés | 7 | **7** | ✅ |
| Produits dépubliés (commerciaux) | 0 | **0** | ✅ |
| Produit test dépublié | `is_published=false` | `is_published=false` | ✅ |

Produits publiés confirmés : Chapeau Panama · Confiture de goyave · Jus Mont-Pelé · Manio Crackers · Pâte de manioc · Savon vétiver · Galettes de manioc.

---

### 4. Navigation menu

| Contrôle | Attendu | Constaté | OK |
|---|---|---|---|
| Total entrées menu (website_id=1) | 13 | **13** | ✅ |
| « Coups de cœur » absent du menu racine | 0 occurrence | **0** | ✅ |
| « Communauté » présente (url="#") | id=598, url=# | id=598, url=# | ✅ |
| Boissons présente | ✅ | id=602 ✅ | ✅ |
| Maison & Bien-être présente | ✅ | id=603 ✅ | ✅ |
| Artisanat présente | ✅ | id=604 ✅ | ✅ |
| Espace pro et sous-entrées | ✅ | ✅ | ✅ |
| Nos producteurs présente | ✅ | ✅ | ✅ |

Menu complet post-fix :

```
Menu principal
├── Tous nos produits         → /shop
├── Épicerie                  → /shop/category/epicerie-1
├── Boissons                  → /shop/category/boissons-123
├── Maison & Bien-être        → /shop/category/soin-bien-etre-2
├── Artisanat                 → /shop/category/artisanat-3
├── Communauté                → #                           ← nouveau
├── Nos producteurs           → /nos-producteurs
└── Espace pro                → #
    ├── Acheter pour mon commerce
    ├── Demander les conditions pro
    ├── Devenir partenaire / distributeur
    └── Contacter C-Kréyòl
```

**Note** : les entrées Boissons (602), Maison & Bien-être (603), Artisanat (604) portent de nouveaux IDs suite à la migration réparation. Comportement attendu — ces entrées ont été supprimées par la 19.0.1.39.0 et recréées par la 19.0.1.40.0.

---

### 5. Smoke test HTTP

| URL | Code attendu | Code constaté | OK |
|---|---|---|---|
| `/odoo/shop` | 200 | 200 | ✅ |
| `/` | 200 | 200 | ✅ |
| `/odoo/shop/cart` | 200 | 200 | ✅ |
| `/odoo/nos-producteurs` | 200 | 200 | ✅ |
| `/odoo/professionnels` | 200 | 200 | ✅ |
| `/shop/category/coups-de-cœur-24` | 200 (catégorie en DB) | 200 | ✅ |

La page `/shop/category/coups-de-cœur-24` retourne 200 car la catégorie existe toujours en base — elle n'est pas liée au header et n'est pas exposée dans la navigation. Comportement conforme au périmètre du ticket.

---

### 6. Home — section « Nos coups de cœur »

Contrôle HTML sur `/` : mentions `featured` et `coups` présentes dans le HTML. La section Home pilotée par `ck_is_featured` est **inchangée** — conforme au périmètre livré.

---

## Observations hors périmètre

Ces points ne bloquent pas le GO mais sont à tracer pour les lots suivants.

### OBS-1 — « Communauté » sans traduction fr_FR dans `website_menu`

L'entrée id=598 a `name = {"en_US": "Communauté"}` sans entrée `fr_FR`. En interface française, Odoo utilise le fallback `en_US` — le label s'affiche correctement mais la structure de données est incomplète.

**Action** : ajouter `fr_FR = "Communauté"` via BO Site web > Menu, ou dans la prochaine livraison. Hors périmètre ticket actuel.

### OBS-2 — « Maison & Bien-être » reconstruit sans correction de libellé

L'entrée menu Maison & Bien-être (id=603) est recréée avec le même libellé `"Maison & Bien-être"` que l'originale (590) — l'incohérence avec la catégorie BO « Soin & Bien-être » subsiste. Point documenté dans [PROTOCOLE_QA_AXE_C_SECURISATION_BO_20260624.md](PROTOCOLE_QA_AXE_C_SECURISATION_BO_20260624.md) action 9, correction BO MOA à venir dans l'Axe C.

### OBS-3 — Catégorie « Coups de cœur » toujours en base avec 3 produits

4 produits étaient assignés avant la livraison ; 3 le sont encore (la 4e affectation a disparu lors du cycle 39.0 / correctif 40.0). Ce delta est à vérifier. La catégorie reste non exposée au header mais la décision MOA-1 (supprimer ou vider) reste ouverte. Cf. [PROTOCOLE_QA_AXE_C_SECURISATION_BO_20260624.md](PROTOCOLE_QA_AXE_C_SECURISATION_BO_20260624.md).

---

## Verdict

**GO — livraison 19.0.1.40.0 recevable dans le périmètre défini.**

| Critère | Résultat |
|---|---|
| « Coups de cœur » absent du header | ✅ |
| « Communauté » présente (href="#") | ✅ |
| Catalogue 7/7 produits publiés | ✅ |
| Navigation complète (Boissons, Artisanat, Maison & Bien-être) | ✅ |
| Routes HTTP 200 | ✅ |
| Tests 31/31 au vert | ✅ |
| Home inchangée | ✅ |
| Régressions 19.0.1.39.0 corrigées | ✅ |

**Passages Axe C** : ce ticket solde l'action 2 du protocole de sécurisation (suppression entrée menu). Les actions 1, 3, 4, 5, 6, 7, 8, 9, 10 restent ouvertes et relèvent des corrections BO/MOA et du ticket Dev `ck_is_featured`.

---

> *Recette réalisée sur `dorevia_ck_marketone_01` · `dorevia_ck_marketone_content` 19.0.1.40.0 · 2026-06-25.*
