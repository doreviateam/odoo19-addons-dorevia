# Lot mentions légales — go-live public CK · 2026-06-14

| Champ | Valeur |
|-------|--------|
| **Chantier** | A — CK maquette V1.2.x |
| **Lot** | Mentions légales go-live public |
| **Module** | `dorevia_ck_marketone_content` **19.0.1.1.0** (local · non commité) |
| **Statut** | **Réserve MOA actée · structure OK · contenu juridique non validé** |
| **Instance recette** | `dorevia_ck_marketone_01` |
| **URL contrôle** | http://localhost:18079/legal?db=dorevia_ck_marketone_01 |

---

## Objectif

Lever le verrou **NO GO public** lié à l’absence de page et de lien footer « Mentions légales », sans rouvrir A1, A7, Phase 10 ni Chantier B.

---

## Livrables techniques

| Élément | Détail |
|---------|--------|
| **Page CMS** | `/legal` · vue `dorevia_ck_marketone_content.legal_page` |
| **Classe page** | `ck-legal-page` |
| **Footer** | Lien « Mentions légales » → `/legal` · colonne **Découvrir** · vue `website.footer_custom` |
| **Bootstrap** | `bootstrap_mentions_legales_page` · `bootstrap_footer_legal_link` (idempotents) |
| **Migration** | `19.0.1.1.0/post-migrate.py` |
| **Tests** | `--test-tags=dorevia_ck_marketone_legal` |

---

## Contenu MOA — placeholders à compléter

Sections publiées avec **texte minimal** et marqueurs `[À compléter MOA]` :

1. **Éditeur** — raison sociale, forme juridique, siège, RCS/SIREN, TVA, capital, directeur de publication
2. **Hébergement** — bloc OVH SAS (à ajuster si infra réelle différente)
3. **Propriété intellectuelle** — texte générique
4. **Données personnelles** — renvoi contact · politique `/privacy` **non publiée** (réserve)
5. **CGV** — renvoi tunnel commande · texte CGV détaillé **non publié** (réserve)

Contact par défaut : `contact@c-kreyol.fr` · formulaire `/contactus`.

---

## Recette

| # | Contrôle | Attendu |
|---|----------|---------|
| 1 | GET `/legal` | HTTP 200 · `ck-legal-page` |
| 2 | Footer `/` | `href="/legal"` · libellé « Mentions légales » |
| 3 | Footer `/shop` | lien présent |
| 4 | Mobile 390 | lien footer accessible (pas de régression layout) |
| 5 | Tests Odoo | tag `dorevia_ck_marketone_legal` OK |

---

## Verdict MOA acté (2026-06-14)

**Réserve MOA — mentions légales structurelles OK, contenu juridique non validé**

| Critère | Statut |
|---------|--------|
| Structure `/legal` | ✅ **OK MOA** |
| Lien footer | ✅ **OK MOA** |
| Contenu juridique | ⚠️ **Réserve MOA** — placeholders non publiables |
| Go-live public | **NO GO maintenu** |
| Commit / PR | **En attente** contenu final MOA |

**Document complétion MOA** : [`COMPLETION_MOA_CONTENU_LEGAL_CK_LEGAL.md`](./COMPLETION_MOA_CONTENU_LEGAL_CK_LEGAL.md)  
**Complétion partielle MOA** : E1/E2/E8/E9/H5 renseignés · brouillons V1 `/legal` `/privacy` `/terms` proposés · **standby Dev** · go-live public **NO GO**

---

## Verdict technique (Dev · 2026-06-14)

| Critère | Statut |
|---------|--------|
| Page publiée + lien footer | ✅ |
| Contenu juridique complet | ⚠️ **MOA à compléter** (placeholders éditeur, CGV, privacy) |
| Go-live public | **NO GO définitif** tant que MOA n’a pas validé le contenu juridique final |
| Verrou Phase 10 F3 | **Partiellement levé** — présence technique OK · validation contenu MOA requise |

---

## Périmètre respecté

- ✅ CMS / contenu légal / footer uniquement
- ✅ Pas de modification `dorevia_ck_theme`
- ✅ Pas de Chantier B
- ✅ A1 / A7 / Phase 10 non rouverts

---

*Lot mentions légales · post-merge A7 · 2026-06-14.*
