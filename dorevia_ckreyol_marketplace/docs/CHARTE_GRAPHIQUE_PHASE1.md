# CHARTE_GRAPHIQUE_PHASE1 — C-Kreyol

**Charte graphique minimale** pour la **Phase 1** du canal **C-Kreyol** (site Odoo 19 CE). Elle ne remplace pas une **charte d’agence** complète à terme ; elle **bloque** le minimum nécessaire pour assurer la **cohérence** du **hero**, du **menu**, du **footer** et du **thème** sans refonte permanente.

**Documents liés** : [BRIEF_SYNTHETIQUE_CK.md](BRIEF_SYNTHETIQUE_CK.md), [DIRECTIONS_ARTISTIQUES_PHASE1.md](DIRECTIONS_ARTISTIQUES_PHASE1.md) (direction **A** recommandée — base avant gel charte), [BRIEF_VISUEL_HERO_PHASE1.md](BRIEF_VISUEL_HERO_PHASE1.md) (production **visuels** hero), [DESIGN.md](DESIGN.md) (§14), [SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md), [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md), [STRUCTURE_MENU_PRINCIPAL.md](STRUCTURE_MENU_PRINCIPAL.md), [ARCHITECTURE_DECISION_RECORD.md](ARCHITECTURE_DECISION_RECORD.md) (**ADR-CKR-002** / **ADR-CKR-003**), [NOTE_DE_CADRAGE.md](NOTE_DE_CADRAGE.md), [README](../README.md).

---

## 1. Ordre recommandé (séquence)

1. **Le présent document** — **principe directeur** (§2), **périmètre figé** (§3), détail **§§4–9**, **hors périmètre** (§10), **décision** (§11) ;
2. **[SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md)** — **figer** titre, sous-texte, CTA, **cadre** visuel **aligné** sur la charte ;
3. **Implémentation** thème / assets Odoo (dans le respect [ADR-CKR-002](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-002) / [ADR-CKR-003](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-003)).

Une **charte étendue** (illustrations, déclinaisons print, social templates, etc.) peut suivre **après** la première mise en ligne si besoin.

---

## 2. Principe directeur Phase 1

La direction artistique retenue pour **C-Kreyol** en Phase 1 est :

**Direction A — « Épicerie fine tropicale »**

*(Issue de [DIRECTIONS_ARTISTIQUES_PHASE1.md](DIRECTIONS_ARTISTIQUES_PHASE1.md), recommandation prioritaire.)*

Cette direction est retenue car elle répond le mieux aux objectifs de Phase 1 :

- perception **retail sérieuse** ;
- chaleur sans folklore ;
- mise en valeur des **produits artisanaux** ;
- cohérence avec l’univers de **La Platine** comme **premier fournisseur** (sans confusion de marque — cf. [SPEC_HERO_HOMEPAGE.md §4](SPEC_HERO_HOMEPAGE.md)) ;
- différenciation nette par rapport à un front-end **Odoo standard** ;
- bonne compatibilité avec une lecture **mobile** claire et un système visuel **maintenable**.

La charte doit soutenir une perception :

- **raffinée** ;
- **terreuse / organique** ;
- **éditoriale** ;
- **chaleureuse** ;
- **sobre** ;
- **non folklorique** — en cohérence avec [DESIGN.md](DESIGN.md) et [NOTE_DE_CADRAGE.md](NOTE_DE_CADRAGE.md).

---

## 3. Périmètre minimal figé pour la Phase 1

| Thème | Décision retenue | Statut |
|--------|------------------|--------|
| **Ton visuel** | Raffiné, organique, éditorial, chaleureux, retail, non folklorique | **Validé** |
| **Logo** | Utilisation sur **fonds clairs** prioritairement ; version **fond sombre** à prévoir si nécessaire ; taille minimale lisible en **header** desktop et mobile ; **zone de respiration** obligatoire autour du logo | **À appliquer** |
| **Palette** | Primaire `#A0522D` ; secondaire `#87A878` ; neutre clair `#F5F1E8` ; neutre foncé `#2C2C2C` ; accent `#D4A373` | **Validé** |
| **Typographie** | Titres : serif éditoriale de type **Playfair Display** (ou équivalent validé) ; corps : sans-serif lisible de type **Inter** | **Validé Phase 1** |
| **Boutons / CTA** | CTA principal **contrasté**, lisible, sobre ; usage prioritaire de la **couleur primaire** ; hover / focus **visibles** ; pas d’effet décoratif superflu | **Validé** |
| **États UI** | Hover, focus, actif, erreur, succès **à décliner** à partir de la palette Phase 1 ; priorité à **lisibilité** et **accessibilité** | **À décliner** |
| **Photographie** | Lumière **naturelle**, textures **réelles**, matières visibles, produits et **transformation** mis en avant ; pas d’imagerie **touristique** | **Validé** |
| **Iconographie** | Icônes **simples**, cohérentes, **discrètes** ; style sobre, trait net, sans effet folklorique | **Validé** |
| **Interdits** | Clichés exotiques cheap ; palmiers / plages / tourisme visuel ; surcharge de couleurs vives ; rendu « **template e-commerce générique** » ; décor trop bavard ; **rendu standard Odoo** trop visible là où la marque doit s’affirmer ([ADR-CKR-003](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-003)) | **Validé** |

---

## 4. Palette Phase 1

### 4.1 Couleurs principales

- **Primaire** — Deep terracotta / baked clay  
  `#A0522D`  
  Usage : CTA principal, accents de marque, éléments d’identité forts.

- **Secondaire** — Sage green / dried foliage  
  `#87A878`  
  Usage : accents secondaires, univers agricole / origine, éléments éditoriaux.

- **Accent** — Golden amber  
  `#D4A373`  
  Usage : ponctuation visuelle, micro-accents, survols légers, détails.

### 4.2 Neutres

- **Fond principal clair** — Warm off-white  
  `#F5F1E8`

- **Texte / contraste fort** — Charcoal  
  `#2C2C2C`

### 4.3 Règle d’usage

Le système visuel doit rester **restreint** :

- peu de couleurs simultanées à l’écran ;
- **neutres dominants** ;
- couleurs de marque utilisées avec **mesure** ;
- priorité à la **lisibilité** et à la **cohérence** plutôt qu’à l’effet décoratif.

---

## 5. Typographie Phase 1

### 5.1 Titres

Direction retenue : **serif éditoriale**, élégante, crédible, liée à l’univers food / maison / sélection.

**Référence Phase 1** :  
- **Playfair Display**  
  ou équivalent validé si besoin technique (cf. note licences dans [DIRECTIONS_ARTISTIQUES_PHASE1.md](DIRECTIONS_ARTISTIQUES_PHASE1.md)).

### 5.2 Corps de texte

Direction retenue : **sans-serif propre**, lisible, **retail-ready**, excellente sur mobile.

**Référence Phase 1** :  
- **Inter**

### 5.3 Règle d’ensemble

- contraste clair entre **titres** et **texte courant** ;
- hiérarchie typographique nette ;
- éviter l’accumulation de **familles** de polices ;
- priorité à la **lisibilité mobile**.

---

## 6. Boutons et CTA

### 6.1 CTA principal

Le CTA principal doit être :

- clairement **visible** ;
- **contrasté** ;
- **simple** ;
- cohérent avec le ton sérieux / chaleureux de la marque.

### 6.2 Principes

- usage prioritaire de la **couleur primaire** ;
- texte lisible sans ambiguïté ;
- hover visible mais **sobre** ;
- focus visible au **clavier** ;
- pas d’effet « bouton gadget ».

### 6.3 CTA secondaire

Le CTA secondaire, s’il existe, doit rester :

- plus **discret** ;
- **complémentaire** ;
- jamais **concurrent** du CTA principal.

---

## 7. Direction photographique

### 7.1 Principes retenus

La photographie Phase 1 doit mettre en valeur :

- les **textures** ;
- les **matières** ;
- la **transformation artisanale** ;
- les produits **réels** ;
- la gourmandise **sobre**.

### 7.2 Références visuelles

À privilégier :

- gros plans produits ;
- textures biscuit / manioc / confiture / pâte ;
- lumière naturelle ;
- surfaces bois, matières brutes, contextes sobres ;
- compositions calmes.

**Références versionnées** : exemple produit (crackers manioc, packaging lisible, fond clair) — [SPEC_HERO_HOMEPAGE.md §3.4](SPEC_HERO_HOMEPAGE.md) ; `docs/assets/exemple_produit_manioc_crackers_la_platine.png`. Moodboard hero macro / matière — [BRIEF_VISUEL_HERO_PHASE1.md §10.2](BRIEF_VISUEL_HERO_PHASE1.md) ; `docs/assets/hero_reference_direction_a_biscuits_confiture.png`. **Banque homepage** (packshots) — [BRIEF_VISUEL_HERO_PHASE1.md §10.3](BRIEF_VISUEL_HERO_PHASE1.md) ; `homepage_maniocookies_sale_la_platine.png`, `homepage_manioc_crackers_sale_ste_anne.png`, `homepage_manioc_pates_mayotte_la_platine.png`.

> Les **packshots homepage** servent de **bibliothèque produit** et de **base catalogue** ; ils ne **remplacent pas** le **visuel hero principal**, qui reste régi par la logique **macro / matière / transformation** (cf. [SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md) et [BRIEF_VISUEL_HERO_PHASE1.md](BRIEF_VISUEL_HERO_PHASE1.md)).

### 7.3 À éviter

- plages ;
- palmiers ;
- imagerie carte postale ;
- folklore visuel ;
- décors artificiellement « caribéens » ;
- photos trop chargées ou **incohérentes** entre elles.

---

## 8. Direction iconographique

L’iconographie doit être :

- **simple** ;
- **lisible** ;
- **discrète** ;
- **cohérente** avec l’ensemble du thème.

À éviter :

- icônes trop décoratives ;
- styles **mélangés** ;
- pictogrammes exotiques **narratifs**.

---

## 9. Application au hero, au menu et au footer

### 9.1 Hero

Le hero doit s’appuyer sur :

- une image forte mais **sobre** ;
- un **contraste** lisible ;
- une hiérarchie **texte / CTA** claire ;
- une sensation de **matière réelle**.

### 9.2 Menu principal

Le menu principal doit refléter :

- la **sobriété** ;
- l’**élégance** ;
- la **lisibilité** ;
- la **différence** avec le standard Odoo ([ADR-CKR-003](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-003)).

### 9.3 Footer

Le footer doit rester :

- **structuré** ;
- **propre** ;
- **discret** ;
- **cohérent** avec le header et le reste du système visuel.

---

## 10. Ce qui peut attendre (hors gel Phase 1 initial)

- déclinaisons **réseaux sociaux** ;
- **print** (flyers, cartes) ;
- **illustrations** complexes ;
- **sous-marques** ou variantes saisonnières élaborées.

---

## 11. Décision cible

**Charte minimale Phase 1 validée** :  
**Direction A — « Épicerie fine tropicale »** retenue comme base visuelle de référence pour **C-Kreyol**.

**Date** : 2026-04-21  
**Version** : Phase 1 — minimale  
**Responsable validation marque** : **[à compléter]**

---

## Historique du document

| Date | Changement |
|------|------------|
| 2026-04-21 | Création : charte **minimale** Phase 1, séquence charte → spec hero → implémentation, tableau périmètre, hors périmètre (ex-§3). |
| 2026-04-21 | **Périmètre** : principe directeur, tableau enrichi (ton visuel, neutres fonctionnels, états UI, iconographie, interdits) ; ordre de travail ; liens **BRIEF**, **DIRECTIONS**. |
| 2026-04-21 | **Gel Phase 1** : **Direction A** retenue ; **§3** périmètre **figé** (palette, typo **Playfair + Inter**, CTA, photo, icono, interdits) ; **§§4–9** détail palette, typo, CTA, photo, icono, hero/menu/footer ; **§11** décision ; fusion avec contenu validé. |
| 2026-04-21 | **§7.2** : renvoi **exemple produit** ([SPEC_HERO_HOMEPAGE.md](SPEC_HERO_HOMEPAGE.md) §3.4, `docs/assets/exemple_produit_manioc_crackers_la_platine.png`). |
| 2026-04-21 | **Documents liés** : **[BRIEF_VISUEL_HERO_PHASE1.md](BRIEF_VISUEL_HERO_PHASE1.md)** (brief production hero). |
| 2026-04-21 | **§7.2** : second fichier **moodboard** hero (`hero_reference_direction_a_biscuits_confiture.png`). |
| 2026-04-21 | **§7.2** : **banque homepage** — 3 **packshots** (lien **BRIEF** §10.3). |
| 2026-04-21 | **§7.2** : phrase de **hiérarchie** — packshots = bibliothèque produit / base catalogue ; **hero** = macro / matière / transformation (liens **SPEC** + **BRIEF**). |
