# Note de livraison — Fiche produit CK · Zone 0 + Onglets

**Projet** : C-Kreyol — Odoo 19  
**Modules** : `dorevia_ck_theme` **19.0.1.35.7** · `dorevia_ck_marketone_content` **19.0.1.25.29**  
**Date** : juin 2026

---

## Principe UX validé MOA

```text
Zone 0 = achat immédiat
Onglets = complément, réassurance, légal
```

---

## Zone 0 (inchangée structurellement)

Bloc achat Lot 1 conservé :

* image · titre · meta (origine · tags · format · prix réf.)
* accroche `description_ecommerce`
* prix · variantes · CTA · favori · réassurance courte

---

## Onglets complémentaires

Regroupement des sections parser `website_description` via `get_ck_product_page_tabs()` :

| Onglet | Contenu |
|--------|---------|
| **Découvrir** | `origin_usage`, `usage`, `origin_producer` |
| **Composition** | `ingredients`, `nutrition` |
| **Conservation & livraison** | `conservation` + note livraison |
| **Détails produit** | specs factuelles (origine attribut, catégorie, contenance, prix réf., attributs, référence) |

Onglets affichés **uniquement si alimentés**.

---

## Éléments retirés / masqués

* Grande section verticale « À propos de ce produit »
* `product_full_description` natif (si onglets CK)
* Table `product_attributes_simple` dans la zone achat
* Accordéon Spécifications Odoo natif
* Bloc documents dupliqué en zone achat
* Grande section snippet `s_ck_product_pro_signal`

---

## Passerelle professionnelle

Ligne discrète sous les onglets (toujours visible sur fiche CK) :

```text
Vous commandez pour un commerce ou un restaurant ? Espace professionnel CK
```

---

## Markdown brut

Sanitisation légère `*Usage :*` → `Usage :` dans `product_page_tabs._sanitize_section_body` (pas de parser Markdown).

---

## Contraintes respectées

| Contrainte | Statut |
|------------|--------|
| Pas de nouveau champ | ✅ |
| Pas de modification BO | ✅ |
| Pas de modification parser | ✅ |
| Zone haute Lot 1 | ✅ |
| `website_description` source éditoriale | ✅ |
| `description_sale` hors hypothèse UX | ✅ |

---

## Tests

Tags : `dorevia_ck_product_page_tabs`, `dorevia_ck_product_page_lot2_front`, `dorevia_ck_theme_phase4`

---

## Documents liés

- `NOTE_FICHE_PRODUIT_LOT2_FRONT_SECTIONS_LONGUES_CK_V1.md` (lot précédent — remplacé structurellement par onglets)
- `NOTE_CLARIFICATION_PARSER_WEBSITE_DESCRIPTION_CK_V1.md`
- `CARTOGRAPHIE_CHAMPS_PRODUIT_CK_V1.md`
