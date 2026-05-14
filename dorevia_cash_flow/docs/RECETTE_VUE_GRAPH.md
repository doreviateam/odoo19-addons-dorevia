# Recette — Vue Graph native (V1)

## Lecture métier (à ne pas confondre)

Le rapport **ne** doit **pas** être lu comme **deux courbes concurrentes** « Constaté » et « Projeté ».

La bonne lecture est **une seule trajectoire de trésorerie** : **une courbe** `date → solde` (`anchor_date` / `balance`). Le couple **constaté / projeté** (`segment`) **qualifie les segments** de cette même courbe (avant / après la date de situation), et non deux trajectoires indépendantes.

---

## Modèle métier (points)

- **`anchor_date`** : date du point ;
- **`balance`** : solde de trésorerie à cette date ;
- **`segment`** : `actual` ou `projected` — qualifie le **segment** de courbe.

Aucune valeur artificielle à **zéro** pour un segment hors sa plage temporelle.

---

## Rendu cible (graphique)

1. **Une courbe unique** `date / balance` ;
2. segment **constaté** jusqu’à la **date de situation** ;
3. segment **projeté** après la date de situation jusqu’à **date de situation + 90 jours** ;
4. **aucune** valeur artificielle à zéro ;
5. **aucune** chute à zéro du constaté après la date de situation ;
6. **aucune** courbe projetée à zéro avant la date de situation.

---

## Repères visuels idéaux (cible produit)

En complément de la courbe, l’intention visuelle est :

1. **Ligne verticale** à la **date de situation** — matérialise la **bascule** constaté / projeté ;
2. **Ligne horizontale** au **seuil d’alerte** — matérialise le plancher sous lequel la trésorerie entre en zone de vigilance / tension ;
3. **Marquage du point bas** de la trajectoire sur la période affichée.

---

## Priorité V1 (vue Graph native)

Si la vue Graph **native** Odoo **ne permet pas** d’afficher proprement la ligne verticale, la ligne horizontale de seuil et le point bas **sur le graphique** (ce qui est le cas en pratique pour une vue `graph` standard limitée à mesures / dimensions), **le consigner en recette** (version Odoo, capture) dans ce fichier.

Dans ce cas, la **priorité V1** reste :

- **une courbe unique** lisible (`anchor_date` / `balance`, **sans** `segment` en colonne — éviter les zéros artificiels dus à deux séries) ;
- **pas** de zéros artificiels hors segment ;
- **point bas** et **seuil d’alerte** visibles dans le **bandeau du wizard** (après génération des points) ;
- **date de situation** clairement affichée sur le **wizard** (repère textuel de la bascule).

Le détail **constaté / projeté** par point reste dans la **vue liste** des points.

---

## Écart structurel : confirmation V2

Lorsque le rendu cible (ligne verticale, ligne de seuil, marqueur du point bas **dans** le graphique) n’est **pas** atteignable avec le graph natif sans compromettre la lecture (zéros, double série), cela **confirme** qu’une **V2** en **client action OWL / Chart.js** (ou équivalent) sera nécessaire pour la **lecture visuelle complète** attendue, **sans** modifier les données Cash Guard.

---

## Choix d’implémentation retenu (V1)

### Une seule série dans le `graph`

Ne pas utiliser `segment` (ni deux mesures dérivées) en **colonne** : le moteur trace deux séries et complète souvent par **0** hors plage → lecture **fausse**.

**Règle** : une mesure `balance`, axe `anchor_date`, type ligne — voir `views/cash_flow_trajectory_views.xml`.

### Histogramme

Si l’utilisateur passe le graph en **barres**, le rendu peut s’écarter de l’intention ; en recette, **rester sur le type ligne**.

### Couleurs par segment sur une seule courbe

Le graph natif ne colore pas deux **segments** d’**une** même ligne différemment sans mécanismes avancés. **Préférer** une courbe unique lisible à une bichromie obtenue au prix de zéros trompeurs. La V2 pourra colorier les segments sans artefacts.

### Faux positifs « zéros » sur série unique

Si une version d’Odoo complétait quand même des mailles pour une série unique, **documenter** ici (version, capture).

---

## Références

- Spécification : `docs/SPEC_CASH_FLOW_TRAJECTORY.md` § 5.3 et § 5.4.
- Code : `dorevia_cash_flow/views/cash_flow_trajectory_views.xml`, assistant `dorevia.cash.flow.trajectory.wizard`.
