# Retour Dev principal — Cadrage Header C-Kréyòl V2.1

| Champ | Valeur |
| --- | --- |
| **Document source** | [`note_07.md`](./note_07.md) — Header média-commerce · e-commerce d’abord |
| **Rédacteur** | Dev principal |
| **Date** | 2026-06-21 |
| **Contexte technique** | Instance `dorevia_ck_marketone_01` · Odoo 19 CE · `dorevia_ck_theme` / `dorevia_ck_marketone_content` · **post Lot Nav-1** (PR #78 · GO merge QA) |
| **Verdict Dev proposé** | **À AMENDER** → **Arbitrages MOA actés** — ticket H1 rédigé |
| **Suite MOA** | [`note_07_reponse_moa.md`](./note_07_reponse_moa.md) — **validé MOA 2026-06-21** |

---

## 1. Synthèse

La note `note_07` est **claire, structurante et alignée** avec la vision « boutique créole média-commerce, e-commerce d’abord ». Le découpage en trois strates (bandeau service · chrome marchand · navigation), le phasage H1 / H2 / H3, les hors périmètre explicites et la règle « entrée visible = page maîtrisée » sont **sains et implémentables** sur Odoo 19 CE dans notre architecture actuelle (QWeb, SCSS, `website.menu`, pages CMS, snippets).

En revanche, **`note_07` ne se superpose pas tel quel** sur l’état technique du dépôt :

- **Lot Nav-1** vient d’être clôturé (GO merge QA) avec des choix **différents** de `note_07` sur plusieurs points structurants (Professionnels, libellés univers, mega Découvrir, mobile).
- Une partie significative de la **Strate 2** est **déjà livrée** ; la rouvrir dans H1 créerait une régression et un conflit de recette.
- Le **vrai delta H1** porte sur la **Strate 0** (bandeau global), la **Strate 1** (marque renforcée, recherche, chrome e-commerce) et le **chrome mobile** — pas sur la navigation.

**Position Dev** : **GO cadrage** sur la direction V2.1 · **À AMENDER** avant ticket H1 · réconciliation explicite avec Nav-1 via arbitrages MOA.

---

## 2. Points forts (à conserver tels quels)

### Doctrine et positionnement

- Priorité e-commerce : recherche, panier, univers produits, accès boutique — cohérent avec Nav-1 et Phase 10.
- Header « média-commerce » sans basculer en média pur : réaliste sur Odoo CE.
- Références 750g / Sept-Fons comme **inspiration structurelle**, pas comme copie — bonne garde-fou.

### Architecture en strates

La séparation **rassurer → vendre → orienter** (§8) est exploitable techniquement :

| Strate | Rôle | Piste technique Odoo |
| --- | --- | --- |
| 0 — Bandeau service | Réassurance transversale | Héritage QWeb `website.layout` au-dessus de `#top` |
| 1 — Logo / recherche / compte / panier | Conversion | Templates header CE + SCSS `website_header.scss` |
| 2 — Navigation | Orientation catalogue + Découvrir | **`nav_sync.py` · Nav-1 livré** |

### Périmètre et phasage

- §16 hors périmètre V1 : blog, forum, méga complexe, refonte shop/home/FP, B2B avancé — **conforme** à notre mode de livraison.
- H2 pages provisoires : pattern déjà en place sur l’instance.
- H1 bis recherche vide : bon backlog, pas bloquant.

### Méthode technique (§15)

Alignée socle actuel : pas de front parallèle, héritages QWeb maîtrisés, SCSS tokens CK — **rien à contredire**.

---

## 3. Alignements avec Nav-1 (acquis — ne pas rouvrir dans H1)

| Élément | `note_07` | État post-Nav-1 | Statut |
| --- | --- | --- | --- |
| `Tous nos produits` | §11.3 | Livré · `/shop` | ✅ Acquis |
| Univers commerce desktop | Épicerie créole · Soin & bien-être | Épicerie · Soin & Bien-être (visibilité BO) | ⚠️ Libellés à trancher |
| Mobile `Nos univers` | §13.2 | Livré + B1/B2 | ✅ Acquis |
| `Découvrir` + sous-liens | Dropdown simple §11.7 | Mega natif CE · Pro + Contact | ⚠️ Forme à trancher |
| CTA Contact header | Contact via dropdown + footer | Retiré · sous Découvrir | ✅ Acquis |
| Visibilité liens | §12 règle pages | `nav_sync.py` §7 bis | ✅ Acquis |
| Artisanat hors nav V1 | §11.6 | Masqué si immature | ✅ Acquis |
| Boissons | Absent nav V1 `note_07` | Masqué (cat. absente seed) | ✅ Acquis |

**Règle Dev** : H1 **ne reticketise pas** `nav_sync.py`, les menus `website.menu`, le mega Découvrir ni le regroupement mobile **sans lot Nav-1 bis** et acte MOA explicite.

---

## 4. Écarts critiques — à arbitrer MOA

### 4.1 Strate 2 — Navigation principale

| Sujet | `note_07` §11 | Nav-1 livré ([`note_06`](./note_06.md) + PR #78) | Risque |
| --- | --- | --- | --- |
| **Professionnels** | **Top-level** (dernière entrée §11.8) | **Sous Découvrir** (mega) | **Pivot majeur** — MOA Nav-1 tranché l’inverse |
| Libellé épicerie | **Épicerie créole** | **Épicerie** | Incohérence header ↔ home S4 |
| Libellé soin | **Soin & bien-être** | **Soin & Bien-être** (MOA Nav-1) | Wording / SEO |
| **Découvrir** | Dropdown **simple** V1 | **Mega-menu** natif | Effort + UX différents |
| Contact | `/contact` · « Contact » | `/contactus` · « Contactez-nous » | Liens Nav-1 + tests HTTP |
| Producteurs | `/producteurs` (hub) | `/producteur/atelier-hauts-goyaviers` | H2 contenu, pas header |
| Recettes | `/recettes-usages` | `/recettes` | Alias ou migration |

### 4.2 Marque « C-Kréyòl » (§2–3)

| Point | État actuel | Commentaire |
| --- | --- | --- |
| Graphie publique | **C-Kreyol** (`website_header.xml`, tests phase10) | Rebrand faisable QWeb + SCSS |
| Nom technique | CK Marketone (modules) | Inchangé — conforme §2.2 |
| Polices | Fraunces + DM Sans self-hosted | Vérifier rendu **ò** en recette 1280/390 |

### 4.3 Strate 0 — Bandeau service (§9)

| Point | `note_07` | Instance actuelle |
| --- | --- | --- |
| Emplacement | **Header global** (toutes pages) | Trust-bar **home S2** (`home_reassurance.py`) |
| Wording | Produits créoles sélectionnés · Origines identifiées · Livraison suivie | Sélection créole · Livraison France & Europe · … |

**Faisabilité** : ✅ modérée (QWeb + SCSS).  
**Décision MOA** : bandeau header global **vs** conserver trust-bar home **vs** les deux (risque redondance).

### 4.4 Strate 1 — Recherche centrale (§10.2)

| Point | `note_07` | Instance actuelle |
| --- | --- | --- |
| Présence | Barre **centrale large** | Icône / comportement header Odoo CE |
| Placeholder | Rechercher un produit, une saveur... | Natif Odoo |

**Faisabilité** : ✅ mais effort **moyen à élevé** — réorganisation templates header Odoo 19, pas simple SCSS.

### 4.5 Mobile chrome (§13)

| Point | `note_07` | Nav-1 |
| --- | --- | --- |
| Ligne chrome | Menu · C-Kréyòl · Recherche · Panier | Burger · logo · icônes CE |
| Compte | Dans le drawer | Icône header (CE) |
| Contact | **Direct** dans le menu mobile | Sous **Découvrir** |

Restructuration chrome mobile faisable ; **contenu drawer** = acquis Nav-1.

### 4.6 Doctrine catalogue §4–5

Règle pertinente mais **hors périmètre header pur** :

- Gouvernance BO / fiche produit (Lot 2 FP en partie).
- Bandeau « Origines identifiées » = promesse marketing ; **preuve** = métadonnées produit visibles.

À référencer H2 / chantier produit, pas bloquant H1.

---

## 5. Faisabilité technique par lot (Odoo 19 CE)

### Lot H1 — Structure header média-commerce (delta recommandé)

| Composant | Faisabilité | Effort | Inclus H1 recommandé |
| --- | --- | --- | --- |
| Bandeau Strate 0 global | ✅ | M | Si MOA acte (option) |
| Logo renforcé + C-Kréyòl | ✅ | S–M | ✅ |
| Recherche centrale + placeholder | ✅ | M–L | Si MOA acte (cœur effort) |
| Panier / compte (poids visuel) | ✅ | S | ✅ |
| Navigation Strate 2 | ✅ déjà fait | — | ❌ **Hors H1** |
| Chrome mobile ligne 1 | ✅ | M | ✅ (sans rouvrir drawer) |
| Tests + recette 1280/390 | ✅ | S | ✅ |

**Périmètre H1 proposé** :

```text
Strate 0 (option MOA) + Strate 1 (marque, recherche, chrome e-commerce) + mobile chrome
Navigation Strate 2 = Nav-1 figé
```

### Lot H2 — Pages provisoires

| Page `note_07` | Instance | Delta |
| --- | --- | --- |
| `/a-propos` | ✅ | Enrichissement optionnel |
| `/professionnels` | ✅ | OK |
| `/recettes-usages` | `/recettes` | Alias ou wording |
| `/contact` | `/contactus` | **Ne pas casser** Nav-1 |
| `/producteurs` | Fiche pilote seule | **Hub à créer** — contenu MOA |

### Lot H3 — Enrichissement Découvrir

Chevauche **Lot Nav-2** déjà identifié. Après H1 + stabilisation Nav-1. Attention conflit dropdown simple (`note_07`) vs mega (Nav-1).

---

## 6. Risques techniques

1. **Double travail navigation** — rouvrir Strate 2 dans H1 annule Nav-1 et invalide recette QA §8 bis.
2. **Bandeau + trust-bar home** — deux messages de réassurance si les deux coexistent sans arbitrage.
3. **Recherche centrale** — régression mobile / accessibilité si layout header mal borné.
4. **Sticky header** — règles dupliquées QWeb + SCSS ; toute refonte Strate 0/1 doit les préserver.
5. **Représentation double BO** (univers desktop + `Nos univers` mobile) — volontaire Nav-1 ; ne pas « simplifier » en BO sans repenser CSS.
6. **Tests header** — assertions `C-Kreyol`, structure `#top_menu`, tags `phase10` / `nav_sync` à mettre à jour si rebrand ou layout.

---

## 7. Amendements suggérés à `note_07`

Avant ticket H1, enrichir le cadrage avec :

1. **§8 bis — État post-Nav-1 (baseline figée)**  
   Tableau Strate 2 livrée · versions modules · lien PR #78 · règle « H1 ne rouvre pas la navigation ».

2. **§11 bis — Réconciliation navigation**  
   Trancher explicitement Professionnels, libellés, mega vs dropdown, URLs.

3. **§9 bis — Bandeau header vs trust-bar home**  
   Un seul message de réassurance transversal ou coexistence assumée.

4. **§18.1 bis — Périmètre H1 delta**  
   Liste inclusive / exclusive par strate (cf. §5 ci-dessus).

5. **§19 bis — Décisions MOA post-Nav-1**  
   Reprendre tableau arbitrages [`note_07_reponse_moa.md`](./note_07_reponse_moa.md).

6. **§12.2 — URLs instance**  
   Aligner tableau sur URLs réelles (`/contactus`, `/recettes`, `/producteur/...`) ou plan de migration.

---

## 8. Proposition de séquencement Dev (après arbitrages MOA)

```text
Lot Nav-1                    → ✅ Clôturé GO merge (PR #78)

Lot H1 (Header V2.1 delta)
  → Arbitrages note_07_reponse_moa
  → Strate 0 optionnelle + Strate 1 + chrome mobile
  → Rebrand C-Kréyòl si acté
  → Recette QA H1 1280 + 390 · non-régression Nav-1

Lot H2 (Pages header)
  → Hub /producteurs · harmonisation URLs si MOA
  → Pages provisoires enrichies

Lot Nav-2 / H3
  → Enrichissement éditorial Découvrir (après H1)
```

---

## 9. Verdict Dev principal

| Critère | Appréciation |
| --- | --- |
| Clarté direction média-commerce | ✅ Validé |
| Strates 0 / 1 / 2 | ✅ Validé en principe |
| Périmètre §16 hors V1 | ✅ Validé |
| Méthode Odoo 19 CE | ✅ Validé |
| Alignement Nav-1 Strate 2 | ❌ Écarts majeurs — amendement requis |
| Prêt ticket H1 | ⚠️ Après arbitrages §4 et amendements §7 |

**Position Dev** : `note_07` peut servir de **base MOA structurante** pour le header V2.1. Je recommande **À AMENDER** puis **GO MOA** sur une version réconciliée avec Nav-1. Le ticket **H1** est **enchaînable** sans refonte lourde si borné au **delta Strate 0 + Strate 1 + mobile chrome**.

---

## 10. Documents de référence consultés

| Document | Rôle |
| --- | --- |
| [`note_07.md`](./note_07.md) | Cadrage MOA source |
| [`note_06.md`](./note_06.md) · Nav-1 | Navigation livrée |
| [`TICKET_DEV_LOT_NAV1_NAVIGATION_CK_V2.md`](../design/TICKET_DEV_LOT_NAV1_NAVIGATION_CK_V2.md) | Ticket Nav-1 clôturé |
| [`NOTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md`](../design/maquette_01.2/NOTE_QA_LOT_NAV1_NAVIGATION_CK_V2.md) | Recette QA GO merge |
| [`website_header.xml`](../../dorevia_ck_theme/views/website_header.xml) | Logo · sticky |
| [`nav_sync.py`](../../dorevia_ck_marketone_content/nav_sync.py) | Sync menus Nav-1 |
| [`home_reassurance.py`](../../dorevia_ck_marketone_content/home_reassurance.py) | Trust-bar home S2 |

---

*Retour Dev principal · Header C-Kréyòl V2.1 · 2026-06-21 · post Nav-1.*
