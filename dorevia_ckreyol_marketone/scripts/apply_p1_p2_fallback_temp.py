#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P1/P2 MOA — retrait temporaire image_shop_tile + fallback image_1920."""

ACTIONS = {
    154: "FALLBACK_TEMP_P1_MOA — retrait image_shop_tile · effet rectangle interne · fallback image_1920",
    156: "FALLBACK_TEMP_P2_MOA — fallback image_1920 · NEEDS_REVIEW_SOURCE · effet rectangle interne",
    471: "FALLBACK_TEMP_P2_MOA — fallback image_1920 · NEEDS_REVIEW_SOURCE · effet rectangle interne",
}


def apply(env):
    Product = env["product.template"].sudo()
    print("BEFORE")
    for pid in ACTIONS:
        p = Product.browse(pid)
        print(
            f"{pid}|{p.name}|tile={bool(p.image_shop_tile)}|"
            f"use={p.marketone_use_shop_tile_on_grid()}|status={p.shop_tile_status}|"
            f"1920={bool(p.image_1920)}"
        )
    for pid, note in ACTIONS.items():
        p = Product.browse(pid)
        if not p.exists():
            raise RuntimeError(f"product.template {pid} introuvable")
        p.write(
            {
                "image_shop_tile": False,
                "shop_tile_status": "pending_review",
                "shop_tile_moa_note": note,
            }
        )
    print("AFTER")
    for pid in ACTIONS:
        p = Product.browse(pid)
        print(
            f"{pid}|{p.name}|tile={bool(p.image_shop_tile)}|"
            f"use={p.marketone_use_shop_tile_on_grid()}|status={p.shop_tile_status}|"
            f"1920={bool(p.image_1920)}"
        )
    total = Product.search_count([("image_shop_tile", "!=", False)])
    flag = env["ir.config_parameter"].sudo().get_param("marketone.shop_tile_enabled")
    print(f"TOTAL_WITH_TILE|{total}")
    print(f"FLAG|{flag}")
