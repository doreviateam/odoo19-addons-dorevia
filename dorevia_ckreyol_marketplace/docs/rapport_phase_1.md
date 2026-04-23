# Rapport de phase — Canal e-commerce C-Kreyol (front Odoo 19)

**Document** : bilan d’intervention à destination de la MOA  
**Module** : `dorevia_ckreyol_marketplace`  
**Version de référence (clôture phase)** : `19.0.1.0.23`  
**Date de rédaction** : 20 avril 2026  
**Environnement cible** : Odoo 19 Community Edition, site web e-commerce.

---

## 1. Objet et périmètre de la phase

La phase couverte par ce rapport regroupe les travaux de **mise en cohérence front-end du canal e-commerce C-Kreyol**, dans une logique **sobre, native Odoo et maintenable** : héritages QWeb ciblés, styles SCSS alignés sur la charte graphique Phase 1 (tokens terracotta / neutres, typographie Playfair Display + Inter), sans duplication de logique métier ni de parcours e-commerce parallèle.

Le périmètre fonctionnel traité s’étend du **socle d’identification et de navigation** (connexion, header) au **cœur du parcours d’achat** (boutique `/shop`, fiche produit), avec des **garde-fous** respectés là où Odoo conditionne l’affichage (langues, listes de prix).

---

## 2. Principes directeurs respectés

- **Standard Odoo d’abord** : réemploi des mécanismes natifs (sélecteur de langue, pricelists, templates `website_sale`, `portal`, etc.).
- **Sur-mesure limité** : intégration dans le layout C-Kreyol et habillage SCSS sous scopes dédiés (`ckr-*`), pas de refonte structurelle des pages e-commerce en V1.
- **Séparation technique / métier** : pas d’injection automatique de données catalogue ; configuration langues, devises et contenus produits du côté exploitation / MOA (documentée).
- **Accessibilité et lisibilité** : états focus, contrastes et composants (menus, formulaires) traités dans la continuité de la charte.

---

## 3. Livrables réalisés (synthèse)

| Domaine | Réalisation | Notes |
|---------|-------------|--------|
| **Page de connexion** `/web/login` | Personnalisation du formulaire (titre « Mon compte », libellés orientés client, masquage d’éléments techniques superflus, CTA et champs alignés charte) | Validée côté MOA |
| **Header site** | Header personnalisé (logo, menu Option B, utilitaires). Menu compte : solution native-friendly (`<details>` + styles), déconnexion et accès `/my`. Correction des conflits CSS (chevauchement, troncature) | Validée |
| **Langues et devises** | Activation des variantes natives **inline + codes** pour le sélecteur de langue ; réinjection des `t_call` natifs (langue + `pricelist_list`) dans le header et le drawer mobile ; fichier `data/website_selectors_activation.xml` | Cible V1 : FR / EN / ES et EUR / GBP selon configuration réelle ; **pas de `post_init_hook`** — voir doc exploitation |
| **Documentation exploitation** | `docs/EXPLOITATION_I18N_DEVISES.md` | Checklist back-office (langues publiées, pricelists, traductions, e-mails) |
| **Portail client** `/my` | Scope et styles d’ensemble (titres, cartes, colonne profil) | Améliorations ultérieures possibles hors périmètre de cette clôture |
| **Fiche produit** `/shop/product/...` | Scope `ckr-product` + fichier `layout/_product.scss` (breadcrumb, titre, prix, variantes, CTA, quantité, accordéons, galerie, alternatives, mentions légales courtes). Finitions : favori, respiration colonne droite, bloc sous CTA ; **ruban produit** harmonisé charte (surcharge des couleurs inline Odoo) | **V1 fiche produit validée** |
| **Boutique** `/shop` | Scope `ckr-shop` + fichier `layout/_shop.scss` (en-tête, barre d’outils, sidebar filtres, tuiles, rubans, pagination, offcanvas) | Cohérence visuelle avec la fiche produit |
| **Stabilité front** | Corrections liées à la compilation Sass (`clamp` / unités), régressions UI corrigées au fil des retours | — |

**Fichiers principaux concernés** (indicatif) :

- Vues : `views/layout/ckr_header.xml`, `views/auth/ckr_login.xml`, `views/portal/ckr_portal.xml`, `views/pages/ckr_product.xml`, `views/pages/ckr_shop.xml`, `data/website_selectors_activation.xml`
- Styles : `static/src/scss/layout/_header.scss`, `_locale.scss`, `_login.scss`, `_portal.scss`, `_product.scss`, `_shop.scss`, tokens et `ckr_main.scss`
- Script : `static/src/js/ckr_header_drawer.js` (drawer + menu compte)

---

## 4. État de validation (MOA / recette)

Les écrans suivants ont fait l’objet d’**validation de principe** ou de **retours itératifs** jusqu’à une version jugée acceptable pour clôturer la phase sur le plan **structure et habillage V1** :

- Connexion « Mon compte »
- Header (compte, langue / devise lorsque configuré, mobile)
- Fiche produit (y compris ruban et finitions UI listées ci-dessus)
- Liste boutique `/shop`

Les **contenus produits** (textes, visuels, richesse éditoriale) restent la **responsabilité métier** et le principal levier qualité perçue ; ils ne sont pas portés par ce module.

---

## 5. Prérequis et exploitation

- **Mise à jour du module** : `odoo -u dorevia_ckreyol_marketplace` sur l’instance concernée après déploiement des sources.
- **Cache navigateur** : en cas d’anomalie d’affichage après mise à jour, prévoir un rechargement forcé (assets frontend régénérés).
- **Internationalisation** : suivre `docs/EXPLOITATION_I18N_DEVISES.md` avant d’exposer plusieurs langues ou devises en production.
- **Jeux de données** : aucun produit de démonstration n’est injecté par le module ; les tests s’appuient sur les données publiées dans Odoo.

---

## 6. Suite recommandée (prochaine phase)

**Suite doctrine homepage / portes catalogue** : **[ADR-006 à 008](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-006)**, **[WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md)** (Bloc 3 Explorer), **[STRUCTURE_MENU_PRINCIPAL.md](STRUCTURE_MENU_PRINCIPAL.md)** §11.

Ordre validé avec la MOA pour la **poursuite du parcours e-commerce** :

1. **Panier** `/shop/cart` — en particulier harmonisation du **CTA principal** (ex. « Payer ») avec la charte terracotta, actuellement encore proche du violet Bootstrap sur certaines captures.
2. **Tunnel de checkout** (adresse, paiement, confirmation), même méthode : natif Odoo, scope SCSS, V1 sobre.
3. Poursuite éventuelle du **contenu produit** et du **polish transversal** (backlog Phase 1bis documenté séparément).

---

## 7. Synthèse exécutive (une phrase)

*La phase a livré une base front C-Kreyol cohérente et maintenable sur la connexion, le header, la boutique, la fiche produit et les mécanismes natifs langue / devise ; la suite logique est le panier puis le checkout, avec priorité à l’alignement visuel du parcours de conversion.*

---

*Fin du rapport — pour toute précision technique, se référer au dépôt du module et au `README.md` associé.*
