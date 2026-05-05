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
    2. Creation / mise a jour du menu Option B :
       Boutique, Collections, Communaute (#, enfants : Idées cadeaux, Recettes,
       Blog), A propos, Contact.
    3. Nettoyage d eventuels website.page stale pointant sur "/" qui
       auraient ete crees par des versions anterieures du module
       (desormais la homepage reste portee par website.homepage_page
       standard, via heritage du template website.homepage).

Idempotent : on peut rejouer la sequence a l install comme au
upgrade (voir migrations/19.0.1.0.1/post-migration.py).

Reference : docs/direction/STRUCTURE_MENU_PRINCIPAL.md, ADR-CKR-003.
"""

import logging

from odoo.api import Environment, SUPERUSER_ID

_logger = logging.getLogger(__name__)

# Clé ``ir.config_parameter`` — alignée sur
# ``controllers/website_sale_ckr.CKR_FEATURED_COLLECTION_PARAM`` (SPEC §4.6).
CKR_FEATURED_COLLECTION_PARAM = (
    "dorevia_ckreyol_marketplace.featured_collection_id"
)

# Entrées racine (hors groupe Communauté).
# (nom, url, sequence) — doctrine : navigation catalogue via conteneur /shop.
CKR_MENU_ITEMS = [
    ("Boutique",    "/shop",        10),
    ("Collections", "/shop?ckr_collection_scope=all", 20),
    ("A propos",    "/a-propos",    50),
    ("Contact",     "/contact",     60),
]

# Parent « Communauté » + sous-menus (navbar regroupée).
CKR_COMMUNITY_PARENT = ("Communauté", "#", 30)
CKR_COMMUNITY_CHILDREN = [
    ("Idées cadeaux", "/offrir",    10),
    ("Recettes",    "/recettes",    20),
    ("Blog",        "/blog",        30),
]
CKR_COMMUNITY_URLS = frozenset(url for _name, url, _seq in CKR_COMMUNITY_CHILDREN)

# URLs des entrees natives a retirer du menu racine du site.
NATIVE_MENU_URLS_TO_REMOVE = ("/", "/shop", "/contactus")


def _sync_community_menu_for_website(website, root, Menu):
    """Crée le menu « Communauté » et rattache Idées cadeaux / Recettes / Blog."""
    name, url, sequence = CKR_COMMUNITY_PARENT
    community = Menu.search(
        [
            ("parent_id", "=", root.id),
            ("website_id", "=", website.id),
            ("name", "=", name),
        ],
        limit=1,
    )
    if community:
        community.write({"url": url, "sequence": sequence})
    else:
        community = Menu.create(
            {
                "name": name,
                "url": url,
                "parent_id": root.id,
                "website_id": website.id,
                "sequence": sequence,
            }
        )

    for child_name, child_url, child_seq in CKR_COMMUNITY_CHILDREN:
        candidates = Menu.search(
            [
                ("website_id", "=", website.id),
                ("url", "=", child_url),
            ]
        )
        at_root = candidates.filtered(lambda m: m.parent_id == root)
        target = at_root[:1] or candidates[:1]
        vals = {
            "name": child_name,
            "parent_id": community.id,
            "sequence": child_seq,
        }
        if target:
            target.write(vals)
        else:
            Menu.create(
                {
                    "name": child_name,
                    "url": child_url,
                    "parent_id": community.id,
                    "website_id": website.id,
                    "sequence": child_seq,
                }
            )

    # Racine : supprimer les doublons si l'entrée existe déjà sous Communauté ;
    # sinon rattache la première occurrence résiduelle.
    meta = {u: (n, s) for n, u, s in CKR_COMMUNITY_CHILDREN}
    for child_url in CKR_COMMUNITY_URLS:
        dup_roots = Menu.search(
            [
                ("parent_id", "=", root.id),
                ("website_id", "=", website.id),
                ("url", "=", child_url),
            ],
        )
        under_comm = Menu.search(
            [
                ("parent_id", "=", community.id),
                ("website_id", "=", website.id),
                ("url", "=", child_url),
            ],
            limit=1,
        )
        for stray in dup_roots:
            if under_comm:
                stray.unlink()
            else:
                cname, cseq = meta[child_url]
                stray.write(
                    {
                        "name": cname,
                        "parent_id": community.id,
                        "sequence": cseq,
                    }
                )
                under_comm = stray


def _sync_ckr_menus(env):
    """Purge les 3 natifs et synchronise le menu Option B sur chaque site."""
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

        # 2. Creation / mise a jour des entrees racine (hors Communauté).
        for name, url, sequence in CKR_MENU_ITEMS:
            existing = Menu.search([
                ("parent_id", "=", root.id),
                ("name", "=", name),
                ("website_id", "=", website.id),
            ], limit=1)
            # Compatibilite retroactive: renommer les entrees existantes
            # en se basant sur l'URL pour eviter un doublon "Offrir".
            if not existing:
                existing = Menu.search([
                    ("parent_id", "=", root.id),
                    ("url", "=", url),
                    ("website_id", "=", website.id),
                ], limit=1)
            if existing:
                existing.write({"name": name, "url": url, "sequence": sequence})
            else:
                Menu.create({
                    "name": name,
                    "url": url,
                    "parent_id": root.id,
                    "website_id": website.id,
                    "sequence": sequence,
                })

        # 3. Groupe Communauté (sous-menus : Idées cadeaux, Recettes, Blog).
        _sync_community_menu_for_website(website, root, Menu)

    # 4. Nettoyage : si un website.page "/" stale (non standard) est
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


def _ensure_featured_collection_parameter(env):
    """Garantit la présence du paramètre Incontournables sans écraser sa valeur.

    Volontairement **hors fichier data XML** : un upgrade module ne doit pas
    repasser l'id collection à ``0`` après configuration BO / exploitation.
    """
    ICP = env["ir.config_parameter"].sudo()
    if ICP.search([("key", "=", CKR_FEATURED_COLLECTION_PARAM)], limit=1):
        return
    ICP.set_param(CKR_FEATURED_COLLECTION_PARAM, "0")
    _logger.info(
        "[C-Kreyol] Paramètre %s créé (défaut 0).",
        CKR_FEATURED_COLLECTION_PARAM,
    )


def _whitelist_crm_lead_pro_form_fields(cr):
    """Autorise les champs CRM MVP03 / rappel sur les formulaires Website.

    ``formbuilder_whitelist`` exige le groupe Designer ; en hook superuser on
    applique la même mise à jour SQL que le core (voir ``website_form.py``).
    """
    cr.execute(
        """
        UPDATE ir_model_fields
        SET website_form_blacklisted = FALSE
        WHERE model = %s AND name IN %s
        """,
        (
            "crm.lead",
            (
                "referred",
                "ckr_activity_type",
                "ckr_callback_slot",
                "ckr_callback_date",
                "ckr_callback_window",
            ),
        ),
    )


def _whitelist_crm_lead_referred_for_website_form(cr):
    """Compat : ancien nom ; délègue à ``_whitelist_crm_lead_pro_form_fields``."""
    _whitelist_crm_lead_pro_form_fields(cr)


def post_init_hook(cr, registry):
    """Déclenché à l'installation initiale du module (signature Odoo standard)."""
    env = Environment(cr, SUPERUSER_ID, {})
    _whitelist_crm_lead_pro_form_fields(cr)
    _sync_ckr_menus(env)
    _ensure_featured_collection_parameter(env)
    env["website"].ckr_ensure_showcase_featured_on_empty_websites()
