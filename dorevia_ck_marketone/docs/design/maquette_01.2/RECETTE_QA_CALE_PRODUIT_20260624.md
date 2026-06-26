# Recette QA — Cale Produit C-Kréyòl

| Champ | Valeur |
|---|---|
| Projet | `dorevia_ck_marketone` |
| Lot | Cale produit — vérification pré-Dev |
| Date recette | 2026-06-24 |
| Rédacteur | QA expert Odoo |
| Base recettée | `dorevia_ck_marketone_01` |
| Sandbox | `http://localhost:18079` |
| Commit référence | `2feac7e` (main, HEAD stabilisé juin 2026) |
| Document audité | `audit-cale-produit-ckreyol.md` (fourni par l'Architecte) |
| Statut | Verdict rendu |

---

## Objet

Ce document constitue le rapport QA de vérification de l'audit `audit-cale-produit-ckreyol.md`.

L'objectif était de contrôler sur l'instance sandbox la justesse des 7 points de l'audit avant toute décision Dev ou arbitrage MOA. Chaque point a été vérifié par requête directe sur la base PostgreSQL et par interrogation HTTP du front Odoo.

La recette ne propose aucune refonte. Elle confirme, corrige ou complète les constats de l'audit, et produit la liste des corrections BO immédiates.

---

## Méthode

### Environnement utilisé

| Paramètre | Valeur |
|---|---|
| URL sandbox | `http://localhost:18079` |
| Base PostgreSQL | `dorevia_ck_marketone_01` |
| Conteneur Odoo | `sandbox-odoo19-odoo-1` |
| Conteneur DB | `sandbox-odoo19-db-1` |
| Authentification | `admin / admin` (JSON-RPC, uid=2 confirmé) |
| Thème actif | `dorevia_ck_theme` 19.0.1.56.0 ✅ |
| Module contenu | `dorevia_ck_marketone_content` 19.0.1.38.0 ✅ |

### Sources interrogées

- Requêtes SQL directes sur PostgreSQL via `docker exec sandbox-odoo19-db-1 psql`
- HTTP GET authentifié sur les routes `/odoo/shop`, `/odoo/shop/<slug>`, `/odoo/shop/category/<slug>`
- Extraction HTML via Python pour les contenus statiques (le filmstrip et certaines zones de navigation sont rendus côté client — non vérifiables via curl)

### Note sur les URLs Odoo 19

En Odoo 19, les URLs publiques ont migré vers le préfixe `/odoo/*` :
- `/shop` → `/odoo/shop` (HTTP 200 authentifié)
- Les anciennes URLs `/shop`, `/shop/category/...` retournent **200** en accès direct sur le serveur interne (tests Odoo, Docker exec) mais **404** en accès HTTP externe sans session
- Toutes les vérifications HTTP ont utilisé le préfixe `/odoo/`

---

## Résultats — Point par point

---

### Point 1 — Produit test "Recette QA CK — Produit test" publié et à dépublier

#### Ce que dit l'audit

> Le produit "Recette QA CK — Produit test" est publié (`is_published = true`). Il pollue le catalogue, risque d'achat accidentel, nuit à la crédibilité. Action : dépublier immédiatement.

#### Vérification

```sql
SELECT pt.name->>'fr_FR' AS produit_fr, pt.name->>'en_US' AS produit_en, pt.is_published
FROM product_template pt
WHERE pt.is_published = false
ORDER BY pt.name->>'fr_FR';
```

Résultat :

| produit_fr | produit_en | is_published |
|---|---|---|
| Manio Crackers salé | Manio Crackers salé | false |
| Manio Crackers sucré | Manio Crackers sucré | false |
| *(vide)* | Recette QA CK — Produit test | false |

#### Constat

Le produit "Recette QA CK — Produit test" **existe** dans la base mais est **déjà dépublié** (`is_published = false`). Il n'apparaît pas sur le front.

Points additionnels :
- Le produit n'a **aucune traduction française** (`name->>'fr_FR' = NULL`) — il n'aurait aucun nom affiché si republié en contexte FR.
- Il reste présent dans le catalogue BO et visible par les administrateurs.

#### Verdict

**Audit inexact sur l'état actuel.** La dépublication est déjà faite. L'action résiduelle est la **suppression complète** du produit en BO — pas une dépublication.

#### Anomalie supplémentaire identifiée

Deux autres templates dépubliés existent : "Manio Crackers salé" et "Manio Crackers sucré" comme templates indépendants, alors qu'un template "Manio Crackers" publié existe avec les variantes Saveur (Salé / Sucré). Probable doublon de saisie ou erreur de modélisation produit. À soumettre à l'Architecte avant décision de suppression.

---

### Point 2 — Produits sans origine visible

#### Ce que dit l'audit

> Confiture de goyave : origine "Guadeloupe" visible front via attribut de variante ✅.
> 5/7 autres produits : attribut origine non renseigné, promesse "origines identifiées" non tenue.

#### Vérification — Structure des attributs

```sql
SELECT pav.name->>'fr_FR' AS val_fr, pav.name->>'en_US' AS val_en,
       pa.name->>'fr_FR' AS attr_fr, pa.name->>'en_US' AS attr_en,
       COUNT(ptav.id) AS nb_usages
FROM product_attribute_value pav
JOIN product_attribute pa ON pa.id = pav.attribute_id
LEFT JOIN product_template_attribute_value ptav ON ptav.product_attribute_value_id = pav.id
GROUP BY pav.id, pav.name, pa.name
ORDER BY nb_usages DESC;
```

Résultat :

| val_fr | val_en | attr_fr | attr_en | nb_usages |
|---|---|---|---|---|
| Manio Crackers Salé | Manio Crackers Salé | Saveur | Saveur | 1 |
| Manio Crackers Sucré | Manio Crackers Sucré | Saveur | Saveur | 1 |
| *(vide)* | Guadeloupe | *(vide)* | Origine | 1 |

#### Vérification — Produit portant l'attribut Origine

```sql
SELECT pt.name->>'fr_FR' AS produit_fr, pt.is_published,
       pav.name->>'en_US' AS valeur, pa.name->>'en_US' AS attribut
FROM product_template_attribute_value ptav
JOIN product_attribute_value pav ON pav.id = ptav.product_attribute_value_id
JOIN product_attribute pa ON pa.id = pav.attribute_id
JOIN product_template pt ON pt.id = ptav.product_tmpl_id
WHERE pa.name->>'en_US' = 'Origine';
```

Résultat :

| produit_fr | is_published | valeur | attribut |
|---|---|---|---|
| Confiture de goyave | true | Guadeloupe | Origine |

#### Vérification — Champ natif `country_of_origin`

```sql
SELECT pt.name->>'fr_FR' AS produit, rc.name->>'fr_FR' AS pays_origine
FROM product_template pt
LEFT JOIN res_country rc ON rc.id = pt.country_of_origin
WHERE pt.is_published = true;
```

Résultat : `country_of_origin = NULL` pour les 7 produits publiés.

#### Vérification — Contenu HTML du produit Confiture de goyave

Requête HTTP GET sur `/odoo/shop/confiture-de-goyave` : aucune occurrence de "Guadeloupe", "Origine", "origine", "provenance", "Antilles" dans le HTML retourné.

#### Constat

1. L'attribut "Origine" / valeur "Guadeloupe" **existe** et est rattaché à Confiture de goyave — la structure est là.
2. Cependant : **ni l'attribut "Origine" ni la valeur "Guadeloupe" n'ont de traduction `fr_FR`**. Seul `en_US` est renseigné. En contexte de langue française, le thème peut rendre la valeur vide ou afficher l'anglais selon son comportement de fallback.
3. Le HTML front ne contient aucune mention de "Guadeloupe" — **la valeur ne s'affiche pas** dans l'état actuel.
4. Le champ natif Odoo `country_of_origin` n'est utilisé pour aucun produit.
5. Les 6 autres produits publiés n'ont **aucun attribut Origine** du tout.

#### Verdict

**Audit confirmé dans la direction, inexact dans le détail.** La situation est plus dégradée que décrite :
- La "référence" Confiture de goyave a la structure mais pas la traduction → l'origine ne s'affiche pas en FR.
- 6/7 produits n'ont aucune structure origine du tout.
- La promesse "origines identifiées" n'est tenue visuellement sur **aucun** produit publié en l'état.

---

### Point 3 — Prix de référence manquants ou non visibles

#### Ce que dit l'audit

> 3 produits sans prix de référence visible : Galettes de manioc, Chapeau Panama, Pâte de manioc.

#### Vérification

```sql
SELECT pt.name->>'fr_FR' AS produit,
       pt.ck_net_quantity,
       uom_net.name->>'fr_FR' AS uom_quantite_nette,
       pt.ck_show_reference_price,
       uom_ref.name->>'fr_FR' AS uom_prix_reference
FROM product_template pt
LEFT JOIN uom_uom uom_net ON uom_net.id = pt.ck_net_quantity_uom_id
LEFT JOIN uom_uom uom_ref ON uom_ref.id = pt.ck_reference_price_uom_id
WHERE pt.is_published = true
ORDER BY pt.name->>'fr_FR';
```

Résultat :

| Produit | `ck_net_quantity` | UOM quantité | `ck_show_reference_price` | UOM prix réf. |
|---|---|---|---|---|
| Chapeau Panama | 0 | *(vide)* | **true** | *(vide)* |
| Confiture de goyave | 320 | **Unité(s)** | **true** | **Pack de 6** |
| Jus Mont-Pelé | 1 | **Jours** | **true** | **Jours** |
| Manio Crackers | 100 | **Unité(s)** | **true** | **Pack de 6** |
| Pâte de manioc | 1 | **Pack de 6** | **true** | **Pack de 6** |
| Savon vétiver | 125 | Unité(s) | false | Pack de 6 |
| Galettes de manioc | 130 | Unité(s) | false | *(vide)* |

#### Constat

Le problème dépasse les 3 produits identifiés par l'audit. La case `ck_show_reference_price` est cochée sur **5 produits**, mais les **unités de mesure sont incorrectes sur la quasi-totalité** :

- **Confiture de goyave** : `ck_net_quantity = 320` avec UOM "Unité(s)" au lieu de "g" → calcul `/kg` sans sens. UOM prix réf. : "Pack de 6" au lieu de "kg".
- **Manio Crackers** : même problème — "Unité(s)" et "Pack de 6" au lieu de "g" et "kg".
- **Jus Mont-Pelé** : UOM = **"Jours"** (unité de durée) pour une quantité nette et un prix de référence de boisson → erreur manifeste de saisie.
- **Pâte de manioc** : UOM quantité et prix = "Pack de 6" → incohérent pour un prix au kg.
- **Chapeau Panama** : `ck_net_quantity = 0`, UOM vide → aucune donnée exploitable malgré la case cochée.
- **Savon vétiver** et **Galettes de manioc** : `ck_show_reference_price = false` → cohérent, rien n'est affiché.

Ce n'est donc pas "3 produits sans prix de référence" mais "5 produits avec prix de référence coché mais UOM erronées". L'affichage front produit des valeurs incohérentes ou sans sens pour ces 5 produits.

#### Verdict

**Audit incomplet.** La correction requise est plus large : révision des champs `ck_net_quantity_uom_id` et `ck_reference_price_uom_id` pour les 5 produits concernés. Action BO.

---

### Point 4 — Fiche Confiture de goyave comme référence de card complète

#### Ce que dit l'audit

> La Confiture de goyave est le **modèle cible** : publication ✅, ruban "Nouveau !" ✅, catégories ✅, quantité nette 320 g ✅, prix au kg ✅, phrase courte ✅, origine Guadeloupe ✅, En vedette ✅.

#### Vérification

```sql
SELECT pt.name->>'fr_FR' AS produit,
       pt.is_published,
       pt.ck_is_featured,
       pt.ck_net_quantity,
       uom_net.name->>'fr_FR' AS uom_net,
       pt.ck_show_reference_price,
       uom_ref.name->>'fr_FR' AS uom_ref,
       pt.description_sale->>'fr_FR' AS phrase_courte,
       string_agg(pc.name->>'en_US', ' · ') AS categories
FROM product_template pt
LEFT JOIN uom_uom uom_net ON uom_net.id = pt.ck_net_quantity_uom_id
LEFT JOIN uom_uom uom_ref ON uom_ref.id = pt.ck_reference_price_uom_id
LEFT JOIN product_public_category_product_template_rel rel ON rel.product_template_id = pt.id
LEFT JOIN product_public_category pc ON pc.id = rel.product_public_category_id
WHERE pt.name->>'fr_FR' ILIKE '%goyave%'
GROUP BY pt.id, uom_net.name, uom_ref.name;
```

Résultat consolidé :

| Critère | Valeur constatée | Attendu audit | OK ? |
|---|---|---|---|
| `is_published` | true | true | ✅ |
| `ck_is_featured` | true | true | ✅ |
| Catégories | Épicerie · Confitures · Coups de cœur | Épicerie/Confitures · Épicerie · Coups de cœur | ✅ (équivalent) |
| `ck_net_quantity` | 320 | 320 g | ⚠️ valeur OK mais UOM = "Unité(s)" ≠ "g" |
| `ck_show_reference_price` | true | true | ⚠️ coché mais UOM réf. = "Pack de 6" ≠ "kg" |
| `description_sale` (phrase courte) | **NULL / vide** | "Confiture artisanale…" | ❌ |
| Attribut Origine "Guadeloupe" | Rattaché mais **sans fr_FR** | Visible front | ❌ non visible front |
| Ruban "Nouveau !" | Non vérifiable (table `product_ribbon` sans colonne `html`) | Présent | ⚠️ non confirmé |

#### Verdict

**Audit inexact sur la complétude de la référence.** La Confiture de goyave est la fiche la plus avancée du catalogue mais elle n'est pas une card complète au sens CK :
- La phrase courte est absente.
- Les UOM du prix de référence sont incorrectes.
- L'origine ne s'affiche pas en FR.

Elle reste la meilleure base pour établir le modèle cible, mais ne peut pas être présentée comme référence valide sans corrections BO préalables.

---

### Point 5 — "Coups de cœur" : catégorie ou curation

#### Ce que dit l'audit

> "Coups de cœur" est utilisé comme catégorie au même niveau qu'Épicerie, Boissons, etc. Il contient des produits de familles hétérogènes. La tension entre catégorie de navigation et tag de curation est réelle.

#### Vérification

```sql
SELECT pc.name->>'fr_FR' AS cat_fr, pc.name->>'en_US' AS cat_en, pc.id,
       COUNT(rel.product_template_id) AS nb_produits
FROM product_public_category pc
LEFT JOIN product_public_category_product_template_rel rel ON rel.product_public_category_id = pc.id
GROUP BY pc.id, pc.name
ORDER BY nb_produits DESC;
```

```sql
SELECT wm.name, wm.url FROM website_menu wm WHERE wm.website_id = 1 ORDER BY wm.sequence;
```

Résultats :

| Catégorie | fr_FR | en_US | Nb produits |
|---|---|---|---|
| Épicerie | Épicerie | Épicerie | 6 |
| Coups de cœur | **NULL** | Coups de cœur | 4 |
| Farines & manioc | **NULL** | Farines & manioc | 2 |
| Artisanat | Artisanat | Artisanat | 1 |
| Boissons | Boissons | Boissons | 1 |
| … | … | … | … |
| Soin & Bien-être | Soin & Bien-être | Soin & Bien-être | 0 |

Produits dans "Coups de cœur" : Confiture de goyave, Manio Crackers, Savon vétiver, Chapeau Panama.

Navigation menu : entrée "Coups de cœur" présente avec URL `/shop/category/coups-de-cœur-24` (HTTP 200 ✅).

#### Constat

- "Coups de cœur" est bien une **catégorie browseable** avec page dédiée accessible — ce n'est pas un tag.
- Elle est au même niveau hiérarchique qu'Épicerie, Boissons, Artisanat (pas de `parent_id`).
- Elle regroupe des produits de familles hétérogènes → ambiguïté catalogue/curation confirmée.
- **Point additionnel** : dans `product_public_category`, la traduction `fr_FR` est **NULL** pour "Coups de cœur". La traduction française n'existe que dans `website_menu`. Selon la source de données utilisée par le thème (catégorie vs menu), l'affichage peut être vide ou incohérent.

#### Verdict

**Audit confirmé.** L'ambiguïté est réelle et documentée. Un point additionnel non documenté : l'absence de `fr_FR` dans la table catégorie elle-même.

---

### Point 6 — Incohérence "Maison & Bien-être" / "Soin & Bien-être"

#### Ce que dit l'audit

> Le libellé varie selon la zone : "Maison & Bien-être" dans le header, "Soin & Bien-être" dans le BO et le filmstrip. L'utilisateur ne sait pas si c'est la même porte.

#### Vérification

```sql
SELECT wm.name->>'en_US' AS menu_label, wm.url
FROM website_menu wm WHERE wm.website_id = 1
ORDER BY wm.sequence;
```

```sql
SELECT pc.id, pc.name->>'fr_FR' AS cat_fr, pc.name->>'en_US' AS cat_en, pc.parent_id
FROM product_public_category pc ORDER BY pc.parent_id NULLS FIRST;
```

Résultats :

| Source | Libellé | fr_FR présent ? |
|---|---|---|
| `website_menu` (nav header) | "Maison & Bien-être" | Non (en_US uniquement) |
| `product_public_category` id=2 | "Soin & Bien-être" | Oui |
| URL résolue | `/shop/category/soin-bien-etre-2` | — |
| Filmstrip (JS) | Non vérifiable via curl | — |

L'entrée de menu "Maison & Bien-être" pointe sur la catégorie "Soin & Bien-être". Le label du menu et le nom de la catégorie sont différents.

Observation complémentaire : la catégorie "Soin & Bien-être" a **0 produits publiés assignés directement**. Savon vétiver est sous "Savons" (sous-catégorie de Soin), non sous "Soin & Bien-être" directement.

#### Verdict

**Audit confirmé** sur l'incohérence header vs BO. La mention filmstrip ne peut pas être confirmée par cette méthode (rendu JS) — à vérifier lors d'une recette manuelle visuelle. Correction BO : éditer l'entrée de menu pour aligner le libellé sur "Soin & Bien-être".

---

### Point 7 — Actions immédiates : BO/MOA, pas de Dev

#### Ce que dit l'audit

> Les corrections identifiées relèvent d'une correction BO/MOA, sans nouveau développement front.

#### Vérification

Chaque correction a été associée à un champ ou une action en base :

| Correction | Champ / action | Mécanisme |
|---|---|---|
| Supprimer produit test | Suppression enregistrement | BO |
| Ajouter attribut Origine sur 6 produits | `product_template_attribute_line` + `product_template_attribute_value` | BO (fiche produit → onglet Attributs) |
| Ajouter traduction `fr_FR` à "Origine" et "Guadeloupe" | `product_attribute.name`, `product_attribute_value.name` | BO (Configuration → Attributs) |
| Corriger UOM quantité nette | `product_template.ck_net_quantity_uom_id` | BO (fiche produit) |
| Corriger UOM prix de référence | `product_template.ck_reference_price_uom_id` | BO (fiche produit) |
| Renseigner phrase courte | `product_template.description_sale` | BO (fiche produit) |
| Corriger label menu | `website_menu.name` | BO (Site web → Menu) |
| Clarifier "Coups de cœur" | Décision structurelle | MOA |

Aucune modification de template QWeb, SCSS, ni de code Python n'est requise pour ces corrections.

#### Verdict

**Audit confirmé.** Toutes les corrections sont des actions BO. Aucun ticket Dev à ouvrir à ce stade.

---

## Écarts supplémentaires non documentés dans l'audit

Ces points ont été identifiés lors de la recette et n'apparaissent pas dans `audit-cale-produit-ckreyol.md`.

### E1 — Galettes de manioc sans traduction française

**Constat** : `product_template.name->>'fr_FR' = NULL`. Seul `en_US = "Galettes de manioc"` est renseigné. En interface française, le nom s'affiche vide sur les cards et dans les listes.

**Sévérité** : Majeur — produit publié sans nom visible.
**Action** : Ajouter la traduction `fr_FR` en BO.

### E2 — UOM incorrectes sur la quasi-totalité des produits

**Constat** : cf. tableau §3. Ce n'est pas un problème de 3 produits isolés mais un problème de configuration systémique des champs `ck_net_quantity_uom_id` et `ck_reference_price_uom_id`. Des UOM de type "Jours", "Pack de 6", "Unité(s)" sont utilisées là où des unités de masse ou volume sont attendues.

**Hypothèse** : les UOM ont été sélectionnées depuis la liste Odoo par défaut sans correspondance métier (g, kg, mL, cL, L absents ou non sélectionnés).

**Sévérité** : Majeur — affiche des prix de référence sans sens sur le front pour les 5 produits concernés.
**Action** : Révision BO de tous les champs UOM. Peut nécessiter de vérifier que les unités "g", "kg", "cL", "L" sont bien présentes dans `uom_uom` avec les catégories correctes.

### E3 — Attribut "Origine" et valeur "Guadeloupe" sans traduction française

**Constat** : `product_attribute.name->>'fr_FR' = NULL` et `product_attribute_value.name->>'fr_FR' = NULL`. L'attribut et sa valeur n'existent qu'en `en_US`. Résultat front : la valeur ne s'affiche pas en contexte FR.

**Sévérité** : Majeur — l'unique produit portant l'attribut Origine (Confiture de goyave) n'affiche pas son origine en français.
**Action** : Ajouter `fr_FR` sur l'attribut "Origine" et la valeur "Guadeloupe" en BO (Configuration → Attributs & variantes).

### E4 — Toutes les sous-catégories sans traduction française

**Constat** : les sous-catégories Confitures, Biscuits, Farines & manioc, Savons, Huiles, Jus de fruits, Alcools, Liqueurs, Épices n'ont **aucune traduction `fr_FR`** dans `product_public_category`. Seul `en_US` est renseigné. Les catégories racines Artisanat, Épicerie, Boissons ont leur `fr_FR`, mais pas leurs enfants.

**Sévérité** : Important — les noms de sous-catégories s'affichent potentiellement en anglais ou vides sur le front et dans les filtres.
**Action** : Compléter les traductions `fr_FR` pour toutes les sous-catégories en BO.

### E5 — "Coups de cœur" sans `fr_FR` dans `product_public_category`

**Constat** : dans la table `product_public_category`, `name->>'fr_FR' = NULL` pour "Coups de cœur". La traduction `fr_FR` est présente dans `website_menu` mais pas dans la catégorie elle-même. Selon la source de données utilisée par le thème (requête sur `product_public_category` vs rendu du menu), l'affichage peut être incohérent.

**Sévérité** : Important.
**Action** : Ajouter `fr_FR = "Coups de cœur"` sur la catégorie id=24 en BO.

### E6 — Trois templates Manio Crackers dans la base

**Constat** :
- Template publié : "Manio Crackers" avec 2 variantes Saveur (Salé, Sucré)
- Template dépublié : "Manio Crackers salé" (template indépendant)
- Template dépublié : "Manio Crackers sucré" (template indépendant)

Les deux templates dépubliés semblent être des doublons antérieurs à la modélisation avec variantes. Ils ne sont pas publiés mais occupent le catalogue BO.

**Sévérité** : À arbitrer — pas de risque front immédiat mais doublon de données.
**Action** : Soumettre à l'Architecte pour décision (suppression ou archivage).

---

## Verdict global

**Audit partiellement inexact — à corriger avant toute décision Dev.**

| Dimension | Résultat |
|---|---|
| **Direction générale de l'analyse** | Correcte — les sujets identifiés sont réels |
| **Exactitude factuelle** | Partiellement inexacte — produit test déjà dépublié, Confiture de goyave non complète, UOM problème plus large |
| **Gravité réelle vs perçue** | Plus grave que décrit — 0/7 produits affichent leur origine en FR, 5/7 ont des UOM prix réf. incohérentes |
| **Nature des corrections** | Confirmée : BO/MOA exclusivement, aucun Dev requis |
| **Passage Axe B (Carte de navigation)** | **Bloqué** — les conditions listées dans §6 de l'audit ne sont pas remplies |

---

## Corrections BO immédiates (liste ordonnée)

| # | Priorité | Action | Champ / zone BO | Produits concernés |
|---|---|---|---|---|
| 1 | 🔴 Critique | Supprimer le produit test | Suppression fiche produit | "Recette QA CK — Produit test" |
| 2 | 🔴 Critique | Ajouter traduction `fr_FR` à l'attribut "Origine" | Configuration → Attributs | Attribut id Origine |
| 3 | 🔴 Critique | Ajouter traduction `fr_FR` à la valeur "Guadeloupe" | Configuration → Attributs → Valeurs | Valeur Guadeloupe |
| 4 | 🔴 Critique | Renseigner l'attribut Origine sur les 6 produits sans origine | Fiche produit → onglet Attributs | Chapeau Panama, Manio Crackers, Savon vétiver, Jus Mont-Pelé, Pâte de manioc, Galettes de manioc |
| 5 | 🔴 Critique | Corriger les UOM quantité nette | `ck_net_quantity_uom_id` | Tous produits avec `ck_show_reference_price = true` |
| 6 | 🔴 Critique | Corriger les UOM prix de référence | `ck_reference_price_uom_id` | Tous produits avec `ck_show_reference_price = true` |
| 7 | 🟡 Important | Ajouter traduction `fr_FR` sur "Galettes de manioc" | Nom produit | Galettes de manioc |
| 8 | 🟡 Important | Renseigner `description_sale` (phrase courte) | Fiche produit | Tous produits publiés |
| 9 | 🟡 Important | Corriger label menu "Maison & Bien-être" → "Soin & Bien-être" | Site web → Menu | Entrée navigation N2 |
| 10 | 🟡 Important | Ajouter `fr_FR` sur toutes les sous-catégories | Configuration → Catégories | Confitures, Biscuits, Farines & manioc, Savons, Huiles, Jus de fruits, Alcools, Liqueurs, Épices |
| 11 | 🟡 Important | Ajouter `fr_FR = "Coups de cœur"` sur la catégorie id=24 | Configuration → Catégories | Coups de cœur |

---

## Points nécessitant arbitrage MOA (aucun Dev sans décision)

### MOA-1 — Statut de "Coups de cœur"

**Question** : "Coups de cœur" doit-il rester une catégorie de navigation (avec page dédiée), devenir une étiquette de curation éditoriale, ou être remplacé par le champ `ck_is_featured` (déjà en place) ?

**Impact** : si supprimé comme catégorie, les 4 produits concernés perdent cette classification ; la page `/shop/category/coups-de-cœur-24` disparaît. Si conservé, aligner le rôle avec la promesse éditoriale.

### MOA-2 — Doublons Manio Crackers

**Question** : les 2 templates dépubliés "Manio Crackers salé" et "Manio Crackers sucré" doivent-ils être supprimés ? Ont-ils été utilisés dans un contexte précédent (commandes, données historiques) ?

**Impact** : suppression irréversible si des lignes de commande y sont attachées.

### MOA-3 — Mécanisme d'origine à terme

**Question** : faut-il conserver l'origine comme attribut de variante (actuel) ou migrer vers le champ natif `country_of_origin` (ou un champ custom produit) ?

**Impact** : si migration, les filtres sidebar "Origines & préférences" devront être reconfigurés. Travail Dev à budgéter séparément. Ne pas déclencher sans décision MOA.

---

## Conditions de passage à l'Axe B (inchangées, état vérifié)

```
☐ Produit test supprimé (dépublié ✅, suppression ☐)
☐ 7/7 produits commerciaux ont l'attribut Origine renseigné ET traduit en fr_FR
☐ 7/7 produits ont les UOM quantité nette et prix de référence correctes
☐ Rôle de "Coups de cœur" clarifié (MOA-1)
☐ Catégories alignées fr_FR (sous-catégories + "Coups de cœur" id=24)
☐ Label menu "Maison & Bien-être" aligné sur "Soin & Bien-être"
```

Aucune de ces conditions n'est remplie à ce jour.

---

## Annexe — Inventaire produits publiés au 2026-06-24

| # | Produit | `is_published` | Origine (attribut) | `ck_is_featured` | `ck_show_ref_price` | UOM net | UOM réf. | `fr_FR` nom |
|---|---|---|---|---|---|---|---|---|
| 1 | Chapeau Panama | ✅ | ❌ absent | ✅ | ✅ coché | ❌ vide | ❌ vide | ✅ |
| 2 | Confiture de goyave | ✅ | ⚠️ "Guadeloupe" sans fr_FR | ✅ | ✅ coché | ❌ Unité(s) | ❌ Pack de 6 | ✅ |
| 3 | Jus Mont-Pelé | ✅ | ❌ absent | ❌ | ✅ coché | ❌ Jours | ❌ Jours | ✅ |
| 4 | Manio Crackers | ✅ | ❌ absent | ✅ | ✅ coché | ❌ Unité(s) | ❌ Pack de 6 | ✅ |
| 5 | Pâte de manioc | ✅ | ❌ absent | ❌ | ✅ coché | ❌ Pack de 6 | ❌ Pack de 6 | ✅ |
| 6 | Savon vétiver | ✅ | ❌ absent | ✅ | ❌ non coché | Unité(s) | Pack de 6 | ✅ |
| 7 | Galettes de manioc | ✅ | ❌ absent | ❌ | ❌ non coché | Unité(s) | ❌ vide | ❌ **NULL** |

**Cards complètes (tous critères remplis)** : 0/7.

---

> *Recette réalisée par requêtes SQL directes sur `dorevia_ck_marketone_01` et vérifications HTTP authentifiées sur `http://localhost:18079`. Filmstrip et zones à rendu JS non vérifiables via cette méthode — compléter par recette visuelle manuelle sur les viewports de référence (1280 / 800 / 390 px).*
