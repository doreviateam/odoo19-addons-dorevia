# Protocole QA — Axe C · Sécurisation avant correction BO

| Champ | Valeur |
|---|---|
| Projet | `dorevia_ck_marketone` |
| Axe | C — Mise à niveau BO / données produit |
| Phase | 1 · Sécurisation pré-correction |
| Date | 2026-06-24 |
| Rédacteur | QA expert Odoo |
| Base | `dorevia_ck_marketone_01` |
| Commit référence | `2feac7e` (main HEAD) |
| Statut | Pré-correction — état figé avant intervention MOA |

---

## Objet

Ce document précède toute intervention BO. Il répond à la question : **chaque action de la checklist MOA est-elle testable et observable dans Odoo 19 CE ?**

Pour chaque point, l'état actuel est documenté, la faisabilité BO est évaluée, et les blockers ou points d'arbitrage sont isolés. La re-recette post-correction (`RECETTE_QA_CALE_PRODUIT_V1_POST_CORRECTION.md`) ne sera produite qu'après les corrections MOA.

---

## État de référence — snapshot base 2026-06-24

### Produits publiés

| id | Produit | is_published | Origine | ck_is_featured | ck_show_ref | UOM net | UOM réf |
|---|---|---|---|---|---|---|---|
| — | Chapeau Panama | ✅ | ❌ absent | ✅ | ✅ coché | *(vide)* | *(vide)* |
| — | Confiture de goyave | ✅ | ⚠️ Guadeloupe (sans fr_FR) | ✅ | ✅ coché | Unité(s) ❌ | Pack de 6 ❌ |
| — | Jus Mont-Pelé | ✅ | ❌ absent | ❌ | ✅ coché | Jours ❌ | Jours ❌ |
| — | Manio Crackers | ✅ | ❌ absent | ✅ | ✅ coché | Unité(s) ❌ | Pack de 6 ❌ |
| — | Pâte de manioc | ✅ | ❌ absent | ❌ | ✅ coché | Pack de 6 ❌ | Pack de 6 ❌ |
| — | Savon vétiver | ✅ | ❌ absent | ✅ | ❌ décoché | Unité(s) | Pack de 6 |
| 20 | Galettes de manioc | ✅ | ❌ absent | ❌ | ❌ décoché | Unité(s) | *(vide)* |

**Produit test** : "Recette QA CK — Produit test" → dépublié (`is_published=false`), existe en DB, en_US uniquement.

### Catégories publiques

| id | fr_FR | en_US | parent | nb_produits |
|---|---|---|---|---|
| 1 | Épicerie | Épicerie | — | 6 |
| **24** | **NULL** | **Coups de cœur** | **—** | **4** |
| 2 | Soin & Bien-être | Soin & Bien-être | — | 0 |
| 3 | Artisanat | Artisanat | — | 1 |
| 123 | Boissons | Boissons | — | 1 |
| 183 | NULL | Biscuits | 1 | 1 |
| 184 | NULL | Confitures | 1 | 1 |
| 185 | NULL | Épices | 1 | 0 |
| 186 | NULL | Jus de fruits | 123 | 1 |
| 187 | NULL | Alcools | 123 | 0 |
| 188 | NULL | Liqueurs | 123 | 0 |
| 189 | NULL | Savons | 2 | 1 |
| 190 | NULL | Huiles | 2 | 0 |
| 388 | NULL | Farines & manioc | 1 | 2 |

### Menu de navigation (website_menu, website_id=1)

| id | label fr_FR | label en_US | URL |
|---|---|---|---|
| 34 | NULL | Tous nos produits | /shop |
| 35 | NULL | Épicerie | /shop/category/epicerie-1 |
| 337 | Boissons | Boissons | /shop/category/boissons-123 |
| **590** | **NULL** | **Maison & Bien-être** | **/shop/category/soin-bien-etre-2** |
| 591 | NULL | Artisanat | /shop/category/artisanat-3 |
| **336** | **Coups de cœur** | **Coups de cœur** | **/shop/category/coups-de-cœur-24** |
| 592 | NULL | Nos producteurs | /nos-producteurs |
| 593 | NULL | Espace pro | # |

### Attributs produit

| Attribut en_US | fr_FR | Valeur en_US | fr_FR | Produit porteur |
|---|---|---|---|---|
| Origine | **NULL** | Guadeloupe | **NULL** | Confiture de goyave |
| Saveur | Saveur | Manio Crackers Salé / Sucré | idem | Manio Crackers |

### UOM disponibles (actives)

| id | fr_FR | en_US | Utilisabilité |
|---|---|---|---|
| 15 | **NULL** | g | ✅ utilisable (libellé universel) |
| 16 | kg | kg | ✅ |
| 12 | ml | ml | ✅ |
| 13 | **NULL** | L | ✅ utilisable (libellé universel) |
| 1 | Unité(s) | Units | Hors contexte prix réf. |
| 5 | Jours | Days | Hors contexte prix réf. |
| 2 | Pack de 6 | Pack of 6 | Hors contexte prix réf. |

### Champ ck_is_featured

```
ir_model_fields.field_description = {"en_US": "En vedette"}
→ présent sur product.product (id=10831) ET product.template (id=10832)
→ fr_FR : absent
→ ir_translation : table inexistante en Odoo 19 (architecture JSON)
```

---

## Analyse de testabilité — checklist BO par action

---

### Action 1 — Retirer la catégorie "Coups de cœur" des fiches produits concernées

**Produits concernés** : Chapeau Panama, Confiture de goyave, Manio Crackers, Savon vétiver (4 fiches).

**Faisabilité BO** : ✅ **Oui** — via fiche produit > onglet E-commerce > Catégories, supprimer "Coups de cœur" de chaque fiche.

**Observable après correction** : ✅ via SQL :
```sql
SELECT pt.name->>'fr_FR', string_agg(pc.name->>'en_US', ' · ')
FROM product_template pt
JOIN product_public_category_product_template_rel rel ON rel.product_template_id = pt.id
JOIN product_public_category pc ON pc.id = rel.product_public_category_id
WHERE pt.is_published = true GROUP BY pt.name->>'fr_FR';
-- Résultat attendu : aucune ligne ne doit contenir "Coups de cœur"
```

**Attendu post-correction** : 0 produit publié avec catégorie "Coups de cœur" assignée.

---

### Action 2 — Retirer "Coups de cœur" du header (navigation)

**Entrée concernée** : `website_menu` id=336, label "Coups de cœur", URL `/shop/category/coups-de-cœur-24`.

**Faisabilité BO** : ✅ **Oui** — Site web > Menu > supprimer l'entrée id=336.

**Observable après correction** : ✅ via SQL :
```sql
SELECT id, name->>'fr_FR', url FROM website_menu
WHERE url ILIKE '%coups%';
-- Résultat attendu : 0 lignes
```
Et HTTP : `GET /shop/category/coups-de-cœur-24` → doit retourner 404.

**Attendu post-correction** : entrée absente du menu, URL renvoie 404.

---

### Action 3 — Retirer "Coups de cœur" du filmstrip / exposition publique catalogue

**Mécanisme** : le filmstrip est rendu côté client (JavaScript). Il n'est pas vérifiable via requête HTTP statique.

**Hypothèse de rendu** : le thème génère le filmstrip depuis la liste des catégories publiques. Si "Coups de cœur" reste en base avec 0 produit, son apparition dépend du comportement de filtrage du thème (filtre les vides ou non).

**Faisabilité BO** : ✅ les actions 1 et 2 sont les prérequis. La disparition du filmstrip doit être vérifiée manuellement.

**Observable après correction** : ⚠️ **recette visuelle obligatoire** — vérifier sur desktop 1280px que le pill "Coups de cœur" n'apparaît plus dans le filmstrip.

**Point d'attention** : si la catégorie existe en base avec 0 produit mais que le thème affiche toutes les catégories sans filtre, le pill restera visible même après les actions 1 et 2. → Voir Action 4.

---

### Action 4 — Masquer, archiver ou désactiver la catégorie "Coups de cœur"

**Constat critique** : `product_public_category` **n'a pas de colonne `active`** en Odoo 19 CE. L'archivage natif Odoo n'est pas disponible pour les catégories publiques.

**Options disponibles** :

| Option | Faisabilité | Risque | Recommandation |
|---|---|---|---|
| Vider la catégorie (0 produit) + supprimer l'entrée menu | ✅ BO | Catégorie reste en DB — pill filmstrip potentiellement visible selon thème | Étape 1 suffisante si thème filtre les vides |
| Supprimer la catégorie | ✅ BO (irréversible) | Irréversible ; vérifier avant qu'aucune page CMS ni composant ne la référence | À n'exécuter que si l'Architecte confirme qu'aucune référence externe n'existe |
| Laisser en DB vide sans entrée menu | ✅ BO | Catégorie orpheline en DB, inoffensive si thème filtre les vides | Acceptable si filmstrip ne l'affiche pas sans produits |

**Faisabilité BO** : ⚠️ **partielle** — pas d'archivage natif ; supprimer ou laisser vide.

**Point d'arbitrage MOA-1** : faut-il supprimer définitivement la catégorie "Coups de cœur" (id=24) ou la laisser en DB sans exposition ? La suppression est irréversible — décision MOA requise avant action.

**Observable après correction** : si suppression → SQL retourne 0 ligne pour `id=24`. Si vidage → SQL retourne `nb_produits=0` pour id=24.

---

### Action 5 — Traductions fr_FR manquantes

#### 5a. Attribut "Origine" et valeur "Guadeloupe"

**État actuel** : `{"en_US": "Origine"}` et `{"en_US": "Guadeloupe"}` — aucune entrée `fr_FR`.

**Faisabilité BO** : ✅ **Oui** — Configuration > Attributs & variantes > éditer l'attribut "Origine" et la valeur "Guadeloupe" pour ajouter la traduction française.

**Observable** :
```sql
SELECT pa.name->>'fr_FR', pav.name->>'fr_FR'
FROM product_attribute pa
JOIN product_attribute_value pav ON pav.attribute_id = pa.id
WHERE pa.name->>'en_US' = 'Origine';
-- Attendu : "Origine" en fr_FR + valeur avec fr_FR renseigné
```

#### 5b. Galettes de manioc — nom fr_FR

**État actuel** : `name = {"en_US": "Galettes de manioc"}` — pas de `fr_FR`.

**Faisabilité BO** : ✅ **Oui** — fiche produit > Nom > ajouter la traduction française.

**Observable** :
```sql
SELECT name->>'fr_FR' FROM product_template WHERE name->>'en_US' ILIKE '%galettes%';
-- Attendu : "Galettes de manioc" (ou traduction équivalente)
```

#### 5c. Sous-catégories — traductions fr_FR

**Catégories sans fr_FR** : Biscuits, Confitures, Épices, Farines & manioc, Huiles, Jus de fruits, Alcools, Liqueurs, Savons.

**Faisabilité BO** : ✅ **Oui** — Configuration > Catégories > éditer chaque catégorie pour ajouter le nom français.

**Note** : la traduction de "Coups de cœur" (id=24) doit être traitée conjointement à l'Action 4 (suppression ou maintien).

**Observable** :
```sql
SELECT name->>'fr_FR' AS cat_fr, name->>'en_US' AS cat_en
FROM product_public_category ORDER BY cat_fr;
-- Attendu : 0 ligne avec cat_fr = NULL pour les catégories actives exposées
```

---

### Action 6 — Renseigner l'origine sur tous les produits commerciaux publiés

**État actuel** : 6/7 produits sans attribut Origine, 1/7 avec Guadeloupe (sans fr_FR).

**Données requises de la MOA** : les origines réelles de chaque produit. Elles ne peuvent pas être déduites par le QA.

| Produit | Origine connue | À confirmer MOA |
|---|---|---|
| Confiture de goyave | Guadeloupe (attribut existant) | ✅ confirmé |
| Chapeau Panama | Non renseigné | ⬜ |
| Jus Mont-Pelé | Non renseigné | ⬜ |
| Manio Crackers | Non renseigné | ⬜ |
| Pâte de manioc | Non renseigné | ⬜ |
| Savon vétiver | Non renseigné | ⬜ |
| Galettes de manioc | Non renseigné | ⬜ |

**Faisabilité BO** : ✅ **Oui** — une fois les valeurs d'attribut créées (ex. Martinique, Réunion, etc.) via Configuration > Attributs, les affecter sur chaque fiche produit > onglet Attributs.

**Prérequis** : Action 5a complétée (fr_FR sur l'attribut) + MOA fournit les données d'origine par produit.

**Observable** :
```sql
SELECT pt.name->>'fr_FR', pav.name->>'fr_FR' AS origine_fr
FROM product_template pt
JOIN product_template_attribute_value ptav ON ptav.product_tmpl_id = pt.id
JOIN product_attribute_value pav ON pav.id = ptav.product_attribute_value_id
JOIN product_attribute pa ON pa.id = pav.attribute_id
WHERE pt.is_published = true AND pa.name->>'en_US' = 'Origine';
-- Attendu : 7 lignes, toutes avec origine_fr non NULL
```

---

### Action 7 — Corriger les UOM de quantité nette et de prix de référence

**UOM disponibles et utilisables** :

| UOM | id | fr_FR | Cas d'usage |
|---|---|---|---|
| g | 15 | NULL (libellé "g" universel) | Masse < 1 kg (confiture, crackers, savon, galettes) |
| kg | 16 | kg | Référence de prix pour la masse |
| ml | 12 | ml | Volume < 1 L |
| L | 13 | NULL (libellé "L" universel) | Référence de prix pour le volume |

**Corrections requises par produit** :

| Produit | Action `ck_net_quantity_uom_id` | Action `ck_reference_price_uom_id` | `ck_show_reference_price` |
|---|---|---|---|
| Confiture de goyave (320) | → **g** (id=15) | → **kg** (id=16) | Garder coché |
| Manio Crackers (100) | → **g** (id=15) | → **kg** (id=16) | Garder coché |
| Galettes de manioc (130) | → **g** (id=15) | → **kg** (id=16) | → **Cocher** (pertinent) |
| Savon vétiver (125) | → **g** (id=15) | → **kg** (id=16) | → **Cocher si MOA valide** |
| Jus Mont-Pelé (1) | → **⬜ MOA** (cL ? mL ?) | → **⬜ MOA** (L ?) | MOA valide la pertinence |
| Pâte de manioc (1) | → **⬜ MOA** (kg ? unité ?) | → **⬜ MOA** | MOA valide ou désactive |
| Chapeau Panama (0) | → **désactiver** (non pertinent) | → **désactiver** | → **Décocher** |

**Point d'arbitrage MOA-2** : pour Jus Mont-Pelé et Pâte de manioc, les unités réelles et la pertinence d'un prix de référence doivent être décidées par la MOA avant saisie BO.

**Faisabilité BO** : ✅ **Oui** — fiche produit > onglet E-commerce > champs "Quantité nette" et "Prix de référence".

**Observable** :
```sql
SELECT pt.name->>'fr_FR', uom_n.name->>'en_US' AS uom_net, uom_r.name->>'en_US' AS uom_ref,
       pt.ck_show_reference_price
FROM product_template pt
LEFT JOIN uom_uom uom_n ON uom_n.id = pt.ck_net_quantity_uom_id
LEFT JOIN uom_uom uom_r ON uom_r.id = pt.ck_reference_price_uom_id
WHERE pt.is_published = true ORDER BY pt.name->>'fr_FR';
-- Attendu : g/kg ou ml/L sur les produits alimentaires ; aucun "Jours" ni "Pack de 6"
```

---

### Action 8 — Désactiver le prix de référence quand non applicable

**Produits concernés** : Chapeau Panama (`ck_net_quantity=0`, pas d'UOM pertinente), éventuellement Jus Mont-Pelé et Pâte de manioc selon décision MOA-2.

**Faisabilité BO** : ✅ **Oui** — décocher "Afficher le prix au kg / litre" sur la fiche produit.

**Observable** :
```sql
SELECT pt.name->>'fr_FR', pt.ck_show_reference_price
FROM product_template WHERE is_published=true ORDER BY pt.name->>'fr_FR';
-- Attendu : false pour Chapeau Panama (et autres selon MOA)
```

---

### Action 9 — Corriger "Maison & Bien-être" → "Soin & Bien-être"

**État actuel** : `website_menu` id=590, `name = {"en_US": "Maison & Bien-être"}`, pas de fr_FR.

**Faisabilité BO** : ✅ **Oui** — Site web > Menu > éditer l'entrée id=590 > modifier le libellé.

**Précision** : en Odoo 19, l'édition du menu dans le backoffice (pas le Website builder) modifie directement le JSONB `name`. Il faut saisir le libellé en français dans le champ langue active.

**Observable** :
```sql
SELECT name->>'fr_FR' AS label_fr, name->>'en_US' AS label_en, url
FROM website_menu WHERE id = 590;
-- Attendu : "Soin & Bien-être" (fr_FR ou en_US selon le champ modifié)
```
Et visuellement sur le header front (recette manuelle).

---

### Action 10 — Renommage "En vedette" → "Afficher à l'accueil"

#### Analyse technique

**Champ concerné** : `ck_is_featured` sur `product.template` et `product.product`.

**Label actuel** : `ir_model_fields.field_description = {"en_US": "En vedette"}` — pas de `fr_FR`.

**Mécanisme de traduction en Odoo 19** : `ir_translation` n'existe plus. Les libellés de champs sont stockés dans `ir_model_fields.field_description` comme JSONB. Pour afficher un libellé différent en français, il faut ajouter `"fr_FR": "Afficher à l'accueil"` dans ce JSON.

#### Options

| Option | Faisabilité | Pérennité | Recommandation |
|---|---|---|---|
| **Via BO** : Settings > Technical > Database Structure > Fields > éditer `field_description` (mode développeur) | ✅ Techniquement possible | ❌ **Écrasé à chaque `odoo -u dorevia_ck_theme`** | Déconseillé en production |
| **Via Dev** : modifier `string="Afficher à l'accueil"` dans la définition Python du champ + upgrade | ✅ Propre | ✅ Pérenne | **Recommandé** |

#### Verdict sur cette action

**Cette action nécessite un ticket Dev léger.** Elle n'est pas faisable proprement en BO seul sans risque de régression à l'upgrade. Il s'agit d'une modification d'une ligne dans le fichier Python du module (`dorevia_ck_theme` ou `dorevia_ck_marketone_content`).

**Point d'arbitrage MOA-3** : confirmer que le libellé cible est bien "Afficher à l'accueil" et non une autre formulation (ex. "Mettre en avant sur l'accueil", "Sélection Home"). La logique fonctionnelle du champ (`ck_is_featured`) **ne change pas** — seul le libellé affiché dans le BO change.

**Impact Dev estimé** : modification d'une ligne dans le modèle Python + `odoo -u` → 30 min Dev maximum.

**Observable après Dev** : libellé affiché "Afficher à l'accueil" sur la fiche produit BO, section E-commerce.

---

## Résumé de faisabilité

| # | Action | Faisable BO | Bloquant | Arbitrage requis |
|---|---|---|---|---|
| 1 | Retirer "Coups de cœur" des 4 fiches | ✅ | Non | — |
| 2 | Supprimer l'entrée menu "Coups de cœur" | ✅ | Non | — |
| 3 | Retirer du filmstrip | ⚠️ Indirect | Non | Recette visuelle obligatoire |
| 4 | Archiver / désactiver la catégorie | ❌ Impossible (pas d'active) | Non | **MOA-1** : supprimer ou laisser vide ? |
| 5a | fr_FR attribut "Origine" + valeur "Guadeloupe" | ✅ | Non | — |
| 5b | fr_FR "Galettes de manioc" | ✅ | Non | — |
| 5c | fr_FR sous-catégories | ✅ | Non | — |
| 6 | Renseigner origine sur 6 produits | ✅ (données MOA requises) | Non | **MOA** : fournir les origines par produit |
| 7 | Corriger UOM | ✅ (partiel) | Non | **MOA-2** : Jus Mont-Pelé et Pâte de manioc |
| 8 | Désactiver prix réf. non pertinent | ✅ | Non | — |
| 9 | Corriger label menu "Maison & Bien-être" | ✅ | Non | — |
| 10 | Renommer "En vedette" → "Afficher à l'accueil" | ❌ BO fragile | Non | **MOA-3** : confirmer libellé → ticket Dev |

---

## Points d'arbitrage MOA — récapitulatif

### MOA-1 — Sort de la catégorie "Coups de cœur" (id=24)

La catégorie ne peut pas être archivée nativement en Odoo 19 CE. Après retrait des 4 produits et suppression de l'entrée menu :

- **Option A** : laisser la catégorie vide en DB (inoffensif si le thème filtre les catégories sans produits dans le filmstrip)
- **Option B** : supprimer la catégorie définitivement (irréversible — s'assurer qu'aucune page CMS ou snippet ne la référence)

Décision requise avant le début des corrections BO.

### MOA-2 — UOM et pertinence du prix de référence pour Jus Mont-Pelé et Pâte de manioc

- **Jus Mont-Pelé** : quelle est la contenance réelle (25 cL, 33 cL, 75 cL…) ? Le prix de référence est-il pertinent (prix au L) ?
- **Pâte de manioc** : quelle est la quantité nette réelle ? Le prix de référence est-il pertinent ?

Si non pertinent pour l'un ou l'autre : décocher `ck_show_reference_price`.

### MOA-3 — Libellé cible du champ `ck_is_featured`

Confirmer le libellé exact souhaité en BO. Le brief indique "Afficher à l'accueil". Ce libellé fera l'objet d'un ticket Dev léger (modification du fichier Python du module + upgrade). Aucun impact fonctionnel sur la logique Home.

---

## Données à fournir par la MOA avant corrections

| Donnée | Destinataire | Urgence |
|---|---|---|
| Origine (pays/territoire) de chaque produit commercial publié | QA / Dev BO | Bloquant pour Action 6 |
| Décision : supprimer ou vider la catégorie "Coups de cœur" | QA | Bloquant pour Action 4 |
| Contenance et pertinence prix réf. pour Jus Mont-Pelé | QA | Bloquant pour Action 7 (ce produit) |
| Quantité nette et pertinence prix réf. pour Pâte de manioc | QA | Bloquant pour Action 7 (ce produit) |
| Libellé BO exact pour `ck_is_featured` | Dev | Ticket Dev |

---

## Prochaine étape

Une fois les arbitrages MOA rendus et les corrections BO effectuées, le QA produira :

**`RECETTE_QA_CALE_PRODUIT_V1_POST_CORRECTION.md`**

Ce document contiendra :
- vérification de chaque correction par requête SQL et/ou HTTP
- recette visuelle desktop 1280 / tablette 800 / mobile 390
- verdict **GO / NO GO** pour passage à l'Axe B — Carte de navigation

---

> *Document de sécurisation pré-correction. Ne déclenche aucune action. Les corrections BO sont sous responsabilité MOA.*
