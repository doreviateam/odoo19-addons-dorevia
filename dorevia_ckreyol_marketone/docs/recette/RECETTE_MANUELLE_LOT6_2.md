# Recette manuelle — Lot 6.2 (porte Origines)

| Champ | Valeur |
|-------|--------|
| **Lot** | 6.2 — Porte Origines |
| **Module** | `19.0.7.0.0` (post-exécution) |
| **Base** | `ckr-marketone-01` — http://localhost:18079 |
| **Ticket exécution** | [`TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md`](../tickets/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES_EXEC.md) |

---

## Prérequis BO

- [ ] Attribut catalogue **Origine** (multi-valeurs, sans variante)
- [ ] 2–3 **valeurs** d’origine (ex. Guadeloupe, Martinique) + produits rattachés
- [ ] 2 profils **`marketone.shop.origin`** : slug, nom visiteur, phrase, **publiés**, `website_id` = **My Website**
- [ ] Vérifier qu’une origine **non publiée** ou slug invalide déclenche le repli documenté

---

## Parcours MOA

| # | Test | Attendu | OK | KO |
|---|------|---------|----|----|
| L62-01 | `/origines` | 301 → `/shop?marketone_mode=origin` | ☐ | ☐ |
| L62-02 | Mode seul | Catalogue **complet** + bandeau **Origines** | ☐ | ☐ |
| L62-03 | Facette une origine | Grille filtrée ; titre peut nommer l’origine | ☐ | ☐ |
| L62-04 | Facette invalide | Redirection `/shop` nu (pas 500) | ☐ | ☐ |
| L62-05 | Filtres Odoo | Sidebar / tri toujours utilisables | ☐ | ☐ |
| L62-06 | Fiche produit | Origine légère ; lien vers porte si prévu | ☐ | ☐ |
| L62-07 | Incontournables | `/shop?marketone_mode=featured` inchangé | ☐ | ☐ |
| L62-08 | Tunnel | Panier + checkout OK | ☐ | ☐ |
| L62-09 | Culture | **Pas** de page territoire longue sur `/shop` | ☐ | ☐ |

---

## Tests auto

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_smoke,dorevia_marketone_lot2,dorevia_marketone_lot2_1,dorevia_marketone_lot3,dorevia_marketone_lot4,dorevia_marketone_lot5,dorevia_marketone_lot6_1_featured,dorevia_marketone_lot6_2_origin \
  --http-port=8071
```

---

## Verdict MOA

| Décision | ☐ |
|----------|---|
| **GO** | |
| **GO avec réserves** | |
| **NO GO** | |

**Date** : _______________ · **Validé par** : _______________
