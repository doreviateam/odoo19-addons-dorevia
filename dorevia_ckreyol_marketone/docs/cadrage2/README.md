Recadrage Dev — CK doit redevenir « odoo-iste »

Nous avons beaucoup avancé sur le front-office CK, mais je souhaite maintenant recadrer l'architecture globale.

La cible CK n'est pas un front externe piloté par des champs techniques dispersés dans Odoo.
La cible est un site basé sur le **standard Odoo eCommerce** :

```text
Socle obligatoire Marketone
  Website · eCommerce (website_sale) · Portal · Wishlist (website_sale_wishlist)

Données et processus natifs
  Produits Odoo · Catégories eCommerce · Attributs / variantes · Images produits
  Catalogue / vente / stock / facturation Odoo

Hors socle Marketone (sauf ticket MOA + ADR dédiés)
  website_blog · website_forum
```

Le back-office doit rester lisible, maintenable et conforme à la logique Odoo.

---

## Doctrine cadrage2 — ADR-034 (validée MOA 2026-06-08)

```text
Odoo exécute. Marketone habille et oriente.
```

| Règle | Application |
|-------|-------------|
| Odoo standard d'abord | Spécifique uniquement si le standard ne couvre pas le besoin |
| `website_sale` souverain | Pas de moteur catalogue / panier / checkout / prix / promo / paiement / livraison parallèle |
| Blog / Forum | **Non requis** au socle — Culture et Savoirs utilisent d'autres conteneurs (ADR Culture / Savoirs) |
| Front compatible natif | Héritage QWeb · extension contrôleur · matrice eCommerce § [`ARBITRAGE_ARCHITECTURE_CADRAGE2.md`](./ARBITRAGE_ARCHITECTURE_CADRAGE2.md) |
| Reprise lots front | Autorisée **lot par lot** — voir [`REPRISE_LOTS_FRONT_CADRAGE2.md`](./REPRISE_LOTS_FRONT_CADRAGE2.md) |

---

## Historique directive initiale (2026-06-08)

La directive initiale mentionnait Blog et Forum comme briques à « vérifier ». L'arbitrage MOA ([ADR-034](../cadrage/DECISIONS.md#adr-034--arbitrage-architecture-cadrage2-socle-odoo-natif)) a tranché : **ils ne sont pas requis au socle Marketone**.

Travail BO produit : **clôturé** (`19.0.16.0.0` — GO avec réserves).

Travail restant cadrage2 :

- ~~Recadrage fiche produit BO~~ ✓
- ~~Arbitrage Blog / Forum + matrice eCommerce~~ ✓ ADR-034
- ~~**Lot 6.3a Promo**~~ ✓ **GO clôture MOA** `19.0.17.0.0` — [`RECEPTION_MOA_LOT6_3A_PROMO.md`](./RECEPTION_MOA_LOT6_3A_PROMO.md)
- ~~**Lot 6.3b Kits & Coffrets**~~ ✓ **GO clôture MOA** `19.0.18.0.0` — [`RECEPTION_MOA_LOT6_3B_PACK.md`](./RECEPTION_MOA_LOT6_3B_PACK.md)
- Reprise progressive autres lots front gelés (recette « fonctionnalité Odoo native préservée »)

---

## Documents du recadrage

| Document | Rôle |
|----------|------|
| [`README.md`](./README.md) | Directive MOA (ce fichier) |
| [`RETOUR_EXPERT_RECADRAGE.md`](./RETOUR_EXPERT_RECADRAGE.md) | Retour d'expert — analyse code v19.0.15.14.1 |
| [`DECISION_MOA_RECADRAGE_BO.md`](./DECISION_MOA_RECADRAGE_BO.md) | Décision MOA — recadrage BO prioritaire, gel front |
| [`PROPOSITION_LOT_RECADRAGE_BO_PRODUIT.md`](./PROPOSITION_LOT_RECADRAGE_BO_PRODUIT.md) | Proposition Dev — restructuration fiche produit |
| [`NOTE_LIVRAISON_LOT_RECADRAGE_BO.md`](./NOTE_LIVRAISON_LOT_RECADRAGE_BO.md) | Livraison Dev `19.0.16.0.0` |
| [`RECETTE_MANUELLE_RECADRAGE_BO_PRODUIT.md`](./RECETTE_MANUELLE_RECADRAGE_BO_PRODUIT.md) | Recette manuelle — GO avec réserves MOA |
| [`RECEPTION_MOA_LOT_RECADRAGE_BO.md`](./RECEPTION_MOA_LOT_RECADRAGE_BO.md) | Clôture lot BO |
| [`ARBITRAGE_ARCHITECTURE_CADRAGE2.md`](./ARBITRAGE_ARCHITECTURE_CADRAGE2.md) | **Arbitrage validé MOA** — matrice eCommerce · ADR-034 |
| [`REPRISE_LOTS_FRONT_CADRAGE2.md`](./REPRISE_LOTS_FRONT_CADRAGE2.md) | Reprise lots front gelés — checklist + template recette |
| [`TICKET_LOT6_3_PORTE_PROMO_PACK.md`](./TICKET_LOT6_3_PORTE_PROMO_PACK.md) | Lot 6.3 — cadrage **GO MOA** (2026-06-08) |
| [`../tickets/lots/TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_3A_PORTE_PROMO_EXEC.md) | **Lot 6.3a** — `19.0.17.0.0` · **GO clôture MOA** |
| [`RECEPTION_MOA_LOT6_3A_PROMO.md`](./RECEPTION_MOA_LOT6_3A_PROMO.md) | Réception MOA Lot 6.3a |
| [`PREP_RECETTE_LOT6_3A_PROMO.md`](./PREP_RECETTE_LOT6_3A_PROMO.md) | Jeu de données recette navigateur |
| [`NOTE_LIVRAISON_LOT6_3A_PROMO.md`](./NOTE_LIVRAISON_LOT6_3A_PROMO.md) | Livraison Dev `19.0.17.0.0` |
| [`TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md`](./TICKET_LOT6_3B_PORTE_KITS_COFFRETS.md) | **Lot 6.3b** — **GO clôture MOA** · `product_pack` |
| [`FICHE_MOA_LOT6_3B_KITS_COFFRETS.md`](./FICHE_MOA_LOT6_3B_KITS_COFFRETS.md) | **Fiche réunion MOA** — arbitrage K1–K9 |
| [`DECISION_MOA_LOT6_3B_KITS_COFFRETS.md`](./DECISION_MOA_LOT6_3B_KITS_COFFRETS.md) | **Décision MOA** — GO cadrage avec réserves |
| [`../tickets/lots/TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md`](../tickets/lots/TICKET_MARKETONE_LOT6_3B_PORTE_PACK_EXEC.md) | **Lot 6.3b** — `19.0.18.0.0` · **GO clôture MOA** |
| [`../recette/lots/RECETTE_MANUELLE_LOT6_3B_PACK.md`](../recette/lots/RECETTE_MANUELLE_LOT6_3B_PACK.md) | Recette Lot 6.3b — **GO clôture MOA** |
| [`RECEPTION_MOA_LOT6_3B_PACK.md`](./RECEPTION_MOA_LOT6_3B_PACK.md) | Réception MOA Lot 6.3b |
| [`DIAGNOSTIC_MOA_SALE_PRODUCT_PACK_19.md`](./DIAGNOSTIC_MOA_SALE_PRODUCT_PACK_19.md) | Diagnostic port OCA `sale_product_pack` · priorité MOA |
| [`NOTE_PHASE_A_SALE_PRODUCT_PACK_OCA_19.md`](./NOTE_PHASE_A_SALE_PRODUCT_PACK_OCA_19.md) | Phase A — sync OCA · **GO MOA** |
| [`ATELIER_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./ATELIER_MOA_PHASE_B_SALE_PRODUCT_PACK.md) | Atelier Phase B — **clôturé** |
| [`DECISION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./DECISION_MOA_PHASE_B_SALE_PRODUCT_PACK.md) | **Décision MOA Phase B** — pilote `detailed` |
| [`RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md) | **Réception MOA** — lexique GO · prochaine marche confirmés |
| [`NOTE_EXECUTION_ETAPE1_PHASE_B_SALE_PRODUCT_PACK.md`](./NOTE_EXECUTION_ETAPE1_PHASE_B_SALE_PRODUCT_PACK.md) | **Étape 1** — merge PR #1 · sandbox · prep |
| [`NOTE_EXECUTION_RECETTE_PHASE_B_SALE_PRODUCT_PACK.md`](./NOTE_EXECUTION_RECETTE_PHASE_B_SALE_PRODUCT_PACK.md) | **Recette B1–B6** — GO avec réserve perf sandbox |
| [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](./DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md) | Doctrine pack = article · filière pack **clôturée** |
| [`DECISION_MOA_SEO_PORTES_SHOP.md`](./DECISION_MOA_SEO_PORTES_SHOP.md) | Décision MOA SEO portes D1–D6 |
| [`CADRAGE_SEO_PORTES_SHOP.md`](./CADRAGE_SEO_PORTES_SHOP.md) | SEO portes `/shop` — canonical / noindex |
| [`../tickets/boutique/TICKET_MARKETONE_SEO_PORTES_SHOP.md`](../tickets/boutique/TICKET_MARKETONE_SEO_PORTES_SHOP.md) | Ticket SEO portes |
| [`NOTE_EXECUTION_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md`](./NOTE_EXECUTION_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md) | Observation technique O1–O6 + F1–F3 |
| [`PREP_RECETTE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](./PREP_RECETTE_PHASE_B_SALE_PRODUCT_PACK_BO.md) | Préparation recette BO pack **7**/**8** |
| [`../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md) | Maintenance explosion composants |

### Statut cadrage2

| Lot / sujet | Version | Verdict |
|-------------|---------|---------|
| Recadrage BO produit | `19.0.16.0.0` | **GO avec réserves MOA** (2026-06-08) |
| Arbitrage architecture | ADR-034 | **Validé MOA** (2026-06-08) |
| Reprise lots front gelés | — | **Autorisée** — Lots 6.3a · 6.3b **GO clôture MOA** |
| Lot 6.3a Promo | `19.0.17.0.0` | **GO MOA clôturé** (2026-06-08) |
| Lot 6.3b Kits & Coffrets | `19.0.18.0.0` | **GO MOA clôturé** (2026-06-08) |
| Maintenance `sale_product_pack` | — | **Clôturé MOA** — [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](./DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md) |
| SEO portes `/shop` | **19.0.19.0.0** | **GO MOA D1–D6** — [`DECISION_MOA_SEO_PORTES_SHOP.md`](./DECISION_MOA_SEO_PORTES_SHOP.md) |
