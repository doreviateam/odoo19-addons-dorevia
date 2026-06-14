# Composition CMS — Page `/professionnels` · CK Marketone

| Champ | Valeur |
|-------|--------|
| **Instance** | `dorevia_ck_marketone_01` |
| **URL** | http://localhost:18079/professionnels |
| **Date** | 2026-06-13 |
| **Ticket** | [`ticket_moa_composition_cms_ck_01`](../ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) §2.3 |
| **GO séquence** | [`go_reprise_odoo_v1_2.md`](./go_reprise_odoo_v1_2.md) |
| **Statut** | **Clôturée OK partiel MOA · Phase 5 · 2026-06-13** |

---

## 1. Livrables

| # | Élément | Statut |
|---|---------|--------|
| 1 | Page CMS `/professionnels` (`website.page` id 5 · view `website.professionnels`) | ✅ |
| 2 | Menu **Professionnels** → `/professionnels` (sequence 40) | ✅ |
| 3 | Double cible (producteurs / distributeurs) | ✅ |
| 4 | Formulaire `website_crm` natif (`crm.lead`) | ✅ |
| 5 | Pas de champ CRM custom | ✅ |
| 6 | Responsive desktop + mobile (390 px) | ✅ — pas d’overflow |

---

## 2. Structure page

1. **Titre** — « Espace professionnel » + lead qualification
2. **Intro** — doctrine CK · prix B2C publics · conditions B2B back-office
3. **Double cible** — 2 blocs :
   - Producteurs & transformateurs créoles · CTA « Proposer vos produits »
   - Boutiques, distributeurs & CHR · CTA « Demander un contact pro »
4. **Note qualification** — demande qualifiée, pas commande B2B
5. **Formulaire** `#ck-pro-form` — `s_website_form` · modèle `crm.lead` · qualification via champ `description`

Snippets utilisés : `s_title` · `s_text_block` · `s_features` (layout 2 colonnes) · `s_website_form`.

---

## 3. Menu website

Ordre actuel :

| Sequence | Menu | URL |
|----------|------|-----|
| 10 | Boutique | `/shop` |
| 20 | Catégories | `/shop` |
| 30 | **Professionnels** | `/professionnels` |

> Header complet : [`COMPOSITION_HEADER_V1_2.md`](./COMPOSITION_HEADER_V1_2.md)

---

## 4. Recette rapide (2026-06-13)

| Contrôle | Résultat |
|----------|----------|
| HTTP `/professionnels` (session DB) | 200 |
| Formulaire `data-model_name="crm.lead"` | présent |
| Double cible visible | oui |
| Overflow mobile 390 px | non |

> **Note instance** : après création CMS via shell, un **restart Odoo** a été nécessaire pour enregistrer la route (`docker restart sandbox-odoo19-odoo-1`).

---

## 5. Suite

```text
✅ Header marchand — COMPOSITION_HEADER_V1_2.md
☐ Hero → Réassurance → Produits → …
☐ Recette formulaire CRM — soumission test lead
☐ Recette finale recette_qa_composition_cms_ck_01.md
```

---

*Composition CMS page Pro — ticket CK 01 · GO reprise Odoo V1.2 · 2026-06-13.*
