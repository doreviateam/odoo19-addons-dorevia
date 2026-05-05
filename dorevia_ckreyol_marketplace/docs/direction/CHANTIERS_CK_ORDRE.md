# Mémo — Chantiers C-Kreyol à ordonner

## Objectif

Garder une vue claire des prochains chantiers C-Kreyol, dans le bon ordre, sans mélanger les sujets produit, UX, technique, e-commerce, contenus et prestataires tiers.

Principe de conduite :

> D’abord stabiliser le parcours d’achat et la confiance de base.  
> Ensuite enrichir l’expérience.  
> Enfin brancher les prestataires tiers et les mécaniques avancées.

---

## 1. Chantier en cours — MVP03 Compte client / demande pro

### Statut

En cours d’atterrissage.

### Contenu

- Création compte particulier B2C via standard Odoo.
- Page demande compte professionnel.
- Formulaire demande pro vers CRM.
- Flux secondaire “Être rappelé”.
- Aucun portail pro automatique.
- Aucune pricelist B2B automatique.

### À terminer

- Recette visuelle finale.
- Recette mobile.
- Recette CRM lead.
- Vérification redirection merci.
- Vérification absence de bascule portail / pricelist.
- Mise à jour PV recette.

### Décision

Clôturer proprement avant d’ouvrir un gros nouveau chantier.

---

## 2. Prochain chantier — Panier

**Cadrage MVP 04** (panier + favoris, lots et garde-fous) : [README MVP 04](../mvp_04/README.md).

### Objectif

Stabiliser l’expérience d’achat immédiate.

### Points à traiter

- Icône panier dans le header.
- Compteur panier.
- État panier vide.
- Lisibilité panier rempli.
- Accès panier depuis desktop / mobile.
- Cohérence checkout.
- Non-régression achat invité.
- Messages quantité / stock / disponibilité si nécessaires.

### Pourquoi avant les favoris

Le panier est le cœur de la conversion.  
Il doit être propre avant d’ajouter des intentions secondaires comme les favoris.

---

## 3. Chantier suivant — Favoris / Wishlist

Lot 2 du **MVP 04** — voir [README MVP 04](../mvp_04/README.md).

### Objectif

Permettre au visiteur de garder une sélection de produits.

### Points à cadrer

- Icône cœur sur fiche produit / carte produit.
- Ajout / retrait favoris.
- Accès à la liste des favoris.
- Comportement utilisateur connecté vs non connecté.
- Persistance des favoris.
- Lien éventuel avec compte client.
- UX mobile.

### Point de doctrine

Favoris ≠ panier.

- Panier : achat maintenant.
- Favoris : intention, sélection, retour plus tard.

---

## 4. Chantier navigation / mondes CK

### Statut

À mûrir.

### Éléments actuels

- Boutique.
- Collections.
- Communauté.
  - Idées cadeaux.
  - Recettes.
  - Blog.
- À propos / Contact.

### Points à clarifier plus tard

- “Idées cadeaux” reste-t-il éditorial ou devient-il une porte commerce ?
- “Recettes” est-il un contenu communautaire ou un moteur d’usage produit ?
- “Blog” doit-il être générique ou structuré en rubriques ?
- La nav mobile reste-t-elle lisible ?

### Décision actuelle

Ne pas figer trop tôt.  
Laisser vivre comme piste éditoriale / communauté.

---

## 5. Chantier contenus éditoriaux

### Objectif

Préparer l’univers CK au-delà de la boutique.

### Contenus possibles

- Idées cadeaux.
- Recettes.
- Articles producteurs.
- Guides d’usage produits.
- Histoires d’origine.
- Conseils de conservation / dégustation.

### Règle

Ne pas laisser l’éditorial ralentir le tunnel boutique.  
Le monde contenu doit enrichir CK, pas bloquer la mise en vente.

---

## 6. Chantier prestataires tiers e-commerce

### Statut

À inventorier, pas à brancher tout de suite.

### Familles à inventorier

- Avis clients :
  - Avis Vérifiés / Skeepers.
  - Trustpilot.
  - Google Customer Reviews.
  - modules Odoo avis produits.
- Paiement :
  - Stripe.
  - PayPal.
  - PSP CB.
- Livraison :
  - Colissimo.
  - Mondial Relay.
  - Chronopost.
  - Sendcloud / Boxtal.
- Emailing :
  - Odoo Email Marketing.
  - Brevo.
  - Mailchimp.
  - Resend.
- Support client :
  - formulaire contact.
  - WhatsApp Business.
  - chat / chatbot.
  - helpdesk.
- Analytics :
  - Matomo.
  - Google Analytics.
  - Search Console.
- Conformité :
  - cookies.
  - RGPD.
  - mentions légales.
  - CGV.

### Fiche d’analyse par prestataire

- Nom.
- Usage CK.
- Moment d’intégration recommandé.
- Coût.
- Données personnelles traitées.
- Dépendance externe.
- Intégration Odoo.
- Priorité : maintenant / plus tard / à éviter.

---

## 7. Chantier avis clients

### Statut

À traiter dans l’inventaire prestataires tiers.

### Intérêt

- Rassurance.
- Preuve sociale.
- Avis boutique.
- Avis produits.

### Point de vigilance

Ne pas brancher avant que le tunnel achat, les emails post-achat et la gestion client soient propres.

---

## 8. Chantier chatbot / assistant CK

### Statut

Piste MVP03+ / MVP04.

### Rôle possible

- Orienter les visiteurs.
- Répondre aux questions simples.
- Expliquer la demande compte pro.
- Diriger vers :
  - demande pro ;
  - être rappelé ;
  - compte particulier ;
  - contact.

### Garde-fous

Le chatbot ne doit pas :

- promettre les tarifs pro ;
- valider un compte pro ;
- négocier des conditions commerciales ;
- remplacer la validation humaine.

### Décision

Pas maintenant.  
À garder comme piste d’assistance future.

---

## 9. Chantier B2B réel / conditions professionnelles

### Statut

Hors MVP03.

### À traiter plus tard

- Validation métier des comptes pro.
- Catégories partenaires.
- Pricelists B2B.
- Affichage contextualisé des prix.
- Conditions de commande pro.
- Minimums de commande.
- Franco de port éventuel.
- Relation distributeur / revendeur.

### Règle

La demande pro MVP03 ne fait que capter l’intérêt.  
Le vrai B2B tarifaire est un chantier séparé.

---

## 10. Ordre recommandé des prochains chantiers

### Court terme

1. Clôturer MVP03 compte client / demande pro.
2. Panier.
3. Favoris.
4. Ajustements nav mobile / header si nécessaire.

### Moyen terme

5. Contenus Communauté : idées cadeaux, recettes, blog.
6. Inventaire prestataires tiers.
7. Avis clients.
8. Emailing / relance / newsletter plus avancée.

### Plus tard

9. Chatbot / assistant CK.
10. B2B tarifaire réel.
11. Automatisations marketing.
12. Analytics avancé.

---

## Décision de conduite

Ne pas tout ouvrir en même temps.

Priorité immédiate :

> Finaliser MVP03, puis sécuriser panier et favoris.

Ensuite seulement :

> Contenus, prestataires tiers, avis, chatbot, B2B avancé.
