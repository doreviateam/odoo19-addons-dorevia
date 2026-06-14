# Recette QA — Composition CMS CK 01

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Ticket source** | [`ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md`](./ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) |
| **Socle thème** | `dorevia_ck_theme` ticket 01 — clôturé · non modifiable |
| **Instance** | `dorevia_ck_marketone_01` — [`REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md`](./REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md) |
| **URL** | `http://localhost:18079` |
| **Références** | [`note_05.md`](../cadrage/note_05.md) · [`brief_01_2.md`](./maquette_01.2/brief_01_2.md) · [`recette_qa_maquette_01_2.md`](./maquette_01.2/recette_qa_maquette_01_2.md) · [`arbitrage_moa_maquette_01_2.md`](./maquette_01.2/arbitrage_moa_maquette_01_2.md) · [`ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md`](./ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) |
| **Date** | 2026-06-12 |
| **Statut QA** | **Reprise home V1.2 autorisée** — arbitrage MOA 2026-06-13 · recette partielle · revalidation mobile pending |

> **Décision MOA (2026-06-12)** : ticket validé · exécution CMS partielle autorisée.  
> **Arbitrage MOA (2026-06-13)** : [`arbitrage_moa_maquette_01_2.md`](./maquette_01.2/arbitrage_moa_maquette_01_2.md) — **GO traduction Odoo** · reprise home bloc par bloc selon maquette V1.2.

---

## 1. Verdict (partiel — 2026-06-13)

```text
PREUVE DE FAISABILITÉ CMS : OK (hero · univers · amorce Dynamic Products)
HOME COMPLÈTE : REPRISE AUTORISÉE — arbitrage V1.2 · ordre bloc par bloc
OK DESKTOP — KO MOBILE LÉGER (overflow horizontal offcanvas)
→ CORRECTION CIBLÉE TICKET 01 APPLIQUÉE — REVALIDATION MOBILE PENDING
```

Verdict final `OK COMPOSITION CMS CK 01` : **en cours** — après composition home selon hiérarchie V1.2 (note_05 §4 · ticket CMS §0.4).

```text
OK COMPOSITION CMS CK 01
```

ou

```text
KO COMPOSITION CMS CK 01 — corrections CMS à reprendre
```

### Contrôle visuel accueil (MOA — localhost:18079)

| Plateforme | Verdict | Détail |
|------------|---------|--------|
| **Desktop** | ✅ OK | `body.ck-theme` · fond `#fffbf7` · typo fallback · pas d’erreur console · pas d’overflow horizontal · hero · CTA · cartes univers · footer |
| **Mobile** | ⚠️ KO léger | Zone blanche / scroll horizontal à droite — voir §6 |

---

## 2. Prérequis

| # | Prérequis | Statut |
|---|-----------|--------|
| 1 | Socle ticket 01 validé (install/QWeb/visuel) | ✅ |
| 2 | Ticket MOA composition CMS validé MOA | ✅ 2026-06-12 |
| 3 | Exécution CMS autorisée (home V1.2 — reprise bloc par bloc) | ✅ |
| 3b | Maquette V1.2 « Boutique élégante » validée MOA/QA | ☐ — prérequis reprise home |
| 4 | Thème `dorevia_ck_theme` actif sur website | ☐ |
| 5 | Données BO minimales (§4 ticket MOA) | ☐ |
| 6 | Aucune modification module `dorevia_ck_theme` | ☐ à vérifier post-exécution |

---

## 3. Checklist recette

### 3.1 Composition accueil

> **Pause note_05** : checklist home complète suspendue jusqu’à maquette V1.2. État instance au 2026-06-13 ci-dessous.

| # | Point | Statut | Note |
|---|-------|--------|------|
| 1 | Page accueil composée Website Builder | ⚠️ | Partielle — preuve faisabilité |
| 2 | Snippet hero CK (`s_ck_hero`) | ✅ | H1 + CTAs `/shop` · `/professionnels` |
| 3 | Snippet liens / univers (`s_ck_category_links`) | ⚠️ | `s_product_list` + cards — pas `s_ck_category_links` |
| 4 | Snippet réassurance (`s_ck_reassurance`) | ☐ | Absent — requis V1.2 §4 |
| 5 | Bandeau / appel Pro (`s_ck_pro_banner` ou CTA) | ☐ | Absent |
| 6 | Snippets éditables en mode Modifier | ☐ | |
| 7 | Ordre blocs conforme hiérarchie V1.2 (note_05 §4) | ☐ | Reprise en cours |

### 3.2 Produits vedettes

| # | Point | Statut | Note |
|---|-------|--------|------|
| 7 | Vedettes via **Dynamic Products** ou **Products** natif | ☐ | |
| 8 | Sélection = config éditoriale Builder / snippet — pas de logique custom | ☐ | |
| 9 | Produits publiés visibles sur accueil | ☐ | |
| 10 | Zone `oe_structure` snippet vedettes alimentée | ☐ | |

### 3.3 Page `/professionnels`

| # | Point | Statut | Note |
|---|-------|--------|------|
| 11 | Page CMS `/professionnels` créée et publiée | ✅ | [`COMPOSITION_PROFESSIONNELS_V1_2.md`](./maquette_01.2/COMPOSITION_PROFESSIONNELS_V1_2.md) |
| 12 | Double cible Pro claire (fournisseur · distributeur) | ☐ | |
| 13 | Doctrine CK et distinction B2C public / B2B back-office | ☐ | |
| 14 | Deux blocs · deux CTA · un formulaire (UX MOA) | ☐ | |

### 3.4 Formulaire `website_crm`

| # | Point | Statut | Note |
|---|-------|--------|------|
| 15 | Formulaire CRM natif présent sur page Pro | ☐ | |
| 16 | **Pas de champ CRM custom** créé pour ce ticket | ☐ | |
| 17 | Qualification Pro via message / description lead si besoin | ☐ | |
| 18 | Soumission formulaire → lead CRM créé | ☐ | |

### 3.5 Menu et liens

| # | Point | Statut | Note |
|---|-------|--------|------|
| 19 | Menu **Professionnels** → `/professionnels` | ✅ | Header V1.2 · seq. 30 · [`COMPOSITION_HEADER_V1_2.md`](./maquette_01.2/COMPOSITION_HEADER_V1_2.md) |
| 20 | CTA accueil / bandeau shop → liens cohérents | ☐ | |
| 21 | Pas de liens morts | ☐ | |

### 3.6 Responsive

| # | Point | Statut | Note |
|---|-------|--------|------|
| 22 | Accueil mobile — smoke test | ⚠️ | KO overflow horizontal · correction §6 appliquée · revalidation pending |
| 23 | Page Pro mobile — smoke test | ☐ | |

### 3.7 Non-régression socle

| # | Point | Statut | Note |
|---|-------|--------|------|
| 24 | `/shop` — template `website_sale` natif | ☐ | |
| 25 | Fiche produit — buy box natif | ☐ | |
| 26 | Panier / checkout natifs | ☐ | |
| 27 | `body.ck-theme` · styles CK actifs | ☐ | |
| 28 | Pas de B2B UI · pas de pricelist publique | ☐ | |
| 29 | Pas de modification `dorevia_ck_theme` hors correction ciblée | ⚠️ | Correction overflow mobile §6 (layout natif offcanvas) |
| 30 | Pas d’extension hors ticket 01 | ☐ | |

---

## 6. Correction ciblée — overflow mobile offcanvas (2026-06-13)

**Constat** : viewport `390px` · `document.scrollWidth` ~`732px` · zone blanche à droite.

**Cause** : offcanvas mobile Odoo fermé — `#top_menu_collapse_mobile.offcanvas.offcanvas-end.o_navbar_mobile` — positionné hors écran (`x=390`, `width=342`) mais contribue à la largeur scrollable.

**Correctif** (`dorevia_ck_theme/static/src/scss/website.scss`) :

```scss
@media (max-width: 991.98px) {
    .ck-theme { overflow-x: clip; }
    .ck-theme #wrapwrap { overflow-x: clip; max-width: 100%; }
}
```

**Instance** : `odoo -u dorevia_ck_theme` · purge assets frontend · restart.

**Revalidation MOA** : hard refresh mobile · confirmer `scrollWidth === clientWidth` · plus de bande blanche à droite.

> Correction **layout ticket 01** (interaction thème CK + navbar native Odoo) — hors contenu CMS · ne couvre pas les autres points checklist.

---

## 7. Pause home — note_05 (2026-06-13)

Référence : [`note_05.md`](../cadrage/note_05.md) · ticket CMS §0.3

**Documents maquette V1.2** (prérequis reprise home) :

| Document | Rôle |
|----------|------|
| [`brief_01_2.md`](./maquette_01.2/brief_01_2.md) | Commande maquette · critères d’acceptation |
| [`recette_qa_maquette_01_2.md`](./maquette_01.2/recette_qa_maquette_01_2.md) | Grille QA · verdict avant reprise Odoo |
| [`go_moa_maquette_01_2.md`](./maquette_01.2/go_moa_maquette_01_2.md) | **GO OFFICIEL MOA** — Move 3 · production en cours |

```text
La recette home complète reprend selon arbitrage MOA V1.2 — GO traduction Odoo.
Référence : arbitrage_moa_maquette_01_2.md · ticket CMS §0.4
Critères de reprise : qualité perçue + efficacité commerciale (produits · prix · réassurance · conversion).
```

**En parallèle** : §3.3 `/professionnels` · §3.4 CRM · §3.5 menu · §3.7 non-régression · revalidation mobile §6.

---

## 4. Hors périmètre recette

```text
pixel-perfect maquette V1.1.1 · typo Fraunces/DM Sans prod · origines/collections custom
B2B custom · pricelists · portail · catalogue parallèle
```

---

## 5. Prochaine étape

```text
1. ✅ Maquette V1.2 — recette + arbitrage MOA actés
2. ⏳ Revalidation mobile accueil post-correction overflow (§6)
3. ✅ Page /professionnels + menu Pro — [`COMPOSITION_PROFESSIONNELS_V1_2.md`](./maquette_01.2/COMPOSITION_PROFESSIONNELS_V1_2.md)
4. ☐ Reprise home — ⏸ pause maquette V1.2.1 · [`go_moa_maquette_v1_2_1.md`](./maquette_01.2/go_moa_maquette_v1_2_1.md)
5. ☐ Verdict tracé — OK ou KO composition CMS CK 01
```

---

*Recette QA composition CMS CK 01 — GO traduction Odoo V1.2 · recette partielle MOA 2026-06-13.*
