# -*- coding: utf-8 -*-
"""Migration 19.0.1.9.5 : fiches vitrine + affectation accueil si emplacements vides.

- Création (data) de 4 produits avec visuel, publiés (recette MOA).
- Câblage optionnel : ``website.ckr_ensure_showcase_featured_on_empty_websites``
  uniquement si les 4 champs ``ckr_homepage_featured_[1-4]`` étaient vides
  (ne remplace **pas** une config existante, même partielle).
"""

from odoo.api import Environment, SUPERUSER_ID


def migrate(cr, version):
    env = Environment(cr, SUPERUSER_ID, {})
    env["website"].ckr_ensure_showcase_featured_on_empty_websites()
