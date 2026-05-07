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

## Synthèse exécutive

**Pourquoi** : ouverture commerciale contrôlée = risque réduit si les parcours d’achat **fréquents** et les **échecs maîtrisés** sont connus et en partie automatisés.

**Quoi** : liste priorisée ci-dessus + tags + lots ; pas de travaux hors tunnel marchand.

**Comment** : étendre `dorevia_ckr_checkout_e2e` par enrichissement ou introduce `dorevia_ckr_checkout_e2e_extended` selon charge ; garder le minimal stable.

**Quand le ticket « cadrage » est clos** : décisions écrites sur indispensable / auto / manuel / données — **avant** le premier merge de tests élargis massifs.
