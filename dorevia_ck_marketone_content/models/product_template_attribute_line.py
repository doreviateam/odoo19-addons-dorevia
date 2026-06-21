# -*- coding: utf-8 -*-
from odoo import models


def _is_origin_attribute_line(line):
    attr_name = (line.attribute_id.name or '').lower()
    return 'origine' in attr_name or 'origin' in attr_name


class ProductTemplateAttributeLine(models.Model):
    _inherit = 'product.template.attribute.line'

    def _ck_refresh_featured_if_origin_line(self):
        templates = self.mapped('product_tmpl_id')
        origin_lines = self.filtered(_is_origin_attribute_line)
        if origin_lines and templates:
            templates._ck_refresh_home_featured_if_stale()

    def create(self, vals_list):
        lines = super().create(vals_list)
        lines._ck_refresh_featured_if_origin_line()
        return lines

    def write(self, vals):
        res = super().write(vals)
        if 'value_ids' in vals or 'attribute_id' in vals:
            self._ck_refresh_featured_if_origin_line()
        return res

    def unlink(self):
        templates = self.mapped('product_tmpl_id')
        had_origin = any(_is_origin_attribute_line(line) for line in self)
        res = super().unlink()
        if had_origin and templates:
            templates._ck_refresh_home_featured_if_stale()
        return res
