# -*- coding: utf-8 -*-
# Copyright 2026 Trixocom
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
from odoo import models


class IrHttp(models.AbstractModel):
    """Inyecta los parámetros de debrand en session_info y en el contexto
    QWeb para que las plantillas (web.layout, login, mails, reports) puedan
    consumirlos sin tocar literales 'Odoo'.
    """

    _inherit = "ir.http"

    def session_info(self):
        result = super().session_info()
        IrConfig = self.env["ir.config_parameter"].sudo()
        brand_name = IrConfig.get_debrand_param("trixocom_debrand.brand_name")
        brand_url = IrConfig.get_debrand_param("trixocom_debrand.brand_url")
        doc_url = IrConfig.get_debrand_param(
            "trixocom_debrand.brand_documentation_url")
        support_url = IrConfig.get_debrand_param(
            "trixocom_debrand.brand_support_url")
        hide_ent = IrConfig.get_debrand_param(
            "trixocom_debrand.hide_enterprise") in (
                "True", "true", "1", True, 1)
        favicon_url = IrConfig.get_debrand_param(
            "trixocom_debrand.favicon_url")

        # Pisar el support_url default de web/models/ir_http.py línea 109
        # ("https://www.odoo.com/buy"). Si el admin lo dejó vacío, dejamos
        # el de Odoo para no romper el menú de soporte.
        if support_url:
            result["support_url"] = support_url

        result["trixocom_debrand"] = {
            "brand_name": brand_name,
            "brand_url": brand_url,
            "documentation_url": doc_url,
            "support_url": support_url,
            "hide_enterprise": hide_ent,
            "favicon_url": favicon_url,
        }
        return result
