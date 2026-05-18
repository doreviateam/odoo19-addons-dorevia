# Recette manuelle — Culture v1 — page territoire pilote

| Champ | Valeur |
|-------|--------|
| **Module** | `dorevia_ckreyol_marketone` `19.0.8.0.0` |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079 |
| **Univers** | Culture — découvrir |
| **ADR** | ADR-026 |
| **Contrat** | C8 |
| **Statut recette** | **GO MOA** (2026-05-18) |

---

## Prérequis BO

| Élément | Détail |
|---------|--------|
| Profil origine | `marketone.shop.origin` publié sur **My Website** |
| Slug pilote | `guadeloupe` (aligné URL Culture et facette Boutique) |
| Attribut | Valeur **Origine** liée au profil |
| Phrase courte | Champ **Phrase courte** (`context_phrase`) — chapô page Culture |
| Produits | Au moins 1 produit publié avec cette origine (pour CTA achetable) |

**Pas** de page hub `/culture`. **Pas** d’entrée menu header Culture.

---

## Exploitation

Après `-u dorevia_ckreyol_marketone`, redémarrer le daemon Odoo si la route `GET /culture/<slug>` répond **404** alors que le profil est publié (même comportement que `/origines`).

```bash
docker compose -f /Users/doreviateam/sandbox-odoo19/docker-compose.yml restart odoo
```

---

## Grille de recette

| # | Scénario | URL / action | Attendu | MOA | Tech |
|---|----------|--------------|---------|-----|------|
| **1** | Page territoire pilote | `/culture/guadeloupe` | **200**, classes `marketone-culture`, titre territoire, chapô, 2 sections courtes, CTA achetable | ☑ | ☑ |
| **2** | Slug inconnu | `/culture/territoire-inconnu` | **404** propre | ☑ | ☑ |
| **3** | CTA principal | Clic « Acheter les produits de ce territoire » | `/shop?marketone_mode=origin&marketone_origin=guadeloupe`, grille filtrée | ☑ | ☑ |
| **4** | CTA secondaire | « Tous les produits » | `/shop` nu | ☑ | ☑ |
| **5** | Bandeau Origines facetté | `/shop?marketone_mode=origin&marketone_origin=guadeloupe` | Lien discret « Découvrir ce territoire » → `/culture/guadeloupe` | ☑ | ☑ |
| **6** | Bandeau Origines seul | `/shop?marketone_mode=origin` | **Pas** de lien Découvrir | ☑ | ☑ |
| **7** | Fiche produit | Produit avec origine Guadeloupe | Lien origine → porte filtrée ; lien **Découvrir** → `/culture/guadeloupe` | ☑ | ☑ |
| **8** | Non-régression Incontournables | `/shop?marketone_mode=featured` | Bandeau featured inchangé, pas de Culture | ☑ | ☑ |
| **9** | Non-régression alias | `/origines`, `/incontournables` | **301** inchangés | ☑ | ☑ |
| **10** | Sobriété éditoriale | Page Culture | Courte (quelques scrolls), **pas** encyclopédique ni grille produits ; mobile 375 px OK | ☑ | ☑ |

---

## Tests automatisés

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_culture_v1,dorevia_marketone_lot6_2_origin \
  --http-port=8071
```

Non-régression complète (Lots 1–6.2 + Culture v1) : **85** post-tests, **0** failed — tags `dorevia_marketone_smoke` … `dorevia_marketone_culture_v1` (voir [`ENV_REFERENCE.md`](ENV_REFERENCE.md)).

---

## Critère GO Culture v1

Un visiteur atteint `/culture/<slug-pilote>`, comprend le territoire en quelques scrolls, puis peut acheter via `/shop?marketone_mode=origin&marketone_origin=<slug>`, **sans régression** des portes Boutique.

**Décision MOA** : **GO Culture v1** — 2026-05-18.
