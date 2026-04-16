# -*- coding: utf-8 -*-
"""Utilitaires pour les tests (bases déjà peuplées, ex. tenant sandbox)."""

import uuid


def helloasso_account_get_or_create(env, company, name="Compte test"):
    """Un compte HelloAsso par société : réutilise l’existant si présent."""
    Account = env["dorevia.helloasso.account"]
    acc = Account.search([("company_id", "=", company.id)], limit=1)
    if acc:
        return acc
    return Account.create(
        {
            "name": name,
            "company_id": company.id,
            "environment": "sandbox",
        }
    )


def helloasso_isolated_company_and_account(env):
    """Société + compte HelloAsso sans paiements (assertions sur search_count)."""
    suffix = uuid.uuid4().hex[:10]
    company = env["res.company"].sudo().create({"name": "HA test %s" % suffix})
    account = env["dorevia.helloasso.account"].create(
        {
            "name": "Compte isolé %s" % suffix,
            "company_id": company.id,
            "environment": "sandbox",
        }
    )
    return company, account
