# -*- coding: utf-8 -*-
"""
Ré-applique les libellés FR accentués sur les rôles livrés (xml_id),
pour toutes les langues actives — corrige aussi les anciennes versions sans migration
ou les fautes de frappe (ex. Trescrier → Trésorier).

La précédente migration 19.0.1.0.2 ne se relançait pas si la base était déjà en 19.0.1.0.2.
"""

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

# Libellés canoniques livrés avec le module (xml_id → nom affiché)
_PRESET_NAMES = (
    ("dorevia_membership_roles.membership_role_benevole", "Bénévole"),
    ("dorevia_membership_roles.membership_role_ca", "Membre du CA"),
    ("dorevia_membership_roles.membership_role_president", "Président"),
    ("dorevia_membership_roles.membership_role_tresorier", "Trésorier"),
    ("dorevia_membership_roles.membership_role_secretaire", "Secrétaire"),
    ("dorevia_membership_roles.membership_role_salarie", "Salarié"),
    ("dorevia_membership_roles.membership_role_intervenant", "Intervenant"),
)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    Lang = env["res.lang"].search([("active", "=", True)])
    codes = list(dict.fromkeys((Lang.mapped("code") or []) + ["fr_FR", "en_US"]))

    for xmlid, canonical in _PRESET_NAMES:
        rec = env.ref(xmlid, raise_if_not_found=False)
        if not rec:
            continue
        for code in codes:
            rec.with_context(lang=code).write({"name": canonical})
        _logger.info(
            "dorevia_membership_roles 19.0.1.0.3 : libellé synchronisé pour %s → %r",
            xmlid,
            canonical,
        )
