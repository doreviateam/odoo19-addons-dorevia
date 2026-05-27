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
