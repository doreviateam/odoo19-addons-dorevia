# Note — Faisabilité et arbitrage technique (Lot 2 Favoris)

**Statut** : note de préparation — **gate technique `/shop` documenté (GO)** ; implémentation Lot 2 sprint **non engagée** sans décision explicite  
**Références** : [`TICKET_FAVORIS_EXECUTION_LOT2.md`](TICKET_FAVORIS_EXECUTION_LOT2.md), [`2_FAVORIS_PARCOURS.md`](2_FAVORIS_PARCOURS.md), [README MVP 04](README.md)

**Contexte** : avant tout développement Lot 2, répondre aux décisions listées dans *Décision attendue avant exécution* du ticket. Ce document propose des **recommandations** et une **estimation de risques / complexité** pour faciliter l’atelier d’arbitrage.

---

## Synthèse exécutive

| Dimension | Recommandation |
| --- | --- |
| **Base technique** | **Conserver et s’appuyer sur le module standard Odoo `website_sale_wishlist`** (modèle `product.wishlist`, route `/shop/wishlist`, boutons `o_add_wishlist`). Le thème CK manipule déjà ces hooks — éviter un stockage parallèle « custom » sauf contrainte forte. |
| **Complexité globale estimée** | **Moyenne** si le périmètre reste « UX CK + cohérence header / homepage » sur la stack existante ; **élevée** si abandon du standard ou double source de vérité. |
| **Risque principal** | Dupliquer les favoris (session custom + wishlist Odoo) ou diverger du comportement fusion/login déjà porté par le standard. |

---

## 1. Base technique pour les Favoris

### Option A — **Standard Odoo `website_sale_wishlist`** (recommandé)

- **Présent** en Odoo 19 Community : addon **`website_sale_wishlist`**, souvent **`auto_install`** avec `website_sale`.
- **Modèle** : `product.wishlist` (`product_id`, `partner_id` optionnel, `website_id`, prix snapshot, etc.).
- **Front** : interactions déjà packagées (`data-action="o_wishlist"`, assets frontend).
- **Alignement CK** : le module CK positionne déjà la wishlist sur les tuiles (`ckr_shop_wishlist_on_product_media`, classes `o_add_wishlist`) — la « base » métier est donc **déjà là** ; Lot 2 peut se concentrer sur **complétude**, **tests** et **UX** plutôt que sur un nouveau datastore.

### Option B — Session / custom uniquement

- **Contre** : double vérité, perte de la fusion login standard, maintenance et recette plus lourdes.
- **À réserver** à une contrainte documentée (ex. refus d’installer `website_sale_wishlist` sur une instance — rare si e-commerce actif).

### Option C — Hybride

- **Risqué** ; à éviter sauf pont court entre ancien état et standard.

**Décision proposée** : **Option A** ; valider sur chaque environnement que **`website_sale_wishlist`** est bien **installé** et que les données `product.wishlist` sont utilisables (pas de module désinstallé sur une base minimaliste).

---

## 2. Stockage invité

### Stratégie réaliste (alignée standard Odoo)

- Les lignes invité sont des enregistrements **`product.wishlist`** avec **`partner_id` vide** ; les **`id`** sont stockés en **`session`** (`wishlist_ids`).
- **Persistance** : tant que la session navigateur / cookie Odoo vit, et que les lignes ne sont pas purgées.

### Limites à communiquer (produit / support)

- **Pas de synchronisation multi-appareils** pour l’invité sans compte (comportement attendu MVP04).
- **Nettoyage automatique** : le standard prévoit un **autovacuum** sur les wishlists invité **anciennes** (paramètre typique **semaines** — à vérifier sur la version déployée). À mentionner en FAQ interne : favoris invités **non garantis à vie**.
- **Changement de navigateur / cookie effacé** : perte possible.

**Décision proposée** : **ne pas réinventer** ; documenter ces limites dans la recette et, si besoin, dans une ligne d’aide côté liste.

---

## 3. Stockage connecté

### Rattachement

- **`res.partner`** du **`users`'s partner`** (`partner_id` sur `product.wishlist`), filtré par **`website_id`**.

### Portail

- Le standard expose la wishlist **website** (`/shop/wishlist`). Une vue **portail** `/my/...` dépend des extensions Odoo / configuration ; pour MVP04, **l’axe principal reste la boutique** — portail **optionnel** (cf. ticket : statut optionnel).

### Modèle

- **`product.wishlist`** (standard), pas de modèle CK obligatoire au premier incrément.

**Décision proposée** : **modèle standard + ACL existantes** ; étendre uniquement si besoin métier CK **léger** (champs calculés, filtres).

---

## 4. Fusion invité → connecté

### Comportement standard Odoo

- Méthode **`_check_wishlist_from_session`** : rattache les entrées session au **partner**, **supprime les doublons** produit entre session et compte.
- C’est une **fusion simple**, prévisible, déjà testée par l’éditeur.

### MVP04

- **Recommandation** : **adopter ce comportement** ; ne pas promettre une fusion « intelligente » au-delà (quantités, listes multiples, etc.).
- Si « pas de promesse » produit : wording du type *« À la connexion, vos favoris en cours sont associés à votre compte lorsque c’est possible »* — sans garantie multi-session invité.

**Décision proposée** : **fusion standard**, pas de développement alternatif sauf cas métier exceptionnel documenté.

---

## 5. Page liste Favoris

| Élément | Proposition |
| --- | --- |
| **URL** | **`/shop/wishlist`** (route standard Odoo 19 — déjà utilisée dans les gabarits CK pour détecter la page liste). |
| **Structure minimale** | Réutiliser le template standard comme socle ; ajuster **charte CK** (titres, grille, CTA) sans casser les boucles `products_in_wishlist` / lignes wishlist. |
| **Retrait** | Mécanisme standard (boutons / interactions packagées) ; à valider en recette après styling. |
| **Lien fiche produit** | Exigence cadrage — déjà couverte par les vues standard ou légers xpath CK. |

**Décision proposée** : **ne pas changer d’URL** sans motif majeur (SEO, liens déjà partagés).

---

## 6. Points d’entrée du premier incrément

Aligné au **cœur minimal** du ticket : **`/shop`** + **fiche produit** + **liste**.

| Point | Recommandation MVP incrément 1 |
| --- | --- |
| **`/shop`** | **In** — tuiles + bouton wishlist déjà branché thème CK. |
| **Fiche produit** | **In** — cohérence avec listing. |
| **Liste `/shop/wishlist`** | **In**. |
| **Home (cartes produit)** | **Optionnel** ou **incrément 2** : même hook wishlist si tuiles partagent le même partial ; effort surtout **QA** multi-contextes. |
| **Header (lien Favoris)** | **Optionnel mais peu coûteux** si limité à un **lien** vers `/shop/wishlist` (déjà présent en navigation CK — **brancher le bon href** et état actif). |
| **Compteur header** | **Optionnel** ; nécessite exposition du **nombre** de lignes wishlist (snippet/controller léger ou valeur déjà disponible dans le contexte — à vérifier au moment de l’implémentation). |

**Décision proposée** : **MVP livrable** = shop + fiche + page liste + **corrections de régression éventuelles** ; Home / compteur = **lot suivant** ou **stretch** selon capacité.

---

## 7. Tests et recette

### Automatisable (HttpCase / tags dédiés futurs)

- **`GET /shop`** → **200**, présence bouton wishlist sur tuile (structure DOM stable).
- **`GET /shop/wishlist`** → **200** (vide ou avec session de test).
- **`GET`** fiche produit → **200**, présence `o_add_wishlist` ou équivalent.
- **Non régression** : pas de **500** sur routes wishlist après mise à jour module.

### Plutôt recette manuelle ou semi-manuelle

- **F1–F3** : clic cœur, feedback visuel immédiat, retrait liste — dépend JS / interactions.
- **F4–F5** : persistance invité / connecté et **fusion au login** — scénarios multi-session.
- **F6** : tactile, responsive fin.

### Risques de maintenance

- **Fort** si surcouche CSS/JS dupliquant la logique wishlist.
- **Modéré** si **xpath + SCSS** sur templates standard et **peu** de JS custom.
- **Tests** : fragilité des sélecteurs DOM si Odoo renomme des classes ; préférer **tests HttpCase** sur routes + **smoke** plutôt que tours fragiles sur chaque patch mineur.

---

## Proposition de périmètre MVP Lot 2 (après GO arbitrage)

**In (minimal)**

1. Valider **`website_sale_wishlist`** installé et **cohérent** sur tous les environnements cibles.
2. **`/shop`** + **fiche produit** : états wishlist **cohérents** avec le cadrage (cœur + liste).
3. **Page `/shop/wishlist`** : lisible, charte CK, retrait + lien produit.
4. Recette **F1–F6** documentée ; au moins **jeu de tests HTTP** minimal + **recette manuelle** checklist.

**Stretch / incrément suivant**

- Home ; lien header « parfait » ; compteur ; polish portail.

**Hors scope** (inchangé README)

- Emailing, partage, marketing, compte forcé.

---

## Prochaine étape formelle

Consigner les **choix réels** (copie de cette note ou tableau signé) dans une **révision** de [`TICKET_FAVORIS_EXECUTION_LOT2.md`](TICKET_FAVORIS_EXECUTION_LOT2.md) ou procès-verbal d’atelier, puis **GO implémentation** explicite.

---

## Recette gate `/shop` (référence — `tenant_o7`, 2026-05)

Le **standard `website_sale_wishlist`** a été validé en recette : **tuile `/shop`** (cœur cliquable, `POST /shop/wishlist/add`), **fiche produit**, **liste `/shop/wishlist`**, **retrait**, console et logs propres. Le blocage **tuile `/shop`** identifié en préflight (clic absorbé / non cliquable) est **levé** (intégration CSS CK, pas de logique wishlist custom).

**Décision enregistrée** : **Gate Favoris `/shop` — GO** dans [`TICKET_FAVORIS_EXECUTION_LOT2.md`](TICKET_FAVORIS_EXECUTION_LOT2.md). Ce GO **ne remplace pas** le **GO implémentation Lot 2** (sprint complet).

**Exploitabilité instance** : après déploiement, si `docker compose up -d` ne recharge pas le worker Odoo, un **`docker compose restart odoo`** peut être nécessaire pour appliquer les assets.

---

*Document préparatoire — pas de livrable code.*
