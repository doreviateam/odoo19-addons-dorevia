# P4 hybride — Recette finale Header enseigne CK

| Champ | Valeur |
| --- | --- |
| Date | 2026-06-23 |
| Périmètre | Correctif du trait logo mobile (réserve MOA #2), recette finale post-correctif |
| Modules | `dorevia_ck_theme` **19.0.1.47.0** · `dorevia_ck_marketone_content` **19.0.1.31.0** |
| Référence | [`P4_HYBRIDE_HEADER_ENSEIGNE_CK.md`](P4_HYBRIDE_HEADER_ENSEIGNE_CK.md) (implémentation, gouvernance visuel rayon — inchangée par ce correctif) |

---

## 1. Correctif réserve #2 — trait logo mobile

### Cause exacte (mesurée, pas supposée)

Le trait était ancré en `left: 0` sur `.navbar-brand.ck-header__brand-link` (le lien englobant). Sur mobile, ce lien est `flex: 1 1 auto` + `text-align: center` (chrome compact entre le bouton menu et les icônes recherche/panier) — **mesuré : conteneur de 226px de large, texte « C-Kréyòl » de 101px, centré dedans**. `left: 0` plaçait donc le trait à l'extrémité gauche des 226px, soit 62px à gauche du mot réellement affiché — exactement l'« élément flottant à gauche » signalé.

Sur desktop, le lien n'est pas flex-grow (largeur ≈ celle du texte), donc le décalage n'était pas perceptible — d'où un bug invisible en recette desktop, révélé seulement sur mobile.

### Correctif

Le trait est maintenant ancré sur `.ck-header__brand` (le `<span>` du texte lui-même, toujours dimensionné à son contenu, sur les deux gabarits) plutôt que sur le lien englobant. Conséquence : le trait suit la position réelle du mot « C-Kréyòl », centré ou non selon le layout du parent, sans logique conditionnelle desktop/mobile distincte.

### Vérification

| Mesure | Avant correctif | Après correctif |
| --- | --- | --- |
| Position du trait (mobile, `left` du `::after`) | `left:0` du conteneur 226px → x=64 (hors texte) | `left:0` du span 101px → x=126,4 (= début exact du mot) |
| Chevauchement baseline (desktop) | n/a (jamais touché) | Vérifié : 2,5px de marge avant le début de « épicerie créole », aucun chevauchement |

Capture avant/après visuelle : trait désormais directement sous le mot, plus aucun espace mort à gauche (cf. `mobile_ferme.png` ci-dessous vs la capture précédente jointe au retour MOA).

---

## 2. Captures de recette finale

Dossier : `captures/recette_header_v22/p4_final/`

| Fichier | Contenu |
| --- | --- |
| `desktop_initial.png` | Header desktop — plaque N2/N3, logo signé (inchangé par ce correctif) |
| `mega_epicerie.png` | Mega-menu Épicerie — visuel rayon BO + bandeau de preuves |
| `mega_boissons.png` | Mega-menu Boissons — visuel rayon BO + bandeau de preuves |
| `mobile_ferme.png` | **Mobile corrigé** — trait logo centré sous le wordmark |

---

## 3. Rappel — réserve #1, toujours active

Les visuels actuellement affichés dans les mega-menus Épicerie et Boissons (`ck.mega.menu.rayon.visual`, BO : *Site Web > Configuration > Visuels rayon mega-menu (identité)*) sont des **placeholders de démonstration**, pas des visuels définitifs :

- Épicerie : photo confiture de goyave (produit catalogue réel, réutilisé une seule fois comme point de départ).
- Boissons : photo jus Mont-Pelé (idem).

Ils sont **remplaçables sans intervention Dev** — édition directe en BO (image, titre, sous-titre). Avant GO final sur cet axe, il reste à cadrer un brief contenu/visuel par rayon (territoire, ambiance, sélection — pas un produit unique érigé en symbole du rayon) avec la MOA/équipe contenu.

---

## 4. Statut

```text
Correctif mobile appliqué et vérifié (mesure DOM + capture).
Recette finale prête : desktop initial, mega Épicerie, mega Boissons, mobile corrigé.
Réserve ouverte : visuels rayon = placeholders, brief définitif à cadrer.
```
