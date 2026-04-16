# -*- coding: utf-8 -*-

import base64

from odoo import _, fields, models
from odoo.exceptions import UserError

from .helloasso_payment_import import (
    import_csv_payment_rows,
    import_csv_payment_rows_message,
    parse_payment_csv_content,
    preview_csv_payment_rows,
)


class DoreviaHelloassoPaymentCsvWizard(models.TransientModel):
    _name = "dorevia.helloasso.payment.csv.wizard"
    _description = "HelloAsso payment — import CSV"

    helloasso_account_id = fields.Many2one(
        "dorevia.helloasso.account",
        string="Compte HelloAsso",
        required=True,
        domain="[('active', '=', True)]",
        default=lambda self: self.env["dorevia.helloasso.account"].search(
            [("company_id", "=", self.env.company.id), ("active", "=", True)],
            limit=1,
        ),
    )
    company_id = fields.Many2one(
        "res.company",
        string="Société",
        related="helloasso_account_id.company_id",
        readonly=True,
    )
    import_platform_only = fields.Boolean(
        string="Limiter au MVP plateforme",
        default=True,
        help="Si activé, n'importe que les paiements plateforme HelloAsso.",
    )
    upload_file = fields.Binary(string="Fichier CSV", required=True)
    upload_filename = fields.Char(string="Nom du fichier")
    preview_text = fields.Text(
        string="Aperçu",
        help="Résumé sans enregistrement : recliquez sur « Prévisualiser » après changement de fichier ou d’option MVP.",
    )

    def _get_csv_rows_or_raise(self):
        self.ensure_one()
        if not self.upload_file:
            raise UserError(_("Veuillez importer un fichier CSV HelloAsso."))
        try:
            csv_text = base64.b64decode(self.upload_file).decode("utf-8-sig")
        except Exception as err:
            raise UserError(_("Impossible de lire le fichier CSV : %s") % err) from err
        rows = parse_payment_csv_content(csv_text)
        if not rows:
            raise UserError(_("Le fichier CSV est vide ou illisible."))
        return rows

    def action_preview_csv(self):
        """Construit un texte d’aperçu (aucune écriture sur ``dorevia.helloasso.payment``)."""
        self.ensure_one()
        rows = self._get_csv_rows_or_raise()
        preview_rows = preview_csv_payment_rows(
            self.env,
            self.helloasso_account_id,
            rows,
            import_platform_only=self.import_platform_only,
        )
        lines = []
        for p in preview_rows:
            if p["outcome"] == "error":
                lines.append(
                    _("Ligne %(row)s : erreur — %(msg)s")
                    % {"row": p["row"], "msg": p["message"]}
                )
            elif p["outcome"] == "skip_mvp":
                lines.append(
                    _(
                        "Ligne %(row)s : ignoré (hors MVP plateforme) — réf. %(ref)s, "
                        "campagne %(camp)s, e-mail %(email)s"
                    )
                    % {
                        "row": p["row"],
                        "ref": p.get("ref") or "",
                        "camp": p.get("campaign_type") or "",
                        "email": p.get("email") or "",
                    }
                )
            elif p["outcome"] == "update":
                lines.append(
                    _(
                        "Ligne %(row)s : import prévu — mise à jour du pivot existant — réf. %(ref)s, "
                        "campagne %(camp)s, e-mail %(email)s"
                    )
                    % {
                        "row": p["row"],
                        "ref": p.get("ref") or "",
                        "camp": p.get("campaign_type") or "",
                        "email": p.get("email") or "",
                    }
                )
            else:
                lines.append(
                    _(
                        "Ligne %(row)s : import prévu — création — réf. %(ref)s, "
                        "campagne %(camp)s, e-mail %(email)s"
                    )
                    % {
                        "row": p["row"],
                        "ref": p.get("ref") or "",
                        "camp": p.get("campaign_type") or "",
                        "email": p.get("email") or "",
                    }
                )
        header = _("Fichier : %(n)s ligne(s). Compte : %(acc)s. MVP plateforme : %(mvp)s.\n\n") % {
            "n": len(rows),
            "acc": self.helloasso_account_id.display_name,
            "mvp": _("oui") if self.import_platform_only else _("non"),
        }
        self.write({"preview_text": header + "\n".join(lines)})
        return {
            "type": "ir.actions.act_window",
            "name": _("Import CSV paiements HelloAsso"),
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }

    def action_import_csv(self):
        self.ensure_one()
        rows = self._get_csv_rows_or_raise()
        stats = import_csv_payment_rows(
            self.sudo().env,
            self.helloasso_account_id,
            rows,
            import_platform_only=self.import_platform_only,
        )
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("HelloAsso payment — import CSV"),
                "message": import_csv_payment_rows_message(stats),
                "type": "success" if not stats.get("errors") else "warning",
                "sticky": True,
            },
        }
