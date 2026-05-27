# -*- coding: utf-8 -*-


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


def pre_init_hook(env):
    """Migration lors de la première installation sous le nouveau nom technique."""
    _rename_module_records(env.cr)


def migrate(cr, version):
    """Migration lors d'une mise à jour (-u) sur une base déjà renommée."""
    _rename_module_records(cr)
