# Clarification technique — Parser sections fiche produit & fallback description

**Projet** : C-Kreyol — Odoo 19  
**Suite à** : `CARTOGRAPHIE_CHAMPS_PRODUIT_CK_V1.md`  
**Nature** : clarification documentaire uniquement (aucun changement code)  
**Fichiers source analysés** : `product_page_details.py`, `hooks.py`, `test_ck_product_page_lot2.py`

---

## Réponse Q1 — Format de saisie `website_description`

### Fichiers & méthodes

| Élément | Chemin |
|---------|--------|
| Parser principal | `dorevia_ck_marketone_content/product_page_details.py` → `_parse_website_description_sections()` |
| Orchestration | `product_page_details.py` → `_build_ck_product_page_detail_sections()` |
| API modèle | `models/product_template.py` → `get_ck_product_page_detail_sections()` |
| Données seed référence | `hooks.py` → `PRODUCT_WEBSITE_DESCRIPTIONS` |

### Principe général

Le parser accepte une structure **souple** basée sur des **titres HTML** (`h2`, `h3`, `h4`).  
La classe `ck-product-enrich` est **recommandée** (utilisée par le seed CK) mais **non obligatoire** : si absente, le contenu racine est parsé tel quel.

### Balises & structure reconnues

| Élément | Détail |
|---------|--------|
| Conteneur optionnel | `<div class="ck-product-enrich">` — si présent, seul le **premier** est parsé |
| Découpage sections | Enfants directs du conteneur ; chaque `h2` / `h3` / `h4` ouvre une nouvelle section |
| Corps de section | Tous les nœuds suivants jusqu’au prochain titre |
| Sans aucun titre | Tout le HTML → **une seule** section `Origine & usage` |
| Paragraphe Usage | Dans section Origine : `<p><strong>Usage :</strong> …</p>` extrait vers section **Conseils d'usage** |
| Conservation | Si le texte contient `Avant ouverture :` / `Après ouverture :` → sous-blocs avec sous-titres |

### Titres reconnus (libellé du heading, insensible à la casse)

Après normalisation (minuscules, espaces unifiés, entités HTML décodées) :

| Titre saisi (variantes) | Clé section | Titre affiché front |
|-------------------------|-------------|-------------------|
| Origine & usage · Origine et usage · Description | `origin_usage` | Origine & usage |
| Usage · Conseils d'usage · Conseils d’usage | `usage` | Conseils d'usage |
| Conservation | `conservation` | Conservation |
| Ingrédients & allergènes · Ingrédients | `ingredients` | Ingrédients & allergènes |
| Valeurs nutritionnelles | `nutrition` | Valeurs nutritionnelles |
| Origine & producteur · Origine et producteur | `origin_producer` | Origine & producteur |

**Titre non listé** : mappé par défaut sur la clé `origin_usage` (titre affiché fixe « Origine & usage »).

Les classes sur les headings (`h5`, `mt-3`, etc.) sont **ignorées** — seul le texte du titre compte.

### Classes CSS

| Classe | Rôle |
|--------|------|
| `ck-product-enrich` | Conteneur éditorial recommandé ; optionnel pour le parser |
| Autres (`h5`, `mt-3`, Bootstrap…) | Cosmétiques — **non interprétées** par le parser |

### Comportements limites

| Cas | Comportement |
|-----|--------------|
| Section absente | Non affichée (sections conditionnelles) |
| Section vide (corps + sous-titres vides) | Ignorée |
| Corps identique à `description_ecommerce` (accroche) | Filtré — pas affiché en double |
| HTML mal formé / erreur parser | `get_ck_product_page_detail_sections()` retourne `[]` (try/except) |
| Attribut produit « Origines » | Section `Origine & producteur` ajoutée si non déjà couverte |
| Document produit nommé « nutrition » | Section `Valeurs nutritionnelles` avec lien |

### Exemple HTML — format **actuellement supporté** (copier-coller Odoo)

Correspond au seed `PRODUCT_WEBSITE_DESCRIPTIONS['Confiture de goyave']` et aux tests `test_ck_product_page_lot2` :

```html
<div class="ck-product-enrich">
  <h3 class="h5">Origine &amp; usage</h3>
  <p>Confiture artisanale créole — goyave sélectionnée par CK.
  Texture fondante, notes florales et légèrement acidulées.</p>
  <p><strong>Usage :</strong> tartines, yaourts, pâtisseries, accords fromages frais.</p>

  <h3 class="h5 mt-3">Conservation</h3>
  <p>Avant ouverture : conserver au sec, à l'abri de la lumière.
  Après ouverture : réfrigérer et consommer sous 3 semaines.</p>

  <h3 class="h5 mt-3">Ingrédients &amp; allergènes</h3>
  <p>Goyave, sucre, jus de citron. Peut contenir des traces de fruits à coque.</p>
</div>
```

**Résultat parser** : 4 sections — `origin_usage`, `usage`, `conservation`, `ingredients`.

### Format minimal sans conteneur (également supporté)

```html
<h3>Origine &amp; usage</h3>
<p>Texte d'origine et de présentation.</p>
<p><strong>Usage :</strong> idées de consommation.</p>

<h3>Conservation</h3>
<p>Avant ouverture : au sec. Après ouverture : au frais.</p>
```

### Ce qui n'est **pas** garanti aujourd'hui

- Titres libres type « Goût », « Conseil CK », « Moment de consommation » comme sections dédiées (→ rattachés à `origin_usage` ou ignorés si vides).
- Structure `<section>` sans `h2`/`h3`/`h4` enfants directs.
- Listes `<ul>` / tableaux sans titre de section parent.

**Recommandation saisie MOA V1** : rester sur le gabarit `ck-product-enrich` + `h3` + titres du tableau ci-dessus.

---

## Réponse Q2 — Fallback `description_sale`

| Point | Réponse |
|-------|---------|
| **Fallback actif ?** | **Oui** |
| **Fichier / méthode** | `product_page_details.py` → `_build_ck_product_page_detail_sections()` (l. 270–276) |
| **Condition de déclenchement** | `website_description` vide **et** `description_sale` non vide **et** texte brut de `description_sale` ≠ texte brut de `description_ecommerce` |
| **Section front reçue** | `origin_usage` — titre affiché « Origine & usage » |
| **Couvert par un test ?** | **Oui** — `test_ck_product_page_lot2.py` → `test_description_sale_fallback` |
| **Souhaité techniquement ?** | **À arbitrer MOA** — voir recommandation ci-dessous |

### Extrait de logique (référence)

```python
website_html = (product.website_description or '').strip()
if website_html:
    sections.extend(_parse_website_description_sections(website_html))
elif (product.description_sale or '').strip():
    body = product.description_sale
    if _plain_text(body) and _plain_text(body) != lead_plain:
        _append_section(sections, 'origin_usage', 'Origine & usage', body)
```

Le fallback ne s'applique **jamais** si `website_description` contient du texte (même minimal).

---

## Recommandation Dev

| Option | Avis Dev | Justification |
|--------|----------|---------------|
| **A — Conserver temporairement** | Possible | Compatibilité produits legacy / bootstrap sans `website_description`. Testé. Risque confusion BO documenté. |
| **B — Supprimer / désactiver** | **Recommandé** (aligné MOA) | `description_sale` = notes commerciales Odoo. Le seed CK remplit désormais `website_description` via `hooks.py`. Le fallback n'est plus nécessaire pour les produits pilotes. |

**Recommandation** : **Option B** dans un ticket ultérieur dédié (hors Lot 2 design). En attendant : **ne pas saisir de contenu client dans `description_sale`** — réserver ce champ aux notes devis / commandes / factures.

---

## Impact documentaire

| Document | Action |
|----------|--------|
| `CARTOGRAPHIE_CHAMPS_PRODUIT_CK_V1.md` | Préciser fallback actif + gabarit HTML §6 |
| `NOTE_BO_PRODUIT_ONGLET_VENTES_CK_V1.md` | Lien vers cette note |
| Guide saisie MOA (futur) | Reprendre l'exemple HTML § Q1 |

---

## Impact futur ticket Lot 2 front

| Point | À intégrer |
|-------|------------|
| Champ éditorial de référence | `website_description` uniquement |
| Gabarit saisie BO | Exemple HTML de cette note |
| `description_sale` | Exclu du rendu front (suppression fallback = ticket séparé Option B) |
| `description_ecommerce` | Accroche zone achat — jamais dupliquée dans sections longues |
| Sections affichées | Liste blanche des clés : `origin_usage`, `usage`, `conservation`, `ingredients`, `nutrition`, `origin_producer` |
| Erreur parser | Comportement silencieux (`[]`) — pas de message BO ; saisie à valider en recette |

---

## Synthèse MOA (2 lignes)

1. **`website_description`** : saisir en `h3` + paragraphes selon le gabarit `ck-product-enrich` documenté ci-dessus.  
2. **`description_sale`** : notes commerciales Odoo seulement — le fallback front existe encore mais **ne doit pas être utilisé** ; suppression recommandée (Option B).
