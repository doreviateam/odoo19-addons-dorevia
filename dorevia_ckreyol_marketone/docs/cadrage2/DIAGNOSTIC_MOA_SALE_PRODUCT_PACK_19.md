# Diagnostic MOA — Port OCA `sale_product_pack` Odoo 19 CE

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-08 |
| **Ticket** | [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md) |
| **Contexte amont** | Lot 6.3b **GO clôture MOA** `19.0.18.0.0` — porte front OK · explosion composants **hors v1** |
| **Base audit** | Sandbox `ckr-marketone-01` · Odoo **19.0-20260324** |
| **Nature** | Diagnostic technique **avant implémentation** — pas de code Marketone |

---

## Verdict MOA proposé

| Option | Recommandation |
|--------|----------------|
| Activer `sale_product_pack` tel quel (copie locale) | **NON** — non installable · code pré-migration 18.0 |
| Implémenter un moteur pack Marketone | **NON** — hors doctrine |
| **Reporter l’activation prod** · **poursuivre le port OCA** sur branche dédiée | **OUI — recommandé** |
| Module pont Dorevia minimal | **Seulement si** écart résiduel post-merge OCA (eCommerce / pricelist) — **à trancher après tests OCA** |

**Formulation MOA** : **GO diagnostic** · **NO GO activation immédiate** · **GO plan port OCA minimal** (phase Dev isolée, sans `depends` Marketone).

---

## Doctrine (rappel)

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

- `dorevia_ckreyol_marketone` **ne doit pas** porter la logique d’explosion composants.
- L’activation attendue = **modules OCA** (`sale_product_pack` + chaîne stock si besoin), installés au niveau plateforme / BO.

---

## 1. Pourquoi `sale_product_pack` est non installable aujourd’hui

### 1.1 Décision dépôt Dorevia (volontaire)

Dans `odoo19-addons-oca/sale_product_pack/__manifest__.py` :

```python
# Copié depuis OCA/product-pack branche 18.0 — installable False jusqu’au port fonctionnel 19.0.
"installable": False,
```

Même pattern pour `stock_product_pack` et `sale_stock_product_pack`.

| Module | Version dépôt | `installable` | État DB sandbox |
|--------|---------------|---------------|-----------------|
| `product_pack` | `19.0.1.0.2` | **True** | installé (via Marketone 6.3b) |
| `sale_product_pack` | `19.0.1.0.0` | **False** | `uninstallable` |
| `stock_product_pack` | `19.0.1.0.0` | **False** | `uninstallable` |
| `sale_stock_product_pack` | `19.0.1.0.0` | **False** | `uninstallable` |

### 1.2 Blocage technique confirmé (tentative d’installation)

Commande exécutée sur sandbox (`-i sale_product_pack` avec `installable=True` temporaire) :

```text
ImportError: cannot import name 'first' from 'odoo.fields'
  → sale_product_pack/models/sale_order_line.py
```

**Cause** : la copie locale est une base **18.0** non migrée. En Odoo 19, `odoo.fields.first` n’existe plus.

### 1.3 État amont OCA (2026-06-08)

Migration 19.0 **en cours** sur [OCA/product-pack](https://github.com/OCA/product-pack) :

| Module | Issue / PR | Statut indicatif |
|--------|------------|------------------|
| `product_pack` | #223 | **Merged** (installable chez nous) |
| `sale_product_pack` | #244 | **PR ouverte** — `installable: True` dans la branche migrée |
| `stock_product_pack` | #227 | PR migrée (ready to merge) |
| `sale_stock_product_pack` | #230 | PR migrée |
| `website_sale_product_pack` | #229 | PR migrée — **absent du dépôt Dorevia** |

La branche migrée OCA (commit `5aab4b7` de PR #244) corrige notamment :

- suppression de `from odoo.fields import first` → `filtered(...)[:1]`
- `product_uom` → `product_uom_id` (onchange)
- `_()` → `self.env._()`
- ajout `_compute_name` pour l’indentation des lignes pack **detailed**

---

## 2. Écarts de portage Odoo 19 (copie locale vs OCA migré)

| Zone | Copie locale `odoo19-addons-oca` | Attendu Odoo 19 / PR OCA |
|------|----------------------------------|---------------------------|
| Import `first` | **Présent** — bloque le chargement | Supprimé |
| Onchange SOL | `product_uom` | `product_uom_id` |
| Tests | `groups_id` sur `res.users` | Probablement `groups_id` → vérifier API 19 (`group_ids` ?) |
| Action window | `view_type: "form"` (deprecated) | À nettoyer en review OCA |
| `product_pack_line.get_sale_order_line_vals` | `_onchange_product_id_warning()` | À valider sur 19 (peut être remplacé par compute) |
| Manifest | `installable: False` | `installable: True` post-migration |

**Conclusion** : le port **existe côté OCA** (PR non mergée) ; le dépôt Dorevia est **volontairement gelé** sur une révision **pré-19**.

---

## 3. Comportement fonctionnel OCA — impact CK Marketone

### 3.1 Configuration packs actuelle recette 6.3b

Script prep / produits recette :

```python
pack_type = "non_detailed"
pack_component_price = "ignored"
```

Conséquence **`sale_product_pack`** (test OCA `test_create_non_detailed_price_order_line`) :

- commande vente = **1 seule ligne** (le pack)
- **aucune explosion** de lignes composants en vente

→ **Installer `sale_product_pack` seul ne change rien** au comportement SO/panier v1 Marketone tant que les packs restent `non_detailed`.

### 3.2 Quand l’explosion composants intervient

| `pack_type` | Lignes SO après `sale_product_pack` | Stock / picking (avec chaîne stock) |
|-------------|-------------------------------------|-------------------------------------|
| `non_detailed` | **1 ligne pack** | Composants **non** sortis automatiquement — ROADMAP OCA : besoin **`sale_stock_product_pack`** pour pickings composants |
| `detailed` | **1 ligne pack + N lignes composants** | `stock_product_pack` + `sale_stock_product_pack` : moves composants · qty pack dérivée des enfants |

### 3.3 Chaîne modules pour la profondeur métier visée

```text
product_pack          ← déjà actif (6.3b)
    ↓
sale_product_pack     ← explosion lignes SO (detailed uniquement)
    ↓
stock_product_pack    ← qty dispo pack · dont_create_move · règles procurement
    ↓
sale_stock_product_pack ← qty_delivered pack · compat SO + stock
```

**Facturation** : avec `invoice_policy=delivery` et packs stockables, `sale_stock_product_pack` aligne `qty_delivered` du pack sur les composants livrés (test OCA `test_delivered_quantities`).

**Préparation / picking** : moves sur **composants** (pas le produit pack parent si `dont_create_move=True` + `detailed`).

### 3.4 eCommerce / panier Marketone

- Lot 6.3b : panier = **1 ligne pack** (`website_sale` standard) — **validé MOA**.
- Sans `website_sale_product_pack` (absent du dépôt) : comportement checkout eCommerce avec packs **detailed** à **recetter** après port (expansion lignes lors `_cart_add` / update prices — contextes `update_prices` / `update_pricelist` gérés par OCA).
- **Pas de widget composants Marketone** — composants fiche = natif OCA BO / fiche produit.

---

## 4. Test comportement commande (état actuel sans `sale_product_pack`)

Sur `ckr-marketone-01` **sans** `sale_product_pack` installé :

| Action | Résultat |
|--------|----------|
| `_cart_add` pack tmpl **7** | **1 ligne** « Maniocookies salés La Platine » |
| Prix ligne | Moteur Odoo pricelist (ex. 4,17 € avec promo 6.3a active) |
| Confirmation SO | Non rejouée dans ce diagnostic — **pas d’explosion composants** attendue |

**Après port OCA** (pack `detailed` + `sale_product_pack`) : attendu **3 lignes** (pack + 2 composants) sur commande BO — à valider par tests OCA `dorevia`/OCA sur sandbox.

---

## 5. Impacts métier documentés

| Processus | Sans chaîne sale/stock pack | Avec chaîne OCA complète (pack `detailed` + modules) |
|-----------|----------------------------|------------------------------------------------------|
| **Vente / devis** | 1 ligne pack | Lignes pack + composants (prix selon `pack_component_price`) |
| **eCommerce** | 1 ligne panier (6.3b v1) | Recette à refaire — expansion au checkout si pack detailed |
| **Stock réservé** | Sur produit pack uniquement | Sur **composants** stockables |
| **Préparation** | Picking pack (si stockable) | Pickings **composants** |
| **Facturation** | Pack entier | Pack / composants selon `invoice_policy` · `qty_delivered` agrégée via `sale_stock_product_pack` |
| **Disponibilité pack** | `product_pack` seul | `stock_product_pack` calcule dispo = min(composants / qty) |

---

## 6. Plan de port minimal recommandé (sans Marketone)

### Phase A — Alignement OCA (Dev plateforme)

1. Récupérer les révisions migrées depuis OCA :
   - PR **#244** `sale_product_pack`
   - PR **#227** `stock_product_pack`
   - PR **#230** `sale_stock_product_pack`
   - Évaluer **#229** `website_sale_product_pack` si eCommerce detailed requis
2. Remplacer / fusionner dans `odoo19-addons-oca/` (branche Dev dédiée).
3. Installer sur sandbox `ckr-marketone-01` **sans** modifier `dorevia_ckreyol_marketone`.
4. Exécuter tests OCA :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 \
  --test-tags=/sale_product_pack,/stock_product_pack,/sale_stock_product_pack \
  --stop-after-init --http-port=0
```

### Phase B — Décision MOA configuration produit

| Choix | Effet |
|-------|--------|
| **B1** — Conserver `non_detailed` + activer seulement `sale_product_pack` | **Peu de gain métier** (1 ligne SO inchangée) · stock composants toujours non géré |
| **B2** — Passer packs CK en `detailed` + `totalized` ou `ignored` + chaîne complète | **Explosion composants** conforme OCA · **recette BO + eCommerce** obligatoire |
| **B3** — Attendre merge OCA officiel 19.0 | **Risque minimal** maintenance · délai |

**Recommandation technique** : viser **B2** pour l’objectif « profondeur Odoo packs » · **B3** en calendrier si contrainte MOA délai / stabilité OCA.

### Phase C — Module pont Dorevia (conditionnel)

**Uniquement si** après Phase A un écart subsiste (ex. pricelist eCommerce, contexte checkout) :

- module **`dorevia_product_pack_sale`** (nom indicatif) · `depends: ['sale_product_pack', 'website_sale']`
- **aucune** logique d’explosion custom · héritages minimaux / tests de non-régression Marketone
- **ne pas** ajouter `sale_product_pack` dans `depends` de `dorevia_ckreyol_marketone`

### Phase D — Recette MOA post-port

- Scénario BO : pack recette **7** en `detailed` · commande · confirmation · picking · facture
- Non-régression 6.3b front : porte pack inchangée · panier selon décision B1/B2
- Mise à jour ADR-035 **si** changement de socle (activation `sale_product_pack` explicite MOA)

---

## 7. Alternatives écartées

| Alternative | Verdict |
|-------------|---------|
| Moteur `marketone.pack.*` | **Interdit** — doctrine |
| Explosion JS / contrôleur Marketone | **Interdit** |
| Réimplémentation partielle dans Marketone | **Interdit** |
| Rester sur `product_pack` seul indéfiniment | **Acceptable v1** — déjà clôturé 6.3b · **insuffisant** pour stock/prépa/facture composants |

---

## 8. Risques et réserves

| Risque | Mitigation |
|--------|------------|
| PR OCA non mergées | Suivre #222 · pin commit SHA · PR Dorevia vers OCA si patches |
| Régression eCommerce 6.3b | Recette R4 + checkout pack après `website_sale_product_pack` |
| Cohabitation promo 6.3a + pack detailed | Recette prix pricelist sur lignes composants |
| PR #234 « modifiable non-detailed » | Relire avant B1 — pourrait modifier le périmètre `non_detailed` |

---

## 9. Synthèse pour décision MOA

| Question MOA | Réponse diagnostic |
|--------------|-------------------|
| Peut-on activer `sale_product_pack` maintenant ? | **Non** — code local non migré · OCA PR #244 non mergée |
| Faut-il un module Marketone ? | **Non** pour l’explosion · pont **optionnel** post-OCA |
| Quel travail minimal ? | Sync PR OCA 244/227/230 (+229 si eCommerce) · tests · recette BO |
| Impact si on n’active pas ? | Front 6.3b OK · back vente/stock/facture reste « pack = produit simple » |
| Prochaine priorité Dev ? | **Phase A** sur branche isolée · **pas** de nouvelle porte front |

---

## Références

| Ressource | Lien |
|-----------|------|
| Ticket maintenance | [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md) |
| Clôture 6.3b | [`RECEPTION_MOA_LOT6_3B_PACK.md`](./RECEPTION_MOA_LOT6_3B_PACK.md) |
| Décision K2 hors v1 | [`DECISION_MOA_LOT6_3B_KITS_COFFRETS.md`](./DECISION_MOA_LOT6_3B_KITS_COFFRETS.md) |
| OCA migration 19.0 | [Issue #222](https://github.com/OCA/product-pack/issues/222) |
| PR sale_product_pack | [PR #244](https://github.com/OCA/product-pack/pull/244) |
| Source locale | `odoo19-addons-oca/sale_product_pack/` |
