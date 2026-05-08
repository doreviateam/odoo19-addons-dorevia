# TICKET — Home spacing Palier B (rythme vertical)

**ID** : `HOME-SPACING-PALIER-B`  
**Date d'ouverture** : 2026-05  
**Priorité** : **P2**  
**Statut** : **À exécuter (après validation ticket)**  
**Module** : `dorevia_ckreyol_marketplace`

---

## 1. Objectif

Uniformiser le rythme vertical entre les sections de la Home, sans changer l’ordre, le contenu ni la direction artistique.

Cette passe est un polish de rythme Home, pas une refonte.

---

## 2. Tokens

```css
--ckr-home-section-gap-mobile: 48px;
--ckr-home-section-gap-desktop: 72px;
```

Breakpoints :

- mobile : `< 992px`
- desktop : `>= 992px`

---

## 3. Règle globale

Appliquer un rythme vertical cohérent entre sections Home via :

```css
section + section
```

dans le conteneur Home.

Principes :

- rythme principal unique ;
- pas d’override local sauf exception validée ;
- éviter les “trous” visuels et les sections collées.

---

## 4. Exceptions autorisées

### Hero → Explorer

- mobile : `40px`
- desktop : `56px`

Raison : enchaînement rapide vers les portes commerce.

### En pratique → Newsletter

- mobile : `40px`
- desktop : `64px`

Raison : liaison logique “confiance → relation”.

Tout le reste conserve le gap standard.

---

## 5. Critères GO

- à scroll identique, la Home paraît régulière ;
- aucun double vide entre sections ;
- aucun bloc collé ;
- les blocs marchands restent visibles tôt sur mobile ;
- desktop conserve sa respiration ;
- pas d’effet patchwork.

---

## 6. Hors scope

- pas de changement de contenu ;
- pas de refonte Hero / Explorer ;
- pas de changement d’ordre des blocs ;
- pas de retouche header / footer ;
- pas de nouvelle section ;
- pas de modification des pattern-blocs.

---

## 7. Décision

Ce ticket cadre un **Palier B de spacing** limité au rythme vertical de la Home.  
Toute évolution hors de ce périmètre devra faire l’objet d’un ticket séparé.

