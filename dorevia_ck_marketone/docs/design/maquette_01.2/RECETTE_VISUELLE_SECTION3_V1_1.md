# Recette visuelle QA — Section 3 « Nos coups de cœur » V1.1 + polish

| Champ | Valeur |
|-------|--------|
| **Public** | Contrôleur qualité · MOA |
| **Date** | 2026-06-16 |
| **Périmètre** | Section 3 home uniquement — **recette visuelle** (pas de revalidation architecture) |
| **Verdict attendu** | GO visuel · GO sous réserves · NO GO |
| **Instance** | `dorevia_ck_marketone_01` — http://localhost:18079/?db=dorevia_ck_marketone_01 |
| **Modules** | `dorevia_ck_marketone_content` ≥ **`19.0.1.20.0`** · `dorevia_ck_theme` (assets à jour) |
| **Références** | [`ONBOARDING_QA_SECTION3_PR73_V1.md`](./ONBOARDING_QA_SECTION3_PR73_V1.md) · [`NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md`](./NOTE_ARCHITECTURE_SECTION3_VEDETTES_V1.md) |

---

## 1. Ordre de mission QA

**Objectif** : valider visuellement et fonctionnellement la Section 3 après livraison **V1.1** (card enrichie) et **polish front** (sous-titre, header, hover, card cliquable).

**Hors périmètre** (ne pas bloquer sur ces points) :

- logique automatique « Nouveau &lt; 30 jours » ;
- champ « Accroche coup de cœur » ;
- refonte `/shop` ;
- Section 4 et suivantes.

**Prérequis environnement** :

```bash
docker exec sandbox-odoo19-odoo-1 bash -c \
  'odoo -d dorevia_ck_marketone_01 --http-port=8079 --no-http \
   -u dorevia_ck_theme,dorevia_ck_marketone_content --stop-after-init'
```

Puis **hard refresh** navigateur (`Cmd+Shift+R` / `Ctrl+Shift+R`) sur `/`.

**Viewports obligatoires** :

| Viewport | Largeur | Usage |
|--------|---------|--------|
| Desktop | **1280** | Grille 3 colonnes · header section |
| Mobile | **390** | 1 colonne · lisibilité prix / CTA |

**Captures à déposer** : `docs/design/maquette_01.2/captures/recette_section3_v1_1/`

| Fichier suggéré | Contenu |
|-----------------|---------|
| `s3_desktop_1280_full.png` | Section complète desktop |
| `s3_desktop_1280_card_confiture.png` | Zoom card Confiture |
| `s3_desktop_1280_hover.png` | Card au survol (ombre + zoom image) |
| `s3_mobile_390_full.png` | Section complète mobile |
| `s3_bo_fiche_produit_ecommerce.png` | Onglet Boutique eCommerce BO |

---

## 2. Jeu de données de référence (instance recette)

Vérifier en BO avant la recette :

| Produit | Catégorie « Coups de cœur » | Étiquettes produit | Ruban | Quantité nette |
|---------|----------------------------|-------------------|-------|----------------|
| Confiture de goyave | Oui | ex. Guadeloupe · Épicerie | au choix MOA | ex. 320 g · prix/kg |
| Manio Crackers | Oui | (vide ou renseigné) | optionnel | optionnel |

**Attendu home** (si seuls Confiture + Manio sont curatés) : **3 cartes** (Confiture + Manio salé + Manio sucré).

---

## 3. Checklist visuelle — header de section

| # | Contrôle | Attendu visuel | ☐ | Note |
|---|----------|----------------|---|------|
| H1 | Titre | **« Nos coups de cœur »** | | |
| H2 | Sous-titre | **« Sélection CK · origine, goût et savoir-faire créole »** — pas l’ancien libellé « prix TTC · origine et famille visibles » | | |
| H3 | Bouton « Toute la boutique → » | Aligné verticalement avec le bloc titre/sous-titre (pas « flottant » trop bas) | | |
| H4 | Lien boutique | Clic → `/shop` | | |

---

## 4. Checklist visuelle — card produit (ex. Confiture)

Structure attendue **de haut en bas** :

```text
[Image 1:1]                    [Ruban haut droite si renseigné]
Nom produit
Étiquettes produit             (ex. Guadeloupe · Épicerie)
Prix TTC
Quantité · prix référence      (ex. 320 g · 18,13 €/kg)
[Voir le produit]
```

| # | Contrôle | Attendu visuel | ☐ | Note |
|---|----------|----------------|---|------|
| C1 | Image | Ratio **1:1**, pas de placeholder Odoo générique | | |
| C2 | Ruban | Badge **haut droite** si ruban BO ; **absent** sans ruban | | |
| C3 | Nom | Libellé variante si Manio (salé / sucré) | | |
| C4 | Étiquettes | Ligne sous le nom = **Étiquettes produit** BO (`Guadeloupe · Épicerie`) — **pas** de champ séparé « Étiquettes card » | | |
| C5 | Prix TTC | Cohérent fiche produit (pas 1,00 € figé si BO différent) | | |
| C6 | Ligne commerciale | `320 g · 18,13 €/kg` si renseigné ; masquée si quantité vide | | |
| C7 | CTA | Libellé **« Voir le produit »** (pas « Voir » seul) | | |
| C8 | Clic CTA | Ouvre la **bonne fiche** / variante | | |
| C9 | Card entière cliquable | Clic sur image, nom ou zone prix → même fiche que le CTA | | |
| C10 | Hover desktop | Ombre légèrement renforcée · zoom image discret · transition douce · pas d’effet agressif | | |

---

## 5. Checklist visuelle — grille et curation

| # | Contrôle | Attendu | ☐ | Note |
|---|----------|---------|---|------|
| G1 | Nombre de cards | = produits curatés (**3** si Confiture + Manio seuls) — **pas 5 forcées** | | |
| G2 | Plafond | Max **8** si plus de produits en catégorie | | |
| G3 | Ordre | Suit `website_sequence` BO | | |
| G4 | Produit retiré de « Coups de cœur » | Disparaît après enregistrement BO + refresh home | | |
| G5 | Mobile 390 | Pas d’overflow horizontal · prix et CTA lisibles | | |

---

## 6. Checklist BO (lisibilité gestionnaire)

Onglet **Boutique eCommerce** — organisation attendue :

```text
Publication
  · Est publié

Classement boutique
  · Catégories
  · Ruban
  · Étiquettes produit

Quantité commerciale
  · Quantité nette
  · Unité de quantité nette
  · Afficher le prix au kg / litre
  · Unité du prix de référence
```

| # | Contrôle | Attendu | ☐ |
|---|----------|---------|---|
| B1 | Pas de bloc « Affichage card » / « Étiquettes visibles sur la card » | | |
| B2 | Quantité nette vide = champ **vide** (pas `0,00`) | | |
| B3 | Modifier étiquettes produit → ligne home mise à jour après enregistrement | | |

---

## 7. Non-régression rapide

| # | Contrôle | ☐ |
|---|----------|---|
| N1 | Section 2 trust-bar **au-dessus** de Section 3 | |
| N2 | `/shop` inchangé (spot check grille native) | |
| N3 | Pas de carousel Odoo Dynamic Products dans Section 3 | |

---

## 8. Pièges connus (ne pas ouvrir de bug à tort)

| Symptôme | Action QA |
|----------|-----------|
| Étiquettes absentes sur la card alors qu’elles sont en BO | Hard refresh · ré-enregistrer la fiche produit (reconstruction home) |
| Sous-titre ancien | Vérifier version module ≥ `19.0.1.20.0` · upgrade · hard refresh |
| Badge « Nouveau ! » sur tous les produits | **Contenu BO** — retirer ruban sur les produits non concernés (pas un bug dev) |
| Home inchangée après edit BO | Ré-enregistrer produit ou catégorie « Coups de cœur » |

---

## 9. Tests auto (complément, non substitut visuel)

```bash
docker exec sandbox-odoo19-odoo-1 bash -c \
  'odoo -d dorevia_ck_marketone_01 --http-port=8079 --no-http \
   -u dorevia_ck_theme,dorevia_ck_marketone_content \
   --test-tags dorevia_ck_marketone_home_section3,dorevia_ck_marketone_home_section3_curation \
   --stop-after-init'
```

**Attendu** : `0 failed, 0 error(s)`.

---

## 10. PV de recette (à remplir par QA)

| Champ | Valeur |
|-------|--------|
| **Recetteur** | QA Codex |
| **Date** | 2026-06-16 |
| **Commit / version module** | `dorevia_ck_marketone_content` 19.0.1.20.4 |
| **Verdict global** | ☑ GO · ☐ GO sous réserves · ☐ NO GO |

**Réserves** (si GO sous réserves) :

1. Sans objet.

**Bloquants** (si NO GO) :

1. Sans objet.

**Constat de validation QA** :

1. Desktop 1280 conforme : titre `Nos coups de cœur`, sous-titre `Sélection CK · origine, goût et savoir-faire créole`, bouton `Toute la boutique →` pointant vers `/shop`.
2. Grille Section 3 conforme : `3` cards visibles, cohérentes avec la curation attendue.
3. Card `Confiture de goyave` conforme : ligne d'étiquettes visible (`Épicerie · Guadeloupe`), prix `5,80 €`, ligne commerciale `320 g · 18,13 €/kg`, CTA `Voir le produit`.
4. Interaction validée : clic sur la card `Confiture de goyave` redirige bien vers `http://localhost:18079/shop/confiture-de-goyave-3`.
5. Mobile 390 conforme sur les points de base : `3` cards, CTA visible, prix visible, pas d'overflow horizontal.

---

*Recette visuelle Section 3 V1.1 — 2026-06-16 · à exécuter avant merge / tag release Section 3.*
