# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    dorevia_vault_connector_enabled = fields.Boolean(
        string="Connecteur Vault actif",
        config_parameter="dorevia_vault_connector.enabled",
    )
    dorevia_vault_connector_target_url = fields.Char(
        string="URL cible (HTTP POST)",
        config_parameter="dorevia_vault_connector.target_url",
    )
    dorevia_vault_connector_token = fields.Char(
        string="Jeton / clé (optionnel)",
        config_parameter="dorevia_vault_connector.token",
    )
    dorevia_vault_connector_timeout_seconds = fields.Integer(
        string="Timeout HTTP (secondes)",
        default=10,
        config_parameter="dorevia_vault_connector.timeout_seconds",
    )
    dorevia_vault_connector_tenant = fields.Char(
        string="Tenant par défaut",
        config_parameter="dorevia_vault_connector.tenant",
    )
