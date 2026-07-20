# S3-A — Audit overrides panier & avertissements de stock
**Garant, lecture seule — 2026-07-19**

## Méthode

Comparaison contre la **source Odoo 19 authentique**, extraite de l'image locale `odoo:19.0` (`f54272f31d5f`) — pas de la 18 ni de mémoire. Ce point est déterminant : ma première lecture, basée sur la 18.0 disponible sur disque, était **fausse** sur un point majeur (voir ci-dessous). Source CK : `odoo19-addons-dorevia @ 68abda8`, arbre propre.

## Cartographie

| Élément | Emplacement |
|---|---|
| Override Python | [sale_order_line.py:8](../../dorevia_ck_marketone_content/models/sale_order_line.py) (18 lignes) |
| Override JS | [ck_cart_stock_warning.js:14](../../dorevia_ck_marketone_content/static/src/js/ck_cart_stock_warning.js) (51 lignes) |
| Asset déclaré | `__manifest__.py:69` → `web.assets_frontend` |
| Dépendance | `website_sale_stock` **présente** au manifeste ✅ surcouche correctement ordonnée |
| Test Python | `test_ck_checkout_stock_001.py:34` (1 test sur le message) |
| Test JS / tour | **aucun** |
| Vue / route / RPC propre | **aucune** — CK réutilise `/shop/cart/update` standard |

Aucune autre dépendance Python↔JS que le champ `data.warning` renvoyé par la route standard.

---

## Zone A — `sale.order.line._set_shop_warning_stock`

### Correction d'une prémisse du mandat

Le mandat postule « remplacement complet du cœur, sans `super()`, signature divergente ». **La signature ne diverge pas.** Odoo 19 standard :

```python
def _set_shop_warning_stock(self, desired_qty, new_qty, save=True):
```

Le paramètre `save` n'est **pas** une invention CK : il existe en 19 (il n'existait pas en 18). CK est **structurellement conforme** : `ensure_one()`, `self.env._()`, gestion de `save`, retour de la variable locale — tout est identique. Le seul écart est **le texte du message**.

C'est un override de personnalisation de libellé, pas une réécriture de logique. Il n'y a d'ailleurs aucun hook standard permettant de changer ce texte sans réécrire la méthode.

### Écarts réels

| # | Écart | Sévérité |
|---|---|---|
| **A1** | Message source **écrit en français**, sans catalogue `.po` CK. Le standard a une source EN + traduction FR livrée. → **un visiteur EN voit du français.** Régression i18n directe vs standard | **haute** |
| **A2** | `unité(s)` est **codé en dur**. Or le cœur 19 convertit `available_qty` dans l'UoM demandée (`_compute_quantity` + `float_round`). Un produit vendu en kg afficherait « 2 unité(s) ». Le standard évite le piège en ne nommant **jamais** l'unité | **moyenne** (latente) |
| **A3** | `desired_qty` est **accepté puis jamais utilisé**. L'information « vous avez demandé 10 » est perdue ; seul le plafond est affiché | **moyenne** |
| **A4** | `product_id.name` perdu. Sans conséquence sur le chemin toast (l'utilisateur vient de modifier cette ligne) ni sur le rendu inline `shop_warning` (positionné près de la ligne). Impact réel faible | **basse** |
| **A5** | CK n'override **que** la méthode sur `sale.order.line`. En 19, `sale.order._set_shop_warning_stock` **n'existe plus** : la branche « produit ajouté sans ligne existante » (Odoo 19 `website_sale_stock` / `sale.order` — branche ajout sans ligne existante) génère son propre message inline. → **deux formulations différentes** selon ligne existante ou nouvelle | **moyenne** |

### Précision sur A2

`dorevia.ck.card.uom` (g/kg/ml…) est un modèle **CK d'affichage de fiche produit** (quantité nette, prix de référence) — il ne pilote **pas** `uom_id` de vente. Le défaut A2 n'est donc **pas actif** tant que tous les produits se vendent en « Unités ». Je le classe **latent**, pas avéré. À confirmer en QA sur données réelles.

### Verdict Zone A
> **Override complet mais justifié** — sévérité **moyenne**.
> La structure est conforme au standard 19. Ce sont les **contenus** (i18n, unité, perte de `desired_qty`) qui doivent être corrigés, pas le principe de l'override.

---

## Zone B — `CartLine._changeQuantity`

### Diff réel contre le standard 19

J'ai comparé ligne à ligne avec `website_sale/static/src/interactions/cart_line.js`. La méthode CK est une **copie fidèle** du standard, à **trois** différences près :

| Ligne | Standard 19 | CK | Nature |
|---|---|---|---|
| 56/58 | `parseInt(input.value \|\| 0)` | `parseInt(..., 10)` | cosmétique (radix explicite) |
| 57 | `isNaN(quantity)` | `Number.isNaN(quantity)` | équivalent ici (`parseInt` retourne toujours un nombre) |
| **83** | `wSaleUtils.showWarning(data.warning)` | `cartNotificationService?.add('', { warning })` | **seul changement fonctionnel** |

Tout le reste est préservé : RPC, garde `!data.cart_quantity` + redirect, propagation `data.quantity` vers tous les inputs, cycle `stopInteractions`/`updateCartNavBar`/`updateQuickReorderSidebar`/`startInteractions`, event bus `cart_amount_changed`.

**Conséquences pour les points de contrôle du mandat :**

- Debounce, changements rapides, verrouillage concurrent : **intacts** — ils vivent dans `dynamicContent` (`this.locked(this.debounced(..., 500))`), que CK ne touche pas.
- Suppression de ligne / quantité nulle : **intacte** (`deleteProduct` → `_changeQuantity`, garde `cart_quantity`).
- Recalcul des totaux, navbar, sidebar réassort : **intacts**.
- Double appel / désync DOM-serveur : **pas de risque ajouté** (`waitFor` + `locked` conservés).
- Comportement perdu : **le bandeau `#data_warning`**, volontairement — documenté en tête de fichier (anti-doublon bandeau+toast).

### Le vrai risque

Il n'est **pas** dans une divergence actuelle — la copie est en phase avec 19.0 aujourd'hui. Il est dans le **mécanisme** : `patch()` sans `super._changeQuantity()` fige une copie de 87 lignes pour n'en changer qu'**une**. Toute évolution amont de `_changeQuantity` (nouveau service, nouveau champ de payload, correctif de concurrence) sera **silencieusement perdue** à la montée de version — sans erreur, sans test rouge.

C'est un ratio coût/bénéfice défavorable : **86 lignes de surface de divergence pour 1 ligne de besoin métier.**

### Verdict Zone B
> **Override complet à réduire** — sévérité **haute** (risque montée de version), **basse** (risque en exploitation courante).

---

## Cible technique recommandée

### Zone B — réduction à un patch minimal

`showWarning` est exporté sur l'objet `default` de `website_sale_utils` et — vérifié sur l'ensemble d'Odoo 19 — possède **exactement un appelant** : `cart_line.js:83`. Le rayon d'impact d'un patch sur cette fonction est donc **nul hors panier**.

```js
// esquisse d'intention — à concevoir et implémenter par le Dev
patch(wSaleUtils, {
    showWarning(message) { /* toast cartNotificationService */ },
});
```

Gains : `_changeQuantity` n'est plus copiée, toute évolution amont est héritée, la surface passe de ~50 lignes à ~8.

**Réserve à traiter par le Dev** : ce patch *échoue en silence* si Odoo renomme ou inline `showWarning` — le warning disparaîtrait sans erreur. Il doit donc être **accompagné d'un test de garde** vérifiant que le toast est bien émis.

### Zone A — corrections de contenu, override conservé

1. Message source en **anglais** + traduction FR dans un `.po` CK → rétablit EN.
2. **Retirer** `unité(s)` ou l'aligner sur l'UoM réelle de la ligne.
3. **Exploiter `desired_qty`** (le standard le fait).
4. Traiter A5 : soit aligner le ton sur la branche « nouvelle ligne », soit assumer l'écart explicitement.

---

## Découpage Dev proposé

| Lot | Contenu | Risque |
|---|---|---|
| **S3-B1** | Réduction JS au patch minimal + test de garde | faible, fort gain upgrade |
| **S3-B2** | Message Python : i18n EN/FR, UoM, `desired_qty` | faible |
| **S3-B3** | Arbitrage A5 (cohérence ligne existante / nouvelle) | décision MOA d'abord |

B1 et B2 sont indépendants et parallélisables.

## Scénarios QA indispensables

1. Ligne existante, quantité > stock → toast, valeur plafonnée, **un seul** message (pas bandeau + toast).
2. **Nouveau** produit hors stock (aucune ligne) → vérifier la formulation (cible A5).
3. **Multi-lignes** : deux produits contraints, message non ambigu.
4. Quantité 0 / suppression → redirect `/shop/cart` correct.
5. Clics rapides +/- → debounce 500 ms, pas de double RPC, pas de désync.
6. **Locale EN** → message en anglais (couvre A1).
7. Produit en UoM non-unitaire, si le catalogue en contient (couvre A2).
8. Mobile 390 px → toast visible, non tronqué.
9. Validation panier (`_check_availability`) → message inline cohérent.

Points 6 et 7 sont **absents de la couverture actuelle** ; le seul test existant appelle la méthode en direct avec `save=False` et ne couvre ni l'intégration, ni l'UoM, ni l'i18n.

---

## Verdict

> ### `CORRECTION RECOMMANDÉE`

Rien n'est cassé en exploitation nominale (locale FR, produits en Unités). Aucun caractère bloquant immédiat.

**Mais** — et cela valide ton hypothèse de départ — la Zone B est un **prérequis réel avant toute montée de version Odoo**. Sur ce périmètre précis, le verdict devient `CORRECTION PRIORITAIRE`. La bonne nouvelle est que le correctif est peu coûteux : une ligne de besoin métier, un patch de huit lignes.

Je nuance en revanche la prémisse du mandat : ces overrides sont nettement **moins divergents** que le finding S2 initial ne le laissait craindre. La signature Python est conforme au standard 19, et le JS est une copie fidèle. Le problème est de **mécanisme** (surface de copie) et de **contenu** (i18n/UoM), pas de logique métier erronée.

## Mandat respecté

Aucune modification de code, aucun commit, aucun push, aucune PR, aucun déploiement, aucune intervention sur environnement partagé. Les seules exécutions ont été des lectures et une extraction en conteneur jetable `--rm` de l'image Odoo officielle locale.

**Arrêt sur rapport — en attente d'arbitrage MOA.**
