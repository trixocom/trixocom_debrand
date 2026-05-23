/** @odoo-module **/
// Copyright 2026 Trixocom
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
//
// Saca el item "My Odoo.com Account" del user menu y registra un item
// alternativo "Documentation" si el admin definió una URL en
// ir.config_parameter trixocom_debrand.brand_documentation_url
// (expuesto via session_info.trixocom_debrand.documentation_url).
//
// IMPLEMENTACIÓN: registry.remove() puede ejecutarse antes que `web` haga
// .add("odoo_account", ...), quedando un add posterior que neutraliza el
// remove. Para evitar la dependencia de orden de carga:
//   1) Forzamos un add con un item que tiene hide:()=>true, pisando lo que
//      pudiera haber (force:true sobre la misma key).
//   2) Adicionalmente, listener al evento UPDATE: si alguien re-registra
//      "odoo_account" con otro callback, lo volvemos a forzar.
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { session } from "@web/session";
import { browser } from "@web/core/browser/browser";

const userMenuRegistry = registry.category("user_menuitems");

function hiddenOdooAccountItem(env) {
    return {
        type: "item",
        id: "odoo_account",
        description: "",
        hide: true,
        callback: () => {},
        sequence: 60,
    };
}

userMenuRegistry.add("odoo_account", hiddenOdooAccountItem, { force: true });

// Defensa contra re-registros posteriores por otros módulos / theme.
userMenuRegistry.addEventListener("UPDATE", (ev) => {
    if (!ev.detail || ev.detail.operation !== "add") return;
    if (ev.detail.key !== "odoo_account") return;
    // Si el callback agregado no es el nuestro, lo pisamos.
    const current = userMenuRegistry.content["odoo_account"];
    if (current && current[1] !== hiddenOdooAccountItem) {
        userMenuRegistry.add("odoo_account", hiddenOdooAccountItem,
                             { force: true });
    }
});

// Agregar item "Documentation" si hay URL configurada.
function documentationItem(env) {
    const url = session.trixocom_debrand && session.trixocom_debrand.documentation_url;
    return {
        type: "item",
        id: "trixocom_documentation",
        description: _t("Documentation"),
        href: url,
        hide: !url,
        callback: () => {
            if (url) {
                browser.open(url, "_blank");
            }
        },
        sequence: 15,
    };
}

userMenuRegistry.add("trixocom_documentation", documentationItem,
                     { force: true });
