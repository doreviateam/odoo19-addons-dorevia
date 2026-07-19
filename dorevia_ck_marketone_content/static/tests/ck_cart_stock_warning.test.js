/** @odoo-module **/

import { describe, expect, test } from '@odoo/hoot';
import wSaleUtils from '@website_sale/js/website_sale_utils';
import {
    assertShowWarningApi,
    showCartStockWarningToast,
} from '@dorevia_ck_marketone_content/js/ck_cart_stock_warning';

describe.current.tags('interaction_dev');

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
