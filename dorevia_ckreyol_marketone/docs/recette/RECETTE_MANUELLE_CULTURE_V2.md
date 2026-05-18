# Recette manuelle — Culture v2 légère — territoires additionnels

| Champ | Valeur |
|-------|--------|
| **Module** | `dorevia_ckreyol_marketone` `19.0.9.0.0` |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079 |
| **ADR** | ADR-027 |
| **Contrat** | C8.v2 |
| **Statut recette** | **GO MOA** (2026-05-18) |
| **Pilote v1** | [`RECETTE_MANUELLE_CULTURE_V1.md`](RECETTE_MANUELLE_CULTURE_V1.md) — `guadeloupe` |

---

## Prérequis BO (3 territoires)

| Slug | Profil `marketone.shop.origin` | `context_phrase` | Attribut **Origine** |
|------|-------------------------------|------------------|----------------------|
| `guadeloupe` | Publié — pilote v1 | renseigné | lié |
| `martinique` | Publié | renseigné | lié |
| `reunion` | Publié | renseigné | lié |

Produits : au moins **1 produit publié** par territoire v2 avec la valeur **Origine** correspondante.

**Pas** de hub `/culture`. **Pas** de menu header Culture. **Pas** de liens croisés entre pages territoire.

---

## Exploitation

Identique v1 : après `-u`, redémarrer Odoo si `/culture/<slug>` répond **404** avec profil publié.

---

## Grille de recette

| # | Scénario | URL / action | Attendu | MOA | Tech |
|---|----------|--------------|---------|-----|------|
| **1** | Martinique | `/culture/martinique` | **200**, `.marketone-culture`, chapô, sections, CTA | ☑ | ☑ |
| **2** | La Réunion | `/culture/reunion` | **200**, même grammaire que Guadeloupe | ☑ | ☑ |
| **3** | Pilote v1 | `/culture/guadeloupe` | **200** — non-régression | ☑ | ☑ |
| **4** | CTA Martinique | Clic achetable | `/shop?marketone_mode=origin&marketone_origin=martinique` | ☑ | ☑ |
| **5** | CTA Réunion | Clic achetable | `…&marketone_origin=reunion` | ☑ | ☑ |
| **6** | Slug inconnu | `/culture/territoire-inconnu` | **404** | ☑ | ☑ |
| **7** | Bandeau facetté | `/shop?marketone_mode=origin&marketone_origin=martinique` | Lien Découvrir → Culture | ☑ | ☑ |
| **8** | Pas de hub | `/culture` | **404** | ☑ | ☑ |
| **9** | Pas de liens croisés | Page Martinique | **Pas** de lien vers `/culture/reunion` | ☑ | ☑ |
| **10** | Non-régression Boutique | Featured, Origines, panier, checkout | Inchangé | ☑ | ☑ |
| — | Mobile 375 px | Pages Culture v2 | Pas de débordement horizontal | ☑ | — |

---

## Tests automatisés

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_culture_v2 \
  --http-port=8071
```

| Périmètre | Résultat |
|-----------|----------|
| Tag `dorevia_marketone_culture_v2` | **6** post-tests, **0** failed |
| Suite Lots 1–6.2 + Culture v1/v2 | **91** post-tests, **0** failed |

---

## Critère GO Culture v2 légère

Les pages `/culture/martinique` et `/culture/reunion` prouvent la **réplicabilité** de la grammaire v1, avec CTA et liens Boutique fonctionnels, **sans** régression du pilote `guadeloupe` ni du socle Boutique.

**Décision MOA** : **GO Culture v2 légère** — 2026-05-18.
