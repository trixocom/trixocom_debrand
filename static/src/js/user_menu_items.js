/** @odoo-module **/
// Copyright 2026 Trixocom
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
//
// Saca el item "My Odoo.com Account" del user menu y registra un item
// alternativo "documentation" si el admin definió una URL en
// ir.config_parameter trixocom_debrand.brand_documentation_url
// (expuesto via session_info -> trixocom_debrand.documentation_url).
//
// Referencia (no copia): el comportamiento del user_menu está documentado en
// addons/web/static/src/webclient/user_menu/user_menu_items.js (rama 19.0)
// y usa registry.category("user_menuitems").
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { session } from "@web/session";
import { browser } from "@web/core/browser/browser";

const userMenuRegistry = registry.category("user_menuitems");

// Sacar "My Odoo.com Account" — siempre que esté presente.
if (userMenuRegistry.contains("odoo_account")) {
    userMenuRegistry.remove("odoo_account");
}

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

userMenuRegistry.add("trixocom_documentation", documentationItem);
