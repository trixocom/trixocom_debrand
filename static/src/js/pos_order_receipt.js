/** @odoo-module **/
// Copyright 2026 Trixocom
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
//
// Estrategia DOM post-render: el inherit XML del template OrderReceipt
// rompía el POS (body vacío). Aquí patcheamos el componente para que en
// el mounted() y patched() reemplace el contenido del <b>Odoo</b> dentro
// del footer .pos-receipt-order-data por el brand_name configurado.
//
// Ventaja: NO modificamos el template QWeb, ni el bundle XML. Solo
// manipulamos el DOM después de que OWL renderizó. Sin riesgo de romper
// el render.
import { patch } from "@web/core/utils/patch";
import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { onMounted, onPatched } from "@odoo/owl";
import { session } from "@web/session";

function getBrand() {
    const dbg = session && session.trixocom_debrand;
    return (dbg && dbg.brand_name) || "Trixocom ERP";
}

function rebrandReceiptFooter(rootEl) {
    if (!rootEl) return;
    const brand = getBrand();
    // El footer del ticket es:
    //   <div class="pos-receipt-order-data text-center pt-3">
    //     <span>Powered by <b> Odoo </b></span>
    //   </div>
    // Reemplazamos el text content del <b> que contenga 'Odoo'.
    const target = rootEl.matches?.(".pos-receipt-order-data")
        ? rootEl
        : rootEl.querySelector?.(".pos-receipt-order-data");
    if (!target) return;
    target.querySelectorAll("b").forEach((b) => {
        if (b.textContent.includes("Odoo")) {
            b.textContent = brand;
        }
    });
}

patch(OrderReceipt.prototype, {
    setup() {
        super.setup();
        const apply = () => {
            // this.__owl__ no es API pública, usamos document.querySelectorAll
            // como fallback robusto: aplicamos a TODOS los receipts visibles.
            document
                .querySelectorAll(".pos-receipt-order-data")
                .forEach(rebrandReceiptFooter);
        };
        onMounted(apply);
        onPatched(apply);
    },
});
