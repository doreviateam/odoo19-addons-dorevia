# P2 — Audit visuel & ajustements hiérarchie Header CK V2.2

| Champ | Valeur |
| --- | --- |
| Date | 2026-06-23 |
| Module | `dorevia_ck_theme` **19.0.1.42.0** · correctif post-P2 hover en **19.0.1.43.0** |
| Périmètre | Hiérarchie visuelle N2/N3 · chrome mobile · respiration mega-menu |
| Hors périmètre | Architecture MOA · profondeur menus · logique nav_sync · contenu seed |

**Objectif P2 :** faire passer le header de « fonctionnellement conforme » à « visuellement mature CK », sans rouvrir l’architecture validée.

---

## 1. Audit visuel (état avant P2 — 19.0.1.41.0)

Analyse sur captures officielles `recette_header_v22/` et inspection instance live.

### 1.1 Hauteur perçue du header

| Constat | Impact |
| --- | --- |
| Empilement N1 + N2 (`min-height: 3.75rem`) + N3 génère un header **haut** au premier regard | Réduit la place utile au hero ; sensation « barre empilée » plutôt que « boutique affûtée » |
| N3 avec `padding-block` généreux | Ligne de navigation occupe plus de vertical que nécessaire |

### 1.2 Équilibre logo + baseline / recherche / panier (N2)

| Élément | Constat |
| --- | --- |
| Logo + baseline | Corrects typographiquement ; baseline discrète (OK MOA) |
| Recherche | `max-width: 36rem` — **domine** visuellement la ligne identité |
| Panier | Pill large (`padding 0.85rem`, fond terracotta 6–10 %) — **poids excessif** vs « Se connecter » |
| Connexion | Visuellement secondaire, léger — déséquilibre N2 droite |

### 1.3 Hiérarchie N3 — 3 groupes

| Groupe MOA | Constat |
| --- | --- |
| Rayons catalogue | Tous les liens au **même poids** visuel (semibold implicite Bootstrap) |
| Sélections | Pas assez distinguées des rayons |
| Relation | **Double séparateur** Maison + Artisanat (les deux portent `ck-nav-n3-group-end`) — brouille la lecture des groupes |
| Séparateur unique attendu | Trait vertical **après Artisanat** uniquement, avant Coups de cœur |

### 1.4 Pill Espace pro

| Constat | Impact |
| --- | --- |
| Fond `rgba(primary, 0.10)` + bordure 22 % | Compète visuellement avec le panier — deux CTA pills sur le header |
| Taille padding généreuse | Attire trop l’attention pour une entrée relationnelle (pas primaire d’achat) |

### 1.5 Nos producteurs

| Constat | Impact |
| --- | --- |
| Semibold seul | À peine distinct de Coups de cœur — manque le traitement « confiance / relation » attendu MOA |

### 1.6 Densité et respiration nav

| Constat | Impact |
| --- | --- |
| `gap: 0.65rem` uniforme | Ligne dense mais **plate** — groupes peu perceptibles |
| Pas de variation de couleur/poids entre rayons et sélections | Effet « 8 liens équivalents » (Coffrets absent sur seed) |

### 1.7 Mega-menu (post-correctif layout 41.0)

| Constat | Impact |
| --- | --- |
| Panneau 1200 px centré | Structure OK |
| Peu de padding / ombre propre au panneau | Aspect « contenu flottant » plus que « carte boutique » |
| 1 colonne seed | Quart gauche peuplé — correct techniquement ; reste à arbitrer éditorialement (hors P2) |

### 1.8 Mobile — chrome et drawer

| Élément | Constat |
| --- | --- |
| Chrome | Compact, logo centré — OK |
| Drawer | Items homogènes (semibold, séparateurs fins) — **pas de respiration inter-groupes** |
| Rayons vs sélections | Non différenciés visuellement |

---

## 2. Propositions SCSS retenues (19.0.1.42.0)

Ajustements **uniquement** dans `website_header.scss` — pas de changement fonctionnel, pas de modification spec MOA.

| # | Axe | Ajustement | Fichier / zone |
| --- | --- | --- | --- |
| P2-1 | Hauteur N2 | `identity-row` : `min-height 3.5rem`, `padding-block 0.45rem`, `gap` réduit | `website_header.scss` ~189 |
| P2-2 | Hauteur N3 | `nav-row` : `padding-block 0.35rem` | ~212 |
| P2-3 | Équilibre recherche | `max-width` recherche 36rem → **32rem** | ~201 |
| P2-4 | Poids panier | Pill plus sobre : `min-height 2.375rem`, padding réduit, fond 4 %, bordure neutre | ~661 |
| P2-5 | Hiérarchie rayons | Rayons en `font-weight 500` + `color muted` ; hover/active → texte plein | ~669 |
| P2-6 | Hiérarchie sélections | Sélections en semibold + couleur texte pleine | ~669 |
| P2-7 | Séparateur groupes | Masquer `group-end` sur Maison si Artisanat suit ; trait unique sur dernier rayon | ~669 (`:has`) |
| P2-8 | Nos producteurs | Semibold + `letter-spacing 0.015em` | ~669 |
| P2-9 | Pill Espace pro | Fond 7 %, bordure 18 %, padding réduit, `font-size sm` | ~669 |
| P2-10 | Mega-menu | Bordure, ombre, padding panneau ; `min-height` desktop pour respiration | ~739 |
| P2-11 | Mobile chrome | `min-height` 3.75rem → **3.5rem** | ~529 |
| P2-12 | Mobile drawer | Trait renforcé après dernier rayon ; rayons muted / sélections semibold | ~622 |

---

## 3. Preuves avant / après

Dossier : `captures/recette_header_v22/p2/`

| Fichier | Scénario | Méthode |
| --- | --- | --- |
| `before_desktop_initial.png` | Desktop chargement — avant P2 | SCSS revert P1 (voir § 3.1) |
| `after_desktop_initial.png` | Desktop chargement — après P2 | État 19.0.1.42.0 |
| `before_desktop_scroll.png` | Scroll (N1 masqué) — avant | Idem — validé tour précédent |
| `after_desktop_scroll.png` | Scroll — après | Script P2 |
| `before_mega_epicerie.png` | Mega Épicerie ouvert — avant | SCSS revert P1 + `openMega()` fiable (§ 3.2) |
| `after_mega_epicerie.png` | Mega Épicerie ouvert — après | État P2 + `openMega()` fiable |
| `before_mobile_ferme.png` | Mobile chrome fermé — avant | Validé tour précédent |
| `after_mobile_ferme.png` | Mobile chrome fermé — après | Script P2 |
| `before_mobile_drawer.png` | Drawer — avant | Validé tour précédent |
| `after_mobile_drawer.png` | Drawer — après | Script P2 |

### 3.1 Méthode « before » fidèle (19.0.1.41.0)

Les captures `before_*` ne recyclent pas d’anciennes images pré-P1 : elles correspondent à l’**état SCSS réel 19.0.1.41.0** (post-correctif layout mega, pré-P2 hiérarchie).

Procédure :

1. Sauvegarde du SCSS P2 actuel (`website_header.scss`).
2. Revert temporaire des **8 zones** modifiées par P2 vers leurs valeurs P1 exactes.
3. Rebuild module + capture `before_*` concernées.
4. Restauration du fichier P2 depuis la sauvegarde (diff vérifié identique).
5. Rebuild final — **état dépôt = P2 inchangé**.

### 3.2 Correctif script capture mega-menu

`ck_h22_p2_captures.mjs` — bug initial : `hover()` + `waitForTimeout(500)` sans vérifier `.show` → capture silencieusement fausse (header fermé) si le hover ne déclenche pas le dropdown.

**Correction** : `openMega()` attend explicitement `.o_mega_menu.show` et `getBoundingClientRect().width > 100` avant screenshot (même logique que `ck_h22_recette_qa.mjs`).

**Vérification mega Épicerie** :

| État | Panneau | Indices visuels |
| --- | --- | --- |
| `before_mega_epicerie.png` | Ouvert, **1200 px** | Sans carte P2-10 (bordure/ombre) ; N3 sans hiérarchie de poids |
| `after_mega_epicerie.png` | Ouvert, **1200 px** | Carte mega P2-10 ; rayons muted / sélections pleines ; pill panier & Espace pro adoucis |

Les paires `desktop_initial`, `desktop_scroll`, `mobile_ferme`, `mobile_drawer` n’ont pas été reprises à ce tour — déjà fiables au tour précédent.

**Relance captures P2 (après uniquement) :**

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 -u dorevia_ck_theme --stop-after-init
cd odoo19-addons-dorevia/dorevia_ck_marketone/docs/design/maquette_01.2/scripts
node ck_h22_p2_captures.mjs
```

---

## 4. Effets attendus par ajustement

| Ajustement | Effet visuel attendu |
| --- | --- |
| P2-1 / P2-2 / P2-11 | Header **~8–12 px plus compact** ; hero plus visible |
| P2-3 | Recherche reste centrale mais **moins écrasante** face au logo |
| P2-4 | Panier lisible sans rivaliser avec le CTA hero |
| P2-5 / P2-6 | Lecture N3 : **rayons = exploration** · **sélections = mise en avant** |
| P2-7 | **Un seul trait** entre rayons et sélections (plus de double séparateur Maison/Artisanat) |
| P2-8 | Producteurs perçus comme entrée **confiance** |
| P2-9 | Espace pro distinct mais **secondaire** vs panier |
| P2-10 | Mega-menu = **carte boutique** (ombre, bordure, padding) |
| P2-12 | Drawer mobile : **respiration** entre blocs rayons / sélections |

---

## 5. Limites connues (inchangées)

- **Contenu seed** : Coffrets absent, Épicerie 1 colonne, Artisanat lien direct — limitent la démo complète V2.2, pas la hiérarchie P2.
- **Fallback 1 colonne mega** : quart gauche peuplé + espace réservé — arbitrage éditorial MOA à prévoir (hors P2).
- **Recette visuelle MOA** : ce document prépare la session qualitative ; le **GO MOA final** reste à poser après revue humaine.

## 5 bis. Correctif post-P2 — traversée hover mega-menu (19.0.1.43.0)

Après validation directionnelle P2, la recette manuelle a révélé un défaut d’usage : le panneau mega-menu pouvait se fermer pendant le trajet pointeur entre l’entrée N3 et le panneau.

Correctif Dev appliqué dans `dorevia_ck_theme` :

- suppression de la zone morte verticale (`margin-top: 0`) sur le panneau `.o_mega_menu:has(.ck-mega-menu)` ;
- ajout de l’interaction JS `ck_header_mega_menu_hover_bridge` pour maintenir le dropdown ouvert pendant la traversée ;
- enrichissement de la recette automatisée avec `mega_hover_bridge.pass: true`.

Ce correctif ne modifie pas les arbitrages visuels P2 ; il fiabilise l’accès réel aux liens des mega-menus desktop.

---

## 6. Prochaine étape suggérée

1. **Session MOA** sur captures `p2/` (comparaison avant/après).
2. Ajustements fins éventuels (1–2 itérations SCSS max).
3. Régénération captures officielles `recette_header_v22/` si P2 validé.
4. Recette contenu complète (Coffrets, familles Épicerie) pour démo header cible à 9 entrées.
