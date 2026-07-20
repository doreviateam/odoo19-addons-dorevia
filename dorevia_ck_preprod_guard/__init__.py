# -*- coding: utf-8 -*-
"""Module guard préprod CK — hooks + modèles (chargement conditionnel)."""
from __future__ import annotations

import os

from .guards import GuardError, assert_preprod_install_allowed

# Modèles Odoo uniquement si le runtime Odoo est présent (install / shell).
try:
    from odoo import models as _odoo_models  # noqa: F401

    from . import models  # noqa: F401
except ImportError:
    pass


def pre_init_hook(env):
    """Refuse l'installation / upgrade hors cible préprod CK (AND)."""
    db_name = getattr(getattr(env, "cr", None), "dbname", None) or os.environ.get(
        "CK_SOFT_LAUNCH_DATABASE", ""
    )
    try:
        assert_preprod_install_allowed(
            env_name=os.environ.get("CK_SOFT_LAUNCH_ENV"),
            domain=os.environ.get("CK_SOFT_LAUNCH_DOMAIN"),
            database=os.environ.get("CK_SOFT_LAUNCH_DATABASE") or db_name,
            runtime_database=db_name,
        )
    except GuardError as exc:
        raise RuntimeError(
            "dorevia_ck_preprod_guard: installation refusée — hors préprod CK. "
            f"{exc}"
        ) from exc
