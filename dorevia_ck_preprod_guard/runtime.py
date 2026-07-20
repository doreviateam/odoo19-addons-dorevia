# -*- coding: utf-8 -*-
"""Gardes runtime — effet module actif uniquement en préprod CK (N-3)."""
from __future__ import annotations

from .guards import EXPECTED_DATABASE, EXPECTED_DOMAIN


def is_ck_preprod_runtime_active(env, request=None) -> bool:
    """AND runtime : base + domaine préprod CK.

    Ne lit ni n'expose de secret. Utilisable depuis QWeb et tests.
  """
    dbname = getattr(getattr(env, "cr", None), "dbname", None) or ""
    if dbname != EXPECTED_DATABASE:
        return False

    host = _resolve_host(env, request)
    if not host or EXPECTED_DOMAIN not in host:
        return False
    return True


def _resolve_host(env, request) -> str | None:
    if request is not None:
        httprequest = getattr(request, "httprequest", None)
        if httprequest is not None:
            host = getattr(httprequest, "host", None) or ""
            if host:
                return host
    try:
        website = env.ref("website.default_website", raise_if_not_found=False)
        if website:
            domain = (website.domain or "").strip()
            if domain:
                return domain
    except Exception:
        pass
    try:
        base = env["ir.config_parameter"].sudo().get_param("web.base.url") or ""
        return base.replace("https://", "").replace("http://", "").split("/")[0]
    except Exception:
        return None
