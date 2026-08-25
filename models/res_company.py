# -*- coding: utf-8 -*-
# Copyright 2026 Trixocom
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    pwa_icon = fields.Image(
        string="Icono de la app (PWA)",
        max_width=512, max_height=512,
        help="Icono cuadrado de la app instalada en el celular. Es tambien el "
             "que identifica cada notificacion push. Vacio: se genera a partir "
             "del logo de la compania, que al ser apaisado suele quedar como "
             "una franja en medio de un cuadrado casi vacio.")
