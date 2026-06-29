# Note MOA — Clôture V1 boutique C-Kréyòl + gel release `v1.0.0-boutique`

| Champ | Valeur |
| --- | --- |
| Date | 29 juin 2026 |
| Projet | C-Kréyòl Marketone — boutique en ligne |
| Destinataires | MOA, Produit, QA |
| Statut | **Clôturé sans réserve** — recette live FR + EN validée MOA |
| **Tag release** | **`v1.0.0-boutique`** sur commit `d2682ca4` |
| Version thème | `dorevia_ck_theme` **19.0.1.103.1** |
| Version content | `dorevia_ck_marketone_content` **19.0.1.63.0** |
| Base recette | `dorevia_ck_marketone_01` — http://localhost:18079 |
| Document gel | [`RELEASE_V1_BOUTIQUE.md`](../../../RELEASE_V1_BOUTIQUE.md) (racine repo) |

---

## Synthèse exécutive

La **V1 boutique est gelée** (tag `v1.0.0-boutique`). Le parcours acheteur complet est validé en français et en anglais :

> **Home → Shop → fiche produit → panier → checkout → confirmation**

La partie achat est **cohérente et exploitable** : CGV checkout actives, email de confirmation SMTP (Mailpit en recette), polish visuel et éditorial terminé (U1–U4b).

**Règle d'exploitation** : ne pas modifier le périmètre V1 sans ouverture explicite d'un sprint V1.1 ou correction d'un bug critique.

---

## Validation live MOA

| Étape | Preuve |
| --- | --- |
| Parcours FR | Commandes **S00098**, **S00099**, **S00102**, **S00103** |
| Parcours EN | `/en/shop/cart`, `/en/shop/manio-crackers-4`, `/en/shop/confirmation` |
| CGV | Case checkout + lien `/terms` |
| Email confirmation | Capture Mailpit (SMTP local, template `sale_confirmation`) |
| Mobile 390px | Tunnel complet sans blocage |
| Polish U4b i18n | Panier vide et confirmation sans fuite FR/EN |

**Couverture automatisée** : 38 tests verts (tags recette U1–U6, Polish, i18n).

---

## Sprint Polish — livrables (inclus dans le tag)

| Lot | Objectif | Verdict |
| --- | --- | --- |
| **U1** | Cohérence visuelle images cards Home ↔ Shop (ratio 1:1, cover) | Vert |
| **U2** | Badges / rubans grille Shop alignés sur la Home | Vert |
| **U3** | CTA panier Home mobile (44 px, pleine largeur ≤ 575 px) | Vert |
| **U4** | Wording réassurance fiche produit (compact, « CGV ») | Vert |
| **U4** | Panier vide éditorialisé + CTA « Découvrir la sélection » | Vert |
| **U4** | Confirmation commande (message + réassurance) | Vert |
| **U4b** | Traductions `en_GB` panier vide et confirmation (`/en`) | Vert |

---

## Périmètre V1 boutique — rappel

Sprints antérieurs inclus dans le gel :

- Navigation header V2.2, mega-menu rayons, toolbar Shop (drawer filtres, note 07).
- Cards produit canon Home / Shop, favoris, breadcrumb, rating, chips producteur.
- Fiche produit CK (layout, galerie, onglets, réassurance).
- CGV : vue `accept_terms_and_conditions` activée + bootstrap XML.
- Parcours panier → adresse → livraison → paiement → confirmation.

---

## Dettes non bloquantes (V1.1 / backlog)

| ID | Description | Priorité |
| --- | --- | --- |
| **D1** | Titre Manio : 2 cards variantes Home vs 1 template Shop (curation produit) | V1.1 |
| **D2** | Inline ruban Home fallback (ex. Savon vétiver) | V1.1 |
| **D3** | Breakpoint grille Home 480–575px (2 col vs 1 col Shop) | V1.1 |
| **D4** | `#top_menu` — inefficacité réseau (appel `/shop/wishlist?count=1`) | Backlog |

Ces points n'empêchent pas l'exploitation commerciale de la boutique.

---

## Hors V1 (non engagé)

Blog, communauté, forum, espace pro · filtres avancés / recherche full-text · stock dynamique · avis clients · upgrade Odoo · perfection esthétique globale.

---

## Actions MOA / exploitation

### Déploiement (équipe technique)

Récupérer le tag :

```bash
git fetch origin tag v1.0.0-boutique
git checkout v1.0.0-boutique   # ou merge sur branche déploiement
```

Upgrade instance :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 \
  -u dorevia_ck_theme,dorevia_ck_marketone_content \
  --i18n-overwrite --load-language=en_GB --stop-after-init
docker restart sandbox-odoo19-odoo-1
```

> `--i18n-overwrite` : **une fois** après passage en `19.0.1.103.1` pour les traductions panier / confirmation.

### Contrôles rapides post-upgrade

1. Parcours commande test FR + EN (cf. commandes témoin ci-dessus).
2. Panier vide FR et EN.
3. Email confirmation visible dans Mailpit.

### Contenu catalogue (toujours MOA)

Actions Axe C back-office — voir [`NOTE_MOA_LIVRAISON_20260626.md`](NOTE_MOA_LIVRAISON_20260626.md).

---

## Prochain sprint

| Option | Description |
| --- | --- |
| **Éditorial** | Contenu Home, rayons, fiches, producteurs, SEO, traductions |
| **V1.1 technique** | Dettes D1–D3 si visibles en prod |
| **Backlog** | D4 réseau header |

---

*Document MOA — C-Kréyòl Marketone · Version 1.1 (gel release) — 29 juin 2026*
