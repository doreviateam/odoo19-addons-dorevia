#!/usr/bin/env python3
"""QA conformité — injecte le bouton pause accessible (WCAG 2.2.2) dans la home figée.

La home (`website.page` url='/') porte un snapshot HTML figé du hero (cf
ck_phase2_configure.py / ck_q1_ssr_featured.py) : éditer dorevia_ck_theme/views/
snippets/ck_snippet_hero.xml ne suffit pas, ce script réplique le même bouton
pause dans l'arch_db de la home. Idempotent — relançable sans risque de doublon.

Usage :
  docker exec -i sandbox-odoo19-odoo-1 odoo shell -d dorevia_ck_marketone_01 --no-http \\
    < ck_a11y_hero_pause_button.py
  docker restart sandbox-odoo19-odoo-1
"""

PAUSE_BUTTON = (
    '<button type="button" class="ck-hero__visual-pause" aria-pressed="false" '
    'aria-label="Mettre en pause le défilement automatique des visuels">'
    '<i class="fa fa-pause" aria-hidden="true"/></button>'
)

page = env['website.page'].search([('url', '=', '/')], limit=1)
view = page.view_id
arch = view.arch_db or view.arch or ''
if isinstance(arch, dict):
    arch = arch.get(env.lang) or next(iter(arch.values()), '')

if 'ck-hero__visual-pause' in arch:
    print('Bouton pause déjà présent — no-op')
else:
    marker = '"Visuel hero 3"'
    occurrences = arch.count(marker)
    if occurrences != 1:
        raise SystemExit(f'Repère "{marker}" trouvé {occurrences} fois (1 attendu) — structure home inattendue')
    pos = arch.find(marker)
    # Depuis le repère, 3 </div> ferment .ck-hero__slide-media, .carousel-item, .carousel-inner
    # — insertion juste avant la fermeture du carrousel lui-même (#ckHeroVisualCarousel).
    for _ in range(3):
        pos = arch.find('</div>', pos) + len('</div>')
    new_arch = arch[:pos] + PAUSE_BUTTON + arch[pos:]
    if 'ckHeroVisualCarousel' not in new_arch[:pos] or new_arch.count('ck-hero__visual-pause') != 1:
        raise SystemExit('Insertion suspecte — abandon sans écriture')
    view.write({'arch_db': new_arch})
    env.cr.commit()
    print('Bouton pause injecté · view_id', view.id, '· restart Odoo requis')
