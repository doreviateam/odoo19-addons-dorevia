# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DoreviaCashGuard(models.Model):
    _name = "dorevia.cash.guard"
    _description = "Dorevia Cash Guard"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_from desc, id desc"

    name = fields.Char(
        required=True,
        copy=False,
        default=lambda self: _("Nouveau"),
        tracking=True,
        index=True,
    )
    date_from = fields.Date(required=True, tracking=True, index=True)
    date_to = fields.Date(required=True, tracking=True, index=True)
    bank_journal_id = fields.Many2one(
        "account.journal",
        required=True,
        domain=[("type", "in", ("bank", "cash"))],
        tracking=True,
        index=True,
    )
    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="company_id.currency_id",
        store=True,
        readonly=True,
    )
    alert_threshold = fields.Monetary(default=0.0, required=True, tracking=True)
    initial_balance = fields.Monetary(readonly=True, copy=False)
    forecast_final_balance = fields.Monetary(readonly=True, copy=False)
    forecast_min_balance = fields.Monetary(readonly=True, copy=False)
    min_balance_date = fields.Date(readonly=True, copy=False)
    risk_status = fields.Selection(
        [("safe", "Securise"), ("warning", "Vigilance"), ("risk", "Risque")],
        default="safe",
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        index=True,
    )
    state = fields.Selection(
        [("draft", "Brouillon"), ("validated", "Valide"), ("closed", "Cloture")],
        default="draft",
        required=True,
        tracking=True,
        index=True,
    )
    responsible_id = fields.Many2one("res.users", index=True)
    line_ids = fields.One2many("dorevia.cash.guard.line", "guard_id")
    note = fields.Text()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("Nouveau")) == _("Nouveau"):
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "dorevia.cash.guard"
                ) or _("Nouveau")
        records = super().create(vals_list)
        records.action_recompute_projection()
        return records

    @api.constrains("date_from", "date_to", "alert_threshold", "bank_journal_id", "company_id")
    def _check_business_constraints(self):
        for guard in self:
            if guard.date_from and guard.date_to and guard.date_from > guard.date_to:
                raise ValidationError(
                    _("La date de debut doit etre inferieure ou egale a la date de fin.")
                )
            if guard.alert_threshold < 0:
                raise ValidationError(_("Le seuil d'alerte doit etre positif ou nul."))
            if guard.bank_journal_id.type not in ("bank", "cash"):
                raise ValidationError(
                    _("Le journal suivi doit etre de type Banque ou Caisse.")
                )
            if guard.bank_journal_id.company_id != guard.company_id:
                raise ValidationError(
                    _("Le journal doit appartenir a la meme societe que le point.")
                )

    @api.constrains("name", "company_id")
    def _check_name_company_unique(self):
        for guard in self:
            if not guard.name or not guard.company_id:
                continue
            duplicate = self.search(
                [
                    ("id", "!=", guard.id),
                    ("name", "=", guard.name),
                    ("company_id", "=", guard.company_id.id),
                ],
                limit=1,
            )
            if duplicate:
                raise ValidationError(
                    _("Le nom du point de tresorerie doit etre unique par societe.")
                )

    def _get_liquidity_account_ids(self):
        self.ensure_one()
        journal = self.bank_journal_id
        field_names = (
            "default_account_id",
            "payment_debit_account_id",
            "payment_credit_account_id",
            "loss_account_id",
            "profit_account_id",
            "suspense_account_id",
        )
        account_ids = set()
        for field_name in field_names:
            if field_name in journal._fields:
                account = journal[field_name]
                if account:
                    account_ids.add(account.id)
        return list(account_ids)

    def _compute_initial_balance(self):
        self.ensure_one()
        liquidity_account_ids = self._get_liquidity_account_ids()
        domain = [
            ("company_id", "=", self.company_id.id),
            ("parent_state", "=", "posted"),
            ("date", "<=", self.date_from),
        ]
        if liquidity_account_ids:
            domain += [
                "|",
                ("journal_id", "=", self.bank_journal_id.id),
                ("account_id", "in", liquidity_account_ids),
            ]
        else:
            domain.append(("journal_id", "=", self.bank_journal_id.id))
        move_lines = self.env["account.move.line"].search(domain)
        return sum(move_lines.mapped("balance"))

    def _compute_risk_status(self, min_balance):
        self.ensure_one()
        if min_balance < 0:
            return "risk"
        if min_balance < self.alert_threshold:
            return "warning"
        return "safe"

    def action_compute_initial_balance(self):
        for guard in self:
            guard.initial_balance = guard._compute_initial_balance()
        return True

    def action_recompute_projection(self):
        for guard in self:
            initial_balance = guard._compute_initial_balance()
            running_balance = initial_balance
            min_balance = initial_balance
            min_balance_date = guard.date_from

            ordered_lines = guard.line_ids.sorted(
                key=lambda l: (l.projection_date or fields.Date.today(), l.sequence, l.id)
            )
            for line in ordered_lines:
                running_balance += line.signed_projected_amount
                line.with_context(skip_cash_guard_recompute=True).write(
                    {"balance_after_line": running_balance}
                )
                if running_balance < min_balance:
                    min_balance = running_balance
                    min_balance_date = line.projection_date

            guard.with_context(skip_cash_guard_recompute=True).write(
                {
                    "initial_balance": initial_balance,
                    "forecast_final_balance": running_balance,
                    "forecast_min_balance": min_balance,
                    "min_balance_date": min_balance_date,
                    "risk_status": guard._compute_risk_status(min_balance),
                }
            )
        return True
