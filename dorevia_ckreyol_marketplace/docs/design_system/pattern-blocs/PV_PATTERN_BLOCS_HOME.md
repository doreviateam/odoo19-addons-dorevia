# PV — Cartographie Home en pattern-blocs (clôture de passe documentaire)

| Champ | Valeur |
| --- | --- |
| **Nature** | Note de clôture — **documentation uniquement** |
| **Périmètre** | Homepage C-Kreyol + composants globaux servant la Home (**header**, **footer**) |
| **Statut** | **Actée** |

---

## 1. Décision

- La **Home CK** est désormais la **première source de référence** pour l’inventaire et les **pattern-blocs** du module [`INVENTAIRE_HOME_PATTERN_BLOCS.md`](./INVENTAIRE_HOME_PATTERN_BLOCS.md)).
- Les **blocs principaux visibles** de la lecture Home (avec header et footer de layout global) sont **documentés** par des fichiers `PATTERN_BLOC_*` dédiés ou préexistants, alignés sur le code lorsque pertinent.
- Cette passe est **exclusivement documentaire** : **aucune refonte** de parcours, **aucun changement runtime**, **aucune création** de snippet Odoo déposable dans l’éditeur Website n’a été livrée dans ce cadre — seule la **capitalisation conception / recette** est actée.

---

## 2. Pattern-blocs couverts (colonne vertébrale Home)

Références dans ce dossier :

| Document |
| --- |
| [`PATTERN_BLOC_HEADER_NAV_3_NIVEAUX.md`](./PATTERN_BLOC_HEADER_NAV_3_NIVEAUX.md) |
| [`PATTERN_BLOC_HOME_HERO.md`](./PATTERN_BLOC_HOME_HERO.md) |
| [`PATTERN_BLOC_HOME_EXPLORER_PORTES.md`](./PATTERN_BLOC_HOME_EXPLORER_PORTES.md) |
| [`PATTERN_BLOC_HOME_SELECTION_PRODUITS.md`](./PATTERN_BLOC_HOME_SELECTION_PRODUITS.md) |
| [`PATTERN_BLOC_HOME_NEWSLETTER.md`](./PATTERN_BLOC_HOME_NEWSLETTER.md) |
| [`PATTERN_BLOC_HOME_EN_PRATIQUE.md`](./PATTERN_BLOC_HOME_EN_PRATIQUE.md) |
| [`PATTERN_BLOC_FOOTER_RESPONSIVE.md`](./PATTERN_BLOC_FOOTER_RESPONSIVE.md) |

---

## 3. Distinctions à maintenir

Conformément à [`../README.md`](../README.md) :

- **Pattern-bloc** — référence **UX/UI** documentée sous `docs/design_system/pattern-blocs/` ;
- **Template QWeb** — implémentation **technique modularisée** (fichiers `views/`, chaînés par `t-call` ou héritage) ;
- **Snippet Odoo (éditeur)** — bloc **réellement réutilisable / déposable** dans l’éditeur Website après enregistrement Odoo approprié — **non équivalent** au seul préfixe de nom `ckr_snippet_*` dans le code CK.

Ne pas extrapoler automatiquement : *pattern documenté ⇒ snippet déposable*.

---

## 4. Candidats futurs à « vrais » snippets Odoo (hypothèses, hors lancement)

Décisions ultérieures, **sans mandatement** dans ce PV :

- **`HOME_EN_PRATIQUE`** (réassurance) — forte réutilisation éditoriale potentielle ;
- **`HOME_NEWSLETTER`** (captation douce) ;
- **`HOME_HERO`** ou **hero éditorial dérivé** — si besoin dupliquer une promesse ailleurs qu’à la racine `/` ;
- **`HOME_EXPLORER_PORTES`** — si une page éditoriale doit reprendre le même tableau d’orientation sans dupliquer le QWeb à la main.

Chaque passage en snippet Odoo nécessitera : périmètre BO, données, tests, régression layout.

---

## 5. Points volontairement hors scope de cette passe

- **Blocs Home Fournisseur / Éditorial** — encore présents en template sous **flag** `ckr_hpage_mvp1_tail_blocks` (**masqués par défaut**) ; pas de fiches pattern-blocs canoniques tant que MOA / gel ne rouvrent pas ce socle ;
- **Gouvernance header N2** — barre desktop **vs** drawer **`website.menu_id`** ; alignement fonctionnel hors clôture documentaire présente ;
- **Transformation généralisée en snippets Odoo déposables** — non engagée ;
- **Patterns** boutique `/shop`, fiche produit, panier, checkout — hors cartographie « Home » de ce PV ;
- **Smoke HTTP live** avec **serveur persistant** — preuves d’intégration documentées ailleurs (procédures module) ;
- **E2E marchand élargi** au-delà du scénario minimal pré-ouverture — tickets dédiés (P4 / suites futures).

---

## Conclusion

La **cartographie principale** de la **Home CK** en **pattern-blocs** est considérée **complète** pour le palier actuel ; les évolutions suivantes passeront par **nouveaux tickets**, **nouveaux fichiers pattern-bloc** ou **révision** des existants après changement MOA ou code.
