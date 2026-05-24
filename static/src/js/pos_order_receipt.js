/** @odoo-module **/
// Copyright 2026 Trixocom
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
//
// Agrega un getter trixocomBrand al componente OrderReceipt del POS para que
// el template (pos_order_receipt.xml) pueda mostrar el nombre de marca en el
// footer "Powered by ..." del ticket.
import { patch } from "@web/core/utils/patch";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { session } from "@web/session";

patch(OrderReceipt.prototype, {
    get trixocomBrand() {
        const dbg = session && session.trixocom_debrand;
        return (dbg && dbg.brand_name) || "Trixocom ERP";
    },
});
