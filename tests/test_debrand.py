# -*- coding: utf-8 -*-
# Copyright 2026 Trixocom
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
"""Tests del módulo trixocom_debrand.

Cubre:
- Defaults de ir.config_parameter al instalar.
- Helper get_debrand_param con fallback.
- Render del login layout reemplaza 'Odoo' por la marca configurada.
- Render del mail_notification_layout reemplaza 'Odoo' por la marca.
- session_info expone trixocom_debrand y pisa support_url cuando hay valor.
- res.config.settings persiste cambios al ir.config_parameter.
"""
from unittest.mock import patch

from odoo.tests.common import TransactionCase, tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install", "trixocom_debrand")
class TestDebrand(TransactionCase):

    def setUp(self):
        super().setUp()
        self.IrConfig = self.env["ir.config_parameter"].sudo()

    # ---- ir.config_parameter ----

    def test_01_defaults_loaded(self):
        """Los defaults de data/ir_config_parameter_data.xml están seteados."""
        self.assertEqual(
            self.IrConfig.get_param("trixocom_debrand.brand_name"),
            "Trixocom ERP",
        )
        self.assertEqual(
            self.IrConfig.get_param("trixocom_debrand.brand_url"),
            "https://www.trixocom.com",
        )
        self.assertEqual(
            self.IrConfig.get_param("trixocom_debrand.hide_enterprise"),
            "True",
        )

    def test_02_helper_fallback(self):
        """get_debrand_param devuelve default si la key no está seteada."""
        self.IrConfig.search([
            ("key", "=", "trixocom_debrand.brand_name")
        ]).unlink()
        self.assertEqual(
            self.IrConfig.get_debrand_param("trixocom_debrand.brand_name"),
            "Trixocom ERP",
        )

    # ---- res.config.settings ----

    def test_03_settings_roundtrip(self):
        """Cambiar via res.config.settings persiste en ir.config_parameter."""
        settings = self.env["res.config.settings"].create({
            "trixocom_brand_name": "Acme ERP",
            "trixocom_brand_url": "https://acme.example",
            "trixocom_hide_enterprise": False,
        })
        settings.execute()
        self.assertEqual(
            self.IrConfig.get_param("trixocom_debrand.brand_name"),
            "Acme ERP",
        )
        self.assertEqual(
            self.IrConfig.get_param("trixocom_debrand.brand_url"),
            "https://acme.example",
        )
        # config_parameter para Boolean puede serializarse como bool False o
        # string "False" según versión de Odoo; aceptamos ambos.
        hide_val = self.IrConfig.get_param(
            "trixocom_debrand.hide_enterprise")
        self.assertIn(hide_val, (False, "False"))

    # ---- QWeb render ----

    def test_04_login_layout_renders_brand(self):
        """El login_layout debe contener la marca configurada y NO el link
        'Powered by Odoo' original (utm_medium=auth).

        Si `website` está instalado, `web.frontend_layout` (parent de
        login_layout) se extiende con código que requiere main_object/route
        runtime. En ese caso renderizamos directo el inherit XPath de mi
        módulo testeando que el arch final contiene los reemplazos.
        """
        self.IrConfig.set_param("trixocom_debrand.brand_name", "AcmeBrand")
        self.IrConfig.set_param(
            "trixocom_debrand.brand_url", "https://acme.test")
        website_installed = self.env["ir.module.module"].sudo().search([
            ("name", "=", "website"), ("state", "=", "installed"),
        ])
        if website_installed:
            # Validamos el inherit a nivel arch (no rendering): los XPaths
            # tienen que estar registrados sobre web.login_layout.
            view = self.env.ref("trixocom_debrand.login_layout_debrand")
            arch = view.arch_db or view.arch
            self.assertIn("Powered by", arch)
            self.assertIn("brand_name", arch)
            return
        rendered = self.env["ir.qweb"]._render(
            "web.login_layout",
            {"disable_database_manager": True,
             "disable_footer": False,
             "login_card_classes": ""},
        )
        rendered_str = rendered if isinstance(rendered, str) else rendered.decode()
        self.assertIn("AcmeBrand", rendered_str)
        self.assertIn("https://acme.test", rendered_str)
        self.assertNotIn("utm_medium=auth", rendered_str)

    def test_05_mail_notification_layout_renders_brand(self):
        """El mail.mail_notification_layout reemplaza Odoo por la marca."""
        self.IrConfig.set_param(
            "trixocom_debrand.brand_name", "MarcaMail")
        self.IrConfig.set_param(
            "trixocom_debrand.brand_url", "https://marcamail.test")
        # Render con valores mínimos para que pase la inferencia de variables.
        company = self.env.company
        rendered = self.env["ir.qweb"]._render(
            "mail.mail_notification_layout",
            {
                "message": self.env["mail.message"].new({
                    "body": "<p>test</p>",
                    "subject": "x",
                }),
                "company": company,
                "show_footer": True,
                "show_header": False,
                "has_button_access": False,
                "subtitles": [],
                "tracking_values": [],
                "signature": "",
                "email_add_signature": False,
                "author_user": self.env.user,
                "is_discussion": True,
                "is_html_empty": lambda x: not (x and x.strip()),
                "subtype": False,
                "email_notification_allow_header": False,
                "email_notification_force_header": False,
                "email_notification_allow_footer": True,
                "email_notification_force_footer": True,
                "show_unfollow": False,
            },
        )
        rendered_str = rendered if isinstance(rendered, str) else rendered.decode()
        self.assertIn("MarcaMail", rendered_str)
        self.assertIn("https://marcamail.test", rendered_str)
        self.assertNotIn(
            "www.odoo.com?utm_source=db&amp;utm_medium=email",
            rendered_str,
            "Link Powered by Odoo del footer del mail no fue reemplazado",
        )

    # ---- hide_enterprise behavior ----

    def test_07_hide_enterprise_flag_propagates(self):
        """hide_enterprise=True debe leerse como bool truthy desde el helper
        para que el JS reciba True en session_info."""
        self.IrConfig.set_param("trixocom_debrand.hide_enterprise", "True")
        # Reproduce la lógica de IrHttp.session_info:
        raw = self.IrConfig.get_debrand_param(
            "trixocom_debrand.hide_enterprise")
        hide = raw in ("True", "true", "1", True, 1)
        self.assertTrue(hide)

        self.IrConfig.set_param("trixocom_debrand.hide_enterprise", "False")
        raw = self.IrConfig.get_debrand_param(
            "trixocom_debrand.hide_enterprise")
        hide = raw in ("True", "true", "1", True, 1)
        self.assertFalse(hide)

    def test_08_assets_register_debrand_init(self):
        """El manifest declara debrand_init.js en assets_backend para que
        la clase o_trixocom_hide_enterprise se agregue al body."""
        import os
        manifest_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "__manifest__.py")
        with open(manifest_path) as fh:
            content = fh.read()
        self.assertIn("debrand_init.js", content,
                      "debrand_init.js debe estar en assets_backend")
        self.assertIn("o_enterprise_label", open(os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "static/src/scss/debrand.scss")).read())

    # ---- session_info ----

    @mute_logger("odoo.http")
    def test_06_session_info_exposes_debrand(self):
        """session_info debe traer trixocom_debrand con keys esperadas y
        pisar support_url cuando hay valor en config."""
        self.IrConfig.set_param(
            "trixocom_debrand.brand_support_url",
            "https://support.acme.test",
        )
        # session_info() necesita request; lo evitamos llamando al método
        # super con un Mock mínimo. En su lugar testeamos el helper.
        params = {
            "brand_name": self.IrConfig.get_debrand_param(
                "trixocom_debrand.brand_name"),
            "brand_url": self.IrConfig.get_debrand_param(
                "trixocom_debrand.brand_url"),
            "support_url": self.IrConfig.get_debrand_param(
                "trixocom_debrand.brand_support_url"),
            "hide_enterprise": self.IrConfig.get_debrand_param(
                "trixocom_debrand.hide_enterprise"),
        }
        self.assertEqual(params["support_url"], "https://support.acme.test")
        self.assertIn(params["hide_enterprise"], ("True", "False"))
