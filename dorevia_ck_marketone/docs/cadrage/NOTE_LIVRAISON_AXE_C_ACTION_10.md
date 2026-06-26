# Note de livraison — Axe C · Action 10

| Champ | Valeur |
| --- | --- |
| Date | 26 juin 2026 |
| Module | `dorevia_ck_marketone_content` **19.0.1.42.0** |
| Ticket | Axe C · Action 10 + avis technique catégorie « Coups de cœur » |
| Statut | Livré Dev — QA BO à confirmer |

---

## 1. Action 10 — Libellé `ck_is_featured`

### Modification

Fichier : `dorevia_ck_marketone_content/models/product_template.py`

| Élément | Avant | Après |
| --- | --- | --- |
| `string` | En vedette | **Afficher sur l'accueil** |
| `help` | Affiche ce produit dans la section Nos coups de cœur… | **Affiche ce produit dans les sélections de la page d'accueil C-Kréyòl lorsque les règles de mise en avant le permettent.** |

### Inchangé

- Nom technique du champ : `ck_is_featured`
- Logique `get_curated_featured_variants()` (sélection homepage)
- Vue BO : toggle dans onglet Ventes > Classement boutique (`product_template_views.xml`)
- Cards produit, catégories publiques, front

### Upgrade

```bash
odoo -u dorevia_ck_marketone_content -d dorevia_ck_marketone_01 --stop-after-init
# Puis redémarrer le worker Odoo (rechargement registre Python)
```

### Test auto ajouté

`test_ck_is_featured_field_label_and_help` dans `tests/test_ck_home_section3_featured_field.py`

### QA BO rapide

- [ ] Ouvrir une fiche produit > onglet **Ventes** > bloc **Classement boutique**
- [ ] Vérifier le libellé **Afficher sur l'accueil** et l'infobulle au survol
- [ ] Cocher / décocher : la section Home « Nos coups de cœur » se met à jour (comportement inchangé)

---

## 2. Avis technique — Catégorie publique « Coups de cœur »

### Contexte

La homepage est pilotée par **`ck_is_featured`** depuis la migration `19.0.1.28.3`. La catégorie `product.public.category` « Coups de cœur » (`xmlid` : `dorevia_ck_marketone_content.public_categ_coups_de_coeur`) n'est **plus la source** de la section Home.

Elle reste en base comme reliquat catalogue / tests / hygiène historique.

### Cartographie des références

| Zone | Référence | Impact si suppression physique |
| --- | --- | --- |
| **Homepage `/`** | `get_curated_featured_variants()` → `ck_is_featured` | **Aucun** |
| **Fiches produit** | M2M `public_categ_ids` | **Aucun** si MOA a retiré la catégorie (Action 1) |
| **Menu header** | `website_menu` id=336 (historique) | **Aucun** si entrée supprimée (Action 2 — déjà clôturée nav Communauté) |
| **Filmstrip `/shop`** | Catégories publiques avec produits publiés | **Aucun** si 0 produit rattaché |
| **URL directe** | `/shop/category/coups-de-cœur-24` | **404** — comportement souhaité |
| **Data module** | `data/ck_public_category_coups_de_coeur.xml` | **Recréation possible** au prochain `-u` |
| **Code** | `_ensure_featured_category()` dans `home_featured.py` | **Recréation** si appelée (migrations anciennes, tests) |
| **Tests auto** | `test_ck_home_section3_*`, `test_ck_featured_propagation` | Utilisent `_ensure_featured_category()` — **pas d'impact runtime** |
| **Mega-menu rayons** | Tag `coup_de_coeur` dans `nav_v22_config.py` | **Distinct** de la catégorie publique — conservé |
| **Ruban BO** | `data/ck_product_ribbon_coups_de_coeur.xml` (« Coup de cœur ») | **Distinct** — ruban produit, pas la catégorie |

### Verdict

| Question | Réponse |
| --- | --- |
| Suppression physique sans risque runtime ? | **Oui**, sous conditions |
| Conditions préalables | Actions 1–3 MOA effectuées (0 produit rattaché, menu retiré, filmstrip vérifié) |
| Risque résiduel | Un **`-u dorevia_ck_marketone_content`** peut **recréer** la catégorie via le fichier data XML (pas de `noupdate="1"`) |
| Recommandation MOA (défaut protocole) | **Option A (préférée à court terme)** : laisser la catégorie en base **vide, sans produit, sans menu, invisible filmstrip** |
| Alternative | **Option B** : suppression physique en BO **acceptable** si MOA accepte une éventuelle réapparition fantôme après upgrade module — ou ticket Dev ultérieur pour retirer le record data / passer `noupdate` |

### Procédure MOA recommandée (sans Dev)

1. Retirer « Coups de cœur » de toutes les fiches produit (Action 1).
2. Confirmer absence du pill filmstrip (Action 3 — recette visuelle).
3. **Ne pas supprimer** la catégorie tant que le point data XML n'est pas arbitré — ou supprimer sachant qu'un upgrade peut la recréer.
4. Si suppression : vérifier `GET /shop/category/coups-de-cœur-24` → 404.

### Hors périmètre Action 10 (ticket ultérieur si MOA tranche suppression définitive)

- Retirer `data/ck_public_category_coups_de_coeur.xml` ou l'entourer de `noupdate="1"` + script de nettoyage
- Simplifier `_ensure_featured_category()` (aujourd'hui utile surtout aux tests et migrations historiques)

---

## 3. Critères d'acceptation — bilan

| Critère | Statut |
| --- | --- |
| Libellé BO **Afficher sur l'accueil** | ✅ Code livré |
| Aide champ présente | ✅ |
| Logique fonctionnelle inchangée | ✅ |
| Libellé durable après `-u` | ✅ (définition Python) |
| Aucun impact front non prévu | ✅ (champ BO uniquement) |
| Avis technique catégorie | ✅ (§2 ci-dessus) |
| Tests vedettes verts | ☐ À confirmer QA (`--test-tags dorevia_ck_marketone_home_section3_featured_field`) |

---

*Livraison Dev Axe C Action 10 — C-Kréyòl / CK Marketone*
