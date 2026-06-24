# P4 — Pistes typographiques wordmark "C-Kréyòl"

| Champ | Valeur |
| --- | --- |
| Date | 2026-06-23 |
| Déclencheur | Arbitrage MOA logo — couleurs/contraste/accent/baseline validés, typographie et personnalité non validées |
| Périmètre | 5 pistes, rendu réel dans le header (pas une maquette isolée) — **aucune n'est implémentée dans le code**, captures uniquement |
| Contraintes respectées | Couleurs inchangées (noir `$ck-text` / terracotta `$ck-primary`), nom et baseline inchangés, polices SIL OFL auto-hébergeables, testées desktop + mobile |

---

## 0. Méthode

Pour ne pas évaluer ces pistes sur une intuition, j'ai :
- téléchargé les vrais fichiers woff2 de chaque police candidate (pas une approximation système) ;
- vérifié la licence **directement sur le dépôt officiel `google/fonts`** (`OFL.txt` de chaque famille), pas de mémoire ;
- injecté chaque police **dans le header réel de l'instance de recette** (pas un mockup isolé), capturé desktop (1280px) et mobile (390px) ;
- gardé les couleurs et la structure HTML strictement identiques — seule la `font-family` change.

Aucun fichier de police n'a été ajouté au module ; les woff2 de test ont été utilisés en mémoire le temps des captures puis supprimés.

---

## 1. V0 — Fraunces actuelle (référence)

| | |
| --- | --- |
| Police | Fraunces (déjà en place) |
| Licence | SIL OFL 1.1 |
| Auto-hébergement | Déjà fait (`static/src/fonts/fraunces-latin.woff2`) |
| Desktop | `logo_fonts/desktop_v0_fraunces_actuel.png` |
| Mobile | `logo_fonts/mobile_v0_fraunces_actuel.png` |

**Appréciation** — Chaleur : faible/moyenne. Lisibilité : bonne. Personnalité : faible (serif élégant mais générique, c'est précisément le constat de départ de la MOA). Risque visuel : nul, déjà en production.

---

## 2. V3 — Fraunces "signature" (grand C, témoin structurel demandé)

| | |
| --- | --- |
| Police | Fraunces (identique à V0, seul le traitement change) |
| Licence | SIL OFL 1.1 |
| Auto-hébergement | Déjà fait |
| Desktop | `logo_fonts/desktop_v3_fraunces_signature.png` |
| Mobile | `logo_fonts/mobile_v3_fraunces_signature.png` |

**Appréciation** — Chaleur : inchangée vs V0 (même police). Lisibilité : légèrement perturbée par le déséquilibre du C surdimensionné. Personnalité : gain réel en desktop (devient un vrai repère), **mais le rendu actuel n'est pas abouti** — l'alignement vertical du C n'est pas corrigé optiquement, ça ressemble plus à un défaut de taille qu'à un geste de marque assumé. Risque visuel : moyen, plus marqué en mobile où l'espace est compté (le C y domine de façon disproportionnée). **À ne retenir que moyennant un vrai travail de calage**, pas en l'état.

---

## 3. Bitter

| | |
| --- | --- |
| Police | Bitter (Sol Matas / Bitter Project Authors) |
| Licence | SIL OFL 1.1 — vérifiée sur `google/fonts/ofl/bitter/OFL.txt` |
| Auto-hébergement | Disponible, même procédure que Fraunces/DM Sans actuels |
| Desktop | `logo_fonts/desktop_bitter.png` |
| Mobile | `logo_fonts/mobile_bitter.png` |

**Appréciation** — Chaleur : bonne — slab serif aux formes pleines, ancrage "épicerie artisanale" net. Lisibilité : très bonne (Bitter est dessinée pour l'écran). Personnalité : bonne — nettement plus "solide/ancré" que Fraunces, sans tomber dans le folklorique. Risque visuel : faible — registre "grocery slab" largement utilisé en e-commerce alimentaire premium, pas un cliché tropical.

---

## 4. Lora

| | |
| --- | --- |
| Police | Lora (Cyreal) |
| Licence | SIL OFL 1.1 — vérifiée sur `google/fonts/ofl/lora/OFL.txt` |
| Auto-hébergement | Disponible, même procédure |
| Desktop | `logo_fonts/desktop_lora.png` |
| Mobile | `logo_fonts/mobile_lora.png` |

**Appréciation** — Chaleur : bonne — courbes d'inspiration calligraphique, contraste de graisse doux, rendu vivant. Lisibilité : bonne. Personnalité : moyenne/bonne — plus singulière que Fraunces, mais reste dans un registre "joli serif éditorial" assez répandu, risque de paraître "safe" pour un e-commerce qui veut se démarquer. Risque visuel : faible.

---

## 5. Newsreader

| | |
| --- | --- |
| Police | Newsreader (Production Type) |
| Licence | SIL OFL 1.1 — vérifiée sur `google/fonts/ofl/newsreader/OFL.txt` |
| Auto-hébergement | Disponible, même procédure |
| Desktop | `logo_fonts/desktop_newsreader.png` |
| Mobile | `logo_fonts/mobile_newsreader.png` |

**Appréciation** — Chaleur : moyenne — registre éditorial contemporain, un peu plus neutre que Lora dans ce rendu. **Limite technique à noter** : Newsreader exprime l'essentiel de sa personnalité via son axe variable "optical size" (taille optique) à grands corps ; le fichier statique utilisé ici pour la comparaison ne l'exploite pas, donc ce rendu **sous-représente** un peu son potentiel réel. Lisibilité : bonne. Personnalité : moyenne dans ce test, potentiellement meilleure avec un export variable dédié. Risque visuel : faible, mais gain de chaleur le plus modeste des 3 alternatives en l'état testé.

---

## 6. Synthèse comparative

| Piste | Chaleur | Lisibilité | Personnalité | Risque visuel |
| --- | --- | --- | --- | --- |
| V0 — Fraunces actuelle | Faible | Bonne | Faible | Nul |
| V3 — Fraunces signature | Faible (=V0) | Moyenne | Bonne (non abouti) | Moyen |
| Bitter | Bonne | Très bonne | Bonne | Faible |
| Lora | Bonne | Bonne | Moyenne | Faible |
| Newsreader | Moyenne | Bonne | Moyenne (sous-testée) | Faible |

---

## 7. Recommandation

Sans trancher à votre place : **Bitter** est la piste qui répond le plus directement au brief ("chaleureux, vivant, premium, sans caricature créole") avec le risque le plus bas — c'est aussi celle qui s'éloigne le plus de Fraunces, donc celle qui change le plus reconnaissablement la perception du mot-symbole. **Lora** est l'option la plus sûre si vous voulez un gain de chaleur sans trop rompre avec le registre serif élégant actuel. **Newsreader** mériterait un second test avec un export variable optical-size avant d'être écartée ou retenue. **V3 n'est pas une option en l'état** (calage à refaire) mais reste une piste de traitement structurel à garder en tête, indépendamment du choix de police.

---

## 8. Prochaine étape

Dans l'attente de votre arbitrage : aucune implémentation. Si une piste est retenue, prochaine étape = ajout du fichier de police au module (`static/src/fonts/`), mise à jour de `website_fonts.scss` et `ck_tokens.scss` (`$ck-font-display`), puis recette visuelle complète du header (pas seulement le logo).
