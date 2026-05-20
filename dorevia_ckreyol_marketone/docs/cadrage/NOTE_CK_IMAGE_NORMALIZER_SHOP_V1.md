# Note de cadrage — CK Image Normalizer V1 (tuiles commerce `/shop`)

| Champ | Valeur |
|-------|--------|
| **Statut** | **GO MOA POC** — arbitrages validés · ticket POC ouvert |
| **Date** | 2026-05-20 |
| **ADR** | [ADR-033](./DECISIONS.md#adr-033--ck-image-normalizer-v1--poc-tuiles-commerce-shop) |
| **Ticket POC** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md`](../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md) |
| **Type** | Cadrage / faisabilité — **pas d’implémentation immédiate** |
| **Périmètre** | Tuiles commerce grille `/shop` uniquement |
| **Module** | `dorevia_ckreyol_marketone` |
| **Références** | [ADR-002](./DECISIONS.md#adr-002--website_sale-moteur-unique) · [ADR-031 UX-3](./DECISIONS.md#adr-031--ux-3-palier-a-grille-produit-shop) · [`NOTE_CK_IMAGE_NORMALIZER_VISION_MOA.md`](./NOTE_CK_IMAGE_NORMALIZER_VISION_MOA.md) · [`RECETTE_MANUELLE_SHOP_UX3_PRODUCT_CARDS.md`](../recette/ux/RECETTE_MANUELLE_SHOP_UX3_PRODUCT_CARDS.md) · [`TICKET_MARKETONE_UX3_PALIER_A_PROPOSITION_DA.md`](../tickets/ux/TICKET_MARKETONE_UX3_PALIER_A_PROPOSITION_DA.md) |

---

## Enjeu produit (MOA)

> Le moteur image sert à transformer des sources vendeurs hétérogènes en visuels commerce contrôlés, sans faire porter toute la charge à l’humain, et sans dégrader la qualité de la boutique.

Vision complète : [`NOTE_CK_IMAGE_NORMALIZER_VISION_MOA.md`](./NOTE_CK_IMAGE_NORMALIZER_VISION_MOA.md).

---

## Synthèse exécutive

| Question | Réponse |
|----------|---------|
| **Opportunité** | **Oui** — le CSS UX-3 a atteint son plafond ; la normalisation média répond à une lacune documentée |
| **Faisabilité V1 sans IA** | **Oui**, avec limites explicites sur lifestyle et fonds complexes |
| **Périmètre V1 proposé** | **Validé** — tuiles `/shop` uniquement, pas de BO Odoo complet |
| **Effort V1 utile** | **~7–12 j/h dev** (POC externe + calibrage + industrialisation légère) |
| **Séquence recommandée** | Outil externe d’abord → recette MOA → pilote catalogue → intégration Odoo lite (V1.5) |
| **Verdict** | **Lancer le chantier**, avec prudence et phasage |

> Ce chantier peut devenir une brique structurante pour la qualité catalogue CK. Il ne s’agit pas d’un simple script de redimensionnement, mais d’un **moteur média à recette fixe**.

---

## 1. Contexte

### 1.1 État visuel actuel de `/shop`

La page `/shop` a retrouvé une base visuelle sobre et premium (UX-3 Palier B1) :

- body blanc / très neutre ;
- sidebar discrète ;
- cartes produits lisibles ;
- zone image légèrement réchauffée en `#F8EEDB` ;
- pas de dégradé ;
- pas d’aplats lourds ;
- ligne e-commerce plus propre.

Mais l’harmonie de la grille reste **fortement dépendante de la qualité des images produits**.

### 1.2 Hétérogénéité des sources

Aujourd’hui, les images peuvent varier fortement :

- formats différents ;
- cadrages différents ;
- produits trop petits ou trop grands ;
- fonds hétérogènes ;
- marges irrégulières ;
- niveaux de zoom différents ;
- compression variable ;
- packshots et images lifestyle mélangés.

Le CSS peut encadrer la grille, mais il **ne peut pas corriger durablement** l’hétérogénéité des visuels sources.

### 1.3 État technique Marketone

Le socle actuel est cohérent et **volontairement incomplet côté média** :

| Élément | État actuel |
|---------|-------------|
| Tuiles produit | **Natives Odoo 19** (`website_sale.products_item`) — aucun héritage QWeb image dans Marketone |
| Style tuiles | SCSS via `--o-wsale-card-*` dans `_shop_product_cards.scss` |
| Ratio | **1:1** (`--o-wsale-card-thumb-aspect-ratio: 1`) |
| `object-fit` | **`contain`** (produit non rogné) |
| Fond zone image | **`#F8EEDB`** (`$ck-bg-image`) |
| Fond corps carte | **`#FDF9F0`** (`$ck-bg-card-body`) |
| Champ image produit | **`product.template.image_1920`** standard (+ dérivés Odoo `image_512`, `image_1024`…) |
| Pipeline normalisation | **Aucun** |

Référence code :

```scss
// static/src/scss/_shop_product_cards.scss
--o-wsale-card-thumb-background:     #{$ck-bg-image};   // #F8EEDB
--o-wsale-card-thumb-aspect-ratio:   1;
--o-wsale-card-thumb-fill-mode:      contain;
```

La doctrine le reconnaît explicitement (ADR-031, réserve non bloquante n°3) :

> *Homogénéisation durable visuels = futur moteur normalisation images*

Le ticket UX-3 Palier A classe également le pipeline image normalisé comme **hors périmètre SCSS** (*« sujet contenu / média, pas CSS seul »*).

---

## 2. Enjeu produit / stratégique

La qualité des visuels produits influence directement la perception de la boutique.

Pour C-Kreyol / Marketone, la grille `/shop` doit porter une ligne :

- premium ;
- lisible ;
- chaleureuse ;
- cohérente ;
- orientée achat ;
- compatible avec des produits créoles très variés.

Les produits peuvent venir de fournisseurs différents, avec des photos de qualités, cadrages et fonds très hétérogènes.

Sans normalisation, le CSS compense partiellement, mais la grille reste fragile.

Le moteur image viserait à traiter le problème **à la source** :

> Produire des visuels de tuiles commerce homogènes avant affichage, pour que la grille `/shop` tienne naturellement.

### 2.1 Ce que le CSS ne corrige pas

| Problème | Cause actuelle | Limite CSS |
|----------|----------------|------------|
| Halos blancs sur packshots | `mix-blend-mode: multiply` retiré (décision UX-3) | Pas de correction fond transparent |
| Ratios hétérogènes | `contain` dans carré 1:1 | Letterboxing variable, densité visuelle inégale |
| Fonds sources mixtes | Pas de normalisation à l’upload | Harmonisation couleur / cadrage impossible |
| Couture image / zone texte | Deux aplats (`#F8EEDB` vs `#FDF9F0`) + filet inset | Unifier en amont ou fond image intégré au fichier |
| Poids visuel inégal | Pas de règle métier sur dimensions source | Pas de scale/crop/padding canonique |
| Packshot vs lifestyle | Un seul `image_1920` | Pas de variante listing dédiée |

---

## 3. Périmètre V1 — Tuiles commerce

La V1 du moteur est concentrée sur les images destinées aux **tuiles commerce** de la grille `/shop`.

### 3.1 Objectif principal

> Produire des visuels carrés, homogènes, lisibles et premium pour les cartes produit e-commerce.

La V1 ne cherche pas encore à couvrir tous les usages image de C-Kreyol.

### 3.2 Inclus V1

| Élément | Détail |
|---------|--------|
| Usage | Image carte produit `/shop` uniquement |
| Format | Carré **1024 × 1024 px** |
| Cadrage | Produit centré |
| Poids visuel | Homogène (règle de fill ratio) |
| Fond | Harmonisé **`#F8EEDB`** (intégré au fichier) |
| Export principal | **WebP** |
| Export fallback | **JPEG** |
| Original | **Conservé** (archive séparée) |
| Traçabilité | **Rapport de traitement** par batch |
| Validation | **Recette** testée sur grille `/shop` réelle |

### 3.3 Hors périmètre V1

- image hero ;
- image éditoriale ;
- image culture ;
- image recette ;
- image blog ;
- image fiche produit enrichie ;
- image mobile dédiée ;
- image collection commerciale ;
- image origine ;
- image bannière ;
- image lifestyle avancée ;
- détourage complexe ;
- IA générative ;
- intégration complète BO Odoo.

### 3.4 Principe directeur

La V1 doit résoudre un problème précis :

> Homogénéiser les tuiles commerce pour que la grille `/shop` soit plus cohérente, plus premium et plus lisible.

Les autres usages image pourront être traités ensuite dans une V2 ou dans des moteurs spécialisés.

---

## 4. Cible visuelle

### 4.1 Une tuile commerce CK doit être

- carrée ;
- nette ;
- centrée ;
- chaude sans excès ;
- premium ;
- lisible en petite taille ;
- cohérente avec les autres produits ;
- adaptée à une grille e-commerce.

### 4.2 Elle ne doit pas produire

- un rendu catalogue industriel froid ;
- un effet IA visible ;
- un détourage agressif ;
- un produit coupé ;
- un produit perdu dans le cadre ;
- un fond trop présent ;
- une compression visible ;
- une perte de texture produit.

### 4.3 Recette de cadrage proposée (V1)

```yaml
recipe_id: ck_shop_tile_v1
canvas_size: 1024
ratio: "1:1"
width: 1024
height: 1024
background: "#F8EEDB"
color_space: "sRGB"

# Poids visuel — produit occupe ~78 % de la surface utile
content_fill_ratio: 0.78
min_padding_px: 64
max_padding_px: 128

# Pré-traitement
trim_uniform_border: true
white_background_replace: true      # profil packshot uniquement
white_threshold: 245                # tolérance fond clair (0-255)

# Profils source
profiles:
  packshot:
    white_background_replace: true
    content_fill_ratio: 0.78
  lifestyle:
    white_background_replace: false
    content_fill_ratio: 0.72

# Export
output:
  webp: { quality: 85 }
  jpeg: { quality: 90 }

# Rejet automatique (heuristiques)
reject_if:
  - content_area_ratio < 0.15       # produit trop petit dans source
  - content_area_ratio > 0.95       # plein cadre / risque crop
  - background_entropy > 0.42       # fond trop complexe (heuristique)

# Statuts rapport
statuses:
  - OK
  - OK_WITH_WARNINGS
  - NEEDS_REVIEW
  - REJECTED
```

> **Arbitrage MOA (2026-05-20)** : fond `#F8EEDB` **baked-in à tester dans le POC** — soumis à recette visuelle MOA (critère G6).

---

## 4.4 Arbitrages MOA (2026-05-20)

| # | Décision MOA |
|---|--------------|
| **M1** | **GO POC** — pas d’implémentation Odoo en V1 |
| **M2** | Périmètre strict : tuiles commerce `/shop` |
| **M3** | Séquence validée : POC CLI → recette MOA → pilote → V1.5 Odoo lite après validation |
| **M4** | Fond `#F8EEDB` baked-in à tester dans le POC |
| **M5** | Ne jamais remplacer `image_1920` — dérivés + rapport uniquement |
| **M6** | Échantillon **21 références** catalogue disponible (révision MOA 2026-05-20, initialement 30) |
| **M7** | Recette `ck_shop_tile_v1` validée (voir §4.3) |

---

## 5. Faisabilité technique

### 5.1 Verdict global

**Faisable sans IA**, avec des limites explicites sur les sources lifestyle et fonds complexes.

### 5.2 Matrice de faisabilité V1

| Étape | Faisabilité | Commentaire |
|-------|-------------|-------------|
| Canvas carré 1024×1024 | ✅ Trivial | Aligné avec dérivés Odoo |
| Fond `#F8EEDB` intégré | ✅ Trivial | Améliore couture image/texte |
| Centrage + marge homogène | ✅ Faisable | Règle de **fill ratio** |
| Trim bordures uniformes | ✅ Faisable | Détection couleur coins + crop |
| Remplacement fond blanc / quasi-blanc | ⚠️ Partiel | Bon sur packshots ; fragile sur lifestyle |
| Export WebP + JPEG | ✅ Trivial | |
| Conservation original | ✅ Trivial | Dossier / champ séparé |
| Rapport de traitement | ✅ Recommandé | Indispensable pour contrôle qualité |
| Détourage complexe | ❌ Hors V1 | Comme prévu |
| IA générative / segmentation | ❌ Hors V1 | Comme prévu |

### 5.3 Ce que la V1 peut réellement normaliser

| Type de source | ROI attendu | Fiabilité auto |
|----------------|-------------|----------------|
| Packshots fond blanc / gris clair | **Très élevé** | 80–90 % |
| Images propres mais mal cadrées | **Élevé** | 85–95 % |
| Lifestyle fond neutre | **Moyen** | 50–70 % (relecture humaine) |
| Scènes chargées, ombres, reflets, multi-produits | **Faible** | < 30 % — flag `NEEDS_REVIEW` ou `REJECTED` |

### 5.4 Estimation honnête catalogue hétérogène

Sur un catalogue CK typique (mix fournisseurs) :

| Catégorie | Proportion estimée |
|-----------|-------------------|
| Traitement auto satisfaisant | **60–75 %** |
| Retouches manuelles légères | **15–25 %** |
| Refus / reprise photo | **5–15 %** |

Ce ratio dépend surtout de la **qualité des sources fournisseurs**, pas de la qualité du code.

### 5.5 Algorithme V1 recommandé (sans IA)

1. Charger l’image source.
2. Détecter le profil (`packshot` vs `lifestyle`) — heuristique ou tag manuel en V1.
3. Trim des bordures uniformes (couleur des 4 coins).
4. *(Profil packshot)* Remplacer fond blanc/quasi-blanc par `#F8EEDB`.
5. Calculer la bounding box du contenu (seuil luminance / alpha).
6. Redimensionner pour atteindre le `content_fill_ratio` cible.
7. Centrer sur canvas 1024×1024 fond `#F8EEDB`.
8. Export WebP (q=85) + JPEG (q=90).
9. Générer entrée rapport avec statut, métriques, vignette comparatif.

**Stack suggérée** : Python 3 + Pillow (aligné écosystème Odoo). Optionnel : `opencv-python` pour heuristiques fond — **sans** modèles IA (`rembg`, segmentation, etc.).

---

## 6. Niveau d’effort

| Phase | Contenu | Effort estimé |
|-------|---------|---------------|
| **A — POC recette externe** | CLI batch, 2 profils, rapport JSON/CSV, échantillon **21 images** | **3–5 j/h** |
| **B — Calibrage MOA** | Itérations recette, grille comparatif avant/après, arbitrage fill ratio | **2–4 j/h** (dont MOA) |
| **C — Industrialisation légère** | Watch folder, nommage, doc opérateur, rejeu catalogue pilote | **2–3 j/h** |
| **D — Intégration Odoo minimale (V1.5)** | Champ `image_shop_tile`, cron/on_write, branchement tuile (héritage QWeb) | **5–8 j/h** |
| **E — BO complet + audit + retraitement** | UI, historique, comparaison, permissions | **8–12 j/h** (V2) |

**V1 recommandée = phases A + B + C ≈ 7–12 j/h dev**, hors temps MOA et hors reprise manuelle des images rejetées.

C’est un effort **modéré mais structurant** — proportionné à l’enjeu, à condition de ne pas viser l’intégration Odoo complète dès le départ.

---

## 7. Risques qualité

| Risque | Gravité | Mitigation V1 |
|--------|---------|---------------|
| Produit trop petit dans la tuile | **Haute** | `content_fill_ratio` + rejet si sous-seuil |
| Produit coupé (trim agressif) | **Haute** | Trim conservateur ; pas de crop « intelligent » |
| Halo autour du packshot | **Moyenne** | Remplacement fond + fond `#F8EEDB` baked-in |
| Dégradation texture (épices, tissu) | **Moyenne** | WebP q≥85, pas de sharpen agressif |
| Lifestyle « aplati » ou sale | **Haute** | Profil lifestyle sans replace bg ; flag `NEEDS_REVIEW` |
| Incohérence packshot vs lifestyle | **Moyenne** | Acceptable en V1 si poids visuel homogène ; V2 = séparation champs |
| Sur-compression mobile | **Faible** | Tester à ~320 px d’affichage (taille tuile réelle) |
| Dérive couleur `#F8EEDB` | **Faible** | sRGB explicite, pas de profil exotique |
| Catalogue uniformément dégradé | **Haute** | Pas de cron massif sans validation MOA ; rapport obligatoire |

---

## 8. Outil externe avant Odoo — pertinence

### 8.1 Recommandation

**Oui — c’est la bonne séquence.** Valider la recette hors Odoo avant toute brique module.

### 8.2 Raisons

- La difficulté principale est **visuelle / métier** (recette, seuils, profils), pas Odoo.
- Itérer une recette dans un module Odoo coûte plus cher (déploiement, upgrade, tests régression).
- Le CLI externe devient le **contrat** du futur module (`recipe ck_shop_tile_v1`).
- Gain réel sur `/shop` vérifiable en réinjectant manuellement 20 produits avant d’écrire du Python Odoo.

### 8.3 Livrables V1 externe

```text
input/              → originaux
output/webp/        → tuiles normalisées WebP
output/jpeg/        → tuiles normalisées JPEG (fallback)
archive/orig/       → copie horodatée des originaux
reports/            → JSON + CSV + vignettes comparatif avant/après
```

### 8.4 Outils à éviter en V1

| Outil / approche | Verdict |
|------------------|---------|
| `rembg` / modèles segmentation | ❌ Contradictoire avec cadrage « sans IA » |
| Remplacement `image_1920` sans archive | ❌ Perte du master |
| SaaS type Cloudinary (auto-bg) | ⚠️ Surdimensionné pour V1 ; à réévaluer en V2 |
| BO Odoo complet dès le départ | ❌ Trop tôt |

---

## 9. Trajectoire vers une brique réutilisable

### 9.1 Architecture cible

```text
┌─────────────────────────────────────────────────────────────┐
│  V1 externe                                                 │
│  Sources → CLI ck_image_normalizer → WebP/JPEG + Rapport   │
└──────────────────────────┬──────────────────────────────────┘
                           │ recette validée MOA
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  V1.5 Odoo lite                                             │
│  image_shop_tile + héritage QWeb tuile /shop               │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  V2 réutilisable                                            │
│  Module dorevia_ck_media (ou ck_image_normalizer)          │
│  Recettes versionnées · batch · on_write · BO audit        │
└─────────────────────────────────────────────────────────────┘
```

### 9.2 Principes de réutilisabilité

- Moteur **agnostique Odoo** (lib Python pure).
- Recettes **versionnées** (`ck_shop_tile_v1`, futur `ck_product_hero_v1`, etc.).
- Séparation **original / dérivé usage** (ne jamais remplacer le master sans archive).
- Module Odoo futur = **orchestrateur**, pas logique image.

### 9.3 Cohérence avec ADR-002

Marketone conserve `website_sale` comme moteur unique. L’intégration V1.5 se limite à :

- un champ binaire dédié sur `product.template` ;
- un héritage QWeb minimal sur `products_item` ;
- **pas** de route e-commerce parallèle ni de moteur catalogue séparé.

---

## 10. Intégration Odoo — ce qu’il ne faut pas faire en V1

| Approche | Verdict | Raison |
|----------|---------|--------|
| Remplacer `image_1920` par la tuile normalisée | ❌ | Perte master, régression fiche produit |
| Cron massif sans validation MOA | ❌ | Risque catalogue uniformément dégradé |
| BO complet avec preview live | ⏳ V2 | Complexité prématurée |
| `<picture>` WebP custom sans mesure perf | ⚠️ | Odoo sert déjà `/web/image` ; WebP utile surtout si CDN / statique |

### 10.1 V1.5 minimale (post-validation recette)

| Élément | Détail |
|---------|--------|
| Champ | `image_shop_tile` (+ `shop_tile_recipe_version`, `shop_tile_processed_at`, `shop_tile_status`) |
| QWeb | Tuile `/shop` → `image_shop_tile` si présent, sinon fallback `image_512` |
| Hors scope | Galerie fiche produit, hero, collections |

---

## 11. Ajustements recommandés au cadrage initial

| Point | Recommandation Dev |
|-------|-------------------|
| Écrasement `image_1920` | **Ne pas** en V1 — produire fichiers + rapport, upload manuel ou semi-auto |
| Recette versionnée | YAML/JSON `ck_shop_tile_v1` — contrat stable |
| Statuts rapport | `OK` / `OK_WITH_WARNINGS` / `NEEDS_REVIEW` / `REJECTED` |
| Profils source | `packshot` + `lifestyle` dès V1 (sans élargir le périmètre fonctionnel) |
| Échantillon MOA | **21 produits** catalogue disponible (révision MOA 2026-05-20, initialement 20–30) |
| Fond baked-in | **Recommandé** — améliore couture `#F8EEDB` / `#FDF9F0` |

---

## 12. Critères GO / NO-GO

### 12.1 GO si

- MOA valide un **gain visuel net** sur grille 4 colonnes desktop **et** 2 colonnes mobile ;
- ≥ **60 %** de l’échantillon pilote passe en `OK` sans retouche ;
- la recette est **stable** (mêmes paramètres, résultats reproductibles) ;
- process opérationnel défini (qui traite les `NEEDS_REVIEW` ?).

### 12.2 NO-GO / pause si

- le catalogue source est majoritairement lifestyle fond complexe ;
- MOA exige un rendu « studio packshot » uniforme sans budget reprise photo ;
- on cherche à compenser un CSS pas encore stabilisé *(non applicable — UX-3 B1 est GO)*.

---

## 13. Prochaine étape proposée (sans implémentation)

Si le cadrage est validé MOA, ouvrir un **ticket POC** (dans `docs/tickets/`) avec :

1. Échantillon de **21 références produit** (catalogue disponible).
2. Spec recette complète (`ck_shop_tile_v1` — voir §4.3).
3. Grille de notation MOA :

   | Critère | Échelle |
   |---------|---------|
   | Lisibilité en petite taille | 1–5 |
   | Chaleur / premium CK | 1–5 |
   | Cohérence grille | 1–5 |
   | Absence d’effet IA / détourage agressif | 1–5 |
   | Préservation texture produit | 1–5 |

4. Seuils d’acceptation batch : `OK` ≥ 60 %, `REJECTED` ≤ 10 %.
5. Arbitrage MOA : fond baked-in `#F8EEDB` vs fond CSS.

---

## 14. Décision Dev — synthèse

| Décision | Recommandation |
|----------|----------------|
| Lancer le chantier ? | **Oui**, avec prudence et phasage |
| Périmètre V1 | **Validé** — tuiles `/shop` uniquement |
| Séquence | **1)** POC CLI → **2)** recette MOA → **3)** pilote 50–100 SKU → **4)** V1.5 Odoo |
| Effort V1 utile | **~7–12 j/h dev** + MOA |
| Intégration Odoo immédiate | **Non** — attendre validation recette |
| Ambition réaliste sans IA | **Homogénéisation « premium pragmatique »**, pas rendu studio parfait |

---

## 15. Références croisées

| Document | Lien |
|----------|------|
| Style tuiles actuel | `static/src/scss/_shop_product_cards.scss` |
| Token fond image | `static/src/scss/_tokens_colors.scss` (`$ck-bg-image: #F8EEDB`) |
| Réserve ADR UX-3 | `cadrage/DECISIONS.md` — ADR-031, réserve (3) |
| Proposition DA UX-3 | `docs/tickets/ux/TICKET_MARKETONE_UX3_PALIER_A_PROPOSITION_DA.md` § Pipeline image |
| Recette UX-3 | `docs/recette/ux/RECETTE_MANUELLE_SHOP_UX3_PRODUCT_CARDS.md` |
| Banque visuelle recette | `docs/recette/reference/ASSETS_REFERENCE.md` |
| Architecture module | `cadrage/ARCHITECTURE.md` |
| Contrats | `cadrage/CONTRACTS.md` — C1 (`website_sale` moteur unique) |

---

## Historique

| Date | Auteur | Action |
|------|--------|--------|
| 2026-05-20 | Dev | Rédaction avis technique initial |
| 2026-05-20 | MOA | **GO POC avec réserves** — clôture POC · doc opérateur livrée |
| 2026-05-20 | MOA | Échantillon POC ramené à **21 refs** (révision depuis 30) |
| 2026-05-20 | Dev | P1 scaffold livré — `tools/ck_image_normalizer/` |
