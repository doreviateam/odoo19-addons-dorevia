# P4 — Audit & propositions « Header enseigne CK »

| Champ | Valeur |
| --- | --- |
| Date | 2026-06-23 |
| Déclencheur | Benchmark MOA bienmanger.com — P3 jugé « techniquement propre, mieux structuré, mais en dessous en perception boutique mature » |
| Périmètre | 2 pistes visuelles prototypes, non commitées — destinées à arbitrage MOA avant implémentation définitive |
| Hors périmètre | Architecture MOA V2.2, profondeur catalogue, contenu seed |
| Référence (état actuel commité) | [`ACTE_MOA_VALIDATION_DIRECTION_HEADER_V22_P1_P2_P3.md`](ACTE_MOA_VALIDATION_DIRECTION_HEADER_V22_P1_P2_P3.md) — P1/P2/P3 validés en direction, codebase inchangée par ce document |
| Modules (état actuel, inchangé) | `dorevia_ck_theme` `19.0.1.45.0` · `dorevia_ck_marketone_content` `19.0.1.30.0` |

---

## 0. Méthode

Les deux pistes ci-dessous ont été **réellement implémentées et capturées** sur l'instance de recette (pas des maquettes statiques), puis **intégralement retirées** du code après captures — restauration vérifiée identique à l'état P3 validé (diff propre sur `website_header.scss` et `nav_mega_menu.py`). Aucune des deux pistes n'est présente dans le code actuel : ce document sert à l'arbitrage, pas à la livraison.

Captures dans `captures/recette_header_v22/p4/` (`piste_a_*.png`, `piste_b_*.png`). Référence neutre P3 dans `captures/recette_header_v22/p3/after_*.png`.

---

## 1. Diagnostic — les 4 constats MOA traduits techniquement

| Constat MOA | Lecture technique aujourd'hui (P3 validé) |
| --- | --- |
| 1. Présence d'enseigne insuffisante | Logo = wordmark seul, aucun repère graphique secondaire ; N2 et N3 lues comme deux barres successives propres, pas comme un seul bloc d'identité |
| 2. Profondeur catalogue peu perceptible dès le menu | Vraie — mais structurelle (seed pauvre, hors Dev, cf. §15 du livrable V2.2) ; ce que P4 peut faire : donner au mega-menu une **respiration éditoriale** qui suggère la richesse même quand le contenu métier est limité |
| 3. Mega-menus = listes de liens, pas éditorial | Le fallback texte P3 (carte avec titre Fraunces + tagline) reste sobre — pas de matière visuelle (image, texture) |
| 4. Preuves de confiance peu visibles | Les preuves CK existent (bandeau N1, trust badges homepage) mais ne **réapparaissent jamais** au niveau du mega-menu, là où l'intention d'achat se précise |

---

## 2. Deux pistes — partagé vs différenciant

**Élément partagé aux deux pistes (gain peu risqué, indépendant du choix de direction) :**

Bandeau de preuves CK en pied de chaque mega-menu rayon (desktop uniquement) : *Origines identifiées · Expédié depuis Nantes · Sélection créole*. Reprend des formulations déjà existantes (bandeau N1), aucune nouvelle promesse inventée — conforme à la contrainte « pas de gros chiffres inventés ».

**Ce qui distingue les deux pistes :** intensité du parti pris sur les axes 1 (logo), 2 (bloc N2/N3) et 3 (mega-menu éditorial).

---

### Piste A — « Enseigne affirmée »

Parti pris le plus proche, en intensité, de ce qui fait l'effet bienmanger.com — sans son registre sombre/corporate.

| Axe | Traitement |
| --- | --- |
| Logo | Wordmark agrandi (1.3125rem → 1.5rem) + macaron rond terracotta « CK » accroché au wordmark |
| N2/N3 | **Fusion en une seule plaque** : tout le header (N2+N3) reçoit la teinte `$ck-bg-soft`, le séparateur entre les deux lignes disparaît — lecture en un seul bloc d'enseigne |
| Mega-menu | Fallback colonne 4 en **photo produit réelle** (catalogue déjà publié, pas d'asset inventé) avec dégradé sombre + titre/tagline en blanc — registre « bannière éditoriale » |
| Preuves | Bandeau de preuves partagé (cf. §2) |

**Captures :** `piste_a_desktop_initial.png` · `piste_a_mega_epicerie.png` · `piste_a_mega_boissons.png` · `piste_a_mobile_ferme.png`

**Lecture :** l'effet « enseigne » est net dès le chargement — le bloc unifié et le macaron donnent un signal de marque plus fort immédiatement. Le mega-menu Épicerie (seed pauvre) gagne nettement en présence grâce à la photo, qui « raconte » le rayon même avec une seule colonne métier réelle.

**Point d'attention mobile (constaté, pas supposé) :** le macaron logo reste actif sur mobile en l'état du prototype et entre en proximité visuelle avec l'icône recherche dans le chrome compact — **nécessiterait un traitement desktop-only ou une taille réduite** avant toute implémentation définitive, pour respecter la contrainte « mobile maîtrisé ».

---

### Piste B — « Éditorial créole »

Parti pris plus retenu, qui densifie la structure en 2 bandes déjà actée en P3 plutôt que de la fusionner.

| Axe | Traitement |
| --- | --- |
| Logo | Pas de macaron — un simple **trait terracotta** sous le wordmark, signature discrète |
| N2/N3 | Les deux bandes restent **distinctes** (pas de fusion) ; la ligne N3 reçoit une bordure d'accent terracotta (2px) en haut — ancrage plus posé, sans alourdir |
| Mega-menu | Fallback colonne 4 en **texture CSS illustrative** (motifs radiaux ton sur ton terracotta/vert CK) — pas de photo, registre plus abstrait/artisanal, tagline en italique |
| Preuves | Bandeau de preuves partagé (cf. §2) |

**Captures :** `piste_b_desktop_initial.png` · `piste_b_mega_epicerie.png` · `piste_b_mega_boissons.png` · `piste_b_mobile_ferme.png`

**Lecture :** effet plus subtil que la piste A — le gain de présence est réel mais moins immédiat. En contrepartie, le rendu reste très proche de l'identité déjà validée (moins de risque de « dénaturer CK »), et l'impact mobile est quasi nul (trait fin, à peine perceptible) — **conforme nativement à la contrainte mobile maîtrisé**, sans ajustement nécessaire.

---

## 3. Comparatif synthétique

| Critère | Piste A — Enseigne affirmée | Piste B — Éditorial créole |
| --- | --- | --- |
| Intensité de l'effet « boutique mature » | Forte, immédiate | Modérée, plus progressive |
| Proximité avec le registre bienmanger (intensité, pas style) | Plus proche | Plus éloignée |
| Risque de dénaturer l'identité CK actuelle | Moyen (fusion de bloc + macaron = changement perceptible) | Faible (ajustements ponctuels) |
| Dépendance à du contenu (photo produit réelle) | Oui — fonctionne grâce au catalogue déjà publié, mais lie visuellement le rayon à *un* produit précis | Non — texture générique, aucune dépendance contenu |
| Impact mobile constaté | Réel, à corriger avant implémentation (macaron) | Quasi nul, déjà conforme |
| Effort d'implémentation définitive | Moyen (gestion d'image par rayon à prévoir, BO ou config) | Faible (CSS uniquement) |

---

## 4. Conformité aux contraintes posées

| Contrainte | Respect |
| --- | --- |
| Ne pas copier BienManger | OK — aucune des deux pistes ne reprend leur registre sombre/corporate ; seuls les *principes* (contraste, ancrage, surface) sont retenus |
| Rester dans le registre CK | OK — Fraunces, terracotta, crème conservés dans les deux pistes |
| Ne pas rouvrir l'architecture MOA V2.2 | OK — aucun changement de structure 3 niveaux, de comportement de menu, ni de règle d'intensité (§4 du livrable) |
| Ne pas créer de fausse profondeur catalogue | OK — le fallback (texte, photo ou texture) ne simule aucune sous-catégorie ni produit qui n'existe pas ; la photo piste A est un produit réellement publié |
| Garder le mobile maîtrisé | **Partiellement** — Piste B conforme nativement ; Piste A nécessite un correctif (macaron desktop-only) avant validation finale |

---

## 5. Recommandation

Aucune des deux pistes n'est présentée comme *la* solution — elles bornent un **spectre d'intensité** (affirmée vs retenue) pour faciliter l'arbitrage MOA. Une voie hybride est également possible et techniquement simple : reprendre le bloc N2/N3 fusionné et la photo mega-menu de la **piste A** avec le traitement logo plus discret de la **piste B** (sans macaron), ce qui limiterait le risque mobile tout en gardant l'essentiel de l'effet « enseigne ».

**Ce document n'engage aucune implémentation.** Dans l'attente de votre arbitrage (piste A, piste B, hybride, ou nouvelle itération), le code reste sur la base P1/P2/P3 validée.

---

## 6. Prochaine étape suggérée

1. Arbitrage MOA sur la direction (A / B / hybride).
2. Si Piste A ou hybride retenue : trancher le mode de gestion de l'image mega-menu (produit phare désigné en config, ou nouveau champ BO dédié — à ne pas confondre avec la colonne 4 `ck.mega.menu.visual.block` existante, réservée aux campagnes).
3. Implémentation définitive + correctif mobile si Piste A retenue.
4. Captures officielles + recette MOA finale.
