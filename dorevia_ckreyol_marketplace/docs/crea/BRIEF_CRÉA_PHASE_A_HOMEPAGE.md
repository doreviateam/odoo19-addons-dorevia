# Brief créatif — Phase A homepage CK

**Objet** : guider la production **créative** (médias, copy hors gel, micro-ajustements visuels) pour la **Phase A** du ticket [TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md](TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md) — **appétence sans déplacer la charpente** (même ordre de blocs dans `ckr_homepage.xml`). **Avant le dev** : checklist **§0** du même ticket (« Prêt pour dev — Phase A »).

**Date** : 2026-04-23  
**Statut** : **brief de travail gelé** pour l’exécution Phase A — à réviser uniquement par décision MOA ou nouveau ticket.

---

## 1. Documents de vérité (ordre de lecture)

| Priorité | Document | Rôle |
|----------|----------|------|
| 1 | [TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md](TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md) | Périmètre Phase A, gels techniques, critères d’acceptation |
| 2 | [PLATEFORME_MARQUE_CK_V1.md](PLATEFORME_MARQUE_CK_V1.md) | Ton, promesse, personnalité, ce qu’il faut éviter (folklore, sur-promesse) |
| 3 | [CADRAGE_DESIGN_CREATION_CK_V1.md](CADRAGE_DESIGN_CREATION_CK_V1.md) | Ambition perçue, densité, rythme §11, images §14, critères échec §19 |
| 4 | [SPEC_HERO_HOMEPAGE.md](../SPEC_HERO_HOMEPAGE.md) §7 | **Copy hero gelé** (titre, sous-texte, CTA) — Phase A **ne change pas** le texte hero sans amendement SPEC |
| 5 | [BRIEF_VISUEL_HERO_PHASE1.md](../BRIEF_VISUEL_HERO_PHASE1.md) | Production du **visuel hero** (ratios, ambiance, livrables) |
| 6 | [PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md](PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md) §9 | Gels layout / composants V1 |
| 7 | [CHARTE_GRAPHIQUE_PHASE1.md](../CHARTE_GRAPHIQUE_PHASE1.md), [DIRECTIONS_ARTISTIQUES_PHASE1.md](../DIRECTIONS_ARTISTIQUES_PHASE1.md) | Palette, typo, photo, interdits |

---

## 2. Périmètre Phase A (rappel)

**Inclus**

- **Médias** : hero, supplier, sélection (et tout visuel déjà présent dans ces blocs) — cohérence lumière, cadrage, ratios ([CADRAGE_DESIGN_CREATION_CK_V1.md](CADRAGE_DESIGN_CREATION_CK_V1.md) §14).
- **Copy** : blocs **non couverts** par le gel SPEC hero (supplier, editorial, titres de section, micro-textes Explorer si hors gel ailleurs) — **une ligne sensorielle ou d’usage** acceptable si elle renforce l’appétence **sans** sur-texte ni ton criard.
- **SCSS** : polish cartes sélection, états hover/focus, **rythme** vertical entre sections (respiration / densité), **sans** violer les arbitrages §9 (hero 60/40, supplier plane, editorial bandeau sobre sans `<h2>`, selection garde-fou, fil rouge).

**Exclus** (autres tickets / phases)

- Réordonnancement des blocs (**Phase B**).
- Nouveaux snippets (portes maîtresses grille, bloc Origines dédié, blog, newsletter) (**Phase C**).
- Refonte menu principal, `/shop`, fiche produit hors contenu déjà visible sur la homepage.

---

## 3. Intention créative Phase A (une phrase)

**Monter le désir perçu par la matière, la cohérence visuelle et des micro-textes sobres** — la promesse hero reste **celle du gel** ; l’appétence se joue surtout sur **images**, **cartes produit**, **supplier**, **éditorial** et **rythme**.

---

## 4. Brief par bloc

### 4.1 Hero

- **Copy** : **conforme [SPEC_HERO_HOMEPAGE.md](../SPEC_HERO_HOMEPAGE.md) §7** — pas de retouche marketing dans le QWeb sans **amendement SPEC** + historique.
- **Visuel** : suivre [BRIEF_VISUEL_HERO_PHASE1.md](../BRIEF_VISUEL_HERO_PHASE1.md) — image **solide** (cadrage §8.1 cadrage design : promesse claire, tenue au site, pas de spectacle vide). Priorité : **matière**, lumière naturelle, continuité avec la charte Direction A.
- **CTA / layout** : inchangés (gel V1 §9).

### 4.2 Explorer (5 portes)

- **Pas de changement structurel** du rail (manuel, ADR-007).
- **Créa** : harmoniser **titres / sous-titres** des cartes porte (lisibilité, même « température » typographique) ; éviter le ton catalogue froid si une **micro-accroche** courte est validée MOA (optionnel, sans alourdir le mobile).

### 4.3 Supplier (mise en avant fournisseur / origine)

- **Levier d’appétence fort** : photo **produit ou atelier** cohérente avec le hero (même famille lumineuse).
- **Copy** : peut porter une **phrase d’usage** ou de **transmission** (goût, savoir-faire, territoire) — **pas** folklore, **pas** sur-promesse logistique ([PLATEFORME_MARQUE_CK_V1.md](PLATEFORME_MARQUE_CK_V1.md) §10).
- **Layout** : variante **plane** gelée §9 — pas de chevauchement type « magazine » en Phase A.

### 4.4 Sélection produits

- **Nombre** : privilégier **peu de références très bien montrées** (cadrage §8.5) si le choix produit est côté contenu ; côté technique, respecter le gabarit existant.
- **Images catalogue** : même direction que §14 — pas de mélange brut de ratios et de styles de fond.
- **SCSS** : renforcer la **désirabilité** des cartes (ombre légère, hover, focus visible) **dans** les tokens existants ; ne pas casser le **garde-fou** responsive (ellipsis, baseline prix — §9.4).

### 4.5 Éditorial (bandeau sobre)

- **Copy** : cœur de la **profondeur de marque** en une phrase + lien — ton **chaleureux, clair, cultivé sans lourd** (plateforme §9–§10).
- **Visuel** : optionnel minimal ; pas de retour aux tuiles overlay sombre (gel §9.3).
- **Pas de `<h2>`** : gel V1 — ne pas introduire de niveau de titre supplémentaire pour « styliser ».

### 4.6 Confiance (Trust)

- **Court et immédiat** (cadrage §8.3) : icônes + libellés **compris en une lecture** ; renforcer si besoin la **preuve de sélection** (fabrication, soin) **sans** paragraphe long.

---

## 5. Direction photographique (synthèse)

- **Cohérence** : une « température » de lumière et de colorimétrie d’un bout à l’autre de la homepage (cadrage §14).
- **Sujets** : matière, produit, geste de fabrication ou de dégustation **sobre** ; éviter le décor exotique cliché (charte / plateforme).
- **Formats** : respecter les **ratios** prévus par les snippets ; pas d’images compressées ou floues sur le hero.

---

## 6. Livrables Phase A (checklist)

- [ ] Assets hero finalisés selon `BRIEF_VISUEL_HERO_PHASE1.md` (ou brief équivalent signé).
- [ ] Assets supplier + sélection (liste fichiers / URLs Odoo documentée pour intégration).
- [ ] Copy révisée **hors SPEC hero** validée MOA (fichier ou table dans la PR).
- [ ] Patch SCSS (fichiers touchés listés) **sans** régression §9.
- [ ] Captures **desktop + mobile** pour recette ; mention des points §6 du ticket.
- [ ] [PV_RECETTE_PHASE_A_HOMEPAGE_CK.md](PV_RECETTE_PHASE_A_HOMEPAGE_CK.md) complété (verdict, gels, blocs, décision §13).

---

## 7. Critères de « succès » créatif (MOA)

1. La page donne une impression plus **construite** et plus **désirable** (cadrage §20 — synthèse ressentie).
2. Aucun glissement vers **folklore**, **surcharge promo** ou **sur-promesse** (plateforme + §19 cadrage).
3. Le hero reste **conforme SPEC §7** ou la SPEC a été **amendée officiellement** avant mise en ligne.

---

## 8. Historique du document

| Date | Changement |
|------|------------|
| 2026-04-23 | Création — brief Phase A aligné ticket `HOMEPAGE-APPETENCE-PARTITION-V1`, plateforme, cadrage design, gels SPEC hero + PROPOSITION §9. |
| 2026-04-23 | Lien vers [PV_RECETTE_PHASE_A_HOMEPAGE_CK.md](PV_RECETTE_PHASE_A_HOMEPAGE_CK.md) dans les livrables (recette MOA). |
| 2026-04-23 | Renvoi vers le ticket **§0** (checklist « prêt pour dev » Phase A). |
