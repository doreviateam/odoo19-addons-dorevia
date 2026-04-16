# Changelog — `dorevia_membership_helloasso_bridge`

## 19.0.1.7.15 (2026-04-16)

### Comportement (E2 — rail V1)

**Typologie exigée (opt-in)** : sur le compte HelloAsso, option **Exiger une typologie adhérent (V1)** (`membership_bridge_require_member_type`, **désactivée par défaut**). Si activée, le service pont **V1** refuse avec **`UserError`** explicite lorsque le contact payeur n’a pas de **`member_type_id`**. Message centralisé dans `membership_helloasso_bridge_user_messages` (story **S7-2** option **A**).

---

## 19.0.1.7.14 (2026-04-16)

### Expérience opérateur (pivot)

**Recherche** : filtre **Pont V2 — sans facture** (compte en rail **V2 comptable** et pivot **sans** `membership_v2_out_invoice_id`) — story **S6-4** ; uniquement vue recherche, sans champ calculé supplémentaire.

---

## 19.0.1.7.13 (2026-04-16)

### Expérience opérateur (fiche pivot V2)

**Boutons** en haut de fiche (`oe_button_box`) : ouverture directe de la **facture V2** et du **paiement enregistré** (`action_open_membership_v2_invoice` / `action_open_membership_v2_account_payment`), visibles seulement en rail **V2 comptable** et si la pièce est renseignée (story **S6-3**).

---

## 19.0.1.7.12 (2026-04-16)

### Expérience opérateur (pivot)

**Recherche** : filtre **Pont V2 — déjà traité (noop)**. **Fiche** (bloc V2) : champ **Moyen HelloAsso (pivot)** en lecture seule, à côté de l’état (story **S6-2**).

---

## 19.0.1.7.11 (2026-04-16)

### Comportement (rail V2 — facture client)

Le **mode de paiement** attendu sur la facture (`preferred_payment_method_line_id`, libellé **Mode de paiement** en UI) est renseigné avec la **même ligne de méthode** que celle utilisée pour l’encaissement HelloAsso (journal banque + classification pivot), **avant** la comptabilisation — et réaligné si besoin après `action_post`. Même logique si une facture **brouillon** V2 est postée dans le chemin idempotent.

---

## 19.0.1.7.10 (2026-04-16)

### Expérience opérateur (fiche pivot V2)

Bloc **Adhésion — constatation (rail V2)** sur la fiche `dorevia.helloasso.payment` : affichage **masqué** si le compte n’est pas en **V2 comptable** ; **badge** pour l’état ; **dernière mise à jour du pivot** (`write_date`) ; pièces **facture / paiement** ; message d’**erreur** dans un sous-groupe visible uniquement en cas d’échec (story **S6-1**).

---

## 19.0.1.7.9 (2026-04-16)

### Expérience opérateur (pivot)

Sur la **liste** des paiements HelloAsso : colonnes optionnelles **État pont V2** et **Facture V2**. Dans la **recherche** : filtres **Pont V2 — erreur / à traiter / traité** (story **S5-1**).

---

## 19.0.1.7.8 (2026-04-16)

### Comportement (rail V2 — facture client)

À la **création** de la facture V2, les champs **Marketing (UTM)** sur `account.move` sont renseignés à partir du pivot : **campagne** (`campaign_name`, ou libellé de secours `HelloAsso (<réf>)` si vide), **médium** (`campaign_type`, ou `HelloAsso — Adhésion` si vide), **source** fixe **HelloAsso** (enregistrement `utm.source` réutilisé ou créé). Dépendance explicite sur le module **`utm`**.

---

## 19.0.1.7.7 (2026-04-16)

### Technique (S3-1 piste C)

Les **libellés UserError** communs au pont **V1** et à la **constatation V2** (produit adhésion, e-mail payeur, archivés, sociétés, fenêtre de dates) sont **centralisés** dans `models/membership_helloasso_bridge_user_messages.py` — **aucun** changement de wording ni de comportement métier.

---

## 19.0.1.7.6 (2026-04-16)

### Expérience opérateur

Sur le **formulaire compte HelloAsso**, lorsque le **pont adhésion** est activé, un **encadré d’aide** rappelle les **refus automatiques** du pont (pivot ou contact archivé, e-mail, produit / dates) et les **actions** à mener côté Odoo, **sans** toucher au miroir HelloAsso.

---

## 19.0.1.7.5 (2026-04-16)

### Technique (garde-fous archivé S3-1 / S4-1)

La résolution des contacts pour les refus **partenaire archivé** et la recherche partenaire côté **V2** utilisent désormais `active_test=False` sur `res.partner`, afin que le message métier « contact archivé » s’applique bien (Odoo exclut par défaut les enregistrements inactifs du `search()`).

---

## 19.0.1.7.4 (2026-04-15)

### Comportement (piste B — éligibilité pivot)

Les enregistrements pivot **`dorevia.helloasso.payment`** **archivés** (`active = False`) sont **refusés** par le pont **V1** et la **constatation V2** avant toute création de ligne d’adhésion / facture, avec un **message d’erreur métier** clair. Alignement des deux rails ; **aucune** modification des champs miroir HelloAsso.

---

## 19.0.1.7.3 (2026-04-15)

### Comportement (Sprint 3 — story S3-1, piste A)

Les paiements HelloAsso rattachés à un **partenaire archivé** (`active = False`) sont désormais **refusés explicitement** par le pont (**V1** — ligne d’adhésion sans facture — et **rail comptable V2**), avec un **message d’erreur métier** clair (`UserError`). **Aucun champ miroir HelloAsso** n’est modifié par cette règle ; seule la **décision métier** côté bridge change (alignement V1 / V2).

**Action utilisateur** : réactiver le contact ou traiter le dossier manuellement si l’adhésion / la constatation doit passer malgré l’archivage.

Références : `Zedocs/odoo19/membership/STORY_S3_1_PREMIERE_REGLE_METIER_PILOTE_BRIDGE.md`.
