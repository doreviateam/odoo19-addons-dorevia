# -*- coding: utf-8 -*-
"""Helpers tests — politique portes catalogue (header Promotions · Kits & Coffrets)."""

import re

_SITE_HEADER_RE = re.compile(
    r'<header\b[^>]*\bid=["\']top["\'][^>]*>.*?</header>',
    re.DOTALL | re.IGNORECASE,
)

_FORBIDDEN_HEADER_LEGACY = re.compile(
    r"""href=['"]/(?:incontournables|origines)(?:['"?]|$)"""
)

_FORBIDDEN_KITS_HEADER = re.compile(r"""href=['"]/kits(?:['"?]|$)""")

_FORBIDDEN_PROMO_HEADER = re.compile(r"""href=['"]/promotions(?:['"?]|$)""")


def html_without_site_header(html):
    return _SITE_HEADER_RE.sub("", html, count=1)


def extract_site_header(html):
    match = _SITE_HEADER_RE.search(html or "")
    return match.group(0) if match else ""


def assert_catalog_gate_policy(
    test_case,
    html,
    *,
    allow_header_promotions=False,
    allow_header_kits=False,
):
    """Portes interdites hors header ; ``/promotions`` et ``/kits`` autorisés header si MOA."""
    header = extract_site_header(html)
    if header:
        test_case.assertIsNone(
            _FORBIDDEN_HEADER_LEGACY.search(header),
            "Lien porte catalogue interdit dans le header site.",
        )
        if not allow_header_kits:
            test_case.assertIsNone(
                _FORBIDDEN_KITS_HEADER.search(header),
                "Lien /kits interdit dans le header (Lot 6.3b non actif).",
            )
        if not allow_header_promotions:
            test_case.assertIsNone(
                _FORBIDDEN_PROMO_HEADER.search(header),
                "Lien /promotions interdit dans le header (Lot 6.3a non actif).",
            )

    audit = html_without_site_header(html)
    forbidden_patterns = (
        r"marketone_mode=",
        r"ckr_mode=",
        r"""href=['"]/(?:promotions|kits|incontournables|origines)(?:['"?]|$)""",
    )
    for pattern in forbidden_patterns:
        test_case.assertIsNone(
            re.search(pattern, audit),
            f"Lien porte catalogue interdit hors header : {pattern}",
        )


def assert_catalog_gate_policy_lot6_front(test_case, html):
    """Politique header post Lots 6.3a + 6.3b — Promotions et Kits autorisés."""
    assert_catalog_gate_policy(
        test_case,
        html,
        allow_header_promotions=True,
        allow_header_kits=True,
    )
