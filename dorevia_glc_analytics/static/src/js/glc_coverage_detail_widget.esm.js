/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { formatMonetary } from "@web/views/fields/formatters";

const STORAGE_KEY_PAID_ONLY = "glc_cockpit_detail_paid_only";

const NUMERIC_FIELDS = [
    "revenue_realized",
    "payroll_realized",
    "expense_realized",
];

export const DETAIL_FAMILIES = [
    {
        label: "Ressources",
        cssStart: "o_glc_family_recettes",
        cssEnd: "o_glc_family_recettes_end",
        realizedKey: "revenue_realized",
        valueType: "amount",
    },
    {
        label: "Cumul RH",
        cssStart: "o_glc_family_payroll",
        cssEnd: "o_glc_family_payroll_end",
        realizedKey: "payroll_realized",
        valueType: "amount",
    },
    {
        label: "Dépenses",
        cssStart: "o_glc_family_expense",
        cssEnd: "o_glc_family_expense_end",
        realizedKey: "expense_realized",
        valueType: "amount",
    },
    {
        label: "Solde",
        cssStart: "o_glc_family_performance",
        cssEnd: "o_glc_family_performance",
        realizedKey: "performance_realized",
        valueType: "performance",
    },
];

export function applyPaidDisplayMode(data, paidOnly) {
    if (!paidOnly) {
        return {
            ...data,
            ...computePerformanceAmounts(data),
        };
    }
    const mapped = {
        ...data,
        revenue_realized: data.revenue_realized_paid || 0,
        payroll_realized: data.payroll_realized_paid || 0,
        expense_realized: data.expense_realized_paid || 0,
    };
    return {
        ...mapped,
        ...computePerformanceAmounts(mapped),
    };
}

export function computePerformanceAmounts(data) {
    const performance_realized =
        (data.revenue_realized || 0) -
        (data.payroll_realized || 0) -
        (data.expense_realized || 0);
    return { performance_realized };
}

/** Retire le préfixe [CODE] d'un libellé analytique Odoo. */
export function stripAnalyticCodePrefix(label) {
    if (!label) {
        return "";
    }
    const match = String(label).match(/^\[([^\]]+)\]\s*(.*)$/);
    if (!match) {
        return String(label).trim();
    }
    const rest = match[2].trim();
    return rest || String(label).trim();
}

/** Extrait le code analytique depuis le champ dédié ou le libellé legacy. */
export function analyticCodeFromLine(line) {
    if (line.analytic_code) {
        return line.analytic_code;
    }
    const match = (line.activity_label || "").match(/^\[([^\]]+)\]/);
    return match ? match[1] : "";
}

/** Libellé MOA : nom métier seul. */
export function activityBusinessLabel(line) {
    const stripped = stripAnalyticCodePrefix(line.activity_label);
    return stripped || line.activity_label || "—";
}

export class GlcCoverageDetailField extends Component {
    static template = "dorevia_glc_analytics.GlcCoverageDetail";
    static props = { ...standardFieldProps };

    setup() {
        this.families = DETAIL_FAMILIES;
        this.state = useState({
            showPaidOnly: this._initialPaidOnlyState(),
        });
    }

    get storageCompanyId() {
        const company = this.props.record.data.company_id;
        if (!company) {
            return "no_company";
        }
        if (Array.isArray(company)) {
            return company[0] || "no_company";
        }
        if (typeof company === "object" && company !== null) {
            return company.id || "no_company";
        }
        return company;
    }

    get paidOnlyStorageKey() {
        const db = session.db || "no_db";
        const uid = session.uid || "no_uid";
        return `${STORAGE_KEY_PAID_ONLY}:${db}:${uid}:${this.storageCompanyId}`;
    }

    _initialPaidOnlyState() {
        const scopedValue = localStorage.getItem(this.paidOnlyStorageKey);
        if (scopedValue !== null) {
            return scopedValue === "1";
        }
        return localStorage.getItem(STORAGE_KEY_PAID_ONLY) === "1";
    }

    get currencyId() {
        const currency = this.props.record.data.currency_id;
        if (!currency) {
            return null;
        }
        if (Array.isArray(currency)) {
            return currency[0];
        }
        if (typeof currency === "object" && currency !== null) {
            return currency.id ?? null;
        }
        return currency;
    }

    get tableColspan() {
        return 5;
    }

    togglePaidOnly(ev) {
        this.state.showPaidOnly = ev.target.checked;
        localStorage.setItem(
            this.paidOnlyStorageKey,
            this.state.showPaidOnly ? "1" : "0"
        );
    }

    isZero(value) {
        if (value === false || value === null || value === undefined) {
            return true;
        }
        return Math.abs(value) < 0.005;
    }

    formatAmount(value) {
        if (this.isZero(value)) {
            return "—";
        }
        return formatMonetary(value, { currencyId: this.currencyId });
    }

    amountClass(value, familyClass) {
        let cls = "text-end o_monetary_field";
        if (familyClass) {
            cls += " " + familyClass;
        }
        if (this.isZero(value)) {
            cls += " o_glc_zero";
        }
        return cls;
    }

    performanceClass(value, familyClass, familyEndClass) {
        let cls = "text-end o_monetary_field";
        if (familyClass) {
            cls += " " + familyClass;
        }
        if (familyEndClass) {
            cls += " " + familyEndClass;
        }
        if (this.isZero(value)) {
            cls += " o_glc_zero";
        } else if (value < 0) {
            cls += " o_glc_performance_negative";
        } else {
            cls += " o_glc_performance_positive";
        }
        return cls;
    }

    cellClass(family, row, bold = false) {
        const value = row[family.realizedKey];
        let cls;
        if (family.valueType === "performance") {
            cls = this.performanceClass(value, family.cssStart, "");
        } else {
            cls = this.amountClass(value, family.cssStart);
        }
        return bold ? cls + " fw-bold" : cls;
    }

    _emptyTotals() {
        const totals = {};
        for (const key of NUMERIC_FIELDS) {
            totals[key] = 0;
        }
        return totals;
    }

    _accumulate(target, source) {
        for (const key of NUMERIC_FIELDS) {
            target[key] += source[key] || 0;
        }
    }

    activityDisplayLabel(line) {
        return activityBusinessLabel(line);
    }

    activityTooltip(line) {
        const code = analyticCodeFromLine(line);
        return code ? `[${code}]` : undefined;
    }

    _normalizeActivityRow(data) {
        const businessLabel = activityBusinessLabel(data);
        const displayData = applyPaidDisplayMode(data, this.state.showPaidOnly);
        return {
            ...displayData,
            activity_label: businessLabel,
        };
    }

    get groupedData() {
        const list = this.props.record.data[this.props.name];
        const records = (list && list.records) || [];
        const map = new Map();
        for (const r of records) {
            const data = r.data;
            if (data.line_kind !== "activity") {
                continue;
            }
            const key = data.month_key || "";
            if (!map.has(key)) {
                map.set(key, {
                    monthKey: key,
                    monthLabel: data.month_label || key,
                    lines: [],
                    totals: this._emptyTotals(),
                });
            }
            const month = map.get(key);
            const rowData = this._normalizeActivityRow(data);
            month.lines.push({ id: r.id, ...rowData });
            this._accumulate(month.totals, rowData);
        }
        const months = [...map.values()].sort((a, b) =>
            a.monthKey.localeCompare(b.monthKey)
        );
        const periodTotals = this._emptyTotals();
        for (const m of months) {
            m.lines.sort((a, b) =>
                (a.activity_label || "").localeCompare(b.activity_label || "", "fr")
            );
            this._accumulate(periodTotals, m.totals);
            Object.assign(m.totals, computePerformanceAmounts(m.totals));
        }
        Object.assign(periodTotals, computePerformanceAmounts(periodTotals));
        return {
            months,
            periodTotals,
            multiMonth: months.length > 1,
            hasLines: months.length > 0,
        };
    }
}

export const glcCoverageDetailField = {
    component: GlcCoverageDetailField,
    displayName: "Détail couverture cockpit GLC",
    supportedTypes: ["one2many"],
    relatedFields: () => [
        { name: "line_kind", type: "selection" },
        { name: "month_key", type: "char" },
        { name: "month_label", type: "char" },
        { name: "activity_label", type: "char" },
        { name: "analytic_code", type: "char" },
        { name: "currency_id", type: "many2one", relation: "res.currency" },
        { name: "revenue_realized", type: "monetary" },
        { name: "revenue_realized_paid", type: "monetary" },
        { name: "payroll_realized", type: "monetary" },
        { name: "payroll_realized_paid", type: "monetary" },
        { name: "expense_realized", type: "monetary" },
        { name: "expense_realized_paid", type: "monetary" },
        { name: "performance_realized", type: "monetary" },
    ],
};

registry.category("fields").add("glc_coverage_detail", glcCoverageDetailField);
