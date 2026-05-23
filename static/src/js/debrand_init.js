/** @odoo-module **/
// Copyright 2026 Trixocom
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
//
// 1) Marca el <html> con o_trixocom_hide_enterprise cuando el admin pidió
//    ocultar las referencias Enterprise. El CSS en debrand.scss usa esa clase.
// 2) Fallback JS: navegadores sin :has() o cualquier .o_setting_box que el
//    selector :has() no haya alcanzado se marca con o_tx_hidden_by_enterprise.
// 3) Limpieza de blocks vacíos: si todas las opciones de un container
//    quedaron ocultas (todas eran enterprise), marca el h2 título y el
//    container para esconderlos también.
//
// Se usa MutationObserver porque en Settings los settings se renderizan
// dinámicamente al cambiar de "app" sin recargar la página.
import { session } from "@web/session";

const debrand = session && session.trixocom_debrand;
if (debrand && debrand.hide_enterprise) {
    document.documentElement.classList.add("o_trixocom_hide_enterprise");

    const hideEnterpriseBoxes = (root) => {
        // 1) ocultar .o_setting_box que contiene un .o_enterprise_label
        const boxes = root.querySelectorAll(
            ".o_setting_box:not(.o_tx_hidden_by_enterprise)"
        );
        boxes.forEach((box) => {
            if (box.querySelector(".o_enterprise_label")) {
                box.classList.add("o_tx_hidden_by_enterprise");
            }
        });

        // 2) si un .o_settings_container queda sin .o_setting_box visibles,
        //    ocultar el container y el h2 inmediatamente anterior.
        const containers = root.querySelectorAll(".o_settings_container");
        containers.forEach((cont) => {
            const visibleBoxes = cont.querySelectorAll(
                ".o_setting_box:not(.o_tx_hidden_by_enterprise)"
            );
            if (visibleBoxes.length === 0) {
                cont.classList.add("o_tx_empty_by_enterprise");
                let prev = cont.previousElementSibling;
                while (prev && !prev.matches("h2, h3, .o_setting_section_header")) {
                    prev = prev.previousElementSibling;
                }
                if (prev) {
                    prev.classList.add("o_tx_empty_by_enterprise");
                }
            } else {
                cont.classList.remove("o_tx_empty_by_enterprise");
            }
        });
    };

    const onReady = () => {
        hideEnterpriseBoxes(document.body);
        const obs = new MutationObserver((mutations) => {
            // Throttling implícito: si llegan muchas, una pasada cubre todo.
            for (const m of mutations) {
                if (m.addedNodes.length) {
                    hideEnterpriseBoxes(document.body);
                    break;
                }
            }
        });
        obs.observe(document.body, { childList: true, subtree: true });
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", onReady, { once: true });
    } else {
        onReady();
    }
}
