# -*- coding: utf-8 -*-
# Copyright 2026 Trixocom
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
{
    "name": "Trixocom Debrand",
    "summary": "Reemplaza referencias a Odoo y oculta opciones Enterprise. "
               "Marca, URLs y links de documentación configurables por sistema.",
    "description": """
Trixocom Debrand
================

Reemplaza las referencias a la marca *Odoo* y a opciones *Enterprise* dentro del
backend, mails, reportes y links de documentación.

Todo es configurable vía *Settings → General Settings → Trixocom Debrand*:

* Nombre de marca (default: *Trixocom ERP*)
* URL principal, documentación y soporte
* Favicon
* Ocultar referencias a opciones / módulos Enterprise

El módulo está pensado para Odoo Community 19.0 — no reemplaza requisitos de
licencia y no remueve atribuciones de copyright del código original.
""",
    "version": "19.0.1.6.0",
    "category": "Extra Tools",
    "author": "Trixocom",
    "website": "https://www.trixocom.com",
    "license": "LGPL-3",
    "depends": [
        "base",
        "base_setup",
        "web",
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_config_parameter_data.xml",
        "views/res_config_settings_views.xml",
        "views/webclient_templates.xml",
        "views/login_templates.xml",
        "views/mail_templates.xml",
        "views/report_templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "trixocom_debrand/static/src/scss/debrand.scss",
            "trixocom_debrand/static/src/js/debrand_init.js",
            "trixocom_debrand/static/src/js/user_menu_items.js",
            "trixocom_debrand/static/src/xml/user_menu.xml",
            "trixocom_debrand/static/src/xml/upgrade_dialog.xml",
        ],
        "web.assets_frontend": [
            "trixocom_debrand/static/src/scss/debrand_frontend.scss",
        ],
    },
    "images": [
        "static/description/icon.png",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
