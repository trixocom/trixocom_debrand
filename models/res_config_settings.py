# -*- coding: utf-8 -*-
# Copyright 2026 Trixocom
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
from odoo import api, fields, models

# Parámetros del sistema (ir.config_parameter) que controlan la marca.
# Se exponen como res.config.settings para que el admin los edite desde
# Settings → General Settings → Trixocom Debrand.
PARAM_BRAND_NAME = "trixocom_debrand.brand_name"
PARAM_BRAND_URL = "trixocom_debrand.brand_url"
PARAM_DOC_URL = "trixocom_debrand.brand_documentation_url"
PARAM_SUPPORT_URL = "trixocom_debrand.brand_support_url"
PARAM_HIDE_ENTERPRISE = "trixocom_debrand.hide_enterprise"
PARAM_FAVICON_URL = "trixocom_debrand.favicon_url"
PARAM_PWA_ICON_URL = "trixocom_debrand.pwa_icon_url"
PARAM_PWA_ICON_BG = "trixocom_debrand.pwa_icon_bg"

DEFAULT_BRAND_NAME = "Trixocom ERP"
DEFAULT_BRAND_URL = "https://www.trixocom.com"
DEFAULT_DOC_URL = "https://www.trixocom.com/documentation"
DEFAULT_SUPPORT_URL = "https://www.trixocom.com/support"



class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    trixocom_brand_name = fields.Char(
        string="Brand Name",
        config_parameter=PARAM_BRAND_NAME,
        default=DEFAULT_BRAND_NAME,
        help="Nombre de marca que reemplaza a 'Odoo' en el web client, "
             "mails y reportes.",
    )
    trixocom_brand_url = fields.Char(
        string="Brand URL",
        config_parameter=PARAM_BRAND_URL,
        default=DEFAULT_BRAND_URL,
        help="URL principal usada en footers y links 'Powered by'.",
    )
    trixocom_documentation_url = fields.Char(
        string="Documentation URL",
        config_parameter=PARAM_DOC_URL,
        default=DEFAULT_DOC_URL,
        help="URL de documentación. Vacío para ocultar el item del menú "
             "de usuario.",
    )
    trixocom_support_url = fields.Char(
        string="Support URL",
        config_parameter=PARAM_SUPPORT_URL,
        default=DEFAULT_SUPPORT_URL,
        help="URL de soporte. Vacío para ocultar el item del menú "
             "de usuario.",
    )
    trixocom_hide_enterprise = fields.Boolean(
        string="Hide Enterprise references",
        config_parameter=PARAM_HIDE_ENTERPRISE,
        default=True,
        help="Oculta banners y módulos Enterprise en Apps y Settings.",
    )
    trixocom_favicon_url = fields.Char(
        string="Favicon URL",
        config_parameter=PARAM_FAVICON_URL,
        help="Path absoluto (p.ej. /trixocom_debrand/static/src/img/favicon.ico) "
             "o URL externa. Vacío usa el favicon por defecto de la compañía.",
    )
    trixocom_pwa_icon = fields.Image(
        string="Icono de la app (PWA)",
        related="company_id.pwa_icon", readonly=False,
        help="Icono cuadrado de la app instalada en el celular, y de sus "
             "notificaciones. Vacío lo genera con el logo de la compañía.",
    )
    trixocom_pwa_icon_url = fields.Char(
        string="PWA Icon URL",
        config_parameter=PARAM_PWA_ICON_URL,
        help="Icono de la app instalada en el celular (y de sus notificaciones "
             "push). Vacío genera el icono a partir del logo de la compañía.",
    )
    trixocom_pwa_icon_bg = fields.Char(
        string="PWA Icon Background",
        config_parameter=PARAM_PWA_ICON_BG,
        help="Color de fondo del icono generado, en hexadecimal (default "
             "#FFFFFF). El icono tiene que ser opaco: sobre fondo oscuro un "
             "logo transparente queda invisible.",
    )


class IrConfigParameter(models.Model):
    """Helper para que el resto del módulo (templates QWeb, controllers) lea
    los parámetros con defaults consistentes sin repetir literales."""

    _inherit = "ir.config_parameter"

    @api.model
    def get_debrand_param(self, key, default=None):
        defaults = {
            PARAM_BRAND_NAME: DEFAULT_BRAND_NAME,
            PARAM_BRAND_URL: DEFAULT_BRAND_URL,
            PARAM_DOC_URL: DEFAULT_DOC_URL,
            PARAM_SUPPORT_URL: DEFAULT_SUPPORT_URL,
            PARAM_HIDE_ENTERPRISE: "True",
            PARAM_FAVICON_URL: "",
            PARAM_PWA_ICON_URL: "",
            PARAM_PWA_ICON_BG: "#FFFFFF",
        }
        value = self.sudo().get_param(key, defaults.get(key, default))
        return value
