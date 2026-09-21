# -*- coding: utf-8 -*-
# Copyright 2026 Trixocom
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
"""Reaplica el renombre del menu para tomar tambien el en_US.

El post_init_hook corre solo al instalar, asi que las bases que ya tenian el
modulo necesitan esta migracion para quedar con el nombre nuevo."""
from odoo.addons.trixocom_debrand.hooks import rename_accounting_menu


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    rename_accounting_menu(api.Environment(cr, SUPERUSER_ID, {}))
