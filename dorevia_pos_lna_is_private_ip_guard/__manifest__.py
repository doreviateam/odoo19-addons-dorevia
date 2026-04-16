# -*- coding: utf-8 -*-
{
    "name": "Dorevia — correctif POS LNA (isPrivateIp)",
    "version": "19.0.1.0.0",
    "category": "Point of Sale",
    "summary": "Évite le crash JS ip.split quand epson_printer_ip n’est pas une chaîne (LNA / Epson).",
    "author": "Dorevia",
    "license": "LGPL-3",
    "depends": ["point_of_sale"],
    "data": [],
    "assets": {
        "point_of_sale._assets_pos": [
            "dorevia_pos_lna_is_private_ip_guard/static/src/js/navbar_lna_guard.js",
        ],
    },
    "installable": True,
    "application": False,
}
