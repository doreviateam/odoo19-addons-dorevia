# Proposition design — C-Kreyol Marketone « Artisanal Terroir »

| Champ | Valeur |
|-------|--------|
| **Nom de direction** | Artisanal Terroir |
| **Positionnement** | Épicerie fine créolophone — premium accessible, chaleureux, product-first |
| **Statut** | Proposition Cursor · à valider MOA · à reproduire dans Open Design (M-05+) |
| **Planche visuelle** | [`PROPOSITION_ARTISANAL_TERROIR.html`](./PROPOSITION_ARTISANAL_TERROIR.html) |

## En une phrase

Une boutique **blanche et tenue**, où le produit photographié plein cadre porte la conversion, et où la chaleur créole passe par **terracotta, sauge et crème** — jamais par un vert marketplace ni un décor tropical.

## Principes (5)

1. **Produit d'abord** — grille lisible, prix terracotta, CTA immédiats, récit court sous la ligne d'achat.
2. **Premium sans luxe** — ombres chaudes légères, serif éditorial, pas de dorure ni dégradés décoratifs.
3. **Chaleur par matière** — papier `#FFFDF8`, lin sidebar `#F3EDE5`, bordures miel `#E2D4BC`.
4. **Culture en appui** — bandeau origines discret ; Savoirs en prolongement, pas en couverture magazine.
5. **Odoo-native** — radius 12–14px cartes, sidebar filtres, chips actifs, preview in-place.

## Palette (production)

| Rôle | Hex | Usage |
|------|-----|--------|
| Body | `#FFFFFF` | Fond page |
| Carte | `#FFFDF8` | Surfaces, header sticky |
| Corps tuile | `#FDF9F0` | Sous image produit |
| Zone photo | `#FDFCFA` | Fond tuile (quasi neutre) |
| Sidebar | `#F3EDE5` | Filtres |
| Texte | `#2A1F18` | Titres, corps |
| Texte muted | `#54433c` | Descriptions |
| Terracotta | `#C4715A` | Prix, CTA primaire, hover titres |
| Sauge | `#5A8A6E` | Labels origine, bordure hover |
| Bordure | `#E2D4BC` | Cartes, champs |
| Accent chip | `#F2E3D2` | Pills filtres (hover uniquement) |

## Typographie

- **Display** : EB Garamond 600–700 — H1 accueil, titres section, noms produit fiche.
- **UI** : Hanken Grotesk 400–800 — nav, filtres, prix, boutons, meta.
- **Eyebrow** : Hanken, uppercase, letter-spacing 0.12em, couleur sauge.

## Composants clés

| Composant | Règle |
|-----------|--------|
| Header | Sticky, fond `#FFFDF8` 92% + blur, logo serif, nav 3 mondes, recherche, icônes outline |
| Tuile shop | Image 1:1 cover, wishlist haut droit, meta « Origine · Catégorie », titre 2 lignes, **Voir** + prix, + au survol |
| Chip filtre | Pill bordure `#E2D4BC`, fond blanc, actif bordure sauge |
| CTA primaire | Fond terracotta, texte blanc, min-height 46px, radius 8px |
| CTA secondaire | Fond blanc, bordure `#E2D4BC` |
| Bloc origine fiche | Encadré `#FDF9F0`, titre « Origine et usage », 3–4 lignes max |

## Structure pages (ordre de lecture)

1. **Accueil** — promesse + CTA boutique + 4 entrées (épicerie, maison, origines, usages) + trust line.
2. **/shop** — sidebar + compteur/chips + grille 3 col.
3. **Fiche** — galerie + buybox sticky mental + origine/usage + réassurance.
4. **Panier** — lignes compactes + summary sticky.
5. **Culture** — intro sombre courte + 3 cartes territoire (pas portail lourd).

## Prompt Open Design (résumé)

Voir bloc complet dans [`PROPOSITION_ARTISANAL_TERROIR.html`](./PROPOSITION_ARTISANAL_TERROIR.html) (`<!-- PROMPT OD -->`).

## Écarts vs piste 1 OD verte

| Élément | Piste 1 OD | Cette proposition |
|---------|------------|-------------------|
| Accent | Vert OKLCH | Terracotta + sauge |
| Display | Avenir / system | EB Garamond |
| Fond page | Crème verdâtre | Blanc + cartes crème |
| Ton | Marketplace tech | Épicerie fine éditoriale |

## Suite

1. Ouvrir la planche HTML et valider le ressenti.
2. Coller le prompt OD (section commentaire HTML) dans le projet `44de8203-...`.
3. Exporter vers `04_exports_open_design/proposition_artisanal_terroir/` ou `piste_1bis_artisanal_terroir/`.
