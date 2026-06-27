# -*- coding: utf-8 -*-
"""Init ck_universe sur les catégories racines CK (bannière univers shop V1).

Initialise le champ `product.public.category.ck_universe` sur les 4 univers
racines existants.  La migration est idempotente : elle ne touche pas les
catégories ayant déjà un univers défini.

Stratégie de recherche : par nom (robuste même sans XML ID stable) — même
pattern que la migration 19.0.1.35.0.  Chaque recherche est insensible à la
casse et accepte des variantes de nommage connues.
"""

_UNIVERSE_SEEDS = [
    ('epicerie',  ('Épicerie créole', 'Épicerie')),
    ('boissons',  ('Boissons', 'Boissons des îles')),
    ('soin',      ('Soin & bien-être', 'Soin et bien-être', 'Bien-être')),
    ('artisanat', ('Artisanat', 'Artisanat & culture')),
]


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    _init_ck_universe(env)


def _init_ck_universe(env):
    Category = env['product.public.category'].sudo()
    updated = 0

    for universe, candidate_names in _UNIVERSE_SEEDS:
        cat = Category.browse()
        for name in candidate_names:
            cat = Category.search([
                ('name', '=ilike', name),
                ('parent_id', '=', False),
                ('ck_universe', '=', False),
            ], limit=1)
            if cat:
                break

        if not cat:
            continue

        cat.write({'ck_universe': universe})
        updated += 1

    return updated
