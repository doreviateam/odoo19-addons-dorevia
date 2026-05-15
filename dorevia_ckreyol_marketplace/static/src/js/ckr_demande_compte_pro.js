/** C-Kreyol : page demande compte pro — replier le formulaire principal à l’ouverture du bloc « Être rappelé ».
 *  Ne dépend pas de ``window.bootstrap`` (souvent absent du bundle Website Odoo) : on synchronise la classe ``show``
 *  du collapse rappel avec celle du collapse du formulaire principal.
 */
(function () {
    "use strict";

    /** Pendant l’animation Bootstrap, ``collapsing`` est présent sans ``show`` encore. */
    function rappelEstOuvertOuEnCours(el) {
        return el.classList.contains("show") || el.classList.contains("collapsing");
    }

    function syncMainFromRappel(mainEl, rappelEl) {
        if (rappelEstOuvertOuEnCours(rappelEl)) {
            mainEl.classList.remove("show");
        } else {
            mainEl.classList.add("show");
        }
    }

    function initDemandeProCollapseSync() {
        var mainEl = document.getElementById("ckrDemandeProMainFormCollapse");
        var rappelEl = document.getElementById("ckrDemandeProRappelCollapse");
        if (!mainEl || !rappelEl) {
            return;
        }

        syncMainFromRappel(mainEl, rappelEl);

        var mo = new MutationObserver(function () {
            syncMainFromRappel(mainEl, rappelEl);
        });
        mo.observe(rappelEl, {
            attributes: true,
            attributeFilter: ["class"],
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initDemandeProCollapseSync);
    } else {
        initDemandeProCollapseSync();
    }
})();
