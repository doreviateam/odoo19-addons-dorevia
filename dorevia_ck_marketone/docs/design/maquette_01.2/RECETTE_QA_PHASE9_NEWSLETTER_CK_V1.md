# Recette QA — Phase 9 · Newsletter M9 simple · CK V1.2.x

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **GO MOA** | [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) **§5decies — ACTÉ 2026-06-14** |
| **Phase 8** | **Clôturée OK partiel MOA · 2026-06-14** |
| **Modules** | `dorevia_ck_theme` **19.0.1.10.0** · `dorevia_ck_marketone_content` **19.0.1.0.0** |
| **Statut** | **✅ CLÔTURÉE OK partiel MOA · 2026-06-14 · Phase 10 suspendue** |
| **E-mail test** | `qa-phase9-newsletter@test.ck.local` · purge après recette |

> **Clôture MOA Phase 9 actée · 2026-06-14** · dual compact newsletter sur `/contactus` et `/professionnels` · home Phase 2 non modifiée.

---

## 0. Rappel gouvernance

| Règle | Statut |
|-------|--------|
| Phases 1–8 clôturées | ✅ |
| Phase 9 exécution Dev | ✅ **Livrée · clôturée MOA · 2026-06-14** |
| Réserve header/menu CK | Dette transversale go-live / Phase 1 · **non bloquante Phase 9** |
| Phase 10 | ☐ **Suspendue** — acte MOA distinct requis |
| Architecture split §4bis | ✅ **Validée · non rouverte** |
| Home dual newsletter | **Phase 2 livré** — recontrôle non-régression · **OK** |

**Contrôle MOA cache-bust** :

```
http://localhost:18079/contactus?db=dorevia_ck_marketone_01&qa_ts=1
http://localhost:18079/professionnels?db=dorevia_ck_marketone_01&qa_ts=1
```

---

## 1. Périmètre Phase 9 (strict · livré)

| # | Livrable | Attendu | Résultat |
|---|----------|---------|----------|
| 9.1 | Modules CE | `mass_mailing` · `website_mass_mailing` actifs | ✅ |
| 9.2 | Mailing list BO | `Newsletter CK` · `data-list-id` réel | ✅ |
| 9.3 | Contact — dual compact | `/contactus` · `#ck-newsletter-subscribe` | ✅ |
| 9.4 | Pro — dual compact | `/professionnels` · CTA `#ck-pro-form` | ✅ |
| 9.5 | Inscription simple | Subscribe JSON-RPC fonctionnel | ✅ |
| 9.6 | Consentement RGPD | Mention claire · désinscription | ✅ |
| 9.7 | Garde-fou M9 | Pas popup · pas automation | ✅ |
| 9.8 | Intégration website | `website.layout` · assets | ✅ |
| 9.9 | Non-régression | Phases 1–8 · home dual intact | ✅ |
| 9.10 | Header/footer | **Inchangés** | ✅ |
| 9.11 | Séparation parcours | B2C contact · CRM Pro · newsletter distincts | ✅ |

---

## 2. Triptyque QA

| Niveau | Contrôle | Résultat |
|--------|----------|----------|
| **1. Contrat Odoo** | `--test-tags=dorevia_ck_theme_phase9` | ✅ **17/17** |
| **2. Smoke curl** | `ck_phase9_ci.sh` | ✅ **2026-06-14** |
| **3. Playwright UX** | Desktop 1280 · mobile 390 px | ✅ |

**Playwright desktop** : dual compact contact/pro · subscribe input · RGPD · pas overflow 1280/1280.

**Playwright mobile** : `/contactus` et `/professionnels` · 390/390 · newsletter visible · pas overflow.

---

## 3. Non-régression Phases 1–8

| Phase | Contrôle | Résultat |
|-------|----------|----------|
| Phase 1 header/footer | inchangés | ✅ |
| Phase 2 home | dual Pro/newsletter · vedettes SSR | ✅ |
| Phase 3 shop | `s_ck_shop_intro` | ✅ |
| Phase 4 fiche produit | `ck-product-page` | ✅ |
| Phase 5 pro | formulaire CRM · contenu existant | ✅ |
| Phase 6 contact | `contactus_form` · layout | ✅ |
| Phase 7 producteur | `ck-producer-page` | ✅ |
| Phase 8 recettes | `ck-recipes-page` | ✅ |

---

## 4. Vigilances MOA (recette)

| # | Point | Résultat Dev |
|---|-------|--------------|
| 1 | Subscribe test · adresse explicite · purge | ✅ `qa-phase9-newsletter@test.ck.local` |
| 2 | reCAPTCHA · non bloquant si natif OK | ✅ subscribe natif fonctionnel |
| 3 | RGPD · désinscription mentionnée | ✅ copy livrée |
| 4 | Séparation B2C / Pro / newsletter | ✅ blocs distincts |

---

## 5. Recontrôle écran MOA · **2026-06-14**

| Page | Contrôles clés | Résultat |
|------|----------------|----------|
| `/contactus` | dual compact · newsletter · RGPD · `contactus_form` · pas `crm.lead` | ✅ |
| `/professionnels` | dual compact · `#ck-pro-form` · `crm.lead` · newsletter distincte | ✅ |
| `/` | dual home Phase 2 · vedettes SSR | ✅ |

---

## 6. Architecture module (§4bis · QA OK acté · 2026-06-14)

| Point | Statut |
|-------|--------|
| Instance `dorevia_ck_marketone_01` | ✅ `dorevia_ck_theme` + `dorevia_ck_marketone_content` |
| QA isolation « thème seul » | ✅ **OK acté** · `19.0.1.10.0` |
| Split thème / contenu | ✅ **Validé MOA · chantier non rouvert** |
| Marque blanche snippets | ⚠️ hors périmètre V1 — thème CK |

---

## 7. Verdict MOA · **CLÔTURÉE OK partiel · 2026-06-14**

| Champ | Valeur |
|-------|--------|
| **Verdict QA documentaire** | ☑ **OK · 2026-06-14** |
| **Verdict Phase 9 exécution** | ☑ **OK partiel MOA · 2026-06-14** |
| **Motif OK partiel** | Triptyque complet · réserve header/menu CK transversale go-live |
| **GO Phase 10** | ☐ **Préparation recette go-live** — pas Dev sans acte MOA §5undecies · focus header/menu |
| **Validé par (clôture)** | MOA CK |
| **Date triptyque + recontrôle** | **2026-06-14** |

```text
Phase 9 — OK partiel MOA.
Newsletter M9 · dual compact contact/pro · subscribe natif · RGPD · séparation B2C/Pro/Newsletter.
Réserve header/menu CK = dette transversale go-live (non bloquante).
```

---

*Recette QA Phase 9 — clôturée OK partiel MOA · 2026-06-14.*
