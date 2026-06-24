# Recette — Shop CK · densification cards + allègement CTA panier (P2A)

| Champ | Valeur |
| --- | --- |
| Date | 2026-06-23 |
| Déclencheur | Comparaison `/shop/category/...` vs bienmanger.com — grammaire card (marque/eyebrow, notation, CTA icône) jugée plus mature |
| Périmètre | Card produit `/shop` et `/shop/category/...` uniquement — P2A Dev, données existantes |
| Hors périmètre (rappel explicite) | P2B contenu (hub éditorial par rayon) — piste séparée, non traitée ici. Notation, contenu saisonnier, profondeur de rayon : **non implémentés, comme demandé** |
| Modules | `dorevia_ck_theme` **19.0.1.52.0** · `dorevia_ck_marketone_content` **19.0.1.34.0** |
| Statut | Implémenté et conservé |

---

## 1. Ce qui a été fait

### 1.1 Eyebrow origine au-dessus du titre
La ligne meta existante (`origine · tags · format · prix réf.`) est **scindée** en deux :
- une eyebrow compacte au-dessus du titre, affichant **uniquement l'origine** (ex. "GUADELOUPE") — joue le rôle visuel de la ligne "marque" chez bienmanger, sans inventer de concept de marque qui n'existe pas pour CK ;
- la ligne secondaire sous le titre garde le reste (tags transversaux · format · prix comparatif), origine retirée pour ne pas la dupliquer.

**Aucune nouvelle donnée** : `_get_featured_origin_and_tag_parts` (déjà utilisée pour construire la ligne combinée) est simplement appelée deux fois — une fois pour extraire l'origine seule, une fois pour le reste. Si un produit n'a pas d'origine renseignée, l'eyebrow ne s'affiche simplement pas (`t-if`), pas de valeur de repli inventée.

### 1.2 CTA panier en icône compacte
- Bouton ramené à 38×38px, circulaire, icône panier visible (réintroduite — elle avait été retirée au lot précédent).
- Libellé "Ajouter au panier" conservé dans le DOM via `.visually-hidden` (Bootstrap) — accessible aux lecteurs d'écran, `aria-label`/`title` déjà présents sur le bouton.
- Zone basse de la card passée en ligne (prix à gauche, bouton à droite) au lieu de l'empilement prix/bouton-pleine-largeur.

### 1.3 Hiérarchie du prix
Aucun CSS dédié nécessaire : le prix redevient l'élément dominant de la zone basse simplement parce que le bouton ne fait plus toute la largeur — effet obtenu par la réorganisation en ligne, pas par un style de prix supplémentaire.

---

## 2. Ce qui n'a volontairement PAS été fait

Conformément à la consigne :

- **Pas de notation** (étoiles) — aucune donnée d'avis produit n'existe dans le système ; en ajouter une serait une fausse promesse.
- **Pas de contenu saisonnier** — aucune bannière "Le retour de l'asperge !" ou équivalent.
- **Pas de profondeur de rayon artificielle** — aucun sous-rayon ni annuaire de catégories inventé.
- **BienManger reste une référence de grammaire** (densité, hiérarchie), pas un gabarit copié.

---

## 3. Vérifications machine

| Vérification | Résultat |
| --- | --- |
| `/shop` répond 200 | ✅ |
| `/shop/category/epicerie-1` répond 200 | ✅ |
| Nombre de cards inchangé | ✅ 7 avant, 7 après |
| Débordement horizontal (desktop/tablette/mobile) | ✅ Aucun |
| Panier rapide fonctionnel | ✅ Clic bouton icône → badge panier 0→1 |
| Tests automatisés (`dorevia_ck_shop_card`, `dorevia_ck_product_origin`) | ✅ 19/19 |

---

## 4. Test mis à jour

`test_metadata_line_reuses_featured_logic` testait l'égalité stricte entre la ligne meta boutique et la ligne combinée home — devenu faux par construction (l'origine est maintenant exclue côté boutique). Remplacé par `test_metadata_line_excludes_origin_shown_separately`, qui vérifie explicitement :
- la ligne secondaire boutique correspond à la nouvelle fonction sans origine ;
- l'eyebrow correspond à l'origine seule ;
- les deux mises bout à bout ne dupliquent pas l'origine par rapport à l'ancienne ligne combinée.

---

## 5. Captures

| Fichier | Référence "avant" | "Après" P2A |
| --- | --- | --- |
| Desktop haut de page | `shop_polish_p1/after_desktop_top.png` (état P1, CTA plein) | `shop_polish_p2a/after_desktop_top.png` |
| Desktop scroll | `shop_polish_p1/after_desktop_scroll.png` | `shop_polish_p2a/after_desktop_scroll.png` |
| Tablette 800 | `shop_polish_p1/after_tablet_800.png` | `shop_polish_p2a/after_tablet_800.png` |
| Mobile 390 | `shop_polish_p1/after_mobile_390.png` | `shop_polish_p2a/after_mobile_390.png` |
| Catégorie Épicerie | `shop_polish_p1/after_category_epicerie.png` | `shop_polish_p2a/after_category_epicerie.png` |

La référence "avant" de ce lot est l'état **après P1** (déjà conservé) — pas de recapture d'un état inchangé.

---

## 6. Limites et points à arbitrer

- **Eyebrow absente sur certains produits** : constaté sur "Manio Crackers" (pas d'attribut Origine renseigné en BO pour ce produit) — comportement attendu (pas de valeur inventée), mais à signaler côté contenu si l'origine doit être systématiquement saisie.
- **P2B contenu** (hub éditorial par rayon — photo lifestyle, mises en avant saisonnières, annuaire de sous-catégories) reste entièrement à cadrer séparément, hors de ce lot.

---

## 7. Statut

```text
P2A implémenté et conservé : eyebrow origine + CTA icône compacte + foot en ligne.
Données 100% existantes — aucune notation, contenu saisonnier ou profondeur
de rayon ajoutés. Vérifications machine et tests automatisés au vert.
```
