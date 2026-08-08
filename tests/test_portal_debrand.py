# -*- coding: utf-8 -*-
# Copyright 2026 Trixocom
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
"""Tests de los overrides de portal.

Se validan sobre el arch combinado (``get_combined_arch``) y no renderizando,
porque el render de estos templates necesita un request HTTP real (portal con
access_token).

Los del sitio web viven en trixocom_debrand_website (repo
trixocom-debrand-apps), que es donde quedaron esos overrides desde la
19.0.3.0.0.
"""
from lxml import etree

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install", "trixocom_debrand")
class TestPortalDebrand(TransactionCase):

    def _arch(self, xmlid):
        return self.env.ref(xmlid).get_combined_arch()

    def test_01_portal_sidebar_sin_logo_odoo(self):
        """El 'Powered by <logo odoo>' del sidebar del portal se reemplaza."""
        arch = self._arch("portal.portal_record_sidebar")
        self.assertNotIn("odoo.com", arch)
        self.assertNotIn("Odoo Logo", arch)
        self.assertIn("trixocom_debrand.brand_name", arch)
        self.assertIn("Powered by", arch)

    def test_02_portal_security_doc_links(self):
        """Los DOS links de doc (2FA y API keys) apuntan al parametro."""
        arch = self._arch("portal.portal_my_security")
        self.assertNotIn("odoo.com", arch)
        self.assertEqual(
            arch.count("trixocom_debrand.brand_documentation_url"), 2,
            "Se esperaban 2 links de documentacion redirigidos (2FA y API "
            "keys). Si Odoo agrego o saco uno, ajustar "
            "views/portal_templates.xml.")

    def test_03_no_depende_de_website(self):
        """El modulo base NO debe depender de website: eso obligaria a
        instalar el modulo Website completo en clientes que no lo usan.
        Los overrides del sitio viven en trixocom_debrand_website."""
        mod = self.env["ir.module.module"].sudo().search([
            ("name", "=", "trixocom_debrand")], limit=1)
        deps = mod.dependencies_id.mapped("name")
        for forbidden in ("website", "sale", "purchase", "website_sale"):
            self.assertNotIn(
                forbidden, deps,
                "trixocom_debrand no puede depender de %s; ese override va en "
                "un modulo puente auto_install." % forbidden)

    def test_04_xpaths_siguen_aplicando(self):
        """Si Odoo cambia el fuente y un XPath deja de matchear, el modulo no
        instala. Este test verifica ademas que los nodos objetivo existan,
        para detectar el problema en el update y no en runtime."""
        tree = etree.fromstring(self._arch("portal.portal_record_sidebar"))
        anchors = tree.xpath("//a[@t-att-href]")
        self.assertTrue(
            anchors,
            "El sidebar del portal perdio el link 'Powered by'; revisar el "
            "inherit portal_record_sidebar_debrand contra el fuente 19.0.")
