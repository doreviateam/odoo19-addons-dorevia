# Contrat d’URL de la porte **Origines** — cadrage et analyse comparative

| Champ | Valeur |
|--------|--------|
| **Statut** | **Arbitrages métier MOA verrouillés** (**§13**, 2026-04-22) — cardinalité, filtre **OU**, principe source de vérité, signal éditorial **par origine**, entrée **`/shop`**, repli référence invalide, état vide, fiche produit, **pas de hub obligatoire** v1. **Reste pour PV / spec d’implémentation** : choix **technique** fin **A1 vs A2** si les deux restent possibles sur l’instance ; **noms exacts** des paramètres d’URL ; **copy** figée des messages ; détail **canonical / SEO**. |
| **Date** | 2026-04-22 (rédaction, validation cadre, position §4.0, **verrouillage arbitrages métier §13**). |
| **Périmètre** | Forme des **URL** empruntées par la carte **Origines** (Explorer), **sélection des produits** sur `/shop`, et **projection front** — dans le respect de [ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007) (convergence boutique). |
| **Prérequis actés** | **Priorité** vague B ; **Collections** gelées ([SPEC_SHOP_PORTES §4.2](SPEC_SHOP_PORTES.md#42-collections)). **Doctrine porte** : **§13** (synthèse MOA). **Source de vérité (principe)** : donnée catalogue **structurée**, **multi-valeurs**, **sans** tag libre seul, **sans** champ texte faible, **sans** modèle CK lourd en **v1** sans besoin démontré — **§4.0** / **§13** ; **implémentation** : priorité **A1** (attribut), repli **A2** si insuffisance **documentée** au PV technique. |

Ce document **structure** les choix, **évalue** les options (§4–§5), fixe le **signal éditorial** (§3) et consigne les **arbitrages métier verrouillés** (**§13**). Il complète la [SPEC_SHOP_PORTES §4.5](SPEC_SHOP_PORTES.md#45-origines) par le détail **URL + données + front + cas limites**.

**Trajectoire actée** : **arbitrages métier** → **§13 verrouillé** ; **suite** : PV ou spec d’implémentation pour **résidu technique** (§12.1 / §12.2 : A1↔A2 si doute, paramètres URL, copy exacte, canonical) → **développement**.

---

## 1. Cadre doctrinal rappelé

1. **Standard Odoo d’abord** ([ADR-CKR-001](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001)) : toute **identification produit** (ce qu’est « une origine » en base) doit **privilégier** un mécanisme natif ou documenté (attribut e-commerce, champ standard, etc.) **si** il assure **cohérence catalogue** et **maintenabilité**.
2. **Convergence commerciale sur `/shop`** ([ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007)) : pas de vitrine d’achat parallèle ; la liste achetable reste le **moteur boutique natif**.
3. **Construction CK minimale** ([ADR-CKR-002](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-002)) : la couche CK **habille** (routes alias, bandeaux, résolution de domaine) ; elle ne **réinvente** pas un second catalogue métier sans nécessité documentée.
4. **Capitalisation** : réemploi du **patron Hybride H1** et de sa **variante cible native** là où le standard expose déjà une URL canonique satisfaisante — voir [CONTRAT_URL_PROMOTIONS.md §13.6](CONTRAT_URL_PROMOTIONS.md) et [CONTRAT_URL_CATEGORIES.md §12](CONTRAT_URL_CATEGORIES.md).

---

## 2. Précision MOA — éviter deux pièges de formulation

### 2.1 « Dimension éditoriale » : la rendre **opérationnelle**

L’expression ne doit **pas** rester une intention flottante. Dans ce document, elle se décline en **obligations vérifiables** (voir §3). Toute proposition de solution (§4–§6) doit explicitement indiquer **comment** chaque obligation est satisfaite.

### 2.2 Interdiction fonctionnelle du **filtre silencieux**

Une entrée depuis **Origines** (carte Explorer, lien partagé, ou URL d’alias) qui se traduirait **uniquement** par l’activation d’un **filtre catalogue** (facette cochée, domaine appliqué) **sans** couche de **contexte de lecture visible et compréhensible** pour le visiteur est **non conforme** à la décision MOA.

**Exemple disqualifiant** : le visiteur atterrit sur une grille `/shop` **strictement identique** visuellement au parcours « boutique générique », sans titre de portée, sans phrase d’accroche, sans distinction claire du mode « je parcours toute la boutique » vs « je suis dans une entrée Origines ».

**Remarque** : le **moteur** de filtrage peut rester **standard** (ex. facettes `attrib`) ; l’exigence porte sur la **couche de lecture CK** (bandeau, copy, titrage — §3) **en plus** du filtre.

---

## 3. Niveau minimal de signal éditorial (exigible livraison)

Les portes **Kits**, **Promotions** et **Catégories** ont fixé un **précédent de lisibilité** : titre / breadcrumb natif ou **bandeau CK** au-dessus de la liste produits. **Origines** doit **au minimum** :

| # | Signal | Description | Contrôle rapide |
|---|--------|---------------|-----------------|
| S1 | **Titre de portée** | Le visiteur voit un **titre** clair du type porte + contexte (ex. bloc titre **« Origines »** et, si une origine précise est active, **mention explicite** de cette origine dans le titre ou à la ligne suivante). | Une capture d’écran sans scroll au-dessus de la grille suffit à comprendre **quelle porte** et **quel repère** sont actifs. |
| S2 | **Ligne de contexte** | Au moins **une phrase courte** ou équivalent (sous-titre, chapô) expliquant **ce que liste la page** (ex. *« Sélection de produits associés à cette origine. »* — copy finale = métier). | Un lecteur naïf comprend **pourquoi** la liste est restreinte. |
| S3 | **Cohérence Explorer** | Le parcours **carte Origines → boutique** ne casse pas la continuité avec les autres portes (niveau de finition, classes SCSS, placement du bandeau **aligné** sur `ckr_shop_pack_banner` / `ckr_shop_promo_banner`). | Revue visuelle comparée aux portes A déployées. |
| S4 | **État vide explicite** | Si **aucun** produit ne correspond au repère demandé (ou si la porte est « vide » côté données), **message dédié** — pas une grille muette « 0 résultat » sans explication métier (voir §8–§13). | Message distinct du cas « recherche sans résultat » générique si pertinent ; **rebond** possible vers boutique ou autres origines (**§13**). |

**Évolutivité** : les points **S1–S4** constituent le **socle** ; des enrichissements ultérieurs (visuels, liens vers contenus éditoriaux, mise en avant d’origines phares) doivent pouvoir s’ajouter **sans** remettre en cause le modèle de données retenu (**§13** + choix technique A1/A2 au PV).

### 3.1 Métadonnées **par origine** (verrouillage MOA — §13)

Au-delà du **bandeau de liste** (S1–S2), chaque **origine** (entité de projection éditoriale, alignée sur la donnée catalogue mais **non** réduite à celle-ci seule) porte **au minimum** les champs suivants — **obligatoires** dès la première implémentation :

| Métadonnée | Rôle |
|------------|------|
| **Nom visiteur** | Libellé lisible sur la porte / bandeau / liens. |
| **Phrase courte de contexte** | Chapô ou sous-titre expliquant la lecture (complète S2 par origine lorsque pertinent). |
| **Slug stable** | Identifiant d’URL **durable** et partageable (cohérent avec le véhicule d’URL retenu au PV technique). |
| **Ordre d’affichage** | Séquence contrôlée (listes, cartes Explorer futures, etc.). |
| **Visibilité site** | Publier / masquer l’origine côté visiteur **sans** supprimer la donnée catalogue sous-jacente. |

**Hors périmètre v1 (ouverts en montée en puissance)** : **image** par origine **non obligatoire** ; **contenu riche** (HTML long, blocs marketing) **non** prérequis de première implémentation (**§13**).

---

## 4. PARTIE A — Source de vérité « origine »

### 4.0 Position MOA — base de discussion atelier *(pré-atelier, à consolider au §12.1)*

Cette section **fixe l’intention MOA** pour nourrir l’atelier et l’analyse comparative **§4.2–§4.6**. Elle **ne remplace pas** le procès-verbal : l’atelier peut **confirmer**, **nuancer** ou **infirmer** chaque point avec **justification** consignée dans **§12.1**.

**Confirmation MOA (séquence atelier)** : la MOA **valide** que l’atelier peut **démarrer** sur la base combinée suivante — **§4.0** (position de départ sur la source de vérité) ; **§12.1** (rôle du PV : **valider**, **nuancer** ou **infirmer** les arbitrages obligatoires) ; **§12.3** (grille **minimale** de questions complémentaires sur données / éditorial / cohérence). **Suite (avant §13)** : tenue de l’atelier → **verrouillage des choix dans le PV** → implémentation. **Après §13** : les **arbitrages métier** sont **figés en §13** ; le **PV** consolide surtout le **résidu technique** (**§12** : A1↔A2, URL, copy, canonical, UI fiche).

**Post-§13** : la **§4.0** ci-dessous reste la **ligne doctrinale** pour la **source de vérité catalogue** ; le **détail technique** A1↔A2 et l’**implémentation** des champs **§3.1** sont **portés** par le **PV** ou la **spec d’implémentation** **sans rouvrir §13** sauf **décision documentée** de la MOA.

#### Intention générale

**Socle produit simple + projection éditoriale distincte** :

- une **donnée produit structurée** pour rattacher clairement un produit à **une ou plusieurs** origines ;
- une **couche éditoriale CK** pour donner à chaque origine une **portée de lecture visible** côté visiteur (cf. §2.2, §3).

L’objectif est d’**éviter** à la fois le **filtrage invisible** seul et un **modèle trop lourd** **dès le départ** si un socle plus simple préserve **lisibilité catalogue**, **traçabilité back-office** et **évolutivité** vers une vraie porte éditoriale.

#### Doctrine résumée (ligne de travail MOA)

> **Origines doit reposer sur une donnée catalogue structurée ; la valeur côté visiteur vient d’une projection éditoriale explicite côté CK.**

En première intention MOA :

- **éviter** le **tag libre** comme **réponse finale** de la source de vérité ;
- **éviter** le **modèle CK dédié complet** **sans besoin démontré** ;
- **privilégier** un **socle structuré sobre**, **enrichi** par une **couche éditoriale CK**.

#### Hiérarchie des options (alignement avec §4.2–§4.6)

| Niveau | Option (réf. §) | Position MOA |
|--------|-----------------|----------------|
| **À privilégier en première analyse** | **A1 — Attribut e-commerce** (§4.2) + **couche CK de projection** (§6, §3) | Sobriété donnée, compatibilité **e-commerce standard**, rattachements clairs, **richesse front** sans refonte précoce du socle. |
| **Acceptable si le standard attribut est trop limitant** | **A2 — Champ custom / taxonomie CK légère** (§4.3) | Si gain **net** sur gouvernance, stabilité des rattachements ou **cas métier** réels non tenables proprement en A1. |
| **À éviter par défaut** | **A3 — Tag libre** (§4.4) comme **seule** source de vérité | Fragilité saisie, robustesse métier, **difficulté** à soutenir une projection front **cohérente dans le temps**. |
| **À ne retenir qu’en cas de besoin démontré** | **A5 — Modèle CK dédié complet** (§4.6) | Uniquement si besoins réels documentés (contenus riches par origine, règles de visibilité fortes, hiérarchie / gouvernance spécifique, ou **impossibilité avérée** de tenir la cible avec un socle plus léger). |
| **Complément géographique** | **A4 — Pays / région** (§4.5) | Souvent **combiné** à A1 ou A2 selon le référentiel métier. |

---

### 4.1 Critères d’évaluation (alignés sur les autres CONTRAT)

| # | Critère | Pondération |
|---|---------|-------------|
| C1 | **Alignement doctrinal** (ADR-001 / 007, pas de catalogue parallèle) | **Élevée** |
| C2 | **Unicité / non-duplication** : une seule notion « origine produit » référencée pour le filtre | **Élevée** |
| C3 | **Exploitabilité e-commerce** (publication site, filtrage `/shop`) | **Élevée** |
| C4 | **Compatibilité multi-valeurs** (produit étiqueté plusieurs origines — §8) | Moyenne à **élevée** selon métier |
| C5 | **Charge CK** (compute, résolveur, synchronisation) | Moyenne |
| C6 | **Projection éditoriale** : peut-on **nommer** et **décrire** proprement chaque valeur côté visiteur ? | **Élevée** |
| C7 | **Maintenabilité upgrade** (Odoo 19 → suivant) | Moyenne |

### 4.2 Option A1 — **Attribut e-commerce** (`product.attribute` / `product.template.attribute.value`)

**Mécanisme** : une famille d’attributs du type *Origine*, *Terroir*, *Région* exposée sur le site ; filtrage via mécanisme **`attrib`** standard sur `/shop`.

| Pour | Contre |
|------|--------|
| Filtrage **natif** ; facettes connues des utilisateurs Odoo shop | Sémantique parfois **variante** (PTAV) — à valider si l’origine est bien portée au **template** ou à la **variante** |
| Nom d’affichage et SEO **réutilisent** le modèle standard | **Seul** `attrib` **sans** bandeau CK = risque de **filtre silencieux** (§2.2) → **couche présentation CK obligatoire** |

**Verdict provisoire** : **aligné préférence MOA (§4.0)** — **candidate privilégiée en première analyse** ; sous réserve des tranchés atelier : **template vs variante** (PTAV), **mono- vs multi-valeurs**, et constat que le **socle attribut suffit** pour porter proprement le rattachement catalogue (sinon pivot vers §4.3). **Couche présentation CK obligatoire** pour S1–S4 (§3).

### 4.3 Option A2 — **Champ structuré** sur `product.template` (Char / Many2one / Many2many custom)

**Mécanisme** : champ(s) dédiés CK ou module tiers ; domaine `/shop` via extension `_search_get_detail` ou équivalent.

| Pour | Contre |
|------|--------|
| Contrôle **total** du schéma | **Charge CK** plus élevée (C5) ; risque de **dupliquer** un attribut déjà existant |
| Adapté si « origine » = référentiel métier **hors** grille attributs | Filtrage **non** `attrib` → plus de code **route / mode** type `ckr_mode=origin` |

**Verdict provisoire** : **candidate de repli MOA (§4.0)** si le **socle attribut standard** est **trop limitant** (gouvernance, stabilité des rattachements, cas métier réels) — amélioration **nette** vs forcer A1.

### 4.4 Option A3 — **`product.tag`** (ou tags équivalents)

**Mécanisme** : tags « Martinique », « Guadeloupe », etc. ; filtre par domaine sur les templates liés.

| Pour | Contre |
|------|--------|
| Rapide à alimenter en **pilotage** | **C2 faible** si les tags servent **aussi** à d’autres usages (promo, saison) — **pollution** sémantique |
| | Risque de **confondre** « étiquette marketing » et « origine géographique » sans gouvernance |

**Verdict provisoire** : **non souhaitée par défaut comme source finale** (MOA §4.0) — **rejet recommandé comme source principale** ; **exception** uniquement sous **gouvernance forte** et périmètre de tags **dédié** et documenté (préfixe, catégorie, convention).

### 4.5 Option A4 — **Référentiel pays / région** (`res.country`, zones custom)

**Mécanisme** : origine = pays ou macro-zone ; filtre par relation Many2one / sélection.

| Pour | Contre |
|------|--------|
| Cohérent pour une **origine strictement géographique** | Granularité **île / terroir** souvent **au-dessus** du pays seul |
| Données **standard** Odoo pour le pays | Peut nécessiter un **référentiel CK** complémentaire pour finesse |

**Verdict provisoire** : **candidate partielle** (souvent en **combinaison** avec A2 ou taxonomie CK).

### 4.6 Option A5 — **Modèle CK dédié** (ex. `ckr.origin` + Many2many produits)

**Mécanisme** : entité éditoriale « Origine » avec nom, texte d’intro, image optionnelle, lien produits.

| Pour | Contre |
|------|--------|
| **C6 élevée** : richesse éditoriale **native** par entité | **C5 élevée** : construction et maintenance **CK** |
| Découple **origine marketing** des attributs catalogue | À **justifier** si A1/A2 suffisent avec une couche présentation |

**Verdict provisoire** : **réservée à un besoin démontré** (MOA §4.0) — **candidate** seulement si la MOA / atelier documente au minimum : contenus **riches** par origine, règles de visibilité **fortes**, hiérarchie ou gouvernance **spécifique**, ou **impossibilité avérée** de tenir la cible avec A1/A2 + projection CK ; sinon **surspec**.

---

## 5. PARTIE B — Contrat d’URL et point d’entrée

### 5.1 Option B1 — **Hybride H1** (aligné **§13** — *à détailler au PV technique*)

**Forme** : **`/origines`** → **redirection HTTP 301** vers **`/shop?ckr_mode=origin`** avec, selon cas, **`ckr_ref=<id>`** ou **`ckr_origin=<slug>`** (nom exact **à figer** pour éviter collision avec les params natifs).

**Alignement** : même logique que [CONTRAT_URL_PACKS §12](CONTRAT_URL_PACKS.md) / [CONTRAT_URL_PROMOTIONS §13.1](CONTRAT_URL_PROMOTIONS.md) ; extension whitelist `CKR_MODES_ALLOWED` ; canonical sur `/shop?...` si exception doctrinale actée (même principe que Pack/Promo).

**Acté MOA (§13)** : **pas de hub CMS obligatoire** en amont pour la **v1** ; la **cible de première intention** est la **convergence directe** vers **`/shop` contextualisé** (liste + bandeau / signaux §3–§3.1).

**Points ouverts (PV technique)** :

- **Entrée Explorer** : une URL d’alias unique (`/origines`) vs **liens profonds** stables par origine (sous-domaine de choix) — sans imposer de **page hub** dédiée en v1.
- **Nom et sémantique du paramètre** de sélection (`ckr_ref` générique vs paramètre dédié) — cohérence avec la checklist [CONTRAT_URL_PROMOTIONS §13.6](CONTRAT_URL_PROMOTIONS.md).

### 5.2 Option B2 — **Filtrage 100 % `attrib`** (URL « native »)

**Forme** : alias **`/origines`** → **301** vers **`/shop?attrib=<id>-<value>`** (forme exacte selon build Odoo 19).

**Alignement** : proche de la **variante cible native** (cf. Catégories).

**Limite** : sans **bandeau / copy CK** (§3), tendance forte au **filtre silencieux** (§2.2) — **bandeau CK quand même obligatoire** si cette option est retenue pour l’URL technique.

### 5.3 Option B3 — **Hub CMS + liens profonds**

**Forme** : page **`/origines`** (non stub) listant les origines avec liens vers `/shop?...` pour chacune.

**Alignement** : acceptable **optionnellement** ou **plus tard** si la MOA souhaite une **vitrine** d’entrée ; la **convergence achat** reste `/shop` ([ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007)). **V1** : **non requis** (**§13**). Risque : **double lieu** à maintenir (copy hub + copy bandeau shop) si cette voie est activée.

---

## 6. Projection front (hors choix URL)

**Livrables typiques** (sur le modèle des portes A) :

- Template QWeb **bandeau** conditionné par le mode origine actif (variables `ckr_origin_mode`, `ckr_origin_title`, `ckr_origin_subtitle`, `ckr_origin_empty` — noms indicatifs).
- SCSS dédié (variante `--empty` si état vide).
- **Pas** de substitution du template produit natif sauf nécessité documentée.

**Règle** : le bandeau doit réaliser **S1 + S2** (§3) **au-dessus** de la grille ; le filtre sous-jacent peut rester invisible techniquement pour le visiteur.

**Acté MOA (§13) — fiche produit** : l’**origine** (ou les origines) doit être **visible sur la fiche produit**, **au moins sous une forme simple**, pour assurer la **cohérence** entre la lecture d’entrée (portes / liste contextualisée) et la consultation produit (snippet, bloc attributs, ou équivalent — **détail d’intégration** au PV technique / maquettes).

---

## 7. Multi-valeurs (produit × plusieurs origines)

**Verrouillage MOA (§13)** :

| Question | Décision actée | Impact implémentation |
|----------|----------------|------------------------|
| **Cardinalité** | Un produit peut être rattaché à **plusieurs** origines ; la donnée est **multi-valeurs** dès le cadrage. | Schéma catalogue + domaine liste |
| **Filtre lorsque plusieurs origines sont sélectionnées** | Logique **OU** : le produit apparaît s’il porte **au moins une** des origines sélectionnées. | `domain` type `('id', 'in', …)` avec union des ensembles produits |
| Affichage fiche produit | **Visibilité simple** des origines (**§6**, §13) ; affichage **de toutes** les valeurs pertinentes ou **primaire + « +n »** — **nuance UI** au PV si besoin. | Templates / snippets |
| Cohérence avec facettes | Si **A1** : respecter le comportement **multi-valeurs** Odoo sur `attrib` + règle **OU** documentée côté CK si l’UI combine plusieurs origines hors facette native. | Spec technique |

---

## 8. État vide et référence invalide

**Exigence (§13)** : un **état vide dédié** pour Origines — message **métier**, formulation **cohérente** avec la lecture d’entrée, classe visuelle dédiée ; **possibilité de rebond** vers la **boutique générique** et/ou vers **d’autres origines** (CTA ou liens — **détail copy** au PV).

**Cas à couvrir** :

- Aucun produit ne porte l’origine demandée (**origine valide** mais catalogue vide pour ce filtre) → **état vide dédié** (**§13**).
- Référence d’origine **invalide** (inconnue, non publiée, hors site, `ckr_*` incohérent) → **repli propre** : **HTTP 302** vers **`/shop`** **nu** (sans paramètres invalides ni contexte d’origine erroné) — acté en **[SPEC_IMPL_ORIGINES.md §3.3](SPEC_IMPL_ORIGINES.md)** ; principe : **pas** de page **cassée** ni d’état **ambigu** pour le visiteur (**§13**).
- Origine **dépubliée** entre-temps → **même repli** que référence invalide (**302** → **`/shop`** nu) si la référence n’est plus résolvable ; sinon état vide dédié si l’origine reste valide mais sans produit (**SPEC_IMPL §3.3** / **§5**).

---

## 9. Sécurité, SEO et canonical

- **Validation des références** : tout identifiant passé en query (`ckr_ref`, slug, etc.) doit être **résolu côté serveur** avec contraintes **website** / **publication** ; en cas d’**échec de résolution**, appliquer le **repli** défini en **§8** / **§13** (boutique **`/shop`** sans contexte invalide).
- **Canonical** : si `ckr_mode=origin` est retenu, trancher explicitement si l’**exception** `website._get_canonical_url` (comme Pack/Promo) s’applique — et documenter les **doublons** éventuels (même liste via `attrib` vs via `ckr_mode`).
- **SEO** : titre de page (`<title>`) et H1 doivent refléter **S1** ; éviter les doubles indexations si plusieurs URL mènent à la même liste.

---

## 10. Compatibilité avec les modes existants (`pack`, `promo`)

Toute implémentation doit préserver la **non-régression** des portes **Kits** et **Promotions** : whitelist stricte, **exclusivité** des modes (un seul « mode Explorer » actif à la fois), strip de `ckr_mode` lors des redirections **Catégories** si pertinent — reprendre les patterns actuels de `controllers/website_sale_ckr.py`.

---

## 11. Références

- [SPEC_SHOP_PORTES.md §4.5](SPEC_SHOP_PORTES.md#45-origines) — matrice porte et décision de fond.
- **§13** — **verrouillage MOA** arbitrages métier.
- [CONTRAT_URL_PACKS.md §12](CONTRAT_URL_PACKS.md) — patron H1 (référence historique).
- [CONTRAT_URL_PROMOTIONS.md §12–13.6](CONTRAT_URL_PROMOTIONS.md) — généralisation multi-modes et check-list.
- [CONTRAT_URL_CATEGORIES.md §12](CONTRAT_URL_CATEGORIES.md) — variante **cible native**.
- [ARCHITECTURE_DECISION_RECORD.md](../direction/ARCHITECTURE_DECISION_RECORD.md) — ADR-CKR-001, 002, 007, 008.

---

## 12. Suite — PV / spec d’implémentation *(résidu après §13)*

Les **arbitrages métier** sont **verrouillés** en **§13**. Le **PV** (ou la **spec d’implémentation** — document **[SPEC_IMPL_ORIGINES.md](SPEC_IMPL_ORIGINES.md)**) documente désormais surtout :

- le **choix technique** **A1** vs **A2** (ou combinaison) **sur l’instance** si un doute subsiste après analyse ;
- les **noms exacts** des **paramètres d’URL** (figés en SPEC) ; le repli « référence invalide » est acté en **302** → **`/shop`** nu (**[SPEC_IMPL_ORIGINES.md §3.3](SPEC_IMPL_ORIGINES.md)**) ;
- la **copy figée** (titres, états vides, rebonds) ;
- les règles **canonical / SEO** détaillées ;
- les **maquettes** ou captures pour **fiche produit** et **bandeau liste**.

Mettre à jour la [SPEC_SHOP_PORTES.md §6](SPEC_SHOP_PORTES.md) lorsque le **résidu** est **clos** et la **version module** est connue.

**Confirmation MOA** : la suite peut se faire via **PV** ou **spec d’implémentation** en s’appuyant **notamment** sur la **check-list §12.2** (les autres sous-sections de **§12** restent des **rappels** de traçabilité).

### 12.1 Synthèse §12.1 historique ↔ §13 *(pour traçabilité)*

| Axe historique §12.1 | Statut après §13 |
|----------------------|------------------|
| **1 — Source de vérité** | Principe acté (**§13.3**) ; **A1 prioritaire**, **A2** si insuffisance **documentée** ; **A3** / **champ texte faible** / **A5 v1 sans besoin** exclus. |
| **2 — Véhicule d’URL** | **Convergence `/shop` contextualisé** ; **pas de hub obligatoire** v1 (**§13.8**) ; détail route / query au PV. |
| **3 — Signal éditorial** | **§3 + §3.1** actés ; image et contenu riche **hors** prérequis v1 (**§13.6**). |
| **4 — Multi-valeurs** | **Multi** + filtre **OU** (**§13.1–§13.2**, §7). |
| **5 — Invalide + vides** | Repli **`/shop`** propre (**§13.9**) ; **état vide dédié** + rebond (**§13.10**, §8). |

### 12.2 Check-list résiduelle *(à cocher au PV / avant merge)*

- [ ] **A1 / A2** : choix technique **écrit** + schéma de données (ou note « A1 validé sur instance »).
- [ ] **Paramètres URL** + code HTTP du repli invalide.
- [ ] **Copy** : messages état vide, rebonds, libellés par origine (§3.1).
- [ ] **Canonical + SEO** : règle publiée (§9).
- [ ] **Fiche produit** : maquette ou screenshot d’acceptation (**§13.7**).

### 12.3 Questions MOA *(grille initiale §4.0)* — **état après §13**

1. **Cardinalité** → **Réponse** : **multi-valeurs** par produit (**§13.1**).
2. **Suffisance du standard (A1)** → **Réponse** : principe **A1 prioritaire** ; **tranché instance** au PV si doute persistant (**§13.3**).
3. **Métadonnées par origine** → **Réponse** : **§3.1** (nom visiteur, phrase, slug, ordre, visibilité) (**§13.5**).
4. **Seuil bascule A5** → **Inchangé** : critères mesurables toujours pertinents pour une **évolution** ; **v1** sans modèle lourd (**§13.3**).
5. **Cohérence sans duplication** → **Principe** : donnée catalogue = **vérité** rattachement ; couche CK = **projection** (§3.1, bandeau, fiche) — **détail d’implémentation** (pas de second référentiel produit) au PV technique.

---

## 13. Verrouillage MOA — arbitrages métier *(2026-04-22)*

Cette section **fige** les décisions MOA **avant** le détail d’implémentation. Elle sert de **référence** pour le **PV** (consolidation), la **spec technique** et le **contrôle de recette**.

**Confirmation MOA (séquence post-verrouillage)** : la MOA **valide** la structuration du contrat — **§13** = **référence métier stable** pour la porte **Origines** ; la suite se fait via **PV** ou **spec d’implémentation** pour le **résidu technique** (**§12**, **notamment la check-list §12.2**) ; puis **développement**. **§13** **ne se rouvre pas** sans **nouvelle décision MOA écrite**.

### Doctrine synthétique

**Origines** = **porte éditoriale de navigation** vers **`/shop`**, appuyée sur une **donnée produit structurée multi-valeurs**, avec un **signal éditorial minimal visible et compréhensible** pour le visiteur.

### 13.1 Cardinalité

Un **produit** peut être rattaché à **plusieurs** origines. La notion **Origines** est **multi-valeurs** dès le cadrage et le schéma de données.

### 13.2 Règle de filtrage (sélection multiple)

Lorsque **plusieurs** origines sont sélectionnées pour affiner la liste, la logique retenue est un **OU** : un produit est **affiché** dès lors qu’il porte **au moins une** des origines sélectionnées.

### 13.3 Source de vérité (principes)

- **Pas** de **tag libre** comme **source finale** de vérité.
- **Pas** de **champ texte faible** (saisie non structurée) comme socle.
- **Pas** de **modèle CK dédié lourd** en **première passe** **sans besoin démontré** (cf. §4.6).
- **Préférence** : **donnée catalogue structurée**, **sobre**, **multi-valeurs**, compatible avec une **projection front éditoriale** — en pratique **priorité d’implémentation** à **A1** (attribut e-commerce), **repli A2** (champ / taxonomie CK **légère**) si le standard attribut est **insuffisant** (à **documenter** au PV technique).

### 13.4 Projection éditoriale

La **donnée produit seule** ne suffit **pas**. Chaque origine doit pouvoir produire une **lecture éditoriale visible** côté visiteur (**bandeau**, contexte, cohérence avec §2.2).

### 13.5 Niveau minimal de signal éditorial *(par origine, v1)*

Pour **chaque** origine, le **minimum** comprend :

| Élément | Exigence |
|---------|----------|
| **Nom visiteur** | Libellé clair. |
| **Phrase courte de contexte** | Chapô / sous-titre lisible. |
| **Slug stable** | URL / clé durable pour liens et résolution. |
| **Ordre d’affichage** | Contrôle de la séquence présentée. |
| **Visibilité site** | Publier / masquer côté visiteur. |

L’entrée par Origines **ne doit jamais** se réduire à un **filtre silencieux** sur une grille **`/shop`** **indiscernable** d’une boutique générique (**§2.2**).

### 13.6 Image et contenu riche *(hors v1 obligatoire)*

- **Image** par origine : **non obligatoire** à ce stade.
- **Contenu riche** : **non** prérequis de **première implémentation**.
- Ces enrichissements restent **ouverts** pour une **montée en puissance** ultérieure.

### 13.7 Fiche produit

L’**origine** doit être **visible sur la fiche produit**, **au moins sous une forme simple**, pour assurer la **cohérence** entre la lecture d’entrée et la consultation produit (**détail UI** au PV / maquettes).

### 13.8 Véhicule d’entrée

La **cible de première intention** est la **convergence directe** vers **`/shop` contextualisé**. **Pas** d’exigence de **hub dédié obligatoire** en amont à ce stade (**§5.3** optionnel / ultérieur).

### 13.9 Référence invalide

En cas de **référence invalide**, **repli propre** : **HTTP 302** vers **`/shop`** **nu** (paramètres erronés neutralisés, pas de contexte d’origine invalide conservé) — **pas** de comportement **cassé** ni **ambigu** pour le visiteur (**§8**, détail **[SPEC_IMPL_ORIGINES.md §3.3](SPEC_IMPL_ORIGINES.md)**).

### 13.10 État vide

Un **état vide dédié** est **requis**, avec formulation **cohérente** avec la lecture d’entrée et **possibilité de rebond** vers la boutique et/ou d’**autres origines** (**§8**).

---

## Historique du document

| Date | Changement |
|------|------------|
| 2026-04-22 | **Création** — cadrage initial : obligations **signal éditorial minimal** (§3), interdit **filtre silencieux** (§2.2), options source de vérité (§4), options URL (§5), projection front (§6), multi-valeurs (§7), état vide (§8), sécurité/SEO (§9), non-régression modes existants (§10), cases à cocher §12. |
| 2026-04-22 | **Validation MOA du cadre** — le document est **reçu** comme **base de travail pour l’atelier** ; trajectoire actée : atelier → **§12.1** (cinq arbitrages minimum) → implémentation. **§12** restructuré : **§12.1** = cinq axes MOA obligatoires (tableau + cases) ; **§12.2** = compléments (copy, canonical, sécurité). Statut en-tête mis à jour. |
| 2026-04-22 | **Position MOA pré-atelier (source de vérité)** : ajout **§4.0** (socle structuré sobre + projection CK ; hiérarchie A1 privilégiée, A2 repli, A3 évité par défaut, A5 si besoin démontré) ; verdicts **§4.2–§4.6** alignés ; **§12.3** = cinq questions explicites (cardinalité, suffisance attribut, métadonnées éditoriales par origine, seuil bascule A5, cohérence sans duplication). Prérequis tableau + note **§12.1** mises à jour. |
| 2026-04-22 | **Confirmation MOA** : réception de l’intégration **§4.0** / verdicts / **§12.3** ; **validation** de la séquence atelier (**§4.0** + **§12.1** + **§12.3** comme point de départ) sans préemption du PV ; suite : atelier → PV verrouillé → implémentation. Paragraphe **« Confirmation MOA (séquence atelier) »** ajouté en tête de **§4.0**. |
| 2026-04-22 | **Verrouillage MOA** : nouvelle **§13** (cardinalité **multi**, filtre **OU**, source structurée sans tag/texte faible/A5 lourd v1, projection + **§3.1** métadonnées par origine, image/contenu riche hors v1, fiche produit, entrée **`/shop`** sans hub obligatoire, repli invalide, état vide dédié) ; **§12** requalifié en **résidu PV / impl** ; §5–§9 alignés. Statut en-tête : arbitrages métier **verrouillés**. |
| 2026-04-22 | **Confirmation MOA** : **§13** acté comme **référence métier stable** ; suite = **PV** ou **spec d’impl.** pour résidu **§12** (notamment **§12.2**) → dev ; **pas de réouverture de §13** sans décision MOA **écrite**. Paragraphes ajoutés en tête de **§13** et en **§12** (rôle **§12.2**). |
| 2026-04-22 | **SPEC_IMPL_ORIGINES.md** créé : spec technique v1 (A1 + modèle léger `ckr.shop.origin`, `ckr_mode`/`ckr_origin`, hooks, bandeau, fiche produit, stub, tests §9, ouvertures §10). Référencé depuis **§12** du contrat. |
| 2026-04-22 | **Alignement contrat ↔ spec** : **§8** et **§13.9** — repli référence invalide / non résolvable acté en **302** → **`/shop`** nu (**SPEC_IMPL §3.3**) ; **§12** (résidu) mis à jour. |
