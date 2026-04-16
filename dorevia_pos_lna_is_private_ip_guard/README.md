# dorevia_pos_lna_is_private_ip_guard

## Problème

Sur certaines builds Odoo 19 POS, le clic ou le flux **LNA** (Local Network Access) appelle
`isPrivateIp(this.pos.config.epson_printer_ip)` alors que `epson_printer_ip` peut valoir
`false` ou un type non chaîne côté RPC. L’implémentation historique faisait `ip.split(...)`
sans garde → **`TypeError: ip.split is not a function`**.

Le correctif officiel est dans Odoo (commit *guard isPrivateIp against non-string ip value*).
Ce module **patche** `Navbar.prototype.openLnaPopup` pour n’appeler `isPrivateIp` qu’avec une
**chaîne** valide.

## Installation

- Dépend de `point_of_sale`
- Installer **« Dorevia — correctif POS LNA (isPrivateIp) »** sur la base qui utilise le POS

## Périmètre

- Uniquement la méthode `openLnaPopup` du navbar POS (Epson / LNA).

## Suite

Quand l’image Odoo inclut le correctif amont, ce module devient redondant mais reste inoffensif.
