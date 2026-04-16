/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Navbar } from "@point_of_sale/app/components/navbar/navbar";
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { isPrivateIp } from "@point_of_sale/utils";

/**
 * Contournement si build Odoo sans le correctif isPrivateIp (non-chaîne) :
 * `epson_printer_ip` peut être false côté RPC avant garde type.
 */
function safeIsPrivateIp(ip) {
    if (!ip || typeof ip !== "string") {
        return false;
    }
    return isPrivateIp(ip);
}

patch(Navbar.prototype, {
    async openLnaPopup() {
        let localPrinterIp;
        if (safeIsPrivateIp(this.pos.config.epson_printer_ip)) {
            localPrinterIp = this.pos.config.epson_printer_ip;
        }
        if (!localPrinterIp) {
            for (const printer of this.pos.config.printer_ids) {
                if (safeIsPrivateIp(printer.epson_printer_ip)) {
                    localPrinterIp = printer.epson_printer_ip;
                }
            }
        }
        if (localPrinterIp) {
            try {
                const protocol = "http:";
                const url = protocol + "//" + localPrinterIp;
                this.address = url + "/cgi-bin/epos/service.cgi?devid=local_printer";
                const params = {
                    method: "POST",
                    body: `<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
                            <s:Body>
                                <epos-print xmlns="http://www.epson-pos.com/schemas/2011/03/epos-print">
                                    <feed line="1" />
                                    <text align="center">This is a test receipt&#10;</text>
                                    <feed line="3" />
                                    <cut type="feed" />
                                </epos-print>
                            </s:Body>
                        </s:Envelope>`,
                    signal: AbortSignal.timeout(15000),
                };
                await fetch(this.address, params);
                return;
            } catch {
                console.error("Could not connect to printer");
            }
        }
        this.dialog.add(AlertDialog, {
            title: _t("LNA Permission status"),
            body: this.pos.lnaState.message,
        });
    },
});
