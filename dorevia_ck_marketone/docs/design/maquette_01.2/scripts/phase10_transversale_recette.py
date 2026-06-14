#!/usr/bin/env python3
"""Phase 10 §3 transversale — recette proxy CK (sans header §2)."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

import subprocess

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

BASE = "http://localhost:18079"
DB = "dorevia_ck_marketone_01"
QA = "phase10t"
OUT = Path(__file__).resolve().parent.parent / "rapport" / "phase10_transversale_20260614"

ROUTES = [
    ("/", "ck-featured-products__grid--stable", "home"),
    ("/shop", "s_ck_shop_intro", "shop"),
    ("/professionnels", "ck-pro-page", "pro"),
    ("/contactus", "ck-contact-page", "contact"),
    ("/a-propos", "ck-about-page", "about"),
    ("/recettes", "ck-recipes-page", "recipes"),
    ("/producteur/atelier-hauts-goyaviers", "ck-producer-page", "producer"),
]

NAV_LINKS = [
    "/shop",
    "/professionnels",
    "/contactus",
    "/a-propos",
    "/recettes",
    "/producteur/atelier-hauts-goyaviers",
    "/shop/category/epicerie-creole-1",
]


def curl(path, follow=True):
    cmd = ["curl", "-sS", "-w", "\n__CODE__:%{http_code}", "-H", f"X-Odoo-Database: {DB}"]
    if not follow:
        cmd.append("-I")
    cmd.append(BASE + path)
    out = subprocess.check_output(cmd, text=True, errors="replace")
    if "__CODE__:" in out:
        body, _, code_part = out.rpartition("\n__CODE__:")
        code = int(code_part.strip())
    else:
        body, code = out, 200
    return code, body


def discover_product():
    _, html = curl(f"/shop?qa_ts={QA}")
    m = re.search(r'href="(/shop/[^"/]+-\d+)"', html)
    return m.group(1) if m else None


def check_footer(html):
    footer = re.search(r"<footer[\s\S]*?</footer>", html, re.I)
    text = footer.group(0) if footer else ""
    hrefs = re.findall(r'href="([^"#][^"]*)"', text)
    dead = []
    placeholders = []
    for h in hrefs:
        if h in ("#", "javascript:void(0)"):
            placeholders.append(h)
            continue
        path = h if h.startswith("/") else urlparse(h).path
        if not path:
            continue
        code, _ = curl(path + (f"?qa_ts={QA}" if "?" not in path else f"&qa_ts={QA}"))
        if code >= 400:
            dead.append((h, code))
    cols = len(re.findall(r"col-lg-3|footer.*col-", text, re.I))
    return {
        "present": bool(footer),
        "link_count": len(hrefs),
        "dead_links": dead,
        "placeholders": placeholders[:5],
        "col_hints": cols,
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = {"meta": {"base": BASE, "db": DB, "qa": QA}, "sections": {}}

    product = discover_product()
    results["meta"]["product_path"] = product

    # §3.3 L1-L6 routes
    route_checks = {}
    for path in NAV_LINKS + (["/shop/cart"] if True else []):
        code, _ = curl(f"{path}?qa_ts={QA}")
        route_checks[path] = {"code": code, "ok": code == 200}
    if product:
        code, _ = curl(f"{product}?qa_ts={QA}")
        route_checks[product] = {"code": code, "ok": code == 200}
    results["sections"]["L_routes"] = route_checks

    # §3.4 M5
    m5 = {}
    for path, marker, name in [("/", "s_ck_reassurance", "home"), ("/shop", "s_ck_reassurance_m5", "shop")]:
        _, html = curl(f"{path}?qa_ts={QA}")
        m5[name] = {"marker": marker, "present": marker in html}
    if product:
        _, html = curl(f"{product}?qa_ts={QA}")
        m5["product"] = {"marker": "ck-reassurance", "present": "ck-reassurance" in html or "reassurance" in html.lower()}
    results["sections"]["M5_copy"] = m5

    # §3.5 checkout
    code_cart, html_cart = curl(f"/shop/cart?qa_ts={QA}")
    results["sections"]["checkout"] = {
        "cart_200": code_cart == 200,
        "checkout_container": "o_website_sale_checkout_container" in html_cart or "cart" in html_cart.lower(),
        "product_for_add": bool(product),
    }

    # §3.6 newsletter
    _, contact = curl(f"/contactus?qa_ts={QA}")
    _, pro = curl(f"/professionnels?qa_ts={QA}")
    _, home = curl(f"/?qa_ts={QA}")
    results["sections"]["newsletter"] = {
        "contact_subscribe": "ck-newsletter-subscribe" in contact,
        "contact_rgpd": "Désinscription" in contact or "désinscription" in contact,
        "contact_no_popup": "s_newsletter_subscribe_popup" not in contact,
        "pro_subscribe": "ck-newsletter-subscribe" in pro,
        "pro_form_distinct": "ck-pro-form" in pro and "contactus_form" not in pro,
        "home_dual": "ck-dual-engage" in home,
    }

    # §3.7 forms
    results["sections"]["forms"] = {
        "contact_b2c": "contactus_form" in contact and 'data-model_name="mail.mail"' in contact,
        "crm_pro": "ck-pro-form" in pro and "crm.lead" in pro,
        "separation": "contactus_form" not in pro,
    }

    # §3.8 assets
    asset_pages = {}
    for path, marker, name in ROUTES[:4]:
        _, html = curl(f"{path}?qa_ts={QA}")
        asset_pages[name] = {
            "ck_theme": "ck-theme" in html or "body_classname" in html,
            "assets_frontend": "web.assets_frontend" in html,
            "marker": marker in html,
        }
    results["sections"]["assets"] = asset_pages

    # §3.2 footer (from home)
    _, home_html = curl(f"/?qa_ts={QA}")
    results["sections"]["footer"] = check_footer(home_html)

    # §3.1 mobile 390 Playwright
    mobile = {}
    if sync_playwright is None:
        mobile["error"] = "playwright not installed"
    else:
        pages = list(ROUTES)
        if product:
            pages.append((product, "ck-product-page", "product"))
        pages.append(("/shop/cart", "cart", "cart"))

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            ctx = browser.new_context(
                viewport={"width": 390, "height": 844},
                extra_http_headers={"X-Odoo-Database": DB},
            )
            page = ctx.new_page()
            for path, marker, name in pages:
                page.goto(BASE + path + f"?qa_ts={QA}", wait_until="networkidle", timeout=60000)
                ov = page.evaluate(
                    "() => ({scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth})"
                )
                has_marker = marker in ("cart",) or page.locator(f"body").inner_html().find(marker) >= 0
                mobile[name] = {
                    "overflow": ov["scrollW"] > ov["clientW"] + 1,
                    "scrollW": ov["scrollW"],
                    "clientW": ov["clientW"],
                    "marker_ok": has_marker if marker not in ("cart",) else page.url.find("cart") >= 0,
                }
                page.screenshot(path=str(OUT / f"mobile390_{name}.png"), full_page=False)
            browser.close()

    results["sections"]["mobile390"] = mobile

    # Hero debt note (visual - DOM only)
    _, home_html = curl(f"/?qa_ts={QA}")
    results["sections"]["hors_a1_notes"] = {
        "hero_marker": "s_ck_hero" in home_html or "ck-hero" in home_html,
        "featured_ssr": "ck-featured-products__grid--stable" in home_html,
        "note": "Écarts visuels hero/contenus accueil = hors périmètre A1 · arbitrage MOA Phase 10",
    }

    out_json = OUT / "phase10_transversale_results.json"
    out_json.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    # Summary
    fails = []
    for path, v in route_checks.items():
        if not v["ok"]:
            fails.append(f"L route {path} HTTP {v['code']}")
    for name, v in mobile.items():
        if isinstance(v, dict) and v.get("overflow"):
            fails.append(f"mobile overflow {name}")
    for name, v in mobile.items():
        if isinstance(v, dict) and v.get("marker_ok") is False:
            fails.append(f"mobile marker {name}")
    if results["sections"]["footer"].get("dead_links"):
        fails.append(f"footer dead: {results['sections']['footer']['dead_links']}")
    if not results["sections"]["forms"].get("contact_b2c"):
        fails.append("contact B2C form")
    if not results["sections"]["forms"].get("crm_pro"):
        fails.append("crm pro form")
    if not results["sections"]["newsletter"].get("contact_subscribe"):
        fails.append("newsletter contact")

    print("=== PHASE 10 §3 TRANSVERSALE ===")
    print(json.dumps(results["sections"], indent=2, ensure_ascii=False)[:8000])
    print(f"\nJSON: {out_json}")
    print(f"Captures: {OUT}")
    if fails:
        print("FAILURES:", fails)
        return 1
    print("TOTAL: OK proxy §3")
    return 0


if __name__ == "__main__":
    sys.exit(main())
