# TICKET — Header & navigation CK — cible MVP04

**ID** : `HEADER-NAV-MVP04`  
**Date d’ouverture** : 2026-05  
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
- les risques de régression sur la navigation actuelle ;
- la cible mobile recommandée.

Ce ticket ne vaut **pas GO** pour une refonte complète tant que les arbitrages ne sont pas validés.

---

## 3. Cible fonctionnelle envisagée

### 3.1 Top_0 — Barre flash info

**Rôle** : afficher une information courte, utile et temporaire.

Exemples : livraison offerte, nouveautés, précommandes, information logistique, message saisonnier.

**Garde-fous** :

- une seule information à la fois ;
- texte court ;
- barre activable / désactivable rapidement ;
- hauteur contenue ;
- aucun impact négatif mobile ;
- pas de zone promotionnelle agressive permanente.

### 3.2 Top_1 — Header actions utiles

Structure cible desktop :

```text
Logo | Recherche | Aide / Contact | Créer un compte | Se connecter | Favoris | Panier
```

Hypothèse mobile à instruire :

```text
Logo | Recherche | Compte | Favoris | Panier | Menu
```

**Fonctions attendues** :

| Élément | Rôle |
|---------|------|
| Logo | Retour accueil. |
| Recherche | Accès rapide produits. |
| Aide / Contact | Réassurance et support. |
| Créer un compte | Entrée parcours compte particulier B2C. |
| Se connecter | Login client. |
| Favoris | Sélection personnelle / intention. |
| Panier | Achat immédiat. |

### 3.3 Top_2 — Navigation exploration

Structure cible desktop :

```text
Tous les produits | Promotions | Collections | Idées cadeaux | Recettes | Professionnels
```

Lien professionnel cible :

```text
/demande-compte-professionnel
```

---

## 4. Lien avec MVP04 (panier / favoris)

MVP04 reste prioritairement :

1. **Panier** — achat immédiat ;
2. **Favoris** — sélection personnelle.

Le header doit au minimum clarifier :

- visibilité panier et favoris ;
- compteurs éventuels ;
- comportement desktop / mobile ;
- distinction panier vs favoris ;
- non-régression checkout ;
- non-régression compte client.

---

## 5. Périmètre demandé au dev

### 5.1 Retour attendu

- faisabilité dans le header CK actuel ;
- impacts QWeb ;
- impacts SCSS ;
- impacts mobile / responsive ;
- dépendances avec composants panier / favoris ;
- points risqués ;
- découpage recommandé entre MVP04 et ticket header dédié.

### 5.2 Questions à instruire

| Sujet | Question |
|-------|----------|
| Top_0 | Peut-on ajouter une barre flash info facilement désactivable ? |
| Recherche | Emplacement compatible avec le header actuel ? |
| Créer un compte / Se connecter | Distinction claire sans alourdir ? |
| Favoris | Visibilité / icône / compteur possibles ? |
| Panier | Visibilité / icône / compteur possibles ? |
| Top_2 | Nav secondaire possible sans casser l'existant ? |
| Mobile | Quelle version condensée recommander ? |
| Professionnels | Entrée vers `/demande-compte-professionnel` sans ambiguïté ? |

---

## 6. Critères d'acceptation du retour dev

Le retour est accepté si les points suivants sont couverts :

- proposition de **découpage en 2 paliers** :
  - **Palier A (MVP04)** : minimum utile pour lisibilité panier/favoris ;
  - **Palier B (chantier dédié)** : évolution large Top_0 / Top_2 et structure globale ;
- inventaire des fichiers potentiellement touchés (QWeb / SCSS / JS) ;
- risques principaux et mitigation proposée ;
- proposition mobile explicite ;
- recommandation claire : intégrer / reporter / ouvrir ticket dédié.

---

## 7. Critères UX minimaux (mesurables)

- **Desktop** : panier et favoris visibles sans interaction hover pour les trouver.
- **Mobile** : actions critiques visibles sans surcharge ; pas d'empilement cassé (pas de retour à la ligne non contrôlé).
- **Clarté** : aucune ambiguïté entre favoris (intention) et panier (achat immédiat).
- **Accès compte** : connexion et création compte restent identifiables.

---

## 8. Critères techniques minimaux

- pas de régression sur le parcours checkout ;
- pas de régression sur le parcours compte client / demande pro ;
- pas de dépendance JS bloquante nouvelle pour afficher la nav de base ;
- priorité aux mécanismes standards Odoo Website / QWeb quand suffisants ;
- pas d'écart avec la doctrine catalogue et la sanctuarisation du tunnel.

---

## 9. Hors périmètre immédiat

Sauf décision ultérieure :

- refonte complète du header ;
- refonte globale mobile ;
- moteur de recherche avancé ;
- méga-menu catalogue ;
- personnalisation marketing avancée ;
- modifications checkout.

---

## 10. Décision attendue après retour dev

```text
[ ] Intégrer seulement les ajustements header nécessaires à MVP04
[ ] Ouvrir un ticket header dédié (Palier B)
[ ] Reporter la refonte header après MVP04
[ ] Limiter MVP04 au strict minimum de visibilité panier/favoris
```

---

## 11. Livrables attendus

| Livrable | Statut |
|----------|--------|
| Retour dev faisabilité QWeb / SCSS / mobile | À produire |
| Proposition de découpage Palier A / Palier B | À produire |
| Arbitrage MOA | À produire |
| Ticket exécution header dédié (si nécessaire) | À produire |

---

## 12. Retour dev — découpage Palier A / Palier B

### Découpage recommandé

#### Palier A — MVP04, minimal et nécessaire

À intégrer dans MVP04 uniquement si cela reste ciblé et sans refonte globale :

- rendre **Panier** et **Favoris** clairement visibles dans le header, desktop + mobile ;
- ajouter un **compteur panier** ;
- ajouter un **compteur favoris** si faisable sans complexité ;
- garantir la séparation claire :
  - **Panier** = achat immédiat ;
  - **Favoris** = intention / sélection ;
- ajouter ou valider l’entrée **Professionnels** vers `/demande-compte-professionnel` sans ambiguïté ;
- maintenir zéro régression sur :
  - checkout ;
  - compte client ;
  - demande pro ;
  - navigation mobile.

#### Palier B — chantier header dédié, hors MVP04

À reporter dans un ticket dédié :

- structuration complète **Top_0 / Top_1 / Top_2** ;
- barre flash info administrable (**Top_0**) ;
- navigation secondaire élargie (**Top_2**) :
  - Promotions ;
  - Collections ;
  - Idées cadeaux ;
  - Recettes ;
  - Communauté ;
  - Professionnels ;
- rationalisation UX / SCSS globale desktop et mobile ;
- préparation éventuelle Website Builder / snippets lorsque les blocs seront stabilisés.

### Justification

Le **Palier A** sécurise la conversion et l’usage immédiat MVP04 : panier, favoris, accès professionnels.

Le **Palier B** évite de transformer MVP04 en refonte complète de navigation.

Cette séparation limite le risque principal : régression header / mobile / checkout.

### Décision de pilotage

Retenir le découpage suivant :

```text
MVP04 = Palier A
Header dédié futur = Palier B
```

### Conséquence pour MVP04

Les prochains tickets MVP04 doivent se concentrer sur :

1. **Panier visible et fiable** ;
2. **Favoris visibles et compréhensibles** ;
3. **Entrée Professionnels validée** ;
4. **zéro régression checkout / compte / mobile**.

La refonte complète Top_0 / Top_1 / Top_2 est reportée.

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-05 | Création du ticket de cadrage header / navigation CK en lien avec MVP04 panier & favoris. |
| 2026-05 | Renforcement du ticket : retour dev attendu, critères UX/tech mesurables, découpage Palier A / Palier B. |
| 2026-05 | Décision de pilotage actée : MVP04 = Palier A ; refonte header dédiée future = Palier B. |

