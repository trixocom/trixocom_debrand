# -*- coding: utf-8 -*-
# Copyright 2026 Trixocom
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
"""Patch del controller Database para debrandear el database manager.

El archivo addons/web/static/src/public/database_manager.qweb.html es HTML
estático (no un template Odoo registrado), por lo que NO se puede heredar via
QWeb XPath. Lo único viable es post-procesar el HTML renderizado.

Heredar la clase Database y override _render_template NO surte efecto: las
rutas (@http.route) están registradas contra la clase original Database, no
contra la subclase, por lo que el método llamado en runtime es el original.

Por eso usamos monkey-patch del método _render_template directamente sobre
Database, que es la forma usada por varios módulos OCA cuando el método a
patchear no es un endpoint en sí mismo sino un helper.
"""
import logging
import re

from odoo import http
from odoo.addons.web.controllers.database import Database

_logger = logging.getLogger(__name__)

# Guardamos referencia al original una sola vez por proceso.
_ORIGINAL_RENDER_TEMPLATE = Database._render_template


def _read_brand_from_any_db():
    """El database manager corre con auth='none' antes de seleccionar DB —
    no hay cursor disponible en http.request.env. Como fallback, abrimos un
    cursor sobre la primera DB listada para leer los ir.config_parameter del
    debrand. Si no hay ninguna DB o no se puede leer, devolvemos los defaults.
    """
    defaults = ("Trixocom ERP", "https://www.trixocom.com")
    try:
        import odoo
        db_names = odoo.service.db.list_dbs(force=True)
    except Exception:
        return defaults
    if not db_names:
        return defaults
    db_name = db_names[0]
    try:
        registry = odoo.modules.registry.Registry(db_name)
        with registry.cursor() as cr:
            cr.execute(
                "SELECT key, value FROM ir_config_parameter "
                "WHERE key IN ('trixocom_debrand.brand_name', "
                "'trixocom_debrand.brand_url')"
            )
            params = dict(cr.fetchall())
        return (
            params.get("trixocom_debrand.brand_name", defaults[0]),
            params.get("trixocom_debrand.brand_url", defaults[1]),
        )
    except Exception:
        return defaults


def _trixocom_render_template(self, **d):
    response = _ORIGINAL_RENDER_TEMPLATE(self, **d)
    try:
        # Intento 1: leer desde http.request.env (válido sólo si la request
        # ya tiene una DB seleccionada — no es el caso del database manager).
        brand_name = brand_url = None
        if http.request and getattr(http.request, "db", None):
            try:
                IrConfig = http.request.env["ir.config_parameter"].sudo()
                brand_name = IrConfig.get_param(
                    "trixocom_debrand.brand_name")
                brand_url = IrConfig.get_param(
                    "trixocom_debrand.brand_url")
            except Exception:
                brand_name = brand_url = None
        # Intento 2 / fallback: cursor directo sobre la primera DB.
        if not brand_name or not brand_url:
            brand_name, brand_url = _read_brand_from_any_db()

        is_str = isinstance(response, str)
        body = response if is_str else getattr(response, "data", None)
        if body is None:
            return response
        if isinstance(body, bytes):
            body = body.decode("utf-8")

        body = re.sub(
            r"<title>\s*Odoo\s*</title>",
            f"<title>{brand_name}</title>",
            body,
        )
        body = body.replace(
            "Your Odoo database manager",
            f"Your {brand_name} database manager",
        )
        body = body.replace(
            "https://www.odoo.com/privacy",
            brand_url,
        )
        body = body.replace(
            "to Odoo online services",
            f"to {brand_name} online services",
        )
        body = body.replace(
            "Odoo needs to know",
            f"{brand_name} needs to know",
        )

        if is_str:
            return body
        response.data = body.encode("utf-8")
        return response
    except Exception:
        _logger.exception("trixocom_debrand: error post-processing "
                          "database manager template; returning original")
        return response


Database._render_template = _trixocom_render_template
