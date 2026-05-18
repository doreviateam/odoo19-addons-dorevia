# Recette manuelle — Lot 6.2 (porte Origines)

| Champ | Valeur |
|-------|--------|
| **Lot** | 6.2 — Porte Origines |
| **Module** | `19.0.7.0.0` |
| **Statut** | **GO MOA** (2026-05-18) — `19.0.7.0.0` |
| **Base** | `ckr-marketone-01` — http://localhost:18079 |
| **Ticket exécution** | [`TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md`](../tickets/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md) |

---

## Avant de commencer

1. **Mise à jour module** : `-u dorevia_ckreyol_marketone` sur la base de recette.
2. **Daemon long-running** : redémarrer Odoo après `-u` pour que **`GET /origines`** réponde en **301** (sinon **404**).
   ```bash
   docker compose -f ~/sandbox-odoo19/docker-compose.yml restart odoo
   ```
3. **En-tête base** (navigateur ou extension) : `X-Odoo-Database: ckr-marketone-01` si multi-bases.

---

## Prérequis BO (obligatoires pour points 4, 6, 10)

| Élément | Où | Détail |
|---------|-----|--------|
| Attribut **Origine** | Catalogue | Multi-valeurs, **sans** variante — créé par le module |
| Valeurs attribut | Produits | Ex. Guadeloupe, Martinique — rattachées aux fiches |
| Profils **`marketone.shop.origin`** | Site → Configuration → **Origines (porte shop)** | Slug, nom visiteur, phrase courte, **publié**, `website_id` = **My Website** |
| Produit test | Boutique | Au moins 1 produit publié avec valeur **Origine** + profil publié sur le même slug |

> **Sandbox 2026-05-18** : la base `ckr-marketone-01` peut avoir **0** profil `marketone.shop.origin` après les tests auto (données transactionnelles). Créer **2 profils** avant la recette facettes / fiche produit.

---

## Parcours MOA (10 points)

Cocher **OK** ou **KO** après vérification **navigateur** (desktop + mobile pour le point 9).

| # | Test | Procédure | Attendu | OK | KO | Notes |
|---|------|-----------|---------|----|----|-------|
| **1** | Alias `/origines` | `GET /origines` (sans suivre la redirection dans l’onglet Réseau) | **301** → `Location: /shop?marketone_mode=origin` | ☑ | ☐ | |
| **2** | Mode Origines | Ouvrir `/shop?marketone_mode=origin` | **200** ; bandeau `marketone-shop-origin-intro` ; titre **Origines** | ☑ | ☐ | |
| **3** | Mode seul = catalogue complet | Comparer le **nombre de produits** (ou la grille) avec `/shop` nu | Même périmètre catalogue ; bandeau Origines en plus | ☑ | ☐ | |
| **4** | Facette `marketone_origin` | URL `/shop?marketone_mode=origin&marketone_origin=guadeloupe` | Grille **filtrée** | ☑ | ☐ | Profils `guadeloupe`, `martinique` |
| **5** | Slug invalide | `/shop?marketone_mode=origin&marketone_origin=slug-inconnu` | **302** → `/shop` nu ; pas de **500** | ☑ | ☐ | |
| **6** | Fiche produit | Fiche avec **Origine** + profil publié | Bloc **Origines** ; lien vers porte filtrée | ☑ | ☐ | Ex. lien `…&marketone_origin=martinique` |
| **7** | Non-régression featured | `/shop?marketone_mode=featured` | Bandeau **Incontournables** ; pas Origines | ☑ | ☐ | |
| **8** | Tunnel achat | Panier → checkout | **200** ; tunnel OK | ☑ | ☐ | |
| **9** | Mobile | Viewport **375 px** | Pas de débordement horizontal | ☑ | ☐ | |
| **10** | Modèle minimal | BO + `/shop` mode Origines | Modèle minimal ; pas hub Culture | ☑ | ☐ | 3 produits + attribut Origine |

### Périmètre modèle `marketone.shop.origin` (point 10)

| Présent (OK) | Absent (interdit Lot 6.2) |
|--------------|---------------------------|
| `slug`, `name_visitor`, `context_phrase`, `website_published`, `website_id`, lien `attribute_value_id` | Page website dédiée, snippets hero territoire |
| Liste / formulaire BO sobres | Champs HTML long, galerie, FAQ, SEO éditorial |
| Bandeau **court** sur `/shop` | Hub Culture, récit territoire, carte interactive |

---

## Pré-contrôles HTTP (sandbox, post-restart)

Contrôles automatiques utiles avant la passe MOA (ne remplacent pas le navigateur) :

```bash
# 1 — 301
curl -sI -H "X-Odoo-Database: ckr-marketone-01" http://localhost:18079/origines | grep -E 'HTTP|Location'

# 2 — bandeau
curl -s -H "X-Odoo-Database: ckr-marketone-01" \
  'http://localhost:18079/shop?marketone_mode=origin' | grep -q marketone-shop-origin-intro && echo OK

# 5 — slug invalide
curl -sI -H "X-Odoo-Database: ckr-marketone-01" \
  'http://localhost:18079/shop?marketone_mode=origin&marketone_origin=slug-inconnu' | grep -E 'HTTP|Location'
```

---

## Tests auto (référence)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_smoke,dorevia_marketone_lot2,dorevia_marketone_lot2_1,dorevia_marketone_lot3,dorevia_marketone_lot4,dorevia_marketone_lot5,dorevia_marketone_lot6_1_featured,dorevia_marketone_lot6_2_origin \
  --http-port=8071
```

**Résultat attendu** : 76 tests, **0** échec.

---

## Réserves d’exploitation

| # | Réserve | Mitigation |
|---|---------|------------|
| R1 | Alias `/origines` en **404** après `-u` sans redémarrage daemon | Redémarrer Odoo (comme `/incontournables`, Lot 6.1) |

---

## Verdict MOA

| Décision | ☑ |
|----------|---|
| **GO** | ☑ |
| **GO avec réserves** | |
| **NO GO** | |

**Date** : 2026-05-18 · **Validé par** : MOA recette manuelle

**Prérequis BO recette** : profils `guadeloupe` et `martinique` publiés sur **My Website** ; 3 produits avec attribut **Origine**.
