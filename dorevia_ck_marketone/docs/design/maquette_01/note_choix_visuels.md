# Note — Choix visuels Maquette CK V1

## Intention

Produire une **V1 marchande opérationnelle** : le visiteur comprend en quelques secondes qu’il peut acheter des produits agro-transformés créoles, voir les prix, et passer à l’achat — sans effet galerie ni exotisme caricatural.

## Direction retenue

- **Ambiance** : marché alimentaire contemporain, lumineux, structuré — inspiration *efficacité* directos.eu, pas copie graphique.
- **Hiérarchie** : produit et prix d’abord ; éditorial court en soutien.
- **Couleur** : fond crème chaud (`#FFFBF7`), CTA corail-appétit (`#D84315`), vert confiance discret pour origines (`#2E7D4F`). Pas de palette startup verte dominante ni pastel premium historique.
- **Typo** : Fraunces (titres, caractère alimentaire) + DM Sans (UI lisible). Choix maquette — à arbitrer pour prod (licences, perf).
- **Cartes produit** : image grande, prix en gras, origine en chip, CTA « + » visible. Zone image en aplat `#FAF6F0` — pas de dégradé décoratif sur la tuile.
- **B2B** : lien header « Professionnels » + bandeau discret en bas `/shop` — ne concurrence pas le CTA boutique.

## Écrans

| Écran | Choix clés |
|-------|------------|
| **Accueil** | Hero 3 questions (quoi / pourquoi / où) ; catégories en pills ; 4 produits vedettes ; réassurance 4 icônes |
| **`/shop`** | Sidebar filtres (desktop) / drawer (mobile) ; grille 4 cols → 2 → 1 ; toolbar tri ; 6 produits démo |
| **Fiche produit** | Layout 2 colonnes desktop, stack mobile ; buy box sticky léger ; bloc usage + réassurance |

## Mobile-first

- Breakpoint principal `768px` : sidebar → bouton « Filtres » + panneau overlay.
- Hero accueil : titre réduit, CTA pleine largeur.
- Fiche : galerie puis buy box en flux vertical ; CTA achat visible sans scroll excessif.

## Ce qui n’est pas une DA finale

Cette V1 sert l’**arbitrage MOA** et la recette QA. Un directeur artistique pourra affiner palette, typo et rythme — les tokens sont exportables pour ne pas repartir de zéro en thème Odoo.

## Ancienne DA

Aucune reprise terracotta / sauge / Garamond-Hanken / prototype OD vert. Mémoires Open Design historiques ignorées pour cette production.
