# Vision média-commerce C-Kreyol

**Projet :** C-Kreyol  
**Statut :** Vision fondatrice figée  
**Objet :** Cadrer l’architecture produit, éditoriale, communautaire et économique de C-Kreyol  
**Portée :** Ce document oriente les décisions **UX**, **éditoriales**, **communautaires**, **publicitaires** et **e-commerce**. Il **structure** ces arbitrages sur le **long terme** sans **élargir** le périmètre de **livraison immédiate** du MVP ni des phases opérationnelles déjà cadrées ([note de cadrage](NOTE_DE_CADRAGE.md)).

**Pilotage :** [ADR-CKR-009](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-009). **E-commerce** B2C / B2B (détail du **monde** e-commerce) : [DOCTRINE_CK_ECOMMERCE_B2C_B2B.md](DOCTRINE_CK_ECOMMERCE_B2C_B2B.md), [ADR-CKR-010](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-010). **Langues créoles** (doctrine **culturelle**, qualité / variantes / gouvernance — **sans** mandat MVP) : [DOCTRINE_CK_LANGUES_CREOLES.md](DOCTRINE_CK_LANGUES_CREOLES.md), [ADR-CKR-011](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-011) ; **technique** FR / EN / ES (Phase 1bis) : [EXPLOITATION_I18N_DEVISES.md](EXPLOITATION_I18N_DEVISES.md). Le cadrage opérationnel Phase 1 reste la [note de cadrage](NOTE_DE_CADRAGE.md) ; le présent texte en précise la **vision long terme** et les **garde-fous** (dont publicité / monétisation).

---

## 1. Vision fondatrice

C-Kreyol est une plateforme **média-commerce créole**, pensée pour l’Europe francophone.

Elle articule trois mondes complémentaires :

1. **Un monde e-commerce**  
   Dédié à la vente de produits créoles sélectionnés, auprès des particuliers et des professionnels.

2. **Un monde éditorial**  
   Dédié aux récits, recettes, origines, producteurs, usages, territoires et cultures créoles.

3. **Un monde communautaire**  
   Dédié aux échanges, recommandations, témoignages et liens entre consommateurs, producteurs, diaspora, curieux et passionnés de l’univers créole.

C-Kreyol n’est donc pas uniquement une boutique en ligne. C’est une destination créole structurée autour de la découverte, de la confiance, de l’achat et de l’appartenance.

---

## 2. Doctrine générale

Le e-commerce vend les produits.  
L’éditorial crée le désir.  
La communauté crée la confiance.  
La régie publicitaire finance l’audience sans dégrader l’expérience marchande.

Cette doctrine doit guider toutes les décisions futures : design, navigation, contenus, partenariats, développement fonctionnel, monétisation et priorisation.

---

## 3. Les trois mondes de C-Kreyol

### 3.1 Monde e-commerce

Le monde e-commerce constitue le cœur marchand de C-Kreyol.

Il est **non monolithique** sur le plan commercial : **deux publics** coexistent sur un **catalogue commun** — **B2C** (particuliers, **prix public conseillé**) et **B2B** (professionnels / distributeurs, **prix partenaire distributeur**). L’**affichage** (prix visibles, remises, conditions de commande) est **contextualisé** selon le **statut** du visiteur, son **compte** et les **listes de prix** Odoo (**doctrine §2.1**). Doctrine détaillée : **[DOCTRINE_CK_ECOMMERCE_B2C_B2B.md](DOCTRINE_CK_ECOMMERCE_B2C_B2B.md)** ; **[ADR-CKR-010](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-010)**.

Il comprend notamment :

- le catalogue produits ;
- les pages catégories ;
- les pages produits ;
- les sélections commerciales ;
- le panier ;
- le tunnel de commande ;
- le compte client ;
- les commandes B2C ;
- les commandes B2B ;
- les promotions ;
- les packs / kits ;
- les recommandations produits internes.

Son modèle économique repose sur :

- la marge commerciale ;
- le volume de vente ;
- le panier moyen ;
- le réachat ;
- la vente aux professionnels ;
- la qualité de la sélection.

Le monde e-commerce doit être protégé au maximum contre toute pollution publicitaire.

### 3.2 Monde éditorial

Le monde éditorial donne du sens aux produits et à l’univers C-Kreyol.

Il peut comprendre notamment :

- des articles ;
- des recettes ;
- des guides d’achat ;
- des dossiers thématiques ;
- des portraits de producteurs ;
- des contenus sur les origines ;
- des contenus culturels ;
- des sélections saisonnières ;
- des contenus autour des usages, traditions et moments de consommation.

Son rôle est de créer le désir, d’éduquer, d’inspirer et d’installer C-Kreyol comme une référence sobre, crédible et chaleureuse autour des produits et cultures créoles.

Le monde éditorial est l’espace naturel de la régie publicitaire, à condition que celle-ci reste sélective, contextualisée, identifiable et maîtrisée.

### 3.3 Monde communautaire

Le monde communautaire crée du lien et de la confiance.

Il peut comprendre notamment :

- des avis ;
- des témoignages ;
- des recommandations ;
- des questions / réponses ;
- des échanges autour des produits ;
- des partages de recettes ;
- des retours d’expérience ;
- des événements ;
- des espaces de discussion encadrés ;
- des mises en relation entre consommateurs, producteurs et passionnés.

Son rôle est de renforcer l’attachement à C-Kreyol et de transformer la plateforme en lieu vivant, et pas seulement en vitrine marchande.

Le monde communautaire peut accueillir des partenaires, mais uniquement de manière encadrée, cohérente et modérée.

### 3.4 Langues créoles dans l’expérience

C-Kreyol a vocation à accueillir **progressivement** les **langues créoles** dans l’expérience utilisateur — **comme** une dimension **culturelle** et **éditoriale**, **pas** comme une simple bascule d’interface.

La doctrine porte sur la **qualité** (traduction humaine qualifiée, relecture, pas de « créole générique »), la **clarté de la variante** proposée et la **protection** du parcours marchand (prix, conditions, obligations — **référence contractuelle** conforme à la doctrine dédiée).

Texte normatif : **[DOCTRINE_CK_LANGUES_CREOLES.md](DOCTRINE_CK_LANGUES_CREOLES.md)** ; **[ADR-CKR-011](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-011)**. L’**activation** des langues **FR / EN / ES** et des sélecteurs Odoo relève de **[EXPLOITATION_I18N_DEVISES.md](EXPLOITATION_I18N_DEVISES.md)** — couche **distincte** (exploitation technique **Phase 1bis**).

---

## 4. Principe économique

Le modèle économique de C-Kreyol repose sur une séparation claire des logiques de financement.

| Monde | Rôle principal | Modèle économique | Niveau de protection |
|---|---|---|---|
| E-commerce | Vendre | Marge, volume, B2B, réachat | Protection maximale |
| Éditorial | Raconter, inspirer, expliquer | Sponsoring, régie, dossiers partenaires | Publicité possible mais maîtrisée |
| Communautaire | Créer du lien et de la confiance | Partenariats, régie ciblée, animation | Publicité très encadrée |

Le monde e-commerce finance sa croissance par la vente aux particuliers et aux professionnels.

Les mondes éditorial et communautaire peuvent être financés par une régie publicitaire sélective, contextualisée et maîtrisée.

La **montée en charge** de cette régie suit la **trajectoire progressive** décrite en **§5.1** (automatisation cloisonnée, puis régie directe et partenaires à maturité), **sans jamais** ouvrir le sanctuaire e-commerce à la publicité agressive.

---

## 5. Doctrine publicitaire

La publicité peut contribuer au financement de C-Kreyol, mais elle ne doit jamais dégrader :

- l’acte d’achat ;
- la confiance produit ;
- la perception de qualité ;
- la lisibilité de l’offre ;
- la sobriété de l’expérience ;
- la relation entre C-Kreyol et ses clients.

La régie publicitaire doit être pensée comme une régie sélective, au service de l’écosystème créole, et non comme une monétisation agressive de l’audience.

C-Kreyol garde le contrôle éditorial, visuel et commercial de toutes les insertions publicitaires.

### 5.1 Trajectoire progressive de la monétisation publicitaire

La monétisation publicitaire CK suit une **trajectoire progressive** :

1. **Phase initiale** — une **régie automatisée**, **strictement cloisonnée** aux **espaces éditoriaux** et **communautaires** (hors sanctuaire e-commerce, cf. §6).
2. **Phase de maturité** — une **régie directe**, **qualitative** et **sélective**, fondée sur l’**édification de partenaires** cohérents avec l’univers créole.

En synthèse :

- l’**automatisation** finance l’**audience** au **démarrage** ;
- l’**édification partenaire** construit la **valeur de l’écosystème** à **maturité** ;
- l’**e-commerce** reste **sanctuarisé** dans les **deux** cas (même règle non négociable que §6.1 et §14).

---

## 6. Règles de protection du e-commerce

### 6.1 Zones interdites à la publicité agressive

Les zones suivantes doivent rester protégées :

- fiche produit ;
- panier ;
- tunnel de commande ;
- compte client ;
- recherche produit ;
- listing boutique principal ;
- pages de paiement ;
- pages de confirmation de commande ;
- espaces liés au SAV et au suivi de commande.

Dans ces zones, aucune publicité externe agressive, automatique ou non maîtrisée ne doit être affichée.

### 6.2 Ce qui reste acceptable

Dans le monde e-commerce, peuvent être acceptées uniquement des mises en avant internes ou fortement maîtrisées, par exemple :

- sélection C-Kreyol ;
- producteur du mois ;
- offre partenaire validée par C-Kreyol ;
- pack recommandé ;
- produit complémentaire ;
- suggestion éditoriale liée au produit ;
- contenu de réassurance ;
- mise en avant d’un fournisseur référencé.

Ces éléments ne doivent jamais entrer en concurrence visuelle avec l’achat.

---

## 7. Espaces naturels de la régie publicitaire

Ces espaces sont le **périmètre naturel** de la monétisation ; en **phase initiale**, toute **automatisation** de régie y reste **strictement limitée** (cf. **§5.1**), sans débordement vers le e-commerce.

La régie publicitaire peut être envisagée prioritairement dans :

- les articles éditoriaux ;
- les recettes ;
- les dossiers thématiques ;
- les guides d’achat ;
- les newsletters ;
- certains espaces communautaires ;
- les événements ;
- les contenus sponsorisés clairement identifiés ;
- les sélections partenaires encadrées.

La publicité doit toujours être contextualisée, lisible, sobre et cohérente avec l’univers C-Kreyol.

---

## 8. Charte de cohérence annonceurs

C-Kreyol peut accepter des annonceurs ou partenaires liés notamment à :

- l’alimentation ;
- la gastronomie ;
- les cultures créoles ;
- les produits ultramarins ;
- l’artisanat ;
- le tourisme ;
- les événements ;
- les services utiles à la diaspora ;
- les médias culturels ;
- les livres ;
- la formation ;
- la logistique ;
- les acteurs économiques ultramarins ;
- les producteurs, marques et distributeurs compatibles avec la ligne C-Kreyol.

C-Kreyol doit refuser les publicités incohérentes avec sa promesse, trop agressives, trop intrusives ou susceptibles de dégrader la confiance.

---

## 9. Ligne rouge

C-Kreyol n’est pas un site publicitaire avec une boutique.

C-Kreyol est une boutique média-communautaire, avec une régie sélective au service d’un écosystème cohérent.

La publicité ne doit jamais prendre le pouvoir sur la boutique, l’éditorial ou la communauté.

---

## 10. Implications UX et produit

Toute évolution future doit être classée dans l’un des trois mondes :

- e-commerce ;
- éditorial ;
- communautaire.

Pour chaque évolution, il faut préciser :

- le monde concerné ;
- le rôle de l’évolution ;
- son impact sur l’expérience utilisateur ;
- son impact sur la monétisation ;
- son niveau de proximité avec l’acte d’achat ;
- les risques de pollution visuelle ou commerciale ;
- les règles de protection à appliquer.

Cette classification doit éviter les mélanges confus entre contenu, publicité, communauté et vente.

---

## 11. Implications techniques

Cette vision n’impose pas de développer immédiatement les trois mondes.

Elle impose en revanche de ne pas fermer les portes suivantes :

- capacité à distinguer les contenus éditoriaux des pages marchandes ;
- capacité à distinguer les espaces communautaires des pages e-commerce ;
- capacité future à intégrer une régie publicitaire maîtrisée ;
- capacité à contextualiser les contenus selon les portes d’entrée ;
- capacité à relier un produit à des contenus éditoriaux ;
- capacité à relier une origine, une collection, une catégorie ou un producteur à des récits ;
- capacité à garder le tunnel marchand propre et protégé.

L’architecture doit rester progressive : on peut commencer par le e-commerce et l’éditorial léger, tout en gardant la vision d’ensemble.

---

## 12. Principe de priorité

À court terme, C-Kreyol peut prioriser :

1. la crédibilité e-commerce ;
2. la qualité de la page boutique ;
3. la clarté des portes d’entrée ;
4. les contenus éditoriaux utiles à la vente ;
5. la préparation d’un futur monde communautaire ;
6. la préparation d’une régie publicitaire sélective.

Le communautaire et la régie peuvent être conçus progressivement, sans fragiliser le socle marchand.

---

## 13. Formule de synthèse

C-Kreyol vend des produits créoles sélectionnés, raconte les cultures et les usages qui leur donnent du sens, et rassemble une communauté autour d’un univers créole vivant, sobre et crédible.

Le commerce porte la vente.  
L’éditorial porte le désir.  
La communauté porte la confiance.  
La régie porte une partie du financement, sans jamais polluer l’expérience d’achat.

---

## 14. Décision figée

La vision média-commerce C-Kreyol est **figée** comme **orientation stratégique long terme**. Elle structure les décisions UX, éditoriales, communautaires, publicitaires et e-commerce, **sans élargir** le périmètre de livraison immédiat du MVP (ni substituer au [cadrage Phase 1](NOTE_DE_CADRAGE.md) et aux ADR de livraison).

Toute **évolution publicitaire** ou **communautaire** future devra respecter la **protection du parcours e-commerce** : **aucune pollution publicitaire agressive** dans les **zones d’achat** (cf. §6.1 et [ADR-CKR-009](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-009)).

Les développements futurs doivent en outre respecter l’architecture à **trois mondes** et, hors zones protégées, toute monétisation publicitaire reste **sélective**, **contextualisée** et **maîtrisée** (§5, §7).

---

## 15. Historique du document

| Date | Changement |
|------|------------|
| 2026-04-26 | Intégration `docs/direction/` ; liens [ADR-CKR-009](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-009), [NOTE_DE_CADRAGE](NOTE_DE_CADRAGE.md) ; §15 (historique). **§14 actée** (MVP, zones d’achat). **§5.1** : trajectoire monétisation (auto **cloisonnée** → régie **directe** à maturité) ; **§4** / **§7** ; e-commerce **sanctuarisé** dans les deux cas. |
| 2026-04-26 | **§3.1** : double cible B2C/B2B — renvoi **[DOCTRINE_CK_ECOMMERCE_B2C_B2B.md](DOCTRINE_CK_ECOMMERCE_B2C_B2B.md)**, **[ADR-CKR-010](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-010)** ; précision **affichage contextualisé** (§2.1 doctrine). |
| 2026-04-26 | **§3.4** — langues créoles : **[DOCTRINE_CK_LANGUES_CREOLES.md](DOCTRINE_CK_LANGUES_CREOLES.md)**, **[ADR-CKR-011](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-011)** ; distinction **EXPLOITATION_I18N** (FR/EN/ES). **En-tête** pilotage complété. |
