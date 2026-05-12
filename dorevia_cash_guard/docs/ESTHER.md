# Projections de trésorerie — Ce que nous vous livrons

## Le problème

Vous avez besoin de savoir, **avant qu'il ne soit trop tard**, si votre trésorerie sera suffisante pour couvrir vos prochaines échéances (salaires, fournisseurs, charges, loyers...).

## La solution

Nous vous livrons un ensemble de trois modules complémentaires qui s'intègrent directement dans votre Odoo, rubrique **Comptabilité > Projection > Trésorerie**.

---

## Module 1 — Projections de trésorerie

Le socle. Il répond à une question simple : **est-ce que ma trésorerie restera positive dans les semaines à venir ?**

Ce que vous y trouvez :

- **Un formulaire par projection** : vous définissez la période, les journaux bancaires à suivre, et un seuil d'alerte.
- **L'onglet Projection** : une ligne par semaine avec le solde projeté, la couverture par rapport au seuil, et un statut couleur (Confort / Vigilance / Tension / Risque). La colonne Documents indique les lignes qui contiennent des pièces détaillées.
- **L'onglet Documents** : la liste de toutes les factures et pièces qui expliquent la projection, avec leur échéance, leur impact et un lien pour les ouvrir.
- **Le détail d'une période** : en cliquant sur une ligne de projection, vous voyez le contexte (projet, dates) et les indicateurs de trésorerie, ainsi que les documents rattachés à cette période.
- **La synthèse** : en haut du formulaire, le solde constaté, la projection finale, le point bas et la couverture minimum.

---

## Module 2 — Simulation Ventes

Une couche optionnelle. Elle permet de répondre à la question : **que se passerait-il si ces devis étaient signés ?**

- Vous activez le **mode simulation** sur une projection.
- Vous sélectionnez des **devis clients** (non encore facturés).
- La projection intègre ces devis comme des encaissements hypothétiques, visuellement distincts des données réelles.
- Vous voyez immédiatement l'impact sur votre trésorerie future.

---

## Module 3 — Simulation Achats

Le complément côté dépenses. Même principe :

- Vous sélectionnez des **commandes d'achat fournisseur** (non encore facturées).
- La projection intègre ces commandes comme des décaissements hypothétiques.
- Vous voyez l'impact combiné ventes + achats simulés.

---

## Ce qui est important à retenir

| Donnée réelle | Donnée simulée |
|---|---|
| Factures validées, écritures bancaires | Devis clients, commandes achat |
| Coloriée selon le risque (vert, bleu, orange, rouge) | Affichée en neutre (noir) |
| Toujours visible | Visible uniquement quand la simulation est activée |

**Une simulation n'est pas une prévision certaine.** C'est un outil de pilotage pour anticiper et décider.
