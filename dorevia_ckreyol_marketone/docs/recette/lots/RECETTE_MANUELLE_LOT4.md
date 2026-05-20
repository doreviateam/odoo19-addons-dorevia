# Recette manuelle — Lot 4 (fiche produit)

| Champ | Valeur |
|-------|--------|
| **Lot** | 4 — Fiche produit retail |
| **Module** | `dorevia_ckreyol_marketone` **`19.0.4.0.0`** |
| **Base** | `ckr-marketone-01` — http://localhost:18079 |
| **Durée indicative** | 20–30 min |
| **Plan complet** | [`RECETTE_MANUELLE.md`](./RECETTE_MANUELLE.md) (home, shop, enveloppe) |
| **Ticket** | [`TICKET_MARKETONE_LOT4_PRODUCT.md`](../../tickets/lots/TICKET_MARKETONE_LOT4_PRODUCT.md) |

---

## Avant de commencer (2 min)

- [ ] Base **`ckr-marketone-01`**, module à jour
- [ ] Site en **français**, prix en **€**
- [ ] Au moins **2 produits** publiés avec image (idéalement les 3 ci-dessous)
- [ ] Navigateur : **desktop** puis **mobile ~375 px** (ou outils dev)

### URLs de recette

| Produit | URL |
|---------|-----|
| Crackers manioc Sainte-Anne *(référence)* | http://localhost:18079/shop/crackers-manioc-sainte-anne-8 |
| Maniocookies salés La Platine | http://localhost:18079/shop/maniocookies-sales-la-platine-7 |
| Pâtes de manioc Mayotte | http://localhost:18079/shop/pates-de-manioc-mayotte-9 |

**Parcours type** : `/shop` → clic carte → fiche → ajout panier → retour `/shop` et `/`.

---

## 1. Scope technique (fiche uniquement)

| # | Test | Attendu | OK | KO |
|---|------|---------|----|----|
| L4-01 | Page charge | HTTP 200, pas d’erreur visible | ☐ | ☐ |
| L4-02 | Classe scope | `marketone-product` sur `#wrap` **uniquement** sur la fiche | ☐ | ☐ |
| L4-03 | Pas de scope shop | Pas de `marketone-shop` sur la fiche | ☐ | ☐ |

*Vérification rapide : clic droit → inspecter `#wrap` ou « Afficher le code source ».*

---

## 2. Rendu desktop (≥ 1280 px)

**Produit** : Crackers manioc Sainte-Anne

| # | Test | Attendu | OK | KO |
|---|------|---------|----|----|
| L4-04 | Fil d’Ariane | Retour vers la boutique lisible | ☐ | ☐ |
| L4-05 | Titre H1 | Nom produit lisible (EB Garamond, hiérarchie claire) | ☐ | ☐ |
| L4-06 | Prix | Visible, contraste OK, format **€** (`5,50 €`) | ☐ | ☐ |
| L4-07 | Galerie | Image(s) avec radius / marge, non écrasée(s) | ☐ | ☐ |
| L4-08 | CTA achat | **Ajouter au panier** visible, bouton terracotta (charte 2.1) | ☐ | ☐ |
| L4-09 | Description | Texte court lisible — **pas** de mur de texte | ☐ | ☐ |
| L4-10 | Niveau visuel | Au moins au niveau home + `/shop` (Artisanal Terroir) | ☐ | ☐ |
| L4-11 | Variantes | Si présentes en BO : sélecteurs utilisables | ☐ | ☐ | N/A |

---

## 3. Rendu mobile (~375 px)

**Produit** : 2ᵉ produit (ex. Maniocookies La Platine)

| # | Test | Attendu | OK | KO |
|---|------|---------|----|----|
| L4-12 | Layout | Image + infos empilées, pas de scroll horizontal | ☐ | ☐ |
| L4-13 | Titre + prix | Lisibles, pas de chevauchement | ☐ | ☐ |
| L4-14 | CTA | Ajouter au panier accessible sans zoom | ☐ | ☐ |

---

## 4. Panier (fonctionnel minimal)

| # | Test | Attendu | OK | KO |
|---|------|---------|----|----|
| L4-15 | Ajout | Clic CTA → produit dans le panier (icône header ou `/shop/cart`) | ☐ | ☐ |
| L4-16 | Quantité | Modification quantité possible (Odoo standard) | ☐ | ☐ |
| L4-17 | Navigation | Retour `/shop` puis `/` sans erreur | ☐ | ☐ |

*Pas de test paiement / checkout au Lot 4.*

---

## 5. Doctrine produit (ADR-018)

| # | Test | Attendu | OK | KO |
|---|------|---------|----|----|
| L4-18 | Retail first | Produit, prix et CTA dominent la page | ☐ | ☐ |
| L4-19 | Pas encyclopédie | Pas d’onglets savoir, recettes longues, densité type 750g | ☐ | ☐ |
| L4-20 | Pas marketplace | Pas de portes pays / diaspora / logique catalogue custom | ☐ | ☐ |

---

## 6. Non-régression (obligatoire Lot 4)

| # | Test | Attendu | OK | KO |
|---|------|---------|----|----|
| L4-21 | Header / footer | Identiques sur fiche, `/shop`, `/` | ☐ | ☐ |
| L4-22 | Home `/` | `marketone-root` intact, pas de régression visuelle | ☐ | ☐ |
| L4-23 | Shop `/shop` | `marketone-shop` intact, grille 3 produits OK | ☐ | ☐ |

---

## 7. Tests auto (équipe / avant commit)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_smoke,dorevia_marketone_lot2,dorevia_marketone_lot2_1,dorevia_marketone_lot3,dorevia_marketone_lot4 \
  --http-port=8071
```

**Attendu** : `0 failed, 0 error(s)`.

---

## 8. Verdict MOA — Lot 4

> Une fiche peut être consultée, comprise et ajoutée au panier sans friction, avec un rendu au moins au niveau Artisanal Terroir (Lot 2.1).

| Décision | ☐ |
|----------|---|
| **GO** | |
| **GO avec réserves** | ☑ |
| **NO GO** | |

**Date** : 2026-05-18 · **Validé par** : MOA

**Réserves** (si GO avec réserves) :

```text
Compteur panier à 2 sur certaines captures : CTA cliqué deux fois pendant la recette — pas une anomalie fonctionnelle.
```

**Motifs NO GO** :

```text

```

### Rappel post-verdict

| Verdict | Action |
|---------|--------|
| GO / GO avec réserves | Commit + push Lot 4 ; MAJ ticket et ROADMAP |
| NO GO | Retour dev avec numéros **L4-xx** en échec ; pas de commit Lot 4 |

---

## Hors périmètre (ne pas bloquer le Lot 4)

- Liste `/shop` (Lot 3 — déjà livré, seulement non-régression)
- Checkout / paiement (Lot 5)
- Page Contact `/contactus` (ticket futur)
- Logo image, contact footer « à compléter » (réserves Lot 2.1)
