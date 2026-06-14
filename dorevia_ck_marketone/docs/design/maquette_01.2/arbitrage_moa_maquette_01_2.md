# Arbitrage MOA — Maquette CK V1.2 · Boutique élégante

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Move** | **Move 3** — suite recette QA maquette V1.2 |
| **Validateur MOA** | MOA CK |
| **Date** | 2026-06-13 |
| **Recette source** | [`recette_qa_maquette_01_2.md`](./recette_qa_maquette_01_2.md) |
| **Verdict recette** | `OK PARTIEL MAQUETTE V1.2 — réserves à lever avant traduction Odoo` |
| **Décision** | **GO TRADUCTION ODOO — MAQUETTE CK V1.2 AVEC RÉSERVES MOA ACCEPTÉES** |

```text
GO TRADUCTION ODOO — MAQUETTE CK V1.2
AVEC RÉSERVES MOA ACCEPTÉES
```

---

## 1. Contexte

Suite à la recette QA relancée sur la maquette CK V1.2, le verdict QA est :

```text
OK PARTIEL MAQUETTE V1.2 — réserves à lever avant traduction Odoo
```

Les **critères bloquants** sont validés.

La maquette répond à la doctrine « boutique élégante » :

* ordre des blocs conforme : hero → réassurance → produits → catégories → coffret → Pro → éditorial → footer ;
* 4 preuves de confiance visibles haut de page ;
* 6 produits affichés avec prix ;
* CTA produits limités à `Voir` / `Découvrir` ;
* catégories liées à des routes `/shop/category/...` plausibles ;
* entrée Pro visible dans le header, le hero et le bandeau Pro ;
* mobile conforme : pas d’overflow, burger OK, preuves puis produits avant éditorial long ;
* footer sans placeholder Odoo.

La maquette est jugée **suffisamment solide pour préparer la traduction Odoo**, sous réserve des arbitrages MOA ci-dessous.

---

## 2. Réserves arbitrées

### 2.1 Promesses commerciales

Les éléments de réassurance affichés — livraison, paiement sécurisé, producteurs sélectionnés, service client — sont **validés en intention**.

| Arbitrage MOA | `ACCEPTÉ AVEC RÉSERVE` |
|---------------|------------------------|

Ces promesses pourront être conservées dans la traduction Odoo, à condition d’être reformulées de manière tenable opérationnellement si nécessaire.

Exemples :

* « Livraison France / Europe » pourra être ajusté selon la promesse logistique réellement activée ;
* « Paiement sécurisé » sera conservé si le parcours paiement cible est confirmé ;
* « Producteurs sélectionnés » est cohérent avec la doctrine CK ;
* « Service client » doit correspondre à un canal de contact réel.

### 2.2 Page `/professionnels`

Le lien `/professionnels` est conforme dans la maquette, mais la page n’est pas encore composée dans Odoo.

| Arbitrage MOA | `ACCEPTÉ — À PRODUIRE EN PARALLÈLE ODOO` |
|---------------|------------------------------------------|

La page `/professionnels` doit être créée **avant mise en ligne publique** ou recette finale de la home Odoo, afin d’éviter tout 404.

### 2.3 Routes et liens fictifs

Certaines routes de maquette restent fictives ou à mapper : fiches produits, logo en `#`, `/legal`.

| Arbitrage MOA | `ACCEPTÉ POUR MAQUETTE — À MAPPER LORS DE LA TRADUCTION ODOO` |
|---------------|----------------------------------------------------------------|

La traduction Odoo devra vérifier que chaque CTA principal pointe vers :

* une page existante ;
* une route Odoo ;
* une catégorie e-commerce ;
* une fiche produit ;
* une ancre réelle ;
* ou une page explicitement prévue.

### 2.4 Visuels placeholders

Les visuels hero, produits, cartes et coffret restent des placeholders assumés dans la livraison maquette.

| Arbitrage MOA | `ACCEPTÉ POUR TRADUCTION STRUCTURELLE — RÉSERVE VISUELLE À LEVER AVANT RECETTE FINALE` |
|---------------|----------------------------------------------------------------------------------------|

La traduction Odoo peut démarrer sur la **structure**, mais les visuels devront être remplacés ou améliorés avant validation finale de qualité perçue.

### 2.5 Univers Artisanat

L’univers **Artisanat** n’est pas mis en avant dans la maquette V1.2.

| Arbitrage MOA | `ACCEPTÉ — ARTISANAT NON PRIORITAIRE PHASE 1` |
|---------------|------------------------------------------------|

La phase 1 reste centrée sur les produits créoles vendables immédiatement : épicerie, agro-transformation, boissons, bien-être cohérent, coffrets / découvertes.

L’univers Artisanat pourra être réintroduit plus tard si le catalogue réel le justifie.

---

## 3. Décision MOA

La MOA **accepte les réserves** ci-dessus et **autorise la reprise de la traduction Odoo** bloc par bloc.

```text
GO TRADUCTION ODOO — MAQUETTE CK V1.2
AVEC RÉSERVES MOA ACCEPTÉES
```

---

## 4. Périmètre de reprise Odoo

Ordre d’exécution — cf. [`TABLEAU_TRADUCTION_ODOO_V1_2.md`](./TABLEAU_TRADUCTION_ODOO_V1_2.md) · [`ticket_moa_composition_cms_ck_01`](../ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) §0.4 :

1. Header ;
2. Hero ;
3. Réassurance ;
4. Produits mis en avant ;
5. Catégories ;
6. Coffret / découverte ;
7. Espace professionnel ;
8. Éditorial ;
9. Footer ;
10. Revalidation desktop + mobile — [`recette_qa_composition_cms_ck_01.md`](../recette_qa_composition_cms_ck_01.md).

---

## 5. Garde-fous maintenus

```text
Odoo 19 CE
Website Builder
snippets first
pas de surcouche autonome
pas de catalogue parallèle
pas de panier / checkout custom
pas de logique B2B custom
```

La home Odoo reprend **uniquement** selon la maquette V1.2 recettée et les réserves MOA acceptées ci-dessus.

---

## 6. Documents liés

| Document | Rôle |
|----------|------|
| [`note_05.md`](../../cadrage/note_05.md) | Doctrine · séquence opérationnelle |
| [`go_moa_maquette_01_2.md`](./go_moa_maquette_01_2.md) | GO production maquette · Move 3 |
| [`recette_qa_maquette_01_2.md`](./recette_qa_maquette_01_2.md) | Recette QA · verdict OK PARTIEL |
| [`ticket_moa_composition_cms_ck_01`](../ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) | Ticket CMS · reprise home |
| [`TABLEAU_TRADUCTION_ODOO_V1_2.md`](./TABLEAU_TRADUCTION_ODOO_V1_2.md) | Mapping bloc par bloc |

---

*Arbitrage MOA — maquette CK V1.2 · GO traduction Odoo · 2026-06-13.*
