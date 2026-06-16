# Acte MOA — GO merge PR #73 · Section 3 Nos coups de cœur

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-15 |
| **PR** | [#73](https://github.com/doreviateam/odoo19-addons-dorevia/pull/73) |
| **Section** | Home V1 — Section 3 · Nos coups de cœur |
| **Base** | `main` (post-merge #72 · `e9a2965`) |
| **Branche** | `feat/ck-home-section3-featured-images` |

---

## 1. Contexte

La PR #73 livre le rapprochement maquette de la Section 3 home :

- titre **« Nos coups de cœur »** ;
- cartes SSR CK (images, chips, badges, CTA **« Voir »**) ;
- BO Odoo standard comme source de vérité ;
- catalogue MOA : Manio Crackers (2 variantes Format) + Galettes séparées.

Revue QA complémentaire : commentaire [PR #73 #issuecomment-4711120495](https://github.com/doreviateam/odoo19-addons-dorevia/pull/73#issuecomment-4711120495).

---

## 2. Résultats QA retenus

| Contrôle | Résultat |
|----------|----------|
| `mergeState` | `CLEAN` |
| GitGuardian | Vert |
| Tests auto | **31/31 OK** · `0 failed` · `0 error` |
| Runtime 1280 / 390 | 5 cartes SSR · médias hauteur stable · pas d’overflow · pas de carousel natif |
| Liens cartes | OK (`/shop`, Confiture, Manio `attribute_values=2/3`, Galettes, Savon) |
| Non-régression S1/S2 | Confirmée |

**Verdict QA** : **GO sous réserves — favorable au merge**.

---

## 3. Réserves MOA maintenues (post-merge)

Avant **validation visuelle finale** Section 3 :

- visuel BO **Confiture de goyave** — à remplacer ou qualifier ;
- visuel BO **Galettes de manioc** — à remplacer ou qualifier.

Ces réserves **ne bloquent pas** le merge technique #73.

---

## 4. Décision MOA

```text
Décision : GO merge PR #73 dans main.
Périmètre strict Section 3 confirmé.
Section 4 Catégories : interdite avant recette post-merge favorable.
```

---

## 5. Recette post-merge attendue

- hash de merge ;
- upgrade `dorevia_ck_theme` + `dorevia_ck_marketone_content` sur `dorevia_ck_marketone_01` ;
- contrôle home 1280/390 : Section 3 + non-régression S1/S2 ;
- levée progressive des réserves visuels BO (Goyave · Galettes).

---

## 6. Garde-fous maintenus

Pas d’ouverture : Section 4 · Lot 6 polish · Chantier B · SEO · Header · reprise Hero · reprise Section 2 (sauf régression).

---

## Verdict MOA

**GO merge PR #73.**
**Réserves visuels BO maintenues pour validation finale Section 3.**

---

*Acte MOA PR #73 — Section 3 Nos coups de cœur · 2026-06-15.*
