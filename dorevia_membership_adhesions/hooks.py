# -*- coding: utf-8 -*-

# Libellé du menu racine applicatif « membership » (toutes langues actives).
ROOT_MEMBERSHIP_APP_MENU_LABEL = "AssoHello"


def sync_root_app_menu_name(env):
    """Force ``ROOT_MEMBERSHIP_APP_MENU_LABEL`` pour toutes les langues (évite le reste « Membres » en fr_FR)."""
    menu = env.ref("membership.menu_association", raise_if_not_found=False)
    if not menu:
        return
    for lang in env["res.lang"].search([("active", "=", True)]):
        menu.with_context(lang=lang.code).write({"name": ROOT_MEMBERSHIP_APP_MENU_LABEL})


def post_init_hook(env):
    """Odoo 19 : ``post_init_hook`` reçoit un ``Environment``."""
    sync_root_app_menu_name(env)
