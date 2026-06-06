# Brief maquette CK Marketone

## Objectif

Produire une premiere proposition de refonte visuelle pour C-Kreyol Marketone, canal e-commerce dedie aux produits issus de territoires creolophones.

La maquette doit aider a choisir une direction UI avant integration dans le module Odoo `dorevia_ckreyol_marketone`.

Mode de travail : **iteratif au fil de l'eau** (Open Design + export versionne + lots Odoo cibles). Voir [01_workflow/WORKFLOW_MAQUETTE_ITERATIVE.md](../01_workflow/WORKFLOW_MAQUETTE_ITERATIVE.md) et [02_backlog/BACKLOG_MAQUETTE.md](../02_backlog/BACKLOG_MAQUETTE.md).

**Reference visuelle obligatoire** : conserver la tendance **premium** deja validee sur le site Odoo (MOA · UX-3 B1.4 · tuiles UX-4). Detail : [CADRAGE_PREMIUM_MAQUETTE_ODOO.md](./CADRAGE_PREMIUM_MAQUETTE_ODOO.md). Les iterations maquette **ne doivent pas** diluer cette ligne (pas de retour palette verte marketplace / style generique).

## Doctrine produit

C-Kreyol articule trois dimensions :

- vendre une selection de produits issus de territoires creolophones ;
- raconter les territoires, langues, producteurs, usages et savoir-faire ;
- transmettre des reperes, recettes, vocabulaire et traditions.

Regle d'agencement :

```text
Le produit d'abord.
Le recit ensuite.
Le savoir en prolongement.
```

## Pages a maquettiser en priorite

- Accueil marketplace
- Boutique `/shop`
- Fiche produit
- Panier / recapitulatif
- Porte Culture / Origines

## Contraintes

- Compatible avec une integration Odoo Website / Website Sale.
- Ne pas produire une boutique exotique generique.
- Ne pas surcharger `/shop` avec du contenu culturel lourd.
- CTA d'achat prioritaire.
- Navigation claire entre Boutique, Culture et Savoirs.
- Design marchand, lisible, chaleureux, premium sans effet catalogue luxe.

## Direction visuelle

### Ligne prod (prioritaire) — Artisanal Terroir premium

- epicerie fine chaleureuse, tenue, editorial sobre ;
- chaine `$ck-*` + EB Garamond / Hanken Grotesk ;
- voir [CADRAGE_PREMIUM_MAQUETTE_ODOO.md](./CADRAGE_PREMIUM_MAQUETTE_ODOO.md).

### Piste 1 OD (exploration structure) — `Marche creole contemporain`

Export historique vert OKLCH : parcours et composants utiles, **couleurs non reference prod**. Alignement premium = iteration **M-05** → dossier `piste_1bis_artisanal_terroir/`.

## Sources locales

Module Odoo :

```text
/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone
```

Atelier maquette (source de verite) — Open Design :

```text
/Users/doreviateam/open-design
```

Projet Open Design C-Kreyol Marketone (piste 1) :

```text
/Users/doreviateam/open-design/.od/projects/44de8203-38b0-4405-af76-2f09c97c5f02/
```

Artefact principal : `index.html`

Export versionne dans le depot (a resynchroniser apres chaque iteration OD) :

```text
docs/maquette_ck_marketone/04_exports_open_design/piste_1_marche_creole_contemporain/index.html
```

Commande de sync :

```bash
cp "/Users/doreviateam/open-design/.od/projects/44de8203-38b0-4405-af76-2f09c97c5f02/index.html" \
  "/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/maquette_ck_marketone/04_exports_open_design/piste_1_marche_creole_contemporain/index.html"
```
