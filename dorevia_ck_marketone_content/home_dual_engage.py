# -*- coding: utf-8 -*-
"""Home Lot 4 — Bloc double Pro / Newsletter (MOA maquette V1)."""
from .hooks import (
    NEWSLETTER_RGPD_NOTE,
    PRO_DUAL_TITLE,
    bootstrap_newsletter_mailing_list,
    build_dual_engage_compact_arch,
)

DUAL_ENGAGE_SECTION_MARKER = 'ck-dual-engage'
DUAL_ENGAGE_HOME_DATA_NAME = 'CK Dual Pro Newsletter home'
PRO_BANNER_MARKER = 's_ck_pro_banner'


def _arch_as_string(arch):
    if isinstance(arch, dict):
        return next(iter(arch.values()), '')
    return arch or ''


def build_home_dual_engage_arch(env):
    """Dual Pro + newsletter compact pour la home · CTA /professionnels."""
    dual = build_dual_engage_compact_arch(
        env,
        pro_cta_href='/professionnels',
    )
    return dual.replace(
        'data-name="CK Dual Pro Newsletter compact"',
        f'data-name="{DUAL_ENGAGE_HOME_DATA_NAME}"',
        1,
    )


def _find_dual_block_bounds(arch):
    start = arch.find('class="s_text_block ck-dual-engage')
    if start < 0:
        for marker in (
            f'data-name="{DUAL_ENGAGE_HOME_DATA_NAME}"',
            'data-name="CK Dual Pro Newsletter compact"',
            'data-name="CK Dual Pro Newsletter"',
        ):
            idx = arch.find(marker)
            if idx >= 0:
                start = arch.rfind('<section', 0, idx)
                break
    if start < 0:
        return -1, -1

    first_close = arch.find('</section>', start)
    if first_close < 0:
        return start, -1
    end = first_close + len('</section>')

    banner_start = arch.find('<section class="s_ck_pro_banner', end)
    if banner_start < 0:
        banner_start = arch.find('data-snippet="s_ck_pro_banner"', end)
        if banner_start >= 0:
            banner_start = arch.rfind('<section', end, banner_start + 1)
    if banner_start >= 0 and banner_start - end < 80:
        banner_close = arch.find('</section>', banner_start)
        if banner_close >= 0:
            end = banner_close + len('</section>')
    return start, end


def _find_dual_insertion_index(arch):
    for marker in ('class="s_text_block ck-discovery-pack', 'data-name="CK Coffrets découverte"'):
        idx = arch.find(marker)
        if idx >= 0:
            section_start = arch.rfind('<section', 0, idx) if 'data-name' in marker else idx
            if section_start < 0:
                section_start = idx
            section_close = arch.find('</section>', section_start)
            if section_close >= 0:
                tail = arch[section_close + len('</section>'):]
                banner_start = tail.find('<section class="s_ck_pro_banner')
                if banner_start >= 0:
                    return section_close + len('</section>') + banner_start
                dual_start = tail.find('class="s_text_block ck-dual-engage')
                if dual_start >= 0:
                    return section_close + len('</section>') + dual_start
                return section_close + len('</section>')
    return -1


def _patch_homepage_dual_arch(arch, dual_arch, *, remove_pro_banner=True):
    start, end = _find_dual_block_bounds(arch)
    if start >= 0 and end >= 0:
        if remove_pro_banner:
            new_arch = arch[:start] + dual_arch + '\n' + arch[end:]
        else:
            first_close = arch.find('</section>', start) + len('</section>')
            new_arch = arch[:start] + dual_arch + '\n' + arch[first_close:]
        return new_arch, True

    insert_at = _find_dual_insertion_index(arch)
    if insert_at < 0:
        return arch, False
    new_arch = arch[:insert_at] + dual_arch + '\n' + arch[insert_at:]
    return new_arch, True


def dual_engage_home_arch_is_valid(arch, env):
    """Recette Lot 4 : dual compact · Pro · newsletter BO · sans bannière Pro redondante."""
    if 'ck-dual-engage--compact' not in arch:
        return False
    chunk_start = arch.find(DUAL_ENGAGE_SECTION_MARKER)
    if chunk_start < 0:
        return False
    chunk = arch[chunk_start:chunk_start + 12000]
    mailing_list = bootstrap_newsletter_mailing_list(env)
    checks = [
        PRO_DUAL_TITLE in chunk,
        'href="/professionnels"' in chunk,
        'ck-newsletter-subscribe' in chunk,
        's_newsletter_subscribe_form' in chunk,
        f'data-list-id="{mailing_list.id}"' in chunk,
        NEWSLETTER_RGPD_NOTE.split('Désinscription')[0].strip()[:20] in chunk,
        'col-lg-6' in chunk,
    ]
    if not all(checks):
        return False
    pack_pos = arch.find('ck-discovery-pack')
    dual_pos = arch.find(DUAL_ENGAGE_SECTION_MARKER)
    if pack_pos >= 0 and dual_pos >= 0 and not (pack_pos < dual_pos):
        return False
    if f'class="{PRO_BANNER_MARKER}' in arch:
        return False
    return True


def bootstrap_home_dual_engage(env, *, remove_pro_banner=True):
    """Lot 4 home — dual Pro/Newsletter compact · retire bannière Pro redondante."""
    website = env['website'].search([], limit=1)
    if not website:
        return False

    bootstrap_newsletter_mailing_list(env)

    page = env['website.page'].sudo().search([
        ('url', '=', '/'),
        ('website_id', '=', website.id),
    ], limit=1)
    if not page or not page.view_id:
        return False

    view = page.view_id.sudo()
    arch = _arch_as_string(view.arch_db or view.arch)
    if not arch.strip():
        return False

    if dual_engage_home_arch_is_valid(arch, env):
        return True

    dual_arch = build_home_dual_engage_arch(env)
    new_arch, patched = _patch_homepage_dual_arch(
        arch,
        dual_arch,
        remove_pro_banner=remove_pro_banner,
    )
    if not patched or new_arch == arch:
        return patched

    view.write({'arch_db': new_arch})
    return dual_engage_home_arch_is_valid(new_arch, env)
