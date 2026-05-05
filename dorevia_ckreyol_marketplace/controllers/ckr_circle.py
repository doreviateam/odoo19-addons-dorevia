# -*- coding: utf-8 -*-
import logging
import urllib.parse

from odoo import http
from odoo.exceptions import MissingError
from odoo.http import request

_logger = logging.getLogger(__name__)

CKR_MAILING_LIST_XMLID = "dorevia_ckreyol_marketplace.ckr_mailing_list_newsletter_ck"
CKR_MAILING_LIST_NAME = "Newsletter C-Kreyol"


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


def _ckr_mailing_list_newsletter(env):
    """Retourne ``mailing.list`` « Newsletter C-Kreyol » (recordset 0 ou 1)."""
    MList = env["mailing.list"].sudo()
    try:
        ref_rec = env.ref(CKR_MAILING_LIST_XMLID)
        rec = MList.browse(ref_rec.id)
        if rec.exists():
            return rec
    except MissingError:
        pass
    return MList.search([("name", "=", CKR_MAILING_LIST_NAME)], limit=1)


def _ckr_subscribe_mailing_list(env, email, list_rec):
    """Inscrit l’e-mail sur la liste. Retourne ``ok`` | ``dup`` | ``err``."""
    if not list_rec:
        return "err"
    MContact = env["mailing.contact"].sudo()
    MSub = env["mailing.subscription"].sudo()
    lid = list_rec.id
    try:
        contact = MContact.search([("email", "=", email)], limit=1, order="id asc")
        if not contact:
            MContact.create({"email": email, "list_ids": [(4, lid)]})
            return "ok"

        sub = MSub.search(
            [("contact_id", "=", contact.id), ("list_id", "=", lid)],
            limit=1,
        )
        if sub:
            if not sub.opt_out:
                return "dup"
            sub.write(
                {
                    "opt_out": False,
                    "opt_out_reason_id": False,
                }
            )
            return "ok"

        contact.write({"list_ids": [(4, lid)]})
        return "ok"
    except Exception:  # pylint: disable=broad-except
        _logger.exception(
            "C-Kreyol: échec inscription newsletter (email=%s list_id=%s)",
            email,
            lid,
        )
        return "err"


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

        norm_fn = request.env["ckr.circle.subscriber"].sudo().normalize_incoming_email
        email = norm_fn(post.get("email", ""))
        if not email:
            return request.redirect(
                f"{back}?{urllib.parse.urlencode({'cc_nl': 'invalid'})}",
                code=303,
            )

        ml = _ckr_mailing_list_newsletter(request.env)
        outcome = _ckr_subscribe_mailing_list(request.env, email, ml)

        if outcome == "dup":
            return request.redirect(
                f"{back}?{urllib.parse.urlencode({'cc_nl': 'dup'})}",
                code=303,
            )
        if outcome == "err":
            return request.redirect(
                f"{back}?{urllib.parse.urlencode({'cc_nl': 'err'})}",
                code=303,
            )
        return request.redirect(
            f"{back}?{urllib.parse.urlencode({'cc_nl': 'ok'})}",
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
