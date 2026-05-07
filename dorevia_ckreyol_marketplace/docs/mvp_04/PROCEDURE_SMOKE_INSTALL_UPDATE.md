# CK — Procédure smoke install/update/rendu

## Objectif

Détecter rapidement les régressions de chargement module, XPath/QWeb et rendu storefront après évolution.

## Pré-requis

- Environnement Odoo 19 CE démarré.
- Base de test dédiée.
- Module `dorevia_ckreyol_marketplace` disponible dans les addons paths.

## Séquence recommandée

1. Installation propre du module sur base neuve.
2. Mise à jour `-u dorevia_ckreyol_marketplace` sur base existante.
3. Vérification HTTP des pages critiques:
   - `/`
   - `/shop`
   - `/shop/cart`
   - `/shop/checkout` (accepter un **3xx** vers `/shop` si panier vide — pas de **500**)
4. Vérification absence d'erreur serveur (logs Odoo) pendant ces accès.

### Smoke **serveur persistant** (preuve runtime live)

Les `curl` ci-dessus sur `/`, `/shop`, etc. exigent un **serveur Odoo en marche** (sans `--stop-after-init`) et une **base sélectionnée** pour le site (ex. ouvrir une fois `/odoo?db=<MA_BASE>` ou équivalent selon déploiement). Sans cela, des **404** ou réponses hors contexte CK peuvent apparaître sans constituer une régression module.

**Preuve d’exécution archivée** (sandbox réelle, base `tenant_o7`, port hôte `18079`) : [`PV_SMOKE_LIVE_SERVEUR_CK.md`](./PV_SMOKE_LIVE_SERVEUR_CK.md).

## Commandes type (à adapter à l'environnement)

```bash
odoo -d <DB_TEST> -i dorevia_ckreyol_marketplace --stop-after-init
odoo -d <DB_TEST> -u dorevia_ckreyol_marketplace --stop-after-init
```

Exemples de checks HTTP:

```bash
curl -I "http://localhost:8069/"
curl -I "http://localhost:8069/shop"
curl -I "http://localhost:8069/shop/cart"
curl -I "http://localhost:8069/shop/checkout"
```

Adapter **hôte et port** (ex. `http://127.0.0.1:18079/...` derrière Docker).

## Critères GO

- Installation OK sans erreur XML/QWeb/asset.
- Update `-u` OK sans erreur.
- Pages `/`, `/shop`, `/shop/cart` répondent sans 500.
- `/shop/checkout` : pas de **500** ; une **redirection** vers `/shop` (ex. panier vide) est acceptable en smoke minimal.
- Aucun traceback critique dans les logs pendant le smoke.
