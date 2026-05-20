# TICKET — Données — dédoublonnage origine `La Réunion` / `Reunion`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_ORIGINE_REUNION_DEDUP` |
| **Type** | **Données / BO** — qualité attribut Origines · zéro rustine QWeb |
| **Statut** | **Clôturé GO MOA données** — `19.0.13.1.0` · PR [#7](https://github.com/doreviateam/odoo19-addons-dorevia/pull/7) merge `632e035` |
| **Version livrée** | **`19.0.13.1.0`** |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Merge** | `fix/marketone-origin-reunion-dedup` → `main` (`632e035`) |

---

## Contexte

Sur `/shop`, la rubrique **Origines** (sidebar) peut afficher **deux entrées** pour le même territoire :

- `La Réunion`
- `Reunion`

Cela nuit à la **confiance** catalogue (données incohérentes) et fausse les futures captures **UX-2**.

**Arbitrage UX-1** : pas de masquage QWeb — correction **à la source** (valeurs d’attribut + rattachements produits / profils porte).

**Alignement existant** :

| Référence | Canon attendu |
|-----------|----------------|
| Culture V2 | Libellé visiteur **« La Réunion »** · slug **`reunion`** |
| Porte `/shop?marketone_mode=origin&marketone_origin=reunion` | `marketone.shop.origin.slug = reunion` |
| Chip UX-1 (origine) | Libellé = nom de la **valeur d’attribut** retenue |

---

## Objectif

Corriger à la source le doublon **`La Réunion` / `Reunion`** dans les valeurs de l’attribut **Origines**, de sorte que la sidebar `/shop` n’expose **qu’une seule** entrée Réunion, avec le libellé **`La Réunion`**, sans perte d’origine sur les produits ni régression des filtres / chips UX-1.

---

## Doctrine

| Règle | Détail |
|-------|--------|
| **Pas de rustine QWeb** | Aucun `t-if` / filtre template pour cacher un doublon |
| **Données d’abord** | `product.attribute` / `product.attribute.value` · lignes produit · profils `marketone.shop.origin` |
| **Migration légère** | `post_init_hook` ou script `migrate` **idempotent** si la base recette / prod contient déjà le doublon |
| **Reproductibilité** | Données XML / hook pour bases neuves **si** le doublon est aussi dans le dépôt |

---

## Périmètre

### In

1. **Inventaire** des valeurs de l’attribut **Origines** (`product.attribute` Marketone).
2. **Identification** des enregistrements doublons `La Réunion` / `Reunion` (et variantes de casse / espaces si présentes).
3. **Canonique retenu** :
   - **Libellé affiché** : `La Réunion`
   - **Slug / logique technique** : inchangé — compatible `marketone_origin=reunion` (profil `marketone.shop.origin` + URLs Culture / porte Origines).
4. **Réaffectation** :
   - `product.template.attribute.value` / variantes liées → valeur canonique ;
   - `marketone.shop.origin.attribute_value_id` → valeur canonique si un profil pointe le doublon.
5. **Suppression ou archivage** de la valeur doublon (après fusion, sans orphelins).
6. **Vérifications** :
   - Sidebar `/shop` : **une seule** entrée Réunion ;
   - Filtre Origines (URL `attribute_values`) : comportement inchangé ;
   - Chip UX-1 : libellé **La Réunion** lorsque l’origine est active.

### Hors périmètre

| Hors scope | Lot |
|------------|-----|
| UX-2 (densité sidebar, accordéons, espacements, zones cliquables) | UX-2 |
| Refonte facettes / modèle Origines | — |
| C4 catégories sidebar | — |
| `remove_url` / reset / logique chips UX-1 | UX-1 (gelé) |
| Savoirs · `shop_ppg` | — |
| Harmonisation **autres** origines (Martinique, Guadeloupe, etc.) sauf si doublon strictement identique détecté au même audit | Ticket séparé |

---

## Analyse technique (indicative)

### Modèles concernés

| Modèle | Rôle |
|--------|------|
| `product.attribute` | Attribut **Origines** (`marketone_product_attribute_origin`) |
| `product.attribute.value` | Valeurs affichées sidebar + chips |
| `product.template.attribute.line` / valeurs produit | Rattachement origine sur fiches produit |
| `marketone.shop.origin` | Profil porte · `slug` **`reunion`** · `attribute_value_id` |

### Pistes d’implémentation (après GO ticket)

1. **Audit SQL / shell** sur `ckr-marketone-01` :
   - lister `product.attribute.value` pour l’attribut Origines ;
   - compter produits par valeur ;
   - lister profils `marketone.shop.origin` par `attribute_value_id`.
2. **Fusion** : conserver l’ID de la valeur canonique **`La Réunion`** (ou migrer vers elle), réécrire les FK, puis `unlink` / archiver le doublon **`Reunion`**.
3. **Hook post_init** (idempotent) pour bases déjà peuplées + garde si une seule valeur existe déjà.
4. **Tests** : test données ou HTTP léger — sidebar ne contient qu’un libellé Réunion · filtre + chip cohérents.

> **Ne pas** renommer le slug `reunion` sur `marketone.shop.origin` — seul le libellé **valeur d’attribut** / visiteur est harmonisé.

---

## Critères GO MOA

| # | Critère | Méthode |
|---|---------|---------|
| G1 | **Une seule** valeur Réunion visible dans la sidebar Origines | Recette manuelle `/shop` |
| G2 | Libellé affiché : **`La Réunion`** | Sidebar + chip UX-1 |
| G3 | **Aucun produit** ne perd son origine Réunion | Échantillon produits + compteur `/shop` filtré |
| G4 | Filtre Origines fonctionne (`attribute_values`, porte `marketone_origin=reunion`) | Clic sidebar · URL · grille |
| G5 | Chip UX-1 affiche **`La Réunion`** (pas `Reunion`) | Combinaison avec autre filtre |
| G6 | Tests existants **non régressés** | `dorevia_marketone_shop_sidebar` · `dorevia_marketone_shop_filter_state` · `dorevia_marketone_shop_regression` · `test_marketone_culture_v2` (reunion) |

**Réserve non bloquante** : autres doublons d’orthographe sur origines → ticket dédié si audit en révèle.

---

## Recette manuelle express (≤ 10 min)

| Étape | Action | Attendu |
|-------|--------|---------|
| R1 | Ouvrir `/shop` · déplier **Origines** | Une seule ligne **La Réunion** (pas `Reunion`) |
| R2 | Cocher **La Réunion** | Grille filtrée · chip UX-1 **La Réunion** |
| R3 | Ouvrir `/shop?marketone_mode=origin&marketone_origin=reunion` | **200** · pas de doublon sidebar |
| R4 | BO — fiche produit avec origine Réunion | Origine toujours renseignée (valeur canonique) |
| R5 | Upgrade module + restart | Pas d’erreur · R1–R3 toujours OK |

---

## Tests auto (cible)

```bash
odoo-bin -d ckr-marketone-01 \
  --test-tags=dorevia_marketone_shop_sidebar,dorevia_marketone_shop_filter_state,dorevia_marketone_shop_regression \
  --stop-after-init

odoo-bin -d ckr-marketone-01 \
  --test-tags=dorevia_marketone_culture_v2 \
  --stop-after-init
```

Test dédié recommandé (après implémentation) : tag `dorevia_marketone_origin_reunion_dedup` — une seule valeur Réunion sur l’attribut Origines.

---

## Découpage proposé (après GO ticket)

| Étape | Livrable |
|-------|----------|
| **D1** | Script d’audit documenté (requête / shell) |
| **D2** | Migration / hook idempotent + données si besoin |
| **D3** | Test + recette · version `19.0.13.1.0` |

**Estimation** : ½ journée si doublon isolé sur `ckr-marketone-01`.

---

## Enchaînement produit

| Ordre | Lot |
|-------|-----|
| 1 | **Ce ticket** — confiance données Origines |
| 2 | **UX-2** — captures sidebar sur base propre |
| 3 | **UX-3** — images produits |

---

## Références

| Document | Lien |
|----------|------|
| UX-1 (hors scope doublon QWeb) | [`TICKET_MARKETONE_UX1_SHOP_ETAT_UTILISATEUR.md`](../ux/TICKET_MARKETONE_UX1_SHOP_ETAT_UTILISATEUR.md) |
| Culture V2 — La Réunion | [`RECETTE_MANUELLE_CULTURE_V2.md`](../../recette/culture/RECETTE_MANUELLE_CULTURE_V2.md) |
| Porte Origines | [`TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES.md`](../lots/TICKET_MARKETONE_LOT6_2_PORTE_ORIGINES.md) |
| Attribut Origines (data) | [`data/marketone_product_attribute_origin.xml`](../../data/marketone_product_attribute_origin.xml) |
| Profil `marketone.shop.origin` | [`models/marketone_shop_origin.py`](../../models/marketone_shop_origin.py) |

---

## Verdict ticket

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-05-19 | **Brouillon — attente GO MOA ticket** | Ticket rédigé · **aucun code** avant validation |
| 2026-05-19 | **GO MOA exécution** | Audit `ckr-marketone-01` · fusion 68→51 · hook + migration · recette dédiée |
| 2026-05-19 | **Clôturé GO MOA données** | PR #7 mergée · post-merge R1–R3 OK · 7/7 produits sur `La Réunion` id 51 · profil `reunion` aligné · chip UX-1 OK · aucun `views/` modifié |
