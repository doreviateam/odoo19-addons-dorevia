# -*- coding: utf-8 -*-
"""Mapping ruban e-commerce BO → classes badge card CK (Home + Shop)."""


def ck_product_ribbon_badge_class(ribbon):
    """Classes maquette CK pour les libellés ruban courants."""
    name = (ribbon.name or '').lower()
    if 'nouveau' in name or 'new' in name:
        return 'badge-new'
    if any(token in name for token in ('coup', 'cœur', 'coeur', 'vente', 'sale', 'promo')):
        return 'badge-heart'
    return 'badge-ribbon'
