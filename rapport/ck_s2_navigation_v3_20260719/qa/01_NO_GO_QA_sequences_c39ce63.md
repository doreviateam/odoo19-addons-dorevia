# Recette QA S2 — navigation V3 canonique

**Verdict : NO GO QA**

## Référence testée

- Dépôt : `odoo19-addons-dorevia`
- Branche locale : `refactor/s2-canonical-navigation-v3`
- SHA exact : `c39ce6329f06625efb218198c7aba01046bea010`
- Content : `19.0.1.96.0`
- Thème actif : `19.0.1.129.0`
- Base dédiée : `ck_s2_qa_20260719`
- Navigateur : Codex In-app Browser
- Desktop : `1280 × 720`
- Mobile émulé : `390 × 844`
- Resynchronisation : `bootstrap_ck_catalogue_navigation(env)`

La branche n'était pas publiée sur `origin` au début de la recette. Le commit
immuable a été extrait depuis la branche locale sans modifier le worktree.

## Défaut bloquant

L'ordre nominal demandé n'est pas respecté après apparition d'une catégorie
éligible sur un fresh install :

```text
Attendu : Accueil · Épicerie · Producteurs · Professionnels
Obtenu : Accueil · Producteurs · Épicerie · Professionnels
```

Snapshot ORM final :

```text
Boutique       sequence=10 id=9
Producteurs    sequence=20 id=10
Épicerie       sequence=20 id=12
Professionnels sequence=40 id=19
```

`Producteurs` existe à la séquence 20 avant l'arrivée d'`Épicerie`. La V3
préserve ensuite cette séquence et crée `Épicerie` à la même séquence. L'ordre
effectif dépend alors de l'identifiant ORM et reste faux après plusieurs
resynchronisations. Le défaut est visible sur desktop et dans le drawer mobile.

Reproduction :

1. Installer thème et content sur une base sans catégorie exposable.
2. Activer le thème sur le site.
3. Créer `Épicerie` et trois produits publiés qualifiés.
4. Exécuter `bootstrap_ck_catalogue_navigation(env)` deux fois.
5. Lire les séquences des menus racine ou ouvrir le header.

## Résultats par scénario

| Scénario | Statut | Résultat |
|---|---|---|
| 1. Navigation desktop | **FAIL** | Icône maison, libellés et liens corrects ; ordre faux. Aucun doublon ni ancien menu. |
| 2. Navigation mobile | **FAIL** | Drawer, ouverture/fermeture, enfants, clics et retour arrière fonctionnent ; ordre faux. Aucun débordement (`scrollWidth=390`). |
| 3. Double resynchronisation | **PASS** | Snapshots identiques, aucun doublon, mais l'état stable conserve l'ordre fautif. |
| 4. Renommage catégorie | **PASS** | Même menu/catégorie, nouveau slug correct, aucun ancien libellé ; restauration OK. |
| 5. Renommage manuel menu | **PASS** | Libellé réaligné sur `category.name`, même ID et même catégorie. |
| 6. Séquence BO | **PASS** | Séquence personnalisée `4242` préservée. |
| 7. Publication/éligibilité | **PASS** | Retrait sur dépublication/archivage, recréation sur réactivation, déplacement/restauration enfant corrects. |
| 8. Producteurs/Professionnels | **PASS** | Producteurs fixe ; Professionnels suit la publication de `/professionnels`. |
| 9. Writers R1 | **PASS avec dette confirmée** | `Communauté` et `Tous nos produits` réapparaissent, puis V3 restaure l'état canonique. |
| 10. Parcours minimaux | **PASS** | Catégorie, sous-catégorie, produit, panier/retour catalogue, Producteurs/fiche et Professionnels répondent et s'affichent. |

## Preuves

- `desktop_header_local_theme.png`
- `mobile_drawer_local_theme.png`

Les premières captures utilisant une URL d'assets absolue préprod ont été
écartées. Les preuves retenues ci-dessus ont été rejouées avec
`web.base.url=http://localhost:18180`, thème actif et bundle local.

## Retour Dev

Corriger le traitement des séquences des racines fixes lorsqu'une catégorie
catalogue devient nouvellement éligible, sans perdre la doctrine de préservation
des séquences BO. Rejouer ensuite les dix scénarios sur un nouveau SHA.

Aucune modification de code, aucun commit, push, PR, merge ou déploiement.
