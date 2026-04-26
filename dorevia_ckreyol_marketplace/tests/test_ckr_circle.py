# -*- coding: utf-8 -*-
"""Tests — chantier Cercle / inscription (MVP2.1 4/5)."""
import re
import time

import psycopg2

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase


@tagged("post_install", "-at_install", "dorevia_ckr_circle")
class TestCkrCircleHomepage(HttpCase):
    """Présence du bloc, page légal, POST fonctionnel (CSRF)."""

    def _extract_csrf(self, html):
        m = re.search(
            r'<input type="hidden" name="csrf_token" value="([^"]*)"',
            html,
        )
        return m.group(1) if m else None

    def test_rc_homepage_renders_circle_block(self):
        r = self.url_open("/", timeout=60)
        self.assertEqual(r.status_code, 200)
        self.assertIn("ckr-circle", r.text)
        self.assertIn("Rejoignez le cercle C-Kreyol", r.text)
        self.assertIn('action="/ckr/circle/subscribe"', r.text)
        self.assertIn("/privacy", r.text)

    def test_rc_privacy_page_200(self):
        r = self.url_open("/privacy", timeout=60)
        self.assertEqual(r.status_code, 200)
        self.assertIn("Politique de confidentialité", r.text)
        self.assertIn("Responsable du traitement", r.text)
        self.assertNotIn("base minimale", r.text.lower())

    def test_rc_terms_page_200(self):
        r = self.url_open("/terms", timeout=60)
        self.assertEqual(r.status_code, 200)
        self.assertIn("Mentions légales", r.text)
        self.assertIn('id="cgv"', r.text)
        self.assertIn("/privacy", r.text)
        self.assertIn("OVH SAS", r.text)
        self.assertIn("Roubaix", r.text)
        self.assertIn("+33", r.text)

    def test_rc_subscribe_post_creates_subscriber(self):
        email = "cercle.httpcase.%s@example.com" % int(time.time() * 1000)
        r0 = self.url_open("/", timeout=60)
        self.assertEqual(r0.status_code, 200)
        token = self._extract_csrf(r0.text)
        self.assertTrue(
            token,
            "Jeton CSRF requis (formulaire cercle en homepage).",
        )
        res = self.url_open(
            "/ckr/circle/subscribe",
            data={
                "csrf_token": token,
                "email": email,
                "redirect": "/",
            },
            timeout=60,
        )
        self.assertIn(
            res.status_code,
            (301, 302, 303),
            "Redirection attendue apres POST inscription.",
        )
        loc = res.headers.get("Location", "")
        self.assertIn("cc_cir=1", loc, "Parametre de succes attendu (query string).")
        self.env.cr.commit()
        sub = self.env["ckr.circle.subscriber"].sudo().search(
            [("email", "=", email)], limit=1
        )
        self.assertTrue(sub, "Enregistrement ckr.circle.subscriber attendu.")
        self.assertTrue(sub.unsubscribe_token)
        self.assertTrue(sub.active)


@tagged("post_install", "-at_install", "dorevia_ckr_circle")
class TestCkrCircleModel(TransactionCase):
    """Règles de persistance côté modèle (sans HTTP)."""

    def test_model_create_normalizes_and_token(self):
        website = self.env.ref("website.default_website")
        sub = self.env["ckr.circle.subscriber"].create(
            {
                "email": "  Upcase@Example.COM ",
                "website_id": website.id,
            }
        )
        self.assertEqual(sub.email, "upcase@example.com")
        self.assertTrue(len(sub.unsubscribe_token) > 8)

    def test_model_unique_per_website(self):
        website = self.env.ref("website.default_website")
        self.env["ckr.circle.subscriber"].search(
            [("email", "=", "dup@example.com"), ("website_id", "=", website.id)]
        ).unlink()
        self.env["ckr.circle.subscriber"].create(
            {
                "email": "dup@example.com",
                "website_id": website.id,
            }
        )
        self.env["ckr.circle.subscriber"].flush_model()
        with self.assertRaises(psycopg2.Error):
            self.env["ckr.circle.subscriber"].create(
                {
                    "email": "dup@example.com",
                    "website_id": website.id,
                }
            )
