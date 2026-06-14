# Recette QA — Phase 5 · Professionnels + CRM · CK V1.2.x

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **GO MOA** | [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) **§5sexies — ACTÉ 2026-06-13** |
| **Prérequis** | Phase 4 clôturée OK partiel MOA · [`RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md`](./RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md) |
| **Capital instance** | [`COMPOSITION_PROFESSIONNELS_V1_2.md`](./COMPOSITION_PROFESSIONNELS_V1_2.md) |
| **Statut** | **✅ Clôturée OK partiel MOA · Phase 6 suspendue** |
| **Module** | `dorevia_ck_theme` **19.0.1.3.0** |

> Header HTTP `X-Odoo-Database: dorevia_ck_marketone_01` requis.

---

## 1. Périmètre Phase 5 (strict) — conforme

| # | Livrable | Statut Dev |
|---|----------|------------|
| 5.1 | Page `/professionnels` | ☑ HTTP 200 · `ck-pro-page` |
| 5.2 | Hero + intro B2B | ☑ wording sobre |
| 5.3 | Double cible | ☑ producteur · fournisseur · distributeur · boutique / CHR |
| 5.4 | Formulaire CRM | ☑ `#ck-pro-form` · `data-model_name="crm.lead"` |
| 5.5 | Qualification lead | ☑ message / `description` · pas champ CRM custom |
| 5.6 | Note qualification | ☑ pas commande B2B · pas tarif automatique |
| 5.7 | Lien `/professionnels` | ☑ menu + signaux Pro intacts |

**Exclus respectés** : pas portail · pas pricing pro public · pas workflow custom · home/shop/fiche/header intacts.

---

## 2. Triptyque QA — résultats Dev

### Gate portable · **OK 2026-06-13**

```text
ck_phase5_ci.sh        : OK
Odoo test-tags         : 11 / 11 OK (dorevia_ck_theme_phase5)
Smoke curl             : /professionnels · fiche · cart · shop · home OK
Soumission CRM         : POST /website/form/crm.lead · crm.lead créé
Playwright UX          : desktop 1280 · mobile 390/390 sans overflow (hors gate)
```

```bash
./scripts/ck_phase5_ci.sh
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 \
  --test-enable --stop-after-init --test-tags=dorevia_ck_theme_phase5 --http-port=8075
node scripts/ck_phase5_desktop1280.mjs
node scripts/ck_phase5_mobile390.mjs
```

---

## 3. Contrôles page `/professionnels`

| Contrôle | Attendu | Résultat |
|----------|---------|----------|
| HTTP 200 | `/professionnels` accessible | ☑ |
| Scope | `ck-pro-page` | ☑ |
| Titre | « Espace professionnel » | ☑ |
| Intro doctrine | Prix grand public · conditions pro après qualification | ☑ |
| Double cible | 2 blocs · 2 CTA · 1 formulaire | ☑ |
| Distinction profils | producteur · fournisseur · distributeur · boutique | ☑ |
| Formulaire CRM | `#ck-pro-form` · champs natifs | ☑ |
| Pas pricing pro | Pas de grille tarifaire B2B publique | ☑ |
| Pas portail | Aucun espace connecté pro | ☑ |

---

## 4. Contrôle soumission CRM

| Contrôle | Attendu | Résultat |
|----------|---------|----------|
| Soumission test | POST `/website/form/crm.lead` OK | ☑ |
| Lead créé | `crm.lead` visible back-office | ☑ |
| Qualification | Description transmise | ☑ |
| Pas champ custom | Aucun champ CRM custom Phase 5 | ☑ |

---

## 5. Smoke curl

| Route | Résultat |
|-------|----------|
| `/professionnels` | ☑ 200 · formulaire · double cible |
| Fiche produit | ☑ 200 · Phase 4 intact |
| `/shop/cart` | ☑ 200 |
| `/shop` | ☑ 200 · Phase 3 intact |
| `/` | ☑ 200 · vedettes SSR |

---

## 6. Playwright UX (hors gate)

| Contrôle | Résultat |
|----------|----------|
| Desktop 1280 | ☑ hero · double cible · formulaire · CTA |
| Mobile 390 | ☑ 390/390 · pas overflow page Pro |
| Formulaire mobile | ☑ champs · submit visibles |
| Non-régression | ☑ home · shop · fiche · cart |

---

## 7. Non-régression Phase 1 · 2 · 3 · 4

| Phase | Résultat |
|-------|----------|
| Phase 1 header/footer | ☑ |
| Phase 2 home SSR 5 cartes | ☑ |
| Phase 3 shop intro | ☑ |
| Phase 4 fiche produit · signal Pro | ☑ |

---

## 8. Verdict QA

| Champ | Valeur |
|-------|--------|
| **Verdict Phase 5** | ☐ OK · ☑ **OK partiel** · ☐ KO |
| **GO Phase 6** | ☑ **Suspendu** |
| **Validé par** | **MOA CK** |
| **Date** | **2026-06-13** |

**Motif OK partiel** : livraison conforme §5sexies · copy M5 à affiner métier avant go-live · bloc dual M9 différé Phase 9.

**Contrôle MOA** : Playwright desktop 1280 · mobile 390 · HTML `/professionnels` · tests Dev (`test_crm_form_submission_creates_lead`) · gate Dev non relancé en parallèle (instabilité env localhost classée non bloquante).

---

## 9. Documents liés

| Document | Rôle |
|----------|------|
| [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) | §5sexies |
| [`RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md`](./RECETTE_QA_PHASE4_FICHE_PRODUIT_CK_V1.md) | Prérequis |
| [`COMPOSITION_PROFESSIONNELS_V1_2.md`](./COMPOSITION_PROFESSIONNELS_V1_2.md) | Capital instance |

---

*Recette QA Phase 5 — clôturée OK partiel MOA · Phase 6 suspendue · 2026-06-13.*
