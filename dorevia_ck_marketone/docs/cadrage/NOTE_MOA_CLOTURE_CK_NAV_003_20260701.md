# Note MOA — Clôture CK-NAV-003 — Navigation catalogue dynamique

| Champ | Valeur |
| --- | --- |
| Date | 1 juillet 2026 |
| Projet | C-Kréyòl Marketone — navigation header |
| Destinataires | MOA, Produit, QA, Dev |
| Statut | **GO recette / GO commit / GO push** |
| Commit de référence | `c0c196de` — `feat(ck-nav): CK-NAV-003 navigation catalogue dynamique` |
| Module | `dorevia_ck_marketone_content` |
| Version livrée | `19.0.1.73.0` |
| Base recette | `dorevia_ck_marketone_01` |

---

## Décision MOA confirmée

La navigation CK repose désormais sur un catalogue dynamique construit depuis les catégories e-commerce Odoo, sans retour au mega-menu éditorial.

Doctrine validée :

- `Boutique` reste une entrée fixe.
- Les catégories e-commerce racines publiées/visibles alimentent la navigation principale.
- Les sous-catégories directes sont affichées en dropdown simple, profondeur maximale 2.
- `Producteurs` est toujours présent, via la route contrôleur `/producteurs`.
- `Professionnels` reste conditionnel selon la visibilité de la page CMS `/professionnels`.
- Aucun mega-menu ni classe CSS legacy ne doit être conservé sur ces entrées.

---

## Correction appliquée

Dans `sync_ck_catalogue_navigation_for_website`, l'entrée `Producteurs` est traitée en upsert inconditionnel.

`Professionnels` conserve son comportement conditionnel via `_page_url_visible`.

La méthode `_upsert_menu` remet déjà `is_mega_menu=False` et `ck_nav_css_class=False` par défaut. Aucun reset additionnel n'est nécessaire.

---

## Recette post-correction

Contrôles effectués sur `c0c196de`.

| Contrôle | Résultat |
| --- | --- |
| Upgrade `-u dorevia_ck_marketone_content` | OK, sans exception bloquante |
| Tests ciblés `dorevia_ck_nav_catalogue,dorevia_ck_nav_v1,dorevia_ck_marketone_nav_sync` | 42 post-tests, 0 failed, 0 error |
| Bootstrap ORM explicite `bootstrap_ck_catalogue_navigation(env)` | 1 site synchronisé |
| Vérification DB | `Producteurs` restauré en `/producteurs`, séquence 60 ; `Professionnels` séquence 70 |
| Mega-menu / CSS legacy | Absent |
| Profondeur navigation | Max 2 respectée |
| Front desktop | Navigation complète visible |
| Front mobile 390 px | Navigation complète visible, sans overflow horizontal |
| Console front | Aucune erreur bloquante constatée |

### Navigation validée

Navigation observée après synchronisation :

`Boutique · Épicerie · Soin & Bien-être · Artisanat · Boissons · Producteurs · Professionnels`

---

## Nuance opérationnelle

Sur une base déjà en `19.0.1.73.0`, un simple `-u` ne rejoue pas `post-migrate.py`.

Pour appliquer la correction sans bump de version, le bootstrap ORM explicite est le bon levier :

```python
from odoo.addons.dorevia_ck_marketone_content.nav_sync import bootstrap_ck_catalogue_navigation
bootstrap_ck_catalogue_navigation(env)
```

Ce point est à conserver comme note d'exploitation pour les recettes ou reprises de base équivalentes.

---

## Point de surveillance

Un retry PostgreSQL transitoire `SerializationFailure` a été observé pendant la chauffe/reprise serveur.

Aucun impact front bloquant n'a été constaté sur la base CK. Ce point est considéré comme un incident infra passager, hors régression CK-NAV-003.

---

## Verdict final

**CK-NAV-003 est clôturé en GO.**

Le lot est validé fonctionnellement, techniquement et visuellement.

Doctrine MOA confirmée :

**Producteurs toujours présent · Professionnels conditionnel · navigation catalogue dynamique Odoo · pas de mega-menu legacy.**
