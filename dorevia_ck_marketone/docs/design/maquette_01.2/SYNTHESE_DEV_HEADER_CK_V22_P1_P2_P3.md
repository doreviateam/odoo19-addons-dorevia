# Synthèse Dev — Header & Mega-menus C-Kréyòl V2.2 (P1 → P2 → P3 pilote)

| Champ | Valeur |
| --- | --- |
| Projet | `dorevia_ck_marketone` (+ `dorevia_ck_theme`, `dorevia_ck_marketone_content`) |
| Objet | Retrace, justifie et documente les trois lots de correctifs/améliorations menés sur le Header V2.2 entre le GO technique initial et la recette visuelle MOA |
| Modules | `dorevia_ck_theme` **19.0.1.45.0** · `dorevia_ck_marketone_content` **19.0.1.30.0** |
| Documents associés | [`LIVRABLE_MOA_HEADER_CK_V2_2.md`](LIVRABLE_MOA_HEADER_CK_V2_2.md) (spec/architecture) · [`P2_AUDIT_HEADER_V22.md`](P2_AUDIT_HEADER_V22.md) · [`P3_RECETTE_VISUELLE_HEADER_V22.md`](P3_RECETTE_VISUELLE_HEADER_V22.md) (verdict P3, **GO directionnel**) |
| Environnement de vérification | `dorevia_ck_marketone_01` · `http://localhost:18079` |

---

## 0. Pourquoi ce document

Le Header V2.2 avait reçu un **GO technique** (41/41 tests, comportements fonctionnels conformes à la spec MOA) mais pas de **GO MOA visuel** : la recette qualitative a révélé un écart entre « fonctionnellement conforme » et « visuellement convaincant ».

Trois lots de travail ont suivi, chacun déclenché par un retour MOA précis, chacun vérifié par la preuve (mesures DOM réelles, échantillonnage pixel, captures avant/après) plutôt que par relecture de code seule. Ce document :

1. retrace **ce qui ne allait pas** et **pourquoi**, techniquement ;
2. explique **ce qui a été corrigé** et **pourquoi ce choix précis** plutôt qu'une autre option ;
3. donne les **preuves de vérification** associées à chaque affirmation ;
4. cadre **ce qui reste ouvert**.

---

## 1. P1 — Le mega-menu desktop ne portait pas la grammaire 4 colonnes

### 1.1 Constat MOA

> « Le sujet n'est pas seulement *il manque du contenu*. Le sujet est : est-ce que le layout livré peut porter la promesse visuelle de la spec ? »

Les captures officielles montraient un mega-menu réduit à un petit encart de 320 px collé au bord du header, quel que soit le rayon — y compris quand le rayon avait plusieurs colonnes de contenu disponibles.

### 1.2 Cause racine — bug 1 : largeur plafonnée à 320 px

`website_header.scss` définissait, pour les dropdowns N3 simples (Espace pro, Nos producteurs) :

```scss
#top_menu.top_menu .dropdown-menu {
    min-width: 220px;
    max-width: 320px;
}
```

Le panneau mega-menu (`.o_mega_menu`) porte **aussi** la classe Bootstrap `.dropdown-menu` — ce sélecteur générique le capturait également. Résultat mesuré en live : panneau rendu à `width: 320px`, quel que soit le nombre de colonnes alimentées. **Même avec Coffrets, Épicerie complète et colonne 4 enrichis, le panneau serait resté plafonné à 320 px.** Le manque de contenu seed aggravait le symptôme mais n'en était pas la cause.

**Correctif :** exclusion explicite (`:not(.o_mega_menu)`) + règle dédiée donnant au panneau une largeur réelle bornée au container éditorial (`$ck-container-max`, 1200px), centrée.

**Pourquoi ce choix plutôt qu'une réécriture du composant :** le mécanisme Odoo natif (`o_mega_menu_container_size`) est une option de l'éditeur de menus, pas un attribut qu'on peut poser depuis du HTML généré côté Python (`mega_menu_content`). Reproduire son effet en CSS scopé au thème CK évite de toucher au modèle `website.menu` ou au pipeline de génération HTML — risque et surface de changement minimaux pour un bug de layout pur.

**Preuve :** mesure DOM live, largeur `320px → 1200px`, centré (`x:40 → 1240` sur viewport 1280px).

### 1.3 Cause racine — bug 2 : recouvrement de la ligne N3

Une fois la largeur corrigée, la MOA a signalé un second défaut : *« le panneau mega-menu recouvre la navigation N3 »*. Bug bloquant distinct du premier, découvert seulement après correction du premier (la largeur de 320 px masquait visuellement le chevauchement).

**Cause racine (5 points vérifiés) :**

| Point d'inspection | Constat |
| --- | --- |
| `top` réel appliqué | Aucun — jamais fixé explicitement |
| Parent de positionnement effectif | Le `<nav>` Odoo englobant **N2 et N3 ensemble**, pas la ligne N3 seule |
| z-index | 1000 sur le panneau, 1030 sur le header — non en cause (le problème était vertical, pas un conflit d'empilement) |
| Héritage `.dropdown-menu` | `data-bs-display="static"` désactive Popper.js → aucun `top`/`inset` n'est injecté automatiquement |
| Ancrage correct visé | Le containing block doit être la ligne N3 elle-même, pas le bloc N2+N3 |

Sans `top` explicite, le navigateur utilise la position « hypothétique » par défaut d'un élément `position:absolute` — celle qu'il aurait eue dans le flux normal, c'est-à-dire au niveau du lien survolé, donc **dans** la ligne N3 plutôt qu'après elle.

**Correctif :** `.ck-header__nav-row` (la ligne N3) reçoit `position: relative` pour devenir le containing block du panneau ; le panneau reçoit `top: 100%` (juste sous N3).

**Preuve :** mesure DOM live, `panel.top === navRow.bottom` exactement, sur Épicerie et Boissons, en haut de page et après scroll (header sticky) — aucun chevauchement constaté dans aucun état testé. Captures officielles `recette_header_v22/03_mega_e_picerie.png` et `04_mega_boissons.png` régénérées en conséquence.

### 1.4 Pourquoi défendre ces deux correctifs comme un seul lot P1

Les deux bugs partagent la même nature : **du CSS Bootstrap générique (`.dropdown-menu`, position absolue sans ancrage) appliqué sans distinction à un composant qui a des besoins de layout différents (mega-menu pleine largeur vs dropdown simple)**. Les corriger ensemble, avec la même méthode (exclusion ciblée + règle dédiée scopée), évite d'introduire deux mécanismes de positionnement concurrents.

---

## 2. P2 — Hiérarchie visuelle N2/N3

### 2.1 Constat

Après P1, le header était structurellement correct mais perçu comme « plat » : pas de hiérarchie perceptible entre rayons catalogue / sélections commerciales / entrées relationnelles, alors que la spec MOA (§3.3 du livrable) prévoit explicitement trois groupes visuellement distincts.

### 2.2 Audit avant P2 (extrait)

| Axe | Constat |
| --- | --- |
| Hauteur | Empilement N1+N2+N3 plus haut que nécessaire |
| N2 | Recherche dominante (36rem), panier en pill large — déséquilibre face à « Se connecter » |
| N3 | Tous les liens au même poids visuel ; **double séparateur** (Maison **et** Artisanat portaient tous deux `ck-nav-n3-group-end`, brouillant la lecture des groupes) |
| Espace pro | Pill aussi imposante que le panier — deux CTA en concurrence |
| Mega-menu | Panneau correct en largeur mais sans traitement « carte » (pas de bordure/ombre propre) |

### 2.3 Décisions retenues (12 ajustements SCSS ciblés)

Compacité (hauteur N2/N3 réduite de ~8–12px), recherche resserrée (36rem → 32rem), panier moins dominant (pill plus sobre, fond 4% au lieu de 6–10%), **rayons en poids 500/muted vs sélections en semibold/texte plein** (lecture immédiate du groupe), **séparateur unique** corrigé via `:has()` (un seul trait après le dernier rayon, plus de double trait), Nos producteurs renforcé (confiance), pill Espace pro adoucie (secondaire vs panier), mega-menu traité en carte (bordure/ombre/padding), drawer mobile avec respiration inter-groupes.

**Défense du choix :** aucun changement fonctionnel ni de spec MOA — uniquement des ajustements de poids typographique, couleur et espacement dans `website_header.scss`. La doctrine MOA §4 (« règle d'intensité des menus ») distingue déjà rayons / sélections / relationnel par leur **comportement** ; P2 fait porter cette distinction déjà actée dans le **rendu visuel**, ce qui n'est pas une réouverture de l'architecture mais sa traduction graphique manquante.

### 2.4 Incident de méthode (transparence)

Lors de la première recette des captures avant/après P2, la paire `mega_epicerie` s'est révélée fausse : le script de capture (`ck_h22_p2_captures.mjs`) n'attendait qu'un délai fixe après le survol, sans vérifier que le panneau s'était réellement ouvert (`.show`). Le `before` montrait par erreur l'état pré-P1 (320 px), le `after` montrait le header fermé. Corrigé en ajoutant une assertion explicite sur la classe `.show` et la largeur réelle avant capture — appliqué au script officiel pour fiabiliser les relances futures.

**Preuve :** paires `before_/after_desktop_initial.png`, `before_/after_desktop_scroll.png`, `before_/after_mega_epicerie.png`, `before_/after_mobile_drawer.png` dans `captures/recette_header_v22/p2/`.

---

## 3. P3 pilote — De « techniquement propre » à « visuellement signé CK »

### 3.1 Constat MOA

> « L'ensemble reste visuellement trop sage / pas assez affirmé […] il doit davantage porter l'identité C-Kréyòl et donner une impression d'enseigne e-commerce mature. »

Six axes ont été identifiés (logo/baseline, N2, recherche, hiérarchie N3, mega-menu éditorial, anti-générique). La MOA a choisi de **piloter sur 2 axes** avant de généraliser, pour ne pas rouvrir toute l'identité d'un coup.

### 3.2 Benchmark — méthode et limite assumée

Étude du header bienmanger.com (bloc de couleur plein, bouton de recherche en aplat, nav N3 sur bande colorée, logo à signature graphique). **Choix défendu :** traduire les *principes* (contraste, ancrage visuel, surfaces différenciées) dans le **registre CK existant** (Fraunces, terracotta, crème) plutôt que copier le registre sombre/corporate de la référence — un header CK en charte graphique bienmanger romprait l'identité de marque déjà validée en V1/V2.

### 3.3 Axe 1 — Surfaces N2/N3 différenciées + recherche en aplat

**Décision :** la ligne N3 porte une bande teintée (`$ck-bg-soft`) full-bleed plutôt que du blanc sur blanc ; le bouton de recherche passe d'un contour discret à un aplat `$ck-primary`.

**Incident technique rencontré et corrigé :** la première implémentation (pseudo-élément `::before` en `z-index:-1`) restait invisible — vérifié par échantillonnage pixel direct (`(255,255,255)` au lieu de la teinte attendue). Cause : `.ck-header__nav-row` n'avait que `position: relative`, sans valeur de `z-index` ; elle ne créait donc pas son propre contexte d'empilement local, et le pseudo-élément `z-index:-1` se positionnait dans le contexte du `<header>` sticky — où il passait **derrière** le `<nav>` Odoo non positionné (contenu de flux normal, peint au-dessus des descendants à z-index négatif), qui a son propre fond blanc opaque. Correctif : `z-index: 0` ajouté sur `.ck-header__nav-row` pour que ce conteneur devienne lui-même la racine du contexte d'empilement local.

**Pourquoi documenter ce détail :** c'est un piège CSS classique (z-index négatif + absence de contexte d'empilement local) qui aurait pu repasser inaperçu en relecture de code — seule la vérification pixel l'a révélé.

**Preuve :** échantillonnage pixel, bande N3 `(255,255,255) → (245,240,232)` (= `$ck-bg-soft` exact) ; bouton recherche `(255,255,255) → (216,67,21)` (= `$ck-primary` exact).

### 3.4 Axe 2 — Fallback éditorial CK pour le mega-menu

**Constat :** sur seed pauvre, la colonne 4 (bloc visuel BO) est vide faute de contenu saisi — le mega-menu Épicerie n'affichait qu'une seule colonne de liens, donnant une impression de panneau quasi vide malgré sa largeur correcte (P1).

**Décision :** `nav_mega_menu.py::_visual_column` génère désormais une **carte de marque CK** (eyebrow + titre Fraunces + tagline par rayon) quand aucun bloc BO n'est saisi, au lieu de renvoyer une colonne vide. Résultat : Épicerie passe de 1 à 2 colonnes visibles, Boissons de 2 à 3.

**Pourquoi ce choix plutôt qu'exiger la saisie BO en amont :** la saisie de blocs visuels par rayon est une charge éditoriale récurrente (campagnes, images, dates de validité) qui ne sera jamais garantie à 100 % en permanence. Un fallback générique, sans dépendance image, assure que le mega-menu ne retombe **jamais** à l'état « liste de liens nue », quel que soit l'état du contenu opérationnel — la colonne 4 éditée par l'équipe contenu reste prioritaire et remplace le fallback dès qu'elle existe (`_get_visual_block` inchangé).

**Réserve assumée, non bloquante :** sur Épicerie (1 seule colonne métier), le panneau garde un espace vide à droite du fallback — acceptable pour le pilote, renvoyé en P3 bis si la MOA souhaite un traitement spécifique des rayons à colonne métier unique (cf. `P3_RECETTE_VISUELLE_HEADER_V22.md` §Réserve).

**Preuve :** captures `before_/after_mega_epicerie.png`, `before_/after_mega_boissons.png` dans `captures/recette_header_v22/p3/`.

### 3.5 Mobile — non impacté, vérifié

Les deux axes sont scopés `@media (min-width: 992px)` / `d-none d-lg-block`. Capture `before_/after_mobile_ferme.png` strictement identique — confirmé, pas seulement supposé.

### 3.6 Verdict

**GO directionnel P3 pilote**, acté dans `P3_RECETTE_VISUELLE_HEADER_V22.md`. Axes restants en **P3 bis** : logo/baseline, accent actif terracotta, Fraunces étendu aux titres de colonnes mega-menu, micro-polish, variante de fallback pour rayon à colonne unique.

---

## 4. Méthode — comment chaque affirmation de ce document a été vérifiée

Principe appliqué tout au long des trois lots : **ne jamais conclure sur la seule lecture du SCSS/Python**, toujours vérifier l'état réellement rendu.

- **Mesures DOM live** (Playwright `getBoundingClientRect`, `getComputedStyle`) pour largeur, position, z-index — pas une supposition basée sur le code source.
- **Échantillonnage pixel direct** (PIL) pour confirmer qu'une couleur déclarée en CSS est réellement peinte à l'écran (a débusqué le bug de contexte d'empilement §3.3).
- **Cycles avant/après contrôlés** : sauvegarde de l'état courant, retour temporaire à l'état précédent (P1-only, ou pré-P3), capture, restauration exacte vérifiée par `diff` byte-à-byte, re-capture — pour garantir que les paires avant/après comparent bien deux états réels du code, pas une reconstruction approximative.
- **Correction des scripts de preuve eux-mêmes** quand ils se sont révélés défaillants (§2.4), plutôt que de tolérer une preuve non fiable.

---

## 5. Récapitulatif des fichiers modifiés

| Fichier | Rôle dans P1/P2/P3 |
| --- | --- |
| `dorevia_ck_theme/static/src/scss/website_header.scss` | Largeur/ancrage mega-menu (P1), hiérarchie N2/N3 (P2), surfaces différenciées + recherche + style fallback (P3) |
| `dorevia_ck_marketone_content/nav_mega_menu.py` | Fallback éditorial colonne 4 (P3) |
| `dorevia_ck_marketone_content/migrations/19.0.1.30.0/post-migrate.py` | Re-sync navigation après ajout du fallback (P3) |
| `dorevia_ck_marketone/docs/design/maquette_01.2/scripts/ck_h22_recette_qa.mjs` | Captures officielles régénérées post-P1 |
| `dorevia_ck_marketone/docs/design/maquette_01.2/scripts/ck_h22_p2_captures.mjs` | Bug d'assertion `.show` corrigé (§2.4) |

---

## 6. État actuel et prochaines étapes

| Jalon | Statut |
| --- | --- |
| P1 — largeur + ancrage mega-menu | **Corrigé et vérifié** |
| P2 — hiérarchie N2/N3 | **Livré et vérifié** |
| P3 pilote — surfaces + fallback éditorial | **GO directionnel MOA** |
| P3 bis — logo/baseline, accent actif, Fraunces étendu, micro-polish | **À planifier** |
| Contenu seed (Coffrets, Épicerie complète, ≥3 familles Artisanat) | **Hors périmètre Dev**, action MOA/Contenu — cf. `LIVRABLE_MOA_HEADER_CK_V2_2.md` §15 |
| GO MOA final Header V2.2 | **En attente** — conditionné à P3 bis et/ou enrichissement du contenu seed |
