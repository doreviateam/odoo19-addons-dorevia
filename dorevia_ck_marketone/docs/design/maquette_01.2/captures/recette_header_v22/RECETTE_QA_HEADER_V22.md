# Recette QA — Header CK V2.2

| Champ | Valeur |
| --- | --- |
| Date | 2026-06-23 |
| Base | `http://localhost:18079` |
| DB | `dorevia_ck_marketone_01` |
| Modules | `dorevia_ck_theme` **19.0.1.45.0** (P3 pilote + hover switch) · `dorevia_ck_marketone_content` **19.0.1.30.0** |

## Statut de validation

| Niveau | Statut |
| --- | --- |
| Socle technique (tests, comportements fonctionnels) | **GO technique** |
| Correctif layout mega-menu (19.0.1.41.0) | **Validé** |
| Recette visuelle P2 — hiérarchie chrome N2/N3 | **Validée direction** |
| Correctif ergonomie hover mega-menu (19.0.1.43.0) | **Validé** |
| Correctif rafraîchissement hover horizontal (19.0.1.45.0) | **Validé** |
| Recette visuelle P3 pilote — surfaces N2/N3 + fallback éditorial | **GO directionnel** |
| Recette QA automatisée + captures reproductibles | **À jour (état P3 pilote)** |
| GO MOA final Header V2.2 (démo contenu complète) | **Sous réserves seed** |

Référence audit P2 : [`P2_AUDIT_HEADER_V22.md`](../../P2_AUDIT_HEADER_V22.md) · recette P3 pilote : [`P3_RECETTE_VISUELLE_HEADER_V22.md`](../../P3_RECETTE_VISUELLE_HEADER_V22.md) · comparaisons avant/après : `p2/`, `p3/`

Les captures seed documentent le chrome et les comportements réels, mais **ne démontrent pas** le header cible à 9 entrées (Coffrets absent, Épicerie partielle, Artisanat lien direct). Voir [`LIVRABLE_MOA_HEADER_CK_V2_2.md`](../../LIVRABLE_MOA_HEADER_CK_V2_2.md).

## Résultat tests automatisés

```text
41 tests · 0 failed · 0 error
Tags : dorevia_ck_header_v22, dorevia_ck_theme_phase10, dorevia_ck_marketone_nav_sync
Durée dernière passe : 19,26 s
```

Log complet : `tests_ck_header_v22.log` (session locale Dev).

## Captures officielles (état P3 pilote — 19.0.1.45.0 / 19.0.1.30.0)

| Fichier | Scénario |
| --- | --- |
| `01_desktop_initial.png` | Desktop 1280 — N1+N2+N3 (header compact, hiérarchie groupes) |
| `02_desktop_scroll.png` | Desktop scroll — bandeau masqué, header sticky |
| `03_mega_e_picerie.png` | Mega-menu Épicerie ouvert — carte boutique 1200 px |
| `04_mega_boissons.png` | Mega-menu Boissons ouvert |
| `05_mega_maison_bien_e_tre.png` | Mega-menu Maison & Bien-être ouvert |
| `06_artisanat.png` | Artisanat (lien direct — < 3 familles) |
| `07_mobile_ferme.png` | Mobile 390 — chrome fermé |
| `08_mobile_drawer.png` | Drawer navigation |
| `08b_mobile_mega_epicerie.png` | Accordéon mobile Épicerie — « Origines & producteurs » dépliée |
| `09_espace_pro_dropdown.png` | Dropdown Espace pro |
| `10_nos_producteurs_nav.png` | Lien Nos producteurs N3 |

Données machine : `recette_header_v22_results.json`

Le script `ck_h22_recette_qa.mjs` ouvre les mega-menus desktop par **survol** (`o_hoverable_dropdown`), vérifie `.o_mega_menu.show`, hauteur > 48 px et `panelWidth` ≈ 1200 px avant capture. Il contrôle aussi la traversée pointeur entrée N3 → panneau (`mega_hover_bridge.pass: true`) et le balayage horizontal entre rayons N3 (`mega_hover_switch.pass: true`). Sur mobile, il déplie les sous-sections accordéon du panneau actif avant screenshot.

## Correctif layout mega-menu (19.0.1.41.0)

**Cause racine (bug CSS)** : `#top_menu.top_menu .dropdown-menu { max-width: 320px }` capturait aussi `.o_mega_menu` → panneau écrasé à 320 px (effet mini-dropdown), indépendamment du contenu seed.

**Correctif** (`website_header.scss`) :

1. `:not(.o_mega_menu)` sur le cap 220/320 px.
2. `.o_mega_menu:has(.ck-mega-menu)` — largeur container 1200 px, centrage.
3. `.ck-mega-menu__col { flex: 0 0 25% }` — grille 4 colonnes à slots fixes.

## P2 — hiérarchie visuelle (19.0.1.42.0)

Ajustements SCSS ciblés (pas de changement fonctionnel) — **validés direction** :

| Axe | Résultat |
| --- | --- |
| Hauteur header | Plus compact (N2/N3) |
| Équilibre N2 | Recherche moins dominante ; panier adouci |
| Hiérarchie N3 | Rayons muted · sélections pleines · séparateur unique inter-groupes |
| Espace pro | Pill sobre, secondaire vs panier |
| Nos producteurs | Traitement relation / confiance renforcé |
| Mega-menu | Carte boutique (bordure, ombre, padding) sur panneau 1200 px |

## Correctif ergonomie hover mega-menu (19.0.1.43.0)

**Cause racine (interaction hover)** : après ancrage du panneau sous N3, Bootstrap/Odoo pouvait fermer le dropdown dès que le pointeur quittait l’entrée N3, avant d’atteindre le panneau. Le panneau était correctement positionné, mais le trajet utilisateur n’était pas stable.

**Correctif** :

1. Suppression du `margin-top` du panneau mega-menu pour éviter une zone morte verticale.
2. Ajout d’une interaction JS `ck_header_mega_menu_hover_bridge` qui maintient le dropdown ouvert tant que le pointeur reste dans le rectangle de transition entrée N3 + panneau.
3. Fermeture différée courte uniquement lorsque le pointeur sort réellement de cette zone.

**Preuve QA** : `mega_hover_bridge.pass: true` dans `recette_header_v22_results.json`, avec survol effectif du lien `Guadeloupe` (`/shop?attrib=2-5`) dans le mega-menu Épicerie.

## Correctif rafraîchissement hover horizontal (19.0.1.45.0)

**Cause racine (interaction multi-rayons)** : le hover bridge 19.0.1.43.0 maintenait correctement le panneau ouvert pendant la descente verticale, mais pouvait conserver plusieurs panneaux `.show` quand le pointeur balayait horizontalement les rayons N3.

**Correctif** :

1. Introduction d’un `activeRecord` côté JS : un seul rayon mega-menu est actif à la fois.
2. À l’entrée sur un rayon, fermeture forcée des autres panneaux (`item`, `panel`, `toggle`, `aria-expanded`).
3. Maintien du bridge uniquement pour le rayon actif.

**Preuve QA** : `mega_hover_switch.pass: true` dans `recette_header_v22_results.json` sur la séquence `Épicerie → Boissons → Maison & Bien-être → Boissons → Épicerie`, avec un seul panneau ouvert à chaque étape.

## P3 pilote — boutique mature (19.0.1.44.0 / 19.0.1.30.0)

Périmètre livré et recetté :

| Axe | Verdict |
| --- | --- |
| N3 sur bande teintée `$ck-bg-soft` | **GO** — effet enseigne/boutique plus affirmé que blanc-sur-blanc |
| Bouton recherche en aplat `$ck-primary` | **GO** — ancre visuellement la recherche sans agrandir le champ |
| Fallback éditorial colonne 4 | **GO directionnel** — améliore les mega-menus seed pauvres sans créer de faux contenu produit |
| Mobile fermé | **OK non impacté** — `before_mobile_ferme.png` et `after_mobile_ferme.png` identiques (`cmp = 0`) |

Captures de comparaison : `p3/before_*` et `p3/after_*`.

Réserve P3 non bloquante : sur Épicerie seed pauvre, le fallback éditorial améliore la perception mais laisse encore un grand espace blanc à droite. C’est acceptable pour le pilote ; un arbitrage P3 bis pourra traiter le placement/recentrage du fallback en cas de panneau à 1 seule colonne métier.

## Comportements seed documentés (non écarts fonctionnels)

### Coffrets — entrée absente

Aucun tag coffret publié sur seed → entrée N3 absente. Comportement **attendu** (pas de fausse profondeur). À recontrôler en recette contenu complète.

### Épicerie — contenu partiel

Une seule colonne peuplée (« Origines & producteurs »). Layout mega **1200 px** conforme ; contenu partiel = seed.

## Réserves non bloquantes

| Sujet | Statut |
| --- | --- |
| **Fallback mega 1 colonne** | Amélioré par P3 (carte éditoriale CK). **À arbitrer en P3 bis** : placement/recentrage si une seule colonne métier est alimentée. |
| **Drawer mobile** | Acceptable P2 (respiration groupes, différenciation rayons/sélections). **Polish ultérieur** possible (alignement, densité, micro-espacements). |
| **Démo header cible 9 entrées** | Requiert alimentation contenu (Coffrets, familles Épicerie, mega Artisanat, blocs visuels colonne 4). |

## Points d'attention — verdict recette

| Critère | Résultat |
| --- | --- |
| Bandeau N1 disparaît au scroll | OK |
| Header sticky, plus compact (P2) | OK |
| Hiérarchie N3 — 3 groupes perceptibles (P2) | OK |
| Mega-menus ouverts (03–05) | OK (`open: true`, `panelWidth: 1200`) |
| Traversée hover N3 → lien mega-menu | OK (`mega_hover_bridge.pass: true`) |
| Rafraîchissement hover horizontal entre rayons | OK (`mega_hover_switch.pass: true`) |
| Mega-menu carte boutique (P2) | OK |
| N3 surface différenciée P3 | OK |
| Recherche bouton plein P3 | OK |
| Fallback éditorial mega-menu P3 | OK directionnel |
| Aucune famille vide exposée | OK |
| Coups de cœur = lien direct | OK |
| Coffrets absent seed | OK — comportement attendu |
| URLs Odoo adaptées | OK |
| Artisanat conditionnel | OK (lien direct) |
| Espace pro dropdown | OK |
| Mobile sans bloc visuel | OK |
| Mobile accordéon Épicerie (08b) | OK |

## Relance

```bash
# Upgrade
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 \
  -u dorevia_ck_theme,dorevia_ck_marketone_content --stop-after-init

# Tests
docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 \
  --test-enable --stop-after-init \
  --test-tags="dorevia_ck_header_v22,dorevia_ck_theme_phase10,dorevia_ck_marketone_nav_sync" \
  --http-port=8077

# Captures officielles
cd odoo19-addons-dorevia/dorevia_ck_marketone/docs/design/maquette_01.2/scripts
node ck_h22_recette_qa.mjs
```
