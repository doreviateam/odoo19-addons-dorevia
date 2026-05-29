# -*- coding: utf-8 -*-

"""Hooks install / migration — nomenclature analytique GLC plan unique."""

GLC_ANALYTIC_ACCOUNT_NORMALIZATION = {
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
    "analytic_account_glc_adhesions": {
        "name": "Adhésions",
        "code": "ADHESIONS",
        "glc_activity_type": "financement",
        "glc_display_sequence": 80,
        "glc_report_active": True,
    },
    "analytic_account_glc_dons": {
        "name": "Dons",
        "code": "DONS",
        "glc_activity_type": "financement",
        "glc_display_sequence": 90,
        "glc_report_active": True,
    },
    "analytic_account_glc_subventions": {
        "name": "Subventions",
        "code": "SUBVENTIONS",
        "glc_activity_type": "financement",
        "glc_display_sequence": 100,
        "glc_report_active": True,
    },
    "analytic_account_glc_ressources_propres": {
        "name": "Ressources propres",
        "code": "RESSOURCES_PROPRES",
        "glc_activity_type": "financement",
        "glc_display_sequence": 110,
        "glc_report_active": True,
    },
}


def _xml_ref_id(cr, xml_name, model):
    cr.execute(
        """
        SELECT res_id
          FROM ir_model_data
         WHERE module = 'dorevia_glc_analytics'
           AND name = %s
           AND model = %s
        """,
        (xml_name, model),
    )
    row = cr.fetchone()
    return row[0] if row else None


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


def _archive_glc_financements_plan(cr):
    """Archive l'ancien plan Financements après consolidation plan unique."""
    financements_plan_id = _xml_ref_id(cr, "analytic_plan_glc_financements", "account.analytic.plan")
    if not financements_plan_id:
        return
    cr.execute(
        """
        UPDATE account_analytic_plan
           SET name = jsonb_build_object(
                   'en_US', 'GLC - Financements (archivé)',
                   'fr_FR', 'GLC - Financements (archivé)'
               ),
               description = jsonb_build_object(
                   'en_US', 'Plan historique — comptes migrés vers GLC - Activités.',
                   'fr_FR', 'Plan historique — comptes migrés vers GLC - Activités.'
               )
         WHERE id = %s
        """,
        (financements_plan_id,),
    )


def _migrate_to_single_glc_plan(cr):
    """Consolide tous les comptes GLC sur le plan unique GLC - Activités."""
    activites_plan_id = _xml_ref_id(cr, "analytic_plan_glc_activites", "account.analytic.plan")
    financements_plan_id = _xml_ref_id(cr, "analytic_plan_glc_financements", "account.analytic.plan")
    if not activites_plan_id:
        return

    if financements_plan_id and financements_plan_id != activites_plan_id:
        cr.execute(
            """
            UPDATE account_analytic_account
               SET plan_id = %s
             WHERE plan_id = %s
            """,
            (activites_plan_id, financements_plan_id),
        )
        _archive_glc_financements_plan(cr)


def _normalize_glc_analytic_accounts(cr):
    """Aligne les 11 comptes GLC officiels sur le plan unique malgré le noupdate XML."""
    activites_plan_id = _xml_ref_id(cr, "analytic_plan_glc_activites", "account.analytic.plan")
    if not activites_plan_id:
        return
    for xml_id, values in GLC_ANALYTIC_ACCOUNT_NORMALIZATION.items():
        cr.execute(
            """
            UPDATE account_analytic_account AS account
               SET name = jsonb_build_object('en_US', %(name)s::text, 'fr_FR', %(name)s::text),
                   code = %(code)s,
                   plan_id = %(plan_id)s,
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
            {**values, "xml_id": xml_id, "plan_id": activites_plan_id},
        )


def _normalize_glc_activites_plan(cr):
    plan_id = _xml_ref_id(cr, "analytic_plan_glc_activites", "account.analytic.plan")
    if not plan_id:
        return
    cr.execute(
        """
        UPDATE account_analytic_plan
           SET name = jsonb_build_object(
                   'en_US', 'GLC - Activités',
                   'fr_FR', 'GLC - Activités'
               ),
               description = jsonb_build_object(
                   'en_US', 'Pilotage GLC — activités, ressources et structure.',
                   'fr_FR', 'Pilotage GLC — activités, ressources et structure.'
               )
         WHERE id = %s
        """,
        (plan_id,),
    )


def migrate_glc_analytic_nomenclature(cr):
    """Plan unique GLC — consolidation + alignement nomenclature officielle."""
    _migrate_to_single_glc_plan(cr)
    _normalize_glc_activites_plan(cr)
    _normalize_glc_analytic_accounts(cr)


def pre_init_hook(env):
    """Migration lors de la première installation sous le nouveau nom technique."""
    _rename_module_records(env.cr)


def migrate(cr, version):
    """Migration lors d'une mise à jour (-u) sur une base déjà renommée."""
    _rename_module_records(cr)
