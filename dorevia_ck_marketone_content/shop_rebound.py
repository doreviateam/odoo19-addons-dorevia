# -*- coding: utf-8 -*-
"""Bloc de rebond rayon pauvre (Note 07 Lot C).

Logique pure sans dépendance Odoo — testable en TransactionCase.
Condition D5/C3 :
    category défini
    AND products_count (search_count) in {1, 2}
    AND pas de recherche active
    AND pas de filtre actif (attrib, tags, prix)
"""

CK_REBOUND_MESSAGE = (
    "Cette sélection s'enrichit progressivement. "
    "Découvrez d'autres produits créoles sur toute la boutique."
)
CK_REBOUND_CTA_LABEL = 'Découvrir toute la boutique'
CK_REBOUND_CTA_URL = '/shop'


def ck_shop_has_active_filters(values, post):
    """Vrai si au moins un filtre actif (attributs, tags ou prix)."""
    if values.get('attrib_set'):
        return True
    if values.get('tags'):
        return True
    min_price = values.get('min_price')
    available_min = values.get('available_min_price')
    max_price = values.get('max_price')
    available_max = values.get('available_max_price')
    if min_price is not None and available_min is not None:
        if round(float(min_price), 2) != round(float(available_min), 2):
            return True
    if max_price is not None and available_max is not None:
        if round(float(max_price), 2) != round(float(available_max), 2):
            return True
    return False


def ck_should_show_rebound(values, post):
    """Condition complète D5/C3 — retourne True si le bloc rebond doit s'afficher."""
    if not values.get('category'):
        return False
    count = values.get('search_count', 0)
    if count == 0 or count >= 3:
        return False
    if values.get('search') or values.get('original_search'):
        return False
    if ck_shop_has_active_filters(values, post):
        return False
    return True
