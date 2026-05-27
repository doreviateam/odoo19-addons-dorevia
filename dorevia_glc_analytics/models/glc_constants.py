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

GLC_FUNDING_CODES = (
    "ADHESIONS",
    "DONS",
    "SUBVENTIONS",
)

GLC_FUNDING_MESSAGES = {
    "ADHESIONS": "Adhésion sans financement ADHESIONS",
    "DONS": "Don sans financement DONS",
    "SUBVENTIONS": "Subvention sans financement SUBVENTIONS",
}

GLC_PERCENT_TOLERANCE = 0.01

# Palier 4 — cockpit couverture des salaires
GLC_COCKPIT_ACTIVITY_REVENUE_CODES = (
    "BAR",
    "PRESTATIONS",
    "PRIVATISATIONS",
)
GLC_COCKPIT_FUNDING_CODES = (
    "SUBVENTIONS",
    "ADHESIONS",
)
GLC_COCKPIT_GENERAL_EXPENSE_CODE = "STRUCTURE"
GLC_COCKPIT_PAYROLL_BUDGET_CODES = (
    "BAR",
    "PRESTATIONS",
    "PRIVATISATIONS",
    "RESIDENCES",
    "MISSIONS",
    "LOCATION_RADIO",
    "STRUCTURE",
)
GLC_EXCLUDED_GL_ACCOUNT_PREFIXES = ("164",)
GLC_COCKPIT_SALARY_EXCLUDED_ANALYTIC_CODES = ("RH_PERSONNEL",)
