# P3 — Recette visuelle pilote Header CK V2.2

| Champ | Valeur |
| --- | --- |
| Date | 2026-06-23 |
| Modules | `dorevia_ck_theme` **19.0.1.45.0** · `dorevia_ck_marketone_content` **19.0.1.30.0** |
| Périmètre | N2/N3 surfaces différenciées · recherche aplat · fallback éditorial mega-menu |
| Hors périmètre | Logo/baseline · accent actif · Fraunces étendu · micro-polish P3 bis |

## Verdict

**GO directionnel P3 pilote.**

Les deux axes priorisés renforcent bien la perception « boutique mature » sans rouvrir l’architecture MOA :

- le header gagne une assise d’enseigne grâce à la bande N3 teintée et au bouton recherche plein ;
- les mega-menus seed pauvres cessent d’être de simples panneaux de liens grâce au fallback éditorial CK ;
- le mobile fermé reste strictement non impacté.

## Captures analysées

Dossier : `captures/recette_header_v22/p3/`

| Paire | Verdict |
| --- | --- |
| `before_header_crop.png` / `after_header_crop.png` | GO — N3 mieux posée, recherche mieux ancrée |
| `before_desktop_initial.png` / `after_desktop_initial.png` | GO — effet boutique plus mature au chargement |
| `before_mega_epicerie.png` / `after_mega_epicerie.png` | GO directionnel — panneau moins pauvre malgré seed limité |
| `before_mega_boissons.png` / `after_mega_boissons.png` | GO — fallback bien intégré comme respiration éditoriale |
| `before_mobile_ferme.png` / `after_mobile_ferme.png` | OK non impacté (`cmp = 0`) |

## Lecture MOA

### N2/N3

La version avant P3 restait propre mais très blanche : N2 et N3 se lisaient comme une barre de template plutôt que comme un bloc d’enseigne.

La version P3 pose une surface différenciée sur N3 (`$ck-bg-soft`) et donne au bouton de recherche un rôle visuel clair via l’aplat `$ck-primary`. L’effet est plus marchand sans devenir corporate.

### Mega-menu Épicerie

Avant P3, le seed pauvre exposait surtout le vide : une seule colonne métier (« Origines & producteurs ») dans un panneau 1200 px.

Après P3, la carte fallback CK ajoute une présence éditoriale sobre. Elle ne crée pas de fausse profondeur produit et reste générique marque. Le panneau reste toutefois très aéré à droite : acceptable pour le pilote, à arbitrer en P3 bis si l’on veut un traitement spécifique des rayons à une seule colonne métier.

### Mega-menu Boissons

Le fallback est plus convaincant ici : deux colonnes métier + une carte éditoriale donnent une lecture équilibrée. Le panneau ressemble davantage à un vrai mega-menu boutique.

### Mobile

Aucun impact attendu ni constaté. Les captures mobile fermé avant/après sont identiques.

## Réserve non bloquante

| Sujet | Réserve |
| --- | --- |
| Fallback Épicerie 1 colonne métier | Le fallback améliore nettement la perception, mais le placement laisse encore un grand blanc à droite. À traiter en P3 bis seulement si la MOA veut une variante de layout pour les panneaux très pauvres. |

## Validation technique

```text
41 post-tests · 0 failed · 0 error(s)
Tags : dorevia_ck_header_v22, dorevia_ck_theme_phase10, dorevia_ck_marketone_nav_sync
Durée dernière passe : 19,26 s
```

Contrôles hover desktop :

- `mega_hover_bridge.pass: true` — descente N3 vers lien du panneau ;
- `mega_hover_switch.pass: true` — balayage horizontal entre rayons N3 avec un seul panneau ouvert.

## Décision

P3 pilote est validé comme direction visuelle.

Les axes restants sont renvoyés à P3 bis :

- logo / baseline ;
- accent actif terracotta ;
- Fraunces étendu ;
- micro-polish N3 / mega-menu ;
- éventuelle variante de fallback pour rayon à une seule colonne métier.
