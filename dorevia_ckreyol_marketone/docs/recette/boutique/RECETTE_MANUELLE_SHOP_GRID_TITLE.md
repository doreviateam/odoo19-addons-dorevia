# Recette manuelle — Haut grille /shop — Compteur & organisation

| Champ | Valeur |
|-------|--------|
| **Module** | `dorevia_ckreyol_marketone` |
| **Version cible** | **`19.0.15.9.4`** |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Statut recette** | **GO MOA** — wording état vide **`9.4`** validé |
| **Signal MOA** | GO compteur zéro filtré « trouvé » + état central « cette sélection » + chips `(n)` |
| **Rapport exécution** | [`RAPPORT_RECETTE_SHOP_UX1_ETAT_FILTRES_20260521.md`](../ux/RAPPORT_RECETTE_SHOP_UX1_ETAT_FILTRES_20260521.md) |

---

## Périmètre

Recette **visuelle et comportementale** du haut de la colonne catalogue `/shop` :

1. **Ligne principale** : compteur (gauche) · recherche (centre) · tri (droite) ;
2. **Ligne secondaire** : « Effacer les filtres » + chips, si filtres actifs ;
3. **Grille produits**.

Le compteur n'est **plus** un H1 / bandeau encadré : c'est une **information de contexte légère** (`.marketone-shop-grid-result`).

**Hors périmètre (inchangé)** :

- sidebar filtres · comportement des chips · tri · grille produit · tuiles conversion · doctrine image · routes `/shop`

**Fichiers concernés** :

| Fichier | Rôle |
|---------|------|
| `views/pages/shop_grid_title.xml` | Toolbar `marketone-shop-catalog-toolbar` · compteur `#products_grid_content_title` |
| `views/pages/shop_empty_state.xml` | État vide central contextualisé (MOA `9.2`) |
| `views/pages/shop_filter_state.xml` | Chips **après** le toolbar (sous recherche / résultat / tri) |
| `controllers/website_sale.py` | Libellés compteur · détection état vide filtré |
| `static/src/scss/_shop_grid_header.scss` | Layout recherche · ligne résultat / tri |
| `static/src/scss/_shop.scss` | Bandeau encadré réservé aux portes featured / origin uniquement |

> **Note UX-1** : chips / reset — voir [`RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md`](../ux/RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md). Le compteur « N produit(s) trouvé(s) » n'est **jamais** dans la ligne de tri.

---

## Structure cible MOA

### Cas par défaut (aucun filtre)

```text
50 produits disponibles        [ Rechercher...        🔍 ]        Trier par : En vedette

[ grille produits ]
```

### Cas filtres actifs

```text
9 produits disponibles        [ Rechercher...        🔍 ]        Trier par : En vedette

Effacer les filtres   [Biscuits salés (4) ×] [Martinique (3) ×]

[ grille produits ]
```

### Évolution par version

| Version | Organisation |
|---------|--------------|
| **`8.4`** | 3 lignes — recherche seule L1 · compteur+tri L2 · chips L3 |
| **`8.5`** | 2 lignes — L1 compacte compteur + recherche centrée + tri · L2 chips |
| **`8.6`** | Correctif Sass — **ne pas utiliser** `min()` avec `calc()` · `width` + `max-width` |
| **`9.2`** | État vide central · `shop_empty_state.xml` |
| **`9.3`** | Compteur zéro → **`Aucun produit disponible`** |

---

## Règles MOA — libellés

| Contexte | Condition | Libellé attendu |
|----------|-----------|-----------------|
| **Pluriel** | n > 1 produits visibles | **`{n} produits disponibles`** |
| **Singulier** | Exactement 1 produit visible | **`1 produit disponible`** |
| **Zéro + filtres** | 0 résultat avec recherche / chips actives | **`Aucun produit trouvé`** |
| **Zéro sans filtre** | Catalogue vide réel | **`Aucun produit disponible`** |

Le compteur global répond à : **combien de produits sont visibles dans la grille actuelle ?**  
Libellé **stable** — jamais « correspondent à votre recherche ».

**Compteur** = total des résultats **toutes pages confondues** (identique à `search_count` UX-1).

### État vide central (grille sans produits)

| Contexte | Message central |
|----------|-----------------|
| Filtres / recherche actifs · 0 résultat | **`Aucun produit ne correspond à cette sélection`** |
| Catalogue réellement vide (sans filtre) | `Aucun produit défini` (Odoo natif) |

Exemple MOA combo 0 résultat (Biscuits salés + La Réunion + Apéritif créole) :

```text
Aucun produit trouvé        [ Rechercher...        🔍 ]        Trier par : En vedette

Effacer les filtres   [Apéritif créole (0) ×] [Biscuits salés (0) ×] [La Réunion (0) ×]

        [ icône loupe ]
Aucun produit ne correspond à cette sélection
```

Référence capture **KO avant 9.3** : [`capture_recette_ux1_avant_wording_etat_vide_20260521.png`](../ux/capture_recette_ux1_avant_wording_etat_vide_20260521.png)

### Compteurs dans les chips (optionnels)

| Type chip | Compteur `(n)` | Règle |
|-----------|----------------|-------|
| Catégorie | Oui si fiable | Produits de cette catégorie dans le contexte courant (sans la facette catégorie) |
| Collection | Oui si fiable | Idem pour la collection |
| Origine | Oui si fiable | Produits de cette origine dans le contexte courant |
| Prix | **Non** | Ambigu / non affiché (garde-fou MOA) |

Exemple : `Biscuits salés (4)` · `Martinique (3)` · `Prix : 5 € – 12 €` (sans chiffre).

---

## Règles MOA — présentation visuelle

| Règle | Attendu |
|-------|---------|
| **Hiérarchie** | Le compteur ne concurrence **pas** la grille produit |
| **Encadrement** | **Pas** de cartouche / bandeau autour du compteur catalogue |
| **Style** | Texte discret · classe `.marketone-shop-grid-result` · ton contexte (label, opacité ~72 %) |
| **Recherche** | **Ligne principale** · visuellement **centrée** · compacte |
| **Ligne principale** | Compteur gauche · recherche centre · tri droite · **une seule ligne** · sans cartouche |
| **Tri** | Calé **à droite** · même ligne que compteur et recherche |
| **Chips** | **Ligne secondaire** · sous la ligne principale · uniquement si filtres actifs |
| **Portes** | Titres featured / origin conservent le bandeau `.marketone-shop-featured-title` / `.marketone-shop-origin-title` |

### Implémentation technique (`8.5`)

Layout **flex compact** + recherche **absolument centrée** dans `_shop_grid_header.scss` :

- **Gauche** : `.marketone-shop-grid-meta` (`flex: 1 1 0`)
- **Centre** : `.o_wsale_products_header_search_form_container` (`position: absolute; left: 50%` · `width: 32rem; max-width: calc(100% - 10rem)`)
- **Droite** : `.o_sortby_dropdown` (`flex: 1 1 0; justify-content: flex-end`)
- Compteur inséré **avant** le champ recherche dans le DOM (`shop_grid_title.xml`)

---

## Prérequis

1. Module à jour :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone --stop-after-init
docker restart sandbox-odoo19-odoo-1
```

2. Hard refresh navigateur (Cmd+Shift+R / Ctrl+Shift+R).
3. Catalogue pilote : **~50 produits** publiés sur `/shop`.

---

## V0 — Organisation du haut de grille (layout `8.5`)

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Ouvrir `/shop` | Classe `marketone-shop-catalog-toolbar` sur `.products_header` | |
| 2 | **Ligne principale** | Compteur **gauche** · recherche **centre** · tri **droite** · **une seule ligne** (desktop) | |
| 3 | Compacité | Zone haute **sobre et compacte** · moins de hauteur qu'en `8.4` | |
| 4 | **Ligne secondaire** (filtres) | Chips + reset **sous** la ligne principale · au-dessus de la grille | |
| 5 | Sans filtre | Pas de ligne secondaire | |
| 6 | Style compteur | Texte discret · **pas** de cartouche / encadrement | |
| 7 | DOM | Un seul `#products_grid_content_title` · compteur **avant** le champ recherche | |

---

## V1 — Cas par défaut (aucun filtre)

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Ouvrir `/shop` sans paramètres | Pas de « Tous les produits » | |
| 2 | Indication résultat (`#products_grid_content_title`) | **`N produits disponibles`** (N = total catalogue publié) | |
| 3 | Ligne de tri | **Pas** de « produits trouvés » · **pas** de compteur doublon | |
| 4 | Barre chips | Absente | |
| 5 | Pagination (si N > page) | Compteur reste **N** (ex. 50), pas le nombre de cartes visibles | |

---

## V2 — Filtres actifs — plusieurs résultats

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Filtrer **Biscuits salés** (sidebar ou `?marketone_category=biscuits-sales-70`) | **`X produits disponibles`** (X = grille filtrée) | |
| 2 | Comparer X | X = compteur cohérent avec la grille filtrée (toutes pages) | |
| 3 | Chip catégorie | **`Biscuits salés (n)`** si n fiable · n ≤ X | |
| 4 | Ordre | Ligne résultat / tri **au-dessus** des chips | |
| 5 | Barre chips | Présente **sous** la ligne résultat / tri · **Effacer les filtres** + chip catégorie | |
| 6 | Ligne de tri | **Sans** compteur doublon | |

**Variantes recommandées** (au moins 1) :

| Filtre | URL indicatif | Chip attendue |
|--------|---------------|---------------|
| Collection sidebar | `/shop?marketone_collection=…` | `Nom collection (n)` |
| Origine sidebar | `/shop?attribute_values=…` | `Martinique (n)` |
| Recherche texte | `/shop?search=confiture` | Compteur global « disponibles » · chips sans chiffre si aucun filtre sidebar |

---

## V3 — Filtres actifs — 0 résultat

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | `/shop?search=zzzzmarketone-zero-zzzz` | Compteur **`Aucun produit disponible`** · état **`Aucun produit ne correspond à vos critères`** | |
| 2 | Combo sidebar **U9** (Biscuits salés + La Réunion + Apéritif créole) | Idem · chips `(0)` visibles | |
| 3 | Grille | Vide · pas de crash | |
| 4 | Wording interdit | **Pas** « Aucun produit défini » · **Pas** `0 produit disponible` | |

---

## V4 — Filtres actifs — 1 résultat

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Appliquer un filtre restrictif donnant **exactement 1** produit | **`1 produit disponible`** (singulier) | |
| 2 | Chip active | `(1)` possible sur la chip si fiable | |

> **Astuce recette** : affiner par catégorie très étroite + origine, ou recherche très précise (nom produit unique).

---

## V5 — Recherche texte

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | `/shop?search=miel` (ou terme avec plusieurs hits) | **`X produits disponibles`** (pas de libellé contextualisé) | |
| 2 | En-tête Odoo natif | **Pas** de « Résultats de recherche pour… » | |
| 3 | Compteur unique | Un seul `#products_grid_content_title` | |

---

## V6 — Portes catalogue (non-régression)

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | `/shop?marketone_mode=featured` | Titre porte **Incontournables** (bandeau porte) · **pas** le compteur catalogue | |
| 2 | `/shop?marketone_mode=origin` | Titre porte **Origines** · **pas** le compteur catalogue | |
| 3 | Lien « Tous les produits » sous la porte | Toujours présent · renvoie `/shop` | |

---

## V7 — Non-régression UX-1 / boutique

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Chips actives | Comportement UX-1 inchangé (retrait, reset, couleurs) | |
| 2 | Sidebar | Ordre Collections → Catégories → Origines → Prix | |
| 3 | Tri | Dropdown « Trier par » fonctionnel · aligné à droite ligne 2 | |
| 4 | Tuiles conversion | Structure tuile inchangée (photo, Voir, prix, panier) | |
| 5 | Mobile ≤ 768 px | Recherche lisible · résultat + tri en wrap acceptable · chips en wrap | |

---

## Tests automatisés

### Tag dédié (compteur + libellés + layout)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_shop_filter_state \
  --http-port=8072
```

Contrôles couverts :

- libellés singulier / pluriel / zéro (unitaires + HTTP)
- `/shop` → « produits disponibles » · classes toolbar
- filtre catégorie → « …produits disponibles » (jamais « correspondent… »)
- recherche / filtre 0 résultat → **`Aucun produit disponible`** + état central contextualisé

### Non-régression boutique

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_shop_regression \
  --http-port=8072
```

Attendu : **`0 failed, 0 error(s)`** — dont `test_ux1_chip_bar_after_toolbar_above_grid` (chips sous ligne recherche / résultat / tri).

---

## Rollback

| Niveau | Action | Effet |
|--------|--------|-------|
| **R0** | Désactiver vue `marketone_shop_grid_title` (BO → Vues) | Retour titre Odoo « Tous les produits » |
| **R1** | Revert `shop_filter_state.xml` (position chips) | Ancien ordre chips |
| **R2** | Revert commit `19.0.15.8.4` | Retour layout `8.3` (flex-wrap) |

---

## Grille verdict MOA

| Scénario | Verdict ☐ OK · ☐ réserve · ☐ KO | Notes |
|----------|----------------------------------|-------|
| V0 — Layout `8.5`/`8.6` | ☑ OK | L1 compacte · L2 chips · CSS OK |
| V1 — Défaut | ☑ OK | `50 produits disponibles` |
| V2 — Plusieurs résultats | ☑ OK | Condiments · Biscuits salés · Apéritif créole |
| V3 — 0 résultat | ☑ GO MOA | **`9.4`** — **`Aucun produit trouvé`** + **`…cette sélection`** · chips `(0)` · Effacer les filtres |
| V4 — 1 résultat | ☑ OK | Biscuits salés + Martinique |
| V5 — Recherche | ☐ | Non rejoué (libellés validés via filtres) |
| V6 — Portes | ☑ OK | Origines · pas de chip porte |
| V7 — Non-régression | ☑ OK | UX-1 · sidebar · mobile 390 px · CSS OK |

**Verdict global** : ☑ GO · ☐ GO sous réserve · ☐ KO

---

## Historique

| Date | Verdict | Note |
|------|---------|------|
| 2026-05-21 | Recette rédigée | Implémentation `19.0.15.8.2` — compteur H1 · signal MOA compteur titre principal |
| 2026-05-21 | **GO MOA** | Libellés `8.2` validés via recette UX-1 — titres observés V1–V2 · V4 · V6 · 0 réserve |
| 2026-05-21 | Recette mise à jour | Ajustement MOA `19.0.15.8.3` — recherche d'abord · compteur discret · chips sous toolbar |
| 2026-05-21 | **GO MOA maintenu** | Relance post-correction CSS `8.3` · 54 tests OK · captures régénérées |
| 2026-05-21 | Implémentation `8.4` | CSS Grid — séparation L1 recherche / L2 résultat+tri (correctif `flex-nowrap` Odoo) |
| 2026-05-21 | **GO MOA maintenu** | Relance post-code `8.4` · 54 tests OK · layout 3 lignes validé |
| 2026-05-21 | Implémentation `8.5` | Ligne compacte compteur + recherche centrée + tri · chips L2 |
| 2026-05-21 | Correctif `8.6` | Sass `min(calc())` → `width` + `max-width` — KO CSS recette corrigé |
| 2026-05-21 | **GO MOA maintenu** | Relance post-`8.6` · 54 tests OK · CSS OK · layout compact validé navigateur |
| 2026-05-21 | **`9.0`–`9.1`** | Compteur « disponibles » · chips `(n)` · sidebar · 55 tests |
| 2026-05-21 | **`9.4`** | **GO MOA wording état vide** — trouvé / cette sélection · Effacer les filtres OK |

---

## Références

| Document | Rôle |
|----------|------|
| [`RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md`](../ux/RECETTE_MANUELLE_SHOP_UX1_ETAT_FILTRES.md) | Chips / reset |
| [`RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md`](./RECETTE_MANUELLE_SHOP_CONVERSION_TILE.md) | Tuiles produit (GO MOA) |
| [`TICKET_MARKETONE_UX1_SHOP_ETAT_UTILISATEUR.md`](../../tickets/ux/TICKET_MARKETONE_UX1_SHOP_ETAT_UTILISATEUR.md) | Cadrage UX-1 initial |

---

## Signal Dev post-recette

```text
Recette haut grille /shop 19.0.15.9.3 — GO MOA maintenu — layout/chips OK — wording 9.2/9.3 documenté — rejouer V3 combo 0 résultat navigateur.
```
