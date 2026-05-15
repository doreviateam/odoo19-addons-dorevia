# -*- coding: utf-8 -*-
from odoo import models


class ProductTemplateAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    def _ckr_filter_origin_attribute_mapping(self, mapping, origin_attr):
        """Filtre défensivement la clé `Origine` d'un mapping specs."""
        filtered = {}
        for attribute, values in (mapping or {}).items():
            # Clé standard: record `product.attribute`.
            attr_id = getattr(attribute, "id", False)
            if attr_id and attr_id == origin_attr.id:
                continue

            # Repli défensif: certains thèmes/versions peuvent fournir une
            # clé non standard (ex. libellé). On filtre alors par nom.
            attr_name = (getattr(attribute, "name", "") or str(attribute or "")).strip().lower()
            if attr_name in {"origine", "origin"}:
                continue

            # Repli final: on inspecte les lignes pour exclure tout groupe
            # rattaché à l'attribut Origine, même si la clé n'est pas fiable.
            if any(
                getattr(line, "attribute_id", False)
                and line.attribute_id.id == origin_attr.id
                for line in (values or [])
            ):
                continue

            filtered[attribute] = values
        return filtered

    def _prepare_single_value_for_display(self):
        """Retire l'attribut Origine des specs bases de la fiche produit.

        MVP2.3: l'origine est affichée en bloc informatif dédié (non interactif)
        dans le haut de fiche. On évite donc un doublon en bas dans
        `product_attributes_simple`.
        """
        result = super()._prepare_single_value_for_display()
        origin_attr = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_product_attribute_origin",
            raise_if_not_found=False,
        )
        if not origin_attr:
            return result
        return self._ckr_filter_origin_attribute_mapping(result, origin_attr)

    def _prepare_single_value_including_multi_type_for_display(self):
        """Retire l'attribut Origine des specs `website_sale_comparison`."""
        result = super()._prepare_single_value_including_multi_type_for_display()
        origin_attr = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_product_attribute_origin",
            raise_if_not_found=False,
        )
        if not origin_attr:
            return result
        return self._ckr_filter_origin_attribute_mapping(result, origin_attr)

    def _prepare_categories_for_display_in_specs_table(self):
        """Retire les lignes Origine des catégories du bloc Spécifications."""
        categories = super()._prepare_categories_for_display_in_specs_table()
        origin_attr = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_product_attribute_origin",
            raise_if_not_found=False,
        )
        if not origin_attr:
            return categories

        filtered_categories = {}
        for category, lines in (categories or {}).items():
            kept = (lines or self).filtered(lambda l: l.attribute_id.id != origin_attr.id)
            if kept:
                filtered_categories[category] = kept
        return filtered_categories
