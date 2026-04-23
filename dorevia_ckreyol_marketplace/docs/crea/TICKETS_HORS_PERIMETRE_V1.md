# TICKETS HORS PÉRIMÈTRE V1 — Suites de la montée en gamme homepage

**Date** : 2026-04-23
**Contexte** : suite à l'implémentation V1 de la montée en gamme créative de la homepage (`dorevia_ckreyol_marketplace` version `19.0.1.6.16` après clôture Ticket 1), les sujets listés ci-dessous ont été identifiés au cours du cycle mais **explicitement déportés hors périmètre V1** — soit par arbitrage MOA, soit parce qu'ils dépendent de décisions produit / édito / data non encore mûres.

**Documents de référence** :
- [PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md](PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md) — §9 arbitrages gelés, §10 hors périmètre.
- [PLAN_IMPL_HOMEPAGE_MONTEE_EN_GAMME_V1.md](PLAN_IMPL_HOMEPAGE_MONTEE_EN_GAMME_V1.md) — §10 hors périmètre, §11 conclusion.

**Convention de priorisation** :
- **P1** : à traiter dans la continuité de V1 (petit ticket, faible risque, dette documentaire ou copy).
- **P2** : à arbitrer côté produit avant exécution (décision édito, impact UX visible).
- **P3** : à réévaluer après mise en production V1 (dépend du retour terrain).

---

## Ticket 1 — [P1] Arbitrage du sous-titre Hero `__subtitle-accent`

**Statut** : **CLÔTURÉ le 2026-04-23**. Arbitrage MOA **Option A (conformité stricte / retrait)** : suppression du `<span class="ckr-hero__subtitle-accent">` dans `ckr_hero.xml`, suppression du bloc `.ckr-hero__subtitle-accent` dans `_hero.scss`, bump module **19.0.1.6.15 → 19.0.1.6.16**. Gel `SPEC_HERO_HOMEPAGE.md` §7 **non amendé** (écart mineur résolu côté code). Motifs MOA : hero plus calme et respirant, ton plus sobre, pas de friction documentaire pour un écart non nécessaire.

**Origine** (avant clôture) : une 2e phrase sous le sous-titre principal était rendue via `.ckr-hero__subtitle-accent` ("Du plaisir d'abord…", italic, `$ckr-text-muted`). Elle **ne figurait pas** dans le gel `SPEC_HERO_HOMEPAGE.md` §7.

**Question à trancher** :
- **Option A — conformité stricte** : retirer la phrase du QWeb pour coller au gel SPEC. Impact : Hero plus court, même ratio 60/40 préservé.
- **Option B — amendement du gel SPEC** : ajouter la phrase au §7 de `SPEC_HERO_HOMEPAGE.md` avec justification édito. Impact : met à jour la SPEC, aligne la copy actuelle.

**Livrables attendus** :
- Décision écrite MOA (A ou B).
- Soit : patch QWeb `ckr_hero.xml` suppression du `.ckr-hero__subtitle-accent` + bump patch module.
- Soit : amendement `SPEC_HERO_HOMEPAGE.md` §7 + historique document + pas de changement de code.

**Effort estimé** : 15 min (décision) + 15 min (exécution).
**Risque** : nul.
**Dépendance** : aucune — arbitrage pur.

---

## Ticket 2 — [P1] Ajout de la référence au document V1 homepage dans les prompts pertinents

**Statut** : **CLÔTURÉ le 2026-04-23**. Exécuté sur les 3 prompts retenus (`prompt_creative.md`, `prompt_dev.md`, `prompt_ticket.md`), `prompt_session.md` non modifié comme convenu. Pas de bump module (fichiers hors assets Odoo). Reformulation initiale documentée ci-dessous pour traçabilité de l'audit.

**Note** : le ticket a été **reformulé le 2026-04-23** après audit. La formulation initiale (« correction de chemins erronés ») partait d'une fausse hypothèse — l'audit a confirmé qu'**aucun chemin n'est erroné** dans les 4 `prompt_*.md`. Le vrai besoin est ailleurs : garantir qu'un futur développeur, créatif ou chat IA qui reprendrait un sujet homepage soit systématiquement orienté vers le document V1 gelé, pour ne pas rouvrir implicitement les arbitrages §9.

**Origine** : depuis le 2026-04-23, la homepage est en état **V1 implémentée et gelée** (module `dorevia_ckreyol_marketplace` version `19.0.1.6.15`, arbitrages §9 non négociables sans ticket explicite). Les 4 prompts templates de la racine module ne font **aucune mention** de ce document ni de ce statut.

**Risque latent si non traité** : une nouvelle session de travail sur la homepage (design ou dev) repart sans connaissance de l'état gelé → propositions qui réouvrent ce qui a déjà été tranché (hero 60/40, supplier plane, editorial sobre sans h2, selection garde-fou, fil rouge amber), retour en arrière sur des décisions MOA, perte de temps en ré-arbitrage.

**Portée retenue** (validée MOA 2026-04-23) :
- `prompt_creative.md` : **ajout** des 3 références V1 + mini-règle « ne pas rouvrir §9 sans ticket explicite ».
- `prompt_dev.md` : **ajout** des 3 références V1 + mini-règle dans les principes d'architecture.
- `prompt_ticket.md` : **mention ciblée homepage** uniquement (léger, pas un pavé).
- `prompt_session.md` : **non modifié** (volontairement court et focalisé sur la reprise de session).

**Livrables attendus** :
- Dans `prompt_creative.md` : 3 lignes dans "Références à parcourir avant de proposer" + 1 ligne dans "Doctrine produit à respecter".
- Dans `prompt_dev.md` : 3 lignes dans le tableau "Ordre de lecture recommandé" + 1 principe d'architecture supplémentaire.
- Dans `prompt_ticket.md` : 1 ligne conditionnelle « si ticket homepage » après la liste de références.
- Pas de bump module (fichiers hors assets Odoo).

**Forme des 3 références** (validée MOA) :
```
- docs/crea/PROPOSITION_HOMEPAGE_MONTEE_EN_GAMME_V1.md  homepage V1 implémentée le 2026-04-23 ; arbitrages §9 gelés
- docs/crea/PLAN_IMPL_HOMEPAGE_MONTEE_EN_GAMME_V1.md    plan d'exécution de la V1
- docs/crea/TICKETS_HORS_PERIMETRE_V1.md                sujets explicitement sortis du périmètre V1
```

**Effort estimé** : 20 min.
**Risque** : nul (textuel uniquement, hors assets Odoo, pas de rechargement).
**Dépendance** : aucune.

---

## Ticket 3 — [P3] Réévaluation de la suréligne Explorer « Porte 0x »

**Origine** : la proposition créative avait suggéré d'ajouter une petite suréligne "Porte 01", "Porte 02"… au-dessus de chaque carte Explorer pour renforcer la lisibilité éditoriale du carrousel. Exclue de V1 au titre de l'ajustement MOA #2 (densité + absence d'invariance dans le gel).

**Question à réévaluer après V1 en production** :
- Le rail Explorer est-il **lisible** en l'état (5 portes visibles simultanément sur desktop, moins en mobile) ?
- Les intitulés de portes suffisent-ils ou une numérotation additionnelle apporte-t-elle un vrai gain d'orientation utilisateur ?

**Méthode suggérée** :
- Observation terrain (analytics, heatmaps, retours utilisateurs) sur la V1 en production.
- Ne pas décider avant au moins 2 semaines d'usage réel.
- Si décision d'activer : définir une **invariance** (toutes les portes ou aucune, même format, même style typographique) pour respecter le principe du gel.

**Livrables attendus** (si activation) :
- Patch QWeb `ckr_entries.xml` : ajout d'un `<span class="ckr-entries__card__overline">Porte 0X</span>` dans chaque carte.
- Patch SCSS `_entries.scss` : style overline conforme au fil rouge (amber, `text-transform: uppercase`, `letter-spacing: 0.08em`, `font-size: 0.75rem`, `color: $ckr-accent`).
- Bump patch ou mineur selon la convention retenue à l'époque.

**Effort estimé** : 45 min d'exécution si activation, 1 h d'analyse terrain en amont.
**Risque** : faible (additif, pas de refonte).
**Dépendance** : ouverture du ticket après mise en production V1 + quelques jours d'usage.

---

## Ticket 4 — [P3] Réévaluation de l'alternance des fonds de section `--bg-warm` / `--bg-soft`

**Origine** : la proposition créative suggérait d'alterner les fonds de section entre `$ckr-bg` (off-white standard) et `$ckr-bg-soft` (beige légèrement plus chaud) pour marquer le rythme vertical. Non retenu en V1 : les fonds actuels (off-white dominant, Supplier en `$ckr-bg-soft`, Trust en `ckr-section--soft`) suffisent à marquer la respiration sans alourdir.

**Question à réévaluer après V1 en production** :
- Avec l'ensemble monté en gamme (filets amber, Hero 60/40, Editorial bandeau sobre, Trust icônes linéaires), la homepage **paraît-elle trop uniforme** visuellement ?
- L'ajout d'une alternance supplémentaire (ex. Selection en `--bg-soft`, Editorial en `--bg-warm`) apporterait-il un gain de rythme ou créerait-il au contraire une impression de patchwork ?

**Méthode suggérée** :
- Captures homepage V1 complète en scroll continu → revue en équipe éditoriale + produit.
- Si décision positive : définir l'alternance globale **cohérente sur toutes les pages CK** (pas seulement homepage), sinon risque d'incohérence inter-pages.

**Livrables attendus** (si activation) :
- Patch SCSS : création de `ckr-section--warm` dans `ckr_main.scss` (si pas déjà présent) + application dans les snippets concernés.
- Régression visuelle à vérifier sur `/shop`, `/product/*`, `/collections` si les sections CK sont réutilisées.
- Bump patch ou mineur.

**Effort estimé** : 30 min si activation propre, plusieurs heures si refonte large de cohérence inter-pages.
**Risque** : moyen — impact visuel large, à cadrer avec soin pour éviter un effet "mosaïque".
**Dépendance** : ouverture du ticket après mise en production V1 + revue éditoriale.

---

## Ticket 5 — [P2] Homepage : appétence perçue & partition (cadrage design)

**Statut** : **Ouvert** (2026-04-23).

**Origine** : après gel de la [PLATEFORME_MARQUE_CK_V1.md](PLATEFORME_MARQUE_CK_V1.md) et du [CADRAGE_DESIGN_CREATION_CK_V1.md](CADRAGE_DESIGN_CREATION_CK_V1.md), constat MOA : la homepage V1 implémentée paraît **insuffisamment appétente** (désir perçu) et **moins partitionnée** que la séquence cible du cadrage (promesse → portes → réassurance → origines → …).

**Spécification détaillée** (phases A/B/C, gels §9, critères d’acceptation, risques) : **[TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md](TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md)**.  
**Brief créatif Phase A** : [BRIEF_CRÉA_PHASE_A_HOMEPAGE.md](BRIEF_CRÉA_PHASE_A_HOMEPAGE.md).  
**PV de recette Phase A** (trame à compléter après livraison) : [PV_RECETTE_PHASE_A_HOMEPAGE_CK.md](PV_RECETTE_PHASE_A_HOMEPAGE_CK.md).

**Effort estimé** : Phase A quelques heures à 1 j ; Phases B–C selon arbitrage (journées).

**Risque** : moyen — tension possible entre **cadrage** (structure riche) et **gels homepage V1 §9** ; mitigation = phases et tickets fils.

**Dépendance** : décisions MOA (priorité de phase, coexistence rail Explorer / portes maîtresses, médias et copy).

---

## Récapitulatif et ordre suggéré

| Ticket | Priorité | Statut | Effort | Dépendance | Ordre suggéré |
|---|---|---|---|---|---|
| 1 — Hero `__subtitle-accent` | P1 | **Clôturé 2026-04-23** | 30 min total | Aucune | — |
| 2 — Ajout références V1 dans prompts | P1 | **Clôturé 2026-04-23** | 20 min | Aucune | — |
| 3 — Explorer suréligne | P3 | Ouvert | 1h45 si activation | Usage terrain V1 | 4 (après retour) |
| 4 — Alternance fonds section | P3 | Ouvert | 30 min – plusieurs heures | Revue éditoriale V1 | 3 (après captures) |
| 5 — [Homepage appétence & partition](TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md) | P2 | **Ouvert** | A : quelques h–1 j ; B–C : selon arbitrage | MOA + médias / édito | 1–2 (si priorité UX homepage) |

**Recommandation** : les 2 tickets P1 sont **clôturés** (2026-04-23). Le **ticket 5 (P2)** peut être piloté dès que MOA valide la phase (recommandation dans le ticket : **Phase A** avant réordonnancement lourd). Attendre au moins 2 semaines de production V1 avant d'ouvrir les 2 tickets P3 (données de terrain nécessaires).

---

## Historique du document

| Date | Changement |
|------|------------|
| 2026-04-23 | Création : 4 tickets déportés hors périmètre V1 lors de la montée en gamme homepage. 2 P1 (arbitrage copy Hero + chemins prompts erronés), 2 P3 (Explorer suréligne + alternance fonds section). Ordre suggéré et méthodes de décision documentés. |
| 2026-04-23 | **Reformulation du Ticket 2** après audit réel des 4 `prompt_*.md` : aucun chemin erroné n'existe (hypothèse initiale infondée). Le ticket devient « ajout de la référence V1 homepage dans les prompts pertinents » — même priorité P1, effort ré-estimé à 20 min, portée validée MOA sur 3 prompts (`creative.md`, `dev.md`, `ticket.md` en mention ciblée, `session.md` non modifié). Forme des 3 références et mini-règle « ne pas rouvrir §9 sans ticket explicite » validées. |
| 2026-04-23 | **Ticket 2 clôturé.** Exécuté : `prompt_creative.md` (8e puce doctrine + 3 références), `prompt_dev.md` (principe 6 + 3 lignes tableau), `prompt_ticket.md` (mention ciblée homepage légère). `prompt_session.md` non modifié. Pas de bump module. Récapitulatif mis à jour avec colonne `Statut`. |
| 2026-04-23 | **Ticket 1 clôturé.** Option A retenue : retrait `ckr-hero__subtitle-accent` (QWeb + SCSS), bump **19.0.1.6.16**, SPEC §7 inchangée. Contexte document + récapitulatif mis à jour. |
| 2026-04-23 | **Ticket 5 ouvert** — Homepage appétence perçue & partition vs [CADRAGE_DESIGN_CREATION_CK_V1.md](CADRAGE_DESIGN_CREATION_CK_V1.md). Fiche détaillée [TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md](TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md). Récapitulatif enrichi. |
| 2026-04-23 | **Brief Phase A** — création [BRIEF_CRÉA_PHASE_A_HOMEPAGE.md](BRIEF_CRÉA_PHASE_A_HOMEPAGE.md) ; lien depuis le ticket Phase A et le ticket 5 (récap). |
| 2026-04-23 | **PV recette Phase A** — trame [PV_RECETTE_PHASE_A_HOMEPAGE_CK.md](PV_RECETTE_PHASE_A_HOMEPAGE_CK.md) ; liens brief, ticket §7, ticket 5. |
