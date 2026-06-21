# -*- coding: utf-8 -*-
"""Polish visuel home CK — espacements, coffret, newsletter FR (sans logique produit)."""
from .home_arch import _arch_as_string
from .home_featured import _featured_target_langs


def _patch_home_visual_polish_lang(env, page):
    """Réinjecte univers, coffret, dual et éditorial pour la langue courante."""
    view = page.view_id.with_env(env).sudo()
    arch = _arch_as_string(view.arch_db or view.arch)
    if not arch.strip():
        return False

    new_arch = arch

    from .home_univers import build_home_univers_arch, _patch_homepage_univers_arch

    univers_arch = build_home_univers_arch(env)
    if univers_arch:
        new_arch, _ = _patch_homepage_univers_arch(new_arch, univers_arch)

    from .home_discovery_pack import (
        build_discovery_pack_arch,
        _patch_homepage_discovery_pack_arch,
    )

    discovery_arch = build_discovery_pack_arch(env)
    if discovery_arch:
        new_arch, _ = _patch_homepage_discovery_pack_arch(new_arch, discovery_arch)

    from .home_dual_engage import build_home_dual_engage_arch, _patch_homepage_dual_arch

    dual_arch = build_home_dual_engage_arch(env)
    if dual_arch:
        new_arch, _ = _patch_homepage_dual_arch(
            new_arch,
            dual_arch,
            remove_pro_banner=True,
        )

    from .home_editorial import build_home_editorial_arch, _patch_homepage_editorial_arch

    editorial_arch = build_home_editorial_arch()
    if editorial_arch:
        new_arch, _ = _patch_homepage_editorial_arch(new_arch, editorial_arch)

    if new_arch == arch:
        return False

    view.write({'arch_db': new_arch})
    return True


def bootstrap_home_visual_polish(env):
    """Replay des sections home concernées par le polish visuel (toutes langues servies)."""
    if not env.is_superuser():
        env = env(su=True)
    website = env['website'].search([], limit=1)
    if not website:
        return False

    page = env['website.page'].sudo().search([
        ('url', '=', '/'),
        ('website_id', '=', website.id),
    ], limit=1)
    if not page or not page.view_id:
        return False

    changed = False
    for lang in _featured_target_langs(env, website):
        lang_env = env(context=dict(env.context, lang=lang))
        if _patch_home_visual_polish_lang(lang_env, page):
            changed = True
    return changed
