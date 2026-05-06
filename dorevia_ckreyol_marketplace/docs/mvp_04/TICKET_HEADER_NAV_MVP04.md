# TICKET — Header & navigation CK — V1 MVP04

**ID** : `HEADER-NAV-MVP04`  
**Date d’ouverture** : 2026-05  
**Priorité** : **P2**  
**Statut** : **Header CK V1 implémenté et figé (baseline avant suite MVP04)**  
**Module** : `dorevia_ckreyol_marketplace`

**Dossier lié** : `docs/mvp_04/` — panier & favoris  
**Références de conduite** : `docs/direction/CHANTIERS_CK_ORDRE.md`, `docs/direction/COMPATIBILITE_SNIPPETS_WEBSITE_CK.md`

---

## 1. Posture actée

MVP04 passe d’un **Palier A minimal** à une **première refonte Header CK V1 assumée**, basée sur :

```text
Top_0 — Barre flash info
Top_1 — Actions utiles client
Top_2 — Exploration boutique / contenus
```

La V1 est livrée par **lots courts** pour garder la maîtrise et limiter les régressions.

---

## 2. Périmètre V1

La V1 couvre **desktop + mobile complets**, sans chercher une version définitive complexe.

Attendu V1 :

- version desktop propre ;
- version mobile propre ;
- hiérarchie lisible ;
- pas de régression checkout / compte / demande pro ;
- pas de surcharge mobile.

---

## 3. Cible fonctionnelle V1

### 3.1 Top_0 — Flash info

- barre fine ;
- texte court ;
- une seule information visible à la fois ;
- désactivable ou facilement neutralisable si possible.

Calibrage retenu :

- rotateur sobre (pas d’effet ticker) ;
- cycle 32s ;
- typo mobile 0.76rem ;
- couleur texte terracotta validée.

Exemple :

```text
Livraison offerte dès X € d’achat en France métropolitaine.
```

### 3.2 Top_1 — Actions utiles

- logo ;
- recherche discrète ;
- aide / contact ;
- compte / connexion ;
- favoris ;
- panier avec compteur.

Garde-fou recherche :

- pas de recherche massive ;
- pas de barre dominante ;
- icône ou champ court uniquement.

Note produit (future recherche globale) :

- le champ de recherche header est conservé comme entrée de recherche globale future ;
- ne pas figer le wording sur "Rechercher un produit" ;
- cible à terme : produits, collections, promotions, idées cadeaux, recettes, articles/blog, contenus Communauté.

Finition créa retenue :

- champ visuel desktop légèrement arrondi ;
- contour terracotta sobre ;
- icône loupe en terracotta ;
- libellé aide harmonisé : `Aide & Contact`.
- doctrine logotype marque/web : voir [PISTE_CREA_LOGOTYPE_CKREYOL.md](PISTE_CREA_LOGOTYPE_CKREYOL.md).

### 3.3 Top_2 — Exploration

- Tous les produits ;
- Promotions ;
- Collections ;
- Idées cadeaux ;
- Recettes ;
- Professionnels.

Lien `Professionnels` :

```text
/demande-compte-professionnel
```

---

## 4. Hors V1

Restent hors V1 :

- méga-menu ;
- recherche avancée ;
- autocomplete recherche ;
- animations lourdes ;
- personnalisation marketing ;
- administration avancée de la barre flash ;
- logique snippet complète ;
- refonte checkout ;
- refonte des pages de destination ;
- navigation éditoriale profonde ;
- règles complexes de compte / B2B.

---

## 5. Priorité de livraison (lots)

### Lot V1.1 — Structure desktop

- Top_0 ;
- Top_1 ;
- Top_2 ;
- panier / favoris / professionnels visibles ;
- recherche discrète ;
- aucune logique avancée.

### Lot V1.2 — Mobile

- condensation mobile ;
- accès panier ;
- accès favoris ;
- menu mobile propre ;
- `Professionnels` dans le menu.

### Lot V1.3 — Finitions / recette

- ajustements SCSS ;
- compteurs ;
- responsive ;
- vérification checkout / compte / demande pro ;
- PV recette.

---

## 6. Garde-fous

- Ne pas dégrader `checkout`, `compte client`, `demande-compte-professionnel`.
- Ne pas surcharger mobile.
- Ne pas confondre :

```text
Panier = achat immédiat
Favoris = intention / sélection
Professionnels = demande d’ouverture de compte pro
```

---

## 7. Décision de pilotage

```text
Header CK V1 = Top_0 / Top_1 / Top_2
Livraison = V1.1 (desktop) + V1.2 (mobile) + V1.3 (finitions/recette)
```

Phrase de conduite :

> On ne bricole plus le header par petites touches.  
> On pose une Header CK V1 claire, sobre, e-commerce, en 3 niveaux, livrée par lots pour garder la maîtrise.

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-05 | Création du ticket de cadrage header / navigation CK en lien avec MVP04 panier & favoris. |
| 2026-05 | Passage en posture **Header CK V1** : refonte structurante en trois niveaux, livrée en lots V1.1 / V1.2 / V1.3. |
| 2026-05 | Gel de la baseline livrée : Top_0 rotateur sobre, Top_1 recherche visuelle discrète, wording recherche globale future, ajustements créa desktop validés. |
| 2026-05 | Ajout d'une piste créa dédiée logotype (`C-Kréyòl` affiché / `C-Kreyol` technique) pour préparation d'une intégration header définitive. |

