# Ticket Dev — Axe B · Correction libellés navigation & badges Home

| Champ | Valeur |
| --- | --- |
| Projet | `dorevia_ck_marketone` |
| Baseline | `main` après S1 Shop recevable · Navigation Communauté `19.0.1.40.0` (`12a24f6`) |
| Axe | B — Carte de navigation |
| Type | Correction libellés / cohérence UX |
| Priorité | Haute |
| Périmètre | Header + libellés de rubans produits visibles |
| Statut | Livré — QA **GO** (`19.0.1.41.0`) |
| Responsable | Dev expert Odoo |
| Références | [PROTOCOLE_QA_AXE_C — action 9](./PROTOCOLE_QA_AXE_C_SECURISATION_BO_20260624.md) · [OBS-2 clôture Communauté](../NOTE_CLOTURE_NAV_COMMUNAUTE_20260625.md) · [RECETTE Shop S1](./RECETTE_SHOP_STRUCTURE_S1_20260624.md) · [Recette QA](./RECETTE_QA_AXE_B_LIBELLES_NAV_BADGES_20260625.md) |
| Modules probables | `dorevia_ck_marketone_content` (nav V2.2, rubans) · `dorevia_ck_theme` (affichage badge uniquement si nécessaire) |

---

## 1. Contexte

La baseline Shop S1 est validée et stabilisée. La Home dispose désormais d'une section éditoriale cohérente **« Nos coups de cœur »**, tandis que la navigation header porte une logique plus claire autour des univers et de la communauté (entrée **Communauté** livrée en `19.0.1.40.0`).

Deux incohérences front restent visibles et doivent être corrigées avant de poursuivre l'Axe B :

1. le header affiche encore **« Maison & Bien-être »**, alors que l'univers cible est **« Soin & Bien-être »** ;
2. certains rubans produits affichent **« New! »** au lieu de **« Nouveau ! »**.

Ces corrections doivent rester **simples, localisées et sans refonte de structure**.

### État technique connu (sandbox `dorevia_ck_marketone_01`)

| Zone | Constat BO / code |
| --- | --- |
| Menu header | `website_menu` → libellé `Maison & Bien-être` · URL `/shop/category/soin-bien-etre-2` |
| Catégorie e-commerce | `product.public.category` racine → **Soin & Bien-être** (id=2) |
| Config nav V2.2 | `nav_v22_config.NAV_MAISON_LABEL = 'Maison & Bien-être'` · alias BO `Soin & Bien-être` déjà présent dans `RAYON_ROOT_ALIASES` |
| Filmstrip `/shop` | Affiche déjà **Soin & Bien-être** (nom catégorie BO) |

La correction header doit **aligner le libellé menu** sur la catégorie, sans renommer la catégorie BO dans ce ticket.

---

## 2. Objectif

Aligner les libellés visibles pour éviter les dissonances UX.

Règle cible :

```text
Une porte = un nom = une catégorie = une breadcrumb.
```

Pour l'univers concerné, le libellé public attendu est :

```text
Soin & Bien-être
```

---

## 3. Demandes

### 3.1 Header — remplacer « Maison & Bien-être »

Remplacer dans la navigation principale, **desktop et mobile** :

```text
Maison & Bien-être
```

par :

```text
Soin & Bien-être
```

Le lien cible doit être **conservé** s'il pointe déjà vers la bonne catégorie Odoo.

À vérifier notamment :

```text
/shop/category/soin-bien-etre-2
```

ou route équivalente selon le routing actif.

**Préférence d'implémentation** (par ordre) :

1. **Configuration nav** — `nav_v22_config.py` (`NAV_MAISON_LABEL` ou renommage explicite `NAV_SOIN_LABEL`) + resync `bootstrap_ck_navigation` / migration post-upgrade ;
2. **Traduction `fr_FR`** sur l'entrée `website_menu` si le libellé en_US reste technique ;
3. Template QWeb — **uniquement en dernier recours** (hack d'affichage non souhaité).

**Points d'attention Dev :**

- Mega-menu associé : libellés éditoriaux dans `nav_mega_menu.py` (`_FALLBACK_VISUAL_COPY`, titres colonnes) — aligner si le nom du rayon y figure ;
- Ne pas réintroduire **Coups de cœur** en navigation header ;
- Conserver **Communauté** (`href="#"`) inchangée.

### 3.2 Badge produit — traduire « New! »

Remplacer le libellé visible :

```text
New!
```

par :

```text
Nouveau !
```

À vérifier sur :

- Home, section **« Nos coups de cœur »** ;
- cards boutique `/shop` ;
- fiche produit si le ruban est affiché.

**Préférence d'implémentation** (par ordre) :

1. **Donnée `product.ribbon`** — corriger le nom du ruban et/ou sa traduction `fr_FR` ;
2. **XML seed** / migration idempotente si le ruban est livré en données CK ;
3. **Surcharge template** — uniquement si la source est un ruban Odoo core non modifiable en données.

Ne pas modifier la mécanique fonctionnelle des badges (`website_ribbon_id`, classes CSS, position).

---

## 4. Hors périmètre

Ne pas modifier dans ce ticket :

- la structure des catégories (renommage racine BO `Soin & Bien-être`) ;
- le filmstrip Shop ;
- la structure / layout des cards produits ;
- les filtres sidebar ;
- la section Home **« Nos coups de cœur »** (titre, règles, sélection `ck_is_featured`) ;
- les produits publiés ;
- les champs BO produit hors ruban ;
- les rubans fonctionnels hors libellé (ex. « Coup de cœur ») ;
- les modules Blog / Forum / Communauté ;
- les lots S2 / S3 / Home V2 ;
- les mega-menus : contenu familles / sélections (sauf libellé du rayon racine si explicitement « Maison & Bien-être »).

---

## 5. Recette attendue

### Desktop

- Le header affiche **Soin & Bien-être**.
- Le header n'affiche plus **Maison & Bien-être**.
- L'entrée **Communauté** reste présente (`href="#"`).
- L'entrée **Coups de cœur** ne réapparaît pas comme entrée de navigation header.
- Les badges produits concernés affichent **Nouveau !** et non **New!**.

### Mobile

- Le menu mobile affiche **Soin & Bien-être**.
- Le menu mobile n'affiche plus **Maison & Bien-être**.
- Les badges restent lisibles et traduits.

### Non-régression

- La section Home **Nos coups de cœur** reste inchangée (titre + produits affichés).
- Le lien vers la catégorie **Soin & Bien-être** fonctionne (HTTP 200).
- Aucun retour de **Coups de cœur** comme catégorie de navigation header.
- Aucun changement de comportement sur panier, recherche, tri, filtres ou URLs Shop.
- Tags tests existants au vert : `dorevia_ck_header_v22`, `dorevia_ck_marketone_nav_sync`, `dorevia_ck_nav_communaute`, `dorevia_ck_shop_s1`.

### Viewports

- Desktop **1280** · mobile **390**.

---

## 6. Livrables attendus

Merci de fournir :

| Livrable | Détail |
| --- | --- |
| Résumé technique | Fichiers, données, migration, traduction ou template touchés |
| Captures | Header desktop + mobile · card avec badge **Nouveau !** |
| Recette | Note `RECETTE_*` ou section dans ticket avec verdict |
| Mention explicite | Canal de correction : BO / XML / migration / traduction / template |

---

## 7. Critère de réussite

La navigation publique ne présente plus de conflit de vocabulaire :

```text
Soin & Bien-être
```

devient le libellé unique de l'univers concerné dans le header (aligné filmstrip / catégorie), et les badges produits visibles sont francisés **sans modifier la structure Odoo ni les mécaniques existantes**.

---

## 8. Piste technique (indicative — non prescriptive)

| Sujet | Piste |
| --- | --- |
| Label header | `dorevia_ck_marketone_content/nav_v22_config.py` · `nav_sync.py` |
| Resync menu | `bootstrap_ck_navigation()` en migration post-upgrade |
| Ruban | `product.ribbon` · `data/ck_product_ribbon_*.xml` · traductions `fr_FR` |
| Tests à étendre | `test_ck_header_v22.py` · `test_ck_nav_sync.py` · assertion libellé + badge |

---

> *Ticket rédigé pour transmission Dev — exécution après validation MOA/Architecte.*
