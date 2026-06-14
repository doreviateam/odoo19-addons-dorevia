# Note référence — Header V1 + mega-menu Découvrir · CK

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Décision MOA** | **H1 — Header & mega-menu acté** |
| **Date acte** | 2026-06-13 |
| **Instance** | `dorevia_ck_marketone_01` |
| **Statut** | **Acté MOA · compatible Phase 1 · soumis GO exécution §5** |
| **Dictionnaire** | [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) §1 |
| **Recette CE** | [`RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md`](./RECETTE_QA_DICTIONNAIRE_MAQUETTE_ODOO_CE_V1.md) §0ter |
| **Gouvernance** | [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) §1bis |

```text
HEADER V1 ACTÉ
Boutique · Découvrir · Producteurs · Professionnels
Mega-menu natif CE sur « Découvrir » uniquement
```

---

## 1. Décision MOA — header V1 cible

```text
Boutique · Découvrir · Producteurs · Professionnels
```

| Entrée | Type V1 acté | Implémentation Odoo |
|--------|--------------|---------------------|
| **Boutique** | Lien simple | `/shop` |
| **Découvrir** | **Mega-menu natif CE** | `website.menu.is_mega_menu` + `mega_menu_content` |
| **Producteurs** | Lien simple **ou** dropdown léger | Pas mega-menu Producteurs V1 |
| **Professionnels** | **Lien direct** | `/professionnels` |

> Remplace l’actuel libellé **Catégories** (trop technique) par **Découvrir**.

### Arbitrage libellé

| Option | Verdict |
|--------|---------|
| **Découvrir** | ✅ **Retenu MOA** |
| Univers | ❌ Non retenu — plus abstrait |

**Motif MOA** : plus clair client · logique découverte produit · meilleur remplacement de « Catégories ».

---

## 2. Mega-menu « Découvrir » — contenu acté

Mega-menu **natif Odoo CE** · configuration BO · pas de JS custom.

### Colonne 1 — Acheter par univers

| Lien | Source Odoo | Condition |
|------|-------------|-----------|
| Épicerie créole | `/shop/category/…` | Si catégorie BO existe |
| Manioc & dérivés | Catégorie ou tag BO | Si BO prête |
| Incontournables CK | Catégorie / sélection BO | Si BO prête |
| Packs & découvertes | Catégorie « Packs & découvertes » | Si BO prête |
| Nouveautés | Tag / catégorie BO | Si BO prête |

**Gate M4** : pas de liens fictifs · catégories BO réelles uniquement.

### Colonne 2 — Explorer par origine

| Lien | Source Odoo | Condition |
|------|-------------|-----------|
| Guadeloupe | Attribut / tag origine | **Si données BO prêtes** |
| Martinique | Attribut / tag origine | **Si données BO prêtes** |
| Réunion | Attribut / tag origine | **Si données BO prêtes** |

**Gate** : différer colonne entière si attributs origine non structurés (instance actuelle : 0 attribut).

### Colonne 3 — Comprendre et cuisiner

| Lien | Cible | Phase contenu |
|------|-------|---------------|
| Recettes & savoirs | `/recettes` | Phase 8 |
| Conseils d’usage | Page CMS / `/a-propos` | Phase 6 |
| Découvrir les produits créoles | `/a-propos` ou `/shop` | Phase 6 |

Structure mega-menu Phase 1 · liens actifs uniquement si pages/catégories existent.

### 2bis. Matrice liens — instance Phase 1 livrée (QA Codex · 2026-06-13)

**Dans le mega Découvrir** :

| Lien | Cible | Statut |
|------|-------|--------|
| Épicerie créole | `/shop/category/epicerie-creole-1` | ✅ intégré · 200 |

**Non intégré (gates BO)** :

| Élément | Motif |
|---------|-------|
| Packs & découvertes | 0 produit publié · URL 404 |
| Colonne origines | 0 attribut BO |
| `/recettes` · `/a-propos` | Pages absentes |
| Producteurs (nav header) | Pas de CMS · **3 entrées** nav livrées |

---

## 3. Producteurs — décision V1

```text
Pas de mega-menu Producteurs lourd en V1
```

| Autorisé V1 | Exclu V1 |
|-------------|----------|
| Lien simple | Mega-menu Producteurs |
| Dropdown léger (2–3 liens) | Annuaire |
| Renvoi fiche producteur pilote | Navigation complexe |
| Page CMS simple | |

**Cibles possibles** :

* Fiche producteur pilote (Phase 7) · `/producteur/atelier-hauts-goyaviers`
* Page CMS simple « Producteurs CK » *(optionnel)*
* Proposer un producteur → `/professionnels` ou `/contactus`

---

## 4. Professionnels — décision V1

```text
Lien direct /professionnels — pas de sous-menu · pas de friction
```

Objectif MOA : accès rapide · qualification B2B prioritaire.

---

## 5. Vérification technique CE (rappel)

| Point | Verdict |
|-------|---------|
| Mega-menu natif | ✅ `is_mega_menu` · `mega_menu_content` |
| Enterprise | ❌ Non requis |
| Configuration | BO / Website Builder Edit Menu |
| Mobile | Accordéon offcanvas natif · recette 390 px |
| `dorevia_ck_theme` | CSS léger `.o_mega_menu` **si nécessaire** |
| Mega-menu custom JS | ❌ Hors scope V1 |

Test QA instance (2026-06-13) : rendu `o_mega_menu` confirmé.

---

## 6. Garde-fous actés

```text
Mega-menu natif CE uniquement · configuration BO first
Adaptation CSS CK légère seulement si nécessaire
Pas de mega-menu custom JS · pas de navigation mobile complexe
Recette mobile 390 px obligatoire
Pas de liens fictifs vers pages ou catégories non prêtes
Compatible Phase 1 · soumis au GO exécution §5
```

---

## 7. Classification dictionnaire (Phase 1)

| Bloc | Action V1 |
|------|-----------|
| Header 4 entrées | Intégrer BO |
| Mega-menu Découvrir | Intégrer · OK CE natif |
| Producteurs | Lien / dropdown léger |
| Professionnels | Lien direct |
| Style mega CK | Conditionnel CSS thème |

---

## 8. Documents liés

| Document | Rôle |
|----------|------|
| [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](./GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) | Dictionnaire §1 |
| [`COMPOSITION_HEADER_V1_2.md`](./COMPOSITION_HEADER_V1_2.md) | État instance (Catégories · à migrer) |
| [`SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md`](./SEQUENCE_REPRISE_ODOO_V1_CK_V1_2_X.md) | Phase 1 |
| [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) | §1bis H1 |

---

*Note référence header V1 + mega-menu Découvrir — décision MOA H1 actée · 2026-06-13.*
