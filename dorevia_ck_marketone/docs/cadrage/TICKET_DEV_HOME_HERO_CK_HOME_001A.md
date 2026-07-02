# Ticket Dev — CK-HOME-001A — Repositionnement du hero Home

Statut : **GO ouverture**, prêt pour mise en place.
Relecture Dev effectuée sur le code réel (`home_hero.py`, manifest, migrations, contrôleur `/producteurs`) avant ouverture. Cette relecture a ajouté 3 précisions techniques et 1 ajustement de contenu (kicker) à la spec MOA d'origine — détaillés en §0.

Base locale : `dorevia_ck_marketone_01`
Versions de référence avant lot :
```
dorevia_ck_marketone_content : 19.0.1.74.0
dorevia_ck_theme             : 19.0.1.114.0 (inchangé, pas de CSS/SCSS à toucher)
```
Version cible après lot : `dorevia_ck_marketone_content : 19.0.1.75.0`

---

## 0. Corrections Dev apportées à la spec MOA reçue

### 0.1 Kicker hero — ajouté au périmètre (décision confirmée)

Le hero a une ligne "kicker" au-dessus du titre (`HERO_KICKER` dans `home_hero.py`), non mentionnée dans la spec MOA initiale. Valeur actuelle :

```
Boutique créole · Livraison France & Europe
```

Cette ligne reste 100 % "boutique" et contredirait visuellement le nouveau titre/sous-titre si elle n'était pas mise à jour. Décision : **le kicker entre dans le périmètre CK-HOME-001A.**

Proposition Dev (à valider MOA au même titre que le titre/sous-titre) :

```
Produits créoles · Producteurs · Savoir-faire
```

### 0.2 Localisation exacte des chaînes en dur à modifier

`hero_home_arch_is_valid()` référence la plupart de ses contrôles via les constantes du module (`HERO_TITLE`, `HERO_KICKER`, `HERO_CTA_PRO_LABEL`, etc.) : changer la constante suffit, le validateur suit automatiquement. **Une seule chaîne est en dur** et doit être éditée à la main, à deux endroits :

```
home_hero.py:139  build_home_hero_arch()       href="/professionnels" → href="/producteurs"
home_hero.py:193  hero_home_arch_is_valid()     'href="/professionnels"' in chunk → 'href="/producteurs"' in chunk
```

### 0.3 Tests existants qui vont casser (à mettre à jour, pas hors périmètre)

Contrairement à l'hypothèse §9.2 de la spec ("si aucun test automatisé spécifique n'existe, documenter"), **une couverture existe déjà** et contient des assertions sur l'ancien contenu. Elle doit être mise à jour dans ce ticket, sinon le run CI affichera un échec qui ressemblera à une régression :

```
tests/test_ck_home_lot1_hooks.py:39-44
  - assertIn(HERO_TITLE, arch)
  - assertIn(escape(HERO_KICKER), arch)
  - assertIn('href="/professionnels"', arch)   → doit devenir '/producteurs'
  - assertIn(HERO_CTA_PRO_LABEL, arch)

tests/test_ck_home_lot1_compose.py:50-53
  - assertIn('Boutique créole', chunk)          → doit être adapté au nouveau kicker
  - assertIn('Livraison France', chunk)         → doit être adapté au nouveau kicker
  - assertIn(HERO_CTA_PRO_LABEL, chunk)
```

Ces deux fichiers importent les constantes (`HERO_TITLE`, `HERO_KICKER`, `HERO_CTA_PRO_LABEL`, ...) depuis `home_hero.py` : si les constantes sont renommées (ex. `HERO_CTA_PRO_LABEL` → `HERO_CTA_PRODUCTEURS_LABEL`), les imports doivent suivre.

Note : `test_ck_home_lot1_compose.py:63` (`assertEqual(self.url_open('/professionnels').status_code, 200)`) reste valide sans modification — la page `/professionnels` existe toujours, seul le CTA hero ne pointe plus dessus.

### 0.4 Vérification faite : `/producteurs` est la route vivante

Il existe une ancienne page CMS `/nos-producteurs` (legacy, redirigée en 301 depuis migration `19.0.1.66.0`). La route réellement servie aujourd'hui est le contrôleur `controllers/producers.py` sur `/producteurs`, peuplée et recettée le 2026-06-30 (`RECETTE_QA_PRODUCTEURS_V1_VERDICT_20260630.md`). Le CTA secondaire vers `/producteurs` ne présente donc aucun risque de page vide ou cassée — confirmé, pas de vérification supplémentaire nécessaire au-delà d'un smoke test HTTP 200.

---

## 1. Contexte

*(inchangé — voir spec MOA)*

Le lot CK-HOME-001C est livré et recetté : newsletter FR, marque C-Kréyòl harmonisée, section "Acheter par univers" à 4 cartes avec Boissons, démo tunnel exploitable. Le hero actuel porte encore une promesse boutique-only :

```
Les saveurs créoles, prêtes à commander.
```

Objectif : repositionner le message vers produits créoles + producteurs + savoir-faire + France/Europe, sans refonte visuelle.

---

## 2. Texte MOA validé (+ kicker Dev à valider)

| Élément | Valeur |
|---|---|
| Kicker (nouveau, à valider MOA) | `Produits créoles · Producteurs · Savoir-faire` |
| Titre | `C-Kréyòl — les saveurs créoles en Europe` |
| Sous-titre | `Une sélection de produits, producteurs et savoir-faire créoles, à découvrir depuis la France et l'Europe.` |
| CTA principal | `Découvrir la boutique` → `/shop` |
| CTA secondaire | `Voir les producteurs` → `/producteurs` |

---

## 3. Périmètre technique (`dorevia_ck_marketone_content/home_hero.py`)

- Modifier `HERO_KICKER`, `HERO_TITLE`, `HERO_LEAD` (sous-titre), `HERO_CTA_SHOP_LABEL` (inchangé côté libellé si "Découvrir la boutique" diffère de l'actuel "Voir la boutique" — **à trancher : le libellé CTA principal change aussi**, voir §3bis), `HERO_CTA_PRO_LABEL` → renommer en constante reflétant "producteurs".
- Remplacer `href="/professionnels"` → `href="/producteurs"` aux deux emplacements identifiés en §0.2.
- Mettre à jour `tests/test_ck_home_lot1_hooks.py` et `tests/test_ck_home_lot1_compose.py` (voir §0.3).
- Bump manifest `19.0.1.74.0` → `19.0.1.75.0`.
- Créer `migrations/19.0.1.75.0/post-migrate.py` sur le patron de `migrations/19.0.1.74.0/post-migrate.py` (import + appel `bootstrap_home_hero(env)` + `cr.commit()` + log métier).

### 3bis — point à noter, pas bloquant

Le CTA principal actuel affiche `"Voir la boutique"` (`HERO_CTA_SHOP_LABEL`) ; la spec MOA demande `"Découvrir la boutique"`. C'est un changement de libellé en plus de ce que suggérait implicitement "mettre à jour les CTA" — confirmé inclus dans le périmètre, aucune action requise de votre part, simple signalement pour traçabilité du diff.

---

## 4. Bootstrap / migration

- `bootstrap_home_hero()` fait un court-circuit sur `hero_home_arch_is_valid()` : dès que les constantes ci-dessus changent, l'ancien arch en DB échoue automatiquement la validation (les checks référencent les constantes, pas des littéraux — sauf le `href` couvert en §0.2) → le bootstrap réécrit proprement l'ancien hero.
- Relancer via la migration `19.0.1.75.0` (upgrade module) — pas de commande manuelle supplémentaire nécessaire au-delà de l'upgrade standard.
- Le compte-rendu Dev/QA doit confirmer explicitement que l'ancien hero (`"Les saveurs créoles, prêtes à commander."`, `"Boutique créole"`, `href="/professionnels"`) n'apparaît plus dans le snapshot HTML `/`.

---

## 5. Règles UX (inchangées)

Conserver fond clair chaud, titre serif, CTA rouge/orange CK, hiérarchie actuelle. Aucun nouveau carrousel, image hero obligatoire, animation, ou refonte structurelle.

---

## 6. Critères d'acceptation

Reprendre CA1 à CA9 de la spec MOA initiale, **+ CA10** :

**CA10 — Kicker** : le hero affiche le nouveau kicker validé MOA (proposition Dev : `Produits créoles · Producteurs · Savoir-faire`), cohérent avec le titre/sous-titre — plus de mention "Boutique créole" isolée en tête de hero.

---

## 7. Recette QA — ajout au smoke test

En plus de la liste §9.1 de la spec MOA, ajouter :

```
Nouveau kicker hero visible et cohérent avec titre/sous-titre
tests/test_ck_home_lot1_hooks.py : PASS (assertions mises à jour)
tests/test_ck_home_lot1_compose.py : PASS (assertions mises à jour)
```

---

## 8. Hors scope (inchangé)

CK-HOME-001B, refonte /producteurs, /communaute, forum, blog, navigation header, newsletter, section univers, footer, SEO complet, déploiement prod, checkout.

---

## 9. Message de commit proposé

```
feat(ck-home): CK-HOME-001A repositionner le hero (titre, kicker, sous-titre, CTA producteurs)
```
