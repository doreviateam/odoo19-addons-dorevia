# Composition CMS — Header marchand V1.2 · CK Marketone

| Champ | Valeur |
|-------|--------|
| **Instance** | `dorevia_ck_marketone_01` |
| **URL test** | http://localhost:18079/ |
| **Date** | 2026-06-13 |
| **Ticket** | [`ticket_moa_composition_cms_ck_01`](../ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) §2.4 |
| **GO séquence** | [`go_reprise_odoo_v1_2.md`](./go_reprise_odoo_v1_2.md) |
| **Prérequis** | [`COMPOSITION_PROFESSIONNELS_V1_2.md`](./COMPOSITION_PROFESSIONNELS_V1_2.md) |
| **Statut** | **Phase 1 OK QA · recette MOA/QA recommandée** |
| **Recette Phase 1** | [`RECETTE_QA_PHASE1_HEADER_FOOTER_CK_V1.md`](./RECETTE_QA_PHASE1_HEADER_FOOTER_CK_V1.md) |

---

## 1. Objectif MOA

Aligner le **header marchand** sur la maquette V1.2 **avant** la reprise des blocs home :

* menu **Phase 1 livré** : **Boutique · Découvrir · Professionnels** ;
* **Producteurs** : absent (pas de cible CMS · gate MOA) ;
* **recherche** + **panier** natifs Odoo ;
* lien **Professionnels** → `/professionnels` (page composée — pas de 404) ;
* header **sobre, clair, marchand** — sans surcharge ;
* desktop + mobile **sans overflow horizontal**.

Garde-fous : CMS / BO uniquement · pas de dev hors thème autorisé · parcours natifs Odoo conservés.

---

## 2. Livrables

| # | Élément | Statut | Détail |
|---|---------|--------|--------|
| 1 | Menu **Boutique** → `/shop` | ✅ | Sequence 10 |
| 2 | Menu **Catégories** → `/shop` | ✅ | Sequence 20 · entrée catalogue native |
| 3 | Menu **Professionnels** → `/professionnels` | ✅ | Sequence 30 |
| 4 | Retrait **Accueil** / **Contact** du nav principal | ✅ | Accueil via logo → `/` · contact reste à `/contactus` |
| 5 | Recherche native | ✅ | Modal desktop · barre mobile offcanvas |
| 6 | Panier native `website_sale` | ✅ | `/shop/cart` |
| 7 | Overflow mobile 390 px | ✅ | `overflow-x: false` · clip thème CK actif |
| 8 | Branding recette | ✅ | Site + société renommés **C-Kreyol** |

---

## 3. Menu website (Phase 1 livré · 2026-06-13)

| Sequence | Menu | URL | Type |
|----------|------|-----|------|
| 10 | Boutique | `/shop` | Lien simple |
| 20 | **Découvrir** | `#` | **Mega-menu natif CE** |
| 30 | Professionnels | `/professionnels` | Lien direct |

**Mega Découvrir** : colonne « Acheter par univers » — **Épicerie créole** uniquement (`/shop/category/epicerie-creole-1`).

**Réserve** : Packs & découvertes non intégré (catégorie sans produit publié · URL 404).

**Producteurs** : non ajouté — pas de page CMS producteur (M1 Phase 7).

---

## 4. Implémentation

| Couche | Action |
|--------|--------|
| `website.menu` | CRUD menus top-level · séquences V1.2 |
| `website` / `res.company` | Nom **C-Kreyol** (instance recette) |
| `dorevia_ck_theme` | **Non modifié** — styles header sticky + clip mobile existants |
| Parcours natifs | `/shop` · `/shop/cart` · `/website/search` · `/professionnels` |

> **Note instance** : restart Odoo recommandé après modification menus pour rafraîchir le cache frontend.

---

## 5. Recette rapide (2026-06-13)

| Plateforme | Menus visibles | Recherche | Panier | Overflow |
|------------|----------------|-----------|--------|----------|
| **Desktop** 1280×800 | Boutique · Catégories · Professionnels | ✅ | ✅ | ✅ non |
| **Mobile** 390×844 | idem (burger) | ✅ | ✅ | ✅ non |

Éléments natifs Odoo conservés dans le drawer mobile : téléphone société · lien connexion — hors périmètre header marchand V1.2.

---

## 7. Corrections BO post-QA (2026-06-13)

| Réserve QA | Correction BO |
|------------|---------------|
| Téléphone fictif offcanvas | `website.header_text_element` → **inactive** |
| Mention « Généré par Odoo » | `website.brand_promotion` inactive + vue `website.custom_hide_brand_promotion_ck_phase1` |
| Copyright | `website.footer_copyright_company_name` → **© C-Kreyol** |

---

## 8. Réserves / suite

| Point | Statut instance | Cible Phase 1 (H1 acté) |
|-------|-----------------|-------------------------|
| Logo graphique C-Kreyol | ✅ texte **C-Kreyol** | Conservé |
| Libellé **Catégories** → `/shop` | ⚠️ Actuel | **Remplacer par Découvrir** + mega-menu natif CE |
| Entrée **Producteurs** | ❌ Absente nav | **Ajouter** — lien simple ou dropdown léger · pas mega V1 |
| Mega-menu **Découvrir** | ❌ Non configuré | 3 colonnes BO · liens réels uniquement (M4) |
| **Professionnels** | ✅ `/professionnels` | **Conserver lien direct** — pas sous-menu |
| Footer liens Contact / légal | ⚠️ Partiel | Phase 1 footer BO 4 col |

Référence : [`note_reference_header_mega_menu_decouverte_ck_v1.md`](./note_reference_header_mega_menu_decouverte_ck_v1.md) §2bis · [`RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md`](./RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md) §0quater · **passe QA pré-Phase 1 OK Codex 2026-06-13**

### Prochaine séquence home (GO MOA §5)

```text
1. ☐ Hero
2. ☐ Réassurance
3. ☐ Blocs produits / collections
4. ☐ Entrée Professionnels (bandeau home)
5. ☐ Footer si nécessaire
```

---

*Composition CMS Header V1.2 — ticket CK 01 · GO reprise Odoo · 2026-06-13.*
