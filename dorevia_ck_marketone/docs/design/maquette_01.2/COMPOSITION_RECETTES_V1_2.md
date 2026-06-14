# Composition — Page Recettes & savoirs · M2 · CK V1.2.x

| Champ | Valeur |
|-------|--------|
| **Référence maquette** | [`artifact/recettes.html`](./artifact/recettes.html) |
| **Route Odoo cible** | `/recettes` |
| **Classe page** | `ck-recipes-page` |
| **Décision** | **M2** — CMS statique · pas blog V1 |
| **Statut** | **Dossier préparation Phase 8 · Dev interdit** |

---

## 1. Intention éditoriale

Page éditoriale simple : usages · transmission · cuisine créole. Contenu lié au catalogue CK — **pas** de moteur éditorial · pas de contribution utilisateur.

---

## 2. Structure pressentie (Odoo)

| # | Bloc maquette | Traduction Odoo | Snippet / composant |
|---|---------------|-----------------|---------------------|
| 8.1 | Hero éditorial | Titre · kicker · lead | `s_title` · `s_text_block` |
| 8.2 | Grille 6 cartes | Recettes · guides · conseils | Cartes CMS · `s_card` / `s_image_text` / grille custom légère |
| 8.3 | Liens catalogue | Produit · shop · catégorie · producteur | Liens BO réels uniquement |
| 8.4 | Note garde-fou | Pas blog / forum | Texte CMS ou absent en prod |

**Enveloppe obligatoire** : `t-call="website.layout"` via `_wrap_website_page_arch()` — **non négociable** (retour d’expérience Phase 7 · 19.0.1.5.0).

---

## 3. Cartes éditoriales — mapping pressenti

| Carte maquette | Type | Lien Odoo pressenti |
|----------------|------|---------------------|
| Clafoutis créole au goyavier | Recette | Produit BO publié (ex. confiture goyave) |
| Comment utiliser les épices colombo | Guide | `/shop` ou catégorie BO si existante |
| Galettes et farine de manioc | Conseil | `/shop` · catégorie épicerie |
| Première commande CK | Guide achat | `/shop` |
| Sirops créoles | Usage | `/shop` · lien sobre si pas de produit cible |
| Comprendre la sélection CK | Savoir | `/producteur/atelier-hauts-goyaviers` · `/a-propos` |

**Règle** : pas de lien fictif maquette · pas `fiche-produit.html` · pas `/recettes` auto-référencé avant publication.

---

## 4. Hors périmètre M2

```text
website_blog · articles dynamiques · commentaires · forum · RSS
Filtres · recherche éditoriale custom · tags recettes BO
Modification header/footer/mega-menu (sauf acte MOA post-recette)
Modification home · shop · fiche produit · contact · à propos · producteur
```

---

## 5. Liens entrants différés (post Phase 8)

| Source | Lien | Statut actuel |
|--------|------|---------------|
| Mega-menu Découvrir | `/recettes` | Exclu Phase 1 · **option post-recette MOA** |
| À propos | CTA recettes | Différé Phase 8 |
| Fiche producteur | Usage / conseil → recettes | Différé Phase 8 |
| Fiche produit | Idée recette inline | Différé · hors scope Phase 8 strict |

---

## 6. Capital instance (état actuel)

| Élément | Instance `dorevia_ck_marketone_01` |
|---------|-------------------------------------|
| Route `/recettes` | **Absente** |
| Page CMS | **À créer** |
| `website_blog` | **Non installé** — conforme M2 |

---

*Composition Recettes V1.2 — dossier Phase 8 · préparation MOA · Dev interdit · 2026-06-14.*
