# Note MOA — Livraisons Dev du 26 juin 2026

| Champ | Valeur |
| --- | --- |
| Date | 26 juin 2026 |
| Base cible | `dorevia_ck_marketone_01` |
| Destinataires | MOA, QA |
| Statut | Livré Dev — actions MOA et upgrade instance à planifier |

---

## Ce qui a été fait côté Dev

### 1. Axe C — Action 10 (champ produit « vedette » accueil)

**Module** : `dorevia_ck_marketone_content` version **19.0.1.42.0**

Sur la fiche produit, onglet **Ventes** > bloc **Classement boutique** :

| Avant | Après |
| --- | --- |
| En vedette | **Afficher sur l'accueil** |

L'infobulle du champ précise : *Affiche ce produit dans les sélections de la page d'accueil C-Kréyòl lorsque les règles de mise en avant le permettent.*

**Ce qui ne change pas pour vous :**

- La section Home **« Nos coups de cœur »** fonctionne comme avant : cochez **Afficher sur l'accueil** sur les produits à mettre en avant (max 4 cards visibles).
- Les cards boutique, catégories et navigation ne sont pas modifiées par ce ticket.

**Détail technique** : [`NOTE_LIVRAISON_AXE_C_ACTION_10.md`](NOTE_LIVRAISON_AXE_C_ACTION_10.md)

---

### 2. Header — logo C-Kréyòl en SVG

**Module** : `dorevia_ck_theme` version **19.0.1.59.0**

- Le logo texte « C-Kréyòl » + baseline « épicerie créole » est remplacé par le **logo SVG** CK (même visuel desktop et mobile).
- Accessibilité conservée : `aria-label="C-Kréyòl — Accueil"`.

**Recette QA** : [`RECETTE_QA_LOGO_HEADER_SVG_20260626.md`](../design/maquette_01.2/RECETTE_QA_LOGO_HEADER_SVG_20260626.md)

---

### 3. Documentation cadrage (pas d'impact site tant que non validé)

- **Note 07** : proposition d'évolution des pages catégories boutique (sidebar → drawer, grille pleine largeur) — **pas encore développée**, en attente validation MOA / Dev / QA.
- **Réponse Dev note 07** : faisabilité, estimation ~1 sprint court — [`note_07_reponse.md`](note_07_reponse.md)
- Protocole **Axe C** et recette produit seed v1 — références QA.

---

## Ce que la MOA doit faire sur l'instance

### Après upgrade modules (voir ci-dessous)

1. **Vérifier le libellé BO** : ouvrir un produit > Ventes > **Afficher sur l'accueil** visible et compréhensible.
2. **Vérifier le logo** sur `/` desktop et mobile 390 px.

### Protocole Axe C — toujours en attente MOA

Les corrections catalogue suivantes restent **à votre charge en back-office** (le Dev ne les déclenche pas) :

| # | Action | Statut |
| --- | --- | --- |
| 1–3 | Retirer « Coups de cœur » des produits, menu, filmstrip | À faire / vérifier |
| 5abc | Traductions fr_FR (Origine, Galettes de manioc, sous-catégories) | À faire |
| 7/8 | UOM g/kg + prix réf. (Confiture, Crackers, Galettes, Savon) ; Panama sans prix réf. | À faire |
| 9 | Menu « Maison & Bien-être » → **Soin & Bien-être** | Partiellement traité nav ; vérifier cohérence |
| **MOA-1** | Supprimer ou laisser vide la catégorie « Coups de cœur » en base ? | **Arbitrage requis** |
| **MOA-2** | Contenance et prix réf. Jus Mont-Pelé, Pâte de manioc | **Arbitrage requis** |

**Avis Dev sur « Coups de cœur » (catégorie)** : la homepage ne dépend plus de cette catégorie. Vous pouvez la **vider et ne plus l'exposer** sans risque pour l'accueil. Une suppression physique en BO est possible si les produits n'y sont plus rattachés ; un futur upgrade technique pourrait la recréer — en cas de doute, **laisser vide et invisible** suffit.

Référence : [`PROTOCOLE_QA_AXE_C_SECURISATION_BO_20260624.md`](../design/maquette_01.2/PROTOCOLE_QA_AXE_C_SECURISATION_BO_20260624.md)

---

## Mise à jour instance (équipe technique)

À exécuter sur `dorevia_ck_marketone_01` :

```text
1. -u dorevia_ck_theme        (migration 19.0.1.59.0 — purge anciennes vues logo)
2. Redémarrage worker Odoo
3. -u dorevia_ck_marketone_content   (libellé Afficher sur l'accueil)
4. Redémarrage worker Odoo
```

Puis recette MOA / QA selon les checklists ci-dessus.

---

## Prochaines étapes suggérées

| Priorité | Sujet | Responsable |
| --- | --- | --- |
| 1 | Upgrade instance + QA logo + libellé BO | Tech + MOA/QA |
| 2 | Arbitrages MOA-1 / MOA-2 + corrections BO Axe C | MOA |
| 3 | Recette post-correction catalogue (`RECETTE_QA_CALE_PRODUIT_V1_POST_CORRECTION`) | QA |
| 4 | Validation approche **note 07** (pages catégories) avant tout Dev | MOA + Produit |

---

*Note de communication MOA — livraisons Dev 26 juin 2026*
