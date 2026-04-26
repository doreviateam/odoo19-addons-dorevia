# TICKET — Sélection produits Homepage MVP2.1 (`website_sale`)

**ID** : `SELECTION-PRODUITS-HOMEPAGE-MVP21`  
**Date d’ouverture** : 2026-04-24  
**Priorité** : **P1** (preuve d’offre réelle sur la homepage).  
**Statut** : **Clôturé** — **GO MOA (2026-04-24)** — [PV](PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md) ; feu vert chantier **4/5** — Inscription.  
**Exécution : clos** — voir [PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md](PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md) ; checklists §0 soldées (2026-04-25).  
**Module** : `dorevia_ckreyol_marketplace`  
**Périmètre** : **bloc Sélection produits** (`views/snippets/ckr_selection.xml` + résolution des enregistrements + SCSS si besoin).

**Décision MOA** : [DECISION_PRODUITS_HOMEPAGE_MVP21.md](../mvp_02/DECISION_PRODUITS_HOMEPAGE_MVP21.md).

**Rattachement** : [TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md](TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md) ; peut chevaucher **hero V2** / **Explorer MVP2** — coordonner `ckr_homepage.xml` et assets.

---

## Contexte

Décision MOA validée : **remplacer la sélection statique** par une **grille de 4 produits dynamiques** issus de **`website_sale`**.  
Voir [DECISION_PRODUITS_HOMEPAGE_MVP21.md](../mvp_02/DECISION_PRODUITS_HOMEPAGE_MVP21.md).  
Cadrage §3 : [1_HOMEPAGE.md](../mvp_02/1_HOMEPAGE.md).

**Décision MOA complémentaire (2026-04-24)** — Pilotage [README MVP 02](../mvp_02/README.md) : source des 4 produits = **sélection explicite** et **maintenable** côté BO (liste de produits ou paramétrage **snippet Website**). **Pas** de logique automatique **complexe** en MVP2.1.

---

## Objectif

Prouver dès la homepage que C-Kreyol est une **vraie boutique en ligne** avec des **produits réels**, **consultables** et **tarifés dynamiquement** (sans sur-promesse — [ADR-CKR-005](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)).

---

## Périmètre

### Structure cible

- **Grille de 4 produits** mis en avant (desktop ; **mobile** : grille responsive sobre — cf. maquette §0).

### Données par carte

| Élément | Détail |
|---------|--------|
| **Image** | Produit (Odoo / média publié) |
| **Label court** | Origine / type / badge — **homogène** sur les 4 cartes ou **masqué partout** si couverture données **inférieure à 80 %** ([PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md §9.4](PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md)) |
| **Nom** | Nom produit |
| **Prix** | **Dynamique** Odoo (pricelist / visiteur) |
| **CTA** | **Voir le produit** → fiche `website_sale` |

### Comportement

- **Clic carte** → **fiche produit** ;
- **Clic CTA** → **fiche produit** ;
- **Lien de section** vers le catalogue **`/shop`** : **optionnel**, distinct des cartes (pas de redirection forcée des **cartes** vers le listing seul).

---

## Contraintes

- Données issues de **`website_sale`** (catalogue publié) ;
- **Pas** de prix **hardcodé** ;
- **Pas** d’**ajout panier direct** sur la grille ; **pas** d’**AJAX** panier inline ;
- **Pas** de grille **8** produits (hors vague MVP2.1) ;
- **Pas** de surcharge « **marketplace** » générique.

---

## Technique (attendu)

- **Brancher** les produits sur la logique Odoo / `website_sale` (contrôleur ou mécanisme de résolution des 4 enregistrements — figé au §0 checklist) ;
- **Conserver** une structure **responsive** propre (tokens / composants CK existants) ;
- **Préserver** la cohérence **style CK** (SCSS du module) ;
- **Ne pas** impacter la **fiche produit standard** Odoo (hors snippet homepage sauf lien canonique).

---

## Hors périmètre

- **Ajout panier direct** ; **quick view** ; **filtre** produit sur la homepage ;
- **Carrousel** produit sur ce bloc ;
- **Refonte** globale de **`/shop`**.

---

## Critères d’acceptation

- [x] **4** produits **dynamiques** affichés (repli catalogue / emplacements BO — voir **PV**) ;
- [x] **Prix** affichés depuis Odoo (**aucun** prix statique en dur) ;
- [x] Chaque **carte** et le **CTA** mènent à la **bonne fiche produit** ;
- [x] **Desktop** et **mobile** validés MOA (réserves mineures **PV**) ;
- [x] Cohérence [ADR-CKR-005](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005) ; **copy** [PLATEFORME_MARQUE_CK_V1.md](PLATEFORME_MARQUE_CK_V1.md) ;
- [x] **Documentation / WIREFRAME** — alignés avec la livraison (cf. phase livraison + **PV**).

---

## Recette

- **PV** : [PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md](PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md) ;
- Phase A (historique) : [PV_RECETTE_PHASE_A_HOMEPAGE_CK.md](PV_RECETTE_PHASE_A_HOMEPAGE_CK.md) §6.4 si utile en complément.

---

## 0. Prêt pour dev — checklist pilotage *(soldée — clos 2026-04-24 / doc 2026-04-25)*

1. [x] **Branche** / intégration — livrée (module ≥ `19.0.1.9.2`).
2. [x] **Règle des 4 produits** — emplacements Site web + repli catalogue (**PV**).
3. [x] **Spec** — grille 4 cartes responsive (recette MOA).
4. [x] **Copy** — titre *Notre sélection du moment*, CTA fiche, **GO MOA** avec réserves mineures.
5. [x] **Label secondaire / origines** — règle §9.4 (cf. impl. + **PV**).
6. [x] **URLs** — fiches `website_sale`.
7. [x] **Accessibilité** — recette MOA.
8. [x] **WIREFRAME / doc** — alignés en phase livraison.
9. [x] **`__manifest__.py`** — bumps appliqués.
10. [x] **Recette** — [PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md](PV_RECETTE_SELECTION_PRODUITS_HOMEPAGE_MVP21_CK.md) **GO MOA**.
11. [x] **Instance / relecteur** — recette MOA complétée.

---

## Livrables techniques (synthèse)

| Livrable | Détail |
|----------|--------|
| **Python** | Résolution des 4 `product.template` (ou équivalent) publiés ; prix via logique boutique. |
| **QWeb** | Grille 4 cartes dynamiques ; CTA **Voir le produit** ; lien section `/shop` optionnel. |
| **SCSS** | Ajustements si nécessaire — cohérence CK. |

---

## Historique

| Date | Changement |
|------|------------|
| 2026-04-24 | Création — suite [DECISION_PRODUITS_HOMEPAGE_MVP21.md](../mvp_02/DECISION_PRODUITS_HOMEPAGE_MVP21.md). |
| 2026-04-24 | **Réécriture** — structure Contexte / Objectif / Périmètre (structure, données, comportement) ; contraintes ; technique ; hors périmètre ; critères ; recette ; checklist §0 conservée. |
| 2026-04-24 | **MOA** — sélection explicite BO / snippet Website ; pas de logique auto complexe ([README MVP 02](../mvp_02/README.md) pilotage). |
| 2026-04-24 | **Livraison code** `19.0.1.9.0` — 4 `Many2one` sur `website` (formulaire Site) ; `ckr_selection.xml` dynamique ; tests `dorevia_ckr_selection`. **Recette MOA / PV** : à compléter. |
| 2026-04-24 | **Clôture** — **GO MOA avec réserves mineures** (PV) ; version recette **≥ 19.0.1.9.7** ; itérations 9.3–9.7 (lecture home, tests, visuels). **Chantier suivant** : Inscription 4/5. |
| 2026-04-25 | **Documentation** — **Exécution : clos** explicite ; critères d’acceptation + checklist §0 **soldés** (homepage MVP2.1 close MOA). |
