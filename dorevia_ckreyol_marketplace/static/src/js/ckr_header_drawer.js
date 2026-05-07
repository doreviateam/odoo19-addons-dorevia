/** C-Kreyol : drawer menu mobile (body scroll, ARIA, fermeture lien / Escape). */
(function () {
    "use strict";

    /**
     * Hauteur du header CK → `--ckr-header-measured` sur :root (mobile fixed + hero immersif).
     * Toujours exécuté si le header existe, indépendamment du drawer.
     */
    function setupHeaderHeightCssVar() {
        var header = document.querySelector("header#top.ckr-header");
        if (!header) {
            document.documentElement.style.removeProperty("--ckr-header-measured");
            return;
        }

        function measure() {
            window.requestAnimationFrame(function () {
                var h = Math.round(header.getBoundingClientRect().height);
                if (!isFinite(h) || h < 32) {
                    document.documentElement.style.removeProperty("--ckr-header-measured");
                    return;
                }
                document.documentElement.style.setProperty("--ckr-header-measured", h + "px");
            });
        }

        if (document.fonts && document.fonts.ready) {
            document.fonts.ready.then(measure).catch(measure);
        } else {
            measure();
        }

        window.addEventListener("resize", measure, { passive: true });
        if (window.visualViewport) {
            window.visualViewport.addEventListener("resize", measure, { passive: true });
        }

        if (typeof ResizeObserver !== "undefined") {
            var ro = new ResizeObserver(measure);
            ro.observe(header);
        }
    }

    function syncDrawerUi(toggle, burger) {
        var on = toggle.checked;
        document.documentElement.classList.toggle("ckr-drawer-open", on);
        document.body.classList.toggle("ckr-drawer-open", on);
        if (burger) {
            burger.setAttribute("aria-expanded", on ? "true" : "false");
            burger.setAttribute("aria-label", on ? "Fermer le menu" : "Ouvrir le menu");
        }
    }

    function initUserMenu() {
        var menus = document.querySelectorAll("details.ckr-header__user-menu");
        if (!menus.length) {
            return;
        }
        document.addEventListener("click", function (ev) {
            menus.forEach(function (m) {
                if (!m.open) { return; }
                if (!m.contains(ev.target)) {
                    m.removeAttribute("open");
                }
            });
        });
        document.addEventListener("keydown", function (ev) {
            if (ev.key !== "Escape") { return; }
            menus.forEach(function (m) {
                if (m.open) {
                    m.removeAttribute("open");
                    var s = m.querySelector("summary");
                    if (s) { s.focus(); }
                }
            });
        });
        menus.forEach(function (m) {
            m.addEventListener("click", function (ev) {
                var a = ev.target.closest("a[href]");
                if (a) { m.removeAttribute("open"); }
            });
        });
    }

    function init() {
        setupHeaderHeightCssVar();
        initUserMenu();
        var toggle = document.getElementById("ckr_drawer_toggle");
        var burger = document.getElementById("ckr_drawer_burger");
        var drawerNav = document.querySelector(".ckr-drawer__nav");
        if (!toggle) {
            return;
        }

        var mqDesktop = window.matchMedia("(min-width: 992px)");

        function closeDrawerIfDesktop() {
            if (mqDesktop.matches && toggle.checked) {
                toggle.checked = false;
                syncDrawerUi(toggle, burger);
            }
        }

        toggle.addEventListener("change", function () {
            syncDrawerUi(toggle, burger);
        });

        if (drawerNav) {
            drawerNav.addEventListener("click", function (ev) {
                var a = ev.target.closest("a[href]");
                if (a) {
                    toggle.checked = false;
                    syncDrawerUi(toggle, burger);
                }
            });
        }

        document.addEventListener("keydown", function (ev) {
            if (ev.key === "Escape" && toggle.checked) {
                toggle.checked = false;
                syncDrawerUi(toggle, burger);
                if (burger) {
                    burger.focus();
                }
            }
        });

        syncDrawerUi(toggle, burger);
        closeDrawerIfDesktop();

        if (mqDesktop.addEventListener) {
            mqDesktop.addEventListener("change", closeDrawerIfDesktop);
        } else if (mqDesktop.addListener) {
            mqDesktop.addListener(closeDrawerIfDesktop);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
