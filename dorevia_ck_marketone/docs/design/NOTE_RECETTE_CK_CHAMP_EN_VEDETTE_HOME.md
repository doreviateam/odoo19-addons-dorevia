# Note recette — Champ BO `En vedette` · Section « Nos coups de cœur »

| Champ | Valeur |
|---|---|
| **Ticket** | `TICKET_DEV_CK_CHAMP_EN_VEDETTE_HOME_COUPS_DE_COEUR.md` |
| **Branche** | `feat/ck-featured-field-home` |
| **Module** | `dorevia_ck_marketone_content` **19.0.1.28.3** |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |

---

## Changement métier

La section homepage **« Nos coups de cœur »** est pilotée par le booléen BO **`product.template.ck_is_featured`** (toggle **En vedette**), et non plus par l’appartenance à la catégorie e-commerce **« Coups de cœur »**.

| Règle | Comportement |
|---|---|
| Source homepage | `ck_is_featured=True` · publié · vendable · image exploitable |
| Ordre / plafond | `website_sequence asc, id asc` · max **8** cartes |
| Aucune vedette | Section **masquée** sur la home (toutes langues SSR) |
| Catégorie « Coups de cœur » | Peut subsister au catalogue / nav — **ne pilote plus** la home |
| Ruban | Indépendant du flag En vedette |
| Migration | Produits déjà en catégorie → `ck_is_featured=True` |

---

## Fichiers modifiés

| Fichier | Nature |
|---|---|
| `models/product_template.py` | Champ `ck_is_featured` + hooks refresh |
| `views/product_template_views.xml` | Toggle sous Étiquettes produit |
| `home_featured.py` | Sélection booléen · bootstrap sans fallback · migration helper |
| `models/product_public_category.py` | Retrait hook refresh catégorie |
| `migrations/19.0.1.28.3/post-migrate.py` | Migration catégorie → booléen + bootstrap home |
| `tests/test_ck_home_section3_*.py` | Refactor tests curation / lot2 / compose |
| `tests/test_ck_home_section3_featured_field.py` | T5 · T7 multi-langues · T8 migration |
| `catalog_manioc_variants.py` | Détection Saveur/Format · alignement prix MOA · gate Manioc exécutable |
| `tests/test_ck_catalog_manioc_variants.py` | Jeu MOA `ck_is_featured` explicite · libellés flexibles |
| `tests/test_ck_product_sales_tab_bo.py` | T1 ordre champ BO |
| `__manifest__.py` | Bump **19.0.1.28.3** |

**Supprimé** : `get_ready_featured_variants()` · `MIN_FEATURED_PRODUCTS` (plus de fallback auto).

---

## Recette BO (manuelle)

1. **Upgrade** : `-u dorevia_ck_marketone_content` sur l’instance seed.
2. **Redémarrer le conteneur Odoo** après l’upgrade (ex. `docker restart sandbox-odoo19-odoo-1`). Sans redémarrage, le worker conserve l’ancien registre Python et le BO peut afficher `ck_is_featured field is undefined` jusqu’au reload du process.
3. Ouvrir un produit → onglet **Ventes** → bloc **Classement boutique** :
   - Vérifier le toggle **En vedette** juste après **Étiquettes produit**.
3. Cocher **En vedette** sur un produit publié avec image → recharger `/` → la card apparaît.
4. Décocher **En vedette** → la card disparaît (sans retirer la catégorie catalogue).
5. Retirer la catégorie « Coups de cœur » d’un produit **En vedette** → la card **reste** sur la home.
6. Décocher toutes les vedettes → la section **Nos coups de cœur** disparaît entièrement.
7. Changer de langue front (`/fr` ou sélecteur) → même comportement masquage / affichage.

---

## Tests automatiques

> **Port HTTP** : ne pas utiliser `--no-http` seul sur le sandbox — le port `8069` est déjà occupé par le worker live. Passer **`--http-port=8078`** (convention QA CK).

```bash
docker exec sandbox-odoo19-odoo-1 odoo \
  -d dorevia_ck_marketone_01 --test-enable --stop-after-init --http-port=8078 \
  --test-tags=dorevia_ck_marketone_home_section3_curation,dorevia_ck_marketone_home_section3_featured_field,dorevia_ck_marketone_home_section3,dorevia_ck_marketone_home_lot2,dorevia_ck_marketone_catalog_manioc,dorevia_ck_product_sales_tab_bo
```

Attendu : **65 tests exécutés** (59 gates section 3 / lot2 / BO + **6** `catalog_manioc`) · 0 failed · 0 error · **0 skipped** sur `catalog_manioc`.

| Tag | Périmètre |
|---|---|
| `dorevia_ck_marketone_home_section3_curation` | Sélection · ordre · cap 8 · ruban · refresh arch |
| `dorevia_ck_marketone_home_section3_featured_field` | T5 sans image · T7 multi-langues · T8 migration |
| `dorevia_ck_marketone_home_section3` | Compose SSR section 3 |
| `dorevia_ck_marketone_home_lot2` | Contrat lot2 sans fallback |
| `dorevia_ck_marketone_catalog_manioc` | Variantes Manio conservées |
| `dorevia_ck_product_sales_tab_bo` | T1 champ BO |

---

## Critères GO merge

- [ ] Upgrade **19.0.1.28.3** OK sur seed
- [ ] Produits seed en catégorie « Coups de cœur » migrés vers `ck_is_featured=True`
- [ ] Home seed affiche les vedettes attendues post-migration
- [ ] Section masquée si 0 vedette — **fr_FR et en_US** (SSR)
- [ ] Tests CI tags ci-dessus verts
- [ ] Nav-Shop / header **non régressés** (catégorie catalogue toujours visible si seed)

---

*Note recette Dev — lot En vedette homepage.*
