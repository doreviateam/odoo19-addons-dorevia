# -*- coding: utf-8 -*-
"""Placeholders image produit CK — neutres visuellement sur la zone média (#faf6f0).

Les anciens tests utilisaient un PNG 1×1 rouge qui, étiré en CSS, produisait
des blocs rouges plein écran sur la recette partagée. Ce module centralise
un placeholder crème discret et des helpers qui ne remplacent pas une vraie photo BO.
"""
import base64

# PNG 1×1 #faf6f0 — aligné sur $ck-image-zone du thème.
CK_CREAM_PLACEHOLDER_PNG_B64 = (
    b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP49e0DAAXOAuG2tfgkAAAAAElFTkSuQmCC'
)
CK_CREAM_PLACEHOLDER_PNG = base64.b64decode(CK_CREAM_PLACEHOLDER_PNG_B64)

# Ancien placeholder rouge (tests / migrations historiques) — à détecter pour nettoyage.
_LEGACY_RED_PLACEHOLDER_PNG_B64 = (
    b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC'
)

# Seuil empirique : une vraie photo BO dépasse largement un PNG 1×1.
_MIN_REAL_IMAGE_B64_LEN = 500


def is_tiny_product_image(image_b64):
    """True si l'image ressemble à un placeholder 1×1 (rouge ou crème)."""
    if not image_b64:
        return True
    if isinstance(image_b64, str):
        image_b64 = image_b64.encode()
    if image_b64 in (CK_CREAM_PLACEHOLDER_PNG_B64, _LEGACY_RED_PLACEHOLDER_PNG_B64):
        return True
    return len(image_b64) < _MIN_REAL_IMAGE_B64_LEN


def ensure_test_product_image(record, field_name='image_1920'):
    """Assure une image test sans écraser une vraie photo BO existante."""
    current = record[field_name]
    if not is_tiny_product_image(current):
        return False
    record.write({field_name: CK_CREAM_PLACEHOLDER_PNG_B64})
    return True


def ensure_test_variant_images(variant):
    """Placeholder discret sur variante + template si nécessaire."""
    changed = ensure_test_product_image(variant, 'image_1920')
    if variant.image_variant_1920 and is_tiny_product_image(variant.image_variant_1920):
        variant.write({'image_variant_1920': CK_CREAM_PLACEHOLDER_PNG_B64})
        changed = True
    template = variant.product_tmpl_id
    if template:
        changed = ensure_test_product_image(template, 'image_1920') or changed
    return changed
