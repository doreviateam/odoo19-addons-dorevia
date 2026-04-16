# -*- coding: utf-8 -*-

from odoo import fields, models


class RadioglProgrammeSlot(models.Model):
    """Créneau affiché sur la vitrine (grille démo Radio Grand Lieu)."""

    _name = "radiogl.programme.slot"
    _description = "Créneau grille radio (démo)"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    day_label = fields.Char(string="Jour", required=True, help="Ex. Lundi, Samedi…")
    slot_time = fields.Char(string="Horaire", required=True, help="Ex. 18h – 19h")
    title = fields.Char(string="Émission", required=True)
