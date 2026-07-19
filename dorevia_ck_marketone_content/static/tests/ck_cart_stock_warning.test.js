/** @odoo-module **/

import { describe, expect, test } from '@odoo/hoot';
import { animationFrame } from '@odoo/hoot-dom';
import { onRpc, patchWithCleanup } from '@web/../tests/web_test_helpers';
import { setupInteractionWhiteList, startInteractions } from '@web/../tests/public/helpers';
import wSaleUtils from '@website_sale/js/website_sale_utils';
import {
    assertShowWarningApi,
    setCartNotificationServiceForTests,
    showCartStockWarningToast,
} from '@dorevia_ck_marketone_content/js/ck_cart_stock_warning';

describe.current.tags('interaction_dev');

setupInteractionWhiteList(['website_sale.cart_line']);

function cartProductHtml(lineId = 1, productId = 10) {
    return `
        <div class="oe_website_sale">
            <div id="shop_cart">
                <div class="o_cart_product">
                    <div class="css_quantity input-group">
                        <input type="text" class="js_quantity form-control"
                            value="5"
                            data-line-id="${lineId}"
                            data-product-id="${productId}"
                            data-max="100"/>
                        <a href="#" class="btn"><i class="oi oi-plus"></i></a>
                    </div>
                    <a href="#" class="js_delete_product">remove</a>
                </div>
            </div>
        </div>
    `;
}

test('assertShowWarningApi accepts current website_sale showWarning', () => {
    expect(() => assertShowWarningApi()).not.toThrow();
    expect(typeof wSaleUtils.showWarning).toBe('function');
});

test('showCartStockWarningToast emits exactly one toast and skips empty message', () => {
    const calls = [];
    const fakeService = {
        add(title, props) {
            calls.push({ title, props });
        },
    };

    showCartStockWarningToast(fakeService, '');
    expect(calls).toEqual([]);

    showCartStockWarningToast(fakeService, 'Only 2 left');
    expect(calls).toHaveLength(1);
    expect(calls[0].props).toEqual({ warning: 'Only 2 left' });
});

test('showCartStockWarningToast fails closed without cartNotificationService', () => {
    expect(() => showCartStockWarningToast(null, 'warn')).toThrow(
        /cartNotificationService unavailable/
    );
});

test('assertShowWarningApi fails when upstream API disappears', () => {
    const original = wSaleUtils.showWarning;
    try {
        wSaleUtils.showWarning = undefined;
        expect(() => assertShowWarningApi()).toThrow(/showWarning is missing/);
    } finally {
        wSaleUtils.showWarning = original;
    }
});

test('patched showWarning emits toast and never creates #data_warning banner', () => {
    const calls = [];
    setCartNotificationServiceForTests({
        add(title, props) {
            calls.push({ title, props });
        },
    });
    document.body.innerHTML = '<div class="oe_website_sale"></div>';

    wSaleUtils.showWarning('Stock limited');
    expect(calls).toHaveLength(1);
    expect(calls[0].props).toEqual({ warning: 'Stock limited' });
    expect(document.querySelectorAll('#data_warning')).toHaveLength(0);

    wSaleUtils.showWarning('');
    expect(calls).toHaveLength(1);
});

test('concurrent showWarning calls emit two toasts and zero banners', async () => {
    const calls = [];
    setCartNotificationServiceForTests({
        add(title, props) {
            calls.push({ title, props });
        },
    });
    document.body.innerHTML = '<div class="oe_website_sale"></div>';

    await Promise.all([
        Promise.resolve(wSaleUtils.showWarning('A')),
        Promise.resolve(wSaleUtils.showWarning('B')),
    ]);

    expect(calls).toHaveLength(2);
    expect(calls.map((c) => c.props.warning).sort()).toEqual(['A', 'B']);
    expect(document.querySelectorAll('#data_warning')).toHaveLength(0);
    expect(typeof wSaleUtils.showWarning).toBe('function');
});

test('CartLine._changeQuantity with data.warning triggers one toast via standard path', async () => {
    const toastCalls = [];
    let rpcCalls = 0;

    onRpc('/shop/cart/update', () => {
        rpcCalls += 1;
        return {
            cart_quantity: 2,
            quantity: 2,
            amount: 10,
            minor_amount: 1000,
            warning: 'Only 2 available',
            notification_info: {},
        };
    });

    patchWithCleanup(wSaleUtils, {
        updateCartNavBar() {},
        updateQuickReorderSidebar() {},
    });

    const { core } = await startInteractions(cartProductHtml());
    expect(core.interactions.length).toBeGreaterThan(0);

    const cartNotificationService = core.env.services.cartNotificationService;
    expect(!!cartNotificationService).toBe(true);
    patchWithCleanup(cartNotificationService, {
        add(title, props) {
            toastCalls.push({ title, props });
        },
    });
    setCartNotificationServiceForTests(cartNotificationService);

    const interaction = core.interactions.find((i) => i.el.classList.contains('o_cart_product'));
    expect(!!interaction).toBe(true);

    const input = interaction.el.querySelector('input.js_quantity');
    input.value = '9';
    await interaction.interaction._changeQuantity(input);
    await animationFrame();

    expect(rpcCalls).toBe(1);
    expect(toastCalls).toHaveLength(1);
    expect(toastCalls[0].props).toEqual({ warning: 'Only 2 available' });
    expect(document.querySelectorAll('#data_warning')).toHaveLength(0);
});

test('CartLine._changeQuantity without warning keeps standard path and emits no toast', async () => {
    const toastCalls = [];
    let rpcCalls = 0;

    onRpc('/shop/cart/update', () => {
        rpcCalls += 1;
        return {
            cart_quantity: 3,
            quantity: 3,
            amount: 15,
            minor_amount: 1500,
            warning: '',
            notification_info: {},
        };
    });

    patchWithCleanup(wSaleUtils, {
        updateCartNavBar() {},
        updateQuickReorderSidebar() {},
    });

    const { core } = await startInteractions(cartProductHtml(2, 20));
    const cartNotificationService = core.env.services.cartNotificationService;
    patchWithCleanup(cartNotificationService, {
        add(title, props) {
            toastCalls.push({ title, props });
        },
    });
    setCartNotificationServiceForTests(cartNotificationService);

    const interaction = core.interactions.find((i) => i.el.classList.contains('o_cart_product'));
    const input = interaction.el.querySelector('input.js_quantity');
    input.value = '3';
    await interaction.interaction._changeQuantity(input);
    await animationFrame();

    expect(rpcCalls).toBe(1);
    expect(toastCalls).toHaveLength(0);
    expect(document.querySelectorAll('#data_warning')).toHaveLength(0);
});
