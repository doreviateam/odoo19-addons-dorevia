# -*- coding: utf-8 -*-
"""Gardes d'environnement AND — module + applicateur (R3-3)."""
from __future__ import annotations

EXPECTED_ENV = "preprod"
EXPECTED_DOMAIN = "preprod-ck.doreviateam.com"
EXPECTED_DATABASE = "ck_marketone_preprod"


class GuardError(Exception):
    """Garde d'environnement refusée."""


def check_guards(
    *,
    env_name: str | None,
    domain: str | None,
    database: str | None,
    runtime_database: str | None = None,
) -> list[str]:
    """Retourne la liste des violations (vide = OK). Logique AND."""
    errors: list[str] = []
    if not env_name:
        errors.append(f"CK_SOFT_LAUNCH_ENV absent (attendu: {EXPECTED_ENV})")
    elif env_name != EXPECTED_ENV:
        errors.append(f"CK_SOFT_LAUNCH_ENV={env_name!r} ≠ {EXPECTED_ENV!r}")

    if not domain:
        errors.append(f"CK_SOFT_LAUNCH_DOMAIN absent (attendu: {EXPECTED_DOMAIN})")
    elif domain != EXPECTED_DOMAIN:
        errors.append(f"CK_SOFT_LAUNCH_DOMAIN={domain!r} ≠ {EXPECTED_DOMAIN!r}")

    declared_db = database or ""
    if not declared_db:
        errors.append(f"CK_SOFT_LAUNCH_DATABASE absent (attendu: {EXPECTED_DATABASE})")
    elif declared_db != EXPECTED_DATABASE:
        errors.append(f"CK_SOFT_LAUNCH_DATABASE={declared_db!r} ≠ {EXPECTED_DATABASE!r}")

    if runtime_database is not None and runtime_database != "" and runtime_database != EXPECTED_DATABASE:
        errors.append(
            f"runtime database={runtime_database!r} ≠ {EXPECTED_DATABASE!r}"
        )
    return errors


def assert_preprod_install_allowed(
    *,
    env_name: str | None,
    domain: str | None,
    database: str | None,
    runtime_database: str | None = None,
) -> None:
    errors = check_guards(
        env_name=env_name,
        domain=domain,
        database=database,
        runtime_database=runtime_database,
    )
    if errors:
        raise GuardError("; ".join(errors))
