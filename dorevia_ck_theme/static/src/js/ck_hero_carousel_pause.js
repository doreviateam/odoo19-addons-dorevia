/** @odoo-module **/

import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";

/**
 * Bouton pause/lecture accessible (clavier + tactile) pour le carrousel Hero.
 * data-bs-pause="hover" seul ne couvre pas WCAG 2.2.2 (Pause, Stop, Hide) :
 * un <button> natif assure le focus clavier et l'activation tactile sans JS
 * supplémentaire, ce module ne fait que relayer l'état vers le carrousel Bootstrap.
 */
export class CkHeroCarouselPause extends Interaction {
    static selector = ".s_ck_hero .ck-hero__visual-carousel";
    dynamicContent = {
        ".ck-hero__visual-pause": {
            "t-on-click": this.onToggle,
            "t-att-aria-pressed": () => String(this.paused),
            "t-att-aria-label": () =>
                this.paused
                    ? "Reprendre le défilement automatique des visuels"
                    : "Mettre en pause le défilement automatique des visuels",
        },
        ".ck-hero__visual-pause .fa": {
            "t-att-class": () => ({
                "fa-play": this.paused,
                "fa-pause": !this.paused,
            }),
        },
    };

    setup() {
        this.paused = false;
    }

    onToggle() {
        const carousel = window.Carousel.getOrCreateInstance(this.el);
        if (this.paused) {
            carousel.cycle();
        } else {
            carousel.pause();
        }
        this.paused = !this.paused;
    }
}

registry
    .category("public.interactions")
    .add("dorevia_ck_theme.ck_hero_carousel_pause", CkHeroCarouselPause);
