# Prompt d’onboarding — développeur C-Kreyol

Document à transmettre à un nouveau développeur ou à coller dans un chat IA.  
Adapter la dernière section selon l’environnement de travail réel.

**Reprise rapide d’un chat** (nouvelle session, même dépôt) : utiliser le bloc prêt à l’emploi dans [`prompt_session.md`](prompt_session.md).  
**Brief créatif / front-end** (design, SCSS, UX homepage) : voir [`prompt_creative.md`](prompt_creative.md).

---

## Contexte métier

Tu intègres le projet **C-Kreyol** : une **marque** et un **canal e-commerce de sélection** (Dorevia). Le **positionnement, la promesse et le ton** sont gelés dans **`docs/crea/PLATEFORME_MARQUE_CK_V1.md`** (2026-04-23) — *maison de sélection e-commerce du monde créole fabriqué*, critère de fabrication, doctrine §15. L’**exigence design** (partition, densité hiérarchisée, systèmes de sections / cartes, critères de réussite perçue) est gelée dans **`docs/crea/CADRAGE_DESIGN_CREATION_CK_V1.md`** (même date). Le **périmètre catalogue opérationnel** au lancement reste en pratique fortement centré sur les **agro-transformés antillais** ; l’alignement progressif copy / navigation / structure de page avec ces documents se fait par **tickets**, sans improvisation hors doc.

Le site vise une image **retail sobre, crédible et rassurante** (cf. plateforme §4, §9–§10). Il ne doit pas sur-promettre sur le **stock**, la **livraison** ou l’**offre réelle**.

Le canal s’appuie sur un **réseau de fournisseurs**. **La Platine** est le **premier partenaire commercial** au démarrage, mais le site ne doit pas devenir une vitrine « La Platine » au détriment de l’identité **C-Kreyol**.

Le contexte commercial est **métropolitain** (Nantes), tandis que les **origines produit** restent **caraïbéennes / créoles** au sens du catalogue actuel. Cette nuance est importante pour le ton éditorial, le contenu et la confiance.

---

## Objectif du développement

Le livrable principal est le module Odoo **`dorevia_ckreyol_marketplace`** sur **Odoo 19 Community Edition**.

Ce module a pour rôle d’**habiller** le site public (`website`, `website_sale`, `portal`) pour refléter l’identité **C-Kreyol**, notamment sur :

- le **header** et le **menu**,
- la **homepage**,
- la **boutique `/shop`**,
- la **fiche produit**,
- le **login**,
- le **portail client**,
- le **footer** aligné sur la société.

### Intention produit

Le visiteur doit pouvoir :

- **comprendre rapidement l’offre**,
- **entrer dans le catalogue** par des portes de lecture claires,
- **acheter** via des parcours cohérents avec le **standard Odoo**.

Le spécifique sert avant tout la **présentation**, la **navigation** et l’**éditorial**.  
Il ne doit pas créer un second moteur e-commerce parallèle au standard Odoo.

---

## Principes d’architecture

Lire ces principes avant de coder.

1. **Standard d’abord** — **ADR-CKR-001** (`docs/direction/ARCHITECTURE_DECISION_RECORD.md`)  
   Toujours composer avec **Odoo 19 CE**. Le spécifique n’est introduit que lorsque le standard ne suffit pas, de manière **justifiée**, **minimale** et **maîtrisée**.

2. **En phase 1, le spécifique « normal » est surtout du front** — **ADR-CKR-002**  
   Le périmètre naturel du spécifique est :

   - le **SCSS**,
   - les **vues QWeb website**,
   - le **JS d’UX** (drawer, rail Explorer manuel, etc.).

   Pas de dette métier lourde sans validation explicite.

3. **Les cinq entrées « Explorer » de la homepage** convergent vers la boutique — **ADR-CKR-007**  
   Les portes **Promotions**, **Collections**, **Kits**, **Catégories** et **Origines** doivent mener vers **`/shop`** ou vers un chemin natif Odoo équivalent.

4. **Bi-lexique visiteur / technique pour les packs** — **ADR-CKR-008**

   - côté site : **Kits**
   - côté back-office / technique : **Pack**, `product_pack`, `pack_ok`

5. **Explorer n’est pas le menu principal**  
   Le menu principal porte la **navigation générale** (Boutique, Collections, **Communauté** — Idées cadeaux, Recettes, Blog, etc.).  
   Le bloc **Explorer** distribue des **modes de lecture du catalogue**, pas la navigation globale.  
   Références :

   - `docs/direction/STRUCTURE_MENU_PRINCIPAL.md` §11
   - `docs/direction/WIREFRAME_HOMEPAGE.md` Bloc 3

6. **Homepage V1 gelée et implémentée** (module version `19.0.1.6.16`, 2026-04-23)  
   La montée en gamme créative de la homepage est **livrée** et ses **arbitrages §9 sont gelés** : hero 60/40, supplier plane, editorial bandeau sobre sans `<h2>`, selection garde-fou responsive, fil rouge amber 1 px (2 px sur Supplier).  
   Ces arbitrages sont **non négociables sans ticket explicite** — ouvrir un ticket dédié avant toute modification qui les remet en cause.  
   Références :

   - `docs/crea/PLATEFORME_MARQUE_CK_V1.md` (marque, promesse, ton — gel 2026-04-23)
   - `docs/crea/CADRAGE_DESIGN_CREATION_CK_V1.md` (design, composition, densité — gel 2026-04-23)
   - `docs/crea/PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md` (arbitrages §9)
   - `docs/crea/PLAN_IMPL_HOMEPAGE_MONTEE_EN_GAMME_V1.md` (plan d’exécution)
   - `docs/crea/TICKETS_HORS_PERIMETRE_V1.md` (sujets hors V1)

**Homepage MVP2.1** — vague **cinq chantiers** (hero immersif, Explorer, sélection, inscription newsletter, réassurance) : **clôturée côté MOA** le **2026-04-25**. Refonte bloc newsletter (2026-05) : [`docs/crea/TICKET_REFONTE_BLOC_NEWSLETTER_HOMEPAGE_CK.md`](../crea/TICKET_REFONTE_BLOC_NEWSLETTER_HOMEPAGE_CK.md). Pilotage, PV et gel : [`docs/mvp_02/README.md`](../mvp_02/README.md), canon [`docs/mvp_02/1_HOMEPAGE.md`](../mvp_02/1_HOMEPAGE.md) ; lancement / historique : [`prompt_lancement_mvp21.md`](prompt_lancement_mvp21.md).

**Pages légales & newsletter homepage** — URLs **`/privacy`**, **`/terms`** (QWeb `views/pages/`) ; inscription **`POST /ckr/circle/subscribe`** (`controllers/ckr_circle.py`) — liste **`mass_mailing`** **Newsletter C-Kreyol**, redirections **`?cc_nl=`** (`ok` \| `dup` \| `invalid` \| `err`). Ticket refonte : [`docs/crea/TICKET_REFONTE_BLOC_NEWSLETTER_HOMEPAGE_CK.md`](../crea/TICKET_REFONTE_BLOC_NEWSLETTER_HOMEPAGE_CK.md). Tests tag **`dorevia_ckr_circle`** : [`tests/test_ckr_circle.py`](../../tests/test_ckr_circle.py). Après changement d’**hébergeur**, mettre à jour le bloc hébergement dans **`ckr_terms.xml`**.

---

## Ordre de lecture recommandé

| Priorité | Fichier | Rôle |
| -------- | ------- | ---- |
| 1 | `README.md` | Vue d’ensemble du module et de son arborescence |
| 2 | `docs/crea/PLATEFORME_MARQUE_CK_V1.md` | Positionnement, promesse, ton, architecture cible, doctrine pilotage (gel 2026-04-23) |
| 3 | `docs/crea/CADRAGE_DESIGN_CREATION_CK_V1.md` | Design, partition homepage, sections, cartes, rythme, densité, doctrine design (gel 2026-04-23) |
| 4 | `docs/direction/ARCHITECTURE_DECISION_RECORD.md` | ADR-CKR-001 à 008, surtout 001, 002, 007, 008 |
| 5 | `docs/direction/WIREFRAME_HOMEPAGE.md` | Structure de la homepage et Bloc 3 Explorer |
| 6 | `docs/direction/DESIGN.md` §7 | Synthèse des blocs homepage |
| 7 | `docs/mvp_01/SPEC_SHOP_PORTES.md` | Vision d’ensemble des portes catalogue vers `/shop` |
| 8 | `docs/mvp_01/CONTRAT_URL_*.md` et `docs/mvp_01/SPEC_IMPL_*.md` | Détails de mise en œuvre selon la porte concernée |
| 9 | `docs/crea/PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md` | Homepage V1 implémentée le 2026-04-23 ; arbitrages §9 gelés |
| 10 | `docs/crea/PLAN_IMPL_HOMEPAGE_MONTEE_EN_GAMME_V1.md` | Plan d’exécution de la V1 |
| 11 | `docs/crea/TICKETS_HORS_PERIMETRE_V1.md` | Sujets explicitement sortis du périmètre V1 |
| 12 | `docs/mvp_02/README.md` | Pilotage **MVP2.1** homepage — **clôturé MOA 2026-04-25** |

---

## Périmètre technique concret

En pratique, tu interviendras principalement sur :

- **Vues** : `views/`
- **Front** : `static/src/scss/`, `static/src/js/`
- **Assets** : `__manifest__.py` (`web.assets_frontend`, etc.)
- **Boutique / logique catalogue** : `controllers/website_sale_ckr.py`, `models/` selon la porte concernée

### Règle d’exécution

Après toute modification sur :

- **XML**
- **SCSS**
- **JS**

il faut :

1. mettre à jour le module avec **`-u dorevia_ckreyol_marketplace`** sur l’instance de test ;
2. recharger les **assets** côté navigateur.

---

## Attitude attendue

Avant d’étendre le périmètre :

- lire le **code existant** ;
- relire les **ADR** et les **contrats** liés à la porte concernée ;
- respecter les **conventions du dépôt** ;
- mettre à jour la **documentation** si la modification touche :

  - un comportement produit,
  - une règle d’URL,
  - ou une doctrine déjà écrite.

Le dépôt doit rester **cohérent**, **documenté** et **aligné avec la doctrine produit**.

---

## Rappel important

Le but n’est pas de « refaire Odoo », mais de **tirer le meilleur du standard Odoo** pour produire un site :

- lisible,
- crédible,
- maintenable,
- et fidèle à la marque **C-Kreyol**.

---

## Contexte d’exécution

À compléter selon l’environnement réel :

- **Branche Git courante** : *…*
- **Instance / base de développement** : *…*
- **Langue des échanges équipe** : français, si applicable
