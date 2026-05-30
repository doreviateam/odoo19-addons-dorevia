# -*- coding: utf-8 -*-
"""Benchmark simple du recalcul cockpit GLC.

Usage sandbox :
  docker compose exec -T odoo odoo shell -c /etc/odoo/odoo.conf \
    -d glc-rgl-test-import --no-http \
    < /mnt/odoo19-addons-dorevia/dorevia_glc_analytics/scripts/benchmark_cockpit_refresh.py
"""

from datetime import date
from time import perf_counter

from odoo import fields


Cockpit = env["glc.coverage.cockpit"]
today = fields.Date.context_today(Cockpit)
date_from = date(today.year, 1, 1)
date_to = today

cockpit = Cockpit.create(
    {
        "company_id": env.company.id,
        "date_from": date_from,
        "date_to": date_to,
    }
)

durations = []
for _idx in range(3):
    start = perf_counter()
    cockpit.action_refresh()
    durations.append(perf_counter() - start)

activity_lines = cockpit.line_ids.filtered(lambda line: line.line_kind == "activity")
print("=== BENCHMARK COCKPIT GLC ===")
print("Societe : %s" % env.company.name)
print("Periode : %s -> %s" % (date_from, date_to))
print("Lignes detail activite : %s" % len(activity_lines))
print("Lignes tresorerie interne : %s" % len(cockpit.treasury_line_ids))
print("Temps recalculs : %s" % ", ".join("%.3fs" % value for value in durations))
print("Meilleur temps : %.3fs" % min(durations))
print("Temps moyen : %.3fs" % (sum(durations) / len(durations)))
