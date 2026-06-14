# Recette QA visuelle post-correction — `dorevia_ck_theme` (ticket 01)

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Module** | `dorevia_ck_theme` |
| **Instance** | `dorevia_ck_marketone_01` |
| **URL** | `http://localhost:18079` |
| **Référence instance** | [`REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md`](./REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md) |
| **Recette fonctionnelle** | [`recette_qa_dorevia_ck_theme_01_fonctionnelle.md`](./recette_qa_dorevia_ck_theme_01_fonctionnelle.md) |
| **Date** | 2026-06-12 |
| **Statut QA** | **OK recette visuelle post-correction — socle ticket 01** |

---

## 1. Verdict

```text
OK RECETTE VISUELLE POST-CORRECTION
```

La correction CSS ciblée du ticket 01 est validée visuellement : le bundle CSS est désormais interprété par le navigateur et les styles Odoo/CK sont effectivement appliqués.

Cette validation ne couvre pas la composition CMS complète, la revue pixel-perfect, l'arbitrage typo production, ni les extensions hors ticket 01.

---

## 2. Cause initiale rappelée

Le verdict fonctionnel initial avait été rétrogradé car le bundle CSS frontend était syntaxiquement invalide côté navigateur.

Cause racine :

```text
@import url(...) Google Fonts dans website.scss
→ URL tronquée dans le bundle Odoo
→ CSS quasi entier ignoré par le navigateur
→ rendu HTML brut : Times, liens bleus, logo énorme
```

Correction appliquée :

- suppression de l'`@import` Google Fonts dans `website.scss` ;
- fallbacks système dans `primary_variables.scss` ;
- upgrade module ;
- purge assets frontend ;
- redémarrage instance.

---

## 3. Contrôles navigateur — desktop

| Page | Contrôle | Statut | Note |
|------|----------|--------|------|
| `/` | HTTP / rendu page | OK | Page `Home`, CMS non composée mais stylée. |
| `/` | `body.ck-theme` | OK | Classe présente. |
| `/` | Fond CK | OK | `rgb(255, 251, 247)`. |
| `/` | Typographie fallback | OK | `system-ui, -apple-system, "Segoe UI", sans-serif`. |
| `/` | Rendu HTML brut absent | OK | Liens non bleus natifs, CSS appliqué. |
| `/shop` | `#wrap.ck-shop-page` | OK | Classe effective sur la boutique. |
| `/shop` | CSS actif | OK | Fond CK, police fallback, liens stylés. |
| `/shop` | Template Odoo natif | OK | Grille `website_sale`, pas catalogue parallèle. |
| Fiche produit | `#wrap.ck-product-page` | OK | Héritage produit effectif. |
| Fiche produit | `ck-product-chips` | OK | Élément présent. |
| Fiche produit | Buy box native | OK | `#product_details` / `o_wsale_product_page`. |

---

## 4. Bundle CSS

| Contrôle | Statut | Preuve |
|----------|--------|--------|
| Bundle frontend chargé | OK | `/web/assets/1/22027f9/web.assets_frontend.min.css` |
| CSS interprété par navigateur | OK | 5625 règles CSS lues via `document.styleSheets`. |
| `ck-theme` appliqué réellement | OK | Fond et police calculés sur `body`. |
| Plus de rendu navigateur brut | OK | Plus de `Times` / liens bleus natifs. |

---

## 5. Responsive smoke

Viewport testé : `390x844`.

| Page | Statut | Note |
|------|--------|------|
| `/` | OK | CSS actif, `ck-theme`, viewport présent. |
| `/shop` | OK | CSS actif, `ck-shop-page`, filtre mobile visible. |
| Fiche produit | OK | CSS actif, `ck-product-page`, buy box native. |

Aucune rupture majeure détectée dans ce smoke test. La revue pixel-perfect reste hors périmètre du socle ticket 01.

---

## 6. Non-régression standard Odoo

| Contrôle | Statut | Note |
|----------|--------|------|
| Panier natif `/shop/cart` | OK | Page panier Odoo, panier vide normal. |
| Checkout natif | OK | Redirection panier/boutique normale si panier vide. |
| Pas de panier custom | OK | Aucun signal `dorevia_ck` custom hors thème. |
| Pas de checkout custom | OK | Aucun tunnel spécifique CK. |
| Pas de B2B implicite | OK | Pas de texte/portail B2B public. |
| Pas de pricelist UI publique | OK | Aucun sélecteur public observé. |
| Pas de modèle custom CK | OK | Aucun modèle `dorevia_ck.*` en base. |

---

## 7. Réserves maintenues

Ces points restent hors validation visuelle post-correction :

- composition CMS accueil complète ;
- raccord Dynamic Products pour les produits vedettes ;
- page Pro CMS + `website_crm` ;
- arbitrage typographie production Fraunces / DM Sans ;
- revue pixel-perfect maquette V1.1.1 ;
- origines, collections, filtre prix ;
- B2B custom, portail, pricelists ;
- panier / checkout custom ;
- toute extension hors ticket 01.

---

## 8. Conclusion QA

```text
OK RECETTE VISUELLE POST-CORRECTION — SOCLE TICKET 01 VALIDÉ
→ TICKET 01 CLÔTURÉ CÔTÉ SOCLE — PHASE CMS MOA
```

Phase suivante : composition éditoriale Website Builder uniquement — pas d’extension · pas de surcouche · pas de B2B custom.

La correction CSS lève le blocage visuel constaté. Le socle thème `dorevia_ck_theme` est visuellement exploitable pour la suite MOA : composition CMS accueil, produits vedettes natifs et page Pro CMS.

Le GO général CK reste non donné. Toute extension hors ticket 01 reste interdite sans ticket séparé et validation MOA/QA.

