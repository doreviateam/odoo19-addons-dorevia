# -*- coding: utf-8 -*-
"""Simulation anomalies GLC YTD — exécuter via odoo shell."""
from collections import Counter

from odoo import fields

today = fields.Date.context_today(env["glc.analytic.anomaly.wizard"])
date_from = today.replace(month=1, day=1)
wizard = env["glc.analytic.anomaly.wizard"].create(
    {
        "company_id": env.company.id,
        "date_from": date_from,
        "date_to": today,
        "include_posted": True,
        "include_draft": False,
    }
)
wizard.action_analyze()

type_labels = dict(env["glc.analytic.anomaly.line"]._fields["anomaly_type"].selection)
counts = Counter(wizard.line_ids.mapped("anomaly_type"))

print("=== SIMULATION ANOMALIES GLC ===")
print("Periode : %s -> %s" % (date_from, today))
print("Societe : %s" % env.company.name)
print("Total anomalies : %s" % wizard.line_count)
print("Poids STRUCTURE (A6) : %.1f%%" % wizard.structure_weight_pct)
print("Alerte STRUCTURE active : %s" % wizard.structure_alert_active)
if wizard.structure_alert_message:
    print("Message A6 : %s" % wizard.structure_alert_message)
print("--- Par type ---")
for key in sorted(counts.keys()):
    print("  %s : %s" % (type_labels.get(key, key), counts[key]))
if not counts:
    print("  (aucune)")
print("--- Exemples (10 premieres lignes) ---")
for line in wizard.line_ids[:10]:
    move = line.move_id.name or line.move_id.ref or str(line.move_id.id)
    partner = line.partner_id.name or "—"
    print(
        "  [%s] %s | %s | %s | %s | %.2f"
        % (line.anomaly_type, line.date, move, partner, line.message, line.amount)
    )
move_lines = wizard._get_move_lines()
print("--- Perimetre ---")
print("Lignes comptables analysees : %s" % len(move_lines))
