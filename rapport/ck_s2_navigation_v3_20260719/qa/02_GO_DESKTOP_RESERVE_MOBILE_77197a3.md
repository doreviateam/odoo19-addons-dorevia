# Verdict QA ciblée — GO avec réserve mobile (`77197a3`)

**Verdict : GO desktop / DOM mobile — réserve visuelle 390 px**

SHA : `77197a3acecbb832e15c8552f1bdd20ea730d766` · version **19.0.1.98.0**

| Contrôle | Résultat |
|---|---|
| Desktop rendu | Conforme |
| Ordre | Boutique → Épicerie → Producteurs → Professionnels |
| Routes | 5/5 en HTTP 200 |
| Collision héritée 20/20 | Réparée au premier sync |
| Rayon BO sur 60 | Déplacé immédiatement |
| BO hors réserves à 45 | Préservé |
| Collision BO 40/40 | Résolue |
| Double resync | Strictement idempotent |
| Drawer mobile (DOM) | Quatre liens, bon ordre, aucun doublon |

**Réserve :** navigateur de la passe fixé à 1280 px. DOM responsive mobile contrôlé ; ouverture interactive et rendu visuel à **390 px** non scellés dans cette passe.

```text
desktop_visual_qa          = passed
mobile_dom_qa              = passed
mobile_390_visual_qa       = reserve
sequence_order             = passed
ready_for_MOA_arbitrage    = no   # contre-recette 390 px requise
```
