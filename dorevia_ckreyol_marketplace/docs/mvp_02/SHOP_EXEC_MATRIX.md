# MVP2.2 — Boutique / Matrice d'exécution

Document de travail **exécutable** pour la mise en œuvre de la boutique C-Kreyol.

Objectif : éviter les ambiguïtés entre **cible UX**, **état livré**, **fallbacks** et **orchestration réelle** des blocs sur `/shop`.

Ce fichier complète :

- [2_SHOP.md](2_SHOP.md) — cible UX / doctrine ;
- [SPEC_SHOP_PORTES.md](../mvp_01/SPEC_SHOP_PORTES.md) — contrats d'URL, modes, priorités ;
- [TICKET_SHOP_MVP22_VISIBLE_WAVE1.md](../crea/TICKET_SHOP_MVP22_VISIBLE_WAVE1.md) — lots d'implémentation.

## Invariants d'orchestration

1. **Un seul `h1` visible** par page boutique.
2. **Un seul bloc contextuel principal** visible à la fois :
   - hero CK pleine largeur ;
   - ou bandeau porte historique ;
   - jamais les deux ensemble.
3. **Le résultat de recherche reste utilitaire** :
   - pas de grand hero ;
   - pas de micro-copy éditoriale longue ;
   - priorité à la recherche, au tri et à la grille.
4. **La sidebar reste adossée au moteur natif Odoo** en Vague 1 :
   - pas de seconde logique filtres (pas de double `base_domain` parallèle) ;
   - pas de navigation collections parallèle au sens **routes nobles** : le rail CK **liste** des collections et **pointe** vers `/collections/...` ;
   - **Extension livrée** (module ≥ **19.0.1.10.18**) : ordre **Catégories → Collections → Origines → Prix**, injection CK dans le rail, fallbacks `opt_wsale_categories` / `show_price_filter`, non-régression `/shop` documentée (**10.26–10.28**) — détail [TICKET_SHOP_SIDEBAR_CATEGORIES.md](TICKET_SHOP_SIDEBAR_CATEGORIES.md), [SHOP_MAQUETTE_ECARTS.md §2](SHOP_MAQUETTE_ECARTS.md).
5. **Les shortcuts commerciaux réutilisent les routes existantes** :
   - `/promotions` ;
   - `/incontournables` ;
   - `/kits`.
6. **Le fallback ne fabrique jamais de faux contexte** :
   - si `featured` n'est pas configuré, retour `/shop` ;
   - si une collection noble est invalide, repli 302 + message flash ;
   - si une origine est valide mais vide, état vide explicite.

## Matrice par contexte

| Contexte | URL d'entrée | Titre / bloc principal attendu | Shortcuts | Sidebar / filtres | Fallback / note d'exécution | Référence |
|----------|--------------|--------------------------------|-----------|-------------------|-----------------------------|-----------|
| **Toute la boutique** | `/shop` | Hero CK possible, `h1` unique ; copy générique boutique | `Toute la boutique` active | Rail filtres : natif + blocs CK (ordre §4 [2_SHOP.md](2_SHOP.md)) ; recette offcanvas / 4 blocs | Pas de doublon avec titre natif Odoo | [2_SHOP §2-§5](2_SHOP.md) ; [TICKET_SHOP_SIDEBAR_CATEGORIES.md](TICKET_SHOP_SIDEBAR_CATEGORIES.md) |
| **Recherche** | `/shop?search=...` | Pas de grand hero ; contexte de recherche prioritaire | Masqués si bruit visuel ; à défaut, jamais actifs en conflit avec la recherche | Natif Odoo | Le mode recherche prime sur l'éditorial | [2_SHOP §8](2_SHOP.md) |
| **Promotions** | `/promotions` → `/shop?ckr_mode=promo` | `h1 = Promotions` ; hero CK ou bandeau, mais pas les deux | `Promotions` active | Natif Odoo ; pas de logique promo parallèle | État vide dédié si aucune promo active | [SPEC_SHOP_PORTES §4.2](../mvp_01/SPEC_SHOP_PORTES.md) |
| **Incontournables** | `/incontournables` → `/shop?ckr_mode=featured` | `h1 = Incontournables` ; copy sélection éditoriale | `Incontournables` active | Natif Odoo | Si paramètre invalide : fallback `/shop`, sans faux contenu | [2_SHOP §5](2_SHOP.md) |
| **Kits** | `/kits` → `/shop?ckr_mode=pack` | `h1 = Kits` ; contexte pack lisible côté visiteur | `Kits` active | Natif Odoo | Aucun mode concurrent ne doit prendre le dessus hors priorité officielle | [SPEC_SHOP_PORTES §4.3](../mvp_01/SPEC_SHOP_PORTES.md) |
| **Origines (hub)** | `/origines` → `/shop?ckr_mode=origin` | `h1 = Origines` ; copy catalogue par origine | Aucun shortcut actif par défaut | Natif Odoo ; ordre visuel des facettes à ajuster seulement en présentation | Pas d'image héroïque trompeuse si le contexte est purement navigatoire | [SPEC_SHOP_PORTES §4.5](../mvp_01/SPEC_SHOP_PORTES.md) |
| **Origines filtrées** | `/shop?ckr_mode=origin&ckr_origin=...` | `h1 = nom visiteur` si une origine, sinon `Origines` | Aucun shortcut actif | Natif Odoo | Si origine valide mais vide : message + rebond `/shop` / `/shop?ckr_mode=origin` | [views/pages/ckr_shop.xml](../../views/pages/ckr_shop.xml) |
| **Catégorie native** | `/shop/category/<id>-<slug>` | `h1 = category.name` porté par le hero CK **ou** par le header natif, jamais les deux | Aucun shortcut actif par défaut | Natif Odoo | Breadcrumb autorisé si lisible ; pas de double titre | [2_SHOP §8](2_SHOP.md) |
| **Collections — vue générale** | `/collections` | Contexte collections noble ; `h1 = Collections` | Aucun shortcut actif | Pas de facette collections dupliquée en sidebar | Pas de canonical visiteur vers `/shop?ckr_mode=collection` | [SPEC_SHOP_PORTES §4.1 / §4.4](../mvp_01/SPEC_SHOP_PORTES.md) |
| **Collections — vue unitaire / union** | `/collections/<slug>` ; `/collections/union/...` | `h1` piloté par la collection / l'union ; bloc contextuel unique | Aucun shortcut actif | Idem vue générale | Repli 302 + flash en cas de slug invalide / union incomplète | [SPEC_SHOP_PORTES §4.4](../mvp_01/SPEC_SHOP_PORTES.md) |

## Vérifications de recette minimales

- Vérifier les contexts : `/shop`, `search`, `promo`, `featured`, `pack`, `category`, `origin`, `collections`.
- Vérifier qu'aucun écran n'empile :
  - hero CK ;
  - bandeau porte historique ;
  - titre natif Odoo dupliqué.
- Vérifier qu'aucun écran ne présente plus de **deux zones de pilotage** majeures avant la première ligne de produits :
  - contexte ;
  - outils / shortcuts.
- Vérifier que le fallback `featured` est **silencieux et propre**.
- Vérifier que le mode recherche ne réintroduit pas de bruit éditorial.

## Historique

| Date | Événement |
|------|-----------|
| 2026-04-26 | Création — matrice d'exécution boutique pour relier cible UX, contexte route, orchestration QWeb et recette. |
| 2026-04-25 | Invariant **sidebar** : précision rail CK + moteur natif ; ligne **Toute la boutique** / filtres ; renvois **10.26–10.28**. |
