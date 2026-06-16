# Onboarding QA — Section 3 · Nos coups de cœur

| Champ | Valeur |
|-------|--------|
| **Public** | Contrôleur qualité · MOA · gestionnaire catalogue |
| **Date** | Révision **2026-06-16** |
| **Focus** | Section 3 « Nos coups de cœur » — V1.1 card + polish front + curation BO |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079/?db=dorevia_ck_marketone_01 |
| **Maquette** | [`artifact/index.html`](./artifact/index.html) (section `#produits`) |
| **Modules** | `dorevia_ck_marketone_content` ≥ **`19.0.1.20.0`** · `dorevia_ck_theme` |
| **Recette visuelle** | **[`RECETTE_VISUELLE_SECTION3_V1_1.md`](./RECETTE_VISUELLE_SECTION3_V1_1.md)** ← **document à exécuter** |
| **Architecture** | [`NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md`](./NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md) |

> **Note historique** : ce document complète la recette PR #73 (merge 2026-06-15). Les évolutions **curation BO**, **badges ruban** et **refresh catégorie** post-#73 sont intégrées ci-dessous.

---

## 1. En une phrase

La Section 3 affiche des **cartes produit maquette** dont la **liste et l'ordre** sont pilotés par la catégorie e-commerce **« Coups de cœur »**, et les **badges** par le **ruban** de chaque fiche produit.

---

## 2. Où en est le chantier

| Section | Bloc | Statut |
|---------|------|--------|
| 1 | Hero | ✅ Mergé — PR #71 |
| 2 | Trust-bar | ✅ Mergé — PR #72 |
| **3** | **Nos coups de cœur** | ✅ **V1.1 livrée** — card enrichie + polish front (`20.0`) · curation BO · badges ruban |
| 4 | Catégories / univers | Suite chantier home |

---

## 3. Principe (rappel)

```text
BO Odoo = source de vérité (produits, catégorie vedettes, rubans, prix, images)
Sélection home = produits de la catégorie « Coups de cœur » (xmlid stable)
Badges = ruban e-commerce (website_ribbon_id) par produit
Rendu home = SSR custom CK (HTML injecté — pas Dynamic Products)
/shop natif = inchangé
```

---

## 4. Comment tester la curation BO

### Ajouter / retirer un produit vedette

**Méthode A — fiche produit** : eCommerce → catégories → cocher / décocher « Coups de cœur » → Enregistrer.

**Méthode B — fiche catégorie** : eCommerce → Catégories → « Coups de cœur » → modifier la liste produits → Enregistrer.

**Attendu** : la home se met à jour (reconstruction HTML automatique).

### Ordonner les vedettes

Fiche produit → **Séquence du site web** (`website_sequence`) → ordre croissant sur la home.

### Badges

Fiche produit → eCommerce → **Ruban** (ex. « Coup de cœur », « Nouveau ! »).

**Attendu** : badge haut **droite** de la carte ; absent si pas de ruban.

---

## 5. Catalogue MOA de référence

Set initial (migration `18.0`) — exemple historique **5 cartes** si les 4 parents sont en catégorie, mais ce n'est pas une règle fixe :

| Carte home | Modèle BO | Ruban suggéré |
|------------|-----------|---------------|
| Confiture de goyave | Template simple | Coup de cœur |
| Manio Crackers salé | Variante Format · parent Manio | Nouveau ! (sur le parent) |
| Manio Crackers sucré | Variante Format · parent Manio | idem |
| Galettes de manioc | Template séparé | (aucun ou au choix) |
| Savon vétiver | Template simple | (aucun ou au choix) |

**Règle actuelle à recetter** : Confiture + Manio seuls dans « Coups de cœur » → **3 cartes** (Galettes et Savon absents). La section ne doit pas compléter à 5.

---

## 6. Accès recette

```text
URL      : http://localhost:18079/?db=dorevia_ck_marketone_01
Home     : /
Shop     : /shop
Maquette : artifact/index.html
```

**Viewports** : desktop **1280** · mobile **390**.

---

## 7. Checklist QA — résumé (détail dans recette visuelle)

> **Commande QA** : exécuter la recette visuelle complète → [`RECETTE_VISUELLE_SECTION3_V1_1.md`](./RECETTE_VISUELLE_SECTION3_V1_1.md)

| # | Contrôle | ☐ |
|---|----------|---|
| 1 | Titre + sous-titre **« origine, goût et savoir-faire créole »** + « Toute la boutique » aligné | |
| 2 | Cards = produits catégorie « Coups de cœur » uniquement (nombre variable, max 8) | |
| 3 | Étiquettes **produit** visibles sous le nom (ex. Guadeloupe · Épicerie) | |
| 4 | Prix TTC + ligne `320 g · 18,13 €/kg` si renseigné en BO | |
| 5 | CTA **« Voir le produit »** + card entière cliquable + hover discret | |
| 6 | Badge = ruban BO · haut droite | |
| 7 | Curation BO (ajout / retrait / ordre) | |
| 8 | Mobile 390 + desktop 1280 | |
| 9 | BO : pas de doublon étiquettes card · quantité vide sans `0,00` | |
| 10 | Non-régression S1 Hero + S2 trust-bar + `/shop` | |

---

## 8. Pièges connus (ne pas confondre avec des bugs)

| Symptôme | Cause | Action |
|----------|-------|--------|
| Home inchangée après edit BO | HTML « cuit » pas encore régénéré | Ré-enregistrer fiche produit ou catégorie ; ou upgrade module |
| Prix à 1,00 € alors que BO différent | Ancien HTML figé | Modifier prix en BO + enregistrer (déclenche refresh) |
| 5 cartes alors que catégorie n'en a que 3 | Ancien HTML ou repli auto (catégorie vide) | Vérifier xmlid catégorie · ré-enregistrer |
| Pas de badge | Pas de ruban sur le produit | Assigner ruban en BO |

---

## 9. Tests automatiques

```bash
docker exec sandbox-odoo19-odoo-1 bash -c \
  'odoo -d dorevia_ck_marketone_01 --http-port=8079 --no-http \
   -u dorevia_ck_theme,dorevia_ck_marketone_content \
   --test-tags dorevia_ck_marketone_home_section3,dorevia_ck_marketone_home_section3_curation,dorevia_ck_marketone_catalog_manioc,dorevia_ck_marketone_home_section2,dorevia_ck_marketone_home_lot1 \
   --stop-after-init'
```

**Attendu** : `0 failed, 0 error(s)`.

---

## 10. Documents de référence

| Document | Usage |
|----------|-------|
| [`NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md`](./NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md) | **Guide principal** — architecture + gestionnaire |
| [`SPEC_SECTION3_VEDETTES_CURATION_BO_V1.md`](./SPEC_SECTION3_VEDETTES_CURATION_BO_V1.md) | Spec curation · matrice livraison |
| [`RECETTE_VISUELLE_SECTION3_V1_1.md`](./RECETTE_VISUELLE_SECTION3_V1_1.md) | **Recette visuelle V1.1** — checklist + captures + PV |
| [`DECISION_MOA_SECTION3_PR73_CURATION_REPORTEE_V1.md`](./DECISION_MOA_SECTION3_PR73_CURATION_REPORTEE_V1.md) | Arbitrage initial curation reportée |

---

*Onboarding QA Section 3 — révision 2026-06-16 · `content` ≥ `19.0.1.20.0` · recette visuelle V1.1.*
