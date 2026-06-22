# Retour Dev principal — Brief MOA Navigation CK V2

| Champ | Valeur |
| --- | --- |
| **Document source** | [`note_06.md`](./note_06.md) — Brief MOA · Navigation CK V2 |
| **Rédacteur** | Dev principal |
| **Date** | 2026-06-21 |
| **Contexte technique** | Instance `dorevia_ck_marketone_01` · modules `dorevia_ck_theme` / `dorevia_ck_marketone_content` · post-merge PR #77 |
| **Verdict Dev proposé** | **À AMENDER** — doctrine solide, cadrage exploitable, arbitrages MOA requis avant Lot Navigation |
| **Suite MOA** | [`note_06_reponse_moa.md`](./note_06_reponse_moa.md) — arbitrages intégrés dans [`note_06.md`](./note_06.md) (2026-06-21) |

---

## 1. Synthèse

La note est **claire, bien structurée et alignée avec la vision CK** telle qu’elle est déjà traduite en code (triptyque Acheter · Apprendre · Contribuer, distinction Apprendre / Découvrir, phasage progressif, hors périmètre explicite).

En tant que Dev principal, je **souscris à la direction produit** et au principe « header marchand d’abord, attachement via Découvrir ensuite ». La note est **implémentable sur Odoo 19 CE** dans l’esprit déjà retenu (menus `website.menu`, mega-menu natif, pages CMS, snippets, pas de surcouche front).

En revanche, le menu cible proposé **ne correspond pas tel quel à ce qui est livré aujourd’hui** ni à certaines décisions documentées en V1.2.x. Avant validation MOA, il faut **trancher explicitement** quelques écarts — sinon le lot Navigation risque une refonte header en pleine contradiction avec la recette Phase 1 déjà GO.

---

## 2. Points forts (à conserver tels quels)

### Doctrine et vocabulaire

La distinction **Apprendre** (intention produit) / **Découvrir** (libellé UI) est essentielle. Elle évite des dérives MOE (« remplacer Découvrir par Apprendre dans le header ») et reste cohérente avec la fiche produit Lot 2, où l’onglet/ancre **Découvrir** est déjà en place côté front.

### Séparation des parcours

Séparer parcours d’achat (catégories commerce) et parcours d’attachement (Découvrir) est sain UX et sain techniquement : liens catalogue = `product.public.category` ; contenus = `website.page` / blog / futures pages éditoriales.

### Phasage et hors périmètre

Les §11–12 de `note_06` sont réalistes et conformes à notre mode de livraison (lots courts, recettables). Le rappel « pas de refonte fiche produit, mais liens CMS possibles » colle exactement à ce qu’on peut faire **sans nouveau modèle métier** — c’est déjà la piste retenue post Lot 2.

### Principes de mise en œuvre (§13)

Alignés avec le socle actuel : snippets first, Website Builder, identité CK, pas de HTML maquette injecté. Rien à contredire.

---

## 3. Écarts avec l’existant — à arbitrer MOA

| Sujet | `note_06` (cible) | État actuel / doc V1.2.x | Risque si non tranché |
| --- | --- | --- | --- |
| Entrées commerce top-level | **6 items** : Tous nos produits · Épicerie · Boissons · Soin · Artisanat · Découvrir | Header Phase 1 livré : **Boutique · Découvrir · Professionnels** ([`COMPOSITION_HEADER_V1_2.md`](../design/maquette_01.2/COMPOSITION_HEADER_V1_2.md)) | Refonte header non planifiée comme simple renommage |
| **Professionnels** | Absent du menu cible | Entrée Phase 1 validée → `/professionnels` | Régression parcours B2B si retiré sans relocation |
| **Boutique** vs **Tous nos produits** | « Tous nos produits » | « Boutique » → `/shop` | Wording + SEO + tests HTTP à mettre à jour |
| Univers home S4 | 5 racines commerce dont **Boissons** | Home S4 figée sur **3 cards** : Épicerie · Soin & bien-être · Artisanat ([`NOTE_ARCHITECTURE_SECTION4_UNIVERS_V1.md`](../design/maquette_01.2/NOTE_ARCHITECTURE_SECTION4_UNIVERS_V1.md)) | Incohérence navigation header ↔ home ↔ catégories BO |
| Mega **Découvrir** | Sous-menu éditorial (6 entrées) | Maquette / guide V1.2 : mega avec colonne « Acheter par univers » ([`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](../design/maquette_01.2/GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md)) | `note_06` **inverse** la logique : commerce au top-level, éditorial sous Découvrir — pivot structurel, pas un détail |
| Libellé **Soin** | Court, évolutif vers « Soin & Beauté » | Home : **Soin & bien-être** · catégorie BO **Maison & bien-être** | Écart libellé menu / card home / slug catégorie |

**Recommandation Dev** : ajouter au brief un **tableau de correspondance BO** (menu → `product.public.category` → URL → produits publiés minimum) et une **décision explicite sur Professionnels** (conserver en top-level ? déplacer footer / bandeau home / page gateway ?).

---

## 4. Faisabilité technique par phase

### Phase 1 — Navigation marchande claire

**Faisable · effort modéré · 1 lot recettable**

Implémentation prévue :

- synchronisation menus via data XML + hook post-init (pattern reproductible sur le dépôt) ;
- liens catégories **uniquement si catégorie BO existe et a au moins un produit publié** — sinon 404 (déjà vécu : Packs & découvertes) ;
- styles header existants (`website_header.scss`, mega `.o_mega_menu`) suffisants pour un menu plus dense ;
- recette obligatoire **390 px** : 6 entrées top-level + mega Découvrir = **point de vigilance UX mobile** (wrap, burger, profondeur accordéon).

**Prérequis MOA avant dev** :

1. valider la **taxonomie catégories racines** (Épicerie / Boissons / Soin / Artisanat) côté catalogue seed ;
2. confirmer le **sort de Professionnels** ;
3. décider si Phase 1 inclut déjà le **sous-menu Découvrir complet** ou une **coquille** (entrée présente, liens actifs seulement vers pages existantes).

### Phase 2 — Structuration de Découvrir

**Faisable · effort moyen · dépend fortement du contenu éditorial**

Chaque sous-entrée = page CMS bootstrap + recette visuelle + éventuel module blog (`website_blog` pour « Le blog CK »). Pas de dev lourd si on reste en pages composées + menus enfants.

**Dépendances** :

- charge rédactionnelle MOA (Producteurs, Histoires, Recettes) ;
- pas de liens fictifs dans le mega (règle déjà actée V1.2) ;
- ordre du sous-menu (§6 de `note_06`) cohérent avec maturité contenu — OK, mais **La communauté** et **Contribuer** peuvent être des pages « teaser » en Phase 2 sans backend communautaire.

### Phase 3 — Contribution utilisateur

**Faisable mais hors périmètre court terme · effort élevé**

Formulaires, modération, comptes contributeurs = nouveau socle (modèles, workflows, droits, anti-spam). Le §12 de `note_06` est correct à les exclure du premier lot. Je recommande de **ne pas laisser ces entrées actives en navigation** tant que la Phase 3 n’est pas arbitrée — pages placeholder ou items masqués.

### Articulation commerce ↔ culture (§10)

**Faisable en léger · compatible avec l’existant**

Sans refonte fiche produit :

- champs BO ou blocs parser `website_description` / sections Lot 2 ;
- liens sortants vers pages CMS (`/histoires/...`, `/recettes/...`) ;
- option ultérieure : relation M2M produit ↔ page éditoriale.

C’est la bonne trajectoire post Lot 2 ancres/sections longues.

---

## 5. Risques techniques et produit

1. **Menu trop chargé** — 6 entrées + mega sur mobile : risque lisibilité / taux de clic. Recette UX desktop + 390 px à inclure dans les critères d’acceptation MOA.
2. **Catégories vides** — chaque entrée commerce doit être **gated** par catalogue réel (sinon 404 et perte confiance).
3. **Double navigation** — si le mega Découvrir conserve une colonne « Acheter par univers » *en plus* des 5 entrées commerce, on crée une redondance. `note_06` semble l’exclure implicitement : **à acter explicitement**.
4. **Dette de tests** — les tests header (`test_ck_phase10_header_compose.py`) assertent aujourd’hui `Boutique · Découvrir · Professionnels`. Tout lot Navigation devra mettre à jour les assertions **et** le dictionnaire maquette ↔ Odoo.
5. **Professionnels** — parcours B2B déjà composé ; le retirer du header sans alternative visible serait une régression fonctionnelle.

---

## 6. Amendements suggérés à `note_06`

Avant validation MOA, enrichir le brief avec :

1. **§4 bis — Correspondance catalogue BO**  
   Tableau menu → catégorie Odoo → slug → statut (publié / à créer / différé).

2. **§4 ter — Entrées transverses hors triptych**  
   Statut de **Professionnels**, **Contact**, **Compte / Panier / Recherche** (hors menu principal mais présents header).

3. **§6 — Règle de visibilité sous-menu Découvrir**  
   « Un lien n’apparaît en navigation que si la page cible existe et est publiée » (reprise règle M4 V1.2).

4. **§11 Phase 1 — Livrable Dev explicite**  
   - menus synchronisés module ;  
   - mega Découvrir minimal ou placeholder ;  
   - recette HTTP + mobile ;  
   - **pas** de modification home S4 dans le même lot sauf arbitrage MOA (sinon mélange deux sujets).

5. **§14 — Critère 9**  
   Cohérence header ↔ home S4 ↔ arborescence `product.public.category`.

6. **§15 — Verdict Dev**  
   Reprendre le tableau §8 ci-dessous.

---

## 7. Proposition de séquencement Dev (après validation MOA amendée)

```text
Lot Nav-1 (Phase 1)
  → Arbitrages MOA (Professionnels, taxonomie, libellés)
  → Seed / alignement catégories BO
  → Sync website.menu + mega Découvrir (liens réels only)
  → Recette QA header 1280 + 390 + non-régression Professionnels

Lot Nav-2 (Phase 2 — par sous-entrée)
  → Bootstrap page CMS + menu enfant + recette visuelle
  → Ordre : Producteurs & territoires → Histoires → Recettes → Blog
  → Communauté / Contribuer en teaser ou masqués

Lot Nav-3 (Phase 3)
  → Cadrage technique séparé (hors note_06 seule)
```

---

## 8. Verdict Dev principal

| Critère | Appréciation |
| --- | --- |
| Clarté doctrine Acheter · Apprendre · Contribuer | ✅ Validé |
| Distinction Apprendre / Découvrir | ✅ Validé — à rappeler en recette MOE |
| Menu commerce top-level | ⚠️ Validé en principe — mapping BO et mobile à préciser |
| Sous-menu Découvrir | ✅ Validé en phasage — pas tout en Lot 1 |
| Hors périmètre Phase 1 | ✅ Validé |
| Alignement avec header V1.2 livré | ❌ Écart majeur — amendement requis |
| Prêt pour ticket Dev | ⚠️ Après arbitrages §3 et amendements §6 |

**Position Dev** : la note peut servir de **base MOA solide** pour la Navigation V2. Je recommande **À AMENDER** plutôt qu’un GO immédiat, puis un **GO MOA** sur une version enrichie (tableau BO + sort Professionnels + règle visibilité liens). Dès validation, le Lot Nav-1 est **enchaînable** sans refonte lourde du thème ni rupture avec le socle post PR #77.

**Mise à jour 2026-06-21** : la MOA a tranché les arbitrages signalés — voir [`note_06_reponse_moa.md`](./note_06_reponse_moa.md) et le brief amendé [`note_06.md`](./note_06.md). Le retour Dev est **accepté** ; le brief est **prêt pour ticket Lot Nav-1**.

---

## 9. Documents de référence consultés

| Document | Rôle |
| --- | --- |
| [`note_06.md`](./note_06.md) | Brief MOA source |
| [`COMPOSITION_HEADER_V1_2.md`](../design/maquette_01.2/COMPOSITION_HEADER_V1_2.md) | Header Phase 1 livré |
| [`GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md`](../design/maquette_01.2/GUIDE_TRADUCTION_MAQUETTE_ODOO_CK_V1.md) | Traduction maquette → Odoo |
| [`NOTE_ARCHITECTURE_SECTION4_UNIVERS_V1.md`](../design/maquette_01.2/NOTE_ARCHITECTURE_SECTION4_UNIVERS_V1.md) | Home S4 · Acheter par univers |
| [`NOTE_FICHE_PRODUIT_LOT2_ANCRES_CK_V1.md`](../design/NOTE_FICHE_PRODUIT_LOT2_ANCRES_CK_V1.md) | Ancre / onglet Découvrir fiche produit |
