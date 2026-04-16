# -*- coding: utf-8 -*-
"""Construction du payload connecteur Odoo -> Vault."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from odoo import models


DOCUMENT_KIND_MAP = {
    "out_invoice": ("sale_invoice", "incoming", 1),
    "in_invoice": ("purchase_invoice", "outgoing", -1),
    "out_refund": ("sale_credit_note", "outgoing", -1),
    "in_refund": ("purchase_credit_note", "incoming", 1),
}


def _document_semantics(move: models.Model) -> Tuple[str, str, int]:
    move_type = move.move_type or ""
    if move_type not in DOCUMENT_KIND_MAP:
        raise ValueError(f"move_type non pris en charge: {move_type}")
    return DOCUMENT_KIND_MAP[move_type]


def build_payload(move: models.Model) -> Dict[str, Any]:
    """Retourne un dict JSON-sérialisable pour un document comptable posté."""
    self = move
    self.ensure_one()
    icp = self.env["ir.config_parameter"].sudo()
    tenant = (icp.get_param("dorevia_vault_connector.tenant") or "").strip() or "default"
    company = self.company_id.name or ""
    partner = self.commercial_partner_id.name or ""
    posted_at = self.write_date or self.create_date
    document_kind, direction, sign = _document_semantics(self)
    return {
        "event_type": "account.move.posted",
        "source_system": "odoo",
        "source_model": "account.move",
        "source_id": self.id,
        "source_ref": self.name or str(self.id),
        "tenant": tenant,
        "company": company,
        "move_type": self.move_type,
        "document_kind": document_kind,
        "direction": direction,
        "sign": sign,
        "document_date": self.invoice_date.isoformat() if self.invoice_date else None,
        "posted_at": posted_at.isoformat(timespec="seconds") if posted_at else None,
        "currency": self.currency_id.name if self.currency_id else None,
        "amount_total": abs(float(self.amount_total)),
        "amount_untaxed": abs(float(self.amount_untaxed)),
        "partner_name": partner,
    }


def build_payment_payload(payment: models.Model) -> Dict[str, Any]:
    """Retourne un dict JSON-sérialisable pour un paiement Odoo validé."""
    self = payment
    self.ensure_one()
    icp = self.env["ir.config_parameter"].sudo()
    tenant = (icp.get_param("dorevia_vault_connector.tenant") or "").strip() or "default"
    company = self.company_id.name or ""
    partner = self.partner_id.name or company
    posted_at = self.move_id.write_date or self.write_date or self.create_date
    direction = "incoming" if self.payment_type == "inbound" else "outgoing"
    sign = 1 if direction == "incoming" else -1

    return {
        "event_type": "account.payment.posted",
        "source_system": "odoo",
        "source_model": "account.payment",
        "source_id": self.id,
        "source_ref": self.name or self.payment_reference or str(self.id),
        "tenant": tenant,
        "company": company,
        "document_kind": "payment",
        "direction": direction,
        "sign": sign,
        "payment_type": self.payment_type,
        "partner_type": self.partner_type,
        "journal_name": self.journal_id.name if self.journal_id else None,
        "document_date": self.date.isoformat() if self.date else None,
        "posted_at": posted_at.isoformat(timespec="seconds") if posted_at else None,
        "currency": self.currency_id.name if self.currency_id else None,
        "amount_total": abs(float(self.amount)),
        "amount_untaxed": abs(float(self.amount)),
        "partner_name": partner,
    }
