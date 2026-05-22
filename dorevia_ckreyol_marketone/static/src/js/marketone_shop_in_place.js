/** UX-4 — Boutique continue : extensions légères du standard Odoo (shop-in-place). */
odoo.define("dorevia_ckreyol_marketone.shop_in_place", function (require) {
    "use strict";

    const publicWidget = require("web.public.widget");

    // Garantit le chargement du widget wishlist standard avant include.
    require("website_sale_wishlist.wishlist");

    publicWidget.registry.ProductWishlist.include({
        /**
         * @override
         */
        start: function () {
            const def = this._super.apply(this, arguments);
            this._marketoneSyncGridWishlistCards();
            return def;
        },

        /**
         * @override
         */
        _onClickAddWish: function (ev) {
            const $el = $(ev.currentTarget);
            if (!$el.hasClass("marketone-shop-card-wishlist")) {
                return this._super.apply(this, arguments);
            }
            ev.preventDefault();
            ev.stopPropagation();
            return this._marketoneToggleGridWishlist($el);
        },

        /**
         * @override — ne pas désactiver le cœur grille après ajout (toggle UX-4).
         */
        _addNewProducts: function ($el) {
            if (!$el.hasClass("marketone-shop-card-wishlist")) {
                return this._super.apply(this, arguments);
            }
            const self = this;
            let productID = $el.data("product-product-id");
            const $form = $el.closest("form");
            let templateId = $form.find(".product_template_id").val();
            if (!templateId) {
                templateId = $el.data("product-template-id");
            }
            $el.prop("disabled", true).addClass("disabled");
            const productReady = this.selectOrCreateProduct(
                $el.closest("form"),
                productID,
                templateId,
                false
            );
            return productReady
                .then(function (productId) {
                    productId = parseInt(productId, 10);
                    if (!productId || _.contains(self.wishlistProductIDs, productId)) {
                        $el.prop("disabled", false).removeClass("disabled");
                        return;
                    }
                    return self
                        ._rpc({
                            route: "/shop/wishlist/add",
                            params: { product_id: productId },
                        })
                        .then(function () {
                            const $navButton = $("header .o_wsale_my_wish").first();
                            self.wishlistProductIDs.push(productId);
                            sessionStorage.setItem(
                                "website_sale_wishlist_product_ids",
                                JSON.stringify(self.wishlistProductIDs)
                            );
                            self._updateWishlistView();
                            const wSaleUtils = require("website_sale.utils");
                            wSaleUtils.animateClone(
                                $navButton,
                                $el.closest("form"),
                                25,
                                40
                            );
                            self._marketoneSetGridWishlistState($el, true);
                        })
                        .guardedCatch(function () {
                            $el.prop("disabled", false).removeClass("disabled");
                        })
                        .finally(function () {
                            $el.prop("disabled", false).removeClass("disabled");
                        });
                })
                .guardedCatch(function () {
                    $el.prop("disabled", false).removeClass("disabled");
                });
        },

        /**
         * @private
         */
        _marketoneToggleGridWishlist: function ($el) {
            const self = this;
            const productID = parseInt($el.data("product-product-id"), 10);
            if (!productID) {
                return Promise.resolve();
            }
            if (_.contains(self.wishlistProductIDs, productID)) {
                $el.prop("disabled", true).addClass("disabled");
                return this._rpc({
                    route: "/shop/wishlist/remove_by_product",
                    params: { product_id: productID },
                })
                    .then(function () {
                        self.wishlistProductIDs = _.without(
                            self.wishlistProductIDs,
                            productID
                        );
                        sessionStorage.setItem(
                            "website_sale_wishlist_product_ids",
                            JSON.stringify(self.wishlistProductIDs)
                        );
                        self._updateWishlistView();
                        self._marketoneSetGridWishlistState($el, false);
                    })
                    .guardedCatch(function () {
                        // noop — état UI inchangé
                    })
                    .finally(function () {
                        $el.prop("disabled", false).removeClass("disabled");
                    });
            }
            return this._addNewProducts($el);
        },

        /**
         * @private
         */
        _marketoneSetGridWishlistState: function ($el, inWishlist) {
            const $card = $el.closest(".oe_product_cart");
            const $icon = $el.find(".fa").first();
            $el.toggleClass("o_in_wishlist is-active", inWishlist);
            $el.attr("aria-pressed", inWishlist ? "true" : "false");
            $el.attr(
                "aria-label",
                inWishlist ? "Retirer de la liste" : "Ajouter à la liste"
            );
            $el.attr(
                "title",
                inWishlist ? "Retirer de la liste" : "Ajouter à la liste"
            );
            if ($icon.length) {
                $icon
                    .toggleClass("fa-heart", inWishlist)
                    .toggleClass("fa-heart-o", !inWishlist);
            }
            $card.toggleClass("marketone-shop-card--in-wishlist", inWishlist);
        },

        /**
         * @private
         */
        _marketoneSyncGridWishlistCards: function () {
            const self = this;
            this.$(".marketone-shop-card-wishlist").each(function () {
                const $el = $(this);
                const productID = parseInt($el.data("product-product-id"), 10);
                if (!productID) {
                    return;
                }
                const inWishlist = _.contains(self.wishlistProductIDs, productID);
                self._marketoneSetGridWishlistState($el, inWishlist);
            });
        },
    });
});
