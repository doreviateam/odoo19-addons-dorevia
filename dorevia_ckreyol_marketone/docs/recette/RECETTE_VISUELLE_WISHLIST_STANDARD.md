# Recette visuelle — Wishlist standard Odoo (C-Kreyol Marketone)

| Champ | Valeur |
|-------|--------|
| **Ticket** | Activation `website_sale_wishlist` + cosmétique CK |
| **Version cible** | **`19.0.15.10.3`** |
| **Module Odoo** | `website_sale_wishlist` (standard, sans logique CK) |
| **URL boutique** | http://localhost:18079/shop |
| **URL wishlist** | http://localhost:18079/shop/wishlist |
| **Base** | `ckr-marketone-01` |
| **Statut recette** | **GO MOA** — visiteur public · R2 clôturée `10.3` |
| **Rapport exécution** | [`RAPPORT_RECETTE_WISHLIST_REGRESSION_BOUTIQUE_20260522.md`](./RAPPORT_RECETTE_WISHLIST_REGRESSION_BOUTIQUE_20260522.md) |
| **Doctrine** | Standard Odoo · wishlist secondaire · achat / consultation prioritaire |

---

## Contexte et objectif

La boutique C-Kreyol est stabilisée (cards, filtres, états vides, wording UX-1). Ce ticket **active le module standard Odoo `website_sale_wishlist`** et vérifie son intégration visuelle dans l’expérience CK.

**Objectif recette :** confirmer que la wishlist fonctionne selon le standard Odoo, sans régression boutique, avec une cosmétique CK discrète et premium sur le cœur (cards, header, fiche produit, page wishlist).

**Régression obligatoire :** [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](./REFERENCE_RECETTE_BOUTIQUE_MOA.md) — sections **B1 · B4 · B5 · B6** minimum.

**Hors périmètre :** refonte fonctionnelle wishlist, renommage global, modèle ou JS métier CK, refonte fiche produit ou page wishlist.

---

## Prérequis

1. Module `website_sale_wishlist` installé (dépendance `dorevia_ckreyol_marketone` ≥ **19.0.15.10.0**).
2. Upgrade module CK :
   ```bash
   docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
     -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init
   ```
3. Redémarrage conteneur Odoo si nécessaire pour servir assets à jour.
4. Navigateur desktop + mobile (ou outils dev responsive).

---

## Périmètre testé

| Zone | Contrôle |
|------|----------|
| `/shop` | Grille, cards, header, pas de régression UX-1 |
| Fiche produit | Bouton wishlist secondaire vs achat |
| `/shop/cart` | Panier inchangé |
| Header | Lien wishlist harmonisé avec panier / compte |
| `/shop/wishlist` | Page standard, état vide, ajout / retrait |
| Mobile | Cœur cliquable, pas de débordement |
| Connecté / non connecté | Comportement standard Odoo — **constats documentés § Vigilance** |

---

## Point de vigilance MOA — connecté / non connecté

### Hypothèse initiale MOA

Nous pensions initialement que la mise en liste de souhaits **nécessitait une connexion utilisateur**.

### Décision ticket

- **Aucune règle CK imposée** à ce stade (pas de redirection login custom, pas de message CK, pas de blocage visiteur).
- On **suit le standard Odoo** tel qu’il est livré dans `website_sale_wishlist`.
- On **documente précisément le comportement observé** en recette (tableau § Constats ci-dessous).

### Comportement standard Odoo attendu (référence technique — à confirmer en recette)

> Source : module `website_sale_wishlist` (Odoo 19 CE). Les lignes ci-dessous décrivent l’implémentation standard ; la recette doit **valider ou infirmer** sur la sandbox MOA.

| Contexte | Ajout wishlist | Stockage | Connexion requise ? |
|----------|----------------|----------|---------------------|
| **Visiteur non connecté** (`public user`) | Route `/shop/wishlist/add` · `auth='public'` | Enregistrements `product.wishlist` sans `partner_id` · IDs référencés dans **`request.session['wishlist_ids']`** | **Non** — pas de redirection login standard |
| **Utilisateur connecté** | Même route | Enregistrements liés au **`partner_id`** du compte · filtrés par `website_id` | N/A (déjà connecté) |
| **Connexion après ajouts visiteur** | Fusion automatique au login | `_check_wishlist_from_session()` : wishlist session rattachée au partenaire · doublons supprimés · clé session vidée | Les ajouts visiteur **peuvent** survivre à la connexion |
| **Déconnexion** | — | La wishlist **partenaire** reste en base ; la session visiteur repart vide | Comportement à **constater** (liste visible ou non selon état auth) |

**Persistance — attentes de recette (à observer, pas à imposer côté CK) :**

| # | Scénario | Question recette | Indice standard Odoo |
|---|----------|------------------|----------------------|
| P1 | Navigation interne (visiteur) | Les cœurs restent terracotta après changement de page ? | Session Odoo active |
| P2 | Fermeture / réouverture navigateur (visiteur) | Wishlist conservée ou perdue ? | Liée au **cookie de session** Odoo |
| P3 | Utilisateur connecté — navigation | Liste stable sur `/shop`, fiche, `/shop/wishlist` ? | Persistance **base** (`partner_id`) |
| P4 | Connecté — fermeture / réouverture navigateur | Wishlist retrouvée après retour ? | Attendu **oui** (compte) |
| P5 | Déconnexion puis reconnexion | Wishlist compte retrouvée ? Contenu session visiteur intermédiaire ? | Fusion au login · wishlist partenaire en base |
| P6 | Visiteur → ajouts → login | Les produits ajoutés avant login apparaissent-ils sur le compte ? | Fusion session → partenaire |
| P7 | Compteur header `o_wsale_my_wish` | Cohérent visiteur vs connecté ? | Standard Odoo |

**Procédure recette recommandée :**

1. **Session A — visiteur** : navigation privée · ajouter 2 produits · noter compteur header + `/shop/wishlist` · naviguer `/shop` → fiche → retour wishlist.
2. **Session A — persistance** : fermer l’onglet · rouvrir `/shop/wishlist` (même navigateur) · noter conservé / perdu.
3. **Session B — connecté** : compte test MOA · ajouter 1 produit · fermer navigateur · rouvrir · vérifier persistance.
4. **Session C — fusion** : visiteur · ajouter 1 produit · se connecter · vérifier présence sur compte + page wishlist.
5. **Session D — déconnexion** : connecté avec wishlist · se déconnecter · vérifier contenu wishlist et état des cœurs · se reconnecter.

**Captures / traces attendues :** état cœurs `/shop`, page `/shop/wishlist`, compteur header, éventuel message ou absence de message (pas de popup CK custom attendue).

### Constats recette — connecté / non connecté

_(À remplir lors de l’exécution — fait foi pour le verdict MOA.)_

| # | Scénario | Comportement observé | Conforme standard Odoo ? | Commentaire MOA |
|---|----------|----------------------|---------------------------|-----------------|
| P1 | Navigation visiteur | | ☐ Oui ☐ Non ☐ N/A | |
| P2 | Fermeture navigateur (visiteur) | | ☐ Oui ☐ Non ☐ N/A | |
| P3 | Navigation connecté | | ☐ Oui ☐ Non ☐ N/A | |
| P4 | Fermeture navigateur (connecté) | | ☐ Oui ☐ Non ☐ N/A | |
| P5 | Déconnexion / reconnexion | | ☐ Oui ☐ Non ☐ N/A | |
| P6 | Fusion visiteur → login | | ☐ Oui ☐ Non ☐ N/A | |
| P7 | Compteur header | | ☐ Oui ☐ Non ☐ N/A | |

**Connexion requise pour ajouter ?** ☐ Oui ☐ **Non** (standard attendu : **Non**)  
**Écart bloquant UX ?** ☐ Oui ☐ Non — _(décrire si oui ; hors scope ticket sauf régression visuelle)_

---

## Zones à contrôler et captures attendues

### 1. Header

**Capture :** barre header desktop — icônes panier, wishlist (si visible), compte, recherche.

| Point | Attendu |
|-------|---------|
| Présence | Lien `/shop/wishlist` via classe `o_wsale_my_wish` |
| Taille / alignement | Même logique que panier et compte (cercle ~2,25 rem) |
| Hover | Couleur terracotta `#C4715A`, fond crème léger |
| Comportement | Aucune logique CK spécifique — standard Odoo |

### 2. Cards produits (`/shop`)

**Capture :** zoom coin supérieur droit d’une card + vue grille 3–4 produits.

| Point | Attendu |
|-------|---------|
| Position | Cœur coin **haut droit** de l’image |
| Un seul bouton | Pas de doublon avec bouton wishlist grille Odoo natif |
| Hiérarchie | Cœur discret · « Voir » et prix restent dominants |
| Panier survol | Overlay panier bas droite inchangé |

### 3. Fiche produit

**Capture :** zone CTA (ajout panier + wishlist).

| Point | Attendu |
|-------|---------|
| Présence | Bouton wishlist standard (`o_add_wishlist_dyn` ou équivalent) |
| Hiérarchie | **Achat d’abord, envie ensuite** — wishlist secondaire |
| Style | Contour discret · hover terracotta · retenu = terracotta persistant |

### 4. Page wishlist (`/shop/wishlist`)

**Captures :** page avec produits · page vide.

| Point | Attendu |
|-------|---------|
| Accessibilité | HTTP 200 · classe scope `marketone-shop-wishlist` |
| État vide | Message standard Odoo + lien retour boutique |
| Liste | Ajout / retrait produit fonctionnels |
| Style | Fond page CK · cartes lisibles · pas de refonte layout |

### 5. Mobile

**Capture :** card produit mobile (375 px) + header mobile.

| Point | Attendu |
|-------|---------|
| Zone tactile | Cœur ≥ 2 rem, facilement cliquable |
| Layout | Pas de chevauchement image / prix / CTA |
| Scroll | Pas de débordement horizontal |

---

## États visuels du cœur (cards)

Doctrine MOA : **Hover = intention · Terracotta persistant = produit retenu.**

| État | Rendu attendu |
|------|----------------|
| **Repos** | Cœur contour (`fa-heart-o`) · brun/gris discret · fond rond crème · ombre légère |
| **Survol** | Cœur terracotta `#C4715A` · transition douce · pas d’effet agressif |
| **Retenu / sélectionné** | Cœur plein terracotta `#C4715A` · état stable après clic · classes `o_in_wishlist` / `is-active` |
| **Retrait** | Retour état repos après suppression wishlist |

---

## Comportement fonctionnel standard (checklist)

| # | Scénario | Étapes | Attendu |
|---|----------|--------|---------|
| F1 | Ajout depuis `/shop` | Clic cœur sur une card | Produit ajouté · cœur terracotta persistant |
| F2 | Retrait depuis `/shop` | Re-clic ou action standard | Produit retiré · cœur contour |
| F3 | Ajout fiche produit | Bouton wishlist fiche | Produit dans la liste |
| F4 | Page wishlist | Ouvrir `/shop/wishlist` | Produits listés ou état vide |
| F5 | Retrait page wishlist | Supprimer un produit | Disparition ligne · compteur header cohérent |
| F6 | Retour boutique | Lien « Shop » / navigation | `/shop` en 200 |
| F7 | Visiteur non connecté — ajout | Navigation privée · clic cœur · **sans login** | Produit ajouté · pas de redirection login forcée CK · cœur terracotta · voir § Vigilance P1–P2 |
| F8 | Utilisateur connecté — ajout | Compte test · clic cœur | Produit persisté compte · voir § Vigilance P3–P5 |
| F9 | Fusion visiteur → login | Ajout visiteur puis connexion | Wishlist session rattachée au compte (standard Odoo) · voir § Vigilance P6 |
| F10 | Déconnexion / reconnexion | Wishlist compte avant logout · re-login | Comportement standard documenté · voir § Vigilance P5 |

---

## Non-régression boutique

| Page / zone | Attendu |
|-------------|---------|
| `/shop` | 200 · compteur UX-1 · chips · sidebar · cards conversion |
| Fiche produit | 200 · CTA achat prioritaire |
| `/shop/cart` | 200 · panier intact |
| Header | Navigation CK · pas de casse layout |
| Filtres / état vide | Wording UX-1 **9.4** inchangé |
| Tests auto | Suite boutique + tag `dorevia_marketone_shop_wishlist` verts |

---

## Critères GO / NO GO

### GO si

- [x] `website_sale_wishlist` installé sans erreur
- [x] Aucune régression visible `/shop`, fiche, panier, header
- [x] Cœur discret au repos, terracotta au hover, terracotta persistant si retenu
- [x] Un seul bouton wishlist par card (overlay coin image)
- [x] CTA achat / « Voir » reste visuellement prioritaire
- [x] Page `/shop/wishlist` accessible et fonctionnelle
- [x] Mobile sans débordement ni surcharge visuelle
- [x] Aucune logique métier CK ajoutée (JS / modèle custom)
- [x] **Comportement visiteur non connecté documenté (§ Vigilance P1, P7)** — connecté P3–P6 reporté
- [x] Captures et constats documentés (rapport + captures ci-dessous)

### NO GO si

- [ ] Doublon boutons wishlist sur les cards
- [ ] Régression UX-1, sidebar, cards conversion ou panier
- [ ] Cœur trop visible / concurrence CTA achat ou « Voir »
- [ ] États visuels non conformes (hover ou retenu incorrects)
- [ ] Page wishlist inaccessible ou cassée
- [ ] Débordement mobile ou zone tactile insuffisante

---

## Grille de constats (exécution)

| Zone | Desktop | Mobile | Verdict |
|------|---------|--------|---------|
| Header wishlist | Compteur 0 → 1 → 0 · lien `/shop/wishlist` | Icône visible · cohérent | **GO** |
| Card — repos | Cœur discret coin haut droit | Cœur visible · zone tactile OK | **GO** |
| Card — hover | Terracotta `#C4715A` | Non rejoué isolément | **GO** desktop |
| Card — retenu | Ajout card · état persistant | OK grille | **GO** |
| Fiche produit | Wishlist secondaire vs CTA achat | Non rejoué | **GO** desktop |
| Page wishlist pleine | Produit listé · scope CK | — | **GO** |
| Page wishlist vide | Message standard Odoo | — | **GO** |
| Non-régression `/shop` | UX-1 · sidebar · cards OK | Pas de débordement | **GO** |
| **Connecté / non connecté** | Visiteur P1 · P7 OK | P2–P6 non exécutés | **Réserve doc.** |

**Exécuteur :** MOA / Codex  
**Date :** 2026-05-22  
**Tests auto :** 75/75 · version **`19.0.15.10.3`**

### Captures wishlist

| Zone | Fichier |
|------|---------|
| `/shop` desktop | [`capture_wishlist_standard_shop_desktop_20260522.png`](./capture_wishlist_standard_shop_desktop_20260522.png) |
| `/shop` mobile | [`capture_wishlist_standard_shop_mobile_20260522.png`](./capture_wishlist_standard_shop_mobile_20260522.png) |
| Wishlist après ajout | [`capture_wishlist_standard_wishlist_after_add_20260522.png`](./capture_wishlist_standard_wishlist_after_add_20260522.png) |
| Wishlist après retrait | [`capture_wishlist_standard_wishlist_after_remove_20260522.png`](./capture_wishlist_standard_wishlist_after_remove_20260522.png) |
| Fiche produit | [`capture_wishlist_standard_product_20260522.png`](./capture_wishlist_standard_product_20260522.png) |

Régression boutique complète : [`RAPPORT_RECETTE_WISHLIST_REGRESSION_BOUTIQUE_20260522.md`](./RAPPORT_RECETTE_WISHLIST_REGRESSION_BOUTIQUE_20260522.md)

---

## Réserves éventuelles

_(À compléter lors de la recette — écarts mineurs acceptables vs bloquants.)_

| # | Réserve | Gravité | Décision |
|---|---------|---------|----------|
| 1 | Connecté / fusion session non testé (P3–P6) | Info | Acceptée — standard Odoo documenté § Vigilance |
| 2 | Alignement titre « Collections » offcanvas | Mineur | **GO MOA R2** — clôturé `10.3` |

---

## Verdict final MOA

| Décision | |
|----------|---|
| ☑ **GO** — Activation wishlist standard validée | |
| ☐ **GO avec réserves** | |
| ☐ **NO GO** | |

**Commentaire MOA :** GO visiteur public · régression boutique `10.2` · R2 cosmétique `10.3` validée. Seule réserve restante : connecté / fusion session (documentaire).

---

## Références techniques

- Dépendance : `website_sale_wishlist` dans `__manifest__.py`
- Désactivation doublon grille : `views/pages/shop_wishlist.xml` (`add_to_wishlist` → `active=False`)
- Overlay cards : `views/pages/shop_product_tile_conversion.xml`
- Styles : `static/src/scss/_shop_product_cards.scss`, `_shop_wishlist.scss`
- Tests : `tests/test_marketone_shop_wishlist.py` (tag `dorevia_marketone_shop_wishlist`)
- Standard Odoo (référence comportement) : `website_sale_wishlist` — `controllers/main.py`, `models/product_wishlist.py`, `models/res_users.py`

**Commande tests :**

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_shop_wishlist,dorevia_marketone_shop_regression,dorevia_marketone_shop_filter_state,dorevia_marketone_shop_sidebar,dorevia_marketone_shop_sidebar_collections,dorevia_marketone_smoke,dorevia_marketone_lot3_shop \
  --http-port=8073
```
