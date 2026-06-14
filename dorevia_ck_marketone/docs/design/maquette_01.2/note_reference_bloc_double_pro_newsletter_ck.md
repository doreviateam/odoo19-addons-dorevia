# Référence visuelle — Bloc double Pro / Newsletter · CK

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Type** | Inspiration complémentaire · maquette V1.2.x |
| **Référence source** | [`references/ref_bloc_double_pro_newsletter.png`](./references/ref_bloc_double_pro_newsletter.png) |
| **Artifact** | [`artifact/index.html`](./artifact/index.html) · [`contact.html`](./artifact/contact.html) · [`professionnels.html`](./artifact/professionnels.html) |
| **Arbitrage** | [`ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md`](./ARBITRAGE_V1_TRADUISIBLE_ODOO_CK_V1_2_X.md) §2 · §15 |
| **Date** | 2026-06-13 |
| **Statut** | **Recetté QA MOA — OK** · complément post-clôture maquette |

```text
Complément post-clôture maquette — n’ouvre pas de portail Pro ni d’espace connecté.
```

---

## 1. Intention CK

Deux lectures côte à côte, sans tunnel complexe :

| Colonne | Rôle | Ton CK |
|---------|------|--------|
| **Gauche — Pro** | Rendre visible la cible B2B · qualification simple | Premium · fiable · pas portail |
| **Droite — Newsletter** | Relation continue avec les visiteurs | Éditorial · sélection · pas promo agressive |

---

## 2. Copy CK retenue

### Bloc professionnel

**Titre** : Vous êtes professionnel ?

**Texte** : Épicerie, boutique créole, restaurant, hôtel, traiteur, distributeur… CK étudie votre demande et vous oriente vers une sélection adaptée.

**CTA** : Faire une demande professionnelle → `/professionnels`

### Bloc lettre d’information

**Titre** : Recevez les nouveautés créoles

**Texte** : Produits, recettes, producteurs, idées d’usage et sélections CK.

**CTA** : S’inscrire

**Note légère** : Sélections CK en cadence mesurée · désinscription à tout moment.

---

## 3. Ce que l’on reprend de la référence

* bloc Pro très visible · contraste fort ;
* CTA simple · une action par colonne ;
* double lecture B2B / relation continue ;
* pas de tunnel · pas d’espace connecté · pas de portail Pro.

## 4. Ce que l’on ne reprend pas (garde-fou MOA)

* ton promotionnel « surprise · bons plans · promos » ;
* promesses commerciales agressives ;
* esthétique discount.

CK garde une tonalité **premium, éditoriale et fiable**.

---

## 5. Emplacements maquette

| Page | Emplacement | Variante |
|------|-------------|----------|
| **Accueil** | Avant éditorial · remplace l’ancien bandeau `pro-home` | Pleine largeur · référence principale |
| **Contact** | Après réassurance · avant footer | Compact |
| **Professionnels** | Avant footer | Compact · CTA Pro → ancre formulaire |
| **Shop / footer** | Non matérialisé V1 maquette | Option footer pré-footer · à arbitrer Odoo |

---

## 6. Traduction Odoo pressentie

| Colonne | Odoo | Classe | Complexité |
|---------|------|--------|------------|
| Pro | Page CMS + lien · snippet `s_ck_pro_banner` ou bloc custom 2 col | V1 prioritaire (Pro) | Faible |
| Newsletter | Mass mailing / `website_mass_mailing` · snippet subscribe | V1 possible | Moyenne |

**Snippet CK cible pressenti** : `s_ck_dual_engage` (2 colonnes Pro + newsletter) — à créer thème si retenu V1.

**Réserve** : newsletter = consentement RGPD · double opt-in · pas de mock en prod.

---

## 7. Classes d’arbitrage

| Élément | Classe |
|---------|--------|
| Bloc Pro (colonne gauche) | V1 prioritaire |
| Bloc newsletter (colonne droite) | V1 possible |
| Snippet dual 2 col unifié | V1 possible |
| Newsletter sur toutes pages footer | V1 différée |

---

## 8. Point MOA ajouté (M9)

| # | Point | Options |
|---|-------|---------|
| **M9** | Newsletter V1 | Intégrer accueil · accueil+contact · différer · mass mailing natif Odoo |

Ajouté dans [`decision_moa_go_reprise_odoo_v1.md`](./decision_moa_go_reprise_odoo_v1.md) pour arbitrage avant GO Odoo.

---

## 9. Recette QA complément (2026-06-13)

| Contrôle | Résultat |
|----------|----------|
| Pages | Accueil · Contact · Professionnels |
| Desktop 1280 px · mobile 390 px | OK — pas d’overflow |
| Ton CK | OK — pas de « promo / surprise / bons plans » |
| Newsletter mock | OK — `onsubmit="return false"` |
| CTA Pro Professionnels | OK — `#ck-pro-form` (formulaire CRM mock) |

**Verdict QA** : OK avec correction CTA appliquée.

---

*Référence bloc double Pro / Newsletter CK · complément maquette V1.2.x · 2026-06-13.*
