# -*- coding: utf-8 -*-
"""Met à jour les libellés de rôles prédéfinis (accents FR) pour les bases déjà installées."""

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

_RENAMES = (
    ("dorevia_membership_roles.membership_role_benevole", "Benevole", "Bénévole"),
    ("dorevia_membership_roles.membership_role_president", "President", "Président"),
    ("dorevia_membership_roles.membership_role_tresorier", "Tresorier", "Trésorier"),
    ("dorevia_membership_roles.membership_role_secretaire", "Secretaire", "Secrétaire"),
    ("dorevia_membership_roles.membership_role_salarie", "Salarie", "Salarié"),
)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for xmlid, old, new in _RENAMES:
        rec = env.ref(xmlid, raise_if_not_found=False)
        if rec and (rec.name or "").strip() == old:
            rec.name = new
            _logger.info(
                "dorevia_membership_roles 19.0.1.0.2 : rôle %s renommé « %s » → « %s »",
                xmlid,
                old,
                new,
            )
