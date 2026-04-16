# -*- coding: utf-8 -*-

"""Garde snapshot / restauration du compte HelloAsso 1:1 société (recette tenant_01)."""

import logging

_logger = logging.getLogger(__name__)

HELLOASSO_ACCOUNT_SNAPSHOT_FIELDS = (
    "name",
    "environment",
    "use_for_members",
    "use_for_ticketing",
    "membership_pont_rail",
    "membership_bridge_enabled",
    "membership_bridge_product_id",
    "membership_bridge_require_member_type",
)


class HelloassoAccountTestGuard:
    """Les tests peuvent réutiliser le compte réel : état capturé puis restauré."""

    @classmethod
    def _helloasso_guard_setup(cls, company, acc_write_vals, payment_ref_prefixes):
        cls._helloasso_guard_payment_ref_prefixes = tuple(payment_ref_prefixes)
        cls._helloasso_guard_snapshot = None
        cls._helloasso_guard_account_created = False

        Account = cls.env["dorevia.helloasso.account"].sudo()
        existing = Account.search([("company_id", "=", company.id)], limit=1)
        if existing:
            cls._helloasso_guard_snapshot = existing.read(
                list(HELLOASSO_ACCOUNT_SNAPSHOT_FIELDS)
            )[0]
            cls.helloasso_account = existing
            cls.helloasso_account.write(acc_write_vals)
        else:
            cls.helloasso_account = Account.create(
                {**acc_write_vals, "company_id": company.id}
            )
            cls._helloasso_guard_account_created = True

    @classmethod
    def _helloasso_guard_pivot_payments(cls, account, prefixes):
        Payment = cls.env["dorevia.helloasso.payment"].sudo()
        found = Payment.browse()
        for pfx in prefixes:
            found |= Payment.search(
                [
                    ("helloasso_account_id", "=", account.id),
                    ("helloasso_payment_ref", "=ilike", pfx),
                ]
            )
        return found

    @classmethod
    def _helloasso_guard_detach_v2_accounting(cls, payment):
        pay = payment.sudo()
        ap = pay.membership_v2_account_payment_id.sudo()
        move = pay.membership_v2_out_invoice_id.sudo()
        if ap:
            try:
                ap.action_cancel()
            except Exception as err:
                _logger.warning(
                    "Helloasso test guard: annulation paiement comptable id=%s: %s",
                    ap.id,
                    err,
                )
            try:
                ap.unlink()
            except Exception as err:
                _logger.warning(
                    "Helloasso test guard: suppression account.payment id=%s: %s",
                    ap.id,
                    err,
                )
        if move and move.exists():
            try:
                if move.state == "posted":
                    move.button_cancel()
                elif move.state == "draft":
                    pass
            except Exception as err:
                _logger.warning(
                    "Helloasso test guard: annulation facture id=%s: %s",
                    move.id,
                    err,
                )
            try:
                move.unlink()
            except Exception as err:
                _logger.warning(
                    "Helloasso test guard: suppression account.move id=%s: %s",
                    move.id,
                    err,
                )

    @classmethod
    def _helloasso_guard_purge_test_data(cls, account, prefixes):
        Line = cls.env["membership.membership_line"].sudo()
        payments = cls._helloasso_guard_pivot_payments(account, prefixes)
        for pay in payments:
            cls._helloasso_guard_detach_v2_accounting(pay)
            Line.search([("dorevia_helloasso_payment_id", "=", pay.id)]).unlink()
            try:
                pay.unlink()
            except Exception as err:
                _logger.warning(
                    "Helloasso test guard: suppression pivot id=%s: %s", pay.id, err
                )

    @classmethod
    def _helloasso_guard_teardown(cls):
        acc = getattr(cls, "helloasso_account", None)
        if not acc:
            return
        acc = acc.sudo()
        if not acc.exists():
            return

        prefixes = getattr(cls, "_helloasso_guard_payment_ref_prefixes", ())
        if getattr(cls, "_helloasso_guard_account_created", False):
            cls._helloasso_guard_purge_test_data(acc, prefixes)
            try:
                if acc.exists():
                    acc.unlink()
            except Exception as err:
                _logger.warning(
                    "Helloasso test guard: suppression compte HelloAsso id=%s: %s",
                    acc.id,
                    err,
                )
        else:
            snap = getattr(cls, "_helloasso_guard_snapshot", None)
            if snap:
                vals = {
                    k: snap[k]
                    for k in HELLOASSO_ACCOUNT_SNAPSHOT_FIELDS
                    if k in snap
                }
                acc.write(vals)

    @classmethod
    def tearDownClass(cls):
        cls._helloasso_guard_teardown()
        super().tearDownClass()
