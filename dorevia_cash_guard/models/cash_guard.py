# -*- coding: utf-8 -*-

from collections import defaultdict
from datetime import date, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class DoreviaCashGuard(models.Model):
    # Champs du point dont une modification doit relancer la projection complète.
    _RECOMPUTE_GUARD_WRITE_FIELDS = {
        "alert_threshold",
        "comfort_threshold_rate",
        "bank_journal_id",
        "company_id",
        "date_from",
        "date_to",
        "liquidity_journal_ids",
        "periodicity",
    }

    _name = "dorevia.cash.guard"
    _description = "Projection de trésorerie Dorevia"
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
    active = fields.Boolean(
        string="Actif",
        default=True,
        copy=False,
        tracking=True,
        help=(
            "Document de projection courant. Désactiver pour archiver la projection "
            "(masquée des vues par défaut ; lignes et analyses restent liées au même document)."
        ),
    )
    date_from = fields.Date(
        string="Date de début",
        required=True,
        tracking=True,
        index=True,
        default=lambda self: self._default_period_date_from(),
        help=(
            "À la création d’un nouveau document : même jour que la date de situation (date du jour), "
            "pour démarrer la projection à partir de maintenant."
        ),
    )
    date_to = fields.Date(
        string="Date de fin",
        required=True,
        tracking=True,
        index=True,
        default=lambda self: self._default_period_date_to(),
        help=(
            "À la création d’un nouveau document : date de début + 90 jours (projection opérationnelle)."
        ),
    )
    situation_date = fields.Date(
        string="Date de situation",
        required=True,
        readonly=True,
        index=True,
        copy=False,
        help=(
            "Date de référence pour le solde constaté : le jour de calcul (date du jour dans "
            "le fuseau utilisateur), borné entre la date de début et la date de fin."
        ),
    )
    liquidity_journal_ids = fields.Many2many(
        "account.journal",
        "dorevia_cash_guard_liquidity_journal_rel",
        "guard_id",
        "journal_id",
        string="Journaux",
        domain=[("type", "in", ("bank", "cash"))],
        tracking=True,
        help=(
            "Banques et caisses incluses dans le solde de trésorerie à date. "
            "Si vide, le journal historique ci-dessous est utilisé."
        ),
    )
    bank_journal_id = fields.Many2one(
        "account.journal",
        string="Journal bancaire (compatibilité)",
        required=False,
        domain=[("type", "in", ("bank", "cash"))],
        tracking=True,
        index=True,
        help=(
            "Champ historique V1 : premier journal banque/caisse. "
            "Préférez « Journaux » pour le périmètre complet."
        ),
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
    comfort_threshold_rate = fields.Float(
        string="Seuil de confort (%)",
        default=20.0,
        tracking=True,
        help=(
            "Marge de sécurité au-dessus du seuil d'alerte. "
            "Le statut Sécurisé n'est atteint que si la projection dépasse "
            "seuil d'alerte × (1 + taux / 100)."
        ),
    )
    periodicity = fields.Selection(
        [
            ("week", "Semaine"),
            ("month", "Mois"),
            ("quarter", "Trimestre"),
        ],
        string="Périodicité",
        default="week",
        required=True,
        tracking=True,
    )
    initial_balance = fields.Monetary(string="Solde début exercice", readonly=True, copy=False)
    observed_balance = fields.Monetary(
        string="Solde de trésorerie constaté",
        readonly=True,
        copy=False,
    )
    observed_balance_date = fields.Date(
        string="Date du solde observé",
        readonly=True,
        copy=False,
    )
    bank_confirmation_rate = fields.Float(
        string="Taux de confirmation bancaire",
        readonly=True,
        copy=False,
        help=(
            "Pourcentage des mouvements de trésorerie confirmés par relevé bancaire "
            "(rapprochés avec une ligne de relevé) par rapport au total des mouvements "
            "sur les journaux de trésorerie du périmètre, jusqu'à la date de situation."
        ),
    )
    bank_unreconciled_amount = fields.Monetary(
        string="Écritures bancaires non rapprochées",
        readonly=True,
        copy=False,
        help=(
            "Montant total (en valeur absolue) des écritures de trésorerie non "
            "rapprochées dans le périmètre du document : lignes comptables de "
            "liquidité sans lien relevé bancaire + paiements postés non rapprochés."
        ),
    )
    forecast_final_balance = fields.Monetary(
        string="Projection en fin de période",
        readonly=True,
        copy=False,
        help=(
            "Dernière valeur cumulée de la colonne Projection (mailles Situation + Projeté), "
            "soit trésorerie constatée et factures ouvertes, avec flux complémentaires par maille."
        ),
    )
    forecast_min_balance = fields.Monetary(
        string="Projection minimum",
        readonly=True,
        copy=False,
        help="Minimum des soldes projetés sur les mailles Situation et Projeté.",
    )
    min_balance_date = fields.Date(
        string="Date du point bas projeté",
        readonly=True,
        copy=False,
        help="Fin de la maille où le minimum de projection est atteint (cohérent avec le suivi).",
    )
    forecast_min_margin = fields.Monetary(
        string="Couverture minimum",
        currency_field="currency_id",
        readonly=True,
        copy=False,
        help=(
            "Au point bas projeté : couverture minimum (projection minimum moins le seuil d'alerte), "
            "alignée sur la colonne Couverture du suivi. Couverture négative : il manque ce montant "
            "par rapport au seuil au point le plus bas."
        ),
    )
    risk_status = fields.Selection(
        [
            ("safe", "Confort"),
            ("warning", "Vigilance"),
            ("tension", "Tension"),
            ("risk", "Risque"),
        ],
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
        help=(
            "Champ technique (plus affiché en V1.1). La projection est une lecture dynamique ; "
            "un vrai cycle de validation pourra s’appuyer sur des snapshots plus tard."
        ),
    )
    responsible_id = fields.Many2one("res.users", string="Resp.", index=True)
    line_ids = fields.One2many(
        "dorevia.cash.guard.line",
        "guard_id",
        string="Flux complémentaires",
    )
    weekly_line_ids = fields.One2many(
        "dorevia.cash.guard.week",
        "guard_id",
        string="Détail de projection",
    )
    projection_period_move_ids = fields.One2many(
        "dorevia.cash.guard.period.move",
        "guard_id",
        string="Détail projection (factures)",
        readonly=True,
    )
    projection_unsecured_period_move_ids = fields.One2many(
        "dorevia.cash.guard.period.move",
        "guard_id",
        string="Détail projection non sécurisées",
        compute="_compute_projection_unsecured_period_move_ids",
        readonly=True,
    )
    total_documents_impact = fields.Monetary(
        string="Total impact",
        compute="_compute_total_documents_impact",
        currency_field="currency_id",
        help="Somme des impacts des documents réels et simulés sur l'ensemble de la projection.",
    )
    note = fields.Text(string="Notes")

    @api.model
    def _default_period_date_from(self):
        """Date du jour : alignée par défaut sur la date de situation (ex. création le 10/05 → 10/05)."""
        return fields.Date.context_today(self)

    @api.model
    def _default_period_date_to(self):
        """Horizon par défaut : 90 jours après la date du jour (cohérent avec ``date_from`` par défaut)."""
        return fields.Date.context_today(self) + timedelta(days=90)

    @api.depends("projection_period_move_ids.period_risk_status")
    def _compute_projection_unsecured_period_move_ids(self):
        for guard in self:
            guard.projection_unsecured_period_move_ids = (
                guard.projection_period_move_ids.filtered(
                    lambda line: line.period_risk_status in ("risk", "tension", "warning")
                )
            )

    @api.depends("projection_period_move_ids", "projection_period_move_ids.signed_amount")
    def _compute_total_documents_impact(self):
        for guard in self:
            guard.total_documents_impact = sum(
                (line.signed_amount or 0.0) for line in guard.projection_period_move_ids
            )

    @api.model
    def _situation_date_for_period(self, date_from, date_to):
        """Date du jour, bornée à la période suivie (référence pour le solde de trésorerie à date)."""
        today = fields.Date.context_today(self)
        if not date_from or not date_to:
            return today
        if not isinstance(date_from, date):
            date_from = fields.Date.from_string(date_from)
        if not isinstance(date_to, date):
            date_to = fields.Date.from_string(date_to)
        return min(max(today, date_from), date_to)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("Nouveau")) == _("Nouveau"):
                seq = self.env["ir.sequence"].next_by_code("dorevia.cash.guard")
                vals["name"] = (
                    _("Projection Trésorerie — %s") % seq if seq else _("Nouveau")
                )
            vals.pop("situation_date", None)
            df = vals.get("date_from")
            dt = vals.get("date_to")
            if df is None:
                vals["date_from"] = self._default_period_date_from()
                df = vals["date_from"]
            if dt is None:
                df_end = df if isinstance(df, date) else fields.Date.from_string(df)
                vals["date_to"] = df_end + timedelta(days=90)
                dt = vals["date_to"]
            vals["situation_date"] = self._situation_date_for_period(df, dt)
        records = super().create(vals_list)
        records._sync_legacy_bank_journal_from_liquidity()
        records.action_recompute_projection()
        return records

    @api.constrains("situation_date", "date_from", "date_to")
    def _check_situation_date_range(self):
        for guard in self:
            if (
                guard.situation_date
                and guard.date_from
                and guard.date_to
                and not (guard.date_from <= guard.situation_date <= guard.date_to)
            ):
                raise ValidationError(
                    _("La date de situation doit être comprise dans la période d'exercice.")
                )

    @api.constrains(
        "date_from",
        "date_to",
        "alert_threshold",
        "bank_journal_id",
        "liquidity_journal_ids",
        "company_id",
    )
    def _check_business_constraints(self):
        for guard in self:
            if guard.date_from and guard.date_to and guard.date_from > guard.date_to:
                raise ValidationError(
                    _("La date de début doit être inférieure ou égale à la date de fin.")
                )
            if guard.alert_threshold < 0:
                raise ValidationError(_("Le seuil d'alerte doit être positif ou nul."))
            journals = guard._liquidity_journals()
            if not journals:
                raise ValidationError(
                    _(
                        "Sélectionnez au moins un journal banque ou caisse "
                        "(ou renseignez le journal de compatibilité)."
                    )
                )
            for journal in journals:
                if journal.type not in ("bank", "cash"):
                    raise ValidationError(
                        _("Les journaux de trésorerie doivent être de type Banque ou Caisse.")
                    )
                if journal.company_id != guard.company_id:
                    raise ValidationError(
                        _("Chaque journal doit appartenir à la même société que le document de projection.")
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
                    _("Le nom du document de projection doit être unique par société.")
                )

    def _liquidity_journals(self):
        """Périmètre banque + caisse : préférence aux journaux explicites, sinon journal V1."""
        self.ensure_one()
        if self.liquidity_journal_ids:
            return self.liquidity_journal_ids
        if self.bank_journal_id:
            return self.bank_journal_id
        return self.env["account.journal"]

    def _bank_only_journals(self):
        """Sous-ensemble banque (type='bank') du périmètre de trésorerie.

        Utilisé pour les indicateurs de confirmation bancaire qui ne
        doivent pas inclure la caisse.
        """
        return self._liquidity_journals().filtered(lambda j: j.type == "bank")

    def _sync_legacy_bank_journal_from_liquidity(self):
        """Aligne le champ historique `bank_journal_id` sur le premier journal du périmètre."""
        for guard in self:
            if guard.liquidity_journal_ids:
                primary = guard.liquidity_journal_ids[0]
                if guard.bank_journal_id != primary:
                    guard.with_context(skip_cash_guard_recompute=True).write(
                        {"bank_journal_id": primary.id}
                    )

    def _liquidity_account_ids_for_journal(self, journal):
        """Comptes explicites liés à un journal (champs + lignes de méthodes de paiement Odoo 19)."""
        field_names = (
            "default_account_id",
            "suspense_account_id",
            "loss_account_id",
            "profit_account_id",
            "non_deductible_account_id",
        )
        legacy_optional = ("payment_debit_account_id", "payment_credit_account_id")
        account_ids = set()
        for field_name in field_names:
            if field_name not in journal._fields:
                continue
            account = journal[field_name]
            if account:
                account_ids.add(account.id)
        for field_name in legacy_optional:
            if field_name not in journal._fields:
                continue
            account = journal[field_name]
            if account:
                account_ids.add(account.id)
        for pm_line in journal.inbound_payment_method_line_ids:
            if pm_line.payment_account_id:
                account_ids.add(pm_line.payment_account_id.id)
        for pm_line in journal.outbound_payment_method_line_ids:
            if pm_line.payment_account_id:
                account_ids.add(pm_line.payment_account_id.id)
        return account_ids

    def _get_liquidity_account_ids(self):
        """Union des comptes liés au périmètre (cf. :meth:`_liquidity_account_ids_for_journal`)."""
        account_ids = set()
        for journal in self._liquidity_journals():
            account_ids.update(self._liquidity_account_ids_for_journal(journal))
        return list(account_ids)

    def _liquidity_account_types_for_journal(self, journal):
        """Types de compte autorisés pour le solde, selon le type de journal.

        Les journaux *cash* acceptent aussi ``asset_current`` : en pratique, la caisse (ex. 530000)
        est parfois paramétrée ainsi dans les plans francophones au lieu de ``asset_cash``.
        Les journaux *bank* / *credit* restent plus stricts ; le suspense bancaire passe par les
        comptes explicites du journal.
        """
        if journal.type == "cash":
            return ("asset_cash", "asset_current")
        if journal.type in ("bank", "credit"):
            return ("asset_cash", "liability_credit_card")
        return ("asset_cash", "liability_credit_card")

    def _compute_bank_balance_at_date(self, target_date):
        """Somme des soldes à date sur les journaux banque/caisse du périmètre (écritures postées)."""
        self.ensure_one()
        if not target_date:
            return 0.0
        journals = self._liquidity_journals()
        if not journals:
            return 0.0
        base_common = [
            ("company_id", "=", self.company_id.id),
            ("parent_state", "=", "posted"),
            ("date", "<=", target_date),
            (
                "display_type",
                "not in",
                ("line_section", "line_subsection", "line_note"),
            ),
        ]
        total = 0.0
        AccountLine = self.env["account.move.line"].sudo()
        for journal in journals:
            explicit_ids = self._liquidity_account_ids_for_journal(journal)
            type_tuple = self._liquidity_account_types_for_journal(journal)
            if explicit_ids:
                account_scope = fields.Domain.OR(
                    [
                        [("account_id.account_type", "in", type_tuple)],
                        [("account_id", "in", list(explicit_ids))],
                    ]
                )
            else:
                account_scope = [("account_id.account_type", "in", type_tuple)]
            domain = fields.Domain.AND(
                [base_common + [("journal_id", "=", journal.id)], account_scope]
            )
            total += sum(AccountLine.search(domain).mapped("balance"))
        return total

    def _compute_bank_confirmation_rate(self, target_date):
        """Taux de confirmation bancaire : abs(confirmé) / (abs(mouvements) + abs(paiements en transit)).

        Deux familles composent le dénominateur :

        1. Mouvements de trésorerie sur comptes de liquidité (mêmes que le solde constaté).
           Un mouvement est « confirmé » si ``statement_line_id`` est renseigné.

        2. Paiements bancaires en transit (``account.payment`` postés, ``is_matched = False``
           sur les journaux du périmètre, date <= situation). Ces paiements ne sont pas encore
           rapprochés avec un relevé : ils gonflent le dénominateur sans augmenter le numérateur.
        """
        self.ensure_one()
        if not target_date:
            return 0.0
        journals = self._bank_only_journals()
        if not journals:
            return 0.0
        base_common = [
            ("company_id", "=", self.company_id.id),
            ("parent_state", "=", "posted"),
            ("date", "<=", target_date),
            (
                "display_type",
                "not in",
                ("line_section", "line_subsection", "line_note"),
            ),
        ]
        total_abs = 0.0
        confirmed_abs = 0.0
        AccountLine = self.env["account.move.line"].sudo()
        for journal in journals:
            explicit_ids = self._liquidity_account_ids_for_journal(journal)
            type_tuple = self._liquidity_account_types_for_journal(journal)
            if explicit_ids:
                account_scope = fields.Domain.OR(
                    [
                        [("account_id.account_type", "in", type_tuple)],
                        [("account_id", "in", list(explicit_ids))],
                    ]
                )
            else:
                account_scope = [("account_id.account_type", "in", type_tuple)]
            domain = fields.Domain.AND(
                [base_common + [("journal_id", "=", journal.id)], account_scope]
            )
            lines = AccountLine.search(domain)
            for line in lines:
                amount = abs(line.balance)
                total_abs += amount
                if line.statement_line_id:
                    confirmed_abs += amount
        outstanding_abs = self._outstanding_payment_abs(journals, target_date)
        total_abs += outstanding_abs
        if not total_abs:
            return 0.0
        return (confirmed_abs / total_abs) * 100.0

    def _outstanding_payment_abs(self, journals, target_date):
        """Montant absolu des paiements postés non rapprochés sur les journaux du périmètre."""
        self.ensure_one()
        self.env.cr.execute(
            """
            SELECT COALESCE(SUM(ABS(pay.amount)), 0)
              FROM account_payment pay
              JOIN account_move move ON move.origin_payment_id = pay.id
             WHERE pay.is_matched IS NOT TRUE
               AND move.state = 'posted'
               AND move.date <= %s
               AND pay.journal_id = ANY(%s)
               AND pay.company_id = %s
            """,
            [target_date, list(journals.ids), self.company_id.id],
        )
        return self.env.cr.fetchone()[0] or 0.0

    def _compute_bank_unreconciled_amount(self):
        """Montant abs des paiements non rapprochés, aligné sur le dashboard Odoo.

        Réutilise ``account.journal._get_journal_dashboard_outstanding_payments``
        (même requête que le bloc « Paiements » du tableau de bord comptable)
        puis somme ``abs()`` du net signé par journal.

        Aucun filtre date : le montant affiché correspond exactement à ce que
        l'utilisateur voit dans le tableau de bord lorsqu'il clique sur le lien.
        """
        self.ensure_one()
        journals = self._bank_only_journals()
        if not journals:
            return 0.0
        dashboard = journals._get_journal_dashboard_outstanding_payments()
        total = 0.0
        for journal in journals:
            entry = dashboard.get(journal.id)
            if not entry:
                continue
            amount = entry[1] if isinstance(entry, (list, tuple)) else entry.get("amount", 0.0)
            total += abs(amount)
        return total

    def _compute_initial_balance(self):
        self.ensure_one()
        return self._compute_bank_balance_at_date(self.date_from)

    def _comfort_threshold_amount(self):
        """Seuil monétaire de confort : seuil d'alerte × (1 + taux / 100)."""
        self.ensure_one()
        th = self.alert_threshold or 0.0
        rate = self.comfort_threshold_rate or 0.0
        return th * (1.0 + rate / 100.0)

    def _compute_risk_status(self, projected_balance):
        """Bands alignées sur la colonne Projection vs seuils (grille Suivi + décorations).

        * ``projected_balance <= 0`` → risk (rouge) ;
        * ``0 < projected_balance < alert_threshold`` → tension (orange) ;
        * ``alert_threshold <= projected_balance < comfort_threshold`` → warning (bleu) ;
        * ``projected_balance >= comfort_threshold`` → safe (vert).
        """
        self.ensure_one()
        pb = projected_balance or 0.0
        th = self.alert_threshold or 0.0
        comfort = self._comfort_threshold_amount()
        if pb <= 0:
            return "risk"
        if pb < th:
            return "tension"
        if pb >= comfort:
            return "safe"
        return "warning"

    def _search_open_invoice_moves(self):
        """Factures / avoirs validés, non soldés — critère métier : posted + résiduel (V1.2)."""
        self.ensure_one()
        return self.env["account.move"].sudo().search(
            [
                ("company_id", "=", self.company_id.id),
                ("state", "=", "posted"),
                (
                    "move_type",
                    "in",
                    ("out_invoice", "in_invoice", "out_refund", "in_refund"),
                ),
                ("amount_residual", "!=", 0.0),
            ]
        )

    def _cash_impact_signed_for_invoice_move(self, move):
        """Impact trésorerie du résidu selon le type de pièce (voir doctrine V1.2)."""
        magnitude = abs(move.amount_residual or 0.0)
        return {
            "out_invoice": magnitude,
            "in_invoice": -magnitude,
            "out_refund": -magnitude,
            "in_refund": magnitude,
        }.get(move.move_type, 0.0)

    def _invoice_flow_amounts_for_move(self, move):
        """Découpe l'impact signé en entrées / sorties affichables (montants positifs)."""
        signed = self._cash_impact_signed_for_invoice_move(move)
        if signed >= 0:
            return signed, 0.0
        return 0.0, -signed

    def _invoice_projected_cash_date(self, move, situation_date):
        """Date d'intégration : max(reference_due, situation_date) avec fallbacks V1.2."""
        ref = move.invoice_date_due or move.invoice_date or situation_date
        if not ref:
            return None
        if not situation_date:
            return ref
        return max(ref, situation_date)

    def _week_index_for_date(self, meta, target_date):
        """Retourne l'indice de maille contenant ``target_date``, ou None."""
        if not target_date:
            return None
        for week_index, wf, wt in meta:
            if wf <= target_date <= wt:
                return week_index
        return None

    def _open_invoice_week_buckets(self, meta, situation_date):
        """Agrège les factures ouvertes par indice de période (réseau de suivi)."""
        self.ensure_one()
        buckets = defaultdict(lambda: {"net": 0.0, "inflow": 0.0, "outflow": 0.0})
        for move in self._search_open_invoice_moves():
            proj_date = self._invoice_projected_cash_date(move, situation_date)
            if not proj_date:
                continue
            widx = self._week_index_for_date(meta, proj_date)
            if widx is None:
                continue
            signed = self._cash_impact_signed_for_invoice_move(move)
            inf, outf = self._invoice_flow_amounts_for_move(move)
            buckets[widx]["net"] += signed
            buckets[widx]["inflow"] += inf
            buckets[widx]["outflow"] += outf
        return buckets

    def _manual_line_net_by_week_index(self, meta, situation_date):
        """Agrège les flux Cash Guard futurs par maille pour conserver la trajectoire V1.1."""
        self.ensure_one()
        buckets = defaultdict(float)
        for line in self.line_ids:
            if not line.projection_date or line.projection_date <= situation_date:
                continue
            widx = self._week_index_for_date(meta, line.projection_date)
            if widx is None:
                continue
            buckets[widx] += line.signed_projected_amount or 0.0
        return buckets

    def _cumulative_projected_by_week_index(
        self, meta, situation_date, observed_balance, invoice_buckets, line_buckets=None
    ):
        """Projection cumulée (champ ``projected_balance``) : V1.1 + factures ouvertes V1.2."""
        self.ensure_one()
        if not meta or situation_date is None:
            return {}
        line_buckets = line_buckets or {}
        sit_week_idx = None
        forecast_indices = []
        for week_index, wf, wt in meta:
            ptype = self._period_type_for_segment(wf, wt, situation_date)
            if ptype == "current":
                sit_week_idx = week_index
            elif ptype == "forecast":
                forecast_indices.append(week_index)
        if sit_week_idx is None:
            return {}
        out = {}
        running = (
            observed_balance
            + line_buckets.get(sit_week_idx, 0.0)
            + invoice_buckets.get(sit_week_idx, {}).get("net", 0.0)
        )
        out[sit_week_idx] = running
        for idx in forecast_indices:
            running += line_buckets.get(idx, 0.0)
            running += invoice_buckets.get(idx, {}).get("net", 0.0)
            out[idx] = running
        return out

    def _is_cash_guard_manager(self):
        return self.env.user.has_group("dorevia_cash_guard.group_cash_guard_manager")

    def _check_write_permissions_by_state(self, vals):
        """V1.1 : pas de verrouillage utilisateur selon ``state`` (workflow masqué en UI).

        Les actions ``action_validate`` / ``action_close`` / ``action_reopen`` restent disponibles
        côté code pour compatibilité et tests ; une validation métier pourra être réintroduite
        avec un mécanisme de snapshot.
        """

    def action_compute_initial_balance(self):
        for guard in self:
            guard.initial_balance = guard._compute_initial_balance()
        return True

    def _get_projection_summary_values(self):
        """Calcule les soldes de synthèse sans effet de bord, utilisable en onchange.

        Les indicateurs « projection » (fin de période, minimum, date du minimum) suivent la
        même trajectoire que la colonne ``projected_balance`` du suivi (Situation + Projeté),
        et non plus un simple enchaînement ligne à ligne des flux.
        """
        self.ensure_one()
        situation_date = self._situation_date_for_period(self.date_from, self.date_to)
        initial_balance = self._compute_bank_balance_at_date(self.date_from)
        observed_balance = self._compute_bank_balance_at_date(situation_date)
        bank_confirmation_rate = self._compute_bank_confirmation_rate(situation_date)
        bank_unreconciled_amount = self._compute_bank_unreconciled_amount()
        meta = self._split_exercise_periods()
        invoice_buckets = self._open_invoice_week_buckets(meta, situation_date)
        line_buckets = self._manual_line_net_by_week_index(meta, situation_date)
        pmap = self._cumulative_projected_by_week_index(
            meta, situation_date, observed_balance, invoice_buckets, line_buckets
        )
        meta_by_idx = {idx: (wf, wt) for idx, wf, wt in meta}

        if pmap:
            ordered_keys = sorted(pmap.keys())
            forecast_final_balance = pmap[ordered_keys[-1]]
            forecast_min_balance = min(pmap.values())
            min_week_idx = min(pmap.items(), key=lambda kv: (kv[1], kv[0]))[0]
            min_balance_date = meta_by_idx[min_week_idx][1]
        else:
            forecast_final_balance = observed_balance
            forecast_min_balance = observed_balance
            min_balance_date = situation_date

        forecast_min_margin = forecast_min_balance - self.alert_threshold

        return {
            "situation_date": situation_date,
            "initial_balance": initial_balance,
            "observed_balance": observed_balance,
            "observed_balance_date": situation_date,
            "bank_confirmation_rate": bank_confirmation_rate,
            "bank_unreconciled_amount": bank_unreconciled_amount,
            "forecast_final_balance": forecast_final_balance,
            "forecast_min_balance": forecast_min_balance,
            "forecast_min_margin": forecast_min_margin,
            "min_balance_date": min_balance_date,
            "risk_status": self._compute_risk_status(forecast_min_balance),
        }

    def _projection_summary_from_weekly_forward_lines(self):
        """Indicateurs projection alignés sur la grille (après ``_sync_weekly_lines``).

        Utilise les ``projected_balance`` des mailles Situation + Projeté uniquement,
        soit exactement la colonne Projection du suivi.
        """
        self.ensure_one()
        lines = self.weekly_line_ids.filtered(
            lambda w: w.period_type in ("current", "forecast")
        ).sorted("week_index")
        situation_date = self._situation_date_for_period(self.date_from, self.date_to)
        observed = self.observed_balance or 0.0
        if not lines:
            fm = observed - self.alert_threshold
            return {
                "forecast_final_balance": observed,
                "forecast_min_balance": observed,
                "forecast_min_margin": fm,
                "min_balance_date": situation_date,
                "risk_status": self._compute_risk_status(observed),
            }
        balances = lines.mapped("projected_balance")
        forecast_final_balance = lines[-1].projected_balance
        forecast_min_balance = min(balances)
        forecast_min_margin = forecast_min_balance - self.alert_threshold
        min_line = min(lines, key=lambda w: (w.projected_balance, w.week_index))
        return {
            "forecast_final_balance": forecast_final_balance,
            "forecast_min_balance": forecast_min_balance,
            "forecast_min_margin": forecast_min_margin,
            "min_balance_date": min_line.date_to,
            "risk_status": self._compute_risk_status(forecast_min_balance),
        }

    @api.onchange(
        "date_from",
        "date_to",
        "liquidity_journal_ids",
        "bank_journal_id",
        "alert_threshold",
        "comfort_threshold_rate",
        "periodicity",
        "line_ids",
        "line_ids.projection_date",
        "line_ids.sequence",
        "line_ids.direction",
        "line_ids.projected_amount",
    )
    def _onchange_projection_inputs(self):
        for guard in self:
            if not guard.date_from or not guard.date_to or not guard.company_id:
                continue
            if not guard._liquidity_journals():
                continue
            values = guard._get_projection_summary_values()
            for field_name, value in values.items():
                guard[field_name] = value

    def _period_type_for_segment(self, seg_date_from, seg_date_to, situation_date):
        self.ensure_one()
        if seg_date_to < situation_date:
            return "historical"
        if seg_date_from > situation_date:
            return "forecast"
        return "current"

    @staticmethod
    def _last_day_of_month(year, month):
        if month == 12:
            return date(year, 12, 31)
        return date(year, month + 1, 1) - timedelta(days=1)

    @staticmethod
    def _last_day_of_quarter_from_month(year, month):
        q_end_month = ((month - 1) // 3 + 1) * 3
        return DoreviaCashGuard._last_day_of_month(year, q_end_month)

    def _split_exercise_weeks(self):
        """Découpe [date_from, date_to] en blocs d'au plus 7 jours."""
        self.ensure_one()
        df = self.date_from
        dt = self.date_to
        if not df or not dt or df > dt:
            return []
        periods = []
        idx = 1
        cur = df
        while cur <= dt:
            week_end = min(cur + timedelta(days=6), dt)
            periods.append((idx, cur, week_end))
            idx += 1
            cur = week_end + timedelta(days=1)
        return periods

    def _split_exercise_months(self):
        """Découpe [date_from, date_to] par mois calendaires."""
        self.ensure_one()
        df = self.date_from
        dt = self.date_to
        if not df or not dt or df > dt:
            return []
        periods = []
        idx = 1
        cur = df
        while cur <= dt:
            mend = self._last_day_of_month(cur.year, cur.month)
            seg_end = min(mend, dt)
            periods.append((idx, cur, seg_end))
            idx += 1
            cur = seg_end + timedelta(days=1)
        return periods

    def _split_exercise_quarters(self):
        """Découpe [date_from, date_to] par trimestres calendaires."""
        self.ensure_one()
        df = self.date_from
        dt = self.date_to
        if not df or not dt or df > dt:
            return []
        periods = []
        idx = 1
        cur = df
        while cur <= dt:
            qend = self._last_day_of_quarter_from_month(cur.year, cur.month)
            seg_end = min(qend, dt)
            periods.append((idx, cur, seg_end))
            idx += 1
            cur = seg_end + timedelta(days=1)
        return periods

    def _split_exercise_periods(self):
        """Découpe la période suivie selon la périodicité (maille d'affichage)."""
        self.ensure_one()
        if self.periodicity == "month":
            return self._split_exercise_months()
        if self.periodicity == "quarter":
            return self._split_exercise_quarters()
        return self._split_exercise_weeks()

    def _week_iso_display_label(self, segment_start):
        """Libellé maille « semaine » : ``Sxx`` = numéro de semaine ISO (01–53) du début de période."""
        self.ensure_one()
        if not segment_start:
            return ""
        if not isinstance(segment_start, date):
            segment_start = fields.Date.from_string(segment_start)
        _year, iso_week, _dow = segment_start.isocalendar()
        return "S%02d" % iso_week

    def _period_display_label(self, index, wf, wt):
        """Fallback si aucune maille « situation » (point d’ancrage P0) n’est résolue."""
        self.ensure_one()
        if self.periodicity == "month":
            return "%02d/%04d" % (wf.month, wf.year)
        if self.periodicity == "quarter":
            quarter = (wf.month - 1) // 3 + 1
            return "T%d %d" % (quarter, wf.year)
        return self._week_iso_display_label(wf)

    def _situation_meta_position(self, meta, situation_date):
        """Index 0-based dans ``meta`` de la maille contenant la date de situation (type « current »)."""
        self.ensure_one()
        if not meta or not situation_date:
            return None
        for pos, (_wi, wf, wt) in enumerate(meta):
            if self._period_type_for_segment(wf, wt, situation_date) == "current":
                return pos
        return None

    def _period_anchor_display_label(self, meta_pos, sit_meta_pos, week_index, wf, wt):
        """Libellé colonne Période : en semaine ISO ``Sxx`` ; sinon P relatif / mois / trimestre."""
        self.ensure_one()
        if self.periodicity == "week":
            return self._week_iso_display_label(wf)
        if sit_meta_pos is None:
            return self._period_display_label(week_index, wf, wt)
        rel = meta_pos - sit_meta_pos
        return "P%d" % rel

    def _sync_weekly_lines(self):
        """Régénère les lignes de suivi par maille (historique / situation / projection engagée)."""
        self.ensure_one()
        Week = self.env["dorevia.cash.guard.week"].sudo()
        Week.search([("guard_id", "=", self.id)]).unlink()

        meta = self._split_exercise_periods()
        sit = self.situation_date
        if not meta or not sit:
            return

        bank = lambda d: self._compute_bank_balance_at_date(d)
        observed = self.observed_balance
        buckets = self._open_invoice_week_buckets(meta, sit)
        line_buckets = self._manual_line_net_by_week_index(meta, sit)
        proj_map = self._cumulative_projected_by_week_index(
            meta, sit, observed, buckets, line_buckets
        )

        sit_meta_pos = self._situation_meta_position(meta, sit)

        prev_closing = None
        forecast_chunks = []

        for meta_pos, (week_index, wf, wt) in enumerate(meta):
            ptype = self._period_type_for_segment(wf, wt, sit)
            label = self._period_anchor_display_label(
                meta_pos, sit_meta_pos, week_index, wf, wt
            )
            bc = buckets.get(
                week_index, {"net": 0.0, "inflow": 0.0, "outflow": 0.0}
            )

            if ptype == "historical":
                if week_index == 1:
                    opening = bank(self.date_from - timedelta(days=1))
                else:
                    opening = prev_closing
                closing = bank(wt)
                prev_closing = closing
                proj_bal = closing
                rs = self._compute_risk_status(proj_bal)
                Week.create(
                    {
                        "guard_id": self.id,
                        "week_index": week_index,
                        "week_label": label,
                        "date_from": wf,
                        "date_to": wt,
                        "period_type": "historical",
                        "opening_balance": opening,
                        "inflow_amount": 0.0,
                        "outflow_amount": 0.0,
                        "closing_balance": closing,
                        "projected_balance": proj_bal,
                        "invoice_inflow_amount": bc["inflow"],
                        "invoice_outflow_amount": bc["outflow"],
                        "min_balance": closing,
                        "risk_status": rs,
                    }
                )

            elif ptype == "current":
                opening = (
                    prev_closing
                    if prev_closing is not None
                    else bank(wf - timedelta(days=1))
                )
                closing = observed
                prev_closing = closing
                proj_bal = proj_map.get(week_index, observed + bc["net"])
                rs = self._compute_risk_status(proj_bal)
                Week.create(
                    {
                        "guard_id": self.id,
                        "week_index": week_index,
                        "week_label": label,
                        "date_from": wf,
                        "date_to": wt,
                        "period_type": "current",
                        "opening_balance": opening,
                        "inflow_amount": 0.0,
                        "outflow_amount": 0.0,
                        "closing_balance": closing,
                        "projected_balance": proj_bal,
                        "invoice_inflow_amount": bc["inflow"],
                        "invoice_outflow_amount": bc["outflow"],
                        "min_balance": closing,
                        "risk_status": rs,
                    }
                )

            else:
                forecast_chunks.append((week_index, wf, wt, label))

        running = observed
        for week_index, wf, wt, label in forecast_chunks:
            lines_week = self.line_ids.filtered(
                lambda l, wf=wf, wt=wt, sit=sit: l.projection_date
                and wf <= l.projection_date <= wt
                and l.projection_date > sit
            )
            nets = []
            for line in lines_week:
                amt = line.signed_projected_amount or 0.0
                nets.append(amt)
            net = sum(nets)
            inflow = sum(a for a in nets if a > 0)
            outflow = sum(-a for a in nets if a < 0)
            closing = running + net
            running = closing
            bc = buckets.get(
                week_index, {"net": 0.0, "inflow": 0.0, "outflow": 0.0}
            )
            proj_bal = proj_map.get(week_index, observed)
            rs = self._compute_risk_status(proj_bal)
            Week.create(
                {
                    "guard_id": self.id,
                    "week_index": week_index,
                    "week_label": label,
                    "date_from": wf,
                    "date_to": wt,
                    "period_type": "forecast",
                    "opening_balance": running - net,
                    "inflow_amount": inflow,
                    "outflow_amount": outflow,
                    "closing_balance": closing,
                    "projected_balance": proj_bal,
                    "invoice_inflow_amount": bc["inflow"],
                    "invoice_outflow_amount": bc["outflow"],
                    "min_balance": closing,
                    "risk_status": rs,
                }
            )

    def _get_simulation_period_move_rows(self, meta, sit, weeks_by_index):
        """Hook pour les modules simulation : retourne les lignes Documents simulés.

        Chaque ligne doit contenir une clé ``_sort`` pour le tri unifié.
        Conçu pour être étendu par ``dorevia_cash_simulation`` et
        ``dorevia_cash_simulation_purchase``.
        """
        return []

    def _sync_projection_period_moves(self):
        """Régénère les lignes Documents : factures ouvertes + documents simulés retenus."""
        self.ensure_one()
        from .cash_guard_period_move import _MOVE_TYPE_LABELS

        PeriodMove = self.env["dorevia.cash.guard.period.move"].sudo()
        PeriodMove.search([("guard_id", "=", self.id)]).unlink()
        meta = self._split_exercise_periods()
        sit = self.situation_date
        if not meta or not sit:
            return
        weeks_by_index = {w.week_index: w for w in self.weekly_line_ids}
        rows = []
        for move in self._search_open_invoice_moves():
            proj_date = self._invoice_projected_cash_date(move, sit)
            if not proj_date:
                continue
            widx = self._week_index_for_date(meta, proj_date)
            if widx is None:
                continue
            week = weeks_by_index.get(widx)
            if not week:
                continue
            signed = self._cash_impact_signed_for_invoice_move(move)
            ref = move.invoice_date_due or move.invoice_date
            is_overdue = bool(ref and sit and ref < sit)
            days_overdue = max(0, (sit - ref).days) if ref and sit and ref < sit else 0
            mag = abs(move.amount_residual or 0.0)
            expl = "inflow" if signed >= 0 else "outflow"
            rows.append(
                {
                    "guard_id": self.id,
                    "week_id": week.id,
                    "move_id": move.id,
                    "partner_id": move.partner_id.id if move.partner_id else False,
                    "responsible_id": move.invoice_user_id.id if move.invoice_user_id else False,
                    "move_name": move.name or "",
                    "invoice_date": move.invoice_date,
                    "invoice_date_due": move.invoice_date_due,
                    "projected_date": proj_date,
                    "amount_residual": mag,
                    "signed_amount": signed,
                    "currency_id": self.company_id.currency_id.id,
                    "company_id": self.company_id.id,
                    "explanation_type": expl,
                    "is_overdue": is_overdue,
                    "days_overdue": days_overdue,
                    "is_simulation": False,
                    "document_type_label": _MOVE_TYPE_LABELS.get(
                        move.move_type, move.move_type or ""
                    ),
                    "display_status": week.risk_status or "safe",
                    "_sort": (week.week_index, proj_date, signed, move.id),
                }
            )

        sim_rows = self._get_simulation_period_move_rows(meta, sit, weeks_by_index)
        rows.extend(sim_rows)

        rows.sort(key=lambda r: r["_sort"])
        seq = 10
        for item in rows:
            item.pop("_sort", None)
            item["sequence"] = seq
            seq += 10
        if rows:
            PeriodMove.create(rows)
        for week in self.weekly_line_ids:
            pm = week.projection_move_ids
            net = sum(pm.mapped("signed_amount"))
            week.sudo().write(
                {
                    "invoice_net_amount": net,
                    "invoice_move_count": len(pm),
                }
            )

    def _realign_period_to_situation_plus_90_days(self):
        """Réaligne sur la situation à date + horizon 90 jours (bouton Actualiser si exposé).

        ``date_from`` = ``situation_date``, ``date_to`` = ``date_from`` + 90 jours.
        Une future évolution pourra préserver une « période personnalisée ».
        """
        self.ensure_one()
        today = fields.Date.context_today(self)
        date_from = today
        date_to = date_from + timedelta(days=90)
        situation_date = self._situation_date_for_period(date_from, date_to)
        date_from = situation_date
        date_to = date_from + timedelta(days=90)
        situation_date = self._situation_date_for_period(date_from, date_to)
        self.with_context(
            skip_cash_guard_recompute=True,
            allow_cash_guard_situation_write=True,
        ).write(
            {
                "date_from": date_from,
                "date_to": date_to,
                "situation_date": situation_date,
            }
        )

    def action_reset_period_to_defaults(self):
        """Réapplique les valeurs par défaut de période (situation à date + 90 j) puis recalcule tout."""
        return self.with_context(cash_guard_actualiser_realign=True).action_recompute_projection()

    def action_recompute_projection(self):
        for guard in self:
            if self.env.context.get("cash_guard_actualiser_realign"):
                guard._realign_period_to_situation_plus_90_days()
            values = guard._get_projection_summary_values()

            running_balance = values["initial_balance"]

            ordered_lines = guard.line_ids.sorted(
                key=lambda l: (l.projection_date or fields.Date.today(), l.sequence, l.id)
            )
            for line in ordered_lines:
                running_balance += line.signed_projected_amount
                line.with_context(skip_cash_guard_recompute=True).write(
                    {"balance_after_line": running_balance}
                )

            guard.with_context(
                skip_cash_guard_recompute=True,
                allow_cash_guard_situation_write=True,
            ).write(values)
            guard._sync_weekly_lines()
            guard._sync_projection_period_moves()
            proj_align = guard._projection_summary_from_weekly_forward_lines()
            guard.with_context(
                skip_cash_guard_recompute=True,
                allow_cash_guard_situation_write=True,
            ).write(proj_align)
        return True

    def action_open_bank_reconciliation(self):
        """Ouvre le tableau de bord comptable filtré sur les journaux banque du périmètre."""
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "account.open_account_journal_dashboard_kanban"
        )
        journals = self._bank_only_journals()
        if journals:
            action["domain"] = [("id", "in", journals.ids)]
        return action

    def action_archive(self):
        """Archive le document de projection (masqué par défaut, lignes inchangées)."""
        self.write({"active": False})
        return True

    def action_unarchive(self):
        """Réactive un document archivé."""
        self.write({"active": True})
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
                _("Seul un manager Cash Guard peut clôturer un document de projection.")
            )
        for guard in self:
            if guard.state != "validated":
                raise UserError(
                    _("Seul un document validé peut être clôturé.")
                )
            guard.state = "closed"
        return True

    def action_reopen(self):
        if not self._is_cash_guard_manager():
            raise UserError(
                _("Seul un manager Cash Guard peut rouvrir un document de projection.")
            )
        for guard in self:
            if guard.state in ("validated", "closed"):
                guard.state = "draft"
        return True

    def write(self, vals):
        vals = dict(vals)
        if "situation_date" in vals and not self.env.context.get(
            "allow_cash_guard_situation_write"
        ):
            vals.pop("situation_date")
        self._check_write_permissions_by_state(vals)
        res = super().write(vals)
        if "liquidity_journal_ids" in vals:
            self._sync_legacy_bank_journal_from_liquidity()
        if self.env.context.get("skip_cash_guard_recompute"):
            return res
        if set(vals) & self._RECOMPUTE_GUARD_WRITE_FIELDS:
            self.action_recompute_projection()
        return res

    @api.model
    def _cron_recompute_open_points(self):
        """Cron optionnel : recalcule tous les points (lecture dynamique à date, sans filtre ``state``)."""
        guards = self.sudo().search([])
        guards.action_recompute_projection()
        return True
