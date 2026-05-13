/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const W = 920;
const H = 440;
const ML = 78;
const MR = 28;
const MT = 36;
const MB = 56;

function parseDate(s) {
    if (!s) {
        return null;
    }
    const parts = String(s).split("-");
    if (parts.length !== 3) {
        return null;
    }
    const y = Number(parts[0]);
    const m = Number(parts[1]) - 1;
    const d = Number(parts[2]);
    return new Date(y, m, d).getTime();
}

function formatShortDate(ms) {
    const dt = new Date(ms);
    const d = dt.getDate();
    const m = dt.getMonth() + 1;
    return `${String(d).padStart(2, "0")}/${String(m).padStart(2, "0")}`;
}

function formatMoney(amount, currencyCode, digits) {
    if (amount === null || amount === undefined || Number.isNaN(amount)) {
        return "";
    }
    try {
        return new Intl.NumberFormat(undefined, {
            style: "currency",
            currency: currencyCode || "EUR",
            maximumFractionDigits: digits,
            minimumFractionDigits: Math.min(2, digits),
        }).format(amount);
    } catch {
        return String(Math.round(amount * 100) / 100);
    }
}

function niceStep(range, targetTicks) {
    const raw = range / Math.max(targetTicks, 1);
    const exp = Math.floor(Math.log10(raw));
    const f = raw / 10 ** exp;
    let nf = 1;
    if (f <= 1) {
        nf = 1;
    } else if (f <= 2) {
        nf = 2;
    } else if (f <= 5) {
        nf = 5;
    } else {
        nf = 10;
    }
    return nf * 10 ** exp;
}

function buildPathD(xs, ys) {
    if (!xs.length) {
        return "";
    }
    let d = `M ${xs[0].toFixed(1)},${ys[0].toFixed(1)}`;
    for (let i = 1; i < xs.length; i++) {
        d += ` L ${xs[i].toFixed(1)},${ys[i].toFixed(1)}`;
    }
    return d;
}

function computeLayout(points, situationDateStr, threshold, currencyCode) {
    const situationMs = parseDate(situationDateStr);
    const times = points.map((p) => parseDate(p.anchor_date)).filter((t) => t !== null);
    const balances = points.map((p) => p.balance ?? 0);
    if (!times.length) {
        return null;
    }
    let tMin = Math.min(...times);
    let tMax = Math.max(...times);
    if (tMax === tMin) {
        tMax = tMin + 86400000;
    }
    let vMin = Math.min(...balances);
    let vMax = Math.max(...balances);
    if (threshold !== null && threshold !== undefined && !Number.isNaN(threshold)) {
        vMin = Math.min(vMin, threshold);
        vMax = Math.max(vMax, threshold);
    }
    if (vMin === vMax) {
        vMin -= 1;
        vMax += 1;
    }
    const padY = (vMax - vMin) * 0.08;
    vMin -= padY;
    vMax += padY;

    const cw = W - ML - MR;
    const ch = H - MT - MB;

    const xScale = (t) => ML + ((t - tMin) / (tMax - tMin)) * cw;
    const yScale = (v) => MT + ((vMax - v) / (vMax - vMin)) * ch;

    const xs = times.map((t) => xScale(t));
    const ys = balances.map((v) => yScale(v));

    let splitIdx = points.findIndex((p) => p.segment === "projected");
    if (splitIdx < 0) {
        splitIdx = points.length;
    }

    let pathActual = "";
    let pathProjected = "";
    if (splitIdx === 0) {
        pathProjected = buildPathD(xs, ys);
    } else if (splitIdx >= points.length) {
        pathActual = buildPathD(xs, ys);
    } else {
        pathActual = buildPathD(xs.slice(0, splitIdx), ys.slice(0, splitIdx));
        const j = splitIdx - 1;
        pathProjected = buildPathD(xs.slice(j), ys.slice(j));
    }

    const lastActualIdx = splitIdx > 0 ? splitIdx - 1 : 0;
    const xSit =
        situationMs !== null ? xScale(situationMs) : xs[Math.min(lastActualIdx, xs.length - 1)];
    const situationLine =
        xSit >= ML && xSit <= ML + cw
            ? {
                  x: xSit,
                  y1: MT,
                  y2: MT + ch,
                  labelX: Math.min(xSit + 6, ML + cw - 70),
                  labelY: MT + 14,
              }
            : null;

    let thresholdLine = null;
    if (threshold !== null && threshold !== undefined && !Number.isNaN(threshold)) {
        const yT = yScale(threshold);
        if (yT >= MT - 2 && yT <= MT + ch + 2) {
            thresholdLine = {
                x1: ML,
                x2: ML + cw,
                y: yT,
                labelX: ML + cw - 2,
                labelY: yT - 6,
            };
        }
    }

    const yStep = niceStep(vMax - vMin, 5);
    const yTicks = [];
    const startY = Math.ceil(vMin / yStep) * yStep;
    for (let v = startY; v <= vMax + yStep * 0.001; v += yStep) {
        if (v < vMin - yStep * 0.001) {
            continue;
        }
        yTicks.push({
            x: ML - 8,
            y: yScale(v) + 4,
            label: formatMoney(v, currencyCode, vMax - vMin > 500 ? 0 : 2),
        });
    }

    const tickCount = Math.min(6, Math.max(3, Math.floor(cw / 100)));
    const xTicks = [];
    for (let i = 0; i < tickCount; i++) {
        const t = tMin + ((tMax - tMin) * i) / (tickCount - 1 || 1);
        xTicks.push({
            x: xScale(t),
            y: H - 18,
            label: formatShortDate(t),
        });
    }

    const hGridLines = [];
    const gridCount = 4;
    for (let i = 0; i <= gridCount; i++) {
        const gy = MT + (ch * i) / gridCount;
        hGridLines.push({ x1: ML, x2: ML + cw, y: gy });
    }

    const vertexMarkers = points.map((p, i) => {
        const seg =
            p.segment === "projected"
                ? "Projeté"
                : p.segment === "actual"
                  ? "Constaté"
                  : String(p.segment || "");
        const bal = formatMoney(p.balance ?? 0, currencyCode, 2);
        const lbl = p.label ? ` · ${p.label}` : "";
        const title = `${p.anchor_date || ""} — ${bal} (${seg})${lbl}`;
        return {
            cx: xs[i],
            cy: ys[i],
            fill: p.segment === "projected" ? "#5dade2" : "#1b6ec2",
            title,
        };
    });

    return {
        viewBox: `0 0 ${W} ${H}`,
        pathActual,
        pathProjected,
        situationLine,
        thresholdLine,
        xTicks,
        yTicks,
        hGridLines,
        vertexMarkers,
        axes: { left: ML, right: ML + cw, top: MT, bottom: MT + ch },
    };
}

export class TrajectoryChartAction extends Component {
    static template = "dorevia_cash_flow.TrajectoryChartAction";
    static props = {
        "*": true,
    };

    setup() {
        this.orm = useService("orm");
        this.actionService = useService("action");
        this.state = useState({
            loading: true,
            error: "",
            subtitle: "",
            viewBox: `0 0 ${W} ${H}`,
            pathActual: "",
            pathProjected: "",
            situationLine: null,
            thresholdLine: null,
            xTicks: [],
            yTicks: [],
            hGridLines: [],
            vertexMarkers: [],
            axes: { left: ML, right: W - MR, top: MT, bottom: H - MB },
            wizardId: null,
            currencyCode: "EUR",
        });

        onWillStart(async () => {
            const wizardId =
                this.props.action?.params?.wizard_id ??
                this.props.action?.context?.default_wizard_id ??
                null;
            if (!wizardId) {
                this.state.loading = false;
                this.state.error = "Paramètre assistant manquant (wizard_id).";
                return;
            }
            this.state.wizardId = wizardId;
            try {
                const wizards = await this.orm.read(
                    "dorevia.cash.flow.trajectory.wizard",
                    [wizardId],
                    [
                        "guard_id",
                        "situation_date",
                        "alert_threshold",
                        "currency_id",
                        "chart_date_end",
                        "fiscal_date_from",
                    ]
                );
                if (!wizards.length) {
                    this.state.error = "Assistant introuvable ou expiré. Rouvrez la trajectoire depuis le menu.";
                    this.state.loading = false;
                    return;
                }
                const wiz = wizards[0];
                const currencyId = wiz.currency_id?.[0];
                let currencyCode = "EUR";
                if (currencyId) {
                    const cur = await this.orm.read("res.currency", [currencyId], ["name"]);
                    if (cur.length && cur[0].name) {
                        currencyCode = cur[0].name;
                    }
                }

                const pointRecs = await this.orm.searchRead(
                    "dorevia.cash.flow.trajectory.point",
                    [["wizard_id", "=", wizardId]],
                    ["anchor_date", "balance", "segment", "label", "sequence"],
                    { order: "sequence, id" }
                );
                if (!pointRecs.length) {
                    this.state.error = "Aucun point de trajectoire. Utilisez « Afficher la trajectoire » depuis l'assistant.";
                    this.state.loading = false;
                    return;
                }

                const layout = computeLayout(
                    pointRecs,
                    wiz.situation_date,
                    wiz.alert_threshold,
                    currencyCode
                );
                if (!layout) {
                    this.state.error = "Impossible de calculer le graphique (dates invalides).";
                    this.state.loading = false;
                    return;
                }

                const guardName = wiz.guard_id?.[1] || "";
                const wizAfter = await this.orm.read(
                    "dorevia.cash.flow.trajectory.wizard",
                    [wizardId],
                    [
                        "min_balance_on_curve",
                        "min_balance_date_on_curve",
                        "info_message",
                    ]
                );
                const w2 = wizAfter[0] || {};
                const extra = [];
                if (w2.min_balance_date_on_curve) {
                    extra.push(
                        `Point bas : ${formatMoney(w2.min_balance_on_curve ?? 0, currencyCode, 2)} (${w2.min_balance_date_on_curve})`
                    );
                }
                if (w2.info_message) {
                    extra.push(String(w2.info_message));
                }
                this.state.subtitle = [
                    guardName ? `Projection : ${guardName}` : "",
                    wiz.situation_date ? `Date de situation : ${wiz.situation_date}` : "",
                    wiz.alert_threshold != null
                        ? `Seuil d'alerte : ${formatMoney(wiz.alert_threshold, currencyCode, 2)}`
                        : "",
                    ...extra,
                ]
                    .filter(Boolean)
                    .join(" · ");

                Object.assign(this.state, layout);
                this.state.currencyCode = currencyCode;
            } catch (e) {
                this.state.error =
                    (e && (e.message || e.data?.message)) ||
                    "Erreur lors du chargement de la trajectoire.";
            } finally {
                this.state.loading = false;
            }
        });
    }

    async onChangeProjection() {
        await this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Choisir une projection",
            res_model: "dorevia.cash.flow.trajectory.wizard",
            views: [[false, "form"]],
            target: "new",
        });
    }

    async onOpenList() {
        if (!this.state.wizardId) {
            return;
        }
        await this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Points de trajectoire",
            res_model: "dorevia.cash.flow.trajectory.point",
            views: [
                [false, "list"],
                [false, "graph"],
            ],
            domain: [["wizard_id", "=", this.state.wizardId]],
            context: {
                create: false,
                edit: false,
                delete: false,
            },
            target: "new",
        });
    }
}

registry.category("actions").add("dorevia_cash_flow_trajectory_chart", TrajectoryChartAction);
