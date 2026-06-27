# Note d'intervention QA — Note 08 · Fiche produit CK V1.1

| Champ | Valeur |
| --- | --- |
| **Projet** | `dorevia_ck_marketone` · C-Kréyòl / CK |
| **Lot** | Note 08 — Modèle de données & architecture d'information fiche produit B2C |
| **Référence MOA** | [`note_08.md`](../../cadrage/note_08.md) |
| **Retour Dev** | [`note_08_reponse.md`](../../cadrage/note_08_reponse.md) |
| **Checklist MOA** | Checklist Recette MOA Note 08 (8 passes) |
| **Verdict Dev pré-rempli** | [`RECETTE_QA_NOTE_08_VERDICT.md`](./RECETTE_QA_NOTE_08_VERDICT.md) |
| **Instance cible** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Modules** | `dorevia_ck_marketone_content` **19.0.1.53.1** · `dorevia_ck_theme` (SCSS/JS fiche produit) |
| **Statut Dev** | **✅ Livré · recette QA clôturée 27 juin 2026** |
| **Statut QA** | **✅ GO avec réserves — 27 juin 2026** |
| **Estimation QA** | **1,5 à 2 j-h** (BO + front desktop + mobile 390 px + non-régression ciblée) |
| **Émetteur** | Dev expert Odoo |
| **Destinataire** | QA expert Odoo |

---

## Guide simple (lire en premier)

Ce lot pose le **socle fiche produit CK B2C V1.1** :

- nouveaux champs BO produit / producteur / badges ;
- zone haute structurée (catégorie, meta, accroche, badges, prix, variantes, réassurance V1) ;
- sections sous ligne de flottaison avec **ancres conditionnelles** : Découvrir · Composition · Conservation · Infos pratiques · Producteur ;
- **repli transitoire** : si `ck_discover_html` est vide, le parser `website_description` (Lot 2) reste actif pour le catalogue seed.

**Produits pivot recette**

| Rôle | Produit / partenaire | Pourquoi |
| --- | --- | --- |
| Variantes + prix absolus | **Manio Crackers** (Salé / Sucré) | 2 variantes, prix 3,60 € / 3,50 €, meta « Guadeloupe · La Platine · 100 g · xx €/kg » |
| Producteur | **La Platine** (`res.partner`) | Bloc Producteur + lien meta `#ck-section-producer` |
| Fallback seed | **Confiture de goyave** | `website_description` structuré sans champs V1.1 renseignés |
| Produit minimal | tout produit publié sans champs CK | non-régression fiche standard |

**Règles absolues MOA**

- aucune ancre vide ;
- pas de `qty_available` / `virtual_available` en front ;
- pas de « remboursement 30 jours » ;
- pas de delta prix variantes (`-0,10 €`) comme info centrale ;
- badges uniquement si sélectionnés en BO — pas de Bio / Sans gluten / etc. par défaut.

---

## 1. Mise en route (obligatoire avant recette écran)

### 1.1 Accès instance

| Paramètre | Valeur |
| --- | --- |
| URL | http://localhost:18079 |
| Base | `dorevia_ck_marketone_01` |
| Conteneur (réf.) | `sandbox-odoo19-odoo-1` |
| Cache-bust | `?qa_ts=note08` sur chaque URL contrôlée |

### 1.2 Mise à jour modules

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 \
  -u dorevia_ck_marketone_content,dorevia_ck_theme --stop-after-init

docker restart sandbox-odoo19-odoo-1
```

**Attendu post-update**

- menu **Badges produit CK** visible (Ventes / catalogue) ;
- onglet **Ventes** produit CK avec blocs Accroche · Origine & producteur · Contenu fiche · Infos pratiques ;
- onglet partenaire **Producteur CK** sur `res.partner`.

### 1.3 Rejeu tests auto (gate entrée QA)

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --test-enable --stop-after-init --http-port=8078 \
  --test-tags dorevia_ck_product_page_note08_recette
```

Puis non-régression fiche produit Lot 2 :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --test-enable --stop-after-init --http-port=8078 \
  --test-tags dorevia_ck_product_page_note08,dorevia_ck_product_page_tabs,dorevia_ck_product_page_lot2_front
```

| Contrôle pré-recette | Attendu | Statut QA |
| --- | --- | --- |
| Modules à jour (`53.1`) | 0 erreur bloquante au `-u` | ✅ |
| Tests `note08_recette` | `0 failed, 0 error(s)` | ✅ 14/14 |
| Tests Lot 2 front | `0 failed, 0 error(s)` | ✅ 29/29 (après correction BUG-N08-001) |
| Instance HTTP 200 | `/shop` + fiche Manio OK | ✅ |

⚠️ Si les tests passent mais la fiche est visuellement inchangée : vérifier que le code local est bien monté dans le conteneur (addons path / volume).

### 1.4 Script visuel automatisé (optionnel mais recommandé)

```bash
cd odoo19-addons-dorevia/dorevia_ck_marketone/docs/design/maquette_01.2/scripts

CK_BASE_URL=http://localhost:18079 \
CK_DB=dorevia_ck_marketone_01 \
CK_MANIO_PATH=/shop/manio-crackers-1 \
CK_SCREENSHOT=1 \
node ck_note08_recette_qa.mjs
```

**Sortie attendue** : `pass: true` · captures dans `captures/note08_recette/`.

---

## 2. Périmètre QA

### 2.1 Inclus

| Zone | Contrôles principaux |
| --- | --- |
| BO produit | champs Note 08 · absence champs interdits · domaine producteur |
| BO badges | référentiel seed · champs gouvernance |
| BO producteur | La Platine · onglet Producteur CK |
| Front zone haute | Manio · meta · accroche · badges · CTA · réassurance V1 |
| Prix / variantes | prix contextualisé · prix/kg · prix absolus Salé/Sucré |
| Sections / ancres | ordre fixe · affichage conditionnel · fallback seed |
| Mobile 390 px | overflow · CTA · ancres · empilement |
| Non-régression | Home cards · Shop · fiche sans champs CK |

### 2.2 Hors périmètre (ne pas bloquer le lot)

- B2B fiche produit · devis pro · tarifs revendeurs ;
- avis clients · recommandations avancées ;
- workflow validation réglementaire badges ;
- fiche producteur CMS complète ;
- refonte checkout.

---

## 3. Recette BO — Passe 1 & 2

**Fiche produit** : Manio Crackers · **Partenaire** : La Platine.

| # | Contrôle | Attendu | ☐ | Note QA |
| ---: | --- | --- | --- | --- |
| B1 | Champs Ventes CK visibles | `description_ecommerce`, `ck_producer_id`, `ck_badge_ids`, champs contenu, `ck_packaging_label`, quantité nette | ✅ | Tous présents — tests + API confirmés |
| B2 | Champs interdits absents | pas de `x_*`, `ck_origin_id`, `ck_logistics_note`, etc. | ✅ | `test_forbidden_fields_not_created` passé |
| B3 | Domaine producteur | `ck_producer_id` ne propose que `ck_is_producer = True` | ✅ | Domain API confirmé |
| B4 | La Platine producteur | `ck_is_producer` coché · accroche · libellé géo renseignés | ✅ | **R3 levée** — SARL La Platine (id=1405) seedée : `ck_is_producer=True` · "Sainte-Anne, Guadeloupe" · accroche courte |
| B5 | Badges seed | Guadeloupe · Fécule de manioc · Producteur identifié | ✅ | 3 badges Manio confirmés : [1, 24, 3] · badge `Fécule de manioc` (id=24) créé 27/06 |
| B6 | Accroche longue (~300 car.) | rendu front desktop + mobile sans casse majeure | ✅ | **R1 levée** — `@api.constrains` ≤255 char + `line-clamp: 3` front (19.0.1.54.0) |

---

## 4. Recette front desktop — Passes 3 à 6

**URL pivot** : fiche **Manio Crackers** · viewport **1280 × 800**.

| # | Contrôle | Attendu | ☐ | Note QA |
| ---: | --- | --- | --- | --- |
| F1 | Catégorie front | chips depuis `public_categ_ids` · pas `categ_id` | ✅ | `ck-product-purchase__chips` · chip "Biscuits" confirmé |
| F2 | Meta ligne | origine · **La Platine** (lien `#ck-section-producer`) · 100 g · prix/kg | ✅ | `"SARL La Platine · 100 g · 36,00 €/kg"` · `metaHasProducerLink: true` — **R3 levée** |
| F3 | Accroche | `description_ecommerce` | ✅ | "Crackers salés à la fécule de manioc..." (seed R3) |
| F4 | Badges | uniquement badges BO · pas Bio/Sans gluten par défaut | ✅ | `hasBadges: true` — 3 badges front (Guadeloupe · Fécule de manioc · Producteur identifié) — **R3 levée** |
| F5 | Réassurance V1 | 3 lignes MOA · **pas** remboursement 30 jours | ✅ | "En stock" · "Livraison suivie" · "Retour selon CGV" — script confirmé |
| F6 | Comparaison | bouton comparaison **absent** · favori présent | ✅ | `hasCompare: false` · wishlist présent — script confirmé |
| F7 | Variantes Manio | Salé **3,60 €** · Sucré **3,50 €** · **pas** de delta `-0,10 €` | ✅🔧 | Prix absolus OK · delta disparu — **BUG-N08-002 corrigé** |
| F8 | Prix principal | suit variante sélectionnée (natif Odoo) | ✅ | natif Odoo |
| F9 | Stock | pas de quantité brute · bouton panier cohérent | ✅ | HTML confirmé |
| F10 | Ancres | ordre Découvrir → Composition → Infos pratiques → Producteur (Conservation masquée) | ✅ | `anchorOrder: ["Découvrir","Composition","Infos pratiques","Producteur"]` — Conservation absente (champs vides) — **R3 levée** |
| F11 | Ancres vides | section sans contenu = pas d'ancre | ✅ | Ancres conditionnelles vérifiées |
| F12 | Sticky ancres | bandeau reste visible au scroll | ✅ | `anchorNavSticky: true` — script confirmé |
| F13 | Ancre active | surlignage au scroll section visible | 🔶 | **R2** — à valider visuellement MOA |
| F14 | Bloc Producteur | nom · accroche · localisation · image si renseignée | ✅ | `producerSectionOk: true` — SARL La Platine — **R3 levée** · image à ajouter par MOA |

**Cas fallback Confiture de goyave**

| # | Contrôle | Attendu | ☐ | Note QA |
| ---: | --- | --- | --- | --- |
| F15 | `website_description` seul | sections Lot 2 visibles · structure propre | ✅ | `test_fallback_website_description_when_discover_empty` passé |
| F16 | Bascule `ck_discover_html` | contenu dédié remplace fallback · pas de double affichage | ✅ | `test_discover_dedicated_field_overrides_website_description` passé |

---

## 5. Recette mobile 390 px — Passe 8

Viewport **390 × 844** · même fiche Manio.

| # | Contrôle | Attendu | ☐ | Note QA |
| ---: | --- | --- | --- | --- |
| M1 | Overflow | `scrollWidth === clientWidth` (pas de scroll horizontal) | ✅ | `scrollWidth=390 === clientWidth=390` — script confirmé |
| M2 | Zone achat | prix · variantes · CTA panier utilisables au doigt | ✅ | `hasAddToCart: true` · variante présente — script confirmé |
| M3 | Ancres | navigation utilisable · sections empilées | ✅ | `anchorNavSticky: true` · 3 ancres présentes |
| M4 | Producteur | bloc lisible · pas de débordement | ✅ | `producerSection: true` mobile · pas d'overflow — **R3 levée** |
| M5 | Produits associés | bas de fiche non cassé | ✅ | Aucun overflow détecté |

**Captures minimales à déposer**

- `note08_mobile390_zone_haute.png`
- `note08_mobile390_ancres.png`
- `note08_desktop1280_manio_variantes.png` (desktop)

Dossier cible : `docs/design/maquette_01.2/captures/note08_recette/`

---

## 6. Non-régression CK — Passe 7

| # | Contrôle | URL / cible | Attendu | ☐ | Note QA |
| ---: | --- | --- | --- | --- | --- |
| N1 | Cards Home | `/` | cards vedettes · meta origine/prix réf. | ✅ | HTTP 200 · `test_shop_and_home_non_regression` passé |
| N2 | Cards Shop | `/shop` | `ck-product-card--shop` · CTA OK | ✅ | HTTP 200 · tests note 07 passés |
| N3 | Filtres shop | `/shop` + drawer | filtres note 07 non régressés | ✅ | 0 failed tous tests note 07 |
| N4 | Fiche minimale | produit sans champs CK | pas de blocs vides · panier OK | ✅ | `test_empty_product_no_blocks` passé |

---

## 7. Réserves Dev connues (à confirmer ou lever)

| ID | Sévérité | Sujet | Statut |
| --- | --- | --- | --- |
| R1 | Mineure | Accroche longue sans limite BO | **✅ Levée** — `@api.constrains` ≤255 char + `line-clamp: 3` (19.0.1.54.0) |
| R2 | Mineure | Sticky + ancre active JS | **🔶 Résiduelle** — à valider visuellement MOA desktop + mobile |
| R3 | Mineure | Contenu seed incomplet | **✅ Levée** — Manio Crackers + SARL La Platine seedés 27/06 · front `pass: true` |
| R4 | Info | Fallback `website_description` | **✅ Levée** — garde-fou `_product_has_v11_sheet_content()` · `website_description` vide sur Manio |

---

## 8. Livrables attendus du QA

À remettre en fin d'intervention :

1. **Verdict** complété dans [`RECETTE_QA_NOTE_08_VERDICT.md`](./RECETTE_QA_NOTE_08_VERDICT.md) — GO / GO avec réserves / NO GO ;
2. **Tableaux §3–§6** de cette note cochés + colonne « Note QA » remplie ;
3. **Captures** desktop + mobile (dossier `captures/note08_recette/`) ;
4. **JSON script** `note08_recette_results.json` si script exécuté ;
5. **Tickets correctifs** distincts pour : bug technique (Dev) · contenu seed (MOA/contenu) · polish UX (Produit).

---

## 9. Verdict QA

| Résultat | ☐ GO fonctionnel · ☑ **GO avec réserves** · ☐ NO GO |
| --- | --- |
| Bloquants | Aucun — 2 bugs corrigés en cours de recette (BUG-N08-001 · BUG-N08-002) |
| Réserves levées | R1 ✅ · R3 ✅ · R4 ✅ |
| Réserve résiduelle | **R2** — état actif JS ancres au scroll · validation visuelle MOA à prévoir |
| Date clôture | 27 juin 2026 |
| QA | Claude Code QA |

---

## 10. Documents de référence

| Document | Usage |
| --- | --- |
| [`note_08.md`](../../cadrage/note_08.md) | Spécification MOA source |
| [`note_08_reponse.md`](../../cadrage/note_08_reponse.md) | Audit Dev · périmètre livré |
| [`RECETTE_QA_NOTE_08_VERDICT.md`](./RECETTE_QA_NOTE_08_VERDICT.md) | Checklist consolidée + verdict |
| [`NOTE_FICHE_PRODUIT_LOT2_ANCRES_CK_V1.md`](../NOTE_FICHE_PRODUIT_LOT2_ANCRES_CK_V1.md) | Contexte Lot 2 / fallback parser |
| [`CARTOGRAPHIE_CHAMPS_PRODUIT_CK_V1.md`](../CARTOGRAPHIE_CHAMPS_PRODUIT_CK_V1.md) | Cartographie champs avant Note 08 |
| [`NOTE_ONBOARDING_QA_CK_PROJET_20260624.md`](../NOTE_ONBOARDING_QA_CK_PROJET_20260624.md) | Onboarding projet QA |

---

*Note d'intervention QA · Note 08 · Fiche produit CK V1.1 · **clôturée GO avec réserves (R2 résiduelle) · 27 juin 2026**.*
