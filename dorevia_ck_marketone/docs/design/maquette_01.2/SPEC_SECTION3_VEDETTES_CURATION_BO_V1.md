# Spécification — Section 3 « Nos coups de cœur » · vedettes curatées en back-office

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` — Home V1.2, Section 3 |
| **Objet** | **Spec MOA opposable** · sélection **curatée en BO** + rendu maquette custom CK |
| **Statut** | ✅ **Livré (cœur fonctionnel)** · dette résiduelle §8 |
| **Code** | `dorevia_ck_marketone_content` ≥ **`19.0.1.18.4`** |
| **Source de vérité opérationnelle** | [`NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md`](./NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md) |
| **Instance recette** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Doctrine** | BO Odoo = source de vérité ; nombre variable ; max 8 cartes ; rendu SSR custom CK ; `/shop` natif inchangé |

---

## Règle opposable

**« Nos coups de cœur » = curation BO, nombre variable, jusqu'à 8 cartes.**

La section n'est pas une sélection éditoriale figée et ne doit pas compléter artificiellement la grille avec des produits hors catégorie. En mode normal, elle reflète strictement la catégorie e-commerce **« Coups de cœur »**.

Le fallback automatique vers les 5 premiers produits publiés est uniquement un filet de sécurité lorsque la catégorie **« Coups de cœur »** est vide.

## 1. Matrice livraison (spec vs code `19.0.1.18.4`)

| Capacité | Spec | Code |
|----------|------|------|
| Catégorie « Coups de cœur » (xmlid) | §3 | ✅ `ck_public_category_coups_de_coeur.xml` |
| Sélection par catégorie | §5 | ✅ `get_curated_featured_variants()` |
| Ordre `website_sequence` | §5 | ✅ |
| Expansion variantes Manio | §4 | ✅ |
| Amorçage set MOA | migrations | ✅ `19.0.1.18.0` |
| Fusion doublons catégorie | — | ✅ `19.0.1.18.2` |
| Refresh home · write **produit** | §7 | ✅ `product_template.py` |
| Refresh home · write **catégorie** | §7 | ✅ `product_public_category.py` (`18.4`) |
| Remplacement section sans doublon | — | ✅ `_remove_all_featured_sections` (`18.2`) |
| Badges `website_ribbon_id` | §9.4 | ✅ `18.3` · ruban `ribbon_coups_de_coeur` |
| Badge position haut droite | maquette | ✅ SCSS `badge-float` |
| Repli auto si catégorie vide | §9 | ✅ `get_ready_featured_variants()` |
| Rendu live QWeb | §9.5 | ❌ arch « cuite » |
| Vue BO liste réordonnable | §8 | ❌ |
| N paramétrable | §9.2 | ❌ 8 curaté / 5 repli |
| Masquer si 0 vedette (sans repli) | §9.3 | ❌ repli actif |
| Ordre vedettes dédié (hors `/shop`) | §9.1 | ❌ |

---

## 2. Contexte

**Historique** : PR #73 livrait le rendu maquette avec sélection **automatique** (5 premiers produits publiés). La MOA avait reporté la curation BO (`DECISION_MOA_SECTION3_PR73_CURATION_REPORTEE_V1.md`, 2026-06-15).

**État actuel** : curation par catégorie **livrée** (`18.0+`). Le gestionnaire pilote la home via « Coups de cœur ». Les badges sont pilotés par le **ruban produit** standard Odoo. Le nombre de cartes affichées dépend du contenu réel de la catégorie.

---

## 3. Décision retenue — sélection

**Catégorie e-commerce dédiée « Coups de cœur »** (xmlid stable, pas le libellé).

| Action gestionnaire | Champ / écran BO |
|---------------------|------------------|
| Mettre en vedette | `public_categ_ids` → « Coups de cœur » |
| Ordonner | `website_sequence` sur la fiche produit |
| Retirer des vedettes | Retirer la catégorie (fiche produit **ou** liste produits sur la fiche catégorie) |

---

## 4. Décision retenue — badges

**Ruban e-commerce** (`website_ribbon_id` → `product.ribbon`).

| Élément | Détail |
|---------|--------|
| Affichage | Haut **droite** de la carte (`badge-float`) |
| Absence de ruban | Pas de badge |
| Mapping styles | Libellé « nouveau » → `badge-new` · « coup/cœur/vente » → `badge-heart` · autre → couleurs BO |
| Ruban CK | `ribbon_coups_de_coeur` en données |

---

## 5. Logique de sélection

1. Candidats = templates publiés dans la catégorie xmlid « Coups de cœur ».
2. Tri `website_sequence asc, id asc`.
3. Multi-variantes → 1 carte par variante publiée avec image.
4. Plafond **8** cartes (mode curaté) · **1 carte minimum** pour afficher la section.
5. Si catégorie vide → repli technique **5** premiers publiés avec image (PR #73).

**Interdit en mode curaté** : forcer 5 cartes, ou compléter avec Galettes / Savon / tout autre produit si ces produits ne sont pas rattachés à **« Coups de cœur »**.

**Exemple conforme** :

| Donnée BO | Résultat home |
|-----------|---------------|
| Confiture de goyave dans « Coups de cœur » | 1 carte |
| Manio Crackers dans « Coups de cœur » | 2 cartes : salé + sucré |
| Galettes de manioc hors « Coups de cœur » | 0 carte |
| Savon vétiver hors « Coups de cœur » | 0 carte |
| **Total** | **3 cartes** |

---

## 6. Rendu carte (inchangé PR #73)

En-tête fixe · grille responsive · carte `product-card` : média · badge · chips · titre · prix · « Voir ».

Données 100 % Odoo. Rendu custom CK (pas `oe_product_cart`).

| Élément carte | Source Odoo |
|---------------|-------------|
| Image | Image produit ou image variante |
| Nom | Nom produit ou nom variante |
| Prix | Prix de vente site TTC |
| Origine | Attribut ou donnée produit configurée |
| Famille | Catégorie ou attribut produit |
| Badge haut droite | Ruban e-commerce `website_ribbon_id` |
| Bouton « Voir » | Lien fiche produit / variante |

---

## 7. Architecture — HTML « cuit » + hooks de refresh

La section est injectée dans `view.arch_db` de `/` par `bootstrap_home_featured_products()`.

**Refresh automatique** (sans upgrade module) quand :

- un produit vedette est modifié (`product_template.write`) ;
- la liste produits de la catégorie « Coups de cœur » est modifiée (`product_public_category.write`).

**Non livré** : rendu live QWeb à chaque visite (recommandation initiale §9.5) — la dette « arch cuite » subsiste, atténuée par les hooks.

**Prix et images** : figés dans le HTML au moment du bootstrap — se mettent à jour au prochain déclencheur ci-dessus.

---

## 8. Dette résiduelle (à arbitrer MOA)

| # | Sujet | Recommandation spec | État |
|---|-------|---------------------|------|
| 9.1 | Ordre vedettes vs `/shop` | `website_sequence` puis ordre dédié si conflit | Même champ |
| 9.2 | N paramétrable | Config, défaut 5 | 8 / 5 figés |
| 9.3 | Catégorie vide | Masquer section | Repli auto actif |
| 9.5 | Rendu live QWeb | Préféré | Non fait |
| — | Vue BO curation dédiée | Liste réordonnable | Non faite |
| — | Chips origine/famille | 100 % attributs BO | Heuristiques démo |

---

## 9. Fichiers livrés

| Fichier | Rôle |
|---------|------|
| `data/ck_public_category_coups_de_coeur.xml` | Catégorie xmlid |
| `data/ck_product_ribbon_coups_de_coeur.xml` | Ruban « Coup de cœur » |
| `home_featured.py` | Sélection · cartes · bootstrap |
| `models/product_template.py` | Refresh write produit |
| `models/product_public_category.py` | Refresh write catégorie |
| `migrations/19.0.1.18.*` | Amorçage · correctifs · badges · refresh catégorie |
| `tests/test_ck_home_section3_curation.py` | Couverture curation + refresh |

---

## 10. Tests

```bash
docker exec sandbox-odoo19-odoo-1 bash -c \
  'odoo -d dorevia_ck_marketone_01 --http-port=8079 --no-http \
   -u dorevia_ck_theme,dorevia_ck_marketone_content \
   --test-tags dorevia_ck_marketone_home_section3_curation,dorevia_ck_marketone_home_section3,dorevia_ck_marketone_catalog_manioc \
   --stop-after-init'
```

**Couverture clé** : sélection catégorie · ordre · variantes Manio · retrait produit (fiche produit + fiche catégorie) · badges ruban · pas de doublon section.

---

## 11. Critères de recette MOA

| # | Règle à vérifier |
|---|------------------|
| R1 | Produit publié, vendable, imagé, ajouté à « Coups de cœur » → apparaît après reconstruction. |
| R2 | Produit retiré de « Coups de cœur » → disparaît après reconstruction. |
| R3 | Manio Crackers dans « Coups de cœur » → 2 cartes distinctes salé / sucré. |
| R4 | Galettes de manioc hors « Coups de cœur » → absente, même si Manio y figure. |
| R5 | Ordre des cartes = `website_sequence` croissant. |
| R6 | Ruban Odoo renseigné → badge ; ruban vide → aucun badge. |
| R7 | 3 cartes éligibles → 3 cartes affichées, pas 5 forcées. |
| R8 | Plus de 8 cartes éligibles → seules les 8 premières sont affichées. |

Contrôles visuels complémentaires : prix / images / liens = BO après refresh ; mobile 390 ; desktop 1280 ; `/shop`, Hero et trust-bar inchangés.

---

## 12. Hors périmètre

Header · SEO · Lot 6 polish · Section 4 · Dynamic Products natif · refonte visuelle carte (validée #73).

---

*Spécification Section 3 curation BO — révision 2026-06-16 · alignée `19.0.1.18.4`.*
