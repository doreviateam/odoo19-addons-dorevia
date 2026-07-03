# Support recette visuelle/fonctionnelle — CATALOG-ARCHI-001 Lots A+B+C

| Champ | Valeur |
| --- | --- |
| Date | 3 juillet 2026 |
| Référence | [`TICKET_DEV_CATALOG_ARCHI_001.md`](TICKET_DEV_CATALOG_ARCHI_001.md) — Lots A/B/C livrés/validés/poussés |
| Objet | Support de recette MOA (avec Carole si possible) — vérifier que l'architecture corrigée donne la perception commerciale attendue |
| Base cible | `dorevia_ck_marketone_01` (sandbox + tunnel démo public, cf. [[project_ck_demo_tunnel_dbfilter]]) |
| Viewports | Desktop 1280 px · Mobile 390 px |
| Statut | À dérouler — aucune case cochée à ce stade |

---

## 1. Comment utiliser ce document

Ce document se déroule en 2 temps :

1. **§3 — Constat sur l'état réel actuel** : rien à modifier, juste observer. Le catalogue réel n'a aujourd'hui que le statut `active` sur toutes ses catégories — les effets des Lots A/B (nav/footer/Home/cards/qualification) sont **déjà visibles tels quels**.
2. **§4 — Test des cas limites Lot C** (redirections 301/302, 404, sitemap) : ces comportements ne se déclenchent que pour des catégories `promise` / `hidden` / `draft` / `archived`. Comme aucune catégorie réelle n'a ce statut aujourd'hui, il faut **basculer temporairement** une catégorie de test (procédure §4.1) pour observer ces cas — puis revenir à l'état initial.

Le §5 est la grille de contrôle à remplir route par route. Le §6 est le verdict final.

---

## 2. Routes de référence

* `/`
* `/shop`
* `/shop/category/epicerie-1`
* `/shop/category/boissons-123`
* `/shop/category/soin-bien-etre-2`
* `/shop/category/artisanat-3`

---

## 3. Constat sur l'état réel actuel (aucune manipulation requise)

État constaté le 3 juillet 2026 sur `dorevia_ck_marketone_01` :

| Catégorie | Statut | Produits qualifiés | Exposable (Lot A) | Indexable (Lot C) |
| --- | --- | --- | --- | --- |
| Épicerie (id 1) | `active` | 4 | **Oui** | **Oui** |
| Soin & Bien-être (id 2) | `active` | 1 | Non (sous le seuil de 3) | Non |
| Artisanat (id 3) | `active` | 2 | Non (sous le seuil de 3) | Non |
| Boissons (id 123) | `active` | 1 | Non (sous le seuil de 3) | Non |

**Ce que ça veut dire concrètement pour la recette** : bien que les 4 catégories soient techniquement `active`, seule Épicerie est aujourd'hui assez riche pour être mise en avant. C'est exactement l'effet recherché par la doctrine CK — à vérifier :

* [ ] Header : seule Épicerie apparaît comme rayon principal (Boissons/Soin/Artisanat absentes de la nav catalogue).
* [ ] Footer (colonne Boutique) : seuls "Tous les produits" et "Épicerie" apparaissent.
* [ ] Home "Acheter par univers" : les 4 cartes univers restent visibles (contenu figé), mais les CTA Boissons/Soin/Artisanat pointent vers `/shop` (pas vers leur catégorie spécifique) ; seul le CTA Épicerie pointe vers sa page catégorie.
* [ ] Sitemap (`/sitemap.xml`) : seule `epicerie-1` apparaît parmi les catégories.
* [ ] Routes directes Boissons/Soin/Artisanat : tant que ces catégories restent `active`, elles peuvent répondre en `200` marchand, mais doivent être `noindex` et absentes du sitemap. Ce n'est pas un NO GO technique du lot ; c'est la doctrine provisoire "non exposé mais accessible".

### 3.1 Clarification doctrine provisoire — routes directes

Décision provisoire MOA à consigner avant lancement public :

```text
Les univers Boissons, Soin & Bien-être et Artisanat restent techniquement active
en environnement de travail, avec pages directes 200 noindex, hors sitemap et
hors navigation forte.

Avant ouverture publique, la MOA devra arbitrer univers par univers entre :
- maintien active si rayon marchand assumé ;
- bascule promise/hidden si univers encore immature.
```

Lecture métier associée :

* **Court terme démo / travail interne** : `active` + `200 noindex` accepté pour montrer ou contrôler les pages directes sans les pousser publiquement.
* **Avant lancement public** : basculer en `promise` ou `hidden` les univers qui ne doivent pas exister comme rayons marchands publics ; les routes directes passeront alors en `302` vers `/shop`.

Qualification produit (Lot B) — à vérifier sur `/shop` :

* [ ] Chapeau Panama : présent sur `/shop`, mais absent des "Coups de cœur" Home (traçabilité manquante — origine/producteur à compléter en BO).
* [ ] Coffret découverte créole : présent sur `/shop`, produit orphelin signalé en interne (`ck_is_orphan`), pas de masquage.
* [ ] Confiture de goyave, Manio Crackers, Savon vétiver, Tambour Gro Ka : qualifiés, éligibles aux Coups de cœur si `ck_is_featured` coché.
* [ ] Ligne meta des cards : présence du nom producteur quand renseigné (ex. Confiture de goyave → "Guadeloupe · Komla · 320 g · ...").
* [ ] Point encore ouvert, hors périmètre Dev (à signaler si toujours visible) : Pâte de manioc affiche une métadonnée "Bien-être" incohérente — correction BO/QA en attente, pas un bug de ce lot.

---

## 4. Test des cas limites Lot C (redirections / 404 / sitemap)

### 4.1 Procédure de bascule temporaire (à faire en BO, réversible)

1. Ouvrir une catégorie de test (ou une catégorie réelle peu sensible, ex. Boissons) en BO.
2. Modifier le champ **Statut d'exposition CK** (`ck_exposure_status`).
3. Observer le comportement de la route associée (tableau §4.2).
4. **Remettre le statut initial (`active`) immédiatement après observation** — ne pas laisser une catégorie réelle dans un statut de test.

### 4.2 Comportement attendu par statut

| Statut testé | Route directe attendue | Sitemap |
| --- | --- | --- |
| `promise` | 302 → `/shop` | Absente |
| `hidden` | 302 → `/shop` | Absente |
| `draft` | 404 | Absente |
| `archived` + `ck_replacement_category_id` renseigné | 301 → catégorie de remplacement | Absente |
| `archived` sans remplaçante | 404 | Absente |

Checklist :

* [ ] `promise` → navigateur redirigé vers `/shop`, pas d'erreur.
* [ ] `hidden` → idem.
* [ ] `draft` → page 404 propre (pas d'écran blanc ni d'erreur serveur).
* [ ] `archived` avec remplaçante → redirection vers la bonne catégorie.
* [ ] `archived` sans remplaçante → 404 propre.
* [ ] Après chaque test, catégorie remise en `active` et comportement normal restauré (vérifier un rechargement de la page catégorie).

---

## 5. Grille de contrôle par route

Pour chaque route : cocher desktop (1280 px) et mobile (390 px) séparément.

| Route | Statut HTTP conforme | Header cohérent | Footer cohérent | Cards cohérentes | Pas d'erreur JS | Pas d'overflow mobile | SEO cohérent (noindex/sitemap) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `/` | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | — |
| `/shop` | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| `/shop/category/epicerie-1` | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| `/shop/category/boissons-123` | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| `/shop/category/soin-bien-etre-2` | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |
| `/shop/category/artisanat-3` | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ | ☐ |

---

## 6. Verdict

```text
Recette visuelle/fonctionnelle CATALOG-ARCHI-001 A+B+C
→ Perception commerciale conforme à la doctrine : OUI / NON
→ Cas limites Lot C (301/302/404/sitemap) : OK / À corriger
→ Point Pâte de manioc (hors périmètre Dev) : toujours ouvert / résolu
→ Verdict global : GO / NO GO
```

Points concernés / captures à joindre si NO GO sur un point précis.
