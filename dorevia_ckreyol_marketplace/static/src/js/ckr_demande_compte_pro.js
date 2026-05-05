/** C-Kreyol : page demande compte pro — replier le formulaire principal à l’ouverture du bloc « Être rappelé ». */
(function () {
    "use strict";

    function initDemandeProCollapseSync() {
        var mainEl = document.getElementById("ckrDemandeProMainFormCollapse");
        var rappelEl = document.getElementById("ckrDemandeProRappelCollapse");
        if (!mainEl || !rappelEl || typeof bootstrap === "undefined") {
            return;
        }

        rappelEl.addEventListener("shown.bs.collapse", function () {
            bootstrap.Collapse.getOrCreateInstance(mainEl, { toggle: false }).hide();
        });

        rappelEl.addEventListener("hidden.bs.collapse", function () {
            bootstrap.Collapse.getOrCreateInstance(mainEl, { toggle: false }).show();
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initDemandeProCollapseSync);
    } else {
        initDemandeProCollapseSync();
    }
})();
