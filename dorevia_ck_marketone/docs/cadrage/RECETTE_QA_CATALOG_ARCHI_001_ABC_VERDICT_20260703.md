# Recette QA — CATALOG-ARCHI-001 Lots A+B+C

| Champ | Valeur |
| --- | --- |
| Date | 3 juillet 2026 |
| Rôle recette | Carole — QA Odoo + regard marketing |
| Support | `RECETTE_SUPPORT_CATALOG_ARCHI_001_ABC.md` |
| Base | `dorevia_ck_marketone_01` |
| URL locale | `http://localhost:18079` |
| Viewports | Desktop 1280 px · Mobile 390 px |
| Artefacts | `captures/recette_catalog_archi_001_abc_20260703/recette_catalog_archi_001_abc_results.json` · `captures/recette_catalog_archi_001_abc_20260703/recette_catalog_archi_001_lotc_switches.json` |

## Verdict

```text
Recette visuelle/fonctionnelle CATALOG-ARCHI-001 A+B+C
→ Perception commerciale conforme à la doctrine : OUI
→ Cas limites Lot C (301/302/404/sitemap) : OK
→ Point Pâte de manioc (hors périmètre Dev) : toujours ouvert
→ Verdict global : GO, avec réserve BO/QA maintenue sur Pâte de manioc
```

## Décision provisoire MOA

La recette technique est GO sur la doctrine actuelle **"non exposé mais accessible"** :

```text
Les univers Boissons, Soin & Bien-être et Artisanat restent techniquement active
en environnement de travail, avec pages directes 200 noindex, hors sitemap et
hors navigation forte.

Avant ouverture publique, la MOA devra arbitrer univers par univers entre :
- maintien active si rayon marchand assumé ;
- bascule promise/hidden si univers encore immature.
```

Conséquence : les routes directes Boissons/Soin/Artisanat en `200 noindex` ne sont pas un bug code immédiat. Elles deviendront `302 /shop` uniquement si la MOA choisit la doctrine plus stricte **"non prêt = non marchand"** et bascule les catégories en `promise` ou `hidden`.

## Constat immédiat

| Point contrôlé | Verdict | Observation |
| --- | --- | --- |
| Catégories réelles | OK | Les 4 catégories sont `active`, mais seul le seuil Épicerie est atteint : Épicerie 4 produits, Soin 1, Artisanat 2, Boissons 1. |
| Header principal | OK | Rendu desktop : `Boutique`, `Épicerie`, `Producteurs`, `Professionnels`. Pas de Boissons/Soin/Artisanat en rayon principal. |
| Footer Boutique | OK | Colonne Boutique : `Tous les produits` + `Épicerie` uniquement. |
| Home univers | OK | Les 4 cartes restent visibles ; Épicerie pointe vers `/shop/category/epicerie-1`, les 3 autres CTA pointent vers `/shop`. |
| SEO/sitemap | OK | `/sitemap.xml` contient `epicerie-1` et exclut `boissons-123`, `soin-bien-etre-2`, `artisanat-3`. |
| Routes catégories actives sous seuil | OK | Boissons/Soin/Artisanat restent accessibles en `200` direct, mais avec `meta robots=noindex` et hors sitemap. |
| Desktop/mobile | OK | Routes de référence en `200`, pas d'overflow horizontal, pas d'erreur JS applicative détectée. |

## Qualification produits

| Produit | Verdict | Observation |
| --- | --- | --- |
| Chapeau Panama | OK | Présent sur `/shop`, absent des Coups de cœur Home. Card sans ligne origine/producteur, cohérent avec la disqualification curation. |
| Coffret découverte créole | OK | Présent sur `/shop`, `ck_is_orphan=true` en base, pas de masquage brutal. |
| Confiture de goyave | OK | Présente Home et `/shop`, meta : `Guadeloupe · Komla · 320 g · 17,19 €/kg`. |
| Manio Crackers | OK | Présent Home et `/shop`, meta producteur/format visible. |
| Savon vétiver | OK | Présent Home et `/shop`, meta : `Dominique (Ile) · Rwan Ltd · Bio · 125 g · 50,40 €/kg`. |
| Tambour Gro Ka | OK | Présent sur `/shop`, meta : `Guadeloupe · GoZié Lantan`; non bloquant s'il n'est pas dans les 4 slots Home actuels. |
| Pâte de manioc | Réserve BO/QA | Toujours visible avec meta incohérente `Guadeloupe · Bien-être · Sans Gluten · 1 kg · 3,95 €/kg`. Hors périmètre Dev de ce lot. |

## Lot C — bascule temporaire Boissons

Boissons (id 123) a été utilisée comme catégorie de test, puis restaurée en `active` sans catégorie de remplacement.

| Statut testé | Résultat HTTP | Sitemap | Verdict |
| --- | --- | --- | --- |
| `promise` | `302` → `/shop` | Boissons absente | OK |
| `hidden` | `302` → `/shop` | Boissons absente | OK |
| `draft` | `404` propre | Boissons absente | OK |
| `archived` avec remplaçante Épicerie | `301` → `/shop/category/epicerie-1` | Boissons absente | OK |
| `archived` sans remplaçante | `404` propre | Boissons absente | OK |
| Restauration | Boissons revenue en `active`, route directe `200` + `noindex` | Boissons toujours absente | OK |

## Grille synthétique routes

| Route | HTTP | SEO | JS | Overflow desktop/mobile | Verdict |
| --- | --- | --- | --- | --- | --- |
| `/` | `200` | indexable | OK | OK | OK |
| `/shop` | `200` | indexable | OK | OK | OK |
| `/shop/category/epicerie-1` | `200` | indexable | OK | OK | OK |
| `/shop/category/boissons-123` | `200` | `noindex`, hors sitemap | OK | OK | OK |
| `/shop/category/soin-bien-etre-2` | `200` | `noindex`, hors sitemap | OK | OK | OK |
| `/shop/category/artisanat-3` | `200` | `noindex`, hors sitemap | OK | OK | OK |

## Note QA

Le drawer mobile n'a pas été ouvert automatiquement par la sonde sur ces pages ; le contrôle mobile confirme toutefois l'absence d'overflow, d'erreur JS et de liens catégories parasites visibles en header fermé. Ce point n'est pas bloquant pour CATALOG-ARCHI-001.
