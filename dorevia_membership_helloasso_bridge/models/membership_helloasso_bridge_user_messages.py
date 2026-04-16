# -*- coding: utf-8 -*-
"""Messages UserError partagés pont V1 (ligne adhésion) et V2 (constatation) — piste C S3-1."""

from odoo import _
from odoo.tools import format_date


def payment_archived_v1(ref):
    return _(
        "Le paiement HelloAsso « %(ref)s » est archivé : le pont d'adhésion ne peut pas "
        "créer de ligne. Réactivez l'enregistrement ou traitez manuellement."
    ) % {"ref": ref}


def payment_archived_v2(ref):
    return _(
        "Le paiement HelloAsso « %(ref)s » est archivé : la constatation V2 ne peut pas "
        "continuer. Réactivez l'enregistrement ou traitez manuellement."
    ) % {"ref": ref}


def partner_archived_v1(partner_name, ref):
    return _(
        "Le contact « %(partner)s » est archivé : le pont d'adhésion refuse de créer "
        "une ligne pour le paiement HelloAsso « %(ref)s ». Réactivez le contact ou "
        "traitez manuellement."
    ) % {"partner": partner_name, "ref": ref}


def partner_missing_member_type_v1(partner_name, ref):
    return _(
        "Le contact « %(partner)s » n'a pas de type d'adhésion (typologie) renseigné : "
        "le pont refuse de créer une ligne pour le paiement HelloAsso « %(ref)s », car "
        "ce compte HelloAsso exige une typologie sur le contact. Renseignez le champ "
        "« Type d'adhésion » sur le contact ou désactivez l'option sur le compte HelloAsso."
    ) % {"partner": partner_name, "ref": ref}


def partner_archived_v2(partner_name, ref):
    return _(
        "Le contact « %(partner)s » est archivé : la constatation V2 refuse de traiter "
        "le paiement HelloAsso « %(ref)s ». Réactivez le contact ou traitez manuellement."
    ) % {"partner": partner_name, "ref": ref}


def product_not_membership(display_name):
    return _("Le produit « %s » n'est pas un produit d'adhésion (membership).") % (
        display_name,
    )


def product_must_be_service():
    return _("Le produit d'adhésion doit être de type service.")


def payment_missing_payer_email():
    return _(
        "Le paiement HelloAsso n'a pas d'e-mail payeur : impossible de résoudre le contact."
    )


def membership_product_company_mismatch(prod_company_name, pay_company_name):
    return _(
        "Le produit d'adhésion (%s) n'est pas sur la même société que le paiement (%s)."
    ) % (prod_company_name, pay_company_name)


def partner_company_mismatch(partner_name, pay_company_name):
    return _("Le contact (%s) n'est pas sur la même société que le paiement (%s).") % (
        partner_name,
        pay_company_name,
    )


def membership_product_dates_required(display_name):
    return _(
        "Le produit d'adhésion « %s » doit avoir des dates de début et de fin."
    ) % (display_name,)


def payment_date_outside_product_window(env, pay_date, prod_display_name, date_from, date_to):
    return _(
        "La date du paiement (%(pay)s) n'entre pas dans la période du produit d'adhésion "
        "« %(prod)s » (%(df)s — %(dt)s)."
    ) % {
        "pay": format_date(env, pay_date),
        "prod": prod_display_name,
        "df": format_date(env, date_from),
        "dt": format_date(env, date_to),
    }
