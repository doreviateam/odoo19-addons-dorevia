# Recette QA — Phase 6 · Contact + À propos · CK V1.2.x

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **GO MOA** | [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) **§5septies — ACTÉ 2026-06-13** |
| **Prérequis** | Phase 5 clôturée OK partiel MOA |
| **Module** | `dorevia_ck_theme` **19.0.1.4.0** |
| **Statut** | **✅ Clôturée OK MOA · 2026-06-13** |

> Header HTTP `X-Odoo-Database: dorevia_ck_marketone_01` requis.

---

## 1. Périmètre Phase 6 (strict)

| # | Livrable | Attendu | Résultat |
|---|----------|---------|----------|
| 6.1 | `/contactus` | HTTP 200 · formulaire natif | ✅ |
| 6.2 | Formulaire contact B2C | `mail.mail` · distinct CRM Pro | ✅ |
| 6.3 | Parcours contact | Renvoi Pro → `/professionnels` | ✅ |
| 6.4 | Nettoyage O1 | Pas de bloc démo « Ma société » | ✅ |
| 6.5 | `/a-propos` | HTTP 200 · `ck-about-page` | ✅ |
| 6.6 | Présentation CK | Mission · sélection · confiance · logistique | ✅ |
| 6.7 | Liens cohérents | `/shop` · `/professionnels` · `/contactus` | ✅ |
| 6.8 | Wording M5 | Client · sobre · promesses tenables | ✅ |

**Exclus vérifiés** :

```text
Pas blog · pas recettes · pas fiche producteur · pas newsletter · pas portail · pas M9
Home · shop · fiche · header/footer : non-régression OK
```

---

## 2. Triptyque QA

| Niveau | Contrôle | Résultat |
|--------|----------|----------|
| **1. Contrat Odoo portable** | `--test-tags=dorevia_ck_theme_phase6` | ✅ **12/12 tests** |
| **2. Smoke curl minimal** | `ck_phase6_ci.sh` | ✅ |
| **3. Playwright UX** | Desktop 1280 · mobile 390 px | ✅ |

```bash
./scripts/ck_phase6_ci.sh
node scripts/ck_phase6_desktop1280.mjs
node scripts/ck_phase6_mobile390.mjs
```

---

## 3. Contrôles `/contactus`

| Contrôle | Attendu | Résultat |
|----------|---------|----------|
| HTTP 200 | `/contactus` accessible | ✅ |
| Formulaire natif | `#contactus_form` · `mail.mail` | ✅ |
| Distinction Pro | Lien `/professionnels` · pas CRM | ✅ |
| O1 résolu | Pas « Ma société » · pas « Fake Buena Vista » | ✅ |
| Wording | « Nous contacter » · client · M5 | ✅ |

---

## 4. Contrôles `/a-propos`

| Contrôle | Attendu | Résultat |
|----------|---------|----------|
| HTTP 200 | `/a-propos` accessible | ✅ |
| Scope | `ck-about-page` | ✅ |
| Mission | Notre mission · sélection · logistique | ✅ |
| Signal Pro | Lien `/professionnels` | ✅ |
| Liens valides | `/shop` · `/professionnels` · `/contactus` | ✅ |
| Pas recettes/producteur | Liens absents | ✅ |

---

## 5. Smoke curl

| Route | Attendu | Résultat |
|-------|---------|----------|
| `/contactus` | 200 · formulaire · pas démo O1 | ✅ |
| `/a-propos` | 200 · contenu CK | ✅ |
| `/professionnels` | 200 · Phase 5 intact | ✅ |
| `/shop` | 200 · Phase 3 intact | ✅ |
| Fiche produit | 200 · Phase 4 intact | ✅ |
| `/` | 200 · vedettes SSR Phase 2 | ✅ |

---

## 6. Playwright UX (hors gate)

| Contrôle | Attendu | Résultat |
|----------|---------|----------|
| Desktop 1280 contact | Formulaire · renvoi Pro · démo retirée | ✅ |
| Desktop 1280 à-propos | Hero · blocs · CTA · liens | ✅ |
| Mobile 390 contact | 390/390 · pas overflow | ✅ |
| Mobile 390 à-propos | 390/390 · pas overflow | ✅ |
| Non-régression | home · shop · fiche · pro · cart | ✅ |

---

## 7. Non-régression Phase 1 · 2 · 3 · 4 · 5

| Phase | Contrôle | Résultat |
|-------|----------|----------|
| Phase 1 | Header · footer · mega | ✅ |
| Phase 2 | Home SSR 5 cartes | ✅ |
| Phase 3 | Shop intro · signal Pro shop | ✅ |
| Phase 4 | Fiche produit · add-to-cart | ✅ |
| Phase 5 | `/professionnels` · `#ck-pro-form` · CRM | ✅ |

---

## 8. Verdict QA · **OK MOA — clôturé · 2026-06-13**

| Champ | Valeur |
|-------|--------|
| **Verdict Phase 6** | ☑ **OK** · ☐ OK partiel · ☐ KO |
| **GO Phase 7** | ☐ **Suspendu** — acte MOA explicite requis |
| **Validé par** | **MOA CK** |
| **Date** | **2026-06-13** |

**Contrôles MOA** : docs · hooks/tests · scripts gate · HTML live · Playwright desktop 1280 · mobile 390.

**Réserves non bloquantes** :

| # | Réserve | Impact |
|---|---------|--------|
| R1 | Copy M5 à relire avant go-live (confiance · logistique) | Métier |
| R2 | `CK_CI_TEST_HTTP_PORT=8075` — éviter deux gates parallèles | Env Dev |
| R3 | `/a-propos` non exposée mega-menu | Conforme gate · option ultérieure |

---

## 9. Documents liés

| Document | Rôle |
|----------|------|
| [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) | §5septies acté |
| [`RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md`](./RECETTE_QA_PHASE5_PRO_CRM_CK_V1.md) | Prérequis |
| [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) | §7 · §10 |

---

*Recette QA Phase 6 — clôturée OK MOA · 2026-06-13.*
