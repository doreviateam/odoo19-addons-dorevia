# Note MOA — Livraison CK-HOME-POLISH-001 — Corrections UX Home avant ouverture

| Champ | Valeur |
| --- | --- |
| Date | 2 juillet 2026 |
| Projet | C-Kréyòl Marketone — home |
| Ticket | **CK-HOME-POLISH-001** — Corrections UX ciblées Home avant ouverture |
| Destinataires | MOA, Produit, QA, Dev |
| Statut | **Clôturé GO exploitation démo** |
| Module contenu | `dorevia_ck_marketone_content` **19.0.1.80.0** |
| Module thème | `dorevia_ck_theme` **19.0.1.116.0** |
| Base recette | `dorevia_ck_marketone_01` |
| URL locale | http://localhost:18079 |
| URL démo publique | https://assure-violation-markets-factors.trycloudflare.com |

---

## Synthèse exécutive

Micro-lot de **polish UX ciblé** sur la Home CK, sans remise en cause de la structure validée (hero, vedettes, univers, coffrets, bloc pro, footer).

**Verdict global : GO** après recette desktop 1280 px, mobile 390 px, parcours fonctionnels et tunnel public.

Quatre irritants majeurs levés avant ouverture publique élargie :

1. **Newsletter non fonctionnelle** — bloc retiré de la Home (message « Merci pour votre inscription ! » visible au chargement).
2. **Header desktop** — favoris et panier immédiatement distinguables (cœur / panier, badges zéro masqués).
3. **Impact hero et prix** — lisibilité renforcée sans changement de wording MOA.
4. **Trust-bar et bloc Pro** — lecture et promesse B2B clarifiées, sans chiffre inventé.

Le tunnel achat reste intact : **Home → Shop → fiche → panier → checkout**.

---

## 1. Ce que voit le visiteur — par priorité

### P0 — Newsletter neutralisée (Home uniquement)

| Avant | Après |
| --- | --- |
| Bloc dual Pro + newsletter avec message de succès visible sans inscription | **Bloc Pro seul**, centré, sans formulaire |
| « Merci pour votre inscription ! » au chargement | **Absent** de la Home |

**Décision MOA respectée** : pas d’activation Email Marketing pour masquer le symptôme. La newsletter reste sur `/contactus` et `/professionnels` (hors périmètre Home).

**Reporté** : stratégie newsletter (liste, consentement, RGPD, SMTP) → lot dédié futur.

### P0 — Header wishlist / panier (desktop)

| Élément | Comportement |
| --- | --- |
| Favoris | Icône **cœur** visible · lien `/shop/wishlist` · libellé AT « Mes favoris » |
| Panier | Icône **panier** visible · lien `/shop/cart` |
| Badges compteur | **Masqués à zéro** (session fraîche : pas de double `0` ambigu) |
| Mobile 390 px | Entrée **« Mes favoris »** conservée dans le drawer · favoris masqué en barre haute (inchangé) |

### P1 — Hero (contenu inchangé, impact visuel renforcé)

- Panneau texte légèrement structuré (fond semi-opaque desktop) pour la lisibilité.
- CTA principal **« Découvrir la boutique »** plus visible (ombre, padding).
- CTA secondaire **« Voir les producteurs »** plus discret (texte atténué).
- Wording hero **non modifié** (kicker, H1, libellés CTA MOA 001A).

### P1 — Prix cards vedettes

- Prix TTC : **15 px / graisse 700** sur les cards « Nos coups de cœur ».
- Métadonnées (origine, producteur, format), badges et CTA **conservés**.

### P2 — Trust-bar

- 4 promesses toujours visibles (livraison, paiement, producteurs, service client).
- Icônes légèrement agrandies (44 px), fond discret, espacement et hiérarchie titre / micro-texte améliorés.

### P2 — Bloc Professionnels

| Élément | Valeur |
| --- | --- |
| Titre | `Vous êtes professionnel ?` |
| Texte | *Vous êtes épicerie, restaurateur ou distributeur ? C-Kréyòl vous accompagne dans la sélection et l'approvisionnement de produits créoles pour votre activité.* |
| CTA | `Demander un accès professionnel` → `/professionnels` |

Aucun chiffre B2B non vérifié ajouté.

### P3 — Alt images

Non traité (audit SEO/accessibilité séparé), conformément à la note de cadrage.

---

## 2. Recette validée

### Desktop 1280 px

| Contrôle | Résultat |
| --- | --- |
| Absence newsletter / message succès | OK |
| Header cœur + panier distincts | OK |
| Hero lisible, CTA principal visible | OK |
| Prix vedettes 15px/700 | OK |
| Trust-bar 4 items | OK |
| Bloc Pro seul | OK |
| CTA Coffrets « Découvrir » → `/kits` | OK → redirection `/shop?marketone_mode=pack` |

### Mobile 390 px

| Contrôle | Résultat |
| --- | --- |
| Pas d'overflow horizontal | OK |
| CTA hero empilés | OK |
| Drawer « Mes favoris » | OK |
| Cards et prix lisibles | OK |

### Parcours fonctionnels

| Route | Résultat |
| --- | --- |
| `/` | 200 |
| `/shop` | 200 |
| `/shop/wishlist` | 200 |
| `/shop/cart` | 200 |
| `/professionnels` | 200 |
| `/kits` | OK (redirection pack) |
| Tunnel public Cloudflare | OK (home polish + parcours coffrets) |

### Hotfix upgrade (thème)

Un premier `-u dorevia_ck_theme` a échoué : XPath panier ciblait `@class` au lieu de `@t-attf-class` sur le template natif Odoo 19 (`website_sale.header_cart_link`).

**Correctif appliqué** : `website_header_v22.xml` ligne 50 — `contains(@t-attf-class, 'my_cart_quantity')`.

Relance upgrade → **OK** · migration `19.0.1.80.0` exécutée · restart sandbox → **OK**.

### Tests automatisés

| Tag | Statut |
| --- | --- |
| `dorevia_ck_home_polish_001` | Ajouté (hooks + compose) |
| `dorevia_ck_marketone_home_lot4` | Mis à jour (Pro seul, sans newsletter home) |
| `dorevia_ck_wishlist_u1` | Mis à jour (badge zéro masqué) |
| Lots home 1 / 5 / trust-bar | Mis à jour (`ck-dual-engage--pro-only`) |

Recette MOA principale : **upgrade Odoo + navigateur + curl** (non re-exécution complète de la suite CI sur cette session).

---

## 3. Périmètre technique livré

### Contenu (`dorevia_ck_marketone_content`)

| Fichier | Modification |
| --- | --- |
| `home_dual_engage.py` | Bloc **Pro seul** home (`ck-dual-engage--pro-only`) · validation sans newsletter |
| `hooks.py` | Wording bloc Pro + CTA « Demander un accès professionnel » |
| `home_polish.py` | Replay inchangé (réinjecte le nouveau dual home) |
| `migrations/19.0.1.80.0/post-migrate.py` | Bootstrap dual home + polish visuel |
| `tests/test_ck_home_polish_001.py` | Recette lot polish |
| Tests lot 1/4/5, 001c, trust-bar | Alignés sur Pro seul |

### Thème (`dorevia_ck_theme`)

| Fichier | Modification |
| --- | --- |
| `views/website_header_wishlist.xml` | Badge favoris si count > 0 · icône cœur explicite |
| `views/website_header_v22.xml` | Badge panier si count > 0 · hotfix `@t-attf-class` |
| `static/src/scss/website.scss` | Hero, trust-bar, prix home, bloc Pro seul |
| `static/src/scss/website_header.scss` | Différenciation visuelle cœur / panier |

### Hors périmètre (inchangé)

- Structure des sections Home validées.
- Activation Email Marketing / SMTP / mailing list.
- Refonte header global hors wishlist/panier.
- Images produits, fiches produit, navigation catalogue.
- Audit alt images (P3 reporté).

---

## 4. Contrôles rapides MOA (3 minutes)

Sur `localhost:18079` ou tunnel démo :

1. **Home** : pas de « Merci pour votre inscription » · pas de formulaire newsletter.
2. **Header desktop** : cœur puis panier · pas de badge `0` en session fraîche.
3. **Hero** : textes 001A inchangés · CTA principal qui ressort.
4. **Vedettes** : prix immédiatement repérables.
5. **Trust-bar** : 4 items lisibles en un coup d'œil.
6. **Bloc Pro** : nouveau texte + CTA « Demander un accès professionnel ».
7. **Mobile 390 px** : drawer « Mes favoris » · pas d'overflow.
8. **Coffrets** : clic « Découvrir » → `/kits` ou équivalent pack.

Commande upgrade si besoin de rejouer :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 \
  -u dorevia_ck_marketone_content,dorevia_ck_theme --stop-after-init
docker restart sandbox-odoo19-odoo-1
```

---

## 5. Suite backlog

| Sujet | Statut |
| --- | --- |
| **CK-HOME-POLISH-001** | **Clôturé GO exploitation démo** — [`NOTE_MOA_CLOTURE_CK_HOME_POLISH_001_20260702.md`](NOTE_MOA_CLOTURE_CK_HOME_POLISH_001_20260702.md) |
| Newsletter CK (Email Marketing, RGPD, délivrabilité) | Lot futur dédié |
| Alt images SEO/accessibilité | Audit séparé (P3) |
| CK-HOME-001B vedettes / coffret | En cours / backlog visuel |
| D4 réseau header (`/shop/wishlist?count=1`) | Backlog technique inchangé |
| Vigilance post-GO (cf. § 6–7) | **Exécutée** — réserves non bloquantes reportées SEO / technique |

---

## 6. Addendum QA — Points de vigilance post-GO

Le lot **CK-HOME-POLISH-001** est confirmé en **GO exploitation démo**.

Les points suivants **ne bloquent pas** la clôture du ticket, mais restent en vigilance QA / backlog :

| # | Point de vigilance | Action attendue |
| --- | --- | --- |
| 1 | **Cycle badge favoris** | Vérifier le cycle complet : ajout produit en wishlist → apparition du compteur → retrait du produit → disparition du badge **sans** affichage résiduel `0`. |
| 2 | **Viewport 375 px** | Compléter la recette responsive (type iPhone SE) : confirmer que le prix renforcé **15 px / graisse 700** ne crée pas de rupture visuelle sur les cards vedettes. |
| 3 | **Firefox desktop** | Passage rapide sous moteur **Gecko** : absence d'effet de bord SCSS sur header / trust-bar. |
| 4 | **Route `/kits`** | Confirmer la doctrine de la route et sa redirection vers `/shop?marketone_mode=pack` — stabilité fonctionnelle et implications SEO. |

Ces contrôles sont des **sécurisations post-GO** et ne remettent pas en cause la livraison CK-HOME-POLISH-001.

---

## 7. Résultats recette addendum (exécutés le 2 juillet 2026)

Recette lancée sur `localhost:18079` · base `dorevia_ck_marketone_01` · script [`ck_home_polish_postgo_qa.mjs`](../design/maquette_01.2/scripts/ck_home_polish_postgo_qa.mjs).

| # | Contrôle | Méthode | Résultat | Détail |
| --- | --- | --- | --- | --- |
| 1 | **Cycle badge favoris** | Tests Odoo `dorevia_ck_wishlist_u1` (HttpCase) | **OK** | 3 tests · 0 échec — ajout → badge `1` au reload → retrait → badge masqué (pas de `0` résiduel) |
| 1b | Cycle badge (navigateur externe Playwright) | Session navigateur hors HttpCase | **Réserve** | Pas de cookie `session_id` sur requêtes externes sandbox → badge non observable en recette Playwright brute ; **non bloquant** — couvert par les tests Odoo ci-dessus |
| 2 | **Viewport 375 px** (iPhone SE) | Playwright Chromium 375×667 | **OK** | Pas d'overflow horizontal (`375/375`) · prix **15px / 700** sur 4 cards · pas de clip prix · capture `home_mobile_375_featured.png` |
| 3 | **Firefox desktop** | Playwright Firefox 1280×900 | **OK** | Pas d'overflow · cœur + panier visibles · trust-bar 4 items · pas de newsletter · bloc `pro-only` présent |
| 4 | **`/kits` → pack** | curl + code | **OK fonctionnel** | `301` → `/shop?marketone_mode=pack` · destination `200` · `/kits` **absent** du `sitemap.xml` (`sitemap=False`) · lien CTA coffret home → `/kits` |
| 4b | SEO canonical pack | curl HTML shop pack | **Réserve** | `canonical` pointe vers `/shop` (générique), pas la query `marketone_mode=pack` — comportement sandbox / démo, à traiter au lot SEO prod |

### Verdict addendum

```text
4/4 axes couverts — GO vigilance
→ Cycle wishlist : validé par tests Odoo (référence)
→ 375 px + Firefox + /kits : OK
→ Réserves mineures : session externe sandbox (wishlist manuel) · canonical pack (SEO)
→ Aucune régression bloquante CK-HOME-POLISH-001
```

---

## Verdict MOA — clôture

```text
CK-HOME-POLISH-001 — CLÔTURÉ GO EXPLOITATION DÉMO

La Home CK est validée après correction des irritants P0/P1/P2 :
newsletter retirée, header wishlist/panier clarifié, hero, prix,
trust-bar et bloc Professionnels renforcés.

L'addendum QA post-GO confirme les contrôles 375 px, Firefox desktop,
cycle wishlist et route /kits.

Aucune réserve bloquante. Canonical pack et wishlist hors session Odoo
→ vigilance technique / SEO future.
```

> Clôture formelle : [`NOTE_MOA_CLOTURE_CK_HOME_POLISH_001_20260702.md`](NOTE_MOA_CLOTURE_CK_HOME_POLISH_001_20260702.md)

---

*Note MOA — C-Kréyòl Marketone · Livraison CK-HOME-POLISH-001 — 2 juillet 2026*
