# TICKET — Header & navigation CK — cible MVP04

**ID** : `HEADER-NAV-MVP04`  
**Date d'ouverture** : 2026-05  
**Priorité** : **P2** (à confirmer au pilotage)  
**Statut** : **Cadrage exécutable — retour dev attendu**  
**Module** : `dorevia_ckreyol_marketplace`

**Dossier lié** : `docs/mvp_04/` — panier & favoris  
**Références de conduite** : `docs/direction/CHANTIERS_CK_ORDRE.md`, `docs/direction/COMPATIBILITE_SNIPPETS_WEBSITE_CK.md`

---

## 1. Contexte

Avec l'arrivée progressive des fonctions e-commerce et relationnelles C-Kreyol (compte client, demande pro, panier, favoris, contenus, portes commerciales), le header doit évoluer vers une structure plus mature.

Ce ticket ne lance pas une refonte totale immédiate. Il pose une **cible** et demande un **retour technique / UX** pour cadrer ce qui est intégrable en MVP04 vs ce qui doit partir en chantier dédié.

Ce ticket est un cadrage transverse header/navigation ; il ne remplace pas les futurs tickets MVP04 dédiés au panier et aux favoris.

Cible de lecture :

```text
Top_0 — Barre flash info
Top_1 — Actions utiles client
Top_2 — Exploration boutique / contenus
```

---

## 2. Objectif du ticket

Produire un retour dev exploitable pour décider :

- ce qui peut être intégré dans MVP04 (minimum utile panier/favoris) ;
- ce qui relève d'un ticket header dédié ;
- les impacts QWeb / SCSS / responsive ;
- les risques de regression sur la navigation actuelle ;
- la cible mobile recommandée.

Ce ticket ne vaut **pas GO** pour une refonte complète tant que les arbitrages ne sont pas validés.

---

## 3. Cible fonctionnelle envisagee

### 3.1 Top_0 — Barre flash info

**Role** : afficher une information courte, utile et temporaire.

Exemples : livraison offerte, nouveautes, precommandes, information logistique, message saisonnier.

**Garde-fous** :

- une seule information a la fois ;
- texte court ;
- barre activable / desactivable rapidement ;
- hauteur contenue ;
- aucun impact negatif mobile ;
- pas de zone promotionnelle agressive permanente.

### 3.2 Top_1 — Header actions utiles

Structure cible desktop :

```text
Logo | Recherche | Aide / Contact | Creer un compte | Se connecter | Favoris | Panier
```

Hypothese mobile a instruire :

```text
Logo | Recherche | Compte | Favoris | Panier | Menu
```

**Fonctions attendues** :

| Element | Role |
|---------|------|
| Logo | Retour accueil. |
| Recherche | Acces rapide produits. |
| Aide / Contact | Reassurance et support. |
| Creer un compte | Entree parcours compte particulier B2C. |
| Se connecter | Login client. |
| Favoris | Selection personnelle / intention. |
| Panier | Achat immediat. |

### 3.3 Top_2 — Navigation exploration

Structure cible desktop :

```text
Tous les produits | Promotions | Collections | Idees cadeaux | Recettes | Professionnels
```

Lien professionnel cible :

```text
/demande-compte-professionnel
```

---

## 4. Lien avec MVP04 (panier / favoris)

MVP04 reste prioritairement :

1. **Panier** — achat immediat ;
2. **Favoris** — selection personnelle.

Le header doit au minimum clarifier :

- visibilite panier et favoris ;
- compteurs eventuels ;
- comportement desktop / mobile ;
- distinction panier vs favoris ;
- non-regression checkout ;
- non-regression compte client.

---

## 5. Perimetre demande au dev

### 5.1 Retour attendu

- faisabilite dans le header CK actuel ;
- impacts QWeb ;
- impacts SCSS ;
- impacts mobile / responsive ;
- dependances avec composants panier / favoris ;
- points risqués ;
- decoupage recommande entre MVP04 et ticket header dedie.

### 5.2 Questions a instruire

| Sujet | Question |
|-------|----------|
| Top_0 | Peut-on ajouter une barre flash info facilement desactivable ? |
| Recherche | Emplacement compatible avec le header actuel ? |
| Creer un compte / Se connecter | Distinction claire sans alourdir ? |
| Favoris | Visibilite / icone / compteur possibles ? |
| Panier | Visibilite / icone / compteur possibles ? |
| Top_2 | Nav secondaire possible sans casser l'existant ? |
| Mobile | Quelle version condensee recommander ? |
| Professionnels | Entree vers `/demande-compte-professionnel` sans ambiguite ? |

---

## 6. Criteres d'acceptation du retour dev

Le retour est accepte si les points suivants sont couverts :

- proposition de **decoupage en 2 paliers** :
  - **Palier A (MVP04)** : minimum utile pour lisibilite panier/favoris ;
  - **Palier B (chantier dedie)** : evolution large Top_0 / Top_2 et structure globale ;
- inventaire des fichiers potentiellement touches (QWeb / SCSS / JS) ;
- risques principaux et mitigation proposee ;
- proposition mobile explicite ;
- recommandation claire : integrer / reporter / ouvrir ticket dedie.

---

## 7. Criteres UX minimaux (mesurables)

- **Desktop** : panier et favoris visibles sans interaction hover pour les trouver.
- **Mobile** : actions critiques visibles sans surcharge ; pas d'empilement casse (pas de retour a la ligne non controle).
- **Clarte** : aucune ambiguite entre favoris (intention) et panier (achat immediat).
- **Acces compte** : connexion et creation compte restent identifiables.

---

## 8. Criteres techniques minimaux

- pas de regression sur le parcours checkout ;
- pas de regression sur le parcours compte client / demande pro ;
- pas de dependance JS bloquante nouvelle pour afficher la nav de base ;
- priorite aux mecanismes standards Odoo Website / QWeb quand suffisants ;
- pas d'ecart avec la doctrine catalogue et la sanctuarisation du tunnel.

---

## 9. Hors perimetre immediat

Sauf decision ulterieure :

- refonte complete du header ;
- refonte globale mobile ;
- moteur de recherche avance ;
- mega-menu catalogue ;
- personnalisation marketing avancee ;
- modifications checkout.

---

## 10. Decision attendue apres retour dev

```text
[ ] Integrer seulement les ajustements header necessaires a MVP04
[ ] Ouvrir un ticket header dedie (Palier B)
[ ] Reporter la refonte header apres MVP04
[ ] Limiter MVP04 au strict minimum de visibilite panier/favoris
```

---

## 11. Livrables attendus

| Livrable | Statut |
|----------|--------|
| Retour dev faisabilité QWeb / SCSS / mobile | À produire |
| Proposition de découpage Palier A / Palier B | À produire |
| Arbitrage MOA | A produire |
| Ticket exécution header dédié (si nécessaire) | À produire |

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-05 | Création du ticket de cadrage header / navigation CK en lien avec MVP04 panier & favoris. |
| 2026-05 | Renforcement du ticket : retour dev attendu, critères UX/tech mesurables, découpage Palier A / Palier B. |

