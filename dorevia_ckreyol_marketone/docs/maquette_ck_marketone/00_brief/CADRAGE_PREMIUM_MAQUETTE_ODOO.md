# Cadrage premium — maquette alignee sur Odoo

| Champ | Valeur |
|-------|--------|
| **Regle** | La tendance **premium** validee en prod / recette MOA prime sur toute nouvelle iteration maquette |
| **Ligne** | Artisanal Terroir · **premium epicerie fine** avant saturation creole (UX-3 B1.4) |
| **Module** | `dorevia_ckreyol_marketone` · reference recette [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) |

## Intention premium (MOA)

- Boutique **chaleureuse et structuree**, pas catalogue froid ni « marketplace generique ».
- **Produit d'abord** : photo pleine, prix et CTA lisibles, recit court.
- Chaleur CK par **aplats dilues et bordures**, pas par fonds satures ni degrades decoratifs.
- **Pas** d'effet luxe ostentatoire : premium accessible, tenue, editorial sobre.

Source tickets : `TICKET_MARKETONE_UX3_PALIER_B1_CREOLE_BACKGROUNDS.md` (B1.4 premium first) · `TICKET_MARKETONE_UX3_PALIER_A_PROPOSITION_DA.md` (variante B « Tenue »).

## Tokens a respecter dans Open Design

Reprendre la chaine `$ck-*` de `static/src/scss/_tokens_colors.scss` :

| Token | Hex | Usage maquette / Odoo |
|-------|-----|------------------------|
| `$ck-bg-body` | `#FFFFFF` | Fond page boutique |
| `$ck-bg-card` | `#FFFDF8` | Sidebar, surfaces, cartes |
| `$ck-bg-card-body` | `#FDF9F0` | Corps tuile sous image |
| `$ck-bg-image-tile` | `#FDFCFA` | Zone photo tuile (quasi invisible) |
| `$ck-bg-sidebar` | `#F3EDE5` | Sidebar lin (pas bloc vert) |
| `$ck-border-soft` | `#E2D4BC` | Bordures chaudes |
| `$ck-text` | `#2A1F18` | Texte principal |
| `$ck-terracotta` | `#C4715A` | Prix, hover titre, CTA secondaires |
| `$ck-sauge` | `#5A8A6E` | Accents discrets, bordure hover carte |
| `$ck-bg-page` | `#F2E3D2` | Reserve accents (chips), **pas** aplat pleine page |

**Interdit** sur iterations « production » :

- Dominante **vert marketplace** type piste 1 OD initiale (`oklch` accent 154°).
- Degrades decoratifs, blobs, palettes type startup e-commerce.
- Sidebar ou body en aplat vert / ocre lourd.

## Typographie (Odoo)

| Role | Police |
|------|--------|
| Titres | **EB Garamond**, Georgia, serif |
| UI / corps | **Hanken Grotesk**, system-ui, sans-serif |

Ne pas remplacer par Inter / Avenir seuls sur les iterations alignees prod.

## Comportements premium deja codes (ne pas contredire en maquette)

| Zone | Attendu |
|------|---------|
| Tuile `/shop` | Photo cover bord a bord · ombre chaude legere · hover `-2px` · prix terracotta |
| Grille | Titre 2 lignes · **Voir** + prix · panier au survol photo |
| Preview | Non modale in-page (UX-4 Lot 3 · finition 3bis premium) |
| Filtres | Chips + compteur MOA (UX-1) |
| Images | Doctrine [`DOCTRINE_IMAGE_V2.md`](../../cadrage/DOCTRINE_IMAGE_V2.md) · pas produit flottant |

## Piste Open Design vs prod

| Artefact | Role |
|----------|------|
| `piste_1_marche_creole_contemporain/` | Exploration structure / parcours (vert OKLCH) — **non** reference couleur prod |
| **Iterations suivantes** | Meme structure, **tokens + typo Odoo** ci-dessus |
| Export cible | `piste_1bis_artisanal_terroir/` (a creer apres M-05) |

## Texte a injecter dans la memoire Open Design

Fichier copiable : [`MEMOIRE_OPEN_DESIGN_PREMIUM.txt`](./MEMOIRE_OPEN_DESIGN_PREMIUM.txt)

## Lien backlog

Iteration gate : **M-05** dans [`02_backlog/BACKLOG_MAQUETTE.md`](../02_backlog/BACKLOG_MAQUETTE.md) — priorite avant nouvelles zones visuelles.
