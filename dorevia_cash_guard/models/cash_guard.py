# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class DoreviaCashGuard(models.Model):
    _PROTECTED_FIELDS_AFTER_VALIDATION = {
        "date_from",
        "date_to",
        "bank_journal_id",
        "alert_threshold",
        "line_ids",
        "company_id",
    }

    _name = "dorevia.cash.guard"
    _description = "Point de trésorerie Dorevia"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_from desc, id desc"

    name = fields.Char(
        string="Nom",
        required=True,
        copy=False,
        default=lambda self: _("Nouveau"),
        tracking=True,
        index=True,
    )
    date_from = fields.Date(string="Date de début", required=True, tracking=True, index=True)
    date_to = fields.Date(string="Date de fin", required=True, tracking=True, index=True)
    bank_journal_id = fields.Many2one(
        "account.journal",
        string="Journal bancaire",
        required=True,
        domain=[("type", "in", ("bank", "cash"))],
        tracking=True,
        index=True,
    )
    company_id = fields.Many2one(
        "res.company",
        string="Société",
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Devise",
        related="company_id.currency_id",
        store=True,
        readonly=True,
    )
    alert_threshold = fields.Monetary(
        string="Seuil d'alerte",
        default=0.0,
        required=True,
        tracking=True,
    )
    initial_balance = fields.Monetary(string="Solde initial", readonly=True, copy=False)
    forecast_final_balance = fields.Monetary(
        string="Solde final prévisionnel",
        readonly=True,
        copy=False,
    )
    forecast_min_balance = fields.Monetary(
        string="Solde minimum prévisionnel",
        readonly=True,
        copy=False,
    )
    min_balance_date = fields.Date(string="Date du point bas", readonly=True, copy=False)
    risk_status = fields.Selection(
        [("safe", "Sécurisé"), ("warning", "Vigilance"), ("risk", "Risque")],
        string="Statut de risque",
        default="safe",
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        index=True,
    )
    state = fields.Selection(
        [("draft", "Brouillon"), ("validated", "Validé"), ("closed", "Clôturé")],
        string="État",
        default="draft",
        required=True,
        tracking=True,
        index=True,
    )
    responsible_id = fields.Many2one("res.users", string="Responsable", index=True)
    line_ids = fields.One2many(
        "dorevia.cash.guard.line",
        "guard_id",
        string="Flux prévisionnels",
    )
    note = fields.Text(string="Notes")

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
                    _("La date de début doit être inférieure ou égale à la date de fin.")
                )
            if guard.alert_threshold < 0:
                raise ValidationError(_("Le seuil d'alerte doit être positif ou nul."))
            if guard.bank_journal_id.type not in ("bank", "cash"):
                raise ValidationError(
                    _("Le journal suivi doit être de type Banque ou Caisse.")
                )
            if guard.bank_journal_id.company_id != guard.company_id:
                raise ValidationError(
                    _("Le journal doit appartenir à la même société que le point.")
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
                    _("Le nom du point de trésorerie doit être unique par société.")
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
            ("journal_id", "=", self.bank_journal_id.id),
            ("parent_state", "=", "posted"),
            ("date", "<=", self.date_from),
        ]
        if liquidity_account_ids:
            domain.append(("account_id", "in", liquidity_account_ids))
        # Lecture comptable en sudo: seul le solde agrege est renvoye.
        move_lines = self.env["account.move.line"].sudo().search(domain)
        return sum(move_lines.mapped("balance"))

    def _compute_risk_status(self, min_balance):
        self.ensure_one()
        if min_balance < 0:
            return "risk"
        if min_balance < self.alert_threshold:
            return "warning"
        return "safe"

    def _is_cash_guard_manager(self):
        return self.env.user.has_group("dorevia_cash_guard.group_cash_guard_manager")

    def _check_write_permissions_by_state(self, vals):
        if self.env.context.get("skip_cash_guard_recompute"):
            return
        is_manager = self._is_cash_guard_manager()
        for guard in self:
            if guard.state == "closed":
                if not is_manager:
                    raise UserError(
                        _(
                            "Un point clôturé ne peut être modifié que par un manager Cash Guard."
                        )
                    )
                continue
            if guard.state == "validated" and not is_manager:
                if self._PROTECTED_FIELDS_AFTER_VALIDATION.intersection(vals):
                    raise UserError(
                        _(
                            "Après validation, les champs structurants sont modifiables "
                            "uniquement par un manager ou après retour en brouillon."
                        )
                    )

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

    def action_validate(self):
        for guard in self:
            if guard.state != "draft":
                continue
            guard.action_recompute_projection()
            guard.state = "validated"
        return True

    def action_close(self):
        if not self._is_cash_guard_manager():
            raise UserError(
                _("Seul un manager Cash Guard peut clôturer un point de trésorerie.")
            )
        for guard in self:
            if guard.state != "validated":
                raise UserError(
                    _("Seul un point validé peut être clôturé.")
                )
            guard.state = "closed"
        return True

    def action_reopen(self):
        if not self._is_cash_guard_manager():
            raise UserError(
                _("Seul un manager Cash Guard peut rouvrir un point de trésorerie.")
            )
        for guard in self:
            if guard.state in ("validated", "closed"):
                guard.state = "draft"
        return True

    def write(self, vals):
        self._check_write_permissions_by_state(vals)
        return super().write(vals)

    @api.model
    def _cron_recompute_open_points(self):
        """Cron optionnel: recalcule uniquement les points ouverts."""
        guards = self.sudo().search([("state", "in", ("draft", "validated"))])
        guards.action_recompute_projection()
        return True
