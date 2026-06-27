# Décision MOA — Note 08 · Fiche produit CK V1.1

| Champ | Valeur |
| --- | --- |
| Date | 27 juin 2026 |
| Référence | `note_08.md` |
| Version livrée | `dorevia_ck_marketone_content` **19.0.1.53.1** |
| Recette QA | [`RECETTE_QA_NOTE_08_VERDICT.md`](../design/maquette_01.2/RECETTE_QA_NOTE_08_VERDICT.md) |
| Retour Dev | [`note_08_reponse.md`](./note_08_reponse.md) |

---

## Décision

**GO avec réserves R1–R4.**

La livraison Note 08 est **acceptée** comme socle technique fiche produit CK V1.1 (modèle de données, BO, front zone haute, sections conditionnelles, badges, producteur).

Les corrections **BUG-N08-001** et **BUG-N08-002** identifiées en recette QA sont **intégrées** dans le commit de clôture Note 08.

---

## Réserves — suivi obligatoire

| ID | Sujet | Action | Ticket / statut |
| --- | --- | --- | --- |
| **R1** | Pas de limite BO sur `description_ecommerce` | Ticket polish BO (widget / gouvernance ~255 car.) | [`TICKET_POLISH_ACCROCHE_ECOMMERCE_NOTE08_R1.md`](./TICKET_POLISH_ACCROCHE_ECOMMERCE_NOTE08_R1.md) |
| **R2** | Ancre active JS au scroll | Validation visuelle MOA (desktop + mobile 390 px) | Prochain passage MOA sur Manio |
| **R3** | Paramétrage contenu Manio + La Platine incomplet (BO Odoo) | Ticket contenu MOA | [`TICKET_CONTENU_SEED_MANIO_PLATINE_NOTE08_R3.md`](./TICKET_CONTENU_SEED_MANIO_PLATINE_NOTE08_R3.md) |
| **R4** | Fallback `website_description` actif | Réserve transitoire jusqu’à migration champs dédiés | Suivi dans ticket R3 · pas de NO GO |

---

## Bugs corrigés (recette QA)

| ID | Correction |
| --- | --- |
| BUG-N08-001 | Label `Contenance` restauré (`product_page_tabs.py`) |
| BUG-N08-002 | XPath prix absolus variantes (`website_sale_product_page_v11.xml`) |

---

## Hors périmètre immédiat

- B2B fiche produit · avis clients · automatisation badges · fiche producteur CMS complète.

---

```text
Décision : GO avec réserves (R1–R4)
Commentaires : Socle technique accepté. Paramétrage contenu MOA (R3) et polish accroche (R1) à planifier.
Date : 27 juin 2026
Validé par : MOA
```
