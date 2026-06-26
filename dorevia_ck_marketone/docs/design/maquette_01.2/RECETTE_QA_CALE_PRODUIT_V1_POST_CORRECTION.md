# Recette QA — Cale produit V1 · Post-correction Axe C

| Champ | Valeur |
| --- | --- |
| Projet | `dorevia_ck_marketone` |
| Axe | C — Mise à niveau BO / données produit |
| Phase | 2 · **Post-correction** |
| Date | 26 juin 2026 |
| Base | `dorevia_ck_marketone_01` |
| Prérequis | Upgrade instance (26/06) + corrections BO MOA effectuées |
| Référence pré-correction | [`PROTOCOLE_QA_AXE_C_SECURISATION_BO_20260624.md`](PROTOCOLE_QA_AXE_C_SECURISATION_BO_20260624.md) |
| Référence baseline v1 | [`RECETTE_QA_CALE_PRODUIT_20260624.md`](RECETTE_QA_CALE_PRODUIT_20260624.md) |
| Hors périmètre | Note 07 / pages catégories pleine largeur — **lot suivant, non lancé** |
| Statut | À exécuter |

---

## Objet

Checklist courte de **vérification terrain** après upgrade Dev + corrections BO Axe C.

**Objectif du jour** : clôturer la cale produit avant d'ouvrir le lot Note 07 (boutique pleine largeur).

```text
Rail 1 (actif)   : Axe C post-correction  ← ce document
Rail 2 (préparé) : Note 07 — NO GO démarrage
```

---

## 0. Prérequis techniques (avant recette)

| # | Action | Fait |
| --- | --- | --- |
| P1 | `-u dorevia_ck_theme` (19.0.1.59.0) + redémarrage worker | ☐ |
| P2 | `-u dorevia_ck_marketone_content` (19.0.1.42.0) + redémarrage worker | ☐ |
| P3 | Corrections BO MOA Axe C (actions 1–9 + arbitrages MOA-1/2) | ☐ |

---

## 1. Checklist post-correction

### A — Livraisons Dev 26/06 (smoke)

| # | Contrôle | Comment vérifier | Attendu | OK |
| --- | --- | --- | --- | --- |
| A1 | Libellé champ vedette accueil | Fiche produit > Ventes > Classement boutique | **Afficher sur l'accueil** (+ infobulle) | ☐ |
| A2 | Logo SVG header desktop | `/` viewport 1280 px | `ck-logo.svg` visible · `aria-label="C-Kréyòl — Accueil"` | ☐ |
| A3 | Logo SVG header mobile | `/` viewport 390 px | Même source SVG · pas de overflow horizontal | ☐ |

Référence : [`RECETTE_QA_LOGO_HEADER_SVG_20260626.md`](RECETTE_QA_LOGO_HEADER_SVG_20260626.md)

---

### B — Coups de cœur (catégorie → curation `ck_is_featured`)

| # | Contrôle | Comment vérifier | Attendu | OK |
| --- | --- | --- | --- | --- |
| B1 | Produits sans catégorie Coups de cœur | BO : fiches Confiture, Manio Crackers, Savon, Panama (ex.) | 0 produit publié avec catégorie « Coups de cœur » | ☐ |
| B2 | Menu header | Header desktop + mobile 390 px | **Pas** d'entrée « Coups de cœur » en nav racine | ☐ |
| B3 | Filmstrip `/shop` | Desktop 1280 px (rendu JS — recette visuelle) | **Pas** de pill « Coups de cœur » | ☐ |
| B4 | Home section 3 | `/` | Titre **Nos coups de cœur** présent · cards affichées si vedettes cochées | ☐ |
| B5 | Pilotage accueil | BO : cocher/décocher **Afficher sur l'accueil** | Home se met à jour (pas de dépendance catégorie) | ☐ |
| B6 | Catégorie en base (MOA-1) | Selon arbitrage MOA | Vide + non exposée **ou** supprimée — documenter choix | ☐ |

---

### C — Navigation et libellés

| # | Contrôle | Comment vérifier | Attendu | OK |
| --- | --- | --- | --- | --- |
| C1 | Libellé Soin & Bien-être | Menu header + page catégorie | **Soin & Bien-être** (pas « Maison & Bien-être ») | ☐ |
| C2 | URL catégorie Soin | Clic menu | `/shop/category/soin-bien-etre-2` · HTTP 200 | ☐ |

---

### D — Traductions `fr_FR`

| # | Contrôle | Comment vérifier | Attendu | OK |
| --- | --- | --- | --- | --- |
| D1 | Attribut Origine | Configuration > Attributs | Libellé **fr_FR** renseigné | ☐ |
| D2 | Valeur Guadeloupe | Fiche Confiture > attributs | **fr_FR** sur la valeur si applicable | ☐ |
| D3 | Galettes de manioc | Nom produit BO + front | **fr_FR** cohérent (pas nom anglais seul en BO) | ☐ |
| D4 | Sous-catégories Épicerie | BO catégories publiques | Biscuits, Confitures, Farines… **fr_FR** renseigné | ☐ |

---

### E — UOM et prix de référence (cards)

| Produit | UOM nette attendue | Prix réf. | OK |
| --- | --- | --- | --- |
| Confiture de goyave | g ou kg | Cohérent (pas Unité(s) / Pack de 6) | ☐ |
| Manio Crackers | g ou kg | Cohérent | ☐ |
| Galettes de manioc | g ou kg | Cohérent | ☐ |
| Savon vétiver | g ou kg (si applicable) | Selon fiche | ☐ |
| Chapeau Panama | — | **Afficher prix réf.** décoché | ☐ |

---

### F — Arbitrage MOA-2 (Jus Mont-Pelé · Pâte de manioc)

| # | Contrôle | Attendu (selon décision MOA documentée) | OK |
| --- | --- | --- | --- |
| F1 | Jus Mont-Pelé — contenance | UOM nette + quantité renseignées **ou** prix réf. désactivé | ☐ |
| F2 | Pâte de manioc — contenance | Idem | ☐ |
| F3 | Cards shop | Ligne meta / prix réf. sans absurdité (ex. « Jours », « Pack de 6 » hors contexte) | ☐ |

---

### G — Cards catalogue (cohérence visible)

| # | Contrôle | Pages | Attendu | OK |
| --- | --- | --- | --- | --- |
| G1 | Grille `/shop` | 1280 px | Cards compactes · origine/meta absents si non renseignés · CTA panier FR | ☐ |
| G2 | Rayon Boissons | `/shop/category/boissons-123` | 1 produit affiché proprement | ☐ |
| G3 | Rayon Soin | `/shop/category/soin-bien-etre-2` | Badge visible si ruban BO (ex. Agriculture Bio) | ☐ |
| G4 | Rayon Artisanat | `/shop/category/artisanat-3` | Badge visible si ruban BO (ex. Nouveau) | ☐ |
| G5 | Fiche produit | `/shop/product/...` | Pas de régression vs baseline | ☐ |
| G6 | Panier | Ajout depuis grille | Badge panier mis à jour | ☐ |

---

## 2. Verdict

| Champ | Valeur |
| --- | --- |
| Date recette | |
| Exécutant | |
| Instance / commit | |
| Résultat global | ☐ GO · ☐ GO avec réserves · ☐ NO GO |

### Réserves / écarts

*(à compléter)*

### Décision

```text
☐ Cale produit V1 clôturée — on peut planifier le démarrage Note 07 (Rail 2)
☐ Corrections BO complémentaires requises avant clôture
```

---

## 3. Rappel séquencement

| Rail | Statut après cette recette |
| --- | --- |
| **Rail 1** Axe C / cale produit | Clôture si GO ci-dessus |
| **Rail 2** Note 07 | Ticket prêt (`83d540a`) — **démarrage seulement après GO Rail 1** |

---

*Recette post-correction Axe C — C-Kréyòl / CK Marketone — 26 juin 2026*
