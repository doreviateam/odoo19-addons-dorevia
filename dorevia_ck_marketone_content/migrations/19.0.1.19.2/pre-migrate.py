# -*- coding: utf-8 -*-
"""Reprise des étiquettes card custom vers product.tag avant suppression du modèle."""

import json


def _label_name_expr(column):
    return f"trim(COALESCE({column}->>'fr_FR', {column}->>'en_US', ''))"


def migrate(cr, version):
    cr.execute(
        """
        SELECT EXISTS (
            SELECT 1
              FROM information_schema.tables
             WHERE table_name = 'product_template_ck_featured_label_rel'
        )
        """
    )
    if not cr.fetchone()[0]:
        return

    name_expr = _label_name_expr('l.name')
    tag_name_expr = _label_name_expr('name')
    cr.execute(
        f"""
        SELECT DISTINCT lower({name_expr}) AS key, {name_expr} AS label
          FROM dorevia_ck_product_label l
          JOIN product_template_ck_featured_label_rel rel ON rel.label_id = l.id
         WHERE {name_expr} <> ''
        """
    )
    label_rows = cr.fetchall()
    tag_by_key = {}
    for key, label in label_rows:
        if not key or not label:
            continue
        cr.execute(
            f"""
            SELECT id FROM product_tag
             WHERE lower({tag_name_expr}) = %s
             ORDER BY id
             LIMIT 1
            """,
            (key,),
        )
        row = cr.fetchone()
        if row:
            tag_by_key[key] = row[0]
        else:
            cr.execute(
                """
                INSERT INTO product_tag (name, create_uid, write_uid, create_date, write_date)
                VALUES (%s::jsonb, 1, 1, NOW() AT TIME ZONE 'UTC', NOW() AT TIME ZONE 'UTC')
                RETURNING id
                """,
                (json.dumps({'fr_FR': label}),),
            )
            tag_by_key[key] = cr.fetchone()[0]

    cr.execute(
        f"""
        SELECT rel.product_tmpl_id, lower({name_expr}) AS key
          FROM product_template_ck_featured_label_rel rel
          JOIN dorevia_ck_product_label l ON l.id = rel.label_id
         WHERE {name_expr} <> ''
        """
    )
    for product_tmpl_id, key in cr.fetchall():
        tag_id = tag_by_key.get(key)
        if not tag_id:
            continue
        cr.execute(
            """
            SELECT 1
              FROM product_tag_product_template_rel
             WHERE product_template_id = %s
               AND product_tag_id = %s
            """,
            (product_tmpl_id, tag_id),
        )
        if not cr.fetchone():
            cr.execute(
                """
                INSERT INTO product_tag_product_template_rel
                    (product_template_id, product_tag_id)
                VALUES (%s, %s)
                """,
                (product_tmpl_id, tag_id),
            )
