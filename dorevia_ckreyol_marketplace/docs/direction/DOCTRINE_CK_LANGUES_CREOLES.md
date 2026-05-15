# Doctrine CK — Langues créoles dans l’expérience utilisateur

**Statut :** Doctrine culturelle **figée** — mise en œuvre **progressive** (ne prescrit pas le MVP obligatoire)  
**Projet :** C-Kreyol  
**Date :** 2026-04-26  
**Nature :** orientation produit, éditoriale et culturelle  
**Périmètre immédiat :** ne déclenche pas de développement MVP obligatoire

**Pilotage :** [ADR-CKR-011](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-011). Complète la [vision média-commerce](VISION_CK_MEDIA_COMMERCE.md) ([ADR-CKR-009](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-009)). **Technique** (activation langues Odoo, sélecteurs) : [EXPLOITATION_I18N_DEVISES.md](EXPLOITATION_I18N_DEVISES.md) — la présente doctrine porte la **qualité**, les **variantes** et la **gouvernance** des contenus créoles, pas le paramétrage seul.

---

## 1. Intention

C-Kreyol a vocation à accueillir progressivement les langues créoles dans son expérience utilisateur.

Cette orientation ne relève pas seulement de la traduction d’interface. Elle participe à la mission culturelle de CK : permettre à certains visiteurs, clients, partenaires ou membres de la communauté de découvrir, lire, acheter et interagir dans une langue créole légitime, vivante et reconnue.

L’introduction des créoles dans CK doit être progressive, gouvernée et respectueuse des variantes linguistiques.

---

## 2. Principe fondateur

> **CK traite les langues créoles comme il traite les produits : avec origine, respect, qualification et responsabilité.**

Cette phrase constitue le cœur de la doctrine.

Comme un produit ne doit pas être présenté comme « créole » de manière vague ou générique, une langue créole ne doit pas être traitée comme un bloc uniforme.

Chaque produit a :

- une origine ;
- un producteur ;
- un usage ;
- une histoire ;
- une légitimité.

Chaque créole a également :

- un territoire ;
- des locuteurs ;
- des variantes ;
- des nuances ;
- une légitimité culturelle.

---

## 3. Refus du « créole générique »

C-Kreyol ne doit pas prétendre traduire son expérience « en créole » de manière indifférenciée.

La doctrine retenue est :

> **Il n’existe pas, pour CK, un créole générique. Il existe des créoles, accueillis progressivement variante par variante.**

Exemples possibles à long terme :

- créole guadeloupéen ;
- créole martiniquais ;
- créole guyanais ;
- créole haïtien ;
- créole réunionnais ;
- autres variantes selon les communautés, les contributeurs et la pertinence CK.

L’utilisateur, le client ou le visiteur doit pouvoir comprendre clairement **quelle variante créole** est proposée.

---

## 4. Traduction humaine qualifiée

La traduction créole publiée dans CK doit être produite par des **humains qualifiés**.

L’IA ne doit **pas** être utilisée comme **générateur principal** de la traduction publiée.

La règle est :

> **La langue créole n’est pas un simple contenu automatisable : c’est un acte de transmission, de respect et de légitimité culturelle.**

Le flux cible est donc :

> **Texte source CK → traduction humaine qualifiée → relecture / validation éditoriale → publication.**

---

## 5. Rôle des contributeurs créoles traducteurs

CK pourra s’appuyer, à terme, sur des contributeurs créoles traducteurs qualifiés.

Leur rôle pourra inclure :

- traduire des éléments d’interface ;
- traduire certains contenus éditoriaux ;
- adapter le ton à la variante créole concernée ;
- signaler les formulations ambiguës ou culturellement faibles ;
- participer à la qualité linguistique de CK ;
- contribuer à la reconnaissance des variantes créoles.

Ces contributeurs ne sont pas de simples exécutants techniques. Ils sont des **garants de légitimité linguistique** pour leur créole.

---

## 6. Gouvernance éditoriale

Aucune traduction créole contributive ne doit être publiée **automatiquement** dans l’expérience CK.

Une gouvernance éditoriale est nécessaire pour protéger :

- la qualité linguistique ;
- la cohérence commerciale ;
- la compréhension du parcours d’achat ;
- la sécurité juridique et commerciale ;
- la dignité culturelle des langues concernées.

La règle de gouvernance est :

> **Contribuer → relire → valider → publier.**

---

## 7. Application à l’expérience e-commerce

L’introduction des langues créoles pourra concerner progressivement :

- certains éléments d’interface ;
- certaines fiches produits ;
- certaines pages éditoriales ;
- certaines rubriques communautaires ;
- des messages d’accueil ou d’accompagnement ;
- des contenus culturels ou pédagogiques.

Cependant, le parcours marchand doit rester **fiable**, **compréhensible** et **sécurisé**.

Les traductions créoles ne doivent **jamais** créer d’ambiguïté sur :

- le prix ;
- les quantités ;
- les conditions de vente ;
- les délais ;
- le paiement ;
- la livraison ;
- le droit de rétractation ;
- les mentions obligatoires.

En cas de doute, la version **française** de référence reste la version **contractuelle principale**, sauf décision juridique contraire future.

Cette exigence est **alignée** avec la **sanctuarisation** du e-commerce ([VISION_CK_MEDIA_COMMERCE.md](VISION_CK_MEDIA_COMMERCE.md) §6, [ADR-CKR-009](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-009)).

---

## 8. Articulation avec les trois mondes CK

La doctrine des langues créoles s’inscrit dans la vision média-commerce CK.

| Monde CK | Rôle possible des langues créoles |
|---|---|
| E-commerce | Expérience d’achat contextualisée, traductions maîtrisées, parcours sécurisé |
| Éditorial | Récits, recettes, origines, usages, transmission linguistique |
| Communautaire | Contributions, échanges, reconnaissance des variantes, animation culturelle |

L’**éditorial** et le **communautaire** seront probablement les **premiers** espaces naturels d’expérimentation.

L’**e-commerce** pourra intégrer les créoles **plus progressivement**, avec un niveau de contrôle **plus élevé**.

---

## 9. Ce que cette doctrine ne déclenche pas immédiatement

Cette doctrine ne signifie pas que CK doit livrer immédiatement :

- une interface multilingue créole complète ;
- toutes les variantes créoles ;
- un système de contribution complexe ;
- un workflow éditorial avancé ;
- une traduction de tout le catalogue ;
- une fonctionnalité communautaire dédiée.

Elle pose une **orientation long terme**.

La mise en œuvre viendra après stabilisation du socle :

- catalogue ;
- parcours e-commerce ;
- ligne éditoriale ;
- communauté ;
- gouvernance de contenu.

---

## 10. Décision

C-Kreyol retient comme orientation long terme l’introduction **progressive** des langues créoles dans son expérience utilisateur.

Cette introduction devra respecter les principes suivants :

1. pas de créole générique ;
2. accueil variante par variante ;
3. traduction produite par des humains qualifiés ;
4. relecture et validation avant publication ;
5. respect des locuteurs et des territoires ;
6. protection du parcours e-commerce ;
7. cohérence avec la vision média-commerce CK.

---

## 11. Phrase canonique

> **CK traite les langues créoles comme il traite les produits : avec origine, respect, qualification et responsabilité.**

---

## 12. Historique

| Date | Événement |
|---|---|
| 2026-04-26 | Formalisation de la doctrine long terme sur l’introduction des langues créoles dans l’expérience utilisateur CK. |
| 2026-04-26 | Intégration `docs/direction/` ; [ADR-CKR-011](ARCHITECTURE_DECISION_RECORD.md#adr-ckr-011) ; liens [VISION_CK_MEDIA_COMMERCE.md](VISION_CK_MEDIA_COMMERCE.md), [EXPLOITATION_I18N_DEVISES.md](EXPLOITATION_I18N_DEVISES.md). |
