# -*- coding: utf-8 -*-
# Copyright 2026 Trixocom
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
"""El renombre del menú a «Contabilidad» pasó a ser el comportamiento por
defecto, sin switch. Las bases que venían de 19.0.3.3.0 tienen el parámetro
del switch: se aplica el renombre y se borra el parámetro, que ya no manda
nada (el que sí queda es el backup del nombre original)."""
from odoo.addons.trixocom_debrand.hooks import rename_accounting_menu


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["ir.config_parameter"].sudo().search(
        [("key", "=", "trixocom_debrand.rename_accounting_menu")]).unlink()
    rename_accounting_menu(env)
