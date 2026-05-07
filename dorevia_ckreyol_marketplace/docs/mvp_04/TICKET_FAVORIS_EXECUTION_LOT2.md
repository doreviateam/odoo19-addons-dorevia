# TICKET — Exécution Lot 2 Favoris (MVP 04)

**ID** : `FAVORIS-EXEC-LOT2`  
**Statut** : **GO incrément minimal Lot 2 Favoris (charte `/shop/wishlist` + tests) — périmètre étendu Lot 2 hors sprint**  
**Type** : Exécution cadrée — **1 héritage QWeb** `product_wishlist` + **SCSS** dédié ; pas de logique wishlist custom  
**Module** : `dorevia_ckreyol_marketplace` (+ **`website_sale_wishlist`** / `website_sale` — dépendance explicite depuis 19.0.1.10.141)

---

## Phase 2 — Charte CK page `/shop/wishlist` (implémenté, **19.0.1.10.141**)

**Objectif** : la liste Favoris hérite du **standard** `website_sale_wishlist.product_wishlist` ; le `#wrap` Odoo n’avait pas les classes CK (`ckr-shop` étant réservé à `/shop`). **Décision** : ajouter **`ckr-root`**, **`ckr-page`**, **`ckr-shop-wishlist`** sur `#wrap` (sans **`ckr-shop`** pour éviter la cascade grille boutique).

| Livrable | Détail |
| --- | --- |
| QWeb | `views/pages/ckr_shop_wishlist.xml` — héritage `website_sale_wishlist.product_wishlist` |
| SCSS | `static/src/scss/layout/_shop_wishlist.scss` — fond, titre, état vide, grille, cartes `article.o_wishlist_item`, bouton **`o_wish_rm`** (cible tactile + `:focus-visible`) |
| Dépendance module | **`website_sale_wishlist`** ajoutée dans `__manifest__.py` |
| Test HTTP | Tag **`dorevia_ckr_shop_wishlist`** — `GET /shop/wishlist` → 200 + présence `ckr-shop-wishlist`, coquille liste vide |

**Recette instance à rejouer** : après `-u` / rebuild assets : état vide lisible, ajout depuis `/shop` → ligne visible, retrait OK, mobile — conformément checklist MOA Phase 2.

---

## Gate technique Favoris `/shop` — **GO** (recette `tenant_o7`, 2026-05)

**Décision** : le **standard `website_sale_wishlist`** est **exploitable** sur la boutique ; le **blocage observé sur les tuiles `/shop`** (cœur visible mais clic sans effet / absorbé) est **levé** après correctif d’intégration **CSS** dans `static/src/scss/layout/_shop.scss` (`pointer-events` sur `.o_add_wishlist`, `z-index` du coin média `.ckr-product-card__media-corner`).

**Limite de ce GO** : il **ne vaut pas** le lancement automatique de **tout** le Lot 2 Favoris (home, header, portail, périmètre complet). Il valide le **prérequis technique** : **tuile `/shop`** + **fiche produit** + **liste `/shop/wishlist`** + **retrait** + absence d’erreurs bloquantes.

### Recette exécutée (résumé)

| Contrôle | Résultat |
| --- | --- |
| Update module | OK |
| `grep` update (alertes) | Vide |
| Cœur tuile `/shop` cliquable | OK |
| Requête wishlist (Network), `POST /shop/wishlist/add` | OK |
| Produit visible `/shop/wishlist` | OK |
| Retrait depuis `/shop/wishlist`, liste vide après | OK |
| Ajout depuis fiche produit (`o_add_wishlist_dyn`) | OK |
| Console JS | OK |
| Logs runtime (`ERROR`, `CRITICAL`, `Traceback`, `QWeb`, `XPath`, `500`) | Vide |

### Opérationnel Docker (précision recette)

Sur l’instance concernée, **`docker compose up -d`** n’avait **pas** suffi à recharger le serveur Odoo persistant ; après **`docker compose restart odoo`**, les **assets** ont été pris en compte et le clic cœur `/shop` est devenu fonctionnel. À prévoir pour les prochains déploiements : **redémarrage explicite** du service Odoo si les seuls `up -d` ne rechargent pas le worker.

### Suite (inchangée par rapport au cadrage dossier)

Le **GO / NO GO implémentation Lot 2** (charge, planning, périmètre sprint) reste **à acter explicitement** — voir [§ Décision attendue avant exécution](#décision-attendue-avant-exécution).

---

## Contexte et décision actuelle

Le **parcours Favoris** est **cadré produit / UX** dans [`2_FAVORIS_PARCOURS.md`](2_FAVORIS_PARCOURS.md). La doctrine dossier est inchangée :

**Lot 2 Favoris : cadré, exécution différée, non bloquant pour le GO technique minimal pré-ouverture.**

Ce fichier **formalise les arbitrages à trancher** avant tout développement. Il **ne déclenche pas** de code, de branche ni de sprint : il sert de **matrice de décision** pour une future phase d’implémentation, une fois le Lot 1 panier / checkout et les jalons pré-ouverture jugés suffisants.

**Références** : [README MVP 04](README.md), [doctrine Panier ≠ Favoris](README.md#doctrine), [hors périmètre implicite](README.md#hors-périmètre-implicite).

**Note technique (pré-arbitrage)** : [`NOTE_ARBITRAGE_TECHNIQUE_FAVORIS_LOT2.md`](NOTE_ARBITRAGE_TECHNIQUE_FAVORIS_LOT2.md) — recommandations, risques et périmètre MVP **proposés** pour l’atelier de décision ; ne remplace pas une **décision écrite** dans la section *Décision attendue avant exécution*.

---

## Orientation technique validée (note faisabilité — documentaire)

La note [`NOTE_ARBITRAGE_TECHNIQUE_FAVORIS_LOT2.md`](NOTE_ARBITRAGE_TECHNIQUE_FAVORIS_LOT2.md) est **validée** sur les points ci-dessous. Elles **orientent** le futur chantier mais **ne constituent pas un GO implémentation** : aucun code, aucune branche Favoris tant que le **GO / NO GO** explicite n’est pas donné (voir fin de ticket).

### Doctrine Lot 2

**Favoris Lot 2 = s’appuyer sur Odoo standard, corriger / habiller / tester — ne pas créer un système CK parallèle.**

- Éviter tout **stockage custom** sauf **contrainte forte documentée** (exception rare).
- Pas d’**emailing**, pas de **partage**, pas de **marketing lourd**, pas de **compte forcé** ([README — Hors périmètre](README.md#hors-périmètre-implicite)).

### 1. Stack technique recommandée

| Élément | Retenu |
| --- | --- |
| **Module** | **`website_sale_wishlist`** (standard Odoo 19, dépend de `website_sale`). |
| **Modèle de données** | **`product.wishlist`** (`product_id`, `partner_id`, `website_id`, …). |
| **URL page liste** | **`/shop/wishlist`** (route standard). |
| **Stockage invité** | **Session** + lignes wishlist **sans `partner_id`**, conformément au **comportement standard** Odoo. |
| **Stockage connecté** | Rattachement au **`partner_id`** du visiteur connecté (standard). |
| **Fusion invité → connecté** | **Comportement standard Odoo** (ex. rattachement session → partner, gestion des doublons) ; **pas de promesse avancée** au-delà du standard. |

### 2. Périmètre MVP Lot 2 recommandé (premier incrément)

À réaliser **uniquement après GO implémentation** :

- **Listing `/shop`** (carte produit + wishlist) ;
- **Fiche produit** ;
- **Page liste Favoris** (`/shop/wishlist`) ;
- **Retrait favori** ;
- **Lien vers fiche produit** depuis la liste ;
- **Recette F1–F6** (section [§6](#6-recette-minimale-reprise-f1f6) ci-dessous ; [`2_FAVORIS_PARCOURS.md`](2_FAVORIS_PARCOURS.md) §9).

### 3. Hors premier incrément (report ou incrément suivant)

- **Home** (cartes produit hors `/shop`) ;
- **Compteur** favoris dans le **header** ;
- **Portail** `/my` ou équivalent étendu ;
- **Marketing**, **partage**, **emailing** (hors périmètre MVP04 — [README](README.md#hors-périmètre-implicite)).

### 4. Décision à venir

| Décision | Statut |
| --- | --- |
| **Gate technique Favoris `/shop`** (wishlist standard exploitable, tuiles OK) | **GO** — recette `tenant_o7` (voir section Gate en tête de document). |
| **GO / NO GO implémentation Lot 2** (sprint complet : home, header, etc.) | **À acter explicitement** après Lot 1 / pré-ouverture et arbitrage restant (charge, planning). |
| **Branche / code Favoris** (chantier Lot 2 élargi) | **Interdit** tant que le **GO implémentation Lot 2** n’est pas donné ; le gate `/shop` **ne déclenche pas** ce sprint. |

Les sections **§1 à §6** ci-dessous conservent la **matrice détaillée** ; les tableaux **§1 à §3** peuvent être lus au travers de l’orientation **wishlist standard** ci-dessus (les lignes « à arbitrer » historiques sont **levées** sur le choix de base ; restent les finitions et le **GO sprint** global).

---

## Objectif du ticket

Transformer le **cadrage** existant en **périmètre d’exécution arbitré** : pour chaque point ci-dessous, la colonne *Statut cible* indique si le point est **indispensable**, **optionnel**, **à arbitrer**, ou **hors MVP04** au sens du dossier — à **valider explicitement** avant développement.

**Légende**

| Libellé | Signification |
| --- | --- |
| **Indispensable** | Doit être livré dans le premier incrément Lot 2 si le Lot 2 est lancé. |
| **Optionnel** | Peut être reporté ou simplifié sans rompre le cadrage produit de base. |
| **À arbitrer** | Choix technique ou produit encore ouvert ; décision requise. |
| **Hors MVP04** | Exclu du périmètre MVP 04 (cf. README hors périmètre / doctrine). |

---

## 1. Stockage invité

*Orientation validée* : **`website_sale_wishlist`** — session + enregistrements **`product.wishlist`** sans `partner_id` ; pas de stockage CK parallèle.

| Option / question | Notes | Statut cible |
| --- | --- | --- |
| **Session** + lignes standard `product.wishlist` | Comportement Odoo documenté ; IDs en session (`wishlist_ids`). | **Retenu** (orientation) |
| **localStorage / cookie** seuls (sans standard) | Alternative non souhaitée si wishlist standard disponible. | Hors orientation |
| **Mécanisme wishlist standard Odoo** | Module **`website_sale_wishlist`**. | **Retenu** (orientation) |
| **Autre** (hybride, service dédié) | Uniquement si contrainte forte documentée. | Hors MVP sauf exception |
| **Persistance invité** | Limites standard (session, éventuel nettoyage automatique) — cf. note faisabilité. | À communiquer en recette |

**Indispensable** : confirmer sur chaque instance que **`website_sale_wishlist`** est **installé** avant développement.

---

## 2. Stockage connecté

*Orientation validée* : lignes **`product.wishlist`** avec **`partner_id`** = partenaire du visiteur connecté ; **website** courant.

| Option / question | Notes | Statut cible |
| --- | --- | --- |
| **Rattachement compte** / **`res.partner`** | Via modèle standard `product.wishlist`. | **Retenu** (orientation) |
| **Usage wishlist standard Odoo** | **`website_sale_wishlist`**. | **Retenu** (orientation) |
| **Comportement portail** (liste `/my`, menu, etc.) | Hors premier incrément — cf. *Orientation technique validée*, §3 *Hors premier incrément*. | Optionnel / report |

**Indispensable** : respecter les **règles d’accès** du module standard (tests ACL après habillage CK).

---

## 3. Fusion invité → connecté

*Orientation validée* : **comportement standard Odoo** (ex. rattachement des entrées session au partner à la connexion, traitement des doublons) ; **pas de promesse produit** au-delà du standard.

| Option | Notes | Statut cible |
| --- | --- | --- |
| **Fusion standard Odoo** | Méthodes du module wishlist (ex. `_check_wishlist_from_session`). | **Retenu** (orientation) |
| **Remplacement / séparation custom** | Non souhaité sauf contrainte documentée. | Hors orientation |
| **Pas de promesse MVP** sur une fusion élaborée | Aligné cadrage [`2_FAVORIS_PARCOURS.md`](2_FAVORIS_PARCOURS.md) §4. | Indispensable (rappel) |

---

## 4. Points d’entrée

**Cœur minimal Lot 2** (hors arbitrage accessoire) : **listing `/shop`** + **fiche produit** + **liste Favoris** (page dédiée). Tout le reste ci-dessous est **complémentaire** ou **à trancher**.

| Point d’entrée | Notes | Statut cible |
| --- | --- | --- |
| **Listing `/shop`** | Carte produit sur la boutique — base du parcours. | Indispensable |
| **Fiche produit** | Alignée au cadrage §3. | Indispensable |
| **Carte produit — homepage** (blocs sélection / explorer, etc.) | Enrichissement ; **pas** le périmètre minimal. | Optionnel / à arbitrer |
| **Accès header** (lien « Favoris » / icône cohérente header V1) | Navigation vers la liste ; arbitrage sous **Décision attendue avant exécution**. | À arbitrer |
| **Compteur** favoris dans le header | Lisibilité vs charge ; pas imposé par le cadrage minimal. | Optionnel |

---

## 5. Liste Favoris

| Élément | Notes | Statut cible |
| --- | --- | --- |
| **Page dédiée** **`/shop/wishlist`** | Vue liste scannable (cadrage §5 *Liste des favoris*) ; URL standard Odoo. | Indispensable |
| **Retrait favori** depuis la liste | Cadrage §3 / §5. | Indispensable |
| **Lien vers fiche produit** | Cadrage §5. | Indispensable |
| **Ajout au panier depuis la liste favoris** | Cadrage : **pas d’obligation** ; chemin panier **distinct**. Inclure un CTA panier = **optionnel**. | Optionnel |
| **Hors scope** : promesse marketing, partage, email | [README — Hors périmètre](README.md#hors-périmètre-implicite) | Hors MVP04 |

---

## 6. Recette minimale (reprise F1–F6)

Reprise des scénarios [§9 — `2_FAVORIS_PARCOURS.md`](2_FAVORIS_PARCOURS.md#9-scénarios-de-recette-minimaux).

| ID | Scénario | Contenu rappel | Statut cible |
| --- | --- | --- | --- |
| **F1** | Ajout **carte produit** (listing) | Clic cœur depuis listing ; état visuel immédiat. | Indispensable |
| **F2** | Ajout **fiche produit** | Même logique que la carte. | Indispensable |
| **F3** | **Retrait** | Suppression depuis la liste favoris ; disparition confirmée. | Indispensable |
| **F4** | **Persistance non connecté** | Conforme à l’**arbitrage** retenu pour l’invité (§1). | Indispensable *après* arbitrage §1 |
| **F5** | **Persistance connecté** | Conforme à l’**arbitrage** retenu pour le compte (§2). | Indispensable *si* persistance connectée retenue |
| **F6** | **Mobile** | Actions cœur + liste sans régression tactile. | Indispensable |

---

## Garde-fous (non négociables MVP04)

- Ne pas **confondre** favoris et panier ([doctrine](README.md#doctrine)).
- Pas d’**emailing automatique**, pas de **partage de liste**, pas de **marketing lourd** ([hors périmètre](README.md#hors-périmètre-implicite)).
- Pas de **compte forcé** sans décision d’arbitrage explicite ([cadrage §2](2_FAVORIS_PARCOURS.md#2-principes-directeurs)).
- Ne pas **retarder** une exécution Lot 1 / pré-ouverture en lançant du développement Favoris **sans** **GO implémentation Lot 2** explicite sur ce ticket (le **gate `/shop`** documenté **ne suffit pas** à ouvrir tout le sprint).

---

## Prochaines étapes (hors scope immédiat)

1. **Gate technique `/shop`** : **GO** (recette documentée en tête de document).
2. Atelier **arbitrage** : trancher les points listés en **Décision attendue avant exécution** (ci-dessous).
3. **GO / NO GO** lancement **implémentation Lot 2** complète (après Lot 1 et jalons pré-ouverture).
4. Découpage technique (routes, modèles, tests) — **après** décision écrite de sprint.

---

## Décision attendue avant exécution

Le **gate technique `/shop`** est **acté** (voir ci-dessous). Sans **GO / NO GO explicite** sur l’**implémentation Lot 2** au sens **sprint complet**, le ticket reste **préparatoire** pour ce périmètre élargi : **aucune branche / sprint Lot 2 complet** tant que la ligne correspondante n’est pas actée (des correctifs d’intégration déjà mergés ne constituent pas ce GO global).

### GO / NO GO implémentation Lot 2

| Décision | Statut |
| --- | --- |
| **Gate technique `/shop` + wishlist standard** (`tenant_o7`, recette 2026-05) | **GO** — voir la section *Gate technique Favoris `/shop`* en tête de document. |
| **GO** ou **NO GO** *lancement développement / sprint Lot 2 complet* (charge, planning, disponibilité après Lot 1 / pré-ouverture) | **À trancher** — seule décision bloquante pour **ouvrir** le développement Lot 2 au sens sprint. |

### Arbitrages déjà orientés (consignés plus haut)

Les points suivants sont **réglés par orientation technique validée** (wishlist standard — section *Orientation technique validée*) :

1. ~~Stockage invité~~ → **standard session + `product.wishlist`**.
2. ~~Stockage connecté~~ → **`partner_id` sur `product.wishlist`**.
3. ~~Fusion invité → connecté~~ → **standard Odoo**, sans promesse avancée.
4. ~~URL liste~~ → **`/shop/wishlist`**.
5. ~~Dépendance wishlist Odoo~~ → **`website_sale_wishlist`** **retenu**.

Restent à trancher **au moment du GO** (ou dans le périmètre du sprint) pour le **premier incrément** :

- **Home** : incluse ou non (par défaut **hors** premier incrément — § Orientation §3).
- **Header** (lien Favoris / comportement) : périmètre du MVP ou report.
- **Compteur** header : inclus ou report.
- **Portail** : hors premier incrément sauf décision contraire.
- **Scénarios F1–F6** : confirmation que **tous** sont dans le même incrément ou découpe documentée.

---

*Gate technique `/shop` documenté ci-dessus. Le **GO implémentation Lot 2** (sprint) reste à acter ; aucune ouverture automatique de chantier Lot 2 complète sans cette décision.*
