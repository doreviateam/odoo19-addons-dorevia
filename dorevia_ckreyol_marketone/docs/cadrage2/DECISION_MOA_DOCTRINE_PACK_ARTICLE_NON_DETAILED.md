# Décision MOA — Doctrine pack CK · **pack = article** · `non_detailed`

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-08 |
| **Verdict** | **GO doctrine `non_detailed`** pour les packs CK |
| **Ticket** | [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md) |
| **Pilote contrôlé** | [`DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md`](./DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md) · [`CADRE_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md`](./CADRE_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md) |
| **Recette Phase B** | [`RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](../recette/maintenance/RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md) |
| **ADR** | [ADR-035](../cadrage/DECISIONS.md#adr-035--activation-product_pack-lot-63b-kits--coffrets) — amendement doctrine pack |

---

## Doctrine opposable

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

**Pour CK Marketone, un pack / coffret est un article commercial à part entière.**

---

## Décision MOA

| Sujet | Décision |
|-------|----------|
| **Doctrine cible packs CK** | **`non_detailed`** — pack = **1 article** |
| **Pack 8** | **Référence doctrine fonctionnelle cible** |
| **Pack 7 `detailed`** | **Preuve technique conservée** — **n’est pas** la cible métier |
| **Généralisation `detailed`** | **NON** — définitivement écartée à ce stade |
| **`sale_product_pack` CK** | **Veille technique** · **pas d’activation métier** |
| **`product_pack` Marketone** | **Maintenu** — `pack_ok` · porte Kits & Coffrets |
| **Marketone** | **Aucune modification** · pas de `depends` `sale_product_pack` |
| **Moteur pack Marketone** | **Interdit** |

---

## Doctrine cible `non_detailed`

| Processus | Comportement attendu |
|-----------|---------------------|
| **Panier** | **1 ligne** pack |
| **Commande** | **1 ligne** pack |
| **Préparation** | **1 ligne** pack |
| **Facture** | **1 ligne** pack |
| **Prix** | Porté par le **pack parent** |
| **Composants** | **Pas d’explosion par défaut** en vente / stock / prépa / facture |

Aligné avec le lot **6.3b** clôturé et le témoin pack **8**.

---

## Bilan pilote `detailed` (pack 7)

| Élément | Statut |
|---------|--------|
| Chaîne OCA `sale_product_pack` | **Fonctionnelle** — preuve technique Phase B |
| Intérêt métier `detailed` | **Insuffisant** pour devenir doctrine CK |
| Cible métier retenue | **`non_detailed`** — pack **8** |

Le test **`detailed`** du pack **7** reste documenté comme **recette / preuve OCA**, sans bascule catalogue ni activation métier.

---

## Conséquences opposables

| Zone | Conséquence |
|------|-------------|
| **Catalogue packs CK** | **`non_detailed`** · pas de généralisation `detailed` |
| **`sale_product_pack`** | **Hors activation métier CK** — veille technique plateforme |
| **`product_pack`** | **Utile et maintenu** — identification `pack_ok` · porte `/shop?marketone_mode=pack` · alias `/kits` |
| **Marketone** | Inchangé · pas de moteur pack |
| **Lot 6.3b front** | **Non rouvert** — doctrine déjà alignée v1 |
| **Activation prod `sale_product_pack`** | **NO GO** pour CK Marketone |
| **#229 `website_sale_product_pack`** | **Hors scope** — checkout `detailed` non requis |

---

## Restauration config catalogue *(sandbox / prod)*

Revenir à la doctrine **`non_detailed`** sur les packs recette :

```bash
docker exec -i sandbox-odoo19-odoo-1 odoo shell -d ckr-marketone-01 --no-http \
  < odoo19-addons-dorevia/dorevia_ckreyol_marketone/scripts/prep_recette_lot6_3b_pack.py
```

Remet packs **7** et **8** en `non_detailed` + `ignored` (config 6.3b).

---

## Verdict MOA

| Date | Verdict |
|------|---------|
| 2026-06-08 | ☑ **GO doctrine `non_detailed` packs CK** |
| 2026-06-08 | ☑ **`sale_product_pack` en veille technique** · ☐ **activation métier CK** |
| 2026-06-08 | ☑ **NON généralisation `detailed`** · ☐ **GO activation prod `sale_product_pack` CK** |

---

## Statut filière MOA

**Filière `sale_product_pack` fermée côté MOA** — reprise lots front gelés ou autres sujets métier.

| Élément | Statut actif |
|---------|--------------|
| Doctrine packs CK | **Pack = article** · **`non_detailed`** |
| `product_pack` Marketone | **Actif** — `pack_ok` · porte Kits & Coffrets |
| `sale_product_pack` CK | **Veille technique** · **NO GO activation métier** |
| Lot **6.3b front** | **Aligné** · **non rouvert** |

### Documents historiques *(traces — pas doctrine active)*

Les documents Phase A / Phase B / pilote pack **7** `detailed` restent comme **preuve technique et recette** :

- [`NOTE_PHASE_A_SALE_PRODUCT_PACK_OCA_19.md`](./NOTE_PHASE_A_SALE_PRODUCT_PACK_OCA_19.md) · [`DECISION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./DECISION_MOA_PHASE_B_SALE_PRODUCT_PACK.md)
- [`RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](../recette/maintenance/RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md) · [`CADRE_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md`](./CADRE_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md)

**Verdict final opposable** : ce document · ticket maintenance · réception Phase B · **ADR-035**.

---

## Références

- [`ARBITRAGE_MOA_POST_PHASE_B_SALE_PRODUCT_PACK.md`](./ARBITRAGE_MOA_POST_PHASE_B_SALE_PRODUCT_PACK.md)
- [`DECISION_MOA_LOT6_3B_KITS_COFFRETS.md`](./DECISION_MOA_LOT6_3B_KITS_COFFRETS.md)
- [`RECEPTION_MOA_LOT6_3B_PACK.md`](./RECEPTION_MOA_LOT6_3B_PACK.md)
