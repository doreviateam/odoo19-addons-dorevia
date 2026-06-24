# Recette — Shop CK et rayon Epicerie · etat courant P2A / pret P2B

| Champ | Valeur |
| --- | --- |
| Date | 2026-06-23 |
| Instance | `dorevia_ck_marketone_01` |
| Base | `http://localhost:18079` |
| Objet | Recette live de `/shop`, `/shop/category/epicerie-1`, sous-familles Epicerie, cards P2A et panier rapide. |
| Script | `docs/design/maquette_01.2/scripts/ck_shop_recette_current.mjs` |
| Resultats JSON | `docs/design/maquette_01.2/captures/shop_recette_current/shop_recette_current_results.json` |
| Statut | OK technique P2A · Epicerie eligible P2B · P2B editorial non implemente |

---

## 1. Verdict

```text
GO recette technique P2A.
GO pour utiliser Epicerie comme rayon pilote P2B.
P2B editorial reste a produire apres validation des contenus/visuels.
```

Le shop actuel est stable techniquement et exploitable.

Il ne doit pas encore etre considere comme une page rayon editorialisee type benchmark BienManger : ce niveau depend du lot P2B contenu + structure editoriale.

---

## 2. Pages controlees

| Page | Resultat |
| --- | --- |
| `/shop` desktop 1280 | 200 · 7 produits · pas d'overflow |
| `/shop/category/epicerie-1` desktop 1280 | 200 · 4 produits · pas d'overflow |
| `/shop` tablette 800 | 200 · pas d'overflow |
| `/shop` mobile 390 | 200 · pas d'overflow |

Captures generees :

```text
docs/design/maquette_01.2/captures/shop_recette_current/
```

---

## 3. Cards P2A

| Critere | Resultat |
| --- | --- |
| Cards CK shop detectees | 7 sur `/shop`, 4 sur Epicerie |
| Eyebrow origine | Present quand donnee disponible |
| CTA panier compact | 38 x 38 px · radius 999px |
| Libelle accessible | `Ajouter au panier` detecte |
| Panier rapide | OK · badge `0` -> `1` |

Produits detectes sur `/shop` :

- Confiture de goyave
- Manio Crackers
- Galettes de manioc
- Savon vetiver
- Chapeau Panama
- Pate de manioc
- Jus Mont-Pele

---

## 4. Epicerie et sous-familles

Les liens reels rendus par Odoo ont ete extraits du DOM avant controle.

| Lien | Resultat |
| --- | --- |
| `/shop/category/epicerie-1` | 200 |
| `/shop/category/epicerie-biscuits-183` | 200 |
| `/shop/category/epicerie-confitures-184` | 200 |
| `/shop/category/epicerie-farines-manioc-388` | 200 |

Conclusion :

```text
Les 3 sous-familles Epicerie visibles sont bien servies par des URLs Odoo valides.
Epicerie respecte le seuil minimum P2B de 3 familles alimentees.
```

---

## 5. Points de vigilance

### 5.1 H1 encore generique sur les categories

Sur `/shop/category/epicerie-1`, le `title` navigateur est bien `Epicerie | C-Kreyol`, mais le H1 visible reste :

```text
Boutique C-Kreyol
```

Ce n'est pas bloquant pour P2A, mais P2B devra corriger ce point :

```text
Une page rayon Epicerie doit afficher un H1 de rayon, par exemple `Epicerie creole`.
```

### 5.2 P2B non encore implemente

La page actuelle reste une page shop structuree :

- intro compacte ;
- filtres ;
- barre catalogue ;
- cards densifiees.

Elle n'est pas encore :

- header de rayon lifestyle ;
- annuaire editorial de sous-familles ;
- mises en avant saisonnieres/commerciales ;
- bloc editorial de rayon.

Ce point depend du brief P2B contenu.

### 5.3 Origine absente sur certains produits

L'eyebrow origine apparait uniquement quand la donnee existe.

Comportement conforme :

```text
Pas de valeur de repli inventee.
```

---

## 6. Conclusion MOA

```text
P2A est techniquement valide.
Le socle catalogue Epicerie est maintenant suffisamment propre pour demarrer P2B.
Le prochain travail n'est plus un correctif technique de listing,
mais la construction editoriale du rayon Epicerie.
```

Priorite suivante :

1. Valider copie courte Epicerie.
2. Choisir ou produire le visuel Epicerie.
3. Valider les 1 a 3 mises en avant.
4. Demander au Dev le bloc P2B rayon pilote Epicerie.
