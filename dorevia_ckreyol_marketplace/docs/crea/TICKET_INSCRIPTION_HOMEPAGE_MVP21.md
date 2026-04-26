# TICKET — Inscription Homepage MVP2.1 (newsletter / cercle)

**ID** : `INSCRIPTION-HOMEPAGE-MVP21`  
**Date d’ouverture** : 2026-04-24  
**Priorité** : **P2** (relationnel ; postérieur aux blocs preuve d’offre — hero, Explorer, sélection).  
**Statut** : **Accepté (GO MOA)** — **2026-04-25** ; preuve : [PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md](PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md)  
**Exécution : clos (2026-04-25)** — voir **PV** ci-dessus ; checklists §0 soldées.  
**Module** : `dorevia_ckreyol_marketplace`  
**Périmètre** : **snippet Inscription / newsletter** + insertion page d’accueil + SCSS associés.

**Décision position (gel)** : [DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md](../mvp_02/DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md) — **après** Éditorial, **avant** Réassurance.

**Rattachement** : [TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md](TICKET_HOMEPAGE_APPETENCE_PARTITION_V1.md) ; cadrage copy §5 [1_HOMEPAGE.md](../mvp_02/1_HOMEPAGE.md).

---

## Contexte

La **structure homepage MVP2.1** est **gelée** côté conception ([1_HOMEPAGE.md](../mvp_02/1_HOMEPAGE.md), **Gel conception**).  
Le bloc **Inscription** est à insérer **après** `ckr_snippet_editorial` et **avant** `ckr_snippet_trust` — repère déjà commenté dans [`views/pages/ckr_homepage.xml`](../../views/pages/ckr_homepage.xml).

**Décision MOA complémentaire (2026-04-24)** — Pilotage [README MVP 02](../mvp_02/README.md) : V1 livrable = **formulaire léger custom** ; pas d’espace membre ni automation avancée. **RGPD** : consentement explicite, **lien** vers **`/privacy`** (libellé interface : **politique de confidentialité**), désinscription. **`mass_mailing`** : n’envisager **que** si cela **simplifie** sans alourdir. **Visuels** : priorité **`docs/assets/`** (réel produit / producteur / geste — pas touristique ni illustratif ; pas d’externes prod. sans validation MOA).

---

## Objectif

Créer un bloc **relationnel** permettant de transformer un visiteur intéressé en **contact qualifié**, sans pression commerciale.

---

## Périmètre

### Position

À insérer dans **`views/pages/ckr_homepage.xml`** **entre** :

- `ckr_snippet_editorial` ;
- `ckr_snippet_trust`.

Nouveau snippet dédié (ex. `ckr_snippet_newsletter` / nom validé en PR) + `t-call` dans la page homepage.

### Contenu (gel MOA pour ce ticket)

| Élément | Texte / règle |
|---------|----------------|
| **Titre** | Rejoignez le cercle C-Kreyol |
| **Texte** | Recevez nos sélections curatées, les histoires de nos producteurs et nos nouveaux arrivages directement dans votre boîte mail. |
| **Champ** | Adresse e-mail |
| **Préférences** *(optionnelles)* | Saveurs ; Épicerie ; Cadeaux ; Origines ; Nouveautés ; Histoires de producteurs |
| **CTA** | S’abonner |
| **Confidentialité** | En vous abonnant, vous acceptez notre politique de confidentialité. Vous pouvez vous désinscrire à tout moment. |
| **Lien RGPD** | Route **`/privacy`** ; le segment **politique de confidentialité** (dans la phrase ci-dessus ou équivalent) est le **texte de lien** visible (`<a href="/privacy">politique de confidentialité</a>`). |

### Avant mise en production (prérequis légal)

- Page **`/privacy`** : **existante**, **accessible**, avec **contenu légal minimal conforme** (hors périmètre rédactionnel détaillé de ce ticket, **bloquant** go-live si absente ou vide).

---

## Rendu attendu

- Composition **split** : visuel à gauche / **formulaire** à droite ;
- Visuel **producteur**, **créateur**, **atelier** ou **geste métier** (pas image touristique décorative) ;
- Ton **calme**, chaleureux, **non agressif** ;
- E-mail + préférences **simples** ; **CTA** visible ;
- **Responsive** desktop / mobile validé MOA.

---

## Contraintes

- Pas de **pop-up** ; pas de **réduction** promise ; pas de **fausse urgence** ; pas d’image **touristique** ;
- Ne pas suggérer une **communauté** complexe si seule l’inscription e-mail est livrée ;
- **RGPD** : consentement **explicite**, **lien** vers **`/privacy`** (libellé **politique de confidentialité**), **désinscription** prévue et traçable.

---

## Points techniques (implémentation)

- **Base retenue** : **formulaire léger custom** (POST contrôleur / `website_form` ou équivalent) — **documenter** dans la PR.
- **`mass_mailing`** : **uniquement** si arbitrage dev + MOA conclut que ça **simplifie** (dépendances `__manifest__.py`, parcours) ;
- **Stockage** des préférences (tags, champs custom, etc.) — à figer avec le choix formulaire ;
- **URL** politique de confidentialité — **`/privacy`** (ne pas substituer d’URL sans ticket MOA) ;
- **Comportement après soumission** (message merci, redirection légère, opt-in double si requis).

---

## Hors périmètre

- **Espace membre** ; **compte communautaire** ;
- **Segmentation marketing avancée** ; **automation** e-mailing complexe.

---

## Critères d’acceptation

- [x] Bloc **visible** au **bon emplacement** — après `ckr_snippet_editorial` si rendu, avant `ckr_snippet_trust` ([`ckr_homepage.xml`](../../views/pages/ckr_homepage.xml), [DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md](../mvp_02/DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md)) ;
- [x] Formulaire e-mail **fonctionnel** — POST `/ckr/circle/subscribe` ; messages retour query `cc_cir` ;
- [x] **Préférences** affichées sans complexité excessive (cases optionnelles) ;
- [x] **Message confidentialité** avec lien **`/privacy`** (libellé **politique de confidentialité**) ;
- [x] **Rendu responsive** validé MOA ;
- [x] **Copy** sobre, alignée marque CK (**PV**).

---

## Recette

- **PV** : [PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md](PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md) — **GO MOA 2026-04-25**.

---

## 0. Prêt pour dev — checklist pilotage *(soldée — clos 2026-04-25)*

1. [x] **Branche** / intégration — `ckr_snippet_circle` + chaînage homepage livrés.
2. [x] **Arbitrage technique** — formulaire **léger custom** (sans `mass_mailing` obligatoire en V1).
3. [x] **Page `/privacy`** — route module + contenu de base (**PV** §2 bis).
4. [x] **Spec** — bloc **centré** (split visuel reporté ; **N/A** V1, voir **PV**).
5. [x] **Copy** — cercle C-Kreyol validée MOA (**PV**).
6. [x] **RGPD** — mention + lien confidentialité ; parcours désinscription selon arbitrage produit (hors scope détail **PV**).
7. [x] **`__manifest__.py`** — conforme livraison module.
8. [x] **Recette** — [PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md](PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md) **GO MOA**.
9. [x] **Instance / relecteur** — recette MOA complétée.

---

## Livrables techniques (synthèse)

| Livrable | Détail |
|----------|--------|
| **QWeb** | Snippet section + formulaire (champs, CTA, lien **`/privacy`** — libellé **politique de confidentialité**). |
| **Python** | Contrôleur ou héritage `website` / `mass_mailing` selon arbitrage. |
| **SCSS** | Bloc centré (`ckr_circle`), responsive, cohérence tokens CK. |
| **Homepage** | `t-call` du snippet à l’emplacement défini dans `ckr_homepage.xml`. |

---

## Historique

| Date | Changement |
|------|------------|
| 2026-04-24 | Création — alignement [DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md](../mvp_02/DECISION_ORDRE_BLOCS_HOMEPAGE_MVP21.md) + [1_HOMEPAGE.md](../mvp_02/1_HOMEPAGE.md) §5. |
| 2026-04-24 | **MOA** — formulaire custom ; RGPD ; `mass_mailing` optionnel si simplifie ; assets `docs/assets/` ; [README MVP 02](../mvp_02/README.md) pilotage. |
| 2026-04-24 | **RGPD** — URL **`/privacy`** ; libellé lien **politique de confidentialité** ; prérequis page `/privacy` avant prod. |
| 2026-04-25 | **Clôture** — **GO MOA** ; [PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md](PV_RECETTE_INSCRIPTION_HOMEPAGE_MVP21_CK.md) ; **Exécution : clos** ; critères + checklist §0 **soldés**. |
| 2026-04-25 | **Post-audit** — correctif contrôleur `sub.search` ; pages `/privacy` / `/terms` ; tests `dorevia_ckr_circle` — voir **PV** § post-recette et [README module](../../README.md) § Pages légales. |
