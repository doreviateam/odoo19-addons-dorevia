# PV — Recette Inscription Homepage MVP2.1

**Ticket** : [TICKET_INSCRIPTION_HOMEPAGE_MVP21.md](TICKET_INSCRIPTION_HOMEPAGE_MVP21.md)  
**Décision position** : [DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md](../mvp_02/DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md)  
**Date recette** : **2026-04-25**  
**Instance** : recette MOA (desktop + mobile)  
**Relecteur MOA** : MOA

---

## Synthèse verdict

**GO MOA** — Bloc **inscription / relationnel** C-Kreyol (chantier **4/5**) accepté dans le cadre de la **clôture homepage MVP2.1** ([README MVP 02](../mvp_02/README.md)), à l’époque sous le libellé **« cercle »** ; depuis **2026-05** la refonte **[TICKET_REFONTE_BLOC_NEWSLETTER_HOMEPAGE_CK.md](TICKET_REFONTE_BLOC_NEWSLETTER_HOMEPAGE_CK.md)** aligne copy, UX et **`mass_mailing`**.

**Implémentation** : `views/snippets/ckr_circle.xml` ; chaînage [`ckr_homepage.xml`](../../views/pages/ckr_homepage.xml) — **après** `ckr_snippet_editorial` lorsque celui-ci est rendu (`ckr_hpage_mvp1_tail_blocks = 1`), sinon **après** `ckr_snippet_selection` ; **avant** `ckr_snippet_trust`.

**Post-recette — correctifs & conformité (2026-04, module ≥ 19.0.1.10.x)** :

- **P0** : correction **`Sub.search` → `sub.search`** dans [`controllers/ckr_circle.py`](../../controllers/ckr_circle.py) (soumissions valides sans `NameError`, redirection `cc_cir=1`).
- **P1 / P2** : politique [`ckr_privacy.xml`](../../views/pages/ckr_privacy.xml) réécrite (information RGPD structurée, plus de ton « MVP à compléter ») ; page **[`/terms`](../../views/pages/ckr_terms.xml)** + `website.page` — mentions légales, **hébergeur** affiché sur la page (coordonnées **OVH SAS** par défaut — **à remplacer** si l’infra réelle diffère) ; tests HTTP [`test_ckr_circle.py`](../../tests/test_ckr_circle.py) alignés (e-mail posté, `/terms`, `/privacy`).

**Refonte bloc newsletter (2026-05 — module ≥ 19.0.1.10.69)** — ticket [TICKET_REFONTE_BLOC_NEWSLETTER_HOMEPAGE_CK.md](TICKET_REFONTE_BLOC_NEWSLETTER_HOMEPAGE_CK.md) :

- Copy **NEWSLETTER** + promesse horizontale ; plus de « cercle » ni de préférences cases à cocher ; texte RGPD long sous filet (pas de lien obligatoire `/privacy` dans ce bloc).
- POST **`/ckr/circle/subscribe`** inchangé côté URL ; retours **`?cc_nl=`** (`ok` \| `dup` \| `invalid` \| `err`) — **remplace** l’ancien jeu **`cc_cir`** pour ce formulaire.
- Persistance : **`mass_mailing`**, liste **Newsletter C-Kreyol** ; tests `dorevia_ckr_circle` mis à jour sur **`mailing.contact`**.

> Le tableau §2 ci-dessous décrit la **recette MVP2.1 d’avril 2026** ; pour le contrôle des critères post-refonte, se référer au **ticket de refonte** et au **README** module.

---

## GO visuel desktop & gel UI newsletter (2026-05)

**GO MOA — rendu desktop du bloc newsletter** : équilibre validé après itérations fines sur la zone formulaire (module **≥ 19.0.1.10.76** — `_newsletter.scss`). Gel convenu : **ne pas** augmenter davantage le `margin-top` du formulaire pour l’instant ; colonne formulaire desktop **× 1,5** sur la base **24 / 28 rem** ; label **NEWSLETTER** en sauge + filet ambre (aligné « En pratique ») ; label champ **E-mail** masqué visuellement, accessible ; bouton **S’inscrire** terracotta inchangé ; espacement newsletter → **Quelques repères** via sélecteur adjacent conservé.

### Recette finale à confirmer sur instance

| Point | Action |
|-------|--------|
| **Mobile** | Confirmer viewport &lt; 768px : empilement, bouton pleine largeur, absence des réglages desktop-only (marge formulaire, largeur ×1.5). |
| **Inscription Odoo** | Vérifier **`mass_mailing`** : contact sur la liste **Newsletter C-Kreyol** après soumission réelle ; module à jour (`-u`). |
| **États** | Tester retours **`?cc_nl=`** : `ok`, `dup`, `invalid`, `err` et messages affichés dans le bloc. |
| **Accessibilité** | Contrôler lecteur d’écran : association label **`ckr-newsletter__label-vh`** ↔ champ **`ckr-newsletter-email`** ; placeholder non seul comme nom accessible. |

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
| Soumission ou comportement **conforme** à l’arbitrage technique | [x] | [ ] | [ ] | **2026-04** : `cc_cir` ; **≥ 19.0.1.10.69** : `cc_nl` + `mailing.contact` (voir § refonte en tête de ce PV). |

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
