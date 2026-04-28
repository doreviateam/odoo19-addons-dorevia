# Standards médias — Fiche produit (MVP2.4 Lot 2)

**Référence ticket** : [TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24_LOT2.md](TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24_LOT2.md)  
**Date** : 2026-04-28  
**Statut** : version opérationnelle v1

---

## 1) Objectif

Définir un standard média homogène pour améliorer la perception qualité des fiches produit, sans refonte technique :

- types de visuels attendus ;
- niveau minimum acceptable ;
- règles de ratio/poids ;
- cohérence visuelle catalogue.

---

## 2) Typologie des visuels

Ordre de priorité recommandé :

1. **Packshot** (obligatoire)  
   - produit lisible, cadrage propre, fond neutre ou cohérent charte.

2. **Détail / texture** (recommandé)  
   - zoom matière, coupe, granularité, détail qui aide à projeter la qualité.

3. **Usage / dégustation** (recommandé)  
   - mise en situation réaliste (service, accompagnement, moment de consommation).

4. **Origine / ambiance** (optionnel, si disponible)  
   - contexte de production/territoire, sans folklore artificiel.

---

## 3) Exigences minimales de qualité

Critères obligatoires :

- image nette (pas de flou non intentionnel) ;
- exposition correcte (ni brûlée, ni trop sombre) ;
- couleurs fidèles au produit ;
- pas d’artefacts de compression visibles ;
- pas de watermark intrusif.

Critères de cohérence :

- même logique de cadrage sur une gamme ;
- fond cohérent entre produits comparables ;
- style photo homogène (lumière, tonalité, rendu).

---

## 4) Ratio, dimensions, poids (guidelines)

Recommandations pratiques :

- **Ratio cible** : 1:1 (ou ratio unique défini par collection, mais stable).
- **Résolution utile** : minimum 1200 px côté long (idéal 1600 px+ source).
- **Poids cible web** : 150 à 450 Ko par image (selon complexité), en gardant la netteté.
- **Format** : privilégier JPEG optimisé pour photo ; PNG seulement si besoin réel.

Règle :

- privilégier la constance catalogue plutôt que l’optimisation extrême d’un cas isolé.

---

## 5) Niveaux de complétude média par fiche

- **Niveau pauvre (minimum publiable)** : 1 visuel packshot propre.
- **Niveau moyen** : packshot + (détail ou usage).
- **Niveau riche** : packshot + détail + usage (+ origine/ambiance si disponible).

---

## 6) Checklist d’acceptation média (par fiche)

- [ ] Packshot présent et lisible.
- [ ] Visuel détail/texture présent (ou NA justifié).
- [ ] Visuel usage/dégustation présent (ou NA justifié).
- [ ] Ratio conforme à la norme catalogue.
- [ ] Poids optimisé sans perte visible excessive.
- [ ] Cohérence visuelle avec les fiches de la même famille.

---

## 7) Gestion des cas NA

Si un visuel n’existe pas encore :

- marquer `NA — asset absent` ;
- ne pas classer en KO dev ;
- créer une action backlog média avec priorité.

---

## 8) Historique

| Date | Changement |
|------|------------|
| 2026-04-28 | Création du standard médias Lot 2 MVP2.4 (typologie, qualité, ratio, poids, checklist). |
