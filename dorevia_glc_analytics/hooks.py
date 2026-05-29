# -*- coding: utf-8 -*-

GLC_ACTIVITY_ACCOUNT_NORMALIZATION = {
    "analytic_account_glc_structure": {
        "name": "Structure & Administration",
        "code": "STRUCTURE",
        "glc_activity_type": "charge",
        "glc_display_sequence": 10,
        "glc_report_active": True,
    },
    "analytic_account_glc_bar": {
        "name": "Bar, Restauration & Cuisine",
        "code": "BAR",
        "glc_activity_type": "mixte",
        "glc_display_sequence": 20,
        "glc_report_active": True,
    },
    "analytic_account_glc_prestations": {
        "name": "Prestations & Animations",
        "code": "PRESTATIONS",
        "glc_activity_type": "mixte",
        "glc_display_sequence": 30,
        "glc_report_active": True,
    },
    "analytic_account_glc_residences": {
        "name": "Résidences artistiques",
        "code": "RESIDENCES",
        "glc_activity_type": "charge_subventionnee",
        "glc_display_sequence": 40,
        "glc_report_active": True,
    },
    "analytic_account_glc_missions": {
        "name": "Déplacements & Missions",
        "code": "MISSIONS",
        "glc_activity_type": "charge",
        "glc_display_sequence": 50,
        "glc_report_active": True,
    },
    "analytic_account_glc_privatisations": {
        "name": "Privatisation d'espace",
        "code": "PRIVATISATIONS",
        "glc_activity_type": "mixte",
        "glc_display_sequence": 60,
        "glc_report_active": True,
    },
    "analytic_account_glc_location_radio": {
        "name": "Location Radio Grand Lieu",
        "code": "LOCATION_RADIO",
        "glc_activity_type": "recette",
        "glc_display_sequence": 70,
        "glc_report_active": True,
    },
}


def _rename_module_records(cr):
    """Renomme dorevia_glc_analytique → dorevia_glc_analytics (SQL idempotent)."""
    cr.execute(
        """
        SELECT name, id, state
        FROM ir_module_module
        WHERE name IN ('dorevia_glc_analytique', 'dorevia_glc_analytics')
        """
    )
    rows = {name: {"id": row_id, "state": state} for name, row_id, state in cr.fetchall()}

    old = rows.get("dorevia_glc_analytique")
    new = rows.get("dorevia_glc_analytics")

    if old and new and old["id"] != new["id"]:
        # Doublon après une installation partielle : libérer le nom cible sans DELETE.
        cr.execute(
            """
            UPDATE ir_module_module
            SET name = 'dorevia_glc_analytics_orphan_' || id
            WHERE id = %s
            """,
            [new["id"]],
        )

    cr.execute("SELECT 1 FROM ir_module_module WHERE name = 'dorevia_glc_analytique'")
    if cr.fetchone():
        cr.execute(
            """
            UPDATE ir_module_module
            SET name = 'dorevia_glc_analytics'
            WHERE name = 'dorevia_glc_analytique'
            """
        )

    cr.execute(
        """
        UPDATE ir_module_module_dependency
        SET name = 'dorevia_glc_analytics'
        WHERE name = 'dorevia_glc_analytique'
        """
    )
    cr.execute(
        """
        UPDATE ir_model_data
        SET module = 'dorevia_glc_analytics'
        WHERE module = 'dorevia_glc_analytique'
        """
    )
    cr.execute(
        """
        UPDATE ir_config_parameter
        SET key = REPLACE(key, 'dorevia_glc_analytique.', 'dorevia_glc_analytics.')
        WHERE key LIKE 'dorevia_glc_analytique.%'
        """
    )


def _normalize_glc_activity_accounts(cr):
    """Aligne les comptes Activités GLC officiels malgré le noupdate XML."""
    for xml_id, values in GLC_ACTIVITY_ACCOUNT_NORMALIZATION.items():
        cr.execute(
            """
            UPDATE account_analytic_account AS account
               SET name = jsonb_build_object('en_US', %(name)s::text, 'fr_FR', %(name)s::text),
                   code = %(code)s,
                   glc_activity_type = %(glc_activity_type)s,
                   glc_display_sequence = %(glc_display_sequence)s,
                   glc_report_active = %(glc_report_active)s,
                   active = TRUE
              FROM ir_model_data AS data
             WHERE data.module = 'dorevia_glc_analytics'
               AND data.name = %(xml_id)s
               AND data.model = 'account.analytic.account'
               AND data.res_id = account.id
            """,
            {**values, "xml_id": xml_id},
        )


def pre_init_hook(env):
    """Migration lors de la première installation sous le nouveau nom technique."""
    _rename_module_records(env.cr)


def migrate(cr, version):
    """Migration lors d'une mise à jour (-u) sur une base déjà renommée."""
    _rename_module_records(cr)
