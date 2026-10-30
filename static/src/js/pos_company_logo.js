/** @odoo-module **/
// Copyright 2026 Trixocom
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
//
// Logo de la empresa en el POS (barra y pantalla de reposo) con una URL
// propia de la empresa de la caja y un parametro que cambia en cada apertura.
// La URL generica /web/binary/company_logo es la misma para todas las
// empresas y Odoo la entrega con cache de 7 dias: una PC que la cargo con otra
// empresa (o con el logo anterior) seguia mostrando ese logo aunque se
// recargara. pos_debrand.scss usa --trx-company-logo con company_logo como
// respaldo.

import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";

patch(PosStore.prototype, {
    async afterProcessServerData() {
        const res = await super.afterProcessServerData(...arguments);
        this.trxSetCompanyLogo();
        return res;
    },

    trxSetCompanyLogo() {
        const companyId = this.company?.id || this.config?.company_id?.id;
        if (!companyId) {
            return;
        }
        const url = `/web/binary/company_logo?company=${companyId}&unique=${Date.now()}`;
        document.documentElement.style.setProperty("--trx-company-logo", `url("${url}")`);
    },
});
