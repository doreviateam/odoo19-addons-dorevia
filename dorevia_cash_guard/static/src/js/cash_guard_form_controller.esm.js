/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

const GUARD_MODEL = "dorevia.cash.guard";

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);
        this.orm = useService("orm");
        onMounted(async () => {
            /* Attendre un tour de microtask : le record racine n’est pas toujours prêt au premier paint. */
            await Promise.resolve();
            await this._doreviaCashGuardRefreshOnOpen();
        });
    },

    /**
     * Document vivant : au chargement du formulaire, recalcul serveur puis rechargement
     * des champs (soldes, grille, synthèse) sans réalignement de période.
     */
    async _doreviaCashGuardRefreshOnOpen() {
        const resModel =
            this.props?.resModel ||
            this.props?.action?.res_model ||
            this.model?.config?.resModel ||
            this.env?.config?.resModel;
        if (resModel !== GUARD_MODEL) {
            return;
        }
        const root = this.model?.root;
        if (!root || root.isNew || !root.resId) {
            return;
        }
        try {
            await this.orm.call(GUARD_MODEL, "action_recompute_projection", [[root.resId]]);
            await root.load();
        } catch {
            /* ne pas bloquer l’ouverture si erreur réseau ou droits */
        }
    },
});
