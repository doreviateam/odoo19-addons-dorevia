# -*- coding: utf-8 -*-
from unittest.mock import MagicMock

from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ckreyol_marketplace.models.crm_lead import CKR_MVP03_FORM_REFERRED


class TestCkrMvp03ProAccountLead(TransactionCase):
    """Marquage des leads « demande compte pro » (formulaire MVP03)."""

    def test_website_form_input_filter_mvp03_marker(self):
        Lead = self.env["crm.lead"]
        website = self.env["website"].search([], limit=1)
        request = MagicMock()
        request.env = self.env
        request.website = website
        values = {
            "referred": CKR_MVP03_FORM_REFERRED,
            "partner_name": "Ma Boutique SAS",
            "contact_name": "Alex",
            "email_from": "alex@example.org",
            "phone": "0690123456",
            "ckr_activity_type": "boutique_epicerie",
            "description": "Message test.",
        }
        out = Lead.website_form_input_filter(request, dict(values))
        self.assertIn("Ma Boutique SAS", out["name"])
        self.assertIn("Demande compte pro C-Kreyol MVP03", out["name"])
        self.assertTrue(out["description"].startswith("[Demande compte pro C-Kreyol MVP03]"))
        self.assertIn("Type d'activité :", out["description"])
        self.assertIn("épicerie", out["description"])

    def test_website_form_input_filter_unchanged_without_marker(self):
        Lead = self.env["crm.lead"]
        website = self.env["website"].search([], limit=1)
        request = MagicMock()
        request.env = self.env
        request.website = website
        values = {"name": "Autre sujet", "partner_name": "X"}
        out = Lead.website_form_input_filter(request, dict(values))
        self.assertEqual(out["name"], "Autre sujet")
