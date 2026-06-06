# Workflow — maquetter et ameliorer CK au fil de l'eau

Objectif : faire evoluer la maquette et la boutique **par petites iterations**, sans big-bang, en gardant une trace dans le depot et une source de verite dans Open Design.

## Principes

1. **Premium Odoo d'abord** — la maquette prolonge la ligne deja validee en prod (MOA UX-3 B1.4, tuiles, preview). Voir [CADRAGE_PREMIUM_MAQUETTE_ODOO.md](../00_brief/CADRAGE_PREMIUM_MAQUETTE_ODOO.md).
2. **Le produit d'abord** — chaque iteration doit clarifier l'achat avant le recit.
3. **Une iteration = un sujet** — ex. « drawer mobile », pas « refonte totale ».
4. **Open Design genere** — Cursor accompagne (prompt, relecture, sync, mapping Odoo). Mettre a jour la memoire OD via [MEMOIRE_OPEN_DESIGN_PREMIUM.txt](../00_brief/MEMOIRE_OPEN_DESIGN_PREMIUM.txt).
5. **Odoo suit quand c'est arbitré** — la maquette precede ou aligne le SCSS/XML, elle ne contredit pas les invariants [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md).
6. **Export git apres chaque run OD valide** — pour MOA, recette et historique.

## Boucle standard (15–45 min)

```text
1. Choisir 1 item dans 02_backlog/BACKLOG_MAQUETTE.md
2. Remplir 03_prompts/PROMPT_ITERATION_TEMPLATE.md (ou demander a Cursor)
3. Open Design : meme projet 44de8203-... — skill prototype — coller le prompt
4. Preview + critique panel OD
5. Si OK : sync export + note journal backlog
6. Si arbitrage MOA requis : pause implementation Odoo
7. Sinon : ticket / lot SCSS cible (1 fichier prefere)
```

## Sync export → depot

```bash
cp "/Users/doreviateam/open-design/.od/projects/44de8203-38b0-4405-af76-2f09c97c5f02/index.html" \
  "/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/maquette_ck_marketone/04_exports_open_design/piste_1_marche_creole_contemporain/index.html"

cp "/Users/doreviateam/open-design/.od/projects/44de8203-38b0-4405-af76-2f09c97c5f02/critique.json" \
  "/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ckreyol_marketone/docs/maquette_ck_marketone/04_exports_open_design/piste_1_marche_creole_contemporain/critique_open_design.json"
```

Preview locale :

```bash
open "docs/maquette_ck_marketone/04_exports_open_design/piste_1_marche_creole_contemporain/index.html"
```

## Quand passer du HTML au code Odoo

| Signal | Action |
|--------|--------|
| Maquette stable sur une zone | Implementer le lot SCSS/XML correspondant |
| Ecart tokens maquette / MOA | Arbitrage : hybride (structure maquette + `$ck-*` dans `_tokens_colors.scss`) |
| Recette UX deja verte sur la zone | Ne pas regresser ; la maquette s'aligne sur le comportement valide |
| Nouvelle page (Savoirs) | Maquette d'abord, route Odoo ensuite |

References implementation :

- Tokens : `static/src/scss/_tokens_*.scss`
- Boutique : `_shop.scss`, `_shop_product_cards.scss`, `_shop_sidebar.scss`
- Brief image : `docs/cadrage/DOCTRINE_IMAGE_V2.md`

## Accompagnement Cursor (comment demander)

Exemples de messages utiles :

- « Iteration backlog M-03 — prepare le prompt Open Design »
- « Relecture webdesign du dernier export CK »
- « Sync maquette OD → repo et mets a jour le journal »
- « Mapping tuile produit maquette → `_shop_product_cards.scss` »

Joindre si possible : numero backlog, capture, ou « ce qui ne va pas » en une phrase.

## Memoire Open Design

Fichiers deja presents dans `/Users/doreviateam/open-design/.od/memory/` :

- `project_c_kreyol_marketone.md`
- `project_c_kreyol_design_direction.md`
- `project_c_kreyol_prototype_audience.md`

Apres une decision forte (palette MOA, typo finale), mettre a jour ces fichiers dans OD pour que les prochains runs restent coherents.

## Pistes visuelles (coexistence)

| Piste | Statut | Dossier export |
|-------|--------|----------------|
| 1 — Marche creole contemporain | **Active** (projet OD actuel) | `04_exports_open_design/piste_1_marche_creole_contemporain/` |
| 1 bis — Meme structure, tokens MOA | A planifier | `piste_1bis_artisanal_terroir/` (a creer) |
| 2 — Savoirs + etats vides | Backlog | — |

Ne pas ecraser la piste 1 tant que la 1 bis n'est pas validee ; dupliquer le dossier export pour comparer.
