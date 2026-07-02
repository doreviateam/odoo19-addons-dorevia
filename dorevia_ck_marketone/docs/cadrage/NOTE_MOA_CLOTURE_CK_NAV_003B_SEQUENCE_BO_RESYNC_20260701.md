# NOTE MOA — Clôture CK-NAV-003b — Séquence BO préservée au resync catalogue

| Champ | Valeur |
| --- | --- |
| Date | 1 juillet 2026 |
| Projet | C-Kréyòl Marketone — navigation header |
| Destinataires | MOA, Produit, QA, Dev |
| Statut | **GO recette / GO commit** |
| Module | `dorevia_ck_marketone_content` |
| Base recette | `dorevia_ck_marketone_01` — http://localhost:18079 |

---

## Objet

Complément de gouvernance à CK-NAV-003.

CK-NAV-003 alimente déjà dynamiquement la navigation catalogue depuis les catégories e-commerce Odoo. Le présent correctif garantit qu'un ordre administré manuellement dans les menus website BO n'est plus écrasé lors d'un resync catalogue.

---

## Décision MOA

GO recette / GO commit.

Après création initiale, la séquence d'un menu website existant devient administrable depuis le BO. Le resync catalogue conserve cette séquence existante, tout en continuant de resynchroniser les données pilotées par le catalogue/code : nom, URL, rattachement catégorie et contenu menu.

---

## Périmètre livré

| Fichier | Modification |
| --- | --- |
| `nav_sync.py` | `preserve_existing_sequence` sur `_upsert_menu` ; activation ciblée sur le chemin catalogue CK-NAV-003 ; préservation des séquences BO pour catégories, Producteurs et Professionnels ; cleanup limité aux catégories non éligibles |
| `test_ck_nav_catalogue_sync.py` | Préservation séquence BO au resync ; cas Producteurs ; nouvelle catégorie publiée sans perturbation des séquences existantes |

---

## Recette

| Contrôle | Résultat |
| --- | --- |
| `dorevia_ck_nav_catalogue` | 24 post-tests, 0 failed, 0 error |
| Non-régression élargie catalogue + v1 + nav_sync | 45 post-tests, 0 failed, 0 error |
| `git diff --check` | OK |
| Conteneur 18079 | Up |

---

## Réserve documentaire

Ce lot est tracé comme **CK-NAV-003b** afin d'éviter la confusion avec la note CK-NAV-004 déjà utilisée pour le lot thème centrage + icône Boutique.

---

## Verdict

**GO MOA confirmé.**
