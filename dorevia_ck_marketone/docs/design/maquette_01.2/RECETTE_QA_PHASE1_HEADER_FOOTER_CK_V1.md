# Recette QA — Phase 1 · Header + footer BO · CK V1.2.x

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079 |
| **Conteneur** | `sandbox-odoo19-odoo-1` |
| **GO MOA** | [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) §5 acté 2026-06-13 |
| **Séquence** | [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) Phase 1 |
| **Date livraison Dev** | 2026-06-13 |
| **Date revalidation QA** | 2026-06-13 |
| **Statut** | **✅ OK Phase 1 QA · recommande GO MOA Phase 2 · acte MOA Phase 2 en attente** |

```text
PHASE 1 — OK QA (revalidation Auto · 2026-06-13)
Q1 + Q2 corrigées · non-régression OK · mobile 390 px OK
Recommandation QA : GO MOA Phase 2
Phase 2 : suspendue jusqu'à acte MOA explicite
Instance : 3 entrées nav · mega Épicerie seule
```

> Recette multi-base : header HTTP `X-Odoo-Database: dorevia_ck_marketone_01` requis.

---

## 1. Périmètre livré

| # | Livrable | Statut Dev |
|---|----------|------------|
| 1.1 | Header consolidé BO | ✅ |
| 1.1b | Mega-menu natif CE sur **Découvrir** | ✅ |
| 1.2 | Footer 4 colonnes BO | ✅ |
| 1.1c | Entrée **Producteurs** | ⏸ **Non créée** — pas de page CMS `/producteur/…` |
| 1.1d | **Professionnels** lien direct | ✅ |

**Hors périmètre respecté** : home non modifiée · Phase 2 non démarrée · pas de JS mega custom · pas de reprise HTML maquette.

---

## 2. Header — état instance

| Sequence | Menu | URL | Type |
|----------|------|-----|------|
| 10 | **Boutique** | `/shop` | Lien simple |
| 20 | **Découvrir** | `#` | Mega-menu natif CE (`website.menu` id 10) |
| 30 | **Professionnels** | `/professionnels` | Lien direct |

**Producteurs** : non ajouté — gate MOA (cible CMS réelle absente · Phase 7 M1).

### Mega-menu « Découvrir » — contenu Phase 1

| Colonne | Contenu | Statut |
|---------|---------|--------|
| Acheter par univers | [Épicerie créole](/shop/category/epicerie-creole-1) | ✅ lien BO 200 |
| Explorer par origine | — | ❌ **Masquée** (0 attribut BO) |
| Comprendre et cuisiner | — | ❌ **Exclue** (`/recettes` · `/a-propos` absents) |

**Réserve MOA — Packs & découvertes** :

```text
Catégorie BO id=4 existante · 0 produit publié · URL /shop/category/packs-decouvertes-4 → 404
→ non intégrée au mega (gate pas de lien fictif / cassé)
À activer quand produits publiés dans la catégorie
```

---

## 3. Footer — 4 colonnes BO

Configuration via `website.footer_custom` (vue **CK Footer Phase 1**).

| Colonne | Liens |
|---------|-------|
| **C-Kreyol** | Texte marque · pas de lien juridique |
| **Boutique** | `/shop` · `/shop/category/epicerie-creole-1` |
| **Découvrir** | `/contactus` |
| **CK** | `/professionnels` · `/` |

**Exclus volontairement** : `/a-propos` · `/recettes` · fiche producteur · mentions légales non validées · liens `#` placeholder Odoo default.

---

## 4. Checklist recette MOA/QA

### 4.1 Desktop (1280 px)

| # | Contrôle | Attendu | Dev |
|---|----------|---------|-----|
| D1 | Nav visible | Boutique · Découvrir · Professionnels | ✅ |
| D2 | Pas « Catégories » | Absent | ✅ |
| D3 | Mega Découvrir | Panel `o_mega_menu` · 1 colonne univers | ✅ |
| D4 | Lien mega Épicerie | `/shop/category/epicerie-creole-1` · 200 | ✅ |
| D5 | Pas origines / recettes dans mega | Guadeloupe · `/recettes` absents | ✅ |
| D6 | Professionnels | `/professionnels` · 200 | ✅ |
| D7 | Footer 4 col | Titres C-Kreyol · Boutique · Découvrir · CK | ✅ |
| D8 | Footer liens réels | Pas de `#` · pas de 404 footer | ✅ |
| D9 | Recherche + panier natifs | Présents header | ✅ *(non-régression)* |

### 4.2 Mobile (390 px)

| # | Contrôle | Attendu | Dev |
|---|----------|---------|-----|
| M1 | `scrollWidth = 390` · pas d'overflow | 390/390 | ✅ QA revalidation |
| M2 | Drawer burger OK | — | ✅ |
| M3 | Accordéon Découvrir OK | Épicerie visible | ✅ |
| M4 | Lien Épicerie cliquable | — | ✅ |
| M5 | Pas de téléphone fictif drawer | 0 occurrence | ✅ |
| M6 | Footer 4 col lisible | — | ✅ |

### 4.3 Non-régression

| Route | HTTP | Dev |
|-------|------|-----|
| `/` | 200 | ✅ |
| `/shop` | 200 | ✅ |
| `/shop/cart` | 200 | ✅ |
| `/professionnels` | 200 | ✅ |
| `/contactus` | 200 | ✅ |
| `/shop/category/epicerie-creole-1` | 200 | ✅ |

*(Contrôles Dev via conteneur · 2026-06-13 · restart Odoo post-config)*

---

## 5. Garde-fous vérifiés (Dev)

| Garde-fou | Respecté |
|-----------|----------|
| Mega-menu natif CE uniquement | ✅ `is_mega_menu` + `mega_menu_content` |
| Pas mega-menu custom JS | ✅ |
| Pas de liens fictifs actifs | ✅ |
| Colonne origines masquée | ✅ |
| `/recettes` · `/a-propos` exclus | ✅ |
| Producteurs sans cible CMS | ✅ absent nav |
| Pas modification home | ✅ |
| Phase 2 non démarrée | ✅ |

---

## 6. Verdict QA — historique

### 6.0 · Revalidation finale — Auto (2026-06-13) · **OK Phase 1**

| Champ | Valeur |
|-------|--------|
| **Responsable QA** | Auto (Cursor Agent) |
| **Verdict Phase 1** | ☑ **OK** · ☐ OK partiel · ☐ KO |
| **Recommandation** | **GO MOA Phase 2** |
| **GO Phase 2** | ☑ **Autorisé MOA** · §5bis acté 2026-06-13 |

| Contrôle | Verdict |
|----------|---------|
| **Q1** Téléphone fictif header/offcanvas | ✅ OK — 0 occurrence `555-555-5556` |
| **Q2** Mention Odoo | ✅ OK — pas `Généré par` · pas `o_brand_promotion` · copyright `© C-Kreyol` |
| Non-régression header / mega / footer / routes | ✅ OK |
| Mobile 390 px (Playwright) | ✅ OK — M1–M6 |

**Observation non bloquante (O1)** : `/contactus` conserve un bloc démo Odoo « Ma société » dans le **corps de page** (adresse + téléphone fictif) — hors drawer · hors périmètre Phase 1 header/footer · traitement Phase 6 contact.

**Réserves R1–R4** : confirmées · classées · non bloquantes.

---

### 6.1 · Première passe — Codex (2026-06-13) · OK partiel

| Champ | Valeur |
|-------|--------|
| **Verdict initial** | OK partiel — 2 réserves Q1/Q2 |
| **Suite** | Corrections Dev §6bis · revalidation §6.0 |

---

## 6bis. Corrections Dev post-QA (2026-06-13)

| Action BO | Détail |
|-----------|--------|
| Désactivation `website.header_text_element` | Supprime le téléphone/email demo Odoo dans offcanvas mobile |
| Désactivation `website.brand_promotion` | Désactive le message Odoo traduit |
| Vue `website.custom_hide_brand_promotion_ck_phase1` | Remplace `t-call="web.brand_promotion"` dans `website.layout` |
| Vue `website.footer_copyright_company_name` | Copyright `© C-Kreyol` |

**Non modifié** (conservé natif CE) : `Se connecter` · `Contactez-nous` dans offcanvas — hors périmètre réserves QA.

---

## 7. Prochaine étape

```text
1. ✅ Revalidation QA Phase 1 — OK (2026-06-13)
2. ✅ Verdict MOA final Phase 1 + acte GO Phase 2 — §5bis acté (2026-06-13)
3. ▶ Phase 2 (Home sobre) — exécution Dev autorisée
```

---

## 8. Documents liés

| Document | Rôle |
|----------|------|
| [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) | GO §5 · conditions Phase 1 |
| [`COMPOSITION_HEADER_V1_2.md`](./COMPOSITION_HEADER_V1_2.md) | Header · état post-Phase 1 |
| [`COMPOSITION_FOOTER_PHASE1_V1.md`](./COMPOSITION_FOOTER_PHASE1_V1.md) | Footer 4 col |
| [`note_reference_header_mega_menu_decouverte_ck_v1.md`](./note_reference_header_mega_menu_decouverte_ck_v1.md) | H1 · matrice liens §2bis |

---

*Recette QA Phase 1 — OK QA revalidation 2026-06-13 · recommande GO MOA Phase 2 · acte MOA en attente.*
