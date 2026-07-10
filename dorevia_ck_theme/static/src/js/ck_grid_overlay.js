/** @odoo-module **/
/**
 * Overlay grille CK — chargé uniquement sur hôtes dev/pré-prod (voir website_layout.xml).
 * Le script n'est pas dans web.assets_frontend : absent du bundle production.
 */
(function () {
    "use strict";

    function setGrid(on) {
        document.body.classList.toggle("ck-grid-on", on);
        var btn = document.getElementById("ckGridToggle");
        if (btn) {
            btn.setAttribute("aria-pressed", on ? "true" : "false");
            var lbl = btn.querySelector(".ck-grid-toggle__lbl");
            if (lbl) {
                lbl.textContent = on ? "Masquer grille" : "Afficher grille";
            }
        }
    }

    function populateGuides() {
        var cols = getComputedStyle(document.documentElement)
            .getPropertyValue("--ck-grid-cols")
            .trim() || "12";
        var n = parseInt(cols, 10);
        document.querySelectorAll(".ck-guides .ck-guides__cols").forEach(function (host) {
            if (host.childElementCount >= n) {
                return;
            }
            host.textContent = "";
            for (var i = 1; i <= n; i++) {
                var c = document.createElement("div");
                c.className = "ck-guides__col";
                var s = document.createElement("span");
                s.textContent = String(i);
                c.appendChild(s);
                host.appendChild(c);
            }
        });
    }

    function opticalAlign() {
        var sel = ".ck-grid-poc .ck-reassurance__title";
        var cvs = document.createElement("canvas");
        var ctx = cvs.getContext("2d");
        if (!ctx) {
            return;
        }
        document.querySelectorAll(sel).forEach(function (el) {
            el.style.marginLeft = "0px";
            var cs = getComputedStyle(el);
            var ch = (el.textContent || "").trim().charAt(0);
            if (!ch) {
                return;
            }
            if (cs.textTransform === "uppercase") {
                ch = ch.toUpperCase();
            }
            ctx.font = cs.fontStyle + " " + cs.fontWeight + " " + cs.fontSize + " " + cs.fontFamily;
            ctx.textAlign = "left";
            var abl = ctx.measureText(ch).actualBoundingBoxLeft;
            if (isFinite(abl)) {
                el.style.marginLeft = abl.toFixed(2) + "px";
            }
        });
    }

    function init() {
        if (!document.body.classList.contains("ck-theme")) {
            return;
        }
        document.body.classList.add("ck-grid-dev");

        if (!document.getElementById("ckGridToggle")) {
            var btn = document.createElement("button");
            btn.type = "button";
            btn.id = "ckGridToggle";
            btn.className = "ck-grid-toggle";
            btn.setAttribute("aria-pressed", "false");
            btn.innerHTML =
                '<span class="ck-grid-toggle__dot" aria-hidden="true"></span>' +
                '<span class="ck-grid-toggle__lbl">Afficher grille</span>';
            document.body.appendChild(btn);
            btn.addEventListener("click", function () {
                setGrid(!document.body.classList.contains("ck-grid-on"));
            });
        }

        document.addEventListener("keydown", function (e) {
            if (
                (e.key === "g" || e.key === "G") &&
                !e.metaKey &&
                !e.ctrlKey &&
                !e.altKey
            ) {
                setGrid(!document.body.classList.contains("ck-grid-on"));
            }
        });

        populateGuides();

        function runOptical() {
            opticalAlign();
        }
        if (document.fonts && document.fonts.ready) {
            document.fonts.ready.then(runOptical);
        }
        runOptical();
        var t;
        window.addEventListener("resize", function () {
            clearTimeout(t);
            t = setTimeout(runOptical, 120);
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
