# TICKET — Réassurance Homepage MVP2.1 (bloc confiance)

**ID** : `REASSURANCE-HOMEPAGE-MVP21`  
**Date d’ouverture** : 2026-04-24  
**Priorité** : **P2** (évolution copy / structure du bloc confiance ; V1 déjà fonctionnelle).  
**Statut** : **Accepté (GO MOA)** — **2026-04-25** ; preuve : [PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md](PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md)  
**Module** : `dorevia_ckreyol_marketplace`  
**Périmètre** : **bloc Réassurance / confiance** — `views/snippets/ckr_trust.xml` + SCSS associés (`ckr-trust`).

**Exécution : clos (2026-04-25)** — verdict **GO MOA** : [PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md](PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md). Les checklists de ce ticket sont **soldées** ci-dessous ; toute évolution rouvre un **ticket MOA**.

**Rattachement** : [TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md](TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md) ; cadrage §6 [1_HOMEPAGE.md](../mvp_02/1_HOMEPAGE.md) ; ordre page [DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md](../mvp_02/DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md).

---

## Contexte

La homepage MVP2.1 est structurée ainsi : **Hero → Explorer → Produits → Éditorial → Inscription → Réassurance** ([1_HOMEPAGE.md](../mvp_02/1_HOMEPAGE.md), gel conception).

Référence historique : ancienne **V1** à **3 axes** (Achat / Livraison / Contact). **MVP2.1 clôturée** : **4 repères** dans `ckr_snippet_trust` — détail [1_HOMEPAGE.md](../mvp_02/1_HOMEPAGE.md) §6 et **PV** ci-dessus.

---

## Objectif

Faire **évoluer** le bloc Réassurance pour **renforcer la confiance** avant achat, sans **surpromesse** ni **surcharge** ([ADR-CKR-005](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005)).

---

## Périmètre

### Cible rédactionnelle (MVP2.1 — cinq intentions)

| # | Titre | Sous-texte |
|---|--------|------------|
| 1 | **Paiement sécurisé** | Vos transactions sont protégées. |
| 2 | **Sélection rigoureuse** | Des produits choisis avec soin pour leur qualité. |
| 3 | **Producteurs et créateurs de confiance** | Un lien direct avec des producteurs et créateurs authentiques. |
| 4 | **Livraison claire** | Suivi précis et emballage soigné. |
| 5 | **À votre écoute** | Un support client réactif et humain. |

### Arbitrage structurel (MOA — 2026-04-24) et livré (2026-04-25)

- **Ticket / pilotage initial** : cible **5 items** ; **fallback 3 enrichis** si lisibilité ([README MVP 02](../mvp_02/README.md)).
- **Livré et validé MOA** : **4 repères** (synthèse des intentions, grille 1 / 2 / 4 colonnes, ton « preuve douce ») — arbitrage chantier documenté dans le **PV** ; pas d’écart bloquant.

---

## Rendu attendu

- Bloc **sobre** ; **icônes** simples ; **textes** courts ;
- **Fond neutre** ; **lisibilité** desktop / mobile ;
- **Cohérence** avec la charte CK ([PLATEFORME_MARQUE_CK_V1.md](PLATEFORME_MARQUE_CK_V1.md), tokens existants).

---

## Contraintes

- Pas de **faux badges** de confiance ; pas de **promesse excessive** ;
- Pas de « **livraison rapide** » si **non garantie** ;
- Pas de **surcharge** visuelle ;
- Rester **sincère** sur capacités **logistiques** et **support** (alignement avec les textes actuels **Livraison** / **Contact** si conservés).

---

## Technique (attendu)

- Adapter **`ckr_trust.xml`** (titres, paragraphes, nombre de `.ckr-trust__item`, icônes si besoin) ;
- Adapter **SCSS** si nécessaire (grille 3 vs 5, gaps, mobile) ;
- Conserver **compatibilité responsive** ; vérifier **impact mobile** si passage à **5 items** ;
- **Bump `__manifest__.py`** si bundle front modifié.

---

## Hors périmètre

- Création de **pages garanties** détaillées (hors lien discret éventuel vers pages existantes) ;
- **Refonte footer** ;
- **Avis clients** ; **badges tiers** non vérifiés.

---

## Critères d’acceptation

- [x] **Messages** affichés clairement — **4 repères** livrés (équivalent au tranchement **5 / fallback 3** du ticket : arbitrage **chantier** + **PV**) ;
- [x] **Aucune** promesse **non maîtrisée** (cohérence ADR-005) ;
- [x] Rendu **cohérent** avec le reste de la homepage MVP2.1 ;
- [x] **Responsive** validé MOA (desktop + mobile) ;
- [x] **Documentation** alignée : [1_HOMEPAGE.md](../mvp_02/1_HOMEPAGE.md) §6, [README MVP 02](../mvp_02/README.md) ; [WIREFRAME_HOMEPAGE.md](../direction/WIREFRAME_HOMEPAGE.md) Bloc 7 = référence macro inchangée en titre (pas d’exigence de mise à jour pixel supplémentaire pour ce chantier).

---

## Recette

- **PV** : [PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md](PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md) — **GO MOA 2026-04-25** (réserve mineure Design System, non bloquante) ;
- Complément historique : [PV_RECETTE_PHASE_A_HOMEPAGE_CK.md](PV_RECETTE_PHASE_A_HOMEPAGE_CK.md) si sections transverses utiles.

---

## 0. Prêt pour dev — checklist pilotage *(soldée — clos 2026-04-25)*

1. [x] **Branche** / intégration — livrée dans le module (cf. historique Git du chantier).
2. [x] **Arbitrage** nombre d’items — **4 repères** validés MOA (voir **PV**).
3. [x] **Copy** — relue ; ton sobre, crédible, sans surpromesse.
4. [x] **Layout** — grille responsive **4** colonnes desktop (sans maquette séparée requise).
5. [x] **Accessibilité** — titres, hiérarchie, focus sobres (recette MOA).
6. [x] **Doc** — `1_HOMEPAGE.md` §6 + pilotage MVP 02 ; wireframe macro conservé.
7. [x] **`__manifest__.py`** — bundle front conforme au module en production recette.
8. [x] **Recette** — [PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md](PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md) **GO MOA**.
9. [x] **Instance / relecteur** — recette MOA réalisée (2026-04-25).

---

## Livrables techniques (synthèse)

| Livrable | Détail |
|----------|--------|
| **QWeb** | `ckr_trust.xml` — **4** repères, textes, icônes sobres. |
| **SCSS** | Grille trust 1 / 2 / 4 colonnes, responsive (`_trust.scss`). |

---

## Historique

| Date | Changement |
|------|------------|
| 2026-04-24 | Création — alignement [1_HOMEPAGE.md](../mvp_02/1_HOMEPAGE.md) §6 ; arbitrage 3 vs 5 items ; PV dédié. |
| 2026-04-24 | **MOA** — cible **5 items** ; fallback **3 enrichis** si lisibilité ; [README MVP 02](../mvp_02/README.md) pilotage. |
| 2026-04-25 | **Clôture** — **GO MOA** ; **4 repères** livrés ; **Exécution : clos** ; checklists soldées ; preuve [PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md](PV_RECETTE_REASSURANCE_HOMEPAGE_MVP21_CK.md). |
