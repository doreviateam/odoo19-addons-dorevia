# -*- coding: utf-8 -*-
{
    "name": "Site vitrine Radio Grand Lieu (démo locale)",
    "version": "19.0.1.1.2",
    "category": "Dorevia",
    "summary": "Accueil type radiograndlieu.fr + menus et pages d’entraînement pour Odoo Website",
    "description": """
        Module d’apprentissage : remplace le contenu vide de la page d’accueil du site web
        par une landing proche de la structure publique de Radio Grand Lieu
        (https://radiograndlieu.fr/), ajoute des menus et des pages stubs.

        Après installation : ouvrir le site public (/) — les textes sont modifiables
        en mode **Site web → Modifier** si la zone conserve ``oe_structure``.

        Lecteur « direct » : renseigner le paramètre système
        ``dorevia_website_radio_grandlieu.stream_url`` avec l’URL du flux ; sinon un lien
        vers le player officiel est affiché.

        Grille : modèle ``radiogl.programme.slot`` (menu **Site → Créneaux grille (démo)**),
        affiché sur l’accueil. Pied de page : copyright orienté association.

        Désinstaller le module pour revenir au gabarit d’accueil standard (vide).
    """,
    "author": "Dorevia Team",
    "license": "LGPL-3",
    "depends": ["website"],
    "data": [
        "views/radiogl_programme_slot_views.xml",
        "security/ir.model.access.csv",
        "data/ir_config_parameter_data.xml",
        "data/radiogl_programme_demo.xml",
        "views/radiogl_homepage_templates.xml",
        "views/radiogl_footer_templates.xml",
        "data/radiogl_stub_pages.xml",
        "data/radiogl_menus.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "dorevia_website_radio_grandlieu/static/src/css/radiogl_branding.css",
        ],
    },
    "installable": True,
    "application": False,
}
