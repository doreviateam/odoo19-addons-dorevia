# Plan de recette manuelle — `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079 |
| **Module** | `dorevia_ckreyol_marketone` — version cible **`19.0.4.0.0`** |
| **Langue recette** | **Français (`fr_FR`)** — EUR |
| **Dernière mise à jour** | 2026-05-18 |

Document opérationnel pour validation **humaine** (MOA). Les tests automatisés restent la référence technique : voir [`ENV_REFERENCE.md`](ENV_REFERENCE.md).

---

## 1. Prérequis

### Environnement

- [ ] Docker `sandbox-odoo19` démarré
- [ ] Base **`ckr-marketone-01`** sélectionnée (login Odoo ou cookie)
- [ ] Module **`dorevia_ckreyol_marketone`** installé / à jour (`19.0.4.0.0` minimum pour Lot 4)
- [ ] **`dorevia_ckreyol_marketplace`** et **`theme_classic_store`** non installés

### Navigateur

- [ ] Session fraîche ou navigation privée recommandée (éviter cache langue / panier)
- [ ] Langue navigateur : français de préférence
- [ ] Deux largeurs testées : **mobile ~375 px** et **desktop ≥ 1280 px**

### Catalogue de recette (BO)

- [ ] **3 produits** publiés avec image (déjà créés en recette, ou équivalent) :

| Produit | Prix indicatif | URL indicative |
|---------|----------------|----------------|
| Maniocookies salés La Platine | 4,90 € | `/shop/maniocookies-sales-la-platine-7` |
| Crackers manioc Sainte-Anne | 5,50 € | `/shop/crackers-manioc-sainte-anne-8` |
| Pâtes de manioc Mayotte | 6,20 € | `/shop/pates-de-manioc-mayotte-9` |

Images source possible : [`ASSETS_REFERENCE.md`](ASSETS_REFERENCE.md).

### Localisation France

- [ ] Site en **français** (libellés : Boutique, Tous les produits, etc.)
- [ ] Prix affichés en **€** (format `4,90 €` et non `$4.90`)

---

## 2. Périmètre de cette recette

| Inclus | Exclu (hors scope actuel) |
|--------|---------------------------|
| Home `/` | Page Contact `/contactus` (Odoo native — ticket futur) |
| Boutique `/shop` | Panier / checkout détaillé (Lot 5) |
| Fiche produit `/shop/<produit>` | Portes catalogue (Lot 6) |
| Header / footer globaux | Contenus éditoriaux lourds (750g / Caribshopper) |
| Panier : ajout + accès | Seed XML, logique métier custom |

**Doctrine** : fiche **retail**, non encyclopédique — produit et CTA d'achat prioritaires (ADR-018, contrat C7.4).

**Référence visuelle** : ne pas faire **moins bien** que le design system **Artisanal Terroir** (Lot 2.1 GO avec réserves).

---

## 3. Enveloppe globale (Lots 2.1 + chrome)

*Rappel — Lot 2.1 déjà GO avec réserves ; vérifier non-régression avant / pendant Lot 4.*

### 3.1 Header

| # | Test | Attendu | OK | KO | Notes |
|---|------|---------|----|----|-------|
| H1 | Logo texte | `C-Kreyol` visible (provisoire accepté) | ☐ | ☐ | |
| H2 | Navigation | Accueil / Boutique / Contact accessibles | ☐ | ☐ | |
| H3 | Utilitaires | Panier, recherche, connexion présents et cliquables | ☐ | ☐ | |
| H4 | Style | Fond clair, typo cohérente, pas d'aspect Odoo natif brut | ☐ | ☐ | |
| H5 | Mobile | Menu burger / offcanvas utilisable | ☐ | ☐ | |

### 3.2 Footer

| # | Test | Attendu | OK | KO | Notes |
|---|------|---------|----|----|-------|
| F1 | Contenu | Blocs C-Kreyol (marque, Boutique, Confiance) | ☐ | ☐ | |
| F2 | Absence Odoo | Pas de « Useful Links », « About us », contacts fictifs Odoo | ☐ | ☐ | |
| F3 | Powered by | « Powered by odoo » non visible | ☐ | ☐ | |
| F4 | Contact | « Contact : à compléter » accepté en sandbox | ☐ | ☐ | Réserve MOA |

### 3.3 Design system (Artisanal Terroir)

| # | Test | Attendu | OK | KO | Notes |
|---|------|---------|----|----|-------|
| D1 | Palette | Terracotta `#884523`, fonds ivoire / crème | ☐ | ☐ | |
| D2 | Typo | Titres serif (EB Garamond), body sans (Hanken Grotesk) | ☐ | ☐ | |
| D3 | Boutons primaires | CTA terracotta, pill, cohérents home / shop | ☐ | ☐ | |

---

## 4. Home `/`

| # | Test | Attendu | OK | KO | Notes |
|---|------|---------|----|----|-------|
| A1 | Scope CSS | Présence `marketone-root` (inspecteur ou vue source) | ☐ | ☐ | |
| A2 | Contenu | Épicerie fine créole, C-Kreyol, accroche, CTA « Découvrir la boutique » | ☐ | ☐ | |
| A3 | CTA | Lien vers `/shop` | ☐ | ☐ | |
| A4 | Réassurance | 3 puces visibles | ☐ | ☐ | |
| A5 | Absence shop | Pas de classe `marketone-shop` sur la home | ☐ | ☐ | |
| A6 | Mobile | Bloc intro lisible, CTA accessible au pouce | ☐ | ☐ | |

---

## 5. Boutique `/shop` (Lot 3 + 2.1)

| # | Test | Attendu | OK | KO | Notes |
|---|------|---------|----|----|-------|
| B1 | Scope CSS | `marketone-shop` sur la page | ☐ | ☐ | |
| B2 | Titre | « Tous les produits » (FR) | ☐ | ☐ | |
| B3 | Grille | **3 cartes** produits avec image, nom, prix en **€** | ☐ | ☐ | |
| B4 | Cartes | Bordures / radius / hover sobres, cohérents charte | ☐ | ☐ | |
| B5 | Prix | Format français (`4,90 €`, virgule décimale) | ☐ | ☐ | |
| B6 | Filtres Odoo | Filtre prix / tri Odoo toujours utilisables (pas cassés) | ☐ | ☐ | |
| B7 | Lien fiche | Clic carte → ouvre fiche produit | ☐ | ☐ | |
| B8 | Absence product | Pas de `marketone-product` sur `/shop` | ☐ | ☐ | |
| B9 | Mobile | Grille lisible, pas de débordement horizontal | ☐ | ☐ | |

---

## 6. Fiche produit — Lot 4 (cœur de recette)

**Fiche dédiée MOA** (Lot 4 seul, ~25 min) : → [`RECETTE_MANUELLE_LOT4.md`](RECETTE_MANUELLE_LOT4.md)

**Produit de référence recommandé** : Crackers manioc Sainte-Anne (ou tout produit avec image).

Répéter les sections **6.2 à 6.5** sur **au moins 2 produits** (dont 1 en mobile).

### 6.1 Accès

| # | Test | Attendu | OK | KO | Notes |
|---|------|---------|----|----|-------|
| P1 | URL | `/shop/<slug>` répond 200, pas d'erreur serveur | ☐ | ☐ | |
| P2 | Scope CSS | Classe **`marketone-product`** sur `#wrap` uniquement | ☐ | ☐ | |
| P3 | Absence shop | Pas de `marketone-shop` sur la fiche | ☐ | ☐ | |

### 6.2 Desktop (≥ 1280 px)

| # | Test | Attendu | OK | KO | Notes |
|---|------|---------|----|----|-------|
| P4 | Fil d'Ariane | Retour boutique lisible | ☐ | ☐ | |
| P5 | Titre (H1) | Nom produit lisible, EB Garamond, hiérarchie claire | ☐ | ☐ | |
| P6 | Prix | Prix visible, contraste suffisant, format € | ☐ | ☐ | |
| P7 | Galerie | Images avec radius / respiration, pas écrasées | ☐ | ☐ | |
| P8 | CTA | Bouton **Ajouter au panier** visible, style terracotta | ☐ | ☐ | |
| P9 | Description | Texte court lisible ; **pas** de mur encyclopédique | ☐ | ☐ | ADR-018 |
| P10 | Variantes | Si variantes BO : sélecteurs utilisables (non masqués) | ☐ | ☐ | N/A si sans variante |
| P11 | Niveau visuel | Au moins égal à home + shop (Lot 2.1) | ☐ | ☐ | |

### 6.3 Mobile (~375 px)

| # | Test | Attendu | OK | KO | Notes |
|---|------|---------|----|----|-------|
| P12 | Layout | Image + infos empilées, pas de scroll horizontal | ☐ | ☐ | |
| P13 | CTA | Ajouter au panier accessible sans zoom | ☐ | ☐ | |
| P14 | Prix + titre | Lisibles sans chevauchement | ☐ | ☐ | |

### 6.4 Parcours panier (fonctionnel minimal)

| # | Test | Attendu | OK | KO | Notes |
|---|------|---------|----|----|-------|
| P15 | Ajout panier | Clic CTA → article dans le panier (icône / `/shop/cart`) | ☐ | ☐ | |
| P16 | Quantité | Modifier quantité possible (comportement Odoo standard) | ☐ | ☐ | |
| P17 | Retour | Retour boutique ou home sans erreur | ☐ | ☐ | |
| P18 | Checkout | Pas de test paiement exigé au Lot 4 ; page panier accessible | ☐ | ☐ | Lot 5 |

### 6.5 Doctrine produit (checklist qualitative)

| # | Test | Attendu | OK | KO | Notes |
|---|------|---------|----|----|-------|
| P19 | Retail first | Produit + prix + CTA dominent la page | ☐ | ☐ | |
| P20 | Pas 750g | Pas de densité média / recettes longues / onglets savoir | ☐ | ☐ | |
| P21 | Pas marketplace | Pas de logique pays / diaspora / portes catalogue | ☐ | ☐ | |

---

## 7. Non-régression transversale

| # | Test | Attendu | OK | KO | Notes |
|---|------|---------|----|----|-------|
| R1 | `/` après visite fiche | Home intacte (`marketone-root`) | ☐ | ☐ | |
| R2 | `/shop` après visite fiche | Liste intacte (`marketone-shop`) | ☐ | ☐ | |
| R3 | Header / footer | Identiques sur `/`, `/shop`, fiche | ☐ | ☐ | |
| R4 | Recherche | Ouverture recherche depuis header OK | ☐ | ☐ | |
| R5 | Connexion | Lien connexion présent (pas de régression) | ☐ | ☐ | |
| R6 | Contact | `/contactus` reste accessible (contenu Odoo accepté en réserve) | ☐ | ☐ | |

---

## 8. Tests automatisés (rappel technique)

À lancer avant ou après recette visuelle pour confirmer le socle :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d ckr-marketone-01 \
  -u dorevia_ckreyol_marketone \
  --test-enable --stop-after-init \
  --test-tags=dorevia_marketone_smoke,dorevia_marketone_lot2,dorevia_marketone_lot2_1,dorevia_marketone_lot3,dorevia_marketone_lot4 \
  --http-port=8071
```

**Attendu** : `0 failed, 0 error(s)` (37 tests au Lot 4).

---

## 9. Grille de décision — Lot 4

### Critère GO (rappel ticket)

```text
Une fiche produit peut être consultée, comprise et ajoutée au panier sans friction,
avec un rendu visuel au moins au niveau du design system Artisanal Terroir Lot 2.1.
```

### Verdict

| Décision | Cocher |
|----------|--------|
| **GO** | ☐ |
| **GO avec réserves** | ☑ |
| **NO GO** | ☐ |

**Date** : 2026-05-18  
**Validé par** : MOA

### Réserves éventuelles (si GO avec réserves)

```text
1. Compteur panier à 2 sur captures : double clic CTA pendant recette — pas une anomalie fonctionnelle.
```

### Motifs NO GO (si applicable)

```text
- 
```

---

## 10. Après décision Lot 4

| Décision | Action |
|----------|--------|
| **GO** ou **GO avec réserves** | Commit / push Lot 4 ; mise à jour ticket + ROADMAP ; enchaîner préparation **Lot 5** (panier / checkout smoke) |
| **NO GO** | Retour équipe dev avec numéros de tests KO ; pas de commit Lot 4 |

---

## 11. Références

| Document | Usage |
|----------|--------|
| [`ENV_REFERENCE.md`](ENV_REFERENCE.md) | Infra, commandes, modules interdits |
| [`ASSETS_REFERENCE.md`](ASSETS_REFERENCE.md) | Images produits recette |
| [`tickets/TICKET_MARKETONE_LOT4_PRODUCT.md`](../tickets/TICKET_MARKETONE_LOT4_PRODUCT.md) | Périmètre Lot 4 |
| [`tickets/TICKET_MARKETONE_LOT2_1_DESIGN_SYSTEM_MINIMAL.md`](../tickets/TICKET_MARKETONE_LOT2_1_DESIGN_SYSTEM_MINIMAL.md) | Référence enveloppe |
| [`cadrage/DECISIONS.md`](../cadrage/DECISIONS.md) | ADR-018, ADR-021 |
