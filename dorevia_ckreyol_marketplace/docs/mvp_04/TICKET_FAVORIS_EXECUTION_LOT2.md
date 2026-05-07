# TICKET — Exécution Lot 2 Favoris (MVP 04)

**ID** : `FAVORIS-EXEC-LOT2`  
**Statut** : **À arbitrer — non lancé**  
**Type** : Préparation d’arbitrage technique / futur chantier — **aucune implémentation ouverte par ce document**  
**Module** : `dorevia_ckreyol_marketplace` (+ dépendances à trancher : `website_sale`, évent. wishlist Odoo)

---

## Contexte et décision actuelle

Le **parcours Favoris** est **cadré produit / UX** dans [`2_FAVORIS_PARCOURS.md`](2_FAVORIS_PARCOURS.md). La doctrine dossier est inchangée :

**Lot 2 Favoris : cadré, exécution différée, non bloquant pour le GO technique minimal pré-ouverture.**

Ce fichier **formalise les arbitrages à trancher** avant tout développement. Il **ne déclenche pas** de code, de branche ni de sprint : il sert de **matrice de décision** pour une future phase d’implémentation, une fois le Lot 1 panier / checkout et les jalons pré-ouverture jugés suffisants.

**Références** : [README MVP 04](README.md), [doctrine Panier ≠ Favoris](README.md#doctrine), [hors périmètre implicite](README.md#hors-périmètre-implicite).

**Note technique (pré-arbitrage)** : [`NOTE_ARBITRAGE_TECHNIQUE_FAVORIS_LOT2.md`](NOTE_ARBITRAGE_TECHNIQUE_FAVORIS_LOT2.md) — recommandations, risques et périmètre MVP **proposés** pour l’atelier de décision ; ne remplace pas une **décision écrite** dans la section *Décision attendue avant exécution*.

---

## Objectif du ticket

Transformer le **cadrage** existant en **périmètre d’exécution arbitré** : pour chaque point ci-dessous, la colonne *Statut cible* indique si le point est **indispensable**, **optionnel**, **à arbitrer**, ou **hors MVP04** au sens du dossier — à **valider explicitement** avant développement.

**Légende**

| Libellé | Signification |
| --- | --- |
| **Indispensable** | Doit être livré dans le premier incrément Lot 2 si le Lot 2 est lancé. |
| **Optionnel** | Peut être reporté ou simplifié sans rompre le cadrage produit de base. |
| **À arbitrer** | Choix technique ou produit encore ouvert ; décision requise. |
| **Hors MVP04** | Exclu du périmètre MVP 04 (cf. README hors périmètre / doctrine). |

---

## 1. Stockage invité

| Option / question | Notes | Statut cible |
| --- | --- | --- |
| **Session** serveur (Odoo `website` / session visiteur) | Cohérent avec un état « panier-like » sans persistance longue durée. | À arbitrer |
| **localStorage / cookie** côté navigateur | Persistance navigateur ; pas de sync multi-appareils sans mécanisme serveur. | À arbitrer |
| **Mécanisme wishlist « standard » Odoo** (si module / API existante en 19) | Réutilisation vs sur-mesure CK ; dépend des modules installés. | À arbitrer |
| **Autre** (hybride, service dédié, etc.) | À documenter si retenu. | À arbitrer |
| **Persistance attendue ou non** pour l’invité (reprise après fermeture navigateur) | Le cadrage [`2_FAVORIS_PARCOURS.md`](2_FAVORIS_PARCOURS.md) (§4 *Connecté vs non connecté*) laisse l’arbitrage ouvert. | À arbitrer |

**Indispensable** : qu’**une** stratégie invité soit **choisie et documentée** avant implémentation (toutes les lignes ci-dessus restent des **options** jusqu’à arbitrage).

---

## 2. Stockage connecté

| Option / question | Notes | Statut cible |
| --- | --- | --- |
| **Rattachement compte** client / `res.partner` | Alignement portail / politique compte MVP03. | À arbitrer |
| **Usage wishlist standard Odoo** (si disponible et pertinent) | Évite le réinventer ; contraintes données / UX CK. | À arbitrer |
| **Comportement portail** (liste visible `/my`, menu, etc.) | Cohérence avec l’expérience « Mon compte » sans déborder MVP04. | Optionnel |

**Indispensable** : si persistance **connectée** retenue, définir **où** les données vivent (modèle, ACL, website).

---

## 3. Fusion invité → connecté

| Option | Notes | Statut cible |
| --- | --- | --- |
| **Fusion** des favoris invités dans le compte à la connexion | Expérience unifiée ; complexité technique. | À arbitrer |
| **Remplacement** (état invité abandonné) | Simple ; perte possible côté invité. | À arbitrer |
| **Conservation séparée** jusqu’à action utilisateur | Évite les surprises ; UX à clarifier. | À arbitrer |
| **Pas de promesse MVP** sur une fusion élaborée | Aligné cadrage [`2_FAVORIS_PARCOURS.md`](2_FAVORIS_PARCOURS.md) §4. | Indispensable (rappel) |

---

## 4. Points d’entrée

**Cœur minimal Lot 2** (hors arbitrage accessoire) : **listing `/shop`** + **fiche produit** + **liste Favoris** (page dédiée). Tout le reste ci-dessous est **complémentaire** ou **à trancher**.

| Point d’entrée | Notes | Statut cible |
| --- | --- | --- |
| **Listing `/shop`** | Carte produit sur la boutique — base du parcours. | Indispensable |
| **Fiche produit** | Alignée au cadrage §3. | Indispensable |
| **Carte produit — homepage** (blocs sélection / explorer, etc.) | Enrichissement ; **pas** le périmètre minimal. | Optionnel / à arbitrer |
| **Accès header** (lien « Favoris » / icône cohérente header V1) | Navigation vers la liste ; arbitrage sous **Décision attendue avant exécution**. | À arbitrer |
| **Compteur** favoris dans le header | Lisibilité vs charge ; pas imposé par le cadrage minimal. | Optionnel |

---

## 5. Liste Favoris

| Élément | Notes | Statut cible |
| --- | --- | --- |
| **Page dédiée** `/…` (URL à fixer) | Vue liste scannable (cadrage §5 *Liste des favoris*). | Indispensable |
| **Retrait favori** depuis la liste | Cadrage §3 / §5. | Indispensable |
| **Lien vers fiche produit** | Cadrage §5. | Indispensable |
| **Ajout au panier depuis la liste favoris** | Cadrage : **pas d’obligation** ; chemin panier **distinct**. Inclure un CTA panier = **optionnel**. | Optionnel |
| **Hors scope** : promesse marketing, partage, email | [README — Hors périmètre](README.md#hors-périmètre-implicite) | Hors MVP04 |

---

## 6. Recette minimale (reprise F1–F6)

Reprise des scénarios [§9 — `2_FAVORIS_PARCOURS.md`](2_FAVORIS_PARCOURS.md#9-scénarios-de-recette-minimaux).

| ID | Scénario | Contenu rappel | Statut cible |
| --- | --- | --- | --- |
| **F1** | Ajout **carte produit** (listing) | Clic cœur depuis listing ; état visuel immédiat. | Indispensable |
| **F2** | Ajout **fiche produit** | Même logique que la carte. | Indispensable |
| **F3** | **Retrait** | Suppression depuis la liste favoris ; disparition confirmée. | Indispensable |
| **F4** | **Persistance non connecté** | Conforme à l’**arbitrage** retenu pour l’invité (§1). | Indispensable *après* arbitrage §1 |
| **F5** | **Persistance connecté** | Conforme à l’**arbitrage** retenu pour le compte (§2). | Indispensable *si* persistance connectée retenue |
| **F6** | **Mobile** | Actions cœur + liste sans régression tactile. | Indispensable |

---

## Garde-fous (non négociables MVP04)

- Ne pas **confondre** favoris et panier ([doctrine](README.md#doctrine)).
- Pas d’**emailing automatique**, pas de **partage de liste**, pas de **marketing lourd** ([hors périmètre](README.md#hors-périmètre-implicite)).
- Pas de **compte forcé** sans décision d’arbitrage explicite ([cadrage §2](2_FAVORIS_PARCOURS.md#2-principes-directeurs)).
- Ne pas **retarder** une exécution Lot 1 / pré-ouverture en lançant du développement Favoris **sans** GO explicite sur ce ticket.

---

## Prochaines étapes (hors scope immédiat)

1. Atelier **arbitrage** : trancher les points listés en **Décision attendue avant exécution** (ci-dessous).
2. **GO / NO GO** lancement implémentation Lot 2 (après Lot 1 et jalons pré-ouverture).
3. Découpage technique (routes, modèles, tests) — **après** décision écrite.

---

## Décision attendue avant exécution

Sans **décision explicite** sur les éléments suivants, ce ticket reste **strictement préparatoire** et **ne mandate aucune implémentation** ni engagement de sprint.

Arbitrages à **trancher par écrit** avant tout code :

1. **Stockage invité** (stratégie retenue parmi §1).
2. **Stockage connecté** (modèle / rattachement `res.partner`, portail éventuel — §2).
3. **Fusion invité → connecté** (fusion, remplacement, séparation, ou absence de promesse — §3).
4. **URL et structure** de la **page liste Favoris** (chemins, gabarit, nom de route).
5. **Points d’entrée retenus** au-delà du **cœur minimal** (`/shop` + fiche produit + liste), y compris **Home** si applicable (optionnel).
6. **Accès header** : retenu ou non pour la V1 Lot 2 ; comportement du lien vers la liste.
7. **Compteur** favoris dans le header : retenu ou non.
8. **Scénarios F1–F6** effectivement **inclus dans le premier incrément** (tous ou sous-ensemble documenté).
9. **Dépendance** ou non à une **wishlist / mécanisme standard Odoo** (modules, API, contraintes installation).

---

*Document préparatoire — aucune implémentation engagée.*
