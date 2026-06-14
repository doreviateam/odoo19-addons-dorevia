# Recette MOA écran — A1 · Header / menu / branding CK · Phase 10 §2

| Champ | Valeur |
|-------|--------|
| **Chantier** | **A — Reprise maquette CK V1.2.x / go-live CMS** |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Modules** | `dorevia_ck_theme` **19.0.1.12.0** · `dorevia_ck_marketone_content` **19.0.1.0.0** |
| **Gouvernance** | [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) §5undecies |
| **Livraison validée** | Reprise visuelle header v2 · [`RAPPORT_A1_REPRISE_DEV_HEADER_20260614.md`](./RAPPORT_A1_REPRISE_DEV_HEADER_20260614.md) |
| **Verdict go-live global** | **Non signé** — **A1 header clôturé OK** |
| **Statut session A1** | **✅ CLÔTURÉE · Verdict MOA final : A1-OK** |
| **Date verdict final** | **2026-06-14** |
| **Exécuteur MOA** | **MOA CK** |
| **Preuves** | captures [`a1_visuelle_20260614_v2/`](./rapport/a1_visuelle_20260614_v2/) · QA 27/27 |

```text
CHAMPIER A — session A1 header CLÔTURÉE (A1-OK).
Périmètre ticket header strict : pas d'élargissement rétroactif (hero · contenus accueil = hors A1).
Suite autorisée : Phase 10 §3–§9 · arbitrage A7 · recette navigateur Chantier B (séquence MOA).
Ne pas mélanger avec dorevia_ckreyol_marketone (Chantier B).
```

---

## Historique verdicts A1

| Date | Verdict | Note |
|------|---------|------|
| 2026-06-14 | **A1-GO Dev ciblé** | Relecture v1 · écart visuel header vs maquette |
| 2026-06-14 | Livraison **19.0.1.12.0** | Reprise visuelle ciblée header · gate + 27/27 QA |
| 2026-06-14 | **A1-OK** | Relecture visuelle MOA captures v2 / URLs contrôle |

---

## Préparation session (5 min)

| Étape | Action |
|-------|--------|
| 1 | Forcer la base : header HTTP `X-Odoo-Database: dorevia_ck_marketone_01` **ou** `?db=dorevia_ck_marketone_01` |
| 2 | Cache-bust : `&qa_ts=phase10a1v2` sur chaque URL |
| 3 | Viewport **1280×800** puis **390×844** (DevTools responsive) |
| 4 | Hard refresh · désactiver cache réseau si doute |
| 5 | Ouvrir les 3 URLs ci-dessous dans l'ordre |

---

## URLs de recontrôle (livraison validée v2)

```text
http://localhost:18079/?db=dorevia_ck_marketone_01&qa_ts=phase10a1v2
http://localhost:18079/contactus?db=dorevia_ck_marketone_01&qa_ts=phase10a1v2
http://localhost:18079/shop?db=dorevia_ck_marketone_01&qa_ts=phase10a1v2
```

---

## Grille MOA — desktop 1280 px

| # | Contrôle | Attendu | ☐ OK | ☐ KO | ☐ Réserve | Notes |
|---|----------|---------|------|------|-----------|-------|
| D1 | Logo C-Kreyol | Logo réel · pas placeholder Odoo | ☑ | | | Identité C-Kreyol typographique · v2 validée MOA |
| D2 | Taille / alignement logo | Lisible · respiration header | ☑ | | | Densité header acceptable MOA |
| D3 | Nav principale | Boutique · Découvrir · Professionnels · Contactez-nous | ☑ | | | Nav desktop lisible · Contactez-nous zone utilitaires |
| D4 | Pas Producteurs (nav) | Absent du menu header | ☑ | | | |
| D5 | Mega Découvrir | Clic ouvre panel · fermeture OK | ☑ | | | |
| D6 | Lien Épicerie créole | Mega · lien 200 · pas 404 | ☑ | | | |
| D7 | Recherche / panier | Icônes natives visibles · cliquables | ☑ | | | Zone utilitaires droite conforme Odoo |
| D8 | Sticky header | Scroll stable · pas saut layout | ☑ | | | |
| D9 | Contraste nav | Texte lisible · hover perceptible | ☑ | | | |
| D10 | Cohérence CK header | Header aligné niveau visuel CK | ☑ | | | Validé MOA v2 · hors hero/contenus page |
| D11 | Overflow 1280 | Pas scroll horizontal page | ☑ | | | |
| D12 | Header identique 3 URLs | Même chrome `/` · contact · shop | ☑ | | | Pas de régression visuelle header MOA |

---

## Grille MOA — mobile 390 px

| # | Contrôle | Attendu | ☐ OK | ☐ KO | ☐ Réserve | Notes |
|---|----------|---------|------|------|-----------|-------|
| M1 | Burger / offcanvas | Ouverture · fermeture | ☑ | | | |
| M2 | Nav mobile complète | Mêmes entrées que desktop | ☑ | | | |
| M3 | Mega mobile Découvrir | Accessible · contenu lisible | ☑ | | | |
| M4 | Épicerie créole mobile | Lien atteignable depuis mega | ☑ | | | |
| M5 | Recherche / panier mobile | Accessibles | ☑ | | | |
| M6 | Touch targets | Liens / burger suffisamment grands | ☑ | | | |
| M7 | Overflow 390 | Pas scroll horizontal | ☑ | | | |
| M8 | Branding offcanvas | Cohérence CK vs pages | ☑ | | | Cohérence mobile/offcanvas validée MOA v2 |
| M9 | Contactez-nous mobile | Présent · lisible | ☑ | | | Offcanvas · comportement Odoo conservé |

---

## Arbitrages MOA

| Sujet | Décision session |
|-------|------------------|
| Contactez-nous en nav | ☑ **Conserver** · zone utilitaires desktop + offcanvas mobile |
| Producteurs en nav | ☑ **Conforme absent** |
| Mega recettes / à-propos | ☑ **Différer** |
| Effet « natif Odoo » résiduel (header) | ☑ **Levé v2** — header CK validé A1-OK |
| Hero / contenus accueil vs maquette | ☑ **Hors périmètre A1** · écarts visibles non bloquants header |

---

## Verdict A1 — signé MOA (final)

```text
☑ A1-OK
   Header / menu / branding acceptés pour go-live V1.
   Livraison 19.0.1.12.0 validée après relecture visuelle MOA.

☐ A1-GO Dev ciblé
   (itération clôturée — reprise v2 livrée et validée)

☐ A1-KO
```

### Points validés MOA (2026-06-14 · relecture v2)

- Identité **C-Kreyol** correctement portée dans le header
- Remplacement du logo générique « Your Logo »
- Navigation desktop lisible et cohérente
- Zone utilitaires à droite conforme à l’usage Odoo
- **Contactez-nous** conservé et correctement intégré
- Densité du header acceptable
- Acquis techniques conservés : sticky · responsive · mega menus · absence d’overflow
- Périmètre respecté : reprise header uniquement · sans réouverture fonctionnelle

### Dettes hors périmètre A1 (non bloquantes)

| Sujet | Traitement MOA |
|-------|----------------|
| Hero · contenus d’accueil vs maquette | **Hors scope A1 header** · traiter en Phase 10 §3–§9 ou phases dédiées |
| Go-live global | **Non signé** sur ce seul acte A1 |

### Traçabilité livraison v2

| Élément | Référence |
|---------|-----------|
| Module | `dorevia_ck_theme` **19.0.1.12.0** |
| Rapport Dev | [`RAPPORT_A1_REPRISE_DEV_HEADER_20260614.md`](./RAPPORT_A1_REPRISE_DEV_HEADER_20260614.md) |
| Captures | [`rapport/a1_visuelle_20260614_v2/`](./rapport/a1_visuelle_20260614_v2/) |
| QA gate | `ck_phase10_ci.sh` OK · tests 3/3 · Playwright 27/27 |

---

## Acte MOA — signature A1 (final)

```text
RECETTE MOA ÉCRAN — A1 Header Phase 10 §2
Chantier A — dorevia_ck_marketone_01
Verdict : A1-OK
Date : 2026-06-14
Validé par : MOA CK
Livraison : dorevia_ck_theme 19.0.1.12.0 (reprise visuelle header v2)

Suite autorisée :
  → Phase 10 §3–§9 transversale
  → Arbitrage A7 Git modules CK (acte MOA explicite requis)
  → Recette navigateur Chantier B (6.3a · 6.3b · SEO) selon séquence MOA

Hors périmètre acte A1 :
  → Pas d'élargissement rétroactif du ticket header
  → Hero / contenus accueil : phases ultérieures
```

---

## Documents liés (Chantier A)

| Document | Rôle |
|----------|------|
| [`RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md`](./RECETTE_QA_PHASE10_GO_LIVE_CK_V1.md) | Dossier Phase 10 complet · suite §3–§9 |
| [`note_reference_header_mega_menu_decouverte_ck_v1.md`](./note_reference_header_mega_menu_decouverte_ck_v1.md) | Cible H1 |
| [`RAPPORT_A1_RECETTE_VISUELLE_20260614.md`](./RAPPORT_A1_RECETTE_VISUELLE_20260614.md) | Recette v1 · référence historique |
| [`RAPPORT_A1_REPRISE_DEV_HEADER_20260614.md`](./RAPPORT_A1_REPRISE_DEV_HEADER_20260614.md) | Livraison Dev v2 · traçabilité |
| [`rapport/a1_visuelle_20260614_v2/`](./rapport/a1_visuelle_20260614_v2/) | Captures MOA · 27/27 QA |
| [`scripts/ck_phase10_ci.sh`](./scripts/ck_phase10_ci.sh) | Gate technique header |

**Hors périmètre session A1** : Chantier B · clôture go-live global.

---

*Session MOA écran A1 — **Verdict final A1-OK** · 2026-06-14 · Chantier A · header 19.0.1.12.0.*
