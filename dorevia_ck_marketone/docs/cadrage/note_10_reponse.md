# Retour Dev/QA — Note 10 · CK-CATALOG-ARCHI-001 · Gouvernance d'exposition catalogue

| Champ | Valeur |
| --- | --- |
| Date | 3 juillet 2026 |
| Référence | [`note_10.md`](note_10.md) |
| Modules cibles | `dorevia_ck_marketone_content` (modèles, nav, sitemap, qualification) · `dorevia_ck_theme` (templates cards/badges) |
| Statut | Analyse Dev/QA — évaluation d'impact + amendements, avant découpage ticket |
| Version module actuelle | `dorevia_ck_marketone_content` 19.0.1.82.0 · `dorevia_ck_theme` 19.0.1.120.0 |

---

## Synthèse

**Le diagnostic MOA est confirmé par le code, et sa cause racine est identifiée précisément.** La navigation catalogue active aujourd'hui (`bootstrap_ck_catalogue_navigation`, [nav_sync.py:678](../../dorevia_ck_marketone_content/nav_sync.py#L678), branchée en `post_init_hook` et dans la dernière migration nav `19.0.1.73.0`) expose au header **toute catégorie racine dès qu'elle a un seul produit publié** — le helper `_category_has_published_products` ([nav_mega_menu.py:47](../../dorevia_ck_marketone_content/nav_mega_menu.py#L47)) ne teste qu'une existence (`limit=1`), sans seuil. C'est très probablement la cause directe de ce que la revue MOA a observé sur Boissons / Soin & bien-être / Artisanat.

**Une partie du dispositif demandé existe déjà, sous une autre forme, et doit être réutilisée plutôt que redupliquée :**

| Demande de la note | Existant réutilisable | Écart réel à combler |
| --- | --- | --- |
| §6.3 seuil catégorie active (3 produits) | Bloc de rebond rayon pauvre déjà livré (Note 07 Lot C) — `ck_should_show_rebound` / `ck_sparse_grid_class` ([shop_rebound.py](../../dorevia_ck_marketone_content/shop_rebound.py)), seuil déjà 1–2 produits = pauvre, ≥3 = ok | Le seuil est en dur (`count >= 3`) et non partagé avec la nav header — à extraire en constante commune |
| §6/§12.1 statut/éligibilité catégorie | `ck_universe` + `_get_ck_universe()` ([product_public_category.py:11](../../dorevia_ck_marketone_content/models/product_public_category.py#L11)) donne déjà l'intention éditoriale par univers | Aucun champ de statut (`active/promise/hidden/draft/archived`) n'existe — 100 % à créer |
| §10 cards par famille | `RAYON_EDITORIAL` (par univers) + ligne meta unifiée sur les vedettes Home ([home_featured.py](../../dorevia_ck_marketone_content/home_featured.py)) | La ligne meta n'est pas différenciée par famille produit sur les cards shop/catégorie (template Odoo standard `website_sale.products_item`, [website_sale_product_card.xml](../../dorevia_ck_theme/views/website_sale_product_card.xml)) |
| §11.4 badge Bio source fiable | `ck.product.badge` a déjà `requires_validation` / `is_sensitive_claim` ([ck_product_badge.py:29](../../dorevia_ck_marketone_content/models/ck_product_badge.py#L29)) | Le rendu carte ne consomme qu'un seul `website_ribbon_id` (standard Odoo, un seul badge) — pas de pool multi-badges avec priorité sur les cards shop/home |
| §12.3 footer | Le footer n'est pas un template CK dédié : c'est la vue standard Odoo `website.footer_custom`, patchée au runtime par `bootstrap_footer_legal_links` ([hooks.py:763](../../dorevia_ck_marketone_content/hooks.py#L763)) | Aucun lien boutique/univers n'y est injecté aujourd'hui — bloc à ajouter selon le même mécanisme (pas de fichier `ckr_footer.xml`, qui appartient à `dorevia_ckreyol_marketplace`, un module Phase 1 distinct — **à ne pas modifier**, voir point de vigilance ci-dessous) |
| §14 filtres origine/producteur | `shop_filter_groups.py` construit déjà les groupes de filtres origine/producteur/préférence | Aucun seuil de masquage (`CK_CATEGORY_FILTER_MIN_PRODUCTS`) — à ajouter dans `CkWebsiteSaleController._get_additional_shop_values` ([controllers/website_sale.py:24](../../dorevia_ck_marketone_content/controllers/website_sale.py#L24)) |

**Ce qui est réellement à construire de zéro (aucun socle) :**

* `ck_exposure_status` + `ck_is_exposable` (§5–§6).
* Tout le §13 SEO/sitemap/routes : aucune surcouche sitemap catégorie n'existe (seul `producer_seo.py` gère un sitemap producteurs) ; aucune notion de `noindex` n'existe dans le code ; le contrôleur shop CK ([controllers/website_sale.py](../../dorevia_ck_marketone_content/controllers/website_sale.py)) n'enrichit que les valeurs de template, il n'intercepte pas la route catégorie elle-même (héritée telle quelle de `website_sale.WebsiteSale`) — un 301/302/404 par statut demande une **surcharge de route**, jamais faite jusqu'ici sur ce contrôleur.
* Qualification produit (`ck_is_qualified_for_public_exposure`) et signalement "produit orphelin" (§7).

---

## 1. Point de vigilance majeur — ambiguïté footer

Une recherche initiale a remonté un fichier `ckr_footer.xml` dans `dorevia_ckreyol_marketplace` ("C-Kreyol - Canal e-commerce spécialisé", Phase 1). Ce module est une **lignée distincte et probablement legacy** — le footer réellement actif pour le site `dorevia_ck_marketone_01` (cf. [[project_ck_demo_tunnel_dbfilter]]) est très vraisemblablement piloté par `bootstrap_footer_legal_links` dans `dorevia_ck_marketone_content/hooks.py`, qui patche la vue standard `website.footer_custom`.

**Avant tout développement Ticket A (bloc footer), le Dev doit confirmer en BO (Réglages > Technique > Vues) quelle vue footer est réellement rendue sur `dorevia_ck_marketone_01`** — ne pas toucher à `dorevia_ckreyol_marketplace` sans validation explicite que ce module est bien installé sur ce site.

## 2. Amendements proposés à la note

1. **Seuil unique centralisé.** Créer une seule constante `CK_CATEGORY_ACTIVE_MIN_PRODUCTS = 3` (nouveau module `ck_catalog_exposure.py` par ex.) et la faire consommer par : le rebond (`shop_rebound.py`, aujourd'hui `count >= 3` en dur), le futur `ck_is_exposable`, et la nav (`_category_has_published_products`). Éviter d'avoir deux seuils "3" qui divergent silencieusement avec le temps.
2. **`ck_exposure_status` par défaut à la migration.** Pour ne rien casser en prod, la migration doit backfiller `active` sur toute catégorie root déjà éligible aujourd'hui (≥1 produit publié) et `hidden` ou `draft` sinon — sans quoi toutes les catégories actuellement visibles disparaîtraient du header au déploiement.
3. **Badges carte (§11) : scinder le périmètre.** Le modèle actuel n'a qu'un seul `website_ribbon_id` par produit sur les cards shop/home (contrairement aux chips multi-badges déjà livrées en fiche produit, cf. [[project_ck_chips_u2]]). Recommandation : soit (a) limiter V1 à un seul ribbon + éventuellement un chip producteur/origine à part (réutiliser le pattern `get_ck_product_page_chips`, pas un "pool de badges avec priorité" sur les cards), soit (b) accepter un chantier plus lourd pour porter un vrai pool multi-badges sur les cards. À trancher avec MOA — la note suppose une capacité (stack de badges + priorité) qui n'existe pas aujourd'hui sur les cards.
4. **Ticket B : séparer données et code.** Les 6 produits cités (Pâte de manioc, Savon vétiver, Chapeau Panama, Jus Mont-Pelé, Tambour, Coffret découverte) **ne sont pas dans des fichiers de données versionnés** — ils vivent en base sur le sandbox. Leur recatégorisation est une **correction BO** (rapide, sans déploiement), pas un ticket Dev. Le ticket Dev ne doit porter que sur le mécanisme (`ck_is_qualified_for_public_exposure`, détection produit orphelin) ; la correction de données doit être faite directement en BO et vérifiée par la QA en recette, indépendamment du déploiement Dev.
5. **§13.2 routes : préférer 301 à 404 par défaut.** Une catégorie `hidden`/`archived` peut déjà être indexée par Google ou partagée en lien. Recommandation : rediriger (301/302 vers `/shop` ou catégorie de remplacement) plutôt que 404 dès que possible, réserver 404 aux catégories `draft` qui n'ont jamais été publiques. La note l'autorise déjà en option ; on le fixe en règle par défaut pour éviter une perte SEO/UX sur des URLs déjà connues.

## 3. Risques

* **Nav** : changer le seuil de la nav catalogue (`_category_has_published_products` → seuil 3) est un changement de comportement direct sur le header live — nécessite recette visuelle sur les 4 univers avant/après, pas seulement des tests unitaires.
* **Sitemap/SEO (Ticket C)** : plus gros risque du lot — net new, touche à l'indexation Google, doit être qualifié par un test dédié "aucune page noindex dans le sitemap public" (déjà demandé en §20.5 de la note) avant mise en prod.
* **Cross-module** : si le footer actif s'avère être `dorevia_ckreyol_marketplace` (à confirmer, cf. §1), le lot touche un troisième module non prévu dans la note.

## 4. Découpage retenu

Conforme à la recommandation §24 de la note — 4 tickets, détaillés dans [`TICKET_DEV_CATALOG_ARCHI_001.md`](TICKET_DEV_CATALOG_ARCHI_001.md) :

* **Lot A** — Statut d'exposition + nav header/Home/footer (dépend de l'amendement §2.1 et §2.2 ci-dessus).
* **Lot B** — Qualification produit + mécanisme carte par famille (la correction de données produit est extraite en tâche QA/BO séparée, cf. amendement §2.4).
* **Lot C** — SEO / sitemap / noindex / routes catégories (net new, le plus risqué).
* **Lot D** — Filtres contextuels + seuils (peut glisser au sprint suivant sans bloquer A/B/C).
