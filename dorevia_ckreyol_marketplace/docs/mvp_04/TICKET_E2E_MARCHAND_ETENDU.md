# TICKET — E2E marchand élargi CK

**ID** : `E2E-MARCHAND-ETENDU`  
**Statut** : À lancer  
**Priorité** : P1 (pré-ouverture commerciale contrôlée)  
**Module** : `dorevia_ckreyol_marketplace` (+ dépendances `website_sale`, envoi mail selon configuration)  
**Type** : Extension de la preuve marchande (tests HttpCase / recette)

---

## Objectif

Passer du **scénario minimal** « un client peut acheter » ([`TICKET_CHECKOUT_E2E_PRE_OUVERTURE.md`](./TICKET_CHECKOUT_E2E_PRE_OUVERTURE.md), tests tag `dorevia_ckr_checkout_e2e`) à une **couverture plus réaliste** des principaux cas d’achat et de défaillance maîtrisée, pour sécuriser une **ouverture commerciale contrôlée**.

Ce ticket **cadre uniquement** : priorisation, prérequis, stratégie d’automatisation, critères GO/NO GO et découpage en lots. **Aucune implémentation de tests** n’est implicite tant que ce ticket n’est pas arbitré.

---

## Hors périmètre explicite (ne pas rouvrir)

- Design, charte, direction artistique.
- Pattern-blocs, design system, documentation snippets.
- Snippets Odoo déposables éditeur Website.
- Doctrine URL boutique / refonte `/shop` / pages éditoriales.
- Nouvelles fonctionnalités métier (hors données de test nécessaires aux scénarios).

Le chantier sert **uniquement** à **élargir la preuve marchande** (tests automatisés et/ou recettes manuelles documentées).

---

## Référence existante

| Élément | Référence |
| --- | --- |
| Ticket socle minimal | [`TICKET_CHECKOUT_E2E_PRE_OUVERTURE.md`](./TICKET_CHECKOUT_E2E_PRE_OUVERTURE.md) |
| Suite Python minimale | `tests/test_ckr_checkout_e2e_pre_opening.py` |
| Tag minimal conservé | `dorevia_ckr_checkout_e2e` |

---

## 1. Scénarios à cadrer

### 1.1 Achat nominal complet renforcé

| # | Scénario | Priorité suggestive |
| --- | --- | --- |
| N1 | Ajout panier depuis `/shop` (liste/grille) | **Indispensable** |
| N2 | Ajout panier depuis **fiche produit** | **Indispensable** |
| N3 | Panier avec **plusieurs quantités** (≥ 2 sur une ligne) | Haute |
| N4 | **Modification** de quantité sur une ligne existante | Haute |
| N5 | **Suppression** d’une ligne | Haute |
| N6 | Checkout **invité** | Déjà couvert partiellement au minimal — à **renforcer** (adresse complète, livraison, paiement) |
| N7 | Adresse **complète** (tous champs requis métier) | Haute |
| N8 | Choix **transporteur** (au moins un disponible) | Haute |
| N9 | **Paiement test** jusqu’à succès | Haute |
| N10 | Page **confirmation** commande (`/shop/confirmation` ou équivalent Odoo 19) | Haute |
| N11 | Vérification **commande créée** en base (`sale.order` attendu) — si faisable en HttpCase sans fragilité | Moyenne |
| N12 | **Email / notification** commande (queue mail, `mail.mail` ou stub selon politique tests) | Moyenne à faible (souvent **manuel** ou test isolé si pas de SMTP en CI) |

**Critère de complétude pour ce bloc** : le parcours reflète un achat « réel » (multi-sources panier, gestion lignes, tunnel complet jusqu’à confirmation).

---

### 1.2 Livraison / transporteur

| # | Scénario | Notes |
| --- | --- | --- |
| L1 | Au moins un transporteur **disponible** pour l’adresse test | Base |
| L2 | **Frais de livraison** visibles / cohérents avant paiement | Souvent extractible du HTML checkout |
| L3 | **Plusieurs transporteurs** : changement de choix, mise à jour montants | Automatisable si données BO préparent 2+ méthodes |
| L4 | Transporteur **indisponible** selon adresse (pays / code postal) si règles métier | Peut rester **manuel** ou test ciblé |
| L5 | **Aucun transporteur** disponible : message utilisateur clair, pas de 500 | Critique ouverture — au minimum **recette manuelle** |

---

### 1.3 Paiement

| # | Scénario | Notes |
| --- | --- | --- |
| P1 | Paiement **test nominal** (succès) | Extension du minimal |
| P2 | **Abandon** avant validation / retour panier ou shop | Souvent navigation HTTP ; peut être tag séparé |
| P3 | Paiement **refusé / annulé** si **simulable** avec le provider test | Dépend du connecteur ; sinon **manuel** |
| P4 | **Confirmation** commande uniquement après état paiement attendu (pas de faux positif) | Assertion sur URL + éventuellement état SO |

---

### 1.4 Produits / stock

| # | Scénario | Notes |
| --- | --- | --- |
| S1 | Produit **vendable en stock** | Déjà proche du minimal |
| S2 | Produit en **rupture** ou non achetable | Comportement liste/fiche/panier ; peut nécessiter jeu de données dédié |
| S3 | **Plusieurs lignes** panier (produits distincts) | Haute valeur |
| S4 | Produit **indisponible entre panier et checkout** (race / désactivation) | Difficile en CI ; souvent **manuel** ou test rare |

---

### 1.5 Client invité / connecté

| # | Scénario | Notes |
| --- | --- | --- |
| U1 | Checkout **invité** | Socle |
| U2 | Checkout **utilisateur portal** connecté | Création user + session ; tests plus lourds |
| U3 | **Réutilisation adresse** si compte avec adresses enregistrées | Optionnel / Lot 2 |
| U4 | Pas de blocage **compte** inexistant pour invité | Régression |

---

### 1.6 Erreurs maîtrisées

Les cas suivants doivent être **compris** et **traités sans 500 / traceback / QWeb** :

| Code | Cas |
| --- | --- |
| E1 | Panier vide → checkout |
| E2 | Adresse incomplète |
| E3 | Email invalide (formulaires où applicable) |
| E4 | Aucun transporteur applicable |
| E5 | Paiement non validé / interrompu |

Extension du minimal déjà partiellement couvert pour **E1 / E2** ; les autres à ajouter selon faisabilité.

**Barrière qualité** : aucune erreur utilisateur ne doit exposer traceback ou page blanche ; logs sans `ERROR`/`Traceback` bloquant sur ces chemins.

---

## 2. Stratégie d’automatisation progressive

### 2.1 Tags proposés

| Tag | Rôle |
| --- | --- |
| `dorevia_ckr_checkout_e2e` | **Conserver** — socle minimal existant ; ne pas casser la CI |
| `dorevia_ckr_checkout_e2e_extended` | **Créer si besoin** — nouveaux tests élargis (nom indicatif ; à figer dans `tests/__init__.py` et convention équipe) |

Alternative : sous-tags par thème (`…_shipping`, `…_payment`) si la durée d’exécution impose un découpage.

### 2.2 Principes

1. **Automatiser en priorité** les chemins **régressifs** et **répétitifs** : panier multi-lignes, qty, transporteur multiple, invité vs portal si ROI test/maintenance acceptable.
2. **Laisser en recette manuelle** documentée : emails réels, paiement refus simulateur limité, cas limites pays/postaux complexes.
3. **Distinguer clairement** dans les commits / README tests : *automatisé* vs *manuel requis avant GO ouverture*.
4. Réutiliser les helpers éprouvés (`POST /shop/cart/add` JSON-RPC, extraction CSRF, etc.) ; éviter la duplication fragile.

### 2.3 Ce qui restera probablement manuel (sans engagement définitif)

- Réception **email** SMTP réel en environnement sandbox.
- Certains cas **paiement refus** selon acquéreur test disponible.
- **Transporteur indisponible** selon zones géographiques fines sans jeu de données exhaustif en CI.

---

## 3. Prérequis data / configuration

À aligner sur l’environnement d’exécution (base dédiée recommandée) :

- Produits : au moins **deux** références vendables + jeu pour rupture si scénario S2.
- **Stock / routes** : cohérents avec `consu` / stock selon politique retenue.
- **Transporteurs** : un obligatoire ; deux ou plus pour L3 si test automatisé.
- **Paiement test** : provider sandbox configuré comme pour le minimal.
- **Taxes / fiscalité** : pays / TVA cohérents avec adresses de test.
- **Website CK** actif, **thème** compatible (`theme_classic_store`).
- Utilisateur **portal** dédié si scénarios U2 (mot de passe connu ou création en `setUpClass`).
- Politique **mail** : queue en test ou désactivation assertion mail si non fiable en CI.

---

## 4. Commandes d’exécution (référence)

À adapter (base, port, chemins config) :

```bash
# Socle minimal existant
odoo … -d <DB> --test-enable --stop-after-init \
  --test-tags=dorevia_ckr_checkout_e2e …

# Lot élargi (une fois implémenté)
odoo … -d <DB> --test-enable --stop-after-init \
  --test-tags=dorevia_ckr_checkout_e2e_extended …
```

Logs : `--log-level=test`, fichier log dédié pour analyse post-run.

---

## 5. Critères GO / NO GO (ticket de cadrage)

### GO — le ticket est « validé » comme livrable documentaire

On sait explicitement :

- quels scénarios sont **indispensables** avant ouverture publique ;
- lesquels peuvent rester **manuels** avec procédure écrite ;
- lesquels **doivent** être **automatisés** pour la définition de « done » technique ;
- quelles **données de test** et configuration sont nécessaires ;
- quels **écarts** (non couverts / trop coûteux en CI) **ne bloquent pas** une ouverture contrôlée si compensés par recette.

### NO GO — le cadrage est insuffisant

- Liste de scénarios **floue** ou tout-en « à faire » sans priorité.
- Confusion entre **preuve minimale** existante et **élargissement** (risque de tout automatiser sans ROI).
- Absence de **découpage en lots** alors que la charge est manifeste.

---

## 6. Limites connues

- Les tests HttpCase **ne remplacent pas** une recette humaine sur device réels et paiement réel contrôlé.
- **Emails** : fiabilité variable selon `mail.catchall`, cron, sandbox.
- **Concurrence** produits / stock : difficile à simuler de façon stable en CI.
- Durée CI : multiplication des scénarios peut imposer **tags séparés** ou exécution **nightly**.

---

## 7. Proposition de découpage en lots

| Lot | Contenu indicatif | Sortie |
| --- | --- | --- |
| **Lot A** | **Premier lot recommandé pour implémentation** — nominal renforcé (voir détail ci-dessous) | Tests + doc mise à jour |
| **Lot B** | Livraison : 2 transporteurs, frais visibles ; erreur sans transporteur | Mix auto / manuel |
| **Lot C** | Paiement : abandon navigation ; refus si simulable | Selon provider |
| **Lot D** | Portal connecté + adresse sauvegardée | Tests plus lourds |
| **Lot E** | Erreurs E3–E5 étendues | Complément |

### Lot A — premier lot recommandé pour implémentation

Après arbitrage du [§10](#10-décision-attendue-avant-implémentation), **implémenter en priorité le Lot A seul** offre en général le meilleur **ratio sécurité / effort** avant d’enchaîner B → E.

Contenu cible du Lot A :

- ajout panier depuis **`/shop`** et depuis **fiche produit** ;
- panier **multi-lignes** (plusieurs produits distincts) ;
- **quantités** (augmentation / modification sur ligne existante) ;
- **suppression** de ligne ;
- checkout **invité** complet jusqu’à **confirmation** de commande ;
- assertion **`sale.order`** créée si faisable en HttpCase **sans fragilité** excessive (sinon recette manuelle ou assertion atténuée documentée).

Les lots **B à E** ne sont pas engagés tant que le Lot A n’est pas arbitré et, idéalement, livré ou explicitement dépriorisé par écrit.

L’ordre **A → B → …** reste suggéré ; arbitrage MOA / technique possible.

---

## 8. Critère de réussite du chantier (implémentation future)

Une fois les lots exécutés :

- Couverture alignée avec la **priorisation** du présent ticket ;
- Tag(s) documentés ; CI verte sur les tags retenus pour la branche principale ;
- Procédure **manuelle résiduelle** listée pour le GO ouverture business si applicable.

---

## 9. Références croisées

- [`TICKET_CHECKOUT_E2E_PRE_OUVERTURE.md`](./TICKET_CHECKOUT_E2E_PRE_OUVERTURE.md)
- [`PV_PRE_OUVERTURE_COMMERCIALE.md`](./PV_PRE_OUVERTURE_COMMERCIALE.md) (risque E2E étendu mentionné)
- [`PROCEDURE_SMOKE_INSTALL_UPDATE.md`](./PROCEDURE_SMOKE_INSTALL_UPDATE.md)

---

## 10. Décision attendue avant implémentation

Avant tout développement de tests élargis, **arbitrer par écrit** :

- **Tag retenu** : enrichissement du tag existant `dorevia_ckr_checkout_e2e` **ou** création et usage de `dorevia_ckr_checkout_e2e_extended` (ou autre nom figé par l’équipe) ;
- **Périmètre exact du Lot A** : quelles lignes du tableau §1.1 et du détail [Lot A §7](#lot-a--premier-lot-recommandé-pour-implémentation) sont **incluses** dans le premier merge ;
- **Scénarios automatisés** vs **scénarios manuels** (procédure de recette pour l’ouverture contrôlée) ;
- **Données de test** à créer ou scripts de préparation (produits, transporteurs, utilisateur portal, etc.) ;
- **Critères bloquants** pour une ouverture commerciale contrôlée : ce qui **doit** être vert (CI ou check-list) vs ce qui peut être couvert **manuellement** une fois documenté.

Sans ces décisions, le présent ticket reste un **cadrage** ; il **ne mandate pas** de livraison de code.

---

## 11. Arbitrage Lot A acté (pré-implémentation) et check-list sandbox

**Date d’arbitrage** : 2026-05-07 (aligné sur la note de faisabilité technique).

### Décisions retenues

- **Tag élargi** : **`dorevia_ckr_checkout_e2e_extended`** — nouveau périmètre Lot A uniquement ; **ne pas modifier** le comportement ni la liste des tests du tag minimal **`dorevia_ckr_checkout_e2e`**.
- **Périmètre** : **strictement Lot A** (§7 et liste §11 ci-dessous) ; les lots **B / C / D / E** restent **hors scope** tant qu’ils ne sont **pas** arbitrés explicitement dans une mise à jour de ce ticket.
- **Implémentation** : **aucune livraison de code** de tests élargis tant que la **check-list sandbox** ci-dessous n’est **pas** validée sur la base cible (**référence projet : `tenant_o7`** ou équivalent documenté au moment du run).

### Risques acceptés (surveillance)

- Parsing **HTML panier** (`line_id`, quantités, suppression) potentiellement **fragile** selon évolutions **website_sale** / thème.
- **Paiement démo** indispensable pour une **preuve commande** bout-en-bout (pas seulement des GET successifs sur les routes).
- Assertion **`sale.order`** : privilégier les **preuves robustes** (référence / token confirmés) ; **plan B** documenté (assertion atténuée) si la charge de maintenance est excessive.

### Check-list sandbox — à cocher **avant** premier commit tests Lot A

Sur la base **`tenant_o7`** (ou base de test explicitement identique en config) :

1. **Provider paiement démo** : visible et **utilisable** pour le website CK ciblé par le test.
2. **Transporteur** : au moins une méthode **disponible** pour l’**adresse de test** retenue.
3. **Adresse de test** : **complète** et **compatible** règles livraison / pays / taxes.
4. **Produits** : **deux** produits **publiés**, **vendables**, **URL fiche** accessibles.
5. **HTTP** : **`/shop`** et **au moins une fiche produit** des produits de test répondent en **200**.
6. **Flux réel** : le parcours manuel (ou script de sonde) permet d’aller jusqu’à une **confirmation exploitable** (commande matérialisée), **pas** seulement enchaîner des GET sur checkout / payment / confirmation.
7. **Assertion `sale.order`** : faisabilité **raisonnable** en test automatisé, **ou** **plan B** écrit (assertion partielle / recette manuelle obligatoire) si l’assertion complète est trop fragile.

**Gate** : tant que la check-list n’est **pas** cochée, le statut d’implémentation Lot A reste **« prêt à coder après validation sandbox »** — **pas** **« en cours d’implémentation »**.

### Prochaine action

Exécuter une **courte vérification** sur l’environnement sandbox (ex. conteneur Odoo, port mappé, session `db=tenant_o7`) pour valider **paiement démo**, **livraison**, **produits** et **routes** `/shop` + fiche produit, puis consigner en une ligne (commentaire de PR ou note interne) la **date** et l’**issue** de la check-list.

---

## 12. Préflight sandbox `tenant_o7` — résultat et diagnostic court

**Date du préflight** : 2026-05-07  
**Décision** : **NO GO configuration / runtime pour Lot A E2E étendu** à ce stade — **ne pas implémenter** le tag **`dorevia_ckr_checkout_e2e_extended`** tant que les **blocages** ci-dessous ne sont pas levés ou explicitement arbitrés (recette manuelle uniquement, hors automate).

### Ce qui est validé (OK)

- **`/`** et **`/shop`** : OK.
- **Deux produits réels** (`Chips`, `Bière`) : fiches OK, prix affichés, **ajout panier** OK.
- **Panier** : deux lignes, **quantités multiples** OK ; **modification de quantité** OK.
- **Checkout** : adresse complète OK ; **transporteur** visible ; **frais** affichés (`Livraison standard`, gratuit dans ce cas).
- **Logs** runtime filtrés `ERROR|CRITICAL|Traceback|QWeb|XPath|500` : **aucune ligne** pertinente sur le périmètre testé.

### Blocage 1 — Aucun moyen de paiement test (`/shop/payment`)

**Symptôme** : message **« Aucun mode de paiement disponible »** ; aucun provider affiché.

**Impact Lot A** : impossible de **finaliser** un paiement test → pas de page **confirmation** exploitable → pas de **référence commande** ni assertion **`sale.order`** bout-en-bout.

**Diagnostic technique court (hypothèses à vérifier côté BO / modules, sans accès base ici)** :

1. **Module `payment_demo`** (ou équivalent fournissant un provider démo) : **non installé** ou désinstallé — fréquent sur une base minimaliste ; sans lui, il peut manquer les **enregistrements** `payment.provider` utilisables en test.
2. **Providers existants mais invisibles storefront** : état **non publié**, **website** non relié au site CK, **journal** / **société** / **devise** incohérents avec la boutique, ou filtre Odoo qui exclut tous les providers pour ce website.
3. **Paiement e-commerce** : vérifier **Paramètres → Website → Paiement** (terminologie Odoo 19) que les providers sont **activés** pour le canal vente web.

**Pistes d’action BO** (ordre logique) : installer **`payment_demo`** si absent → rouvrir **Comptabilité / Paiement / Providers** → activer **Demo** pour le **website** concerné → associer **journal de paiement** valide → republier → retester `/shop/payment`.

---

### Blocage 2 — Suppression d’une ligne panier KO (JS)

**Symptôme** : suppression ligne **échoue** ; console :

`TypeError: Cannot read properties of null (reading 'classList')`

**Impact Lot A** : le périmètre inclut **suppression de ligne** ; tant que le parcours est **instable** en navigateur, l’automate ou la recette « complète » restent **non fiables**.

**Diagnostic technique court** :

- L’erreur est typique d’un script qui applique **`classList`** sur un **élément DOM introuvable** après une interaction (RPC panier + mise à jour UI).
- **Module CK** : les JS livrés (`ckr_cart_feedback.js`, etc.) utilisent `classList` sur le **toast** et le **badge header**, pas sur les lignes panier — **cause peu probable** pour la suppression seule, sauf effet de bord indirect (timing / mutation observer).
- **Cause probable** : JS **standard `website_sale`** (ou bundle thème) qui suppose une **structure HTML** de ligne panier (ids / classes) ; **écart** avec le DOM rendu par **`theme_classic_store`** ou un **xpath CK** sur la page panier.
- **Étape suivante** : reproduire avec **trace complète** (fichier + ligne dans la stack, pas seulement le message) ; comparer le HTML de **`#shop_cart`** avec une instance **vanilla** Odoo 19 + même thème ; identifier le **sélecteur** qui renvoie `null`.

**Correctif attendu** : **minimal** — aligner un héritage QWeb ou un patch JS **ciblé** une fois la ligne de code source identifiée ; **pas** de refonte panier.

---

### Synthèse décisionnelle

| Condition | Statut |
| --- | --- |
| Check-list §11 point 1 (paiement démo utilisable) | **KO** |
| Check-list §11 point 6 (flux jusqu’à confirmation réelle) | **KO** (bloqué par paiement) |
| Suppression ligne panier (Lot A) | **KO** (JS) |

**Gate Lot A** : **fermé** jusqu’à correction **sandbox paiement** + **suppression panier** (ou réécriture du périmètre Lot A pour **exclure** la suppression et documenter **paiement** exclusivement via **données de test injectées en CI** — arbitrage MOA / tech).

---

## 13. Plan de déblocage — deux gates puis nouveau préflight

**Décision actée** : le Lot A E2E étendu reste **bloqué** ; **ne pas implémenter** le tag **`dorevia_ckr_checkout_e2e_extended`** tant que les gates ci-dessous ne sont pas **GO**. Priorité au **déblocage runtime** sandbox ; pas de correctif CK « au hasard » sur le panier avant **stack JS complète**.

### Gate 1 — Paiement test (configuration / environnement)

Traiter d’abord comme **sujet de configuration sandbox**, pas comme bug module CK.

**À contrôler** (BO / modules) :

- module **`payment_demo`** installé ou non ;
- provider **Demo** activé ;
- provider **publié** et **utilisable** pour le **website CK** ;
- **journal** / **société** / **devise** cohérents ;
- site web correctement relié au provider ;
- **`/shop/payment`** affiche au moins **un** moyen de paiement test.

**Critère GO** : au moins **un** provider test **utilisable** apparaît sur **`/shop/payment`**.

### Gate 2 — Suppression ligne panier (diagnostic puis correctif minimal)

**Ne pas coder à l’aveugle.** Recueillir au clic suppression :

- fichier **JS** ;
- **ligne** ;
- **fonction** ;
- **contexte DOM** (élément attendu absent ou déplacé).

**Objectif** : trancher **`website_sale`** standard vs **`theme_classic_store`** vs **vue CK** qui altère le DOM attendu.

**Critère GO** : suppression d’une ligne panier **sans erreur JS** en navigation réelle.

### Enchaînement

1. Lever **Gate 1** puis **Gate 2** (ordre recommandé : paiement d’abord si les deux peuvent être menés en parallèle côté équipe, sinon Gate 1 souvent plus rapide).
2. **Relancer le préflight Lot A** (repasser la check-list du §11 et le scénario §12).
3. **Seulement si le préflight passe** : réarbitrer l’**implémentation** du tag **`dorevia_ckr_checkout_e2e_extended`** (toujours sans toucher au tag minimal **`dorevia_ckr_checkout_e2e`** sans décision explicite).

---

## 14. Implémentation livrée (Lot A — tag étendu)

**Référence code** : `tests/test_ckr_checkout_e2e_extended_lot_a.py`  
**Tag Odoo** : `dorevia_ckr_checkout_e2e_extended` (le tag minimal `dorevia_ckr_checkout_e2e` reste distinct et inchangé).

**Décisions documentaires** :

* Objectif : parcours marchand **HTTP déterministe** (listing → fiches → JSON-RPC panier → adresse invité → paiement Demo → confirmation), **sans** simulation de clic sur les boutons « ajouter » des tuiles `/shop` (cf. docstring du test).
* **Prérequis** : module **`payment_demo`** installé et enregistrements Demo présents ; sinon le test est **ignoré** explicitement (`skipTest`).
* **Assertion `sale.order`** : recherche par **email partenaire** lorsque la commande est retrouvée ; si aucune correspondance (effets de contexte / partenaire), le test ne s’appuie pas sur cet échec seul une fois la **confirmation HTTP** validée (plan B décrit dans le code).
* **État `sale.order.state`** : le Lot A prouve le parcours marchand HTTP complet jusqu’à la confirmation avec paiement Demo. L’état final `sale.order.state` dépend de la configuration paiement / confirmation Odoo et peut rester **`draft`** en sandbox ou avec le provider Demo ; **l’assertion backend ne doit pas être bloquante sur `sale` / `done` pour ce tag** — plage tolérée dans le test : `draft`, `sale`, `done`.

---

## Synthèse exécutive

**Pourquoi** : ouverture commerciale contrôlée = risque réduit si les parcours d’achat **fréquents** et les **échecs maîtrisés** sont connus et en partie automatisés.

**Quoi** : liste priorisée ci-dessus + tags + lots ; pas de travaux hors tunnel marchand.

**Comment** : tag dédié **`dorevia_ckr_checkout_e2e_extended`** pour le Lot A (le minimal **`dorevia_ckr_checkout_e2e`** reste inchangé) ; voir [§11](#11-arbitrage-lot-a-acté-pré-implémentation-et-check-list-sandbox).

**Quand le ticket « cadrage » est clos** : décisions écrites sur indispensable / auto / manuel / données — **avant** le premier merge de tests élargis massifs.
