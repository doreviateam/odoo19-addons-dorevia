# -*- coding: utf-8 -*-

from .models.marketone_origin_reunion_dedup import marketone_dedup_reunion_origin_values


def post_init_hook(env):
    """Fusion La Réunion / Reunion après install ou upgrade (idempotent)."""
    marketone_dedup_reunion_origin_values(env)
