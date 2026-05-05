# MVP 03 — Comptes clients C-Kreyol

Dossier de **cadrage** pour la vague **MVP 03** : parcours de **création de compte** et **demande compte professionnel**, distinct de **`docs/mvp_01/`** (catalogue / portes `shop`) et **`docs/mvp_02/`** (homepage, boutique wave 1…).

**Statut documentaire** : intention et principes **gelés au niveau produit** ; **pas de ticket d’exécution** ni de PV de recette référencés ici tant que le chantier n’est pas ouvert côté dev.

> MVP_03 prépare la distinction entre **compte particulier** et **demande de compte professionnel**, sans créer immédiatement une mécanique B2B lourde ni une **boutique parallèle** — alignement [doctrine B2C/B2B](../direction/DOCTRINE_CK_ECOMMERCE_B2C_B2B.md), [ADR-010](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-010).

**Documents du dossier**

| Document | Rôle |
|----------|------|
| [1_COMPTE_CLIENT_PARCOURS.md](1_COMPTE_CLIENT_PARCOURS.md) | Parcours **particulier** vs **demande compte pro**, états, points d’entrée, arbitrages et critères de recette cible |
| [2_COMPTE_CLIENT_SPEC_UX.md](2_COMPTE_CLIENT_SPEC_UX.md) | Spec **UX** : écrans cibles, ton et messages, états, critères recette interface, arbitrages MOA — suite du parcours |

---

## Intention

Structurer la création de compte client sur C-Kreyol en distinguant deux parcours :

1. **Compte particulier** — création de compte client **classique** (B2C).
2. **Demande de compte professionnel / entreprise** — **demande** d’ouverture compte pro, **sans** accès automatique aux conditions professionnelles ; soumise à **validation** métier / exploitation Odoo.

---

## Doctrine (résumé)

Le **compte particulier** correspond à une inscription client standard (tunnel Odoo / portail selon arbitrage technique).

Le **compte entreprise** **ne donne pas** automatiquement accès aux tarifs ou conditions **B2B**. Il s’agit d’une **demande** ; la suite (validation, pricelist partenaire, visibilité prix partenaire) relève du **contexte Odoo** décrit en doctrine globale.

---

## Alignement avec la doctrine e-commerce CK

| Référence | Rôle pour MVP 03 |
|-----------|------------------|
| [DOCTRINE_CK_ECOMMERCE_B2C_B2B.md](../direction/DOCTRINE_CK_ECOMMERCE_B2C_B2B.md) | **§2.1** — catalogue commun, **affichage commercial contextualisé** (statut, **compte**, pricelists). **§4 / §8** — monde B2B, implications **comptes** et accès prix partenaire **conditionnés**. |
| [ADR-CKR-010 — Doctrine e-commerce B2C et B2B](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-010) | Sanctuarise la double lecture ; les **implications comptes / portail** sont des **orientations**, pas un mandat MVP élargi par défaut. |
| [ADR-CKR-001 — Standard Odoo d’abord](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-001) | Privilégier auth / portal / partner / pricelist **natifs** avant spécifique lourd. |
| [NOTE_DE_CADRAGE.md](../direction/NOTE_DE_CADRAGE.md) | Périmètre Phase 1 / MVP global ; MVP 03 ne **remplace** pas cette note mais doit rester **cohérent** avec elle. |

**Phrase canonique** (rappel) : le catalogue est **commun** ; prix et conditions dépendent du **contexte** (compte, listes de prix) — voir doctrine **§9**.

---

## Objectif MVP 03

Permettre à un visiteur de comprendre **clairement** quel type de compte **créer** ou **demander**, sans alourdir le parcours d’achat ni exposer prématurément les **tarifs B2B**.

Le **parcours particulier** doit rester **court** et ne pas devenir plus **administratif** qu’un parcours e-commerce **standard** — la distinction B2C / demande pro ne doit **pas** durcir l’ensemble du parcours compte.

---

## Points clés produit

- Séparer **B2C** et **B2B** dès l’**entrée** du parcours compte (libellés, chemins, attentes).
- Garder le **compte particulier** simple et rapide.
- Encadrer le **compte entreprise** comme une **demande** (délai, validation, pas de promesse tarifaire immédiate).
- Préparer la **future** logique prix partenaire / distributeur **sans** l’activer par défaut pour tout nouvel inscrit « pro ».
- **Ne pas** exposer automatiquement les tarifs B2B sur simple inscription ou simple formulaire.
- Rester aligné CK : **catalogue commun**, **affichage contextualisé** ([doctrine §2.1](../direction/DOCTRINE_CK_ECOMMERCE_B2C_B2B.md)).

---

## Périmètre plausible (à préciser par tickets futurs)

| Zone | Pistes (non contractuelles tant que non ticketées) |
|------|-----------------------------------------------------|
| **UX** | Choix B2C vs « Demande pro » sur `/web/signup`, `/my/account`, ou page dédiée selon arbitrage MOA. |
| **Back-office** | Workflow validation demande pro (sales team, étiquette partenaire, pricelist après accord). |
| **Données** | Champs société, SIRET, métier — au minimum nécessaire pour qualification. |
| **Tests** | Parcours critiques + non-régression tunnel achat **sans** compte. |

---

## Hors périmètre implicite (sauf nouveau ticket)

- Remplacer la **doctrine** prix B2C/B2B ou la **vision** trois mondes.
- Créer une **boutique parallèle** catalogue B2B séparée (interdit par doctrine sans révision explicite — [ADR-010](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-010)).
- Promettre des **remises** ou **prix pro** avant validation du compte.

---

## Livrables et pilotage (à renseigner quand le chantier démarre)

| Élément | Statut |
|---------|--------|
| Cadrage parcours | [1_COMPTE_CLIENT_PARCOURS.md](1_COMPTE_CLIENT_PARCOURS.md) — **rédigé** (2026-05) |
| Spec UX | [2_COMPTE_CLIENT_SPEC_UX.md](2_COMPTE_CLIENT_SPEC_UX.md) — **rédigé** (2026-05) |
| Ticket créa / spec MOA (parcours, copies, erreurs) | *À créer* |
| Ticket ou PR dev (`dorevia_ckreyol_marketplace`) | *À créer* |
| PV recette (desktop / mobile, cas B2C + demande B2B + edge cases) | *À créer* |
| Jeux de tests Odoo (`--test-tags=…`) | *À définir* |

**Prompt / lancement** : à produire lorsque MOA aura validé le découpage (équivalent éventuel de [`prompt_lancement_mvp21.md`](../prompting/prompt_lancement_mvp21.md) pour cette vague).

---

## Liens utiles hors MVP 03

- Vision long terme commerce / média : [VISION_CK_MEDIA_COMMERCE.md](../direction/VISION_CK_MEDIA_COMMERCE.md) — [ADR-CKR-009](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-009).
- Doctrine linguistique créole (hors mandat MVP compte) : [DOCTRINE_CK_LANGUES_CREOLES.md](../direction/DOCTRINE_CK_LANGUES_CREOLES.md).

---

## Historique

| Date | Événement |
|------|-----------|
| 2026-05 | README MVP 03 : intention comptes B2C / demande B2B, références [doctrine B2C-B2B](../direction/DOCTRINE_CK_ECOMMERCE_B2C_B2B.md) et [ADR-010](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-010), périmètre plausible, hors périmètre, tableau livrables — chantier non ouvert côté tickets. |
| 2026-05 | Ajout [1_COMPTE_CLIENT_PARCOURS.md](1_COMPTE_CLIENT_PARCOURS.md) — parcours, états, points d’entrée (`/web/login`, `/my`, signup), arbitrages techniques, critères de recette cible. |
| 2026-05 | Alignement **synthèse recommandations** (prudence CE, non-ticket-exécutable, friction B2C, achat invité, libellés « demande d’ouverture de compte pro », arbitrages réponse/données) — voir historique dans [1_COMPTE_CLIENT_PARCOURS.md](1_COMPTE_CLIENT_PARCOURS.md). |
| 2026-05 | Ajout [2_COMPTE_CLIENT_SPEC_UX.md](2_COMPTE_CLIENT_SPEC_UX.md) — principes UX, points d’entrée, parcours A/B écran, états et messages, accessibilité, critères recette UX, arbitrages MOA. |
