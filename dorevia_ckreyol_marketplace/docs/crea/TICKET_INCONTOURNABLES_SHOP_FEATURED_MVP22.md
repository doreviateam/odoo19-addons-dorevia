# Ticket dev — Porte Incontournables / `featured`

| Champ | Valeur |
|--------|--------|
| **Périmètre** | MVP2.2 Boutique — porte **Incontournables** (`ckr_mode=featured`) |
| **Statut ticket** | Prêt **chiffrage** puis implémentation |
| **Cadrage MOA** | [2_SHOP.md](../mvp_02/2_SHOP.md) ; contrat technique [SPEC_SHOP_PORTES.md §4.6](../mvp_01/SPEC_SHOP_PORTES.md) |
| **Date** | 2026-04-25 |

**Chaîne documentaire** (exploitable par dev ou PO, sans dérive « maquette seule » ni spec sans ticket opérationnel) :

```text
2_SHOP.md
→ cadrage UX / doctrine MOA

SPEC_SHOP_PORTES.md §4.6
→ contrat porte Incontournables / featured

docs/crea/TICKET_INCONTOURNABLES_SHOP_FEATURED_MVP22.md
→ ticket chiffrable et exécutable
```

**Statut** : le sujet **Incontournables / `featured`** est prêt pour :

1. **Chiffrage**
2. **Création de branche**
3. **Implémentation**
4. **Tests HTTP + non-régression**
5. **PR** avec preuve de réutilisation de la mécanique collection (voir § *Règle de conduite — pull request*)

**Règle d’or du lot** :

```text
featured expose une collection configurée ; il ne crée pas une nouvelle logique catalogue.
```

**Conventions Git** *(proposition)* :

| Élément | Valeur |
|---------|--------|
| **Branche** | `feature/shop-featured-incontournables` |
| **Commit de départ** *(message type)* | `feat(shop): add featured entry point for incontournables` |

---

## Objectif

Implémenter la porte commerciale **Incontournables**, correspondant à une **sélection éditoriale manuelle** de produits, **sans dupliquer** la logique métier des collections.

La porte doit s’appuyer sur une **`ckr.shop.collection`** existante, configurée via le paramètre :

`dorevia_ckreyol_marketplace.featured_collection_id`

---

## Rappel doctrine

- Libellé visiteur : **Incontournables**
- URL courte : `/incontournables`
- URL canonique : `/shop?ckr_mode=featured`
- Source BO : collection éditoriale existante
- **Interdit** : `best_sellers`, `top_sales`, ou toute logique statistique sans calcul réel documenté
- **Interdit** : recoder une mécanique de sélection **parallèle** aux collections (voir *Note vigilance (dev)* en **SPEC_SHOP_PORTES** §4.6)

---

## Lots dev

### Lot 1 — Route / contrôleur

- Ajouter la route courte `/incontournables`
- Rediriger en **301** vers `/shop?ckr_mode=featured`
- Ajouter **`featured`** à la whitelist des `ckr_mode`
- Préserver les comportements existants des portes `pack`, `promo`, `origin`, `collection`

### Lot 2 — Domaine produit

- Lire le paramètre `dorevia_ckreyol_marketplace.featured_collection_id`
- Vérifier que la collection existe et est **active**
- **Réutiliser** la logique collection existante pour récupérer les produits
- **Ne pas** créer de nouvelle mécanique de sélection produit
- Prévoir **fallback** si paramètre absent, invalide ou collection inactive

### Lot 3 — SEO / canonical

- `/incontournables` redirige en **301** vers `/shop?ckr_mode=featured`
- `/shop?ckr_mode=featured` expose un **canonical** cohérent
- **Ne pas** créer de canonical contradictoire avec les autres portes

### Lot 4 — Bandeau contextuel

- Ajouter le contexte bandeau pour **Incontournables**
- Titre recommandé : `Incontournables`
- Micro-copy possible : *Une sélection de produits mis en avant par C-Kreyol pour découvrir les essentiels de la boutique.*
- Image / fallback selon règles MVP2.2 ([2_SHOP.md](../mvp_02/2_SHOP.md) §3)

### Lot 5 — Chip / raccourci commercial

- Ajouter la chip **Incontournables**
- État actif si `ckr_mode=featured`
- **Ne pas** utiliser le libellé « Meilleures ventes »
- Préserver les chips existantes Promotions / Kits si déjà prévues

### Lot 6 — Tests HTTP + non-régression

Couvrir au minimum :

- `/incontournables` → **301** vers `/shop?ckr_mode=featured`
- `/shop?ckr_mode=featured` retourne **200** si collection valide
- **fallback** propre si paramètre absent / invalide / collection inactive
- **canonical** présent et cohérent
- chip Incontournables **active** dans le bon contexte
- priorité multi-modes respectée : `pack > promo > featured > origin > collection`
- **non-régression** sur Promotions, Kits, Origines, Collections

---

## Critères d’acceptation

- La porte **Incontournables** est accessible via `/incontournables`
- L’URL courte redirige correctement vers `/shop?ckr_mode=featured`
- La grille affiche les produits de la collection configurée
- Aucun mécanisme métier **parallèle** aux collections n’est créé
- Le bandeau affiche le contexte Incontournables
- La chip Incontournables est visible et active dans le bon contexte
- Le fallback est propre si la collection n’est pas configurée
- Les tests HTTP passent
- Les portes existantes ne régressent pas

---

## Chiffrage dev — Porte Incontournables / `featured`

**Estimer** (effort / risque / dépendances) les lots suivants :

1. Route / contrôleur  
2. Domaine produit via collection existante  
3. SEO / canonical  
4. Bandeau contextuel  
5. Chip Incontournables  
6. Tests HTTP + non-régression  

**Arbitrages à traiter au chiffrage** (ou en tout début d’implémentation) :

- **Fallback** exact si collection absente / invalide / inactive (retour `/shop`, état vide dédié, message discret, etc.) ;
- Lien **Explorer** homepage vers `/incontournables` dès **V1** ou **V1.1** ;
- **Image** spécifique bandeau ou **fallback** générique boutique (cf. [2_SHOP.md](../mvp_02/2_SHOP.md) §3) ;
- **Paramètre système** simple (`ir.config_parameter`) ou **interface BO** dédiée pour `featured_collection_id`.

---

## Règle de conduite — pull request

La **PR** doit **démontrer** (description + revue + tests) que **`ckr_mode=featured`** **réutilise** la mécanique **collection** existante (`ckr.shop.collection`, filtre catalogue aligné porte Collections) et **ne crée pas** une seconde logique de sélection produit parallèle. Réf. *Note vigilance (dev)* — [SPEC_SHOP_PORTES.md §4.6](../mvp_01/SPEC_SHOP_PORTES.md).

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-04-25 | Création du ticket à partir du cadrage **2_SHOP.md** + **SPEC_SHOP_PORTES** §4.6. |
| 2026-04-25 | Ajout **chaîne documentaire**, section **Chiffrage dev**, **règle de conduite PR**. |
| 2026-04-25 | **Prêt pour** (chiffrage → branche → impl. → tests → PR) ; **règle d’or du lot** ; **conventions Git** (branche + commit type). |
