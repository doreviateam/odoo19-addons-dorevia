# Proposition Dev — Lot recadrage BO produit

| Champ | Valeur |
|-------|--------|
| **Référence MOA** | [`DECISION_MOA_RECADRAGE_BO.md`](./DECISION_MOA_RECADRAGE_BO.md) |
| **Module** | `dorevia_ckreyol_marketone` |
| **Version cible** | `19.0.16.0.0` (lot BO uniquement) |
| **Statut** | **Exécuté** — livré `19.0.16.0.0` · réception MOA [`RECEPTION_MOA_LOT_RECADRAGE_BO.md`](./RECEPTION_MOA_LOT_RECADRAGE_BO.md) |
| **Périmètre** | Back-office `product.template` · **aucun front** |

---

## 1. Restructuration de la fiche produit

### 1.1 Principe

- **Un seul fichier de vues BO produit** : `views/product_template_marketone_bo_views.xml`.
- Héritage de **`website_sale.product_template_form_view`** (pas seulement `product.product_template_form_view`) pour rester aligné sur l’eCommerce Odoo.
- **Suppression** du bloc actuel collé à `image_1920` (`views/product_template_shop_tile_views.xml`).
- **Retrait** de l’extension collections éparpillée dans `views/marketone_shop_collection_views.xml` (déplacée dans le fichier unifié).
- **Aucune modification** de la zone image principale (`image_1920`) : elle reste le master produit standard Odoo.

### 1.2 Onglets proposés (notebook)

Visibles lorsque `sale_ok` est coché (produit vendable), comme les champs eCommerce natifs.

| Onglet | Nom technique (`name`) | Contenu | Public cible |
|--------|------------------------|---------|--------------|
| **Publication site** | `marketone_bo_publication` | Champs eCommerce Odoo regroupés | Éditeur site / vente |
| **Catalogue CK** | `marketone_bo_catalogue` | Merchandising CK + renvoi origines | Éditeur catalogue |
| **Qualité image / contenu** | `marketone_bo_media_quality` | Dérivé média + statut + note MOA | Éditeur contenu / MOA |
| **Technique** | `marketone_bo_technical` | Traces batch / pipeline | `base.group_no_one` uniquement |

### 1.3 Maquette XML (cible)

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Masquer les champs eCommerce à leur emplacement d'origine (évite doublon visuel) -->
    <record id="product_template_form_view_marketone_bo_hide_ecommerce_dup" model="ir.ui.view">
        <field name="name">product.template.form.marketone.bo.hide.ecommerce.dup</field>
        <field name="model">product.template</field>
        <field name="inherit_id" ref="website_sale.product_template_form_view"/>
        <field name="priority">20</field>
        <field name="arch" type="xml">
            <!-- À caler sur les xpath réels Odoo 19 au moment de l'implémentation -->
            <field name="website_published" position="attributes">
                <attribute name="invisible">1</attribute>
            </field>
            <field name="public_categ_ids" position="attributes">
                <attribute name="invisible">1</attribute>
            </field>
            <!-- website_sequence, description eCommerce : idem si présents dans la vue standard -->
        </field>
    </record>

    <!-- Notebook CK — 4 onglets -->
    <record id="product_template_form_view_marketone_bo" model="ir.ui.view">
        <field name="name">product.template.form.marketone.bo</field>
        <field name="model">product.template</field>
        <field name="inherit_id" ref="website_sale.product_template_form_view"/>
        <field name="priority">25</field>
        <field name="arch" type="xml">
            <xpath expr="//notebook" position="inside">
                <page string="Publication site"
                      name="marketone_bo_publication"
                      invisible="not sale_ok">
                    <group>
                        <group string="Visibilité boutique">
                            <field name="website_published"/>
                            <!-- is_published si exposé par website_sale sur ce modèle -->
                        </group>
                        <group string="Classement catalogue">
                            <field name="public_categ_ids"
                                   widget="many2many_tags"
                                   placeholder="Catégories eCommerce…"/>
                            <field name="website_sequence"/>
                        </group>
                    </group>
                    <group string="Description boutique" colspan="2">
                        <field name="website_description"
                               placeholder="Description affichée sur le site…"/>
                    </group>
                </page>

                <page string="Catalogue CK"
                      name="marketone_bo_catalogue"
                      invisible="not sale_ok">
                    <group>
                        <field name="marketone_collection_ids"
                               widget="many2many_tags"
                               string="Collections commerciales"
                               placeholder="Rattachement merchandising CK…"/>
                    </group>
                    <div class="alert alert-info mb-0" role="alert">
                        Les <strong>origines</strong> sont gérées via l’attribut
                        « Origines » (onglet <em>Attributs &amp; variantes</em>).
                        Les profils éditoriaux associés se configurent dans
                        <em>Site web → Configuration → Origines (porte shop)</em>.
                    </div>
                </page>

                <page string="Qualité image / contenu"
                      name="marketone_bo_media_quality"
                      invisible="not sale_ok">
                    <group>
                        <group string="Vignette catalogue normalisée">
                            <field name="image_shop_tile"
                                   widget="image"
                                   class="oe_avatar"
                                   options="{'zoom': true}"/>
                            <field name="shop_tile_status"/>
                        </group>
                        <group string="Gouvernance MOA">
                            <field name="shop_tile_moa_note"
                                   placeholder="Note qualité visuelle…"/>
                        </group>
                    </group>
                    <div class="text-muted">
                        Si aucune vignette normalisée n’est validée pour l’affichage
                        catalogue, le site utilise l’<strong>image produit principale</strong>
                        (<code>image_1920</code>).
                    </div>
                </page>

                <page string="Technique"
                      name="marketone_bo_technical"
                      invisible="not sale_ok"
                      groups="base.group_no_one">
                    <group string="Traçabilité pipeline média">
                        <field name="shop_tile_recipe_version" readonly="1"/>
                        <field name="shop_tile_processed_at" readonly="1"/>
                        <field name="shop_tile_source_run" readonly="1"/>
                    </group>
                </page>
            </xpath>
        </field>
    </record>
</odoo>
```

### 1.4 Points d’attention implémentation

| Point | Action |
|-------|--------|
| Xpath Odoo 19 | Valider les noms de champs réels dans `website_sale.product_template_form_view` (ex. `is_published` vs `website_published`, `website_description` vs `description_ecommerce`) avant merge |
| Doublons | Ne masquer (`invisible`) un champ standard **que** s’il est re-présenté dans « Publication site » |
| Ordre onglets | Insérer après les onglets natifs ; séquence `priority` 25 pour passer après les héritages existants |
| Attribut Origines | **Pas de nouveau champ produit** : rester sur `attribute_line_ids` standard |

### 1.5 Schéma cible (BO)

```text
Fiche produit (product.template)
├── Image principale (image_1920)          ← inchangée, zone standard Odoo
├── Onglets natifs Odoo (Général, Ventes, …)
└── Notebook CK (si sale_ok)
    ├── Publication site     → website_published, public_categ_ids, website_sequence, website_description
    ├── Catalogue CK         → marketone_collection_ids + aide origines
    ├── Qualité image        → image_shop_tile, shop_tile_status, shop_tile_moa_note
    └── Technique (no_one)   → shop_tile_recipe_version, shop_tile_processed_at, shop_tile_source_run
```

---

## 2. Champs — conserver, masquer, renommer, déplacer

### 2.1 Règle générale

- **Noms techniques Python** (`image_shop_tile`, `shop_tile_*`) : **inchangés** — scripts batch (`scripts/import_shop_tiles.py`), tests front et API internes restent stables.
- **Libellés utilisateur** (`string=`, labels Selection, textes d’aide) : **renommés** en langage métier.
- **Aucun champ supprimé** dans ce lot.

### 2.2 Table de décision

| Champ | Action | Emplacement BO | Libellé cible (utilisateur) |
|-------|--------|----------------|----------------------------|
| `image_1920` | Conserver | Zone image standard | *(libellé Odoo natif)* |
| `website_published` | Déplacer | Publication site | *(libellé Odoo natif)* |
| `public_categ_ids` | Déplacer | Publication site | *(libellé Odoo natif)* |
| `website_sequence` | Déplacer | Publication site | *(libellé Odoo natif)* |
| `website_description` | Déplacer | Publication site | *(libellé Odoo natif)* |
| `marketone_collection_ids` | Déplacer | Catalogue CK | Collections commerciales |
| Attribut « Origines » | Conserver | Attributs & variantes (standard) | — |
| `image_shop_tile` | Conserver + renommer | Qualité image | **Vignette catalogue normalisée** |
| `shop_tile_status` | Conserver + renommer | Qualité image | **Statut média catalogue** |
| `shop_tile_moa_note` | Conserver + renommer | Qualité image | **Note qualité visuelle** |
| `shop_tile_recipe_version` | Masquer (no_one) | Technique | Version recette pipeline |
| `shop_tile_processed_at` | Masquer (no_one) | Technique | Traité le |
| `shop_tile_source_run` | Masquer (no_one) | Technique | Identifiant run batch |
| Param `marketone.shop_tile_enabled` | Conserver | Paramètres système | Hors fiche produit |

### 2.3 Renommage des valeurs `shop_tile_status`

| Valeur technique | Libellé actuel | Libellé proposé |
|------------------|----------------|-----------------|
| `none` | Aucune | Aucune |
| `validated_grid` | Validée grille /shop | **Validée pour affichage catalogue** |
| `validated_storage` | Validée stockage (non affichée) | **Validée — stockage uniquement** |
| `validated_reserve` | Validée avec réserve | Validée avec réserve |
| `pending_review` | En revue | En revue |
| `needs_review_source` | Source à revoir | Source à revoir |
| `rejected` | Rejetée | Rejetée |
| `validated` | Validée (legacy pilote) | Validée (historique pilote) |

### 2.4 Renommage Python (`models/product_template_shop_tile.py`)

| Champ | `string` actuel | `string` proposé | `help` proposé |
|-------|-----------------|----------------|----------------|
| `image_shop_tile` | Tuile /shop | Vignette catalogue normalisée | Dérivé média pour la grille boutique. Ne remplace pas l’image produit principale. |
| `shop_tile_status` | Statut tuile /shop | Statut média catalogue | Indique si la vignette normalisée peut être affichée en catalogue. |
| `shop_tile_recipe_version` | Recette tuile | Version recette pipeline | *(visible no_one uniquement)* |
| `shop_tile_processed_at` | Tuile traitée le | Traité le | *(visible no_one uniquement)* |
| `shop_tile_source_run` | Run source CLI | Identifiant run batch | *(visible no_one uniquement)* |
| `shop_tile_moa_note` | Note MOA tuile | Note qualité visuelle | Commentaire MOA sur la qualité visuelle catalogue. |

### 2.5 Logique métier — inchangée

```python
# Comportement front conservé tel quel
marketone_use_shop_tile_on_grid()
# → validated_grid + flag marketone.shop_tile_enabled + image_shop_tile
# → sinon fallback image_1920
```

Aucune modification de `marketone_use_shop_tile_on_grid()`, des templates QWeb, des contrôleurs ou des assets.

---

## 3. Impacts XML / vues / groupes de sécurité

### 3.1 Fichiers modifiés

| Fichier | Action |
|---------|--------|
| `views/product_template_marketone_bo_views.xml` | **Créer** — vues unifiées BO |
| `views/product_template_shop_tile_views.xml` | **Supprimer** |
| `views/marketone_shop_collection_views.xml` | **Retirer** le record `product_template_form_marketone_collections` |
| `models/product_template_shop_tile.py` | **Modifier** — libellés `string` / `help` / Selection uniquement |
| `__manifest__.py` | Remplacer `product_template_shop_tile_views.xml` par `product_template_marketone_bo_views.xml` ; bump version `19.0.16.0.0` |

### 3.2 Fichiers explicitement hors périmètre (aucune modification)

| Zone | Fichiers |
|------|----------|
| Front QWeb | `views/pages/*.xml`, `views/layout/*.xml` |
| Contrôleurs | `controllers/*.py` |
| Assets | `static/src/**` |
| Scripts batch | `scripts/import_shop_tiles.py`, `scripts/apply_*.py` |
| Modèles catalogue / front | `models/product_template.py`, `models/marketone_shop_*.py` (hors libellés tuile) |
| Données | `data/*.xml` |
| Sécurité modèles | `security/ir.model.access.csv` |

### 3.3 Groupes de sécurité

| Besoin | Solution | Nouveau groupe ? |
|--------|----------|------------------|
| Onglet Technique | `groups="base.group_no_one"` sur la page | **Non** |
| Champs batch en lecture seule | `readonly="1"` dans l’onglet Technique | **Non** |
| Édition vignette / statut | Groupes produit standard (`sales`/designer) | **Non** |
| Accès collections / origines (menus BO) | Inchangé — `website.group_website_designer` | **Non** |

**Conclusion sécurité** : pas de nouveau `res.groups` dans ce lot. Le masquage repose sur `base.group_no_one` (standard Odoo pour le technique).

### 3.4 Risque upgrade Odoo

Si une mise à jour `website_sale` déplace les xpath des champs eCommerce, l’héritage `product_template_form_view_marketone_bo_hide_ecommerce_dup` peut nécessiter un ajustement xpath — à couvrir par un test d’installation / vue (voir §4).

---

## 4. Tests de non-régression

### 4.1 Nouveau fichier — `tests/test_marketone_product_form_bo.py`

| Test | Assertion |
|------|-----------|
| `test_bo_view_no_tile_block_near_main_image` | L’arch ne contient ni `Tuile commerce /shop` ni `marketone_shop_tile_group` |
| `test_bo_view_notebook_pages_present` | Présence des pages `marketone_bo_publication`, `marketone_bo_catalogue`, `marketone_bo_media_quality`, `marketone_bo_technical` |
| `test_bo_technical_page_restricted` | Page `marketone_bo_technical` avec `groups="base.group_no_one"` |
| `test_bo_technical_fields_not_on_media_page` | `shop_tile_recipe_version`, `shop_tile_source_run` absents de `marketone_bo_media_quality` |
| `test_bo_field_labels_renamed` | Champs `image_shop_tile`, `shop_tile_moa_note` — libellés sans « tuile », « /shop », « CLI » |
| `test_bo_collections_field_on_catalogue_page` | `marketone_collection_ids` dans l’onglet Catalogue CK |

Tag suggéré : `@tagged("post_install", "-at_install", "dorevia_marketone_bo")`.

### 4.2 Suite existante — exécution obligatoire sans modification fonctionnelle

| Fichier test | Pourquoi |
|--------------|----------|
| `test_marketone_shop_tile_image.py` | Garantit que le front grille conserve le fallback / dérivé |
| `test_marketone_lot3_shop.py` | Grille /shop |
| `test_marketone_shop_in_place.py` | UX preview (non modifiée) |
| `test_marketone_collection_lot_a.py` | M2M collections |
| `test_marketone_smoke.py` | Install module |

Commande cible :

```bash
odoo-bin -d <base_test> --test-tags=dorevia_marketone_bo,dorevia_marketone_shop_tile -i dorevia_ckreyol_marketone --stop-after-init
```

Puis recette manuelle MOA courte :

1. Ouvrir un produit vendable publié.
2. Vérifier absence du bloc « Tuile commerce /shop » sous l’image principale.
3. Parcourir les 4 onglets CK.
4. Mode développeur : vérifier l’onglet Technique.
5. Visiter `/shop` — rendu identique (tuiles / fallback).

### 4.3 Critères GO lot

- [ ] Tous les tests CI du module passent.
- [ ] Aucun diff dans `views/pages/`, `controllers/`, `static/`.
- [ ] Recette manuelle BO validée MOA.
- [ ] Recette visuelle `/shop` sans régression constatée.

---

## 5. Confirmation — aucune logique front nouvelle

### 5.1 Engagement lot

Ce lot est **strictement BO**. Il ne contient :

- ❌ aucun nouveau template QWeb ;
- ❌ aucun contrôleur HTTP ;
- ❌ aucun asset SCSS / JS ;
- ❌ aucune route `/shop` ;
- ❌ aucune modification de `marketone_use_shop_tile_on_grid()` ;
- ❌ aucun changement de domaine catalogue / facettes ;
- ❌ aucune dépendance `website_blog` / `website_forum`.

### 5.2 Comportement front garanti inchangé

| Mécanisme | Fichier | Statut lot BO |
|-----------|---------|---------------|
| Affichage vignette grille | `views/pages/shop_product_tile_image.xml` | Inchangé |
| Doctrine image v2 | `models/product_template_shop_tile.py` (méthodes) | Inchangé |
| Flag global | `data/marketone_shop_tile_config.xml` | Inchangé |
| Import batch tuiles | `scripts/import_shop_tiles.py` | Inchangé (noms champs stables) |

### 5.3 Gel UX front (rappel MOA)

Jusqu’à validation MOA de ce lot :

- lots UX-4+ : **gelés** ;
- corrections de **régression** ou **bug bloquant** : autorisées, hors périmètre fonctionnel ;
- Blog / Forum : **traitement séparé**, hors ce lot.

---

## 6. Estimation et séquencement

| Étape | Durée estimée |
|-------|---------------|
| Vues XML + retrait anciennes vues | 0,5 j |
| Renommage libellés Python | 0,25 j |
| Tests BO + exécution suite | 0,5 j |
| Recette manuelle MOA | 0,25 j |
| **Total** | **~1,5 j ouvré** |

Séquence recommandée :

1. Implémenter vues + libellés.
2. Lancer tests automatisés.
3. Recette BO MOA.
4. GO → seulement ensuite reprise éventuelle lots front ou arbitrage Blog.

---

## Documents liés

| Document | Rôle |
|----------|------|
| [`DECISION_MOA_RECADRAGE_BO.md`](./DECISION_MOA_RECADRAGE_BO.md) | Décision MOA |
| [`RETOUR_EXPERT_RECADRAGE.md`](./RETOUR_EXPERT_RECADRAGE.md) | Analyse initiale |
| [`../cadrage/DOCTRINE_IMAGE_V2.md`](../cadrage/DOCTRINE_IMAGE_V2.md) | Deux images, trois décisions |
| [`../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) | Anti-régression `/shop` |
