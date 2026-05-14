/** @odoo-module **/

import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const W = 920;
const H = 440;
const ML = 78;
/** Marge droite : bandeau pour libellés de seuils (hors zone de lecture de la courbe). */
const MR = 72;
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

function formatFrDate(value) {
    if (!value) {
        return "";
    }
    const s = String(value).slice(0, 10);
    const ms = parseDate(s);
    if (!ms) {
        return String(value);
    }
    const dt = new Date(ms);
    const d = dt.getDate();
    const m = dt.getMonth() + 1;
    const y = dt.getFullYear();
    return `${String(d).padStart(2, "0")}/${String(m).padStart(2, "0")}/${y}`;
}

/** Année de référence du graphique (priorité : date de situation, sinon premier point). */
function chartReferenceYear(situationDateStr, points) {
    const yearFrom = (s) => {
        if (!s) {
            return null;
        }
        const head = String(s).slice(0, 10);
        const y = parseInt(head.slice(0, 4), 10);
        return Number.isFinite(y) && y >= 1970 && y <= 2100 ? y : null;
    };
    const fromSit = yearFrom(situationDateStr);
    if (fromSit !== null) {
        return fromSit;
    }
    if (points && points.length) {
        const fromPt = yearFrom(points[0].anchor_date);
        if (fromPt !== null) {
            return fromPt;
        }
    }
    return new Date().getFullYear();
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

/** Montants cockpit / sous-titres métier (séparateurs milliers à la française). */
function formatMoneyFr(amount, currencyCode, digits) {
    if (amount === null || amount === undefined || Number.isNaN(amount)) {
        return "";
    }
    try {
        return new Intl.NumberFormat("fr-FR", {
            style: "currency",
            currency: currencyCode || "EUR",
            maximumFractionDigits: digits,
            minimumFractionDigits: Math.min(2, digits),
        }).format(amount);
    } catch {
        return formatMoney(amount, currencyCode, digits);
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

function computeLayout(points, situationDateStr, alertThreshold, comfortThreshold, currencyCode) {
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
    if (alertThreshold !== null && alertThreshold !== undefined && !Number.isNaN(alertThreshold)) {
        vMin = Math.min(vMin, alertThreshold);
        vMax = Math.max(vMax, alertThreshold);
    }
    if (comfortThreshold !== null && comfortThreshold !== undefined && !Number.isNaN(comfortThreshold)) {
        vMin = Math.min(vMin, comfortThreshold);
        vMax = Math.max(vMax, comfortThreshold);
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
                  /** Libellé sous l’axe des abscisses, centré sur la ligne (hors zone de tracé). */
                  labelX: Math.max(ML + 22, Math.min(xSit, ML + cw - 22)),
                  labelY: MT + ch + 5,
              }
            : null;

    let comfortThresholdLine = null;
    const alertVal =
        alertThreshold !== null && alertThreshold !== undefined && !Number.isNaN(alertThreshold)
            ? alertThreshold
            : null;
    const comfortVal =
        comfortThreshold !== null &&
        comfortThreshold !== undefined &&
        !Number.isNaN(comfortThreshold)
            ? comfortThreshold
            : null;
    let yComfort = null;
    if (
        comfortVal !== null &&
        (alertVal === null || comfortVal > alertVal + 1e-6)
    ) {
        const yC = yScale(comfortVal);
        if (yC >= MT - 2 && yC <= MT + ch + 2) {
            yComfort = yC;
        }
    }

    let yAlert = null;
    if (alertVal !== null) {
        const yT = yScale(alertVal);
        if (yT >= MT - 2 && yT <= MT + ch + 2) {
            yAlert = yT;
        }
    }

    let comfortLabelY = yComfort;
    let alertLabelY = yAlert;
    if (
        yComfort !== null &&
        yAlert !== null &&
        Math.abs(yAlert - yComfort) < 22
    ) {
        comfortLabelY = yComfort - 10;
        alertLabelY = yAlert + 10;
    }

    /** Juste à droite du cadre de tracé (bord « axe » droit du graphique). */
    const labelX = ML + cw + 2;
    if (yComfort !== null) {
        comfortThresholdLine = {
            x1: ML,
            x2: ML + cw,
            y: yComfort,
            labelX,
            labelY: comfortLabelY,
        };
    }

    let thresholdLine = null;
    if (yAlert !== null) {
        thresholdLine = {
            x1: ML,
            x2: ML + cw,
            y: yAlert,
            labelX,
            labelY: alertLabelY,
        };
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

    const moneyDigits = vMax - vMin > 500 ? 0 : 2;
    const BAL_EPS = 0.005;

    const vertexMarkers = points.map((p, i) => {
        const seg =
            p.segment === "projected"
                ? "Projeté"
                : p.segment === "actual"
                  ? "Constaté"
                  : String(p.segment || "");
        const curr = Number(p.balance ?? 0) || 0;
        const prevBal = i > 0 ? Number(points[i - 1].balance ?? 0) || 0 : null;
        const differsFromPrev =
            prevBal === null ? true : Math.abs(curr - prevBal) > BAL_EPS;
        const showValueLabel = Math.abs(curr) > BAL_EPS && differsFromPrev;
        const valueLabel = formatMoney(curr, currencyCode, moneyDigits);
        const lbl = p.label ? ` · ${p.label}` : "";
        const title = `${p.anchor_date || ""} — ${formatMoney(curr, currencyCode, 2)} (${seg})${lbl}`;
        const dx = 6;
        const dyBelow = 10;
        let valueLabelX = xs[i] + dx;
        let valueLabelAnchor = "start";
        const plotRight = ML + cw;
        if (valueLabelX > plotRight - 48) {
            valueLabelX = xs[i] - dx;
            valueLabelAnchor = "end";
        }
        let valueLabelY = ys[i] + dyBelow;
        if (valueLabelY > MT + ch - 4) {
            valueLabelY = MT + ch - 4;
        }
        return {
            cx: xs[i],
            cy: ys[i],
            fill: p.segment === "projected" ? "#5dade2" : "#1b6ec2",
            title,
            showValueLabel,
            valueLabel,
            valueLabelX,
            valueLabelY,
            valueLabelAnchor,
        };
    });

    return {
        viewBox: `0 0 ${W} ${H}`,
        pathActual,
        pathProjected,
        situationLine,
        comfortThresholdLine,
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
            modeBanner: "",
            modeAlertVariant: "warning",
            trajectoryMode: "contextualized",
            contextualizedKind: "projection",
            pageTitle: "Trajectoire de trésorerie",
            viewBox: `0 0 ${W} ${H}`,
            pathActual: "",
            pathProjected: "",
            situationLine: null,
            comfortThresholdLine: null,
            thresholdLine: null,
            xTicks: [],
            yTicks: [],
            hGridLines: [],
            vertexMarkers: [],
            axes: { left: ML, right: W - MR, top: MT, bottom: H - MB },
            wizardId: null,
            currencyCode: "EUR",
            cockpitMode: false,
            guardId: null,
            cockpitRefreshing: false,
            /** Repères d’analyse (libellés graphique, légende, valeurs aux ruptures) — masqués par défaut. */
            showRefChartLabels: false,
            /** Année affichée au-dessus du graphique (référence projection). */
            chartHeadingYear: null,
        });

        onWillStart(async () => {
            await this.loadTrajectory();
        });
    }

    isCockpit() {
        return Boolean(this.props.action?.params?.cockpit);
    }

    async loadTrajectory() {
        this.state.loading = true;
        this.state.error = "";
        this.state.chartHeadingYear = null;
        this.state.cockpitMode = this.isCockpit();
        const params = this.props.action?.params || {};
        this.state.guardId = params.guard_id ?? null;
        const trajectoryMode = params.trajectory_mode || "contextualized";
        const contextualizedKind = params.contextualized_kind || "projection";
        this.state.trajectoryMode = trajectoryMode;
        this.state.contextualizedKind = contextualizedKind;
        if (trajectoryMode === "reference") {
            this.state.modeAlertVariant = "success";
            this.state.modeBanner =
                "Trajectoire de référence — pilotage système (vérité cash de référence, non hypothèse utilisateur).";
            this.state.pageTitle = "Trajectoire de référence";
        } else if (contextualizedKind === "simulation") {
            this.state.modeAlertVariant = "warning";
            this.state.modeBanner =
                "Trajectoire de simulation — hypothèse ; ne remplace pas la trajectoire de référence système.";
            this.state.pageTitle = "Trajectoire de simulation";
        } else {
            this.state.modeAlertVariant = "warning";
            this.state.modeBanner =
                "Trajectoire contextualisée — projection métier sélectionnée ; ne remplace pas la trajectoire de référence système.";
            this.state.pageTitle = "Trajectoire contextualisée";
        }
        if (this.state.cockpitMode && trajectoryMode === "reference") {
            this.state.modeBanner = "";
        }

        const wizardId = this.props.action?.params?.wizard_id ?? null;
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
                    "comfort_threshold_amount",
                    "currency_id",
                    "chart_date_end",
                    "fiscal_date_from",
                ]
            );
            if (!wizards.length) {
                this.state.error =
                    "Assistant introuvable ou expiré. Rouvrez la trajectoire depuis le menu.";
                this.state.loading = false;
                return;
            }
            const wiz = wizards[0];
            if (!this.state.guardId && wiz.guard_id?.[0]) {
                this.state.guardId = wiz.guard_id[0];
            }
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
                this.state.error =
                    "Aucun point de trajectoire. Utilisez « Afficher la trajectoire » depuis l'assistant.";
                this.state.loading = false;
                return;
            }

            this.state.chartHeadingYear = chartReferenceYear(wiz.situation_date, pointRecs);

            const comfortRaw = wiz.comfort_threshold_amount;
            const comfortNum =
                comfortRaw === false || comfortRaw === null || comfortRaw === undefined
                    ? null
                    : Number(comfortRaw);

            const layout = computeLayout(
                pointRecs,
                wiz.situation_date,
                wiz.alert_threshold,
                comfortNum,
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
            if (this.state.cockpitMode && trajectoryMode === "reference") {
                const parts = ["Trajectoire de référence"];
                if (wiz.situation_date) {
                    parts.push(`Situation au ${formatFrDate(wiz.situation_date)}`);
                }
                if (wiz.alert_threshold != null && !Number.isNaN(wiz.alert_threshold)) {
                    parts.push(`Alerte : ${formatMoneyFr(wiz.alert_threshold, currencyCode, 2)}`);
                }
                const comfortCockpit =
                    wiz.comfort_threshold_amount !== false &&
                    wiz.comfort_threshold_amount !== null &&
                    wiz.comfort_threshold_amount !== undefined
                        ? Number(wiz.comfort_threshold_amount)
                        : null;
                const alertNum = Number(wiz.alert_threshold ?? 0);
                if (
                    comfortCockpit !== null &&
                    !Number.isNaN(comfortCockpit) &&
                    comfortCockpit > alertNum + 1e-6
                ) {
                    parts.push(`Confort : ${formatMoneyFr(comfortCockpit, currencyCode, 2)}`);
                }
                if (w2.min_balance_date_on_curve) {
                    parts.push(
                        `Point bas : ${formatMoneyFr(w2.min_balance_on_curve ?? 0, currencyCode, 2)} le ${formatFrDate(w2.min_balance_date_on_curve)}`
                    );
                }
                this.state.subtitle = parts.join(" · ");
            } else {
                const src =
                    trajectoryMode === "reference"
                        ? "Source : référence résolue (pilotage système)"
                        : contextualizedKind === "simulation"
                          ? "Source : hypothèse simulation (document)"
                          : "Source : projection contextualisée (assistant)";
                this.state.subtitle = [
                    src,
                    guardName ? `Projection : ${guardName}` : "",
                    wiz.situation_date ? `Date de situation : ${wiz.situation_date}` : "",
                    wiz.alert_threshold != null
                        ? `Seuil d'alerte : ${formatMoney(wiz.alert_threshold, currencyCode, 2)}`
                        : "",
                    (() => {
                        const c = Number(wiz.comfort_threshold_amount);
                        const a = Number(wiz.alert_threshold ?? 0);
                        if (
                            wiz.comfort_threshold_amount !== false &&
                            wiz.comfort_threshold_amount !== null &&
                            wiz.comfort_threshold_amount !== undefined &&
                            !Number.isNaN(c) &&
                            c > a + 1e-6
                        ) {
                            return `Seuil de confort : ${formatMoney(c, currencyCode, 2)}`;
                        }
                        return "";
                    })(),
                    ...extra,
                ]
                    .filter(Boolean)
                    .join(" · ");
            }

            Object.assign(this.state, layout);
            this.state.currencyCode = currencyCode;
        } catch (e) {
            this.state.error =
                (e && (e.message || e.data?.message)) ||
                "Erreur lors du chargement de la trajectoire.";
        } finally {
            this.state.loading = false;
        }
    }

    toggleShowRefChartLabels(ev) {
        this.state.showRefChartLabels = Boolean(ev.target?.checked);
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

    async onOpenGuardForm() {
        if (!this.state.guardId) {
            return;
        }
        await this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Projection de trésorerie",
            res_model: "dorevia.cash.guard",
            res_id: this.state.guardId,
            views: [[false, "form"]],
            target: "current",
        });
    }

    async onOpenGuardList() {
        await this.actionService.doAction("dorevia_cash_guard.action_dorevia_cash_guard");
    }

    async onOpenTrajectoryWizard() {
        await this.actionService.doAction("dorevia_cash_flow.action_dorevia_cash_flow_trajectory_wizard");
    }

    async onOpenReferenceTrajectoryMenu() {
        await this.actionService.doAction("dorevia_cash_flow.action_dorevia_cash_flow_trajectory_reference");
    }

    async onCockpitRefresh() {
        if (!this.state.guardId || !this.state.wizardId) {
            return;
        }
        this.state.cockpitRefreshing = true;
        try {
            await this.orm.call("dorevia.cash.guard", "action_recompute_projection", [
                this.state.guardId,
            ]);
            await this.orm.call(
                "dorevia.cash.flow.trajectory.wizard",
                "action_refresh_points_from_guard",
                [this.state.wizardId]
            );
            await this.loadTrajectory();
        } finally {
            this.state.cockpitRefreshing = false;
        }
    }
}

registry.category("actions").add("dorevia_cash_flow_trajectory_chart", TrajectoryChartAction);
