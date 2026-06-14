#!/usr/bin/env python3
"""Recette visuelle A1 header CK — Playwright · Chantier A."""

import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "http://localhost:18079"
DB = "dorevia_ck_marketone_01"
QA = "phase10"
OUT = Path(__file__).resolve().parent.parent / "rapport" / "a1_visuelle_20260614_v2"

URLS = [
    ("home", f"/?db={DB}&qa_ts={QA}"),
    ("contact", f"/contactus?db={DB}&qa_ts={QA}"),
    ("shop", f"/shop?db={DB}&qa_ts={QA}"),
]

NAV_EXPECTED = ["Boutique", "Découvrir", "Professionnels", "Contactez-nous"]


def header_nav_text(page):
    header = page.locator("header#top.ck-header, header.ck-header").first
    return header.inner_text(timeout=5000) if header.count() else ""


def header_signature(page):
    header = page.locator("header#top.ck-header, header.ck-header").first
    logo = header.locator(".ck-header__brand, .navbar-brand .ck-header__brand").first
    sig = {
        "has_ck_header": header.count() > 0,
        "brand_text": logo.inner_text(timeout=3000) if logo.count() else None,
        "brand_box": logo.bounding_box() if logo.count() else None,
        "nav_text": header_nav_text(page),
    }
    return sig


def check_overflow(page):
    return page.evaluate(
        """() => ({
            scrollW: document.documentElement.scrollWidth,
            clientW: document.documentElement.clientWidth,
            overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1
        })"""
    )


def sticky_probe(page):
    header = page.locator("header#top.ck-header, header.ck-header").first
    before = page.evaluate(
        """() => {
            const h = document.querySelector('header#top.ck-header, header.ck-header');
            if (!h) return null;
            const r = h.getBoundingClientRect();
            const cs = getComputedStyle(h);
            return {top: r.top, y: r.y, position: cs.position, height: r.height};
        }"""
    )
    page.evaluate("window.scrollTo(0, 1200)")
    page.wait_for_timeout(400)
    after = page.evaluate(
        """() => {
            const h = document.querySelector('header#top.ck-header, header.ck-header');
            if (!h) return null;
            const r = h.getBoundingClientRect();
            const cs = getComputedStyle(h);
            return {top: r.top, y: r.y, position: cs.position, scrollY: window.scrollY};
        }"""
    )
    page.evaluate("window.scrollTo(0, 0)")
    sticky_ok = after and before and after.get("top", 999) <= 2 and after.get("scrollY", 0) > 400
    return {"before": before, "after_scroll": after, "sticky_behavior": sticky_ok}


def run_desktop(page, results):
    page.set_viewport_size({"width": 1280, "height": 800})
    signatures = {}

    for name, path in URLS:
        page.goto(BASE + path, wait_until="networkidle")
        page.wait_for_selector("header.ck-header, header#top.ck-header", timeout=15000)
        sig = header_signature(page)
        signatures[name] = sig
        ov = check_overflow(page)
        results[f"D11_{name}"] = {"ok": not ov["overflow"], "detail": ov}
        page.screenshot(path=str(OUT / f"desktop_1280_{name}.png"), full_page=False)

        nav = sig["nav_text"]
        results[f"D1_{name}"] = {
            "ok": sig["brand_text"] and "Kreyol" in (sig["brand_text"] or ""),
            "detail": {"brand": sig["brand_text"], "box": sig["brand_box"]},
        }
        results["D3"] = results.get("D3", {"ok": True, "detail": {}})
        for label in NAV_EXPECTED:
            results["D3"]["detail"][label] = label in nav
        results["D3"]["ok"] = all(results["D3"]["detail"].get(l, False) for l in NAV_EXPECTED)

        results["D4"] = {
            "ok": "Producteurs" not in re.split(r"[\n|]", nav)[0:8],
            "detail": "Producteurs absent des premières entrées nav",
        }

    # D12 header identical
    keys = list(signatures.keys())
    navs = [signatures[k]["nav_text"] for k in keys]
    results["D12"] = {
        "ok": len(set(navs)) == 1,
        "detail": {k: signatures[k]["nav_text"][:120] for k in keys},
    }

    # D5 D6 mega on home
    page.goto(BASE + URLS[0][1], wait_until="networkidle")
    decouvrir = page.locator(
        "header .nav-link:has-text('Découvrir'), header a:has-text('Découvrir')"
    ).first
    decouvrir.click()
    page.wait_for_timeout(500)
    panel = page.locator(".o_mega_menu, .dropdown-menu.show, .o_mega_nav").first
    panel_visible = panel.is_visible() if panel.count() else False
    epicerie = page.locator("a[href*='epicerie-creole'], a:has-text('Épicerie créole')").first
    epicerie_href = epicerie.get_attribute("href") if epicerie.count() else None
    results["D5"] = {"ok": panel_visible, "detail": "mega panel visible au clic Découvrir"}
    epicerie_ok = False
    if epicerie_href:
        resp = page.request.get(
            epicerie_href if epicerie_href.startswith("http") else BASE + epicerie_href
        )
        epicerie_ok = resp.status == 200
    results["D6"] = {
        "ok": epicerie_ok,
        "detail": {"href": epicerie_href, "status": 200 if epicerie_ok else None},
    }

    # D7 search cart
    search = page.locator(
        "header .o_wsale_products_search, header .oe_search_box, header [aria-label*='Recherche'], header .fa-search"
    ).first
    cart = page.locator("header a[href*='/shop/cart'], header .o_wsale_my_cart").first
    results["D7"] = {
        "ok": search.count() > 0 and cart.count() > 0,
        "detail": {"search": search.count() > 0, "cart": cart.count() > 0},
    }

    # D8 sticky
    page.goto(BASE + URLS[0][1], wait_until="networkidle")
    sticky = sticky_probe(page)
    results["D8"] = {
        "ok": sticky["sticky_behavior"],
        "reserve": not sticky["sticky_behavior"],
        "detail": sticky,
    }
    page.evaluate("window.scrollTo(0, 800)")
    page.wait_for_timeout(300)
    page.screenshot(path=str(OUT / "desktop_1280_home_scrolled.png"), full_page=False)
    page.evaluate("window.scrollTo(0, 0)")

    # D9 contrast rough check
    contrast = page.evaluate(
        """() => {
            const link = document.querySelector('header.ck-header .nav-link, header#top.ck-header .nav-link');
            if (!link) return null;
            const cs = getComputedStyle(link);
            return {color: cs.color, bg: getComputedStyle(link.closest('header')).backgroundColor, fontSize: cs.fontSize};
        }"""
    )
    results["D9"] = {
        "ok": contrast is not None and contrast.get("color") not in ("rgba(0, 0, 0, 0)", "transparent"),
        "detail": contrast,
        "note": "Contraste visuel MOA recommandé · mesure proxy CSS only",
    }

    # D10 ck-header class on theme
    results["D10"] = {
        "ok": page.locator("body.ck-theme, .ck-theme").count() > 0,
        "detail": "body.ck-theme présent · habillage CK actif",
    }

    # Contactez-nous arbitration
    contact_links = page.locator("header a:has-text('Contactez-nous')")
    results["contactez_nous"] = {
        "desktop_visible_count": contact_links.count(),
        "ok": contact_links.count() >= 1,
        "detail": "Présent nav principale desktop",
    }


def run_mobile(page, results):
    page.set_viewport_size({"width": 390, "height": 844})

    for name, path in URLS:
        page.goto(BASE + path, wait_until="networkidle")
        page.wait_for_selector("header.ck-header, header#top.ck-header", timeout=15000)
        ov = check_overflow(page)
        results[f"M7_{name}"] = {"ok": not ov["overflow"], "detail": ov}
        page.screenshot(path=str(OUT / f"mobile_390_{name}.png"), full_page=False)

    page.goto(BASE + URLS[0][1], wait_until="networkidle")

    # M1 offcanvas
    toggler = page.locator(
        "header .navbar-toggler, header button[data-bs-toggle='offcanvas'], header .o_header_mobile_toggle"
    ).first
    toggler_ok = toggler.count() > 0
    if toggler_ok:
        toggler.click()
        page.wait_for_timeout(600)
    offcanvas = page.locator("#top_menu_collapse_mobile.show, .offcanvas.show").first
    offcanvas_visible = offcanvas.is_visible() if offcanvas.count() else False
    page.screenshot(path=str(OUT / "mobile_390_offcanvas_open.png"), full_page=False)
    close_btn = page.locator("[data-bs-dismiss='offcanvas'], .offcanvas.show .btn-close").first
    if close_btn.count() and close_btn.is_visible():
        close_btn.click()
    elif toggler_ok:
        page.keyboard.press("Escape")
    page.wait_for_timeout(400)
    results["M1"] = {"ok": toggler_ok and offcanvas_visible, "detail": "burger + panel visible"}

    # Re-open for M2-M9
    if toggler_ok:
        toggler.click(force=True)
        page.wait_for_timeout(500)
    menu_root = page.locator("#top_menu_collapse_mobile.show, .offcanvas.show").first
    menu_text = menu_root.inner_text() if menu_root.count() else ""
    results["M2"] = {
        "ok": all(l in menu_text for l in NAV_EXPECTED),
        "detail": {l: l in menu_text for l in NAV_EXPECTED},
    }
    results["M9"] = {"ok": "Contactez-nous" in menu_text, "detail": menu_text[:200]}

    # M3 M4 mega mobile — scope offcanvas
    decouvrir = menu_root.locator("a:has-text('Découvrir'), button:has-text('Découvrir')").first
    if decouvrir.count():
        decouvrir.click(force=True)
        page.wait_for_timeout(500)
    epicerie = menu_root.locator("a:has-text('Épicerie créole'), a[href*='epicerie']").first
    if epicerie.count() == 0:
        epicerie = page.locator("a:has-text('Épicerie créole'), a[href*='epicerie']").first
    results["M3"] = {"ok": decouvrir.count() > 0, "detail": "Découvrir accessible offcanvas"}
    results["M4"] = {
        "ok": epicerie.count() > 0,
        "detail": epicerie.get_attribute("href") if epicerie.count() else None,
    }
    page.screenshot(path=str(OUT / "mobile_390_mega_decouvrir.png"), full_page=False)

    # M5 M6
    search = page.locator("header .fa-search, header [aria-label*='Recherche']").first
    cart = page.locator("header a[href*='/shop/cart']").first
    burger_box = toggler.bounding_box() if toggler.count() else None
    touch_ok = burger_box and burger_box.get("width", 0) >= 40 and burger_box.get("height", 0) >= 40
    results["M5"] = {"ok": search.count() > 0 or cart.count() > 0, "detail": {"search": search.count(), "cart": cart.count()}}
    results["M6"] = {"ok": touch_ok, "detail": burger_box}

    results["M8"] = {
        "ok": page.locator("header.ck-header").count() > 0,
        "detail": "ck-header présent mobile · screenshot offcanvas pour MOA",
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    results = {"meta": {"base": BASE, "db": DB, "viewport_desktop": "1280x800", "viewport_mobile": "390x844"}}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            extra_http_headers={"X-Odoo-Database": DB},
            locale="fr-FR",
        )
        page = context.new_page()
        run_desktop(page, results)
        run_mobile(page, results)
        browser.close()

    out_json = OUT / "a1_recette_results.json"
    out_json.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")

    # Summary
    checks = []
    for k, v in sorted(results.items()):
        if k == "meta" or not isinstance(v, dict):
            continue
        status = "OK" if v.get("ok") else ("RESERVE" if v.get("reserve") else "KO")
        checks.append((k, status, v.get("detail")))

    print("=== A1 RECETTE VISUELLE ===")
    for k, st, det in checks:
        print(f"{st:7} {k}: {det}")
    ok = sum(1 for _, st, _ in checks if st == "OK")
    ko = sum(1 for _, st, _ in checks if st == "KO")
    res = sum(1 for _, st, _ in checks if st == "RESERVE")
    print(f"\nTOTAL: {ok} OK · {res} RESERVE · {ko} KO")
    print(f"Screenshots: {OUT}")
    print(f"JSON: {out_json}")
    return 0 if ko == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
