/** @odoo-module **/

import { onMounted, onWillUnmount } from "@odoo/owl";
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";

const GLC_COCKPIT_FILTER_FIELDS = new Set([
    "date_from",
    "date_to",
    "budget_scenario",
    "company_id",
    "activity_account_id",
    "reference_bank_journal_id",
]);

export class GlcCoverageCockpitFormController extends FormController {
    setup() {
        super.setup(...arguments);
        this.display.controlPanel = false;
        this._patchedRecords = new WeakSet();
        onMounted(() => {
            this._patchCockpitRecord();
            this._rootObserver = setInterval(() => this._patchCockpitRecord(), 250);
        });
        onWillUnmount(() => {
            if (this._rootObserver) {
                clearInterval(this._rootObserver);
            }
        });
    }

    async onWillSaveRecord(record, changes) {
        if (record.resModel !== "glc.coverage.cockpit") {
            return true;
        }
        delete changes.line_ids;
        delete changes.treasury_line_ids;
        for (const fieldName of Object.keys(changes)) {
            if (!GLC_COCKPIT_FILTER_FIELDS.has(fieldName)) {
                delete changes[fieldName];
            }
        }
        return true;
    }

    _patchCockpitRecord() {
        const record = this.model.root;
        if (
            !record ||
            record.resModel !== "glc.coverage.cockpit" ||
            this._patchedRecords.has(record)
        ) {
            return;
        }
        this._patchedRecords.add(record);
        const originalUpdate = record.update.bind(record);
        record.update = async (changes, options = {}) => {
            const result = await originalUpdate(changes, options);
            const hasFilterChange = Object.keys(changes).some((fieldName) =>
                GLC_COCKPIT_FILTER_FIELDS.has(fieldName)
            );
            if (hasFilterChange && record.resId && !options.save) {
                await record.save();
            }
            return result;
        };
    }
}

export const glcCoverageCockpitFormView = {
    ...formView,
    Controller: GlcCoverageCockpitFormController,
};

registry.category("views").add("glc_coverage_cockpit_form", glcCoverageCockpitFormView);
