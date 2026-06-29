# Note MOA — Livraison Sprint Producteurs CK V1

| Champ | Valeur |
| --- | --- |
| Date | 30 juin 2026 |
| Projet | C-Kréyòl Marketone — annuaire et fiches producteurs |
| Base recette | `dorevia_ck_marketone_01` — http://localhost:18079 |
| Destinataires | MOA, Produit, QA |
| Statut | **✅ GO QA / MOA — clôturé 30 juin 2026** |
| Verdict QA | **GO fonctionnel** — [`RECETTE_QA_PRODUCTEURS_V1_VERDICT_20260630.md`](RECETTE_QA_PRODUCTEURS_V1_VERDICT_20260630.md) |
| Contexte | Post-gel boutique `v1.0.0-boutique` — lot **Éditorial** (cf. [clôture V1](NOTE_MOA_CLOTURE_V1_BOUTIQUE_20260629.md)) |
| Modules | `dorevia_ck_marketone_content` **19.0.1.65.0** · `dorevia_ck_theme` **19.0.1.104.0** |

---

## Synthèse exécutive

Le sprint **Producteurs CK V1** met en ligne l'annuaire public des partenaires et leurs fiches dédiées, avec lien depuis les chips producteur des fiches produit. Le tunnel achat gelé V1 n'est **pas modifié**.

| URL | Rôle |
| --- | --- |
| `/producteurs` | Liste des partenaires `ck_is_producer = True` |
| `/producteur/<slug>-<id>` | Fiche producteur + grille produits publiés |

Comportements SEO : slug canonique Odoo (`ir.http._slug`), redirection **301** si slug obsolète (même ID), **404** si ID invalide ou partenaire non producteur.

---

## Ce qui a été livré côté Dev

### 1. Routes et contrôleur

**Fichier** : `dorevia_ck_marketone_content/controllers/producers.py`

- `GET /producteurs` — liste triée par nom, compteur produits publiés/vendables par producteur.
- `GET /producteur/<slug>` — fiche avec accroche, histoire HTML, site web, produits associés.
- Sitemap : liste incluse (`sitemap=True`), fiches exclues (`sitemap=False`).

### 2. Templates QWeb

| Template | Fichier |
| --- | --- |
| `ck_producers_list_page` | `views/website_producers_list.xml` |
| `ck_producer_detail_page` | `views/website_producer_detail.xml` |

Contenu éditorial affiché depuis les champs BO existants (Note 08) :

| Champ `res.partner` | Affichage |
| --- | --- |
| `name` | Titre fiche / card |
| `image_1920` | Photo ou placeholder feuille |
| `ck_producer_location_label` | Origine (ex. Sainte-Anne, Guadeloupe) |
| `ck_producer_short_description` | Accroche courte |
| `ck_producer_story_html` | Bloc éditorial long (HTML) |
| `website` | Lien externe si renseigné |

### 3. Modèle et chips fiche produit

**Fichier** : `models/res_partner.py`

- `get_ck_producer_url()` — URL canonique `/producteur/{slug}-{id}`.
- `get_ck_producer_products()` — produits `is_published` + `sale_ok` liés via `ck_producer_id`.

**Fichier** : `models/product_template.py` — `get_ck_product_page_chips()` expose `producer_url`.

**Fichier** : `views/website_sale_product_page.xml` — chip producteur → lien `<a class="ck-chip ck-chip--producer">` si URL disponible.

### 4. Styles

**Fichier** : `dorevia_ck_theme/static/src/scss/producer_page.scss` — tokens CK (cards liste, fiche, chip cliquable).

### 5. Correctifs inclus

| Correctif | Détail |
| --- | --- |
| Guillemets typographiques | Champs `string=` / `help=` dans `res_partner.py` — délimiteurs Python invalides (U+2019) |
| Import slug Odoo 19 | `get_ck_producer_url()` utilise `env['ir.http']._slug()` (convention projet) |

---

## Tests automatisés

**Tag** : `dorevia_ck_producers_v1` · **23 tests** (8 modèle + 15 HTTP)

| Scénario | Couverture |
| --- | --- |
| **A** | Liste `/producteurs` — 200, nom, localisation |
| **B** | Fiche — 200, nom, localisation, accroche, produit, lien retour |
| **D** | 301 slug incorrect · 404 ID inexistant / non entier / non producteur |
| **F** | Chip fiche produit — lien vers fiche producteur · absence de lien sans producteur |

**Commande recette** :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --http-port=8079 \
  -u dorevia_ck_marketone_content,dorevia_ck_theme \
  --test-tags=dorevia_ck_producers_v1 --test-enable --stop-after-init
```

> Utiliser `--http-port=8079` si le worker Odoo tourne déjà sur 8069.

**Résultat sandbox 30/06/2026** : **23/23 verts** — `0 failed, 0 error(s)`.

---

## Mise à jour instance (équipe technique)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --http-port=8079 \
  -u dorevia_ck_marketone_content,dorevia_ck_theme \
  --stop-after-init

docker restart sandbox-odoo19-odoo-1
```

Hard refresh navigateur (`Cmd+Shift+R`) pour valider les assets SCSS.

---

## Recette MOA / QA — checklist manuelle

> **Verdict 30/06** : GO fonctionnel — détail dans [`RECETTE_QA_PRODUCTEURS_V1_VERDICT_20260630.md`](RECETTE_QA_PRODUCTEURS_V1_VERDICT_20260630.md).

### Pages producteurs

- [x] `/producteurs` — grille cards, compteur produits, CTA « Découvrir le producteur ».
- [x] Fiche **SARL La Platine** — accroche, localisation, contenu long, produits Manio visibles. *(Réserve : placeholder image, pas de `image_1920`.)*
- [x] Lien retour « Tous nos producteurs » → `/producteurs`.
- [x] Slug obsolète avec bon ID → redirection 301 vers URL canonique.
- [x] URL invalide → page 404 Odoo.

### Depuis fiche produit

- [x] Chip **SARL La Platine** sur Manio Crackers → lien cliquable vers `/producteur/sarl-la-platine-1405`.
- [x] Produit sans `ck_producer_id` (`Galettes de manioc`) → pas de lien `/producteur/`.

### Non-régression boutique gelée V1

- [x] Parcours Home → Shop → fiche → panier → checkout → confirmation (FR) — commande témoin **S00103**.
- [x] Tunnel EN `/en/shop/...` navigable jusqu'au checkout.
- [x] Mobile 390 px — liste et fiche sans overflow horizontal.

### Contenu MOA (back-office)

Actions sur les partenaires producteurs (`Contacts` > onglet **Producteur CK**) :

| Action | Priorité |
| --- | --- |
| Vérifier / compléter `ck_producer_short_description` et `ck_producer_story_html` | Haute |
| Ajouter `image_1920` (logo ou photo) si disponible | Moyenne |
| Lier les produits via `ck_producer_id` sur chaque fiche produit | Haute |
| Ajouter lien menu header ou footer vers `/producteurs` (CMS / navigation) | MOA |

Référence seed : [`TICKET_CONTENU_SEED_MANIO_PLATINE_NOTE08_R3.md`](TICKET_CONTENU_SEED_MANIO_PLATINE_NOTE08_R3.md).

---

## Hors périmètre V1 (backlog)

- Traductions `en_GB` des pages producteurs.
- Filtres / recherche sur l'annuaire.
- Blocs éditoriaux avancés (critères sélection CK, focus produits emblématiques).
- Sitemap dynamique des fiches individuelles.

---

## Réserves non bloquantes (QA 30/06)

| Sujet | Responsable |
| --- | --- |
| Photo producteur La Platine (`image_1920`) | MOA |
| Lien menu / footer vers `/producteurs` | MOA |
| Accès instance : sélectionner la base `dorevia_ck_marketone_01` avant recette | Tech / QA |
| Erreurs cron base `glc-audit-paliers-0-3` (hors périmètre) | Tech — backlog séparé |

---

## Prochaines étapes suggérées

| Priorité | Sujet | Responsable |
| --- | --- | --- |
| 1 | Enrichissement contenu producteurs + entrée navigation | MOA |
| 2 | Traduction EN pages producteurs (si ouverture sprint i18n) | Produit |
| 3 | Déploiement prod (post-validation MOA) | Tech |

---

*Note de communication MOA — Sprint Producteurs CK V1 — 30 juin 2026 · recette QA clôturée*
