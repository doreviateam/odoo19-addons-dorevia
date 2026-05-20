# Proposition de traduction technique — UX-3 Palier A × doctrine CK

| Champ | Valeur |
|-------|--------|
| **Statut** | **GO MOA UX-3 Palier A** — variante B « Tenue » mergée (`19.0.15.2.0`) |
| **Branche** | `feat/marketone-ux3-product-cards-palier-a` |
| **Version précédente** | `19.0.15.1.0` — variante douce |
| **Version actuelle** | `19.0.15.2.0` — variante B « Tenue » implémentée |
| **PR** | [#9](https://github.com/doreviateam/odoo19-addons-dorevia/pull/9) — mergée |
| **Recette liée** | `docs/recette/RECETTE_MANUELLE_SHOP_UX3_PRODUCT_CARDS.md` |
| **Date** | 2026-05-19 |

---

## Contexte

Retour à froid MOA / direction artistique C-Kreyol :

- CK garde une ligne premium propre ;
- UX-2 sidebar validé, mergé et stable ;
- UX-3 Palier A améliore techniquement la grille produit ;
- mais la page risque encore de devenir trop « catalogue premium générique » sans précision DA.

**Ce document n'est pas une liste de règles à appliquer mécaniquement.**  
C'est une proposition de traduction technique, à arbitrer MOA avant tout commit d'intégration finale.

> La doctrine donne la direction.  
> Le Dev propose la traduction technique.  
> La MOA arbitre les choix visuels avant intégration finale.

---

## 1. Lecture de l'intention (reformulation)

La boutique doit rester **premium et structurée**, mais **vivante et chaleureuse** :

- l'image crée le désir ;
- le texte donne le sens ;
- le terracotta guide l'achat ;
- les accents (sauge, or, rose) restent rares.

Le risque actuel n'est pas technique — c'est une dérive vers une **grille « card SaaS »** (carte blanche encadrée, ombre, hover, séparation image/texte) qui concurrence le produit plutôt que de le révéler.

**Principe central CK :**

> Le pastel crée la lumière.  
> Le texte donne le sens.  
> L'image crée le désir.  
> L'interface accompagne l'achat.

---

## 2. État des lieux — ce que UX-3 apporte déjà

| Élément | Statut | Alignement doctrine |
|---|---|---|
| Système Odoo 19 (`--o-wsale-card-*`) | ✅ Solide | Technique durable |
| `object-fit: contain` | ✅ | Image non rognée |
| Ratio maîtrisé (réglage en tête de fichier) | ✅ | À arbitrer (4/3 vs 1/1) |
| Variante douce (ombre/lift/zoom réduits) | ✅ Partiel | Va dans le bon sens |
| `mix-blend-mode` désactivé | ✅ | Évite le refroidissement lifestyle |
| Hiérarchie titre / description / prix (SCSS) | ✅ | Hanken sur carte ; Garamond encore sur `.oe_product` legacy dans `_shop.scss` |
| UX-1 chips / UX-2 sidebar | ✅ Non touchés | Stable |
| Palette doctrine CK | ⚠️ Partielle | Tokens actuels = lot « Artisanal Terroir », pas la palette pastel CK du document |
| Action d'achat visible sur carte | ❓ | Hors Palier A actuel ; dépend du template Odoo |
| Pipeline image normalisé | ❌ Hors SCSS | Doctrine §7 — sujet contenu / média, pas CSS seul |

### Écart palette (extrait)

| Rôle doctrine | CK cible | Token actuel | Écart |
|---|---|---|---|
| Fond page | `#F5EDE0` | `$marketone-bg-soft` `#fbf2ed` | Proche, pas identique |
| Fond sidebar | `#EDE3D4` | transparent (UX-2) | Pas de panneau dédié |
| Fond image | `#F0E8DC` | `$marketone-bg-soft` en variante douce | À cibler explicitement |
| Texte | `#2A1F18` | `#1e1b18` | Plus froid / plus noir |
| Terracotta achat | `#C4715A` | `#a65d39` | Plus soutenu, moins « brûlé » |
| Vert sauge | `#5A8A6E` | `#4c6547` | Plus pastel en doctrine |
| Bordure | `#DDD0C2` | `#d9c2b8` | Proche |

---

## 3. Ce que je propose de conserver (sans discussion)

- Architecture **CSS custom properties** Odoo 19 sur `.oe_product_cart`.
- **`object-fit: contain`** (surcharge `--o-wsale-card-thumb-fill-mode`).
- **Scope `.marketone-shop`** — pas de refonte globale dans ce palier.
- **Non-régression** UX-1 / UX-2 (tests existants).
- **`mix-blend-mode: multiply` retiré** par défaut (déjà fait en `19.0.15.1.0`).
- **Réglages A/B** en tête de `_shop_product_cards.scss` (ratio, blend, lift).

---

## 4. Ce que je propose d'adoucir / ajuster (sous doctrine)

### 4.1 Cartes — poids visuel

| Axe | Constat | Proposition | Risque |
|---|---|---|---|
| Ombre | Encore « card flottante » | Repos : **aucune ombre** ou `0 1px 4px rgba(42,31,24,0.06)` ; hover : `0 4px 16px rgba(42,31,24,0.08)` max | Moins de relief → plus « posé », moins SaaS |
| Lift hover | `-4px` peut encore dominer | **`-2px` à `-3px`** ou lift **0** + seulement bordure/ombre hover | Moins d'effet catalogue |
| Zoom image | `1.03` OK | Garder **`1.02`** ou supprimer sur desktop | Discrétion |
| Bordure | `rgba` sur token ancien | Bordure **`#DDD0C2`** pleine mais **fine** ; hover légèrement plus marquée | Plus chaud si token CK |
| Fond carte | Blanc pur `#fff` | Tester **`#F5EDE0` très léger** sur toute la carte OU garder blanc avec fond image `#F0E8DC` seulement | **Arbitrage MOA** |
| Séparation image/texte | Bloc image ≠ bloc texte | **Même teinte de fond** image + zone info OU radius **12px** uniforme sur carte entière (overflow hidden) | Réduit l'effet « deux blocs collés » |

### 4.2 Ratio image

| Option | Ratio | Effet | Recommandation |
|---|---|---|---|
| A | **1 / 1** | Grille plus compacte, moins verticale, produit centré | **⭐ Recommandée** pour « vivant + achat » |
| B | **4 / 3** | Compromis actuel variante douce | Bon si MOA veut plus d'air vertical |
| C | **4 / 5** | Très portrait, effet « catalogue mode » | **Déconseillée** sauf arbitrage explicite |

### 4.3 Couleur & hiérarchie achat

| Élément | Proposition | Arbitrage MOA |
|---|---|---|
| **Prix actif** | `#C4715A` (terracotta pastel doctrine) | Fréquent = oui selon doctrine |
| **Hover titre lien** | Terracotta `#C4715A` (pas `#a65d39` actuel) | Remplacer partout cartes ou cartes seules ? |
| **Hover / CTA carte** | **Ne pas** passer au vert sauge sur toute la carte (doctrine : un accent vif à la fois) | Sauge réservé badges origine / nouveau |
| **Badges promo** | Terracotta ; sauge pour « Nouveau » / origine ; or/rose très rare | Mapping sémantique à valider |
| **Description** | Brun muted dérivé de `#2A1F18` (~70–75 % opacité), pas gris `#86736b` froid | Lisibilité + chaleur |

### 4.4 Typographie carte

- **Titre + prix** : Hanken Grotesk (déjà sur carte UX-3) — bon pour le scan.
- **Harmoniser** : retirer la double lecture Garamond via règles legacy `.oe_product` dans `_shop.scss` **uniquement sur la grille** (sinon conflit visuel). → Petit patch SCSS, pas QWeb.

### 4.5 Palette — où l'appliquer maintenant

**Recommandation : palier 1 = UX-3 + harmonisation légère `/shop` uniquement**, pas migration globale des tokens sur home / fiche produit / panier.

| Zone | Appliquer maintenant ? | Fichier |
|---|---|---|
| Fond image carte | ✅ Oui — `#F0E8DC` | `_shop_product_cards.scss` |
| Prix / hover titre carte | ✅ Oui — terracotta CK | idem |
| Ombres chaudes `rgba(42,31,24,…)` | ✅ Oui | idem |
| Fond page `/shop` | ⚠️ Proposer — `#F5EDE0` | `_shop.scss` |
| Fond sidebar `#EDE3D4` | ⚠️ Arbitrage — panneau vs transparent actuel | `_shop_sidebar.scss` |
| Tokens globaux `_tokens_colors.scss` | ❌ Pas en bloc brutal | Risque régression home, culture, checkout |

**Alternative tokens** (si MOA valide une base commune shop) : ajouter des **alias CK** sans casser l'existant :

```scss
// Exemple — à valider MOA avant commit
$ck-bg-page:    #F5EDE0;
$ck-bg-sidebar: #EDE3D4;
$ck-bg-image:   #F0E8DC;
$ck-text:       #2A1F18;
$ck-terracotta: #C4715A;
$ck-sauge:      #5A8A6E;
$ck-border:     #DDD0C2;
```

Puis les utiliser dans `_shop_product_cards.scss` (et éventuellement `_shop.scss` / `_shop_sidebar.scss`), **sans** remplacer immédiatement `$marketone-primary` partout le site.

---

## 5. Ce que je propose de ne pas faire dans ce palier

- Refonte complète de la palette sur tout le module (home, fiche produit, panier).
- Ajout de décoratif (traits or, rose, multiples accents sur une carte).
- Réintroduction de `multiply` sans test MOA ciblé packshots vs lifestyle.
- Modifier filtres, contrôleurs, QWeb fonctionnel UX-1/UX-2.
- Promettre une homogénéisation image par CSS seul (doctrine §7 = pipeline média).

---

## 6. Variantes pour recette MOA (3 rendus comparables)

À produire sur `ckr-marketone-01`, même jeu de produits, captures côte à côte.

| Variante | Carte | Image | Hover | Prix | Intent |
|---|---|---|---|---|---|
| **A — « Légère »** | Bordure seule, pas d'ombre repos | `#F0E8DC`, ratio **1:1** | Pas de lift ; zoom 1.02 max | `#C4715A` | Maximum chaleur, minimum SaaS |
| **B — « Tenue »** ⭐ | Bordure `#DDD0C2` + ombre repos très légère chaude | `#F0E8DC`, ratio **1:1** | Lift **-2px**, zoom **1.02** | `#C4715A` | **Recommandée** — équilibre doctrine |
| **C — « Encadrée »** | Proche variante douce actuelle mais couleurs CK | `#F0E8DC`, ratio **4:3** | Lift **-3px** | `#C4715A` | Si MOA veut un peu plus de structure |

**Livrable recette** : 3 captures desktop + 1 filtre actif + note sur 2–3 images lifestyle (blend off) + 2 packshots fond blanc (halos acceptables ?).

---

## 7. Fichiers impactés (estimation)

| Fichier | Nature du changement | Priorité |
|---|---|---|
| `static/src/scss/_shop_product_cards.scss` | Cartes, variables Odoo, couleurs CK locales | P0 |
| `static/src/scss/_shop.scss` | Fond page shop, neutralisation legacy `.oe_product` grille | P1 (si MOA valide) |
| `static/src/scss/_shop_sidebar.scss` | Fond sidebar `#EDE3D4` optionnel | P2 — **arbitrage** |
| `static/src/scss/_tokens_colors.scss` | Alias CK seulement | P2 — si stratégie tokens validée |
| `docs/recette/RECETTE_MANUELLE_SHOP_UX3_PRODUCT_CARDS.md` | Grille A/B/C + checklist doctrine | Doc |
| `__manifest__.py` | Bump patch `19.0.15.2.0` après GO visuel | Post-arbitrage |

**Non impactés** : contrôleurs, vues filtres, `shop_sidebar_ux2.xml`, tests régression (sauf ajout smoke couleur optionnel, non bloquant).

---

## 8. Risques identifiés

| Risque | Mitigation |
|---|---|
| Sidebar plus foncée (`#EDE3D4`) vs grille claire → contraste fort | Tester panneau sidebar vs fond page unifié |
| Prix terracotta partout vs chips UX-1 déjà colorés | Vérifier cohérence chips / reset |
| Migration tokens globale | **Reporter** — scope shop uniquement |
| Packshots fond blanc sans `multiply` | Accepter halos légers ou pipeline image futur |
| PR #9 merge prématuré | Maintenir **pause merge** jusqu'à GO visuel variante B (ou A) |

---

## 9. Questions d'arbitrage MOA — historique avant décision

> **Source de vérité** : section **Arbitrages MOA (validés)** ci-dessous.

1. **Palette** : application **UX-3 + `/shop` seulement**, ou mise à jour des tokens globaux dès maintenant ?
2. **Sidebar** : conserver transparent (UX-2 actuel) ou panneau **`#EDE3D4`** ?
3. **Ratio desktop par défaut** : **1:1** (recommandé), **4:3**, ou autre ?
4. **Prix** : terracotta `#C4715A` sur toutes les cartes — confirmé ?
5. **Hover titre** : terracotta sur cartes uniquement, ou aussi liens ailleurs sur `/shop` ?
6. **Carte** : variante **A (légère)**, **B (tenue)** ou **C (encadrée)** comme cible merge ?
7. **`multiply`** : définitivement **off**, ou test optionnel packshots en variante séparée ?
8. **Fond carte** : blanc pur vs **lin `#F5EDE0`** sur toute la surface carte ?
9. **PR #9** : mise à jour avec réserve documentée, ou attente recette A/B/C ?

---

## 10. Plan d'exécution proposé (après réponses MOA)

| Étape | Action | Responsable |
|---|---|---|
| 1 | MOA arbitre questions §9 + choix variante A/B/C | MOA |
| 2 | Implémentation **une seule** variante retenue + alias couleurs CK locaux | Dev |
| 3 | Recette visuelle cycle 4 (grille doctrine + captures) | MOA |
| 4 | GO visuel explicite → bump version → mise à jour PR #9 → merge | MOA + Dev |

**Pas de commit d'intégration** tant que les points 1 et 6 ne sont pas tranchés.

---

## 11. Position sur le process

| Statut | Position |
|---|---|
| GO technique | ✅ Maintenu |
| PR documentée | ✅ PR #9 peut rester ouverte avec bannière « en attente arbitrage DA » |
| GO merge PR #9 | ☑ MOA 2026-05-20 |
| Prochaine livraison | **Cette proposition** → puis **1 variante codée** post-arbitrage |

---

## 12. Synthèse

La base technique (variables Odoo, `contain`, non-régression) est solide.  
Le travail restant est **directionnel** :

- moins de carte SaaS ;
- plus de révélation produit ;
- palette pastel CK maîtrisée ;
- accents dosés.

**Objectif final :** premium vivant, pas catalogue froid.

---

## Arbitrages MOA (validés)

| # | Question | Décision |
|---|---|---|
| 1 | Palette scope | `/shop` uniquement — alias `$ck-*` |
| 2 | Sidebar | Panneau `#EDE3D4` |
| 3 | Ratio | `1:1` |
| 4 | Prix terracotta | Oui `#C4715A` |
| 5 | Hover titre | Cartes uniquement |
| 6 | Variante | **B — Tenue** |
| 7 | `multiply` | Off définitif |
| 8 | Fond carte | Blanc `#fff` |
| 9 | PR #9 | Mise à jour, pas de merge avant recette visuelle |

**Implémentation** : commit post-arbitrage sur `feat/marketone-ux3-product-cards-palier-a`, version `19.0.15.2.0`.

**Recette cycle 4** (2026-05-20) : GO technique + **GO visuel MOA** — 21/21 tests, doctrine CK validée.

**Réserve non bloquante** : séparation image/texte perceptible sur certaines cartes (bandeau fond image) — Palier A clos ; reprise SCSS ou moteur image ultérieur.

**Réserve mobile** : capture 768px non produite ; CSS responsive documenté en recette.

**Merge PR #9** : commit `9b6354d8e377378394fb101c66846c0cbf02b8f9` (2026-05-20).
