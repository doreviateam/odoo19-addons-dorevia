# -*- coding: utf-8 -*-
{
    "name": "Dorevia — HelloAsso Members",
    "version": "19.0.1.30.1",
    "category": "Dorevia",
    "summary": "Synchronisation HelloAsso Membership → res.partner (API v5)",
    "description": """
        Module métier **Members** (refonte HelloAsso) :
        - **Compte HelloAsso** (``dorevia.helloasso.account``) : **une société Odoo = un compte** (environnement, slug, identifiants) ; repli res.company + ICP si aucun compte
        - Synchro paiements Membership éligibles → contacts
        - Champs ``res.partner`` (traçabilité HelloAsso, type d'adhésion, compte source)
        - Prévisualisation lecture seule, planificateur **actif par défaut** (toutes les **6 h** si identifiants OK ; modifiable), actions Paramètres
        - **OCA** ``partner_firstname`` (copie locale sous ``odoo19-addons-oca/partner_firstname``, dépôt
          `OCA/partner-contact` 19.0) : prénom / nom sur les contacts ; le pont V2 renseigne
          ``firstname`` / ``lastname`` sur les contacts créés depuis HelloAsso.

        Dépend du socle ``dorevia_helloasso_connector`` (client HTTP, journal).
    """,
    "author": "Dorevia Team",
    "website": "https://doreviateam.com",
    "license": "LGPL-3",
    "icon": "/dorevia_helloasso_members/static/description/icon.png",
    "depends": [
        "base",
        "base_setup",
        "contacts",
        "partner_firstname",
        "dorevia_helloasso_connector",
    ],
    "external_dependencies": {
        "python": ["requests"],
    },
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rule_helloasso_res_partner.xml",
        "views/helloasso_account_views.xml",
        "data/ir_cron_data.xml",
        "views/helloasso_preview_wizard_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "application": False,
    "post_init_hook": "post_init_hook",
}
