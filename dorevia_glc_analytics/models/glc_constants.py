# -*- coding: utf-8 -*-

"""Constantes partagées — contrôles analytiques GLC Palier 1."""

GLC_LEGACY_ANALYTIC_CODES = (
    "ADHESION_GLC",
    "BAR_RESTAU",
    "DEPLACEMENT_MISSION",
    "ESPACE_GLC",
    "FRAIS_STRUCTURE",
    "PRESTA_GLC",
    "RESIDENCE_GLC",
    "RH_PERSONNEL",
    "SUBVENTION_GLC",
)

GLC_PAYROLL_ACCOUNT_PREFIXES = ("631", "633", "641", "645")

GLC_EXPENSE_ACCOUNT_TYPES = (
    "expense",
    "expense_direct_cost",
    "expense_depreciation",
)

GLC_INCOME_ACCOUNT_TYPES = (
    "income",
    "income_other",
)

# Axes financement / ressources — plan unique GLC - Activités, Type GLC = Recette
GLC_FUNDING_ANALYTIC_CODES = (
    "ADHESIONS",
    "DONS",
    "FIN_EXT",
    "FIN_INT",
)

GLC_FUNDING_CODES = GLC_FUNDING_ANALYTIC_CODES

GLC_FUNDING_MESSAGES = {
    "ADHESIONS": "Adhésion sans axe financement ADHESIONS",
    "DONS": "Don sans axe financement DONS",
    "FIN_EXT": "Recette sans axe financement externe FIN_EXT",
    "FIN_INT": "Recette sans axe financement interne FIN_INT",
}

GLC_PERCENT_TOLERANCE = 0.01

# Comptes opérationnels (hors axes financement) — recettes d'activité cockpit
GLC_COCKPIT_ACTIVITY_REVENUE_CODES = (
    "BAR_REST",
    "PRESTA",
    "LOC_PRIV",
    "LOC_RGL",
)

GLC_COCKPIT_FUNDING_CODES = GLC_FUNDING_ANALYTIC_CODES

GLC_COCKPIT_GENERAL_EXPENSE_CODE = "STRUCTURE"

GLC_COCKPIT_PAYROLL_BUDGET_CODES = (
    "BAR_REST",
    "PRESTA",
    "LOC_PRIV",
    "RESIDENCES",
    "DEPL_MIS",
    "LOC_RGL",
    "STRUCTURE",
)

GLC_OFFICIAL_ANALYTIC_CODES = (
    "STRUCTURE",
    "BAR_REST",
    "PRESTA",
    "RESIDENCES",
    "DEPL_MIS",
    "LOC_PRIV",
    "LOC_RGL",
    "ADHESIONS",
    "DONS",
    "FIN_EXT",
    "FIN_INT",
)

# Renommages historiques → cible MOA plan unique
GLC_ANALYTIC_CODE_MIGRATION = {
    "STR_ADM": "STRUCTURE",
    "STRUCTURE": "STRUCTURE",
    "BAR": "BAR_REST",
    "BAR_REST": "BAR_REST",
    "PRESTATIONS": "PRESTA",
    "PRESTA": "PRESTA",
    "MISSIONS": "DEPL_MIS",
    "DEPL_MIS": "DEPL_MIS",
    "PRIVATISATIONS": "LOC_PRIV",
    "LOC_PRIV": "LOC_PRIV",
    "LOCATION_RADIO": "LOC_RGL",
    "LOC_RGL": "LOC_RGL",
    "RESIDENCES": "RESIDENCES",
    "RES_EXT": "RESIDENCES",
    "ADHESIONS": "ADHESIONS",
    "DONS": "DONS",
    "SUBVENTIONS": "FIN_EXT",
    "FIN_EXT": "FIN_EXT",
    "RESSOURCES_PROPRES": "FIN_INT",
    "FIN_INT": "FIN_INT",
}

GLC_EXCLUDED_GL_ACCOUNT_PREFIXES = ("164",)
GLC_COCKPIT_SALARY_EXCLUDED_ANALYTIC_CODES = ("RH_PERSONNEL",)
