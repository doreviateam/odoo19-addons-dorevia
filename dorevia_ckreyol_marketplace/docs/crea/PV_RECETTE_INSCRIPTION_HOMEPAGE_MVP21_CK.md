# PV — Recette Inscription Homepage MVP2.1

**Ticket** : [TICKET_INSCRIPTION_HOMEPAGE_MVP21.md](TICKET_INSCRIPTION_HOMEPAGE_MVP21.md)  
**Décision position** : [DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md](../mvp_02/DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md)  
**Date recette** : **2026-04-25**  
**Instance** : recette MOA (desktop + mobile)  
**Relecteur MOA** : MOA

---

## Synthèse verdict

**GO MOA** — Bloc **Cercle C-Kreyol** (chantier **4/5**) accepté dans le cadre de la **clôture homepage MVP2.1** ([README MVP 02](../mvp_02/README.md)).

**Implémentation** : `views/snippets/ckr_circle.xml` ; chaînage [`ckr_homepage.xml`](../../views/pages/ckr_homepage.xml) — **après** `ckr_snippet_editorial` lorsque celui-ci est rendu (`ckr_hpage_mvp1_tail_blocks = 1`), sinon **après** `ckr_snippet_selection` ; **avant** `ckr_snippet_trust`.

**Post-recette — correctifs & conformité (2026-04, module ≥ 19.0.1.10.x)** :

- **P0** : correction **`Sub.search` → `sub.search`** dans [`controllers/ckr_circle.py`](../../controllers/ckr_circle.py) (soumissions valides sans `NameError`, redirection `cc_cir=1`).
- **P1 / P2** : politique [`ckr_privacy.xml`](../../views/pages/ckr_privacy.xml) réécrite (information RGPD structurée, plus de ton « MVP à compléter ») ; page **[`/terms`](../../views/pages/ckr_terms.xml)** + `website.page` — mentions légales, **hébergeur** affiché sur la page (coordonnées **OVH SAS** par défaut — **à remplacer** si l’infra réelle diffère) ; tests HTTP [`test_ckr_circle.py`](../../tests/test_ckr_circle.py) alignés (e-mail posté, `/terms`, `/privacy`).

---

## 1. Emplacement et structure

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Bloc **avant** Réassurance ; **après** Éditorial lorsque l’éditorial est affiché | [x] | [ ] | [ ] | Ordre conforme au gel MOA. |
| Composition **split** (visuel / formulaire) desktop | [ ] | [ ] | [x] | **V1** : bloc **centré** (formulaire seul) — validé MOA ; split reporté amélioration continue. |
| **Responsive** mobile lisible | [x] | [ ] | [ ] | **Mobile OK**. |

---

## 2. Formulaire et contenu

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Titre + texte + CTA conformes au périmètre relationnel | [x] | [ ] | [ ] | Cercle C-Kreyol, ton calme. |
| Champ e-mail + préférences **simples** | [x] | [ ] | [ ] | Préférences cases optionnelles. |
| Lien **`/privacy`** avec libellé **politique de confidentialité** (RGPD) | [x] | [ ] | [ ] | Lien sous le formulaire ; page dédiée structurée (voir §2 bis). |
| Soumission ou comportement **conforme** à l’arbitrage technique | [x] | [ ] | [ ] | POST `/ckr/circle/subscribe`, messages retour query `cc_cir`. |

---

## 2 bis. Pages légales liées au formulaire (`/privacy`, `/terms`)

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Route **`/privacy`** accessible (HTTP 200) | [x] | [ ] | [ ] | `website.page` + `ckr_page_privacy` — information des personnes (RGPD) : responsable, finalités, base légale, droits, désinscription, etc. |
| Route **`/terms`** accessible (HTTP 200) | [x] | [ ] | [ ] | `website.page` + `ckr_page_terms` — éditeur, **hébergement** (mentions sur la page), propriété intellectuelle, renvoi `/privacy`, **CGV** (`#cgv`). Footer : `/terms` et `/terms#cgv`. |
| Contenu **relu côté juridique** avant ouverture publique | [ ] | [ ] | [x] | Recommandé : validation MOA / conseil sur textes définitifs et sur l’**hébergeur réel** si différent du bloc **OVH SAS** livré par défaut. |

---

## 3. Contraintes MOA

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Pas de pop-up / réduction / fausse urgence | [x] | [ ] | [ ] | |
| Pas d’image touristique décorative seule | [x] | [ ] | [ ] | Pas de visuel split imposé en V1. |
| Ton calme, non agressif | [x] | [ ] | [ ] | |

---

## 4. Verdict

- [x] **Validé**
- [ ] **Validé sous réserve** *(lister les réserves)*
- [ ] **Refusé** *(motifs)*

**Signature / date** : MOA — **2026-04-25**
