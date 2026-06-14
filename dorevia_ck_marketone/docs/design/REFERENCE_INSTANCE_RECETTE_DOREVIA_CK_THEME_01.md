# Référence instance — recette fonctionnelle ticket 01 `dorevia_ck_theme`

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Ticket** | [`ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md`](./ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md) |
| **Recette squelette** | [`recette_qa_dorevia_ck_theme_01_squelette.md`](./recette_qa_dorevia_ck_theme_01_squelette.md) — **OK statique** |
| **Recette fonctionnelle** | [`recette_qa_dorevia_ck_theme_01_fonctionnelle.md`](./recette_qa_dorevia_ck_theme_01_fonctionnelle.md) — **OK install/QWeb · OK visuel post-correction** |
| **Recette visuelle** | [`recette_qa_dorevia_ck_theme_01_visuelle_post_correction.md`](./recette_qa_dorevia_ck_theme_01_visuelle_post_correction.md) — **OK socle ticket 01** |
| **Phase CMS MOA** | [`ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md`](./ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) — **Odoo en pause** · `/professionnels` + header conservés |
| **Phase maquette V1.2** | [`go_moa_maquette_01_2.md`](./maquette_01.2/go_moa_maquette_01_2.md) **GO OFFICIEL** · recette + arbitrage actés · [`TABLEAU_TRADUCTION_ODOO_V1_2.md`](./maquette_01.2/TABLEAU_TRADUCTION_ODOO_V1_2.md) |
| **Date** | 2026-06-13 |

---

## 1. État projet acté

```text
Note d’approche technique     : validée MOA
Ticket dorevia_ck_theme_01    : clôturé côté socle (2026-06-12)
Exécution encadrée ticket 01  : terminée — socle livré et validé QA
Verrou Odoo                   : levé ticket 01 uniquement — maintenu ailleurs
GO général CK                 : non donné
Extensions hors ticket 01     : interdites
Phase courante                : Maquette V1.2.x — matérialisation vision CK (pause Odoo)
Décision MOA                  : decision_moa_pause_odoo_iteration_maquette_v1_2_x.md
Cadrage maquette              : CADRAGE_MAQUETTE_CK_V1_2_X.md
Prochaine étape maquette      : GO Lot 1 — accueil · fiche produit · professionnels (go_moa_maquette_v1_2_x_lot1.md)
Prochaine étape Odoo          : ⏸ post-verdict maquette + arbitrage traduction
Page /professionnels          : ✅ COMPOSITION_PROFESSIONNELS_V1_2.md
Header marchand V1.2          : ✅ COMPOSITION_HEADER_V1_2.md
```

Référentiel technique :

```text
Odoo 19 CE · snippets first · pas de surcouche autonome
```

---

## 2. Instance Odoo de référence

| Paramètre | Valeur |
|-----------|--------|
| **Base / instance** | `dorevia_ck_marketone_01` |
| **URL locale** | http://localhost:18079 |
| **Conteneur** | `sandbox-odoo19-odoo-1` |
| **Login recette** | `admin` |
| **Mot de passe recette** | `admin` |
| **Thème website actif** | `dorevia_ck_theme` (`website.theme_id`) |

> **Attention** : identifiants valables uniquement pour l’environnement local / recette. Ne pas utiliser en production.

Accès multi-base : préciser `?db=dorevia_ck_marketone_01` ou sélectionner la base au login.

### Prérequis recette — thème actif

Odoo 19 exclut les assets SCSS des modules « theme » non sélectionnés sur le website. Pour la recette (et tout déploiement) :

```text
Website → Configuration → activer dorevia_ck_theme comme thème du site
```

Sans cette étape : xpath QWeb OK · SCSS non compilé dans `web.assets_frontend`.

---

## 3. Socle Odoo cible

Modules standards installés sur l’instance :

| Module | Rôle |
|--------|------|
| `website` | Site web / Website Builder |
| `website_sale` | Boutique `/shop` |
| `website_crm` | Formulaires CRM (page Pro future) |
| `dorevia_ck_theme` | Thème CK ticket 01 |

Objectif : environnement Odoo 19 CE propre, sans données démo métier CK, pour valider le squelette thème.

---

## 4. Livrable Dev — squelette module

Chemin : `odoo19-addons-dorevia/dorevia_ck_theme/`

| Composant | Fichiers |
|-----------|----------|
| Manifest | `__manifest__.py` — deps `website`, `website_sale`, `website_crm` |
| SCSS | `primary_variables.scss`, `bootstrap_overridden.scss`, `website.scss`, `website_sale.scss` |
| QWeb léger | `website_layout.xml`, `website_sale_templates.xml` |
| Snippets CK | `s_ck_hero`, `s_ck_category_links`, `s_ck_featured_products`, `s_ck_reassurance`, `s_ck_shop_intro`, `s_ck_pro_banner` |
| Groupe Builder | `CK Marketone` |

Hors périmètre respecté : pas de `models/`, `controllers/`, JS métier, B2B, catalogue parallèle.

---

## 5. QA statique — validée

Verdict : **OK squelette ticket 01** (document [`recette_qa_dorevia_ck_theme_01_squelette.md`](./recette_qa_dorevia_ck_theme_01_squelette.md)).

---

## 6. Recette fonctionnelle — checklist instance

| # | Point | Statut | Note |
|---|-------|--------|------|
| 1 | Installation `dorevia_ck_theme` | ✅ | `state=installed` |
| 2 | Installation `website` / `website_sale` / `website_crm` | ✅ | |
| 3 | Vues QWeb enregistrées (11 clés `dorevia_ck_theme.*`) | ✅ | |
| 4 | Compilation assets frontend | ✅ | Correction `@import` Google Fonts validée en navigateur — 5625 règles CSS lues |
| 5 | XPath `products_ck_theme` (`#wrap` → `ck-shop-page`) | ✅ | `/shop` |
| 6 | XPath `layout_ck_theme` (`body` → `ck-theme`) | ✅ | Correction `body_classname` · Odoo 19 |
| 7 | XPath `product_ck_theme` (`product_details`) | ✅ | Fiche produit test |
| 8 | Groupe `CK Marketone` Website Builder | ✅ | Registry |
| 9 | Snippets CK éditables | ✅ | 6 snippets — composition CMS MOA à faire |
| 10 | Rendu `/shop` | ✅ | HTTP 200 · template natif |
| 11 | Rendu fiche produit | ✅ | Produit test publié |
| 12 | Responsive mobile | ✅ | Smoke test (viewport · mobile UA) |
| 13 | Non-régression panier / checkout standard | ✅ | |
| 14 | Absence B2B implicite | ✅ | |
| 15 | Placeholder vedettes → Dynamic Products | ⚠️ | Zone `oe_structure` — composition CMS MOA |
| 16 | Typo Fraunces + DM Sans | ⚠️ | Fallbacks système ticket 01 · self-host = arbitrage prod |

### Correction ciblée `ck-theme` — verdict QA (2026-06-12)

```text
OK correction ciblée ck-theme
```

| Contrôle | Verdict |
|----------|---------|
| Approche `body_classname` + `priority="20"` | ✅ Conforme ticket 01 · Odoo 19 |
| Recette HTTP `/` · `/shop` · fiche produit | ✅ |

---

### Recette visuelle post-correction — verdict QA (2026-06-12)

```text
OK RECETTE VISUELLE POST-CORRECTION — SOCLE TICKET 01 VALIDÉ
```

| Contrôle | Verdict |
|----------|---------|
| Bundle CSS interprété par navigateur | ✅ 5625 règles CSS |
| `body.ck-theme` | ✅ `/` · `/shop` · fiche produit |
| Fond CK `#fffbf7` appliqué | ✅ |
| Typographie fallback système | ✅ |
| Rendu HTML brut / Times / liens bleus natifs | ✅ Absent |
| `/shop` avec `ck-shop-page` | ✅ |
| Fiche produit `ck-product-page` / `ck-product-chips` | ✅ |
| Responsive smoke mobile | ✅ |
| Panier / checkout natifs | ✅ |
| Pas de B2B/pricelist UI publique | ✅ |

---

## 7. Hors périmètre maintenu

```text
origines custom · collections custom · filtre prix avancé
portail B2B custom · configuration B2B complète
pricelists / devis / portail client
module métier CK · extension e-commerce
catalogue parallèle · panier/checkout custom
front autonome · injection HTML maquette
logique transactionnelle hors Odoo standard
```

Toute extension = constat limite Odoo + arbitrage MOA + ticket séparé.

---

## 8. Prochaine étape — phase maquette V1.2.x prioritaire

### Phase maquette V1.2 (en cours)

| Document | Rôle |
|----------|------|
| [`note_05.md`](../cadrage/note_05.md) | Doctrine MOA · pause home |
| [`decision_moa_pause_odoo_iteration_maquette_v1_2_x.md`](./maquette_01.2/decision_moa_pause_odoo_iteration_maquette_v1_2_x.md) | **Décision active** — pause Odoo · matérialisation vision |
| [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](./maquette_01.2/CADRAGE_MAQUETTE_CK_V1_2_X.md) | Cadrage pages · concepts · arbitrage |
| [`recette_qa_maquette_v1_2_x.md`](./maquette_01.2/recette_qa_maquette_v1_2_x.md) | Recette QA vision complète |
| [`go_moa_maquette_01_2.md`](./maquette_01.2/go_moa_maquette_01_2.md) | GO initial maquette V1.2 — historique utile |
| [`brief_01_2.md`](./maquette_01.2/brief_01_2.md) | Commande opérationnelle maquette |
| [`ticket_dev_maquette_01_2_open_design.md`](./maquette_01.2/ticket_dev_maquette_01_2_open_design.md) | Ticket Dev — périmètre exécution |
| [`recette_qa_maquette_01_2.md`](./maquette_01.2/recette_qa_maquette_01_2.md) | Grille QA post-livraison |

```text
1. ✅ Socle ticket 01 — clôturé
2. ✅ Ticket composition CMS CK 01 — validé MOA
3. ✅ Première composition home — preuve faisabilité Odoo
4. ✅ Note d’itération MOA — note_05 · pause home complète
5. ✅ GO OFFICIEL MOA — go_moa_maquette_01_2.md
6. ✅ Production maquette CK V1.2 — livrée Dev · LIVRAISON_V1_2.md
7. ✅ Recette maquette + arbitrage MOA — GO traduction Odoo
8. ⏸ Reprise composition home V1.2 · suspendue jusqu’au verdict maquette V1.2.x
9. ✅ Parallèle : /professionnels · menu Pro — COMPOSITION_PROFESSIONNELS_V1_2.md
10. ☐ Arbitrage typo Fraunces/DM Sans prod (hors CMS)
```

**Phase courante** : maquette V1.2.x — matérialisation vision CK avant toute reprise Odoo.

Extensions Dev : ticket séparé + arbitrage MOA uniquement.

---

*Référence opposable — instance recette ticket 01 `dorevia_ck_theme`.*
