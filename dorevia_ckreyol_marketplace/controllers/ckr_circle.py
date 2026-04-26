# -*- coding: utf-8 -*-
import logging
import urllib.parse

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


def _ckr_safe_redirect_path(raw):
    """Refuse open redirects : chemin relatif commençant par / (pas //)."""
    if not raw or not isinstance(raw, str):
        return "/"
    p = raw.strip()
    if not p.startswith("/") or p.startswith("//"):
        return "/"
    if len(p) > 2048:
        return "/"
    return p


class CkrCircleController(http.Controller):
    @http.route(
        ["/ckr/circle/subscribe"],
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
        csrf=True,
    )
    def ckr_circle_subscribe(self, **post):
        website = request.website
        if not website:
            return request.redirect("/", code=303)

        back = _ckr_safe_redirect_path(post.get("redirect") or post.get("r") or "/")
        err_qs = {"cc_cir": "0"}

        raw_email = post.get("email", "")
        sub = request.env["ckr.circle.subscriber"].sudo()
        email = sub.normalize_incoming_email(raw_email)
        if not email:
            return request.redirect(
                f"{back}?{urllib.parse.urlencode(err_qs)}",
                code=303,
            )

        opt_offers = post.get("opt_offers") == "1"
        opt_recipes = post.get("opt_recipes") == "1"
        opt_news = post.get("opt_news") == "1"

        try:
            existing = sub.search(
                [
                    ("website_id", "=", website.id),
                    ("email", "=", email),
                ],
                limit=1,
            )
            if existing:
                existing.write(
                    {
                        "opt_offers": opt_offers,
                        "opt_recipes": opt_recipes,
                        "opt_news": opt_news,
                        "active": True,
                    }
                )
            else:
                sub.create(
                    {
                        "email": email,
                        "website_id": website.id,
                        "opt_offers": opt_offers,
                        "opt_recipes": opt_recipes,
                        "opt_news": opt_news,
                    }
                )
        except Exception:  # pylint: disable=broad-except
            _logger.exception("C-Kreyol: échec inscription cercle (email=%s)", email)
            return request.redirect(
                f"{back}?{urllib.parse.urlencode(err_qs)}",
                code=303,
            )

        ok_qs = {"cc_cir": "1"}
        return request.redirect(
            f"{back}?{urllib.parse.urlencode(ok_qs)}",
            code=303,
        )

    @http.route(
        ["/ckr/circle/unsubscribe/<string:token>"],
        type="http",
        auth="public",
        methods=["GET"],
        website=True,
        sitemap=False,
        csrf=False,
    )
    def ckr_circle_unsubscribe(self, token, **kw):
        if not token:
            return request.not_found()

        rec = (
            request.env["ckr.circle.subscriber"]
            .sudo()
            .search([("unsubscribe_token", "=", token)], limit=1)
        )
        if not rec:
            return request.render(
                "dorevia_ckreyol_marketplace.ckr_page_circle_unsubscribed",
                {
                    "ckr_unsub_state": "unknown",
                },
            )

        rec.write({"active": False})
        return request.render(
            "dorevia_ckreyol_marketplace.ckr_page_circle_unsubscribed",
            {
                "ckr_unsub_state": "ok",
            },
        )
