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
4. Vérification absence d'erreur serveur (logs Odoo) pendant ces accès.

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
```

## Critères GO

- Installation OK sans erreur XML/QWeb/asset.
- Update `-u` OK sans erreur.
- Pages `/`, `/shop`, `/shop/cart` répondent sans 500.
- Aucun traceback critique dans les logs pendant le smoke.
