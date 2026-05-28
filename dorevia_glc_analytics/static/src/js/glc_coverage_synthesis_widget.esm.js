/** @odoo-module **/

import { Component, onMounted, onPatched, onWillUnmount, useRef, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { formatMonetary } from "@web/views/fields/formatters";
import { loadJS } from "@web/core/assets";
import { computePerformanceAmounts } from "./glc_coverage_detail_widget.esm";

const NUMERIC_FIELDS = [
    "revenue_realized",
    "revenue_budget",
    "payroll_realized",
    "payroll_budget",
    "expense_realized",
    "expense_budget",
];

const COLOR_REAL = "#198754";
const COLOR_BUDGET = "#adb5bd";
const COLOR_REVENUE = "#3b7ddd";
const COLOR_PAYROLL = "#f29440";
const COLOR_EXPENSE = "#b8bdc5";
const COLOR_POSITIVE = "#198754";
const COLOR_NEGATIVE = "#b02a2a";
const COVERAGE_GREEN = "#198754";
const COVERAGE_ORANGE = "#f0a020";
const COVERAGE_RED = "#b02a2a";

export class GlcCoverageSynthesisField extends Component {
    static template = "dorevia_glc_analytics.GlcCoverageSynthesis";
    static props = { ...standardFieldProps };

    setup() {
        this.perfChartRef = useRef("perfChart");
        this.structChartRef = useRef("structChart");
        this.activityChartRef = useRef("activityChart");
        this._charts = {};
        this.state = useState({ chartsReady: false });

        onMounted(async () => {
            await loadJS("/web/static/lib/Chart/Chart.js");
            this.state.chartsReady = true;
            this._renderCharts();
        });

        onPatched(() => {
            if (this.state.chartsReady) {
                this._renderCharts();
            }
        });

        onWillUnmount(() => this._destroyCharts());
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

    formatSignedAmount(value) {
        if (this.isZero(value)) {
            return "—";
        }
        const formatted = formatMonetary(Math.abs(value), { currencyId: this.currencyId });
        return value < 0 ? `- ${formatted}` : `+ ${formatted}`;
    }

    formatCoverageRate(rate) {
        if (rate === null || rate === undefined) {
            return "—";
        }
        return `${rate.toFixed(0)} %`;
    }

    coverageClass(rate) {
        if (rate === null || rate === undefined) {
            return "o_glc_kpi_neutral";
        }
        if (rate >= 100) {
            return "o_glc_kpi_positive";
        }
        if (rate >= 80) {
            return "o_glc_kpi_warning";
        }
        return "o_glc_kpi_negative";
    }

    coverageColor(rate) {
        if (rate === null || rate === undefined) {
            return COLOR_BUDGET;
        }
        if (rate >= 100) {
            return COVERAGE_GREEN;
        }
        if (rate >= 80) {
            return COVERAGE_ORANGE;
        }
        return COVERAGE_RED;
    }

    signedClass(value) {
        if (this.isZero(value)) {
            return "o_glc_kpi_neutral";
        }
        return value < 0 ? "o_glc_kpi_negative" : "o_glc_kpi_positive";
    }

    _cockpitSalaryCoverageRate() {
        const rate = this.props.record.data.salary_coverage_rate;
        if (rate === false || rate === null || rate === undefined) {
            return null;
        }
        return rate;
    }

    get resourcesRealized() {
        return this.props.record.data.resources_realized || 0;
    }

    get fundingRealized() {
        return this.props.record.data.funding_realized || 0;
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

    get aggregates() {
        const list = this.props.record.data[this.props.name];
        const records = (list && list.records) || [];
        const monthsMap = new Map();
        const activitiesMap = new Map();
        const periodTotals = this._emptyTotals();

        for (const r of records) {
            const data = r.data;
            if (data.line_kind !== "activity") {
                continue;
            }
            const monthKey = data.month_key || "";
            if (!monthsMap.has(monthKey)) {
                monthsMap.set(monthKey, {
                    monthKey,
                    monthLabel: data.month_label || monthKey,
                    totals: this._emptyTotals(),
                });
            }
            this._accumulate(monthsMap.get(monthKey).totals, data);

            const activityLabel = data.activity_label || "—";
            if (!activitiesMap.has(activityLabel)) {
                activitiesMap.set(activityLabel, {
                    label: activityLabel,
                    totals: this._emptyTotals(),
                });
            }
            this._accumulate(activitiesMap.get(activityLabel).totals, data);

            this._accumulate(periodTotals, data);
        }

        const months = [...monthsMap.values()].sort((a, b) =>
            a.monthKey.localeCompare(b.monthKey)
        );
        for (const m of months) {
            Object.assign(m.totals, computePerformanceAmounts(m.totals));
        }

        const activities = [...activitiesMap.values()].map((a) => ({
            ...a,
            totals: { ...a.totals, ...computePerformanceAmounts(a.totals) },
        }));
        activities.sort(
            (a, b) => b.totals.performance_realized - a.totals.performance_realized
        );

        const perfPeriod = computePerformanceAmounts(periodTotals);

        const salaryCoverageRate = this._cockpitSalaryCoverageRate();

        return {
            hasLines: months.length > 0,
            multiMonth: months.length > 1,
            months,
            activities,
            periodTotals: { ...periodTotals, ...perfPeriod },
            salaryCoverageRate,
        };
    }

    _destroyCharts() {
        for (const k of Object.keys(this._charts)) {
            try {
                this._charts[k].destroy();
            } catch (e) {
                // ignore
            }
            delete this._charts[k];
        }
    }

    _renderCharts() {
        if (!window.Chart) {
            return;
        }
        this._destroyCharts();
        const agg = this.aggregates;
        if (!agg.hasLines) {
            return;
        }
        this._renderPerformanceMonthly(agg);
        this._renderStructureMonthly(agg);
        this._renderPerformanceByActivity(agg);
    }

    _commonOptions(currencyTickFn) {
        return {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: "index", intersect: false },
            plugins: {
                legend: { position: "bottom", labels: { boxWidth: 12, font: { size: 11 } } },
                tooltip: {
                    callbacks: {
                        label: (ctx) => {
                            const v = ctx.parsed.y ?? ctx.parsed.x ?? ctx.parsed;
                            return `${ctx.dataset.label}: ${this.formatAmount(v)}`;
                        },
                    },
                },
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { callback: currencyTickFn },
                },
            },
        };
    }

    _currencyTick(value) {
        return formatMonetary(value, { currencyId: this.currencyId });
    }

    _renderPerformanceMonthly(agg) {
        const canvas = this.perfChartRef.el;
        if (!canvas) {
            return;
        }
        const labels = agg.months.map((m) => m.monthLabel);
        const realData = agg.months.map((m) => m.totals.performance_realized);
        const budgetData = agg.months.map((m) => m.totals.performance_budget);
        const options = this._commonOptions((v) => this._currencyTick(v));
        this._charts.perf = new window.Chart(canvas, {
            type: "bar",
            data: {
                labels,
                datasets: [
                    {
                        label: "Marge réelle",
                        data: realData,
                        backgroundColor: COLOR_REAL,
                        borderRadius: 2,
                    },
                    {
                        label: "Marge budget",
                        data: budgetData,
                        backgroundColor: COLOR_BUDGET,
                        borderRadius: 2,
                    },
                ],
            },
            options,
        });
    }

    _renderStructureMonthly(agg) {
        const canvas = this.structChartRef.el;
        if (!canvas) {
            return;
        }
        const labels = agg.months.map((m) => m.monthLabel);
        // Convention MOA : salaires et dépenses en valeurs positives de consommation.
        const revenueData = agg.months.map((m) => Math.abs(m.totals.revenue_realized || 0));
        const payrollData = agg.months.map((m) => Math.abs(m.totals.payroll_realized || 0));
        const expenseData = agg.months.map((m) => Math.abs(m.totals.expense_realized || 0));
        const options = this._commonOptions((v) => this._currencyTick(v));
        this._charts.struct = new window.Chart(canvas, {
            type: "bar",
            data: {
                labels,
                datasets: [
                    { label: "Ressources", data: revenueData, backgroundColor: COLOR_REVENUE, borderRadius: 2 },
                    { label: "Salaires", data: payrollData, backgroundColor: COLOR_PAYROLL, borderRadius: 2 },
                    { label: "Dépenses", data: expenseData, backgroundColor: COLOR_EXPENSE, borderRadius: 2 },
                ],
            },
            options,
        });
    }

    _renderPerformanceByActivity(agg) {
        const canvas = this.activityChartRef.el;
        if (!canvas) {
            return;
        }
        const labels = agg.activities.map((a) => a.label);
        const data = agg.activities.map((a) => a.totals.performance_realized);
        const colors = data.map((v) => (v < 0 ? COLOR_NEGATIVE : COLOR_POSITIVE));
        this._charts.activity = new window.Chart(canvas, {
            type: "bar",
            data: {
                labels,
                datasets: [
                    {
                        label: "Marge réelle (cumul période)",
                        data,
                        backgroundColor: colors,
                        borderRadius: 2,
                    },
                ],
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: (ctx) => this.formatAmount(ctx.parsed.x),
                        },
                    },
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: { callback: (v) => this._currencyTick(v) },
                    },
                },
            },
        });
    }
}

export const glcCoverageSynthesisField = {
    component: GlcCoverageSynthesisField,
    displayName: "Synthèse graphique cockpit GLC (marge d'activité)",
    supportedTypes: ["one2many"],
    relatedFields: () => [
        { name: "line_kind", type: "selection" },
        { name: "month_key", type: "char" },
        { name: "month_label", type: "char" },
        { name: "activity_label", type: "char" },
        { name: "currency_id", type: "many2one", relation: "res.currency" },
        { name: "revenue_realized", type: "monetary" },
        { name: "revenue_budget", type: "monetary" },
        { name: "payroll_realized", type: "monetary" },
        { name: "payroll_budget", type: "monetary" },
        { name: "expense_realized", type: "monetary" },
        { name: "expense_budget", type: "monetary" },
        { name: "performance_realized", type: "monetary" },
        { name: "performance_budget", type: "monetary" },
        { name: "variance_performance", type: "monetary" },
    ],
};

registry.category("fields").add("glc_coverage_synthesis", glcCoverageSynthesisField);
