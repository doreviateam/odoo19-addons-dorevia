# Note d’itération MOA — CK / Home e-commerce

| Statut | **Actée MOA** — 2026-06-13 · **pause Odoo · maquette V1.2.x vision complète** |
| Verdict QA | **OK note d’itération** — réserves mineures intégrées · base opposable V1.2 |
| Documents liés | [`decision_moa_pause_odoo_iteration_maquette_v1_2_x.md`](../design/maquette_01.2/decision_moa_pause_odoo_iteration_maquette_v1_2_x.md) · [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](../design/maquette_01.2/CADRAGE_MAQUETTE_CK_V1_2_X.md) · [`recette_qa_maquette_v1_2_x.md`](../design/maquette_01.2/recette_qa_maquette_v1_2_x.md) · [`ticket_moa_composition_cms_ck_01`](../design/ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) · [`recette_qa_composition_cms_ck_01`](../design/recette_qa_composition_cms_ck_01.md) · [`brief_01_2.md`](../design/maquette_01.2/brief_01_2.md) · [`recette_qa_maquette_01_2.md`](../design/maquette_01.2/recette_qa_maquette_01_2.md) · [`go_moa_maquette_01_2.md`](../design/maquette_01.2/go_moa_maquette_01_2.md) · [`arbitrage_moa_maquette_01_2.md`](../design/maquette_01.2/arbitrage_moa_maquette_01_2.md) |

---

## 1. Contexte

Une première phase de traduction de la maquette CK dans Odoo 19 CE a été menée sur l’instance `dorevia_ck_marketone_01`.

Cette phase a permis de vérifier que le socle technique est exploitable :

* le thème `dorevia_ck_theme` fonctionne ;
* le Website Builder permet de composer les pages ;
* les snippets natifs Odoo peuvent être utilisés ;
* le catalogue Odoo peut remonter des produits dans la home ;
* la logique “Odoo 19 CE · snippets first · pas de surcouche autonome” reste valide.

Le travail réalisé constitue donc une preuve de faisabilité technique et une première base CMS propre.

## 2. Constat MOA

La page d’accueil Odoo actuelle reste toutefois en dessous de l’intention commerciale portée par la maquette CK.

Elle reprend certains codes visuels, mais elle reste encore trop proche d’une première composition CMS simplifiée. Elle ne traduit pas suffisamment la densité e-commerce attendue : produits visibles rapidement, prix assumés, catégories actionnables, réassurance immédiate, entrée professionnelle structurée et parcours d’achat court.

La maquette elle-même doit également évoluer. Elle pose une direction esthétique pertinente, mais elle peut encore trop tirer vers une logique de vitrine premium, calme et contemplative.

Or CK n’est pas seulement une marque à présenter. CK est une boutique à faire fonctionner.

### Verdict QA — home Odoo actuelle (2026-06-13)

```text
OK socle technique
OK faisabilité CMS
KO traduction cible commerciale complète
```

La pause home **n’est pas un échec technique** : le socle Odoo et la composition Builder sont validés comme preuve de faisabilité. L’écart porte sur la **traduction commerciale** — densité produit, preuves, conversion — par rapport à la cible boutique élégante.

## 3. Doctrine révisée

La doctrine MOA évolue ainsi :

> CK doit être une boutique claire, désirable et rassurante, capable de déclencher l’achat rapidement, tout en conservant une identité soignée.

L’élégance reste un critère de qualité, mais elle n’est pas la finalité.
La finalité est la **conversion** : vendre davantage, rassurer plus vite, guider mieux, tout en conservant une identité visuelle cohérente.

**Conversion** (définition MOA) :

```text
Progression vers achat, consultation produit, ajout panier, contact professionnel ou qualification commerciale.
```

La conversion inclut donc la porte Pro et la qualification B2B, pas seulement le panier B2C.

Chaque écran doit donc répondre à au moins l’un de ces objectifs :

* donner envie d’un produit ;
* faciliter l’accès à une catégorie ;
* lever un doute d’achat ;
* rassurer sur la livraison, le paiement ou la qualité ;
* orienter clairement vers le panier, la boutique ou l’espace professionnel.

Une section belle mais qui ne montre ni produit, ni preuve, ni action utile devra être simplifiée, déplacée plus bas ou reformulée.

## 4. Nouvelle cible pour la home

La home CK doit évoluer d’une logique de vitrine premium vers une logique de boutique élégante.

La hiérarchie cible recommandée est la suivante :

1. Header marchand clair : marque, boutique, catégories, professionnels, recherche, panier.
2. Hero court : promesse CK + CTA boutique + CTA professionnel.
3. Réassurance immédiate : livraison, paiement sécurisé, producteurs sélectionnés, service client.
4. Produits mis en avant : coups de cœur, nouveautés, coffrets ou premières sélections.
5. Catégories / univers d’achat réellement actionnables.
6. Packs / coffrets découverte comme axe fort de conversion.
7. Espace professionnel : qualification producteurs et distributeurs.
8. Contenu éditorial / SEO placé plus bas.
9. Footer CK propre, sans contenu générique Odoo.

**Mobile** : l’ordre peut être encore plus strict qu’en desktop. Sur mobile, les **produits** et les **preuves** (réassurance) doivent apparaître **avant tout contenu éditorial long**. Ordre recommandé mobile :

1. Hero court
2. Preuves / réassurance
3. Produits (prix visibles)
4. Catégories actionnables
5. Espace pro
6. Éditorial / SEO · coffrets · footer

## 5. Rapport à Directos

Directos est une **référence d’efficacité e-commerce** — pas une référence d’identité CK.

```text
Directos = benchmark marchand (densité produit · prix · preuves · catégories)
Directos ≠ modèle graphique · identité · ton CK
```

Directos ne doit pas être copié graphiquement, mais il rappelle ce qu’une boutique en ligne doit faire fonctionner :

* rendre les produits visibles rapidement ;
* afficher les prix ;
* proposer des catégories actionnables ;
* répéter les messages de confiance ;
* clarifier la promesse logistique ;
* mettre en avant les coffrets et sélections ;
* rendre l’entrée professionnelle identifiable.

CK doit reprendre cette force marchande sans reprendre l’empilement visuel.
La cible est une boutique plus élégante, plus respirante, mais tout aussi efficace commercialement.

## 6. Décision MOA actée

La MOA **acte** que la maquette CK doit être reprise avant de poursuivre l’exécution CMS complète dans Odoo.

L’objectif n’est pas de repartir de zéro, mais de faire évoluer la maquette vers une version plus marchande :

> Maquette CK V1.2 — Boutique élégante

Cette V1.2 devra rester réaliste et traduisible dans Odoo Website Builder.
Elle ne devra pas introduire de logique de front autonome, de catalogue parallèle ou de parcours e-commerce hors Odoo.

## 7. Demande au Dev / maquettage

Il est demandé de faire évoluer la maquette CK selon la doctrine suivante :

* renforcer la visibilité immédiate des produits ;
* afficher les prix plus tôt ;
* rendre les catégories plus directement orientées achat ;
* intégrer la réassurance très haut dans la page ;
* mettre en avant les coups de cœur, nouveautés ou coffrets ;
* conserver l’entrée professionnelle ;
* nettoyer le header et le footer dans une logique CK ;
* maintenir une direction artistique soignée mais non contemplative ;
* prévoir une traduction réaliste dans Odoo 19 CE avec Website Builder et snippets.

## 8. Critères QA V1.2 — acceptation maquette

La maquette V1.2 sera **validée MOA/QA** lorsque les critères suivants sont remplis (testables en recette maquette) :

| # | Critère | Seuil |
|---|---------|-------|
| 1 | Produits visibles | Dans les **10 premières secondes** (above the fold desktop · 1er scroll mobile) |
| 2 | Prix visibles | Affichés sur **chaque carte produit** mise en avant |
| 3 | Preuves de confiance | **Au moins 3** visibles haut de page (livraison · paiement · qualité / producteurs · service) |
| 4 | Catégories actionnables | Liées à des **routes / filtres Odoo plausibles** (`/shop/category/…` · `product.public.category`) |
| 5 | CTA Pro | Lien ou ancre vers page Pro — **sans 404** |
| 6 | Footer | **Sans placeholder Odoo** (texte générique · liens morts · crédits template) |
| 7 | Sections complètes | **Aucune section placeholder ou vide** (pas de bloc « lorem » · pas de zone produit sans contenu) |
| 8 | Mobile | Produits + preuves **avant** éditorial long (cf. §4) |
| 9 | Traduisibilité Odoo | Chaque bloc mappable vers snippet natif ou CK Marketone — pas de front autonome |

Verdict attendu post-recette maquette :

```text
OK MAQUETTE CK V1.2 — BOUTIQUE ÉLÉGANTE
```

ou

```text
KO MAQUETTE V1.2 — corrections à reprendre (critères §8 non satisfaits)
```

## 9. Suite opérationnelle

L’exécution Odoo n’est pas abandonnée. Elle est simplement mise en pause sur la home complète le temps de réaligner la cible.

La séquence recommandée est :

1. ✅ finaliser la note MOA d’itération ;
2. ✅ transmettre la nouvelle doctrine au Dev / maquettage — [`brief_01_2.md`](../design/maquette_01.2/brief_01_2.md) ;
3. ✅ produire une maquette CK V1.2 — livrée Dev [`LIVRAISON_V1_2.md`](../design/maquette_01.2/LIVRAISON_V1_2.md) ;
4. ✅ valider MOA / QA cette nouvelle cible — critères §8 · [`recette_qa_maquette_01_2.md`](../design/maquette_01.2/recette_qa_maquette_01_2.md) · arbitrage [`arbitrage_moa_maquette_01_2.md`](../design/maquette_01.2/arbitrage_moa_maquette_01_2.md) ;
5. ☐ matérialiser vision CK en maquette V1.2.x — [`decision_moa_pause_odoo_iteration_maquette_v1_2_x.md`](../design/maquette_01.2/decision_moa_pause_odoo_iteration_maquette_v1_2_x.md) · [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](../design/maquette_01.2/CADRAGE_MAQUETTE_CK_V1_2_X.md) ;
6. ☐ reprendre la composition Odoo Website Builder bloc par bloc — **après** validation maquette ;
7. recetter chaque bloc selon deux critères : qualité perçue et efficacité commerciale.

**Documents opérationnels liés** (mise à jour 2026-06-13) :

| Document | Rôle |
|----------|------|
| [`ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md`](../design/ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) | Ticket CMS — §0.3 pause home · séquence reprise |
| [`recette_qa_composition_cms_ck_01.md`](../design/recette_qa_composition_cms_ck_01.md) | Recette QA — §7 pause · état partiel instance |
| [`REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md`](../design/REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md) | Instance recette — phase courante |
| [`points_a_arbitrer.md`](../design/maquette_01/points_a_arbitrer.md) | Arbitrages · évolution V1.2 |
| [`brief_01_2.md`](../design/maquette_01.2/brief_01_2.md) | Brief Dev/maquettage V1.2 — déclinaison opérationnelle |
| [`recette_qa_maquette_01_2.md`](../design/maquette_01.2/recette_qa_maquette_01_2.md) | Recette QA maquette V1.2 — exécutée · GO traduction post-arbitrage |
| [`arbitrage_moa_maquette_01_2.md`](../design/maquette_01.2/arbitrage_moa_maquette_01_2.md) | **Arbitrage MOA** — réserves acceptées · GO traduction Odoo |
| [`decision_moa_pause_odoo_iteration_maquette_v1_2_x.md`](../design/maquette_01.2/decision_moa_pause_odoo_iteration_maquette_v1_2_x.md) | **Décision MOA** — pause Odoo · matérialisation vision maquette |
| [`CADRAGE_MAQUETTE_CK_V1_2_X.md`](../design/maquette_01.2/CADRAGE_MAQUETTE_CK_V1_2_X.md) | Cadrage pages · concepts · arbitrage |
| [`go_moa_maquette_v1_2_x_lot1.md`](../design/maquette_01.2/go_moa_maquette_v1_2_x_lot1.md) | **GO MOA Lot 1** — accueil · fiche produit · professionnels |
| [`recette_qa_maquette_v1_2_x.md`](../design/maquette_01.2/recette_qa_maquette_v1_2_x.md) | Recette QA vision complète |
| [`ticket_dev_maquette_01_2_open_design.md`](../design/maquette_01.2/ticket_dev_maquette_01_2_open_design.md) | Ticket Dev — périmètre exécution |
| [`go_moa_maquette_01_2.md`](../design/maquette_01.2/go_moa_maquette_01_2.md) | **GO OFFICIEL MOA** — Move 3 |

## 10. Principe de travail

Le projet CK sera conduit par itérations courtes.

Chaque itération devra produire au moins l’un des résultats suivants :

* un meilleur rendu ;
* une meilleure compréhension ;
* une décision plus claire ;
* une réduction d’écart entre la maquette et Odoo ;
* une amélioration de la capacité commerciale du site.

Principe MOA retenu :

> Nous ne perdons jamais : nous apprenons, nous capitalisons, puis nous améliorons.
