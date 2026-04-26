# BACKLOG_PHASE_1BIS_FRONT — C-Kreyol

## 1. Objet du document

Ce document recense les **items de polish et de stabilisation** identifiés à l'issue de la **clôture Phase 1 front-end** (cf. [BRIEF_DEV.md](BRIEF_DEV.md) §11, critères d'acceptation validés).

Il sert de **backlog opérationnel** pour le lot **Phase 1bis**, non bloquant pour la revue Phase 1, mais nécessaire avant une mise en production ou un élargissement du périmètre.

Ce n'est **pas un ADR** : aucune décision structurante n'y est prise. Les choix tranchants (accessibilité AA, SEO, perf assets) qui émergeraient de ce lot devront être formalisés à part dans [ARCHITECTURE_DECISION_RECORD.md](ARCHITECTURE_DECISION_RECORD.md) si nécessaire.

---

## 2. Contexte

À la clôture Phase 1 :

- **Header** (logo + menu Option B + utilitaires) : personnalisé, opaque au scroll, lisible.
- **Hero homepage** : titre, lead, CTA, visuel macro.
- **Homepage** : wireframe retail enrichie complet (hero, **Explorer** = cinq portes catalogue, fournisseur, sélection, éditorial, confiance) — doctrine : [ADR-006 à 008](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-006), [WIREFRAME_HOMEPAGE.md](WIREFRAME_HOMEPAGE.md) Bloc 3.
- **Footer** : entièrement personnalisé, bandeau copyright Odoo standard neutralisé.
- **Menus et pages stubs** : créés via `post_init_hook` + migration, purge des entrées natives.
- **SCSS** : tokens (couleurs, typo, espacements), entry point `ckr_main.scss`, compatibilité Dart Sass.
- **Console** : clean (plus d'erreur `topMenu`, plus de bandeau "A css error occured").
- **Mobile web** : utilisable, grilles responsives, burger exposé.

Les items ci-dessous sont **additionnels** : ils ne remettent en cause ni la doctrine (respect Odoo CE 19), ni les livrables validés.

---

## 3. Organisation du backlog

Chaque item est structuré ainsi :

- **Titre court**
- **Zone** (header / hero / homepage / footer / back-office / SEO / perf / accessibilité / documentation)
- **Description** (ce qu'il y a à faire)
- **Critère d'acceptation** (ce qui permet de fermer l'item)
- **Priorité** : `H` (haut), `M` (moyen), `B` (bas)
- **Effort indicatif** : `S` (< 0.5 j), `M` (0.5 – 1 j), `L` (> 1 j)

La priorité est donnée à titre indicatif. L'ordonnancement réel est posé en revue Phase 1bis.

---

## 4. Items — Header

### HDR-01 — Hauteur logo et rythme utilitaires

- **Zone** : header.
- **Description** : ajuster la hauteur du logo et l'espacement entre bloc menu et bloc utilitaires (recherche / compte / panier) selon la charte §9.2 et les proportions visées sur desktop et mobile.
- **Critère d'acceptation** : hauteur logo cohérente avec la grille verticale du header, espacement utilitaires homogène avec les tokens `$ckr-space-*`, pas de saut visuel entre viewports.
- **Priorité** : M
- **Effort** : S

### HDR-02 — État actif menu principal

- **Zone** : header.
- **Description** : harmoniser le traitement visuel de l'entrée de menu active (actuellement soulignement par défaut de lien visité). Trancher entre soulignement plein, barre sous-jacente ou pastille, en cohérence avec la charte §9.2.
- **Critère d'acceptation** : un seul traitement actif visible, identique sur les 6 entrées Option B, stable sur desktop et mobile.
- **Priorité** : M
- **Effort** : S

### HDR-03 — Burger mobile — finition

- **Zone** : header.
- **Description** : vérifier l'animation d'ouverture, la fermeture au clic extérieur, et le focus trap clavier du menu mobile.
- **Critère d'acceptation** : ouverture / fermeture fluides, focus clavier piégé dans le panneau ouvert, restitution au bouton burger à la fermeture.
- **Priorité** : M
- **Effort** : M

---

## 5. Items — Hero

### HRO-01 — Contraste AA lead sur fond crème

- **Zone** : hero / accessibilité.
- **Description** : valider le ratio de contraste du lead (texte gris sombre) sur le fond crème du hero. Ajuster la nuance si sous le seuil AA (4.5:1 pour texte courant).
- **Critère d'acceptation** : ratio ≥ 4.5:1 mesuré sur le lead, pas de régression visuelle sur le titre.
- **Priorité** : H
- **Effort** : S

### HRO-02 — Visuel hero final

- **Zone** : hero / assets.
- **Description** : remplacer le packshot provisoire du hero par le **visuel hero principal** validé (logique macro / matière / transformation, cf. charte §7.2 et [BRIEF_VISUEL_HERO_PHASE1.md](BRIEF_VISUEL_HERO_PHASE1.md)).
- **Critère d'acceptation** : visuel déposé dans `static/src/img/`, référencé dans `ckr_hero.xml`, conforme à la hiérarchie hero vs packshots.
- **Priorité** : H
- **Effort** : S (si visuel livré)

### HRO-03 — Versions responsive du visuel hero

- **Zone** : hero / perf.
- **Description** : fournir au moins deux déclinaisons (desktop ≥ 1600px et mobile ≤ 768px) du visuel hero pour éviter le downscaling lourd sur mobile.
- **Critère d'acceptation** : balises `<picture>` ou `srcset` en place, poids total hero ≤ cible fixée en §8 (perf).
- **Priorité** : M
- **Effort** : M

---

## 6. Items — Homepage (blocs hors hero)

### HOM-01 — Carte "Boutique" mise en avant

- **Zone** : homepage / entrées d'exploration.
- **Description** : décider du traitement de la carte "Boutique" actuellement mise en avant (fond accent + soulignement du titre). Trancher : badge "Actif", simple accent visuel, ou retour à 4 cartes homogènes.
- **Critère d'acceptation** : traitement validé documenté dans [DESIGN.md](DESIGN.md), reflété dans `_entries.scss`.
- **Priorité** : M
- **Effort** : S

### HOM-02 — Bloc fournisseur : partenaire réel

- **Zone** : homepage / éditorial.
- **Description** : remplacer le contenu générique du bloc fournisseur par la fiche éditoriale du premier partenaire validé (nom, portrait, pitch court).
- **Critère d'acceptation** : copy et visuel définitifs en place, conformes à la doctrine "origines réelles, pas de sur-promesse".
- **Priorité** : M
- **Effort** : S (si fiche livrée)

### HOM-03 — Sélection produits : branchement catalogue

- **Zone** : homepage / sélection.
- **Description** : aujourd'hui le bloc sélection affiche des packshots statiques. Évaluer le branchement sur `product.template` (sélection éditoriale tagguée) pour que la homepage reflète le catalogue réel.
- **Critère d'acceptation** : décision prise (statique vs dynamique) et documentée, implémentation alignée si dynamique, en respect de la doctrine "pas de logique métier parallèle".
- **Priorité** : B
- **Effort** : L

### HOM-04 — Bloc éditorial : copy définitive

- **Zone** : homepage / éditorial.
- **Description** : figer la copy du bloc éditorial (actuellement rédactionnelle polishable cf. [BRIEF_DEV.md](BRIEF_DEV.md) §7) après relecture marque.
- **Critère d'acceptation** : copy validée par responsable marque, intégrée dans `ckr_editorial.xml`.
- **Priorité** : M
- **Effort** : S

---

## 7. Items — Footer

### FTR-01 — Pages légales

- **Zone** : footer / contenus statutaires.
- **État (2026-04-25)** : le module livre des pages **publiées** **`/privacy`** (politique de confidentialité), **`/terms`** (mentions légales + **hébergement** sur la page + CGV `#cgv`), liées depuis le **footer** et depuis `/privacy` (renvoi éditeur). Le formulaire **Cercle** pointe vers `/privacy`.
- **Reste à faire** : **validation juridique** des textes et des coordonnées (éditeur, **hébergeur réel** si différent du bloc **OVH SAS** par défaut dans `ckr_terms.xml`, CGV détaillées si requis). Les URLs retenues dans le thème CK sont **`/privacy`** et **`/terms`** (pas `/mentions-legales` / `/confidentialite` séparés).
- **Critère d'acceptation** : contenu **validé** par le responsable légal / MOA ; hébergeur affiché **conforme** au contrat d’hébergement en vigueur.
- **Priorité** : H (pré-requis mise en ligne publique)
- **Effort** : M → **S** pour la partie technique (déjà amorcée) ; **M** pour la relecture métier / juridique.

### FTR-02 — Informations de contact

- **Zone** : footer.
- **Description** : vérifier cohérence entre l'adresse Nantes / La Platine affichée en footer et le `res.company` côté back-office (cf. BAC-01).
- **Critère d'acceptation** : une seule source de vérité, pas de divergence entre footer et e-mails transactionnels.
- **Priorité** : M
- **Effort** : S

---

## 8. Items — Back-office (cohérence minimale)

### BAC-01 — Configuration `res.company`

- **Zone** : back-office.
- **Description** : configurer nom, adresse, logo, e-mail et téléphone de la société "C-Kreyol" dans `res.company` pour que les e-mails transactionnels, devis et factures futurs soient cohérents avec l'identité de marque.
- **Critère d'acceptation** : fiche société complète, logo et couleurs alignés charte §9, cohérent avec le footer.
- **Priorité** : H
- **Effort** : S

### BAC-02 — Utilisateur portail & préférences site

- **Zone** : back-office.
- **Description** : vérifier les préférences du site (`website` : nom, langue par défaut, favicon, domaine public) et la configuration portail client.
- **Critère d'acceptation** : `website.default_lang` = `fr_FR`, favicon C-Kreyol, nom du site = "C-Kreyol".
- **Priorité** : M
- **Effort** : S

---

## 9. Items — SEO

### SEO-01 — Meta homepage et stubs

- **Zone** : SEO.
- **Description** : renseigner `website.meta_title`, `website.meta_description` et Open Graph (`og:title`, `og:description`, `og:image`) sur la homepage et chaque page stub (Offrir, Recettes, Collections, À propos, Contact).
- **Critère d'acceptation** : toutes les pages ont un title et une description uniques et pertinents, OG image par défaut (hero homepage ou déclinaison).
- **Priorité** : M
- **Effort** : M

### SEO-02 — Favicon et touch icons

- **Zone** : SEO / identité.
- **Description** : fournir favicon `.ico`, `apple-touch-icon`, et déclinaisons 32 / 192 / 512 px pour PWA minimale.
- **Critère d'acceptation** : favicon visible dans tous les navigateurs cibles, pas de 404 sur les touch icons.
- **Priorité** : M
- **Effort** : S

### SEO-03 — Robots et sitemap

- **Zone** : SEO.
- **Description** : vérifier `/robots.txt` et `/sitemap.xml` générés par Odoo, s'assurer qu'ils reflètent les pages publiques et excluent les stubs si besoin tant que leur contenu n'est pas finalisé.
- **Critère d'acceptation** : sitemap à jour, robots conforme à la politique d'indexation Phase 1bis.
- **Priorité** : B
- **Effort** : S

---

## 10. Items — Performance

### PRF-01 — `loading="lazy"` sur visuels hors viewport initial

- **Zone** : perf.
- **Description** : appliquer `loading="lazy"` à tous les visuels hors hero (entrées, fournisseur, sélection, éditorial).
- **Critère d'acceptation** : audit Lighthouse confirme réduction du coût initial, pas de régression visuelle.
- **Priorité** : M
- **Effort** : S

### PRF-02 — Formats modernes (webp / avif)

- **Zone** : perf / assets.
- **Description** : convertir la banque packshots et le visuel hero en `webp` (minimum) et `avif` (optionnel), avec fallback `jpg` via `<picture>`.
- **Critère d'acceptation** : poids total homepage réduit d'au moins 30 % versus état Phase 1, LCP ≤ 2.5 s sur connexion "Fast 3G" simulée.
- **Priorité** : M
- **Effort** : M

### PRF-03 — Audit Lighthouse baseline

- **Zone** : perf / documentation.
- **Description** : produire un audit Lighthouse (mobile + desktop) sur la homepage et consigner les scores en état Phase 1bis comme référence.
- **Critère d'acceptation** : rapport consigné dans `docs/` ou annexé, scores baseline connus.
- **Priorité** : B
- **Effort** : S

---

## 11. Items — Accessibilité

### A11Y-01 — Audit contrastes global

- **Zone** : accessibilité.
- **Description** : auditer le contraste AA sur l'ensemble des textes (titres, lead, CTA, cartes, footer), pas seulement le hero (cf. HRO-01).
- **Critère d'acceptation** : aucun texte courant en dessous de 4.5:1, aucun texte large en dessous de 3:1.
- **Priorité** : M
- **Effort** : M

### A11Y-02 — Navigation clavier

- **Zone** : accessibilité.
- **Description** : vérifier que tous les liens, CTA, burger et champs atteignables clavier ont un `:focus-visible` lisible et respectent un ordre de tabulation logique.
- **Critère d'acceptation** : parcours clavier complet homepage + menu sans perte de focus ni élément inaccessible.
- **Priorité** : M
- **Effort** : M

### A11Y-03 — Attributs ARIA header/footer

- **Zone** : accessibilité.
- **Description** : vérifier `role`, `aria-label` et `aria-current` sur la navigation principale, `role="contentinfo"` sur le footer, et `aria-hidden` sur les éléments purement décoratifs.
- **Critère d'acceptation** : pas de warning axe-core bloquant sur header / footer.
- **Priorité** : M
- **Effort** : S

---

## 12. Items — Documentation

### DOC-01 — README module à jour

- **Zone** : documentation.
- **Description** : refléter dans [README.md](../../README.md) la clôture Phase 1 front (statut des blocs, version module, principaux fichiers SCSS / XML).
- **Critère d'acceptation** : section "État du module" ou équivalent à jour, pas de divergence avec la structure réelle.
- **Priorité** : M
- **Effort** : S

### DOC-02 — Journal des polish Phase 1bis

- **Zone** : documentation.
- **Description** : au fil de la Phase 1bis, tenir à jour une section "Historique" dans ce backlog, avec les items fermés et leur date.
- **Critère d'acceptation** : chaque item fermé est tracé (date, commit ou référence).
- **Priorité** : B
- **Effort** : continu

---

## 13. Synthèse priorités

| Priorité `H` (pré-requis mise en ligne) | Priorité `M` (polish attendu avant élargissement) | Priorité `B` (amélioration continue) |
|---|---|---|
| HRO-01, HRO-02, FTR-01, BAC-01 | HDR-01, HDR-02, HDR-03, HRO-03, HOM-01, HOM-02, HOM-04, FTR-02, BAC-02, SEO-01, SEO-02, PRF-01, PRF-02, A11Y-01, A11Y-02, A11Y-03, DOC-01 | HOM-03, SEO-03, PRF-03, DOC-02 |

---

## 14. Historique

| Date | Changement |
|------|------------|
| 2026-04-20 | Création du backlog Phase 1bis à la clôture Phase 1 front-end (header opaque au scroll validé, homepage retail enrichie complète, console clean). |
