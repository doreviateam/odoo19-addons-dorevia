# Livraison Dev — Maquette CK V1.2.x · Lot 3+

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **GO MOA** | [`go_moa_maquette_v1_2_x_lot3.md`](./go_moa_maquette_v1_2_x_lot3.md) |
| **Date livraison** | 2026-06-13 |
| **Statut** | **Verdict MOA OK — vision complète** · [`decision_moa_verdict_maquette_v1_2_x_vision_complete.md`](./decision_moa_verdict_maquette_v1_2_x_vision_complete.md) |

```text
ODOO EN PAUSE — AUCUNE TRADUCTION ODOO
```

---

## 1. Artifact HTML livré

| Page | Fichier | Route Odoo cible |
|------|---------|------------------|
| À propos / démarche CK | [`artifact/a-propos.html`](./artifact/a-propos.html) | `/a-propos` |
| **Fiche producteur type** | [`artifact/fiche-producteur.html`](./artifact/fiche-producteur.html) | `/producteur/atelier-hauts-goyaviers` |
| Recettes & savoirs | [`artifact/recettes.html`](./artifact/recettes.html) | `/recettes` ou `/savoirs` |
| Contact | [`artifact/contact.html`](./artifact/contact.html) | `/contactus` |

**Preview** : `http://127.0.0.1:8766/fiche-producteur.html` · `…/a-propos.html` · `…/recettes.html` · `…/contact.html`

---

## 2. Vision CK complète (Lots 1 + 2 + 3+)

| Lot | Rôle |
|-----|------|
| **Lot 1** | Promesse · fiche produit · Pro |
| **Lot 2** | Catalogue · catégorie · parcours achat |
| **Lot 3+** | Confiance · **producteur** · éditorial · contact |

```text
Producteur → Origine → Savoir-faire → Produits → Usage → Achat → Logistique CK
```

Parcours démo :

```text
Accueil → Shop → Catégorie → Fiche produit → Fiche producteur
     ↘ À propos · Recettes · Contact · Pro
```

---

## 3. Fiche producteur type (`fiche-producteur.html`)

**Producteur modèle** : Atelier Les Hauts Goyaviers · Saint-Pierre, La Réunion — cohérent avec la fiche produit Confiture goyavier.

| Bloc MOA | Contenu |
|----------|---------|
| 7.1 Hero | Nom · Réunion · visuel verger · tagline · CTA produits / Pro |
| 7.2 Présentation | Histoire · savoir-faire · territoire · raison CK · encart « En bref » |
| 7.3 Critères sélection | 6 critères CK (qualité · origine · cohérence · commercial · appro · compatibilité) |
| 7.4 Produits proposés | **Grille 4 cartes** · visuel · prix · origine · lien fiche produit |
| 7.5 Sélection CK | 2 focus emblématiques · badges Incontournable / Découverte / Pour les pros |
| 7.6 Usage / conseil | Clafoutis goyavier · associations · lien recettes |
| 7.7 Logistique CK | Sélection · Europe · service client · distinction B2B |
| 7.8 CTA sortie | Boutique · collection · Pro · proposer producteur |

**Phrase de référence** : « Voici d’où ça vient, qui le fait, pourquoi CK l’a choisi, et quels produits je peux découvrir. »

**Réserve explicite** : pas d’annuaire partenaires · pas de portail producteur · pas de fiches auto-générées Odoo fournisseur.

---

## 4. À propos · Recettes · Contact

Voir sections précédentes — enrichies :

* **À propos** : lien vers fiche producteur type ;
* **Recettes** : carte « Comprendre la sélection CK » → fiche producteur ;
* **Contact** : 4 parcours (ajout « Proposer un producteur ») · sujet formulaire dédié.

---

## 5. Liens transverses

| Source | Lien |
|--------|------|
| Fiche produit | Bloc producteur → `fiche-producteur.html` |
| Accueil éditorial | À propos · fiche producteur · recettes |
| Footer (9 pages) | Découvrir : À propos · **Fiche producteur** · Recettes · Contact |

---

## 6. Classes d’arbitrage — première lecture Lot 3+

| Classe | Éléments |
|--------|----------|
| **V1 prioritaire** | À propos CMS · contact `/contactus` · grille produits fiche producteur · logistique CK · distinction Pro |
| **V1 possible** | Fiche producteur CMS · critères sélection · focus emblématiques · recettes statiques · 4 parcours contact |
| **V1 différée** | Annuaire producteurs · blog · recettes auto-liées · fiches fournisseur Odoo natives |
| **Réserve** | Page CMS vs module fournisseur · forum · portail · workflow proposition producteur |
| **Hors scope** | Annuaire partenaires · portail producteur · espace connecté · automation |

---

## 7. Suite MOA

```text
1. ✅ GO MOA Lot 3+ (fiche producteur incluse)
2. ✅ Production artifact Lot 3+ — ce document
3. ✅ Recette QA Lot 3+ — [`recette_qa_maquette_v1_2_x_lot3.md`](./recette_qa_maquette_v1_2_x_lot3.md)
4. ✅ Verdict MOA · vision CK complète — [`decision_moa_verdict_maquette_v1_2_x_vision_complete.md`](./decision_moa_verdict_maquette_v1_2_x_vision_complete.md)
5. ✅ Arbitrage périmètre V1 traduisible — [`ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md`](./ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md)
6. ☐ Décisions MOA M1–M9 · GO Odoo — [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md)
```

---

*Livraison Dev maquette CK V1.2.x Lot 3+ · 2026-06-13.*
