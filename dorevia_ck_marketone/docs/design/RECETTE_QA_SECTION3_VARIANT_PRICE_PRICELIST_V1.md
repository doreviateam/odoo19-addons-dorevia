# Recette QA — Section 3 · Prix variante · Pricelist active · V1

| Champ | Valeur |
|-------|--------|
| **Périmètre** | Prix cards « Nos coups de cœur » avec **liste de prix publique active** (cible CK B2C) |
| **Module** | `dorevia_ck_marketone_content` ≥ **19.0.1.25.6** |
| **Tag tests auto** | `dorevia_ck_marketone_home_section3_pricelist` |
| **Script Playwright** | `docs/design/maquette_01.2/scripts/ck_section3_variant_price_pricelist_recette.mjs` |
| **Prérequis instance** | Groupe Odoo **Pricelists** activé · liste **CK B2C Recette** (ou équivalent) liée au site |

```text
Le correctif 25.5 corrige template.list_price → variant.lst_price sans pricelist.
La cible commerciale CK impose la validation avec pricelist active (B2C, futur B2B).
```

---

## 1. Prérequis instance recette

1. Activer **Ventes → Paramètres → Pricelists** (`product.group_product_pricelist`).
2. Créer une liste de prix **CK B2C Recette** :
   - `selectable = True`
   - `website_id` = site CK
3. Règles **par variante** (Manio Crackers) :
   - `Manio Crackers salé` → **3,60 €** (`applied_on = Product Variant`)
   - `Manio Crackers sucré` → **3,50 €**
4. `-u dorevia_ck_marketone_content` puis redémarrage Odoo si assets touchés.

---

## 2. Tests automatisés (obligatoires)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 \
  --test-enable --stop-after-init --http-port=18088 \
  --test-tags=dorevia_ck_marketone_home_section3_pricelist
```

| ID | Critère MOA | Couverture |
|----|-------------|------------|
| P1 | Pricelist active sur le site | `test_pricelist_available_on_website` |
| P2 | `_get_product_price(variant)` par variante | `test_get_product_price_per_variant` |
| P3 | Card suit la pricelist (pas le lst_price) | `test_featured_price_uses_pricelist_not_template` |
| P4 | Règle variante salé ne contamine pas sucré | `test_variant_rule_does_not_contaminate_sibling` |
| P5 | Produit simple sans variante | `test_simple_product_pricelist_price` |
| P6 | Prix au kg cohérent | `test_reference_price_coherent_with_pricelist_amount` |
| P7 | Manio salé : home = fiche = panier | `test_home_card_product_cart_price_alignment_sale` |
| P8 | Manio sucré : home = fiche = panier | `test_home_card_product_cart_price_alignment_sweet` |

**Verdict auto attendu** : 0 failed.

---

## 3. Recette Playwright (complément visuel)

```bash
node docs/design/maquette_01.2/scripts/ck_section3_variant_price_pricelist_recette.mjs
```

Contrôles : prix cards home Manio salé/sucré, cohérence avec fiche produit (HTTP).

---

## 4. Verdict MOA

| Verdict | Condition |
|---------|-----------|
| **GO** | Tests P1–P8 OK + script Playwright OK |
| **NO GO** | Écart card / fiche / panier ou contamination variantes |
