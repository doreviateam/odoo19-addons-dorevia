# Décision — Section Produits Homepage MVP2.1 (sélection dynamique)

**Statut** : actée (MOA).  
**Date** : 2026-04-24.  
**Périmètre** : bloc **Sélection produits** (wireframe [Bloc 5](../direction/WIREFRAME_HOMEPAGE.md) — `ckr_snippet_selection` / `views/snippets/ckr_selection.xml`).

> La **mise en avant fournisseur** (Bloc 4 — `ckr_snippet_supplier`) n’est **pas** couverte par cette décision ; seule la **grille produits** sous `docs/mvp_02/1_HOMEPAGE.md` §3 « Sélection » évolue selon les règles ci-dessous.

## Contexte

Les produits mis en avant sont **branchés sur `website_sale`** : images, noms, prix et URLs de fiche relèvent du **catalogue publié Odoo**, sans contenu de grille « inventé » ou prix figé en dur.

## Cible retenue

- **Grille de 4 produits** (desktop ; comportement mobile : **grille responsive** sobre, détail en ticket / maquette).
- Données **100 % dynamiques** Odoo (`product.template` / politique de publication conforme au site).
- **Carte produit** simple et lisible, avec pour chaque carte :
  - image produit ;
  - **label court** (origine, type ou badge) — **même nature d’information** sur les quatre cartes, ou **aucun** label si la règle de couverture globale impose le masquage ([PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md §9.4](../crea/PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md)) ;
  - nom produit ;
  - **prix dynamique** (prix public / liste tel qu’affiché par la boutique) ;
  - CTA **Voir le produit** → **fiche produit** native `website_sale`.

## Comportement

- Clic sur la **carte** (zone produit) → **fiche produit**.
- Clic sur le **CTA** → **fiche produit**.
- **Pas** de redirection **forcée** de la carte vers le listing générique `/shop` : le parcours standard est **fiche produit** (cohérence parcours e-commerce Odoo).
- Un lien de **section** vers le catalogue (`/shop`) reste **optionnel** et distinct des cartes (ex. « Voir tous les produits »), s’il est conservé côté copy.

## Hors périmètre MVP2.1

- **Ajout panier direct** depuis la grille homepage.
- Logique **AJAX** / panier **inline** sur la homepage.
- **Prix statique** ou prix non synchronisé avec le catalogue.
- Grille **8 produits** (non retenue pour cette vague ; réouverture ultérieure par ticket si besoin).
- **Surcharge UX** (animations lourdes, informations redondantes, marketplace générique).

## Synthèse (gel fonctionnel)

```text
Section Sélection produits MVP2.1 :
grille de 4 produits dynamiques issus de website_sale,
avec prix affiché et accès à la fiche produit,
sans ajout panier direct.
```

## Impacts

- **QWeb** : remplacement des cartes statiques par un rendu piloté par **données** (boucle sur un recordset ou snippet paramétrable — détail au ticket).
- **Python** : contrôleur ou méthode de résolution des **4** produits (règle métier : tag, liste manuelle, domaine `website_published`, etc.) — à figer au ticket.
- **Sincérité offre** : produits réellement publiés / achetables selon [ADR-CKR-005](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005) et [DESIGN.md §5.1](../direction/DESIGN.md).
- **`__manifest__.py`** : bump si bundle front modifié.
- **Documentation** : aligner [WIREFRAME_HOMEPAGE.md](../direction/WIREFRAME_HOMEPAGE.md) Bloc 5 après merge si le wireframe décrit encore uniquement des placeholders — **même PR ou commit doc immédiat**.

## Références

| Document | Rôle |
|----------|------|
| [1_HOMEPAGE.md](1_HOMEPAGE.md) | §3 — cadrage homepage |
| [TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md](../crea/TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md) | Exécution — checklist avant PR |
| [PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md](../crea/PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md) | Trame recette après livraison |
| [DECISION_HERO_HOMEPAGE_V2.md](DECISION_HERO_HOMEPAGE_V2.md) / [DECISION_EXPLORER_HOMEPAGE_MVP2.md](DECISION_EXPLORER_HOMEPAGE_MVP2.md) | Chantiers homepage parallèles — coordonner PR |

## Historique

| Date | Événement |
|------|-----------|
| 2026-04-24 | Actée — grille 4 produits dynamiques `website_sale`, prix + fiche produit, hors panier inline / hors 8 cartes ; ticket + PV créés. |
| 2026-04-24 | **Ticket sélection** réécrit (fiche MOA / dev complète) ; conservation checklist §0, §9.4, ADR-005. |
| 2026-04-24 | **Livraison** : module **19.0.1.9.0** — 4 `Many2one` `product.template` sur `website` ; QWeb + `_get_combination_info` ; règle §9.4 origines ; tests `dorevia_ckr_selection`. |
| 2026-04-24 | **19.0.1.9.4** : test `TransactionCase` — emplacement BO sans binaire fiche/variante **ignoré** ; complément issue du **pool** catalogue (non-régression repli [1_HOMEPAGE](1_HOMEPAGE.md) §3). |
| 2026-04-24 | **Recette** — [PV](../crea/PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md) : **GO MOA** (réserves mineures) ; contrat MVP2.1 tenu ; passage chantier **Inscription (4/5)**. |
