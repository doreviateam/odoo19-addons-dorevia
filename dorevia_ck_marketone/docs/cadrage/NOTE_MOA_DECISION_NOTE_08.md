# Décision MOA — Note 08 · Fiche produit CK V1.1

| Champ | Valeur |
| --- | --- |
| Date | 27 juin 2026 |
| Référence | `note_08.md` |
| Version livrée | `dorevia_ck_marketone_content` **19.0.1.54.0** · `dorevia_ck_theme` **19.0.1.80.0** |
| Recette QA | [`RECETTE_QA_NOTE_08_VERDICT.md`](../design/maquette_01.2/RECETTE_QA_NOTE_08_VERDICT.md) |
| Retour Dev | [`note_08_reponse.md`](./note_08_reponse.md) |

---

## Décision

**GO avec réserve résiduelle R2.**

La livraison Note 08 est **acceptée** comme socle technique fiche produit CK V1.1 (modèle de données, BO, front zone haute, sections conditionnelles, badges, producteur).

Les corrections **BUG-N08-001** et **BUG-N08-002** identifiées en recette QA sont **intégrées** (commit `09793d7`).  
Les réserves **R1**, **R3** et **R4** sont **levées** au 27 juin 2026. Seule **R2** (ancre active JS au scroll) reste à valider visuellement par MOA.

---

## Réserves — suivi obligatoire

| ID | Sujet | Statut | Référence |
| --- | --- | --- | --- |
| **R1** | Limite accroche `description_ecommerce` | **✅ Levée** — contrainte ≤255 car. + help BO + `line-clamp: 3` front (`44954a9`) | [`TICKET_POLISH_ACCROCHE_ECOMMERCE_NOTE08_R1.md`](./TICKET_POLISH_ACCROCHE_ECOMMERCE_NOTE08_R1.md) |
| **R2** | Ancre active JS au scroll | **🔶 Résiduelle** — validation visuelle MOA (desktop + 390 px) | Prochain passage MOA sur Manio |
| **R3** | Paramétrage contenu Manio + SARL La Platine | **✅ Levée** — seed BO 27/06/2026 | [`TICKET_CONTENU_SEED_MANIO_PLATINE_NOTE08_R3.md`](./TICKET_CONTENU_SEED_MANIO_PLATINE_NOTE08_R3.md) |
| **R4** | Fallback `website_description` | **✅ Levée** — garde-fou V1.1 · `website_description` vide sur Manio | Dev `44954a9` + clôture MOA R3 |

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
Décision : GO avec réserve résiduelle R2
Commentaires : Socle technique accepté. R1/R3/R4 levées 27/06/2026. R2 = validation visuelle ancres au scroll.
Date : 27 juin 2026
Validé par : MOA
```
