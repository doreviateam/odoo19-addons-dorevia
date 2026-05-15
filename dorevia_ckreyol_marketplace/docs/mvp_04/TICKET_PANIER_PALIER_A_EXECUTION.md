# TICKET — Panier MVP04 — Palier A (exécution)

**ID** : `PANIER-MVP04-PALIER-A`  
**Date d'ouverture** : 2026-05  
**Priorité** : **P1**  
**Statut** : **Recette en cours — GO directionnel desktop** (P1–P6 à finaliser ; **priorité P6 mobile**)  
**Module** : `dorevia_ckreyol_marketplace`

**Dossier lié** : `docs/mvp_04/`  
**Références** : [README.md](README.md), [1_PANIER_PARCOURS.md](1_PANIER_PARCOURS.md), [TICKET_HEADER_NAV_MVP04.md](TICKET_HEADER_NAV_MVP04.md)

---

## 1. Objectif

Sécuriser le parcours panier MVP04 sur la baseline header V1 figée, sans ouvrir une refonte checkout.

Objectif produit :

- panier lisible et fiable ;
- transitions claires vers checkout ;
- non-régression invité/connecté ;
- desktop + mobile utilisables.

---

## 2. Périmètre Palier A

Inclus :

- accès panier header (icône + compteur cohérent) ;
- comportement après ajout produit vérifié : compteur mis à jour, feedback utilisateur clair, accès panier disponible ;
- état panier vide clair, avec sortie vers boutique ;
- état panier rempli exploitable (ajuster quantité / retirer ligne) ;
- CTA checkout visible et opérationnel ;
- contrôle desktop/mobile des actions principales.

Exclu :

- refonte checkout ;
- marketing panier (upsell, relance, reco) ;
- wishlist/favoris ;
- personnalisation avancée ;
- mini-panier / panneau latéral complexe.

---

## 3. Critères d'acceptation

1. Le panier est accessible clairement depuis le header desktop/mobile.
2. Le compteur panier reflète le contenu courant (pas d'écart visible).
3. L'état vide ne crée pas d'impasse (retour boutique explicite).
4. En panier rempli, quantité et suppression ligne fonctionnent sans blocage.
5. Le passage vers checkout est visible et suit le flux attendu.
6. Si l'achat invité est activé, aucun blocage compte n'est introduit au niveau panier.
7. Les interactions critiques restent utilisables en mobile (tactile).

---

## 4. Scénarios de recette minimaux

- **P1** : ajout produit depuis `/shop` -> compteur + ligne panier.
- **P2** : quantité Q1 -> Q2 -> Q1, total recalculé correctement.
- **P3** : suppression ligne, cohérence état vide/rempli ; en panier vide, une sortie vers la boutique reste disponible.
- **P4** : parcours invité panier -> checkout (sans forçage compte au niveau panier).
- **P5** : parcours connecté équivalent, sans divergence inattendue.
- **P6** : contrôle mobile des actions panier principales sur `/shop/cart` (voir **§4.3** pour la grille tactile détaillée).

---

## 4.1 Retour recette — desktop (GO directionnel)

Validation desktop : page panier propre, standard Odoo préservé, header V1 stable, compteur visible, résumé lisible, quantités / suppression / CTA paiement / lien continuer les achats conformes au ticket ; pas de refonte checkout cachée.

**Poursuite** : enchaîner la recette **P1 à P6** — **priorité P6** (mobile sur `/shop/cart` : quantité, suppression, total, CTA paiement, continuer les achats).

### Points de vigilance (non bloquants Palier A)

1. **CTA `Payer`** : style violet/Odoo encore visible — acceptable Palier A si on privilégie le standard ; harmonisation charte CK envisageable en lot ultérieur (hors scope strict Palier A si non demandé).
2. **`Enregistrer pour plus tard`** : fonctionnalité standard Odoo pouvant recouper les favoris / wishlist — **à surveiller** pour ne pas brouiller la doctrine `Panier ≠ Favoris` côté wording et parcours utilisateur ; arbitrage produit si friction.
3. **Mobile `/shop/cart`** : valider explicitement P6 (**checklist §4.3**).
4. **Top_0** : apparence parfois « pâle » en transition — réserve connue, **hors périmètre panier** ; non bloquant pour clôture recette panier.

---

## 4.2 Résultats recette P1–P6

À compléter au fil des passes (**priorité** : documenter **P6 mobile** en premier). **Statut** : `À faire` → `OK` / `KO` / `N/A`. Préciser **navigateur / viewport** ou **compte** (invité / connecté) dans **Notes** si utile.

| P | Scénario | Statut | Notes |
|---|----------|--------|-------|
| **P1** | Ajout depuis `/shop` → compteur + ligne panier | | |
| **P2** | Quantité Q1 → Q2 → Q1, total cohérent | | |
| **P3** | Suppression ligne ; panier vide / rempli cohérent ; sortie boutique toujours dispo si panier vide | | |
| **P4** | Invité : panier → checkout, pas de forçage compte au panier | | |
| **P5** | Connecté : équivalent P4, pas de divergence inattendue | | |
| **P6** | Mobile `/shop/cart` — grille tactile **§4.3** ; statut global une fois tous les points cochés | | |

---

## 4.3 P6 — Points à vérifier en premier (mobile / tactile)

**Contexte** : `/shop/cart` sur viewport mobile ; **GO** pour remplir la ligne **P6** du tableau §4.2 en premier. Cocher mentalement ou noter les écarts dans la colonne **Notes** de P6.

- panier accessible depuis le **header** ;
- **compteur** visible et cohérent avec le contenu ;
- **lignes panier** lisibles ;
- boutons **`−` / `+`** utilisables au doigt ;
- **suppression** ligne utilisable au tactile ;
- **total** lisible ;
- **CTA paiement** accessible sans ambiguïté ;
- lien **`Continuer vos achats`** (ou équivalent libellé standard) disponible ;
- pas de **blocage compte** au niveau panier (aligné critère §3 pt. 6 si achat invité actif) ;
- pas de **rupture visuelle majeure** liée au **header V1**.

---

## 4.4 Enchaînement après la passe P6 (mobile)

Une fois la ligne **P6** complétée dans §4.2 (statut + notes viewport / navigateur), poursuivre systématiquement le **tableau P1–P5** si une ligne reste vide ou « À faire » :

| Ordre | Scénario | Rappel utile |
|-------|----------|----------------|
| **P6** | *(déjà prioritaire)* | grille **§4.3** ; mobile `/shop/cart`. |
| **P1** | Ajout `/shop` → panier | peut être repassé en **mobile** pour confirmer compteur + toast (si actif) après ajout. |
| **P2** | Quantités / total | desktop suffit si P6 a validé **±** au tactile ; sinon repasser Q1→Q2→Q1 sur petit écran. |
| **P3** | Suppression + panier vide | vérifier **sortie boutique** en état vide (cf. P3 §4). |
| **P4** | Invité → checkout | session **sans connexion** ; pas d’obstacle compte sur **panier uniquement**. |
| **P5** | Connecté → équivalent | même scénario que P4 avec compte client. |

**Clôture Palier A recette** : toutes les lignes du §4.2 en **OK** (ou **N/A** documenté) → mettre à jour le **statut** en tête de ticket (ex. *Recette Palier A terminée*) et pointer les éventuels écarts résiduels dans **Notes** ou en nouvelle entrée **§7 Historique**.

---

## 5. Garde-fous d'implémentation

- Ne pas relancer de chantier header : baseline V1 figée.
- Ne pas modifier la doctrine `Panier ≠ Favoris`.
- Privilégier le comportement standard Odoo `website_sale` dès qu'il répond au besoin MVP04.
- Le clic sur l'icône panier doit rester proche du comportement standard Odoo, sauf arbitrage explicite.
- Ne pas introduire d'effets UI lourds non nécessaires.
- Privilégier un lot court, testable, réversible rapidement.

---

## 6. Sortie attendue

- implémentation Palier A terminée ;
- checklist recette P1..P6 passée ;
- écarts documentés ;
- base stable pour ouvrir ensuite le lot Favoris.

---

## 6.0 Tests automatisés (Odoo HttpCase)

Invariants HTTP couverts dans le module (complément à la **recette manuelle**) :

| Tag | Fichier | Rôle |
|-----|---------|------|
| `dorevia_ckr_shop_cart` | `tests/test_ckr_shop_cart_mvp04.py` | `/shop/cart` 200, header CK (lien panier + badge), gabarit checkout Odoo 19 (`#shop_cart`, résumé, panier vide + sortie boutique : CTA « Shop » / « Boutique » Odoo 19 ou libellés « Continue shopping » / FR) |

Commande-type (adapter `-d`) :

```text
odoo -d <base> --test-enable --stop-after-init \\
  --test-tags=dorevia_ckr_shop_cart
```

Non couverts ici (prévoir e2e ou tests contrôleurs séparés) : zones tactiles, panier **rempli**, bouton **Payer** actif, parcours invité jusqu’au paiement.

---

## 6.1 Zones techniques à inspecter

- `views/layout/ckr_header.xml` — accès panier / compteur header.
- `views/pages/ckr_shop.xml` — bouton ajout panier si concerné.
- templates standard `website_sale` panier / checkout — à privilégier avant surcharge.
- SCSS header / shop si ajustement visuel nécessaire.

---

## 7. Historique

| Date | Événement |
|------|-----------|
| 2026-05 | Création du ticket d'exécution Panier Palier A sur baseline Header CK V1 figée. |
| 2026-05 | GO directionnel recette **desktop** panier ; poursuite **P1–P6** ; vigilances notées (bouton Payer, « Enregistrer pour plus tard », mobile, Top_0). |
| 2026-05 | Ajout §**4.2** — tableau résultats recette **P1–P6** à compléter au fil des passes. |
| 2026-05 | Doctrine `Panier ≠ Favoris` unifiée ; **P3** explicite (sortie boutique si panier vide) ; priorité recette **P6 mobile** rappelée en en-tête / §4.1 / §4.2. |
| 2026-05 | **§4.3** — grille tactile **P6** `/shop/cart` (header, compteur, lignes, ±, suppression, total, CTA, continuer achats, compte, header V1) ; GO remplir **P6** en premier dans §4.2. |
| 2026-05 | **§4.4** — ordre d’enchaînement après P6 (**P1→P5**) et critères de **clôture recette** Palier A. |
| 2026-05 | **§6.0** — tests automatisés HttpCase tag ``dorevia_ckr_shop_cart`` + fichier ``tests/test_ckr_shop_cart_mvp04.py``. |
