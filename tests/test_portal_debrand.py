# -*- coding: utf-8 -*-
# Copyright 2026 Trixocom
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
"""Tests de los overrides de portal y website.

Se validan sobre el arch combinado (``get_combined_arch``) y no renderizando,
porque el render de estos templates necesita un request HTTP real (portal con
access_token, website con main_object/route).
"""
from lxml import etree

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install", "trixocom_debrand")
class TestPortalDebrand(TransactionCase):

    def _arch(self, xmlid):
        return self.env.ref(xmlid).get_combined_arch()

    # ---- portal ----

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

    # ---- website ----

    def test_03_brand_promotion_sin_free_website(self):
        """El footer del sitio no debe ofrecer 'Create a free website'."""
        arch = self._arch("web.brand_promotion")
        self.assertNotIn("odoo.com", arch)
        self.assertNotIn("free website", arch)

    def test_04_website_info_sin_referencias_odoo(self):
        """/website/info no debe nombrar a Odoo ni linkear a odoo.com."""
        arch = self._arch("website.website_info")
        self.assertNotIn("odoo.com", arch)
        self.assertNotIn("Odoo Version", arch)
        self.assertNotIn("instance of Odoo", arch)

    # ---- guardas contra cambios de upstream ----

    def test_05_xpaths_siguen_aplicando(self):
        """Si Odoo cambia el fuente y un XPath deja de matchear, el modulo no
        instala. Este test verifica ademas que los nodos objetivo existan y
        sean unicos, para detectar el problema en el update y no en runtime.
        """
        tree = etree.fromstring(self._arch("portal.portal_record_sidebar"))
        anchors = tree.xpath("//a[@t-att-href]")
        self.assertTrue(
            anchors,
            "El sidebar del portal perdio el link 'Powered by'; revisar el "
            "inherit portal_record_sidebar_debrand contra el fuente 19.0.")
