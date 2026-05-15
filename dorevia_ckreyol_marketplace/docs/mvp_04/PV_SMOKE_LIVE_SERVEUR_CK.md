# PV — Smoke live serveur persistant CK

**Date** : 2026-05-07  
**Module** : `dorevia_ckreyol_marketplace`  
**Portée** : Preuve runtime minimale post palier pré-ouverture technique (complément **P5**)

---

## 1. Décision

**GO smoke live serveur persistant.**

Ce verdict clôture la **preuve HTTP live** manquante sur un Odoo **continu** (hors `--stop-after-init`). Il ne remplace pas un lot **E2E marchand étendu** (checkout complet, paiement, livraison).

---

## 2. Environnement d’exécution

| Élément | Valeur |
| --- | --- |
| Conteneur Odoo | `sandbox-odoo19-odoo-1` |
| Base PostgreSQL | `tenant_o7` |
| Port côté hôte | `18079` (mapping vers le serveur Odoo du conteneur) |
| Session Website | Initialisée via `/odoo?db=tenant_o7` avant les `curl` |

---

## 3. Mise à jour module

- Commande : `-u dorevia_ckreyol_marketplace` (log type `/tmp/ckr_smoke_update.log`).
- **Code retour** : `0`.
- **Filtre log** `ERROR|CRITICAL|Traceback|QWeb|XPath|500` : **aucune occurrence** (sortie vide).

---

## 4. Résultats HTTP live (`curl -I`, session `tenant_o7` active)

| Endpoint | Résultat |
| --- | --- |
| `/` | `HTTP/1.1 200 OK` |
| `/shop` | `HTTP/1.1 200 OK` |
| `/shop/cart` | `HTTP/1.1 200 OK` |
| `/shop/checkout` | `HTTP/1.1 303 SEE OTHER` → `Location: /shop` |

**Lecture produit** : le **303** sur `/shop/checkout` avec renvoi vers `/shop` est interprété comme un **repli cohérent** en contexte **panier vide** / checkout non initialisé — **pas** comme une erreur applicative, dès lors qu’aucune **500** ni traceback n’apparaît en logs.

**Note méthode** : des **404** peuvent être observés **sans** sélection de base (`/odoo?db=…`) ; ils ne sont pas retenus comme régression CK une fois la session **`tenant_o7`** correctement initialisée.

---

## 5. Logs runtime (serveur persistant)

Après navigation sur les URLs ci-dessus : **aucune** ligne rapportée parmi :

- `ERROR`, `CRITICAL`, `Traceback`, `QWeb`, `XPath`, `HTTP 500`.

---

## 6. Limites conservées

- Ce smoke **ne substitie pas** un périmètre **E2E marchand élargi** (paiement test, livraison, mails, multi-navigateurs, etc.).
- Il valide une **stabilité de rendu et de routage HTTP** minimale sur les entrées critiques listées après **`-u`** sur la base désignée.

---

## 7. Références croisées

- Procédure générale install/update/rendu : [`PROCEDURE_SMOKE_INSTALL_UPDATE.md`](./PROCEDURE_SMOKE_INSTALL_UPDATE.md)
- PV jalons pré-ouverture : [`PV_PRE_OUVERTURE_COMMERCIALE.md`](./PV_PRE_OUVERTURE_COMMERCIALE.md)
