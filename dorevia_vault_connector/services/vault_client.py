# -*- coding: utf-8 -*-
"""Client HTTP minimal (stdlib) — pas de dépendance `requests` en V1."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Dict

from odoo.api import Environment


def send_to_vault(env: Environment, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Envoie le payload en POST JSON vers l'URL configurée.

    Retour attendu : ``success`` (bool), ``message`` (str), ``remote_ref`` (str|None).
    """
    icp = env["ir.config_parameter"].sudo()
    url = (icp.get_param("dorevia_vault_connector.target_url") or "").strip()
    token = (icp.get_param("dorevia_vault_connector.token") or "").strip()
    timeout_raw = icp.get_param("dorevia_vault_connector.timeout_seconds") or "10"
    try:
        timeout = max(1, min(120, int(timeout_raw)))
    except (TypeError, ValueError):
        timeout = 10

    if not url:
        return {"success": False, "message": "URL cible non configurée.", "remote_ref": None}

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json",
        },
    )
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            remote_ref = None
            if body.strip():
                try:
                    parsed = json.loads(body)
                    if isinstance(parsed, dict):
                        remote_ref = parsed.get("id") or parsed.get("ref") or parsed.get("reference")
                        if remote_ref is not None:
                            remote_ref = str(remote_ref)
                except json.JSONDecodeError:
                    remote_ref = None
            return {
                "success": 200 <= resp.status < 300,
                "message": "OK" if resp.status < 300 else f"HTTP {resp.status}",
                "remote_ref": remote_ref,
            }
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")[:500]
        return {
            "success": False,
            "message": f"HTTP {e.code}: {err_body or e.reason}",
            "remote_ref": None,
        }
    except urllib.error.URLError as e:
        return {"success": False, "message": str(e.reason or e), "remote_ref": None}
    except Exception as e:  # noqa: BLE001 — connecteur borné, on remonte un message lisible
        return {"success": False, "message": str(e), "remote_ref": None}
