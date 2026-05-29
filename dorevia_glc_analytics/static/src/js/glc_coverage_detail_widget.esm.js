/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { formatMonetary } from "@web/views/fields/formatters";

const STORAGE_KEY = "glc_cockpit_detail_show_budget_variance";

const NUMERIC_FIELDS = [
    "revenue_realized",
    "revenue_budget",
    "variance_revenue",
    "payroll_realized",
    "payroll_budget",
    "variance_payroll",
    "expense_realized",
    "expense_budget",
    "variance_expense",
];

export const DETAIL_FAMILIES = [
    {
        label: "Recette",
        cssStart: "o_glc_family_recettes",
        cssEnd: "o_glc_family_recettes_end",
        realizedKey: "revenue_realized",
        budgetKey: "revenue_budget",
        varianceKey: "variance_revenue",
        valueType: "amount",
    },
    {
        label: "Cumul RH",
        cssStart: "o_glc_family_payroll",
        cssEnd: "o_glc_family_payroll_end",
        realizedKey: "payroll_realized",
        budgetKey: "payroll_budget",
        varianceKey: "variance_payroll",
        valueType: "amount",
    },
    {
        label: "Dépense",
        cssStart: "o_glc_family_expense",
        cssEnd: "o_glc_family_expense_end",
        realizedKey: "expense_realized",
        budgetKey: "expense_budget",
        varianceKey: "variance_expense",
        valueType: "amount",
    },
    {
        label: "Solde",
        cssStart: "o_glc_family_performance",
        cssEnd: "o_glc_family_performance",
        realizedKey: "performance_realized",
        budgetKey: "performance_budget",
        varianceKey: "variance_performance",
        valueType: "performance",
    },
];

export function computePerformanceAmounts(data) {
    const performance_realized =
        (data.revenue_realized || 0) -
        (data.payroll_realized || 0) -
        (data.expense_realized || 0);
    const performance_budget =
        (data.revenue_budget || 0) -
        (data.payroll_budget || 0) -
        (data.expense_budget || 0);
    return {
        performance_realized,
        performance_budget,
        variance_performance: performance_realized - performance_budget,
    };
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
            showBudgetVariance:
                localStorage.getItem(STORAGE_KEY) === "1",
        });
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
        return this.state.showBudgetVariance ? 13 : 5;
    }

    toggleBudgetVariance(ev) {
        this.state.showBudgetVariance = ev.target.checked;
        localStorage.setItem(
            STORAGE_KEY,
            this.state.showBudgetVariance ? "1" : "0"
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

    varianceClass(value, familyClass, familyEndClass) {
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
            cls += " o_glc_variance_negative";
        } else {
            cls += " o_glc_variance_positive";
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

    cellClass(family, columnType, row, bold = false) {
        const keyMap = {
            realized: family.realizedKey,
            budget: family.budgetKey,
            variance: family.varianceKey,
        };
        const value = row[keyMap[columnType]];
        let cls;
        if (family.valueType === "performance") {
            if (columnType === "realized" || columnType === "variance") {
                cls = this.performanceClass(
                    value,
                    columnType === "realized" ? family.cssStart : "",
                    ""
                );
            } else {
                cls = this.amountClass(value, "");
            }
        } else if (columnType === "variance") {
            cls = this.varianceClass(value, "", family.cssEnd);
        } else {
            cls = this.amountClass(
                value,
                columnType === "realized" ? family.cssStart : ""
            );
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

    _withPerformance(data) {
        return {
            ...data,
            ...computePerformanceAmounts(data),
        };
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
        return {
            ...this._withPerformance(data),
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
            month.lines.push({ id: r.id, ...this._normalizeActivityRow(data) });
            this._accumulate(month.totals, data);
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
        { name: "revenue_budget", type: "monetary" },
        { name: "variance_revenue", type: "monetary" },
        { name: "payroll_realized", type: "monetary" },
        { name: "payroll_budget", type: "monetary" },
        { name: "variance_payroll", type: "monetary" },
        { name: "expense_realized", type: "monetary" },
        { name: "expense_budget", type: "monetary" },
        { name: "variance_expense", type: "monetary" },
        { name: "performance_realized", type: "monetary" },
        { name: "performance_budget", type: "monetary" },
        { name: "variance_performance", type: "monetary" },
    ],
};

registry.category("fields").add("glc_coverage_detail", glcCoverageDetailField);
