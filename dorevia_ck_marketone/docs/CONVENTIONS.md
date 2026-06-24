# Conventions documentaires

Ces règles gardent la documentation exploitable sans imposer une migration massive de l’existant.

## Où créer un document

| Type | Emplacement |
|---|---|
| Vision, gouvernance, doctrine | `docs/cadrage/` |
| Architecture ou référence transverse | `docs/design/` |
| Décision, livraison ou recette de la V1.2.x | `docs/design/maquette_01.2/` |
| Capture de recette | `docs/design/maquette_01.2/captures/<sujet>/` |
| Script QA | `docs/design/maquette_01.2/scripts/` |
| Rapport publié | `docs/design/maquette_01.2/rapport/` |

Ne plus ajouter de nouveau document dans `maquette_01/`, réservé à l’historique V1.1.

## En-tête minimal

Tout nouveau document doit commencer par un titre explicite puis ce tableau :

```md
# Type — Sujet · Version

| Champ | Valeur |
|---|---|
| Projet | `dorevia_ck_marketone` |
| Statut | Brouillon / À arbitrer / Actif / Clôturé / Historique |
| Date | AAAA-MM-JJ |
| Responsable | MOA / Dev / QA |
| Remplace | lien ou — |
| Remplacé par | lien ou — |
```

## Nommage

Utiliser un préfixe qui annonce la fonction du document :

- `DECISION_MOA_…` ou `ACTE_MOA_…` : arbitrage signé ;
- `SPEC_…` : comportement attendu et durable ;
- `TICKET_DEV_…` : demande d’implémentation ;
- `RECETTE_QA_…` : protocole et verdict QA ;
- `LIVRAISON_…` : contenu effectivement livré ;
- `RAPPORT_…_AAAAMMJJ` : constat daté ;
- `NOTE_ARCHITECTURE_…` : explication technique maintenue.

Éviter les nouveaux noms génériques comme `note_06.md`, `final.md`, `nouveau.md` ou `v2_final_bis.md`.

## Cycle de vie

- **Brouillon** : incomplet, non opposable.
- **À arbitrer** : choix MOA requis.
- **Actif** : référence à utiliser.
- **Clôturé** : résultat acquis, conservé pour preuve.
- **Historique** : remplacé ; doit pointer vers son successeur.

Un document remplacé n’est pas supprimé : ajouter en haut un renvoi visible vers la référence active, puis mettre à jour l’index du dossier.

## Pièces de preuve

Une recette Markdown porte le verdict. Les captures, JSON et scripts sont des annexes : ils doivent être liés depuis la recette, sans devenir eux-mêmes une nouvelle porte d’entrée documentaire.
