/** @odoo-module **/

import { Interaction } from '@web/public/interaction';
import { registry } from '@web/core/registry';

/**
 * Fiche produit CK V1.1 — navigation ancres sticky + état actif au scroll.
 */
export class CkProductPageAnchors extends Interaction {
    static selector = '.ck-product-page';

    start() {
        this._initAnchorNavigation();
    }

    _initAnchorNavigation() {
        const nav = this.el.querySelector('.ck-product-page__anchor-nav');
        if (!nav) {
            return;
        }
        const links = [...nav.querySelectorAll('.ck-product-page__anchor-link')];
        const sections = links
            .map((link) => {
                const href = link.getAttribute('href') || '';
                if (!href.startsWith('#')) {
                    return null;
                }
                return this.el.querySelector(href);
            })
            .filter(Boolean);
        if (!sections.length) {
            return;
        }

        const setActive = (activeId) => {
            for (const link of links) {
                const href = link.getAttribute('href') || '';
                link.classList.toggle('is-active', href === `#${activeId}`);
            }
        };

        const observer = new IntersectionObserver(
            (entries) => {
                const visible = entries
                    .filter((entry) => entry.isIntersecting)
                    .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
                if (visible.length) {
                    setActive(visible[0].target.id);
                }
            },
            {
                root: null,
                rootMargin: '-35% 0px -55% 0px',
                threshold: [0, 0.15, 0.35, 0.55],
            },
        );
        for (const section of sections) {
            observer.observe(section);
        }
        setActive(sections[0].id);
    }
}

registry
    .category('public.interactions')
    .add('dorevia_ck_marketone_content.product_page_anchors', CkProductPageAnchors);
