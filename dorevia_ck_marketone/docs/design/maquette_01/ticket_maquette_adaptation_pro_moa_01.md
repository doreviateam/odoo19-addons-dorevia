# Ticket — Maquette adaptation Pro MOA (V1.1.1)

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Type** | Micro-évolution textuelle maquette — **pas Dev Odoo** |
| **Référence MOA** | [`note_transmission_arbitrage_david_01_v1_1.md`](./note_transmission_arbitrage_david_01_v1_1.md) |
| **Suite de** | Maquette V1.1 validée QA |
| **Artefact** | `/Users/doreviateam/open-design/.od/projects/ck-marketone-maquette-v1/index.html` |
| **Date** | 2026-06-12 |
| **Statut** | Livré — **QA validée V1.1.1** |

---

## Objet

Dernière adaptation maquette **avant GO Dev éventuel** : aligner textes et signaux Pro sur les arbitrages §10 actés MOA.

```text
Micro-évolution textuelle uniquement — pas de refonte UX lourde.
Verrou Odoo maintenu pendant cette étape.
Décisions MOA §10 complétées ≠ GO Dev.
GO Dev confirmé uniquement après validation QA de cette adaptation.
```

---

## Périmètre

### Inclus

- Section **Espace professionnel** (`#pro`) : double cible fournisseur / distributeur
- Doctrine **brick & mortar** intégrée
- Deux blocs + deux CTA distincts
- Formulaire maquette avec champ **« Nature de la demande professionnelle »**
- Rappel discret prix publics = canal B2C CK
- Bandeau `/shop` et hero alignés
- Note prix boutique `/shop`

### Exclu (interdit)

```text
Aucune base Odoo
Aucun module
Aucun ticket dorevia_ck_theme
Aucun QWeb / SCSS
Aucune extension origines, collections, filtre prix
Aucun portail B2B transactionnel
Aucune refonte layout globale
```

---

## Modifications livrées (V1.1 → V1.1.1)

| Zone | Changement |
|------|------------|
| Hero accueil | CTA « Espace professionnel » → `#pro` |
| Section `#pro` | Nouvelle : doctrine, deux blocs, formulaire, footnote B2C/B2B |
| Intro `/shop` | Note discrète prix canal B2C |
| Bandeau `/shop` | Texte double cible + lien `#pro` — retrait « volume » / « parcours complet » |
| Navigation | Onglet + liens header/mobile → `#pro` |
| Version | Bandeau maquette V1.1.1 |

---

## Critères QA

Voir [`recette_qa_maquette_01_1.md`](./recette_qa_maquette_01_1.md).

```text
Validation QA requise avant toute levée du verrou Odoo.
Si GO confirmé ensuite → premier ticket strictement borné : dorevia_ck_theme (tokens + layout uniquement).
```

---

## Verrou Odoo

**Maintenu** — cette livraison ne constitue pas un GO développement.
