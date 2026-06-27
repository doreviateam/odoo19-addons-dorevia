# Ticket contenu — R3 · Paramétrage Manio Crackers + La Platine (Note 08)

| Champ | Valeur |
| --- | --- |
| Type | **Paramétrage contenu MOA** (back-office Odoo) |
| Périmètre Dev | **Hors scope** — aucun texte produit hardcodé dans le module |
| Réserve | R3 (+ clôture progressive R4) |
| Priorité | Moyenne |
| Bloquant | Non (démo MOA enrichie) |
| Porteur | MOA / rédaction contenu |
| Produits pivot | **Manio Crackers** · partenaire **La Platine** |

## Contexte

La recette QA Note 08 a validé le **socle technique** (champs V1.1, BO, front, ancres conditionnelles).  
R3 consiste à **renseigner le contenu métier dans Odoo** pour rendre la fiche Manio présentable, vendable et cohérente avec la grammaire CK V1.1.

> **Règle gouvernance** : pas de seed technique ni de textes figés dans `dorevia_ck_marketone_content`, sauf demande explicite MOA pour une base démo/test.

---

## 1. La Platine (`Contacts` → partenaire)

Menu : **Contacts** → rechercher **La Platine** → onglet **Producteur CK**.

| Champ BO | Action |
| --- | --- |
| `ck_is_producer` | Cocher |
| `ck_producer_short_description` | Accroche courte du bloc Producteur (texte validé MOA) |
| `ck_producer_location_label` | Ex. Guadeloupe |
| `ck_producer_story_html` | Texte éditorial optionnel — **éditeur Odoo** si mise en forme |
| `image_1920` | Logo / photo producteur si disponible |

---

## 2. Manio Crackers (`Ventes` → Produit → onglet **Ventes**)

Produit pivot recette : **Manio Crackers** (`/shop/manio-crackers-*`).

### Origine & producteur

| Champ BO | Action |
| --- | --- |
| `ck_producer_id` | Lier **La Platine** (domaine : partenaires `ck_is_producer = True`) |
| `ck_badge_ids` | Sélectionner les badges MOA — ex. Guadeloupe · Farine de manioc · Producteur identifié |

> Les badges affichés front proviennent **uniquement** de cette sélection BO (pas de badge implicite).

### Contenu fiche (sections V1.1)

| Champ BO | Section front | Mode de saisie |
| --- | --- | --- |
| `description_ecommerce` | Accroche zone haute | Texte court (~255 car. — voir réserve R1) |
| `ck_discover_html` | Découvrir | **Éditeur Odoo** / snippets si contenu éditorial |
| `ck_ingredients` | Composition | Texte ou liste validée MOA |
| `ck_allergens` | Composition | Si applicable — données réglementaires validées |
| `ck_nutrition_html` | Composition | **Éditeur Odoo** si tableau / mise en forme |
| `ck_conservation_before` | Conservation | Texte validé MOA |
| `ck_conservation_after` | Conservation | Texte validé MOA |

### Infos pratiques

| Champ BO | Action |
| --- | --- |
| `ck_packaging_label` | Ex. Sachet 100 g |
| `ck_net_quantity` + `ck_net_quantity_uom_id` | Vérifier cohérence meta (ex. 100 g · prix/kg) |

> L’origine géographique en meta reste portée par l’attribut **Origines** (onglet Attributs & variantes), pas par un champ dédié fiche.

---

## 3. R4 — Clôture fallback `website_description`

Une fois les champs V1.1 renseignés (Découvrir · Composition · Conservation selon contenu disponible) :

1. Ouvrir **Description pour le site e-commerce** (`website_description`) ;
2. **Vider** ou archiver le contenu redondant (bloc seed historique `ck-product-enrich` si présent) ;
3. Contrôler la fiche front : **aucun double affichage** (priorité aux champs dédiés V1.1).

R4 reste **transitoire** tant que la migration contenu n’est pas faite — pas de NO GO technique.

---

## 4. Critères d’acceptation MOA

| Contrôle | Attendu |
| --- | --- |
| Meta zone haute | Origine · **La Platine** (lien `#ck-section-producer`) · contenance · prix/kg |
| Badges | Visibles uniquement si sélectionnés en BO |
| Ancres | **Composition** et **Producteur** actives si contenu renseigné — pas d’ancre vide |
| Bloc Producteur | La Platine visible avec accroche / localisation |
| Script QA | `ck_note08_recette_qa.mjs` : `informational.metaHasProducerLink` et `producerSectionOk` à `true` |
| Non-régression | R1 ouvert (polish accroche) · R2 vérifié au prochain passage visuel |

---

## 5. Hors périmètre R3

- Développement module · migration code · seed automatisé ;
- Validation réglementaire des allégations (allergènes, nutrition) — responsabilité MOA ;
- Fiche producteur CMS complète (`/producteur/…`) — hors Note 08.

---

## Références

- [`note_08.md`](./note_08.md) · § affichage conditionnel sections V1.1
- [`NOTE_QA_INTERVENTION_NOTE_08_FICHE_PRODUIT_CK_V1_1.md`](../design/maquette_01.2/NOTE_QA_INTERVENTION_NOTE_08_FICHE_PRODUIT_CK_V1_1.md)
- [`RECETTE_QA_NOTE_08_VERDICT.md`](../design/maquette_01.2/RECETTE_QA_NOTE_08_VERDICT.md) — R3/R4
- [`NOTE_MOA_DECISION_NOTE_08.md`](./NOTE_MOA_DECISION_NOTE_08.md)
