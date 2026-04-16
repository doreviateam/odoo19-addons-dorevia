# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import format_date

from . import membership_helloasso_bridge_user_messages as bu_msg


class DoreviaMembershipHelloassoBridge(models.AbstractModel):
    """Pont métier : pivot ``dorevia.helloasso.payment`` → ``membership.membership_line`` sans facture.

    Règle d'idempotence (Sprint 1, no-op strict) : si une ligne existe déjà avec le même
    ``dorevia_helloasso_payment_id``, aucune écriture n'est effectuée.

    Renouvellement (V1) : pas de prolongation ; refus si une ligne existe déjà pour le même
    contact et produit avec des dates qui recoupent la période du produit (CADRAGE).
    """

    _name = "dorevia.membership.helloasso.bridge"
    _description = "Pont HelloAsso : pivot paiement → adhésion Odoo"

    @api.model
    def process_payment_to_membership_line(self, payment, membership_product):
        """Crée une ligne d'adhésion sans facture, ou retourne un no-op strict.

        :param payment: enregistrement ``dorevia.helloasso.payment``
        :param membership_product: ``product.product`` marqué ``membership`` (service)
        :return: dict avec clés ``state`` (``created`` | ``noop``), ``line``, ``message``
        """
        payment.ensure_one()
        membership_product.ensure_one()

        if not payment.active:
            raise UserError(
                bu_msg.payment_archived_v1(
                    payment.helloasso_payment_ref or str(payment.id)
                )
            )

        Line = self.env["membership.membership_line"].sudo()
        existing = Line.search(
            [("dorevia_helloasso_payment_id", "=", payment.id)], limit=1
        )
        if existing:
            return {
                "state": "noop",
                "line": existing,
                "message": _("Déjà traité : ligne d'adhésion existante pour ce paiement (idempotence)."),
            }

        if not membership_product.membership:
            raise UserError(
                bu_msg.product_not_membership(membership_product.display_name)
            )
        if membership_product.type != "service":
            raise UserError(bu_msg.product_must_be_service())

        email = (payment.payer_email or "").strip().lower()
        if not email:
            raise UserError(bu_msg.payment_missing_payer_email())

        Partner = self.env["res.partner"].sudo().with_context(active_test=False)
        domain = [
            ("email", "=ilike", email),
            "|",
            ("company_id", "=", False),
            ("company_id", "=", payment.company_id.id),
        ]
        partners = Partner.search(domain)
        if len(partners) == 0:
            raise UserError(
                _("Aucun contact trouvé pour l'e-mail « %s » (société %s).")
                % (email, payment.company_id.display_name)
            )
        if len(partners) > 1:
            raise UserError(
                _("Plusieurs contacts pour l'e-mail « %s » : cas nominal ambigu (règle pont).")
                % (email,)
            )
        partner = partners[0]

        # Garde-fou métier (S3-1 piste A) : le bridge tranche, sans modifier le miroir HelloAsso.
        if not partner.active:
            raise UserError(
                bu_msg.partner_archived_v1(
                    partner.display_name,
                    payment.helloasso_payment_ref or str(payment.id),
                )
            )

        account = payment.helloasso_account_id
        if (
            account
            and account.membership_bridge_require_member_type
            and not partner.member_type_id
        ):
            raise UserError(
                bu_msg.partner_missing_member_type_v1(
                    partner.display_name,
                    payment.helloasso_payment_ref or str(payment.id),
                )
            )

        if (
            membership_product.company_id
            and membership_product.company_id != payment.company_id
        ):
            raise UserError(
                bu_msg.membership_product_company_mismatch(
                    membership_product.company_id.display_name,
                    payment.company_id.display_name,
                )
            )
        if partner.company_id and partner.company_id != payment.company_id:
            raise UserError(
                bu_msg.partner_company_mismatch(
                    partner.display_name, payment.company_id.display_name
                )
            )

        pay_date = fields.Date.today()
        if payment.payment_date:
            pay_date = fields.Datetime.to_datetime(payment.payment_date).date()

        date_from = membership_product.membership_date_from
        date_to = membership_product.membership_date_to
        if not date_from or not date_to:
            raise UserError(
                bu_msg.membership_product_dates_required(
                    membership_product.display_name
                )
            )
        # Règle v1 : date de référence du paiement dans la fenêtre produit (voir ZeDocs REGLE_DATES_…).
        if pay_date < date_from or pay_date > date_to:
            raise UserError(
                bu_msg.payment_date_outside_product_window(
                    self.env,
                    pay_date,
                    membership_product.display_name,
                    date_from,
                    date_to,
                )
            )

        # Renouvellement V1 : nouvelle ligne uniquement si pas de recoupement (contact + produit).
        overlap = Line.search(
            [
                ("partner", "=", partner.id),
                ("membership_id", "=", membership_product.id),
                ("date_from", "<=", date_to),
                ("date_to", ">=", date_from),
            ],
            limit=1,
        )
        if overlap:
            raise UserError(
                _(
                    "Une ligne d'adhésion existe déjà pour ce contact et ce produit sur une période "
                    "qui recoupe celle du produit « %(prod)s » (%(df)s — %(dt)s). "
                    "Renouvellement / doublon de période : traitement manuel ou arbitrage métier (V1)."
                )
                % {
                    "prod": membership_product.display_name,
                    "df": format_date(self.env, date_from),
                    "dt": format_date(self.env, date_to),
                }
            )

        amount = payment.amount_tariff or payment.amount_total
        if amount in (False, None) or amount == 0:
            amount = membership_product.list_price

        vals = {
            "partner": partner.id,
            "membership_id": membership_product.id,
            "member_price": float(amount),
            "date": pay_date,
            "date_from": date_from,
            "date_to": date_to,
            "state": "paid",
            "dorevia_helloasso_payment_id": payment.id,
        }
        line = Line.create(vals)
        # ``membership_extension`` peut recalculer ``member_price`` depuis le list_price au create : réaligner le pivot.
        if line.member_price != float(amount):
            line.write({"member_price": float(amount)})

        return {
            "state": "created",
            "line": line,
            "message": _("Ligne d'adhésion créée."),
        }
