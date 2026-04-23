# -*- coding: utf-8 -*-
"""Hooks d installation / mise a jour pour dorevia_ckreyol_marketplace.

Contexte :
    Sur Odoo 19 CE, chaque site web possede son propre menu racine
    ("Top Menu for Website N"), copie dynamique du template
    `website.main_menu`. Impossible de cibler ce menu via un simple
    `search` XML sur le nom. On passe donc par un hook Python qui
    utilise `website.menu_id` (champ relationnel pointant sur la racine
    du site courant).

Portee :
    1. Suppression des 3 entrees natives installees par `website` et
       `website_sale` sous le menu racine (Home, Shop, Contact us)
       pour eviter les doublons avec le menu Option B.
    2. Creation des 6 entrees Option B :
       Boutique, Collections, Offrir, Recettes, A propos, Contact.
    3. Nettoyage d eventuels website.page stale pointant sur "/" qui
       auraient ete crees par des versions anterieures du module
       (desormais la homepage reste portee par website.homepage_page
       standard, via heritage du template website.homepage).

Idempotent : on peut rejouer la sequence a l install comme au
upgrade (voir migrations/19.0.1.0.1/post-migration.py).

Reference : docs/STRUCTURE_MENU_PRINCIPAL.md, ADR-CKR-003.
"""

import logging

_logger = logging.getLogger(__name__)


CKR_MENU_ITEMS = [
    # (nom, url, sequence)
    ("Boutique",    "/shop",        10),
    ("Collections", "/collections", 20),
    ("Offrir",      "/offrir",      30),
    ("Recettes",    "/recettes",    40),
    ("A propos",    "/a-propos",    50),
    ("Contact",     "/contact",     60),
]

# URLs des entrees natives a retirer du menu racine du site.
NATIVE_MENU_URLS_TO_REMOVE = ("/", "/shop", "/contactus")


def _sync_ckr_menus(env):
    """Purge les 3 natifs et cree les 6 entrees Option B sur chaque site."""
    Website = env["website"]
    Menu = env["website.menu"]
    Page = env["website.page"]

    websites = Website.search([])
    if not websites:
        _logger.warning(
            "[C-Kreyol] sync_ckr_menus : aucun site web trouve, "
            "abandon."
        )
        return

    for website in websites:
        root = website.menu_id
        if not root:
            _logger.warning(
                "[C-Kreyol] site %s sans menu racine, ignore.",
                website.display_name,
            )
            continue

        # 1. Purge des entrees natives sous le menu racine.
        native = Menu.search([
            ("parent_id", "=", root.id),
            ("url", "in", list(NATIVE_MENU_URLS_TO_REMOVE)),
            ("website_id", "=", website.id),
        ])
        if native:
            _logger.info(
                "[C-Kreyol] site %s : suppression de %d entrees natives.",
                website.display_name, len(native),
            )
            native.unlink()

        # 2. Creation / mise a jour des 6 entrees Option B.
        for name, url, sequence in CKR_MENU_ITEMS:
            existing = Menu.search([
                ("parent_id", "=", root.id),
                ("name", "=", name),
                ("website_id", "=", website.id),
            ], limit=1)
            if existing:
                existing.write({"url": url, "sequence": sequence})
            else:
                Menu.create({
                    "name": name,
                    "url": url,
                    "parent_id": root.id,
                    "website_id": website.id,
                    "sequence": sequence,
                })

    # 3. Nettoyage : si un website.page "/" stale (non standard) est
    #    present (versions precedentes du module), on le retire pour
    #    laisser website.homepage_page piloter la homepage.
    stale = Page.search([("url", "=", "/")])
    homepage_page = env.ref("website.homepage_page", raise_if_not_found=False)
    if homepage_page and stale:
        stale = stale - homepage_page
    if stale:
        _logger.info(
            "[C-Kreyol] suppression de %d website.page stale sur '/'.",
            len(stale),
        )
        stale.unlink()

    _logger.info("[C-Kreyol] sync_ckr_menus : OK.")


def post_init_hook(env):
    """Declenche a l install initial du module."""
    _sync_ckr_menus(env)
