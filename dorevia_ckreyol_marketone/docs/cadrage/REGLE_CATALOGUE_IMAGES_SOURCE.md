# Règle catalogue — images source produit

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-20 |
| **Univers** | Boutique `/shop` |
| **Contexte** | Pilote CK Image Normalizer |
| **Statut** | Règle interne MOA |

---

## Règle

```text
Un produit publié doit avoir une image source exploitable, distincte et identifiable.
Pas de même visuel pour deux SKU différents, sauf pack assumé ou collection.
```

---

## Sens produit

Le moteur `CK Image Normalizer` peut améliorer une source correcte.

Il ne doit pas compenser :

- une image générique ;
- une image incohérente avec le SKU ;
- une source dupliquée entre deux produits distincts ;
- un produit trop petit ou impossible à identifier ;
- une image lifestyle sans produit dominant.

---

## Application

Avant traitement image :

- vérifier que le SKU est identifiable ;
- vérifier que l’image correspond bien au produit vendu ;
- vérifier qu’elle n’est pas réutilisée pour un autre SKU distinct ;
- isoler les packs / collections quand le visuel mutualisé est assumé.

Si la source échoue à ces règles :

```text
demande fournisseur
ou exclusion temporaire du flux image
```

Pas de publication automatique sur une source ambiguë.
