# -*- coding: utf-8 -*-
# Copyright 2026 Trixocom
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
"""Icono de la PWA (la app que el usuario instala en el celular).

Odoo sirve en /web/manifest.webmanifest los iconos morados de Odoo. Cuando el
usuario instala la app, esos iconos son los que quedan en la pantalla de inicio
y —lo que mas se nota— los que identifican cada notificacion push: sin PWA
instalada la notificacion figura como del navegador, y con la PWA de Odoo figura
con el logo de Odoo. Aca se reemplazan por el logo de la compania (o el que se
configure), dejando el resto del manifest como lo arma web.
"""
import base64
import io
import logging

from odoo import http
from odoo.http import request

from odoo.addons.web.controllers.webmanifest import WebManifest

_logger = logging.getLogger(__name__)

#: tamanos que pide el manifest (Android usa 192 para la notificacion y el
#: launcher, 512 para el splash / Play Store).
ICON_SIZES = (192, 512)

#: margen alrededor del logo, en % del lado: un poco de aire para que el recorte
#: redondeado de Android no le coma los bordes, sin desperdiciar el cuadrado. Un
#: logo apaisado igual va a quedar como una franja centrada: para esos casos esta
#: el parametro "PWA Icon URL", que permite cargar un icono cuadrado propio.
ICON_MARGIN_RATIO = 0.06

PARAM_PWA_ICON_URL = "trixocom_debrand.pwa_icon_url"
PARAM_PWA_ICON_BG = "trixocom_debrand.pwa_icon_bg"
DEFAULT_ICON_BG = "#FFFFFF"


def _hex_to_rgb(value, fallback=(255, 255, 255)):
    value = (value or "").strip().lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    if len(value) != 6:
        return fallback
    try:
        return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return fallback


class WebManifestDebrand(WebManifest):

    # ------------------------------------------------------------------ #
    #  Manifest
    # ------------------------------------------------------------------ #
    def _get_webmanifest(self):
        manifest = super()._get_webmanifest()
        IrConfig = request.env["ir.config_parameter"].sudo()
        custom = (IrConfig.get_param(PARAM_PWA_ICON_URL) or "").strip()
        if custom:
            manifest["icons"] = [{
                "src": custom,
                "sizes": "any",
                "type": "image/png",
            }]
            return manifest
        if not self._debrand_pwa_logo():
            # Sin logo de compania no hay nada mejor que el icono de Odoo.
            return manifest
        manifest["icons"] = [{
            "src": "/trixocom_debrand/pwa_icon/%d.png" % size,
            "sizes": "%dx%d" % (size, size),
            "type": "image/png",
            "purpose": "any",
        } for size in ICON_SIZES]
        bg = IrConfig.get_param(PARAM_PWA_ICON_BG) or DEFAULT_ICON_BG
        manifest["background_color"] = bg
        return manifest

    # ------------------------------------------------------------------ #
    #  Icono generado a partir del logo de la compania
    # ------------------------------------------------------------------ #
    def _debrand_pwa_logo(self):
        """Logo de la compania en binario, o False."""
        company = request.env.company.sudo()
        if not company:
            company = request.env["res.company"].sudo().search([], limit=1)
        logo = company.logo
        if not logo:
            return False
        try:
            return base64.b64decode(logo)
        except Exception:  # noqa: BLE001
            return False

    @http.route("/trixocom_debrand/pwa_icon/<int:size>.png", type="http",
                auth="public", methods=["GET"], readonly=True)
    def debrand_pwa_icon(self, size, **kw):
        if size not in ICON_SIZES:
            size = ICON_SIZES[0]
        raw = self._debrand_pwa_logo()
        if not raw:
            return request.not_found()
        bg = _hex_to_rgb(request.env["ir.config_parameter"].sudo().get_param(
            PARAM_PWA_ICON_BG) or DEFAULT_ICON_BG)
        try:
            png = self._debrand_square_png(raw, size, bg)
        except Exception:  # noqa: BLE001 - un icono no debe tirar el manifest
            _logger.exception("No se pudo generar el icono PWA")
            return request.not_found()
        return request.make_response(png, headers=[
            ("Content-Type", "image/png"),
            ("Cache-Control", "public, max-age=86400"),
        ])

    def _debrand_square_png(self, raw, size, background):
        """Logo centrado sobre un lienzo cuadrado opaco. Cuadrado porque el
        manifest declara 192x192/512x512 y Android descarta el icono si no
        coincide; opaco porque la transparencia sobre fondo oscuro deja el logo
        invisible."""
        from PIL import Image  # Pillow ya es dependencia de Odoo

        margin = int(size * ICON_MARGIN_RATIO)
        box = max(size - 2 * margin, 1)
        src = Image.open(io.BytesIO(raw))
        if src.mode != "RGBA":
            src = src.convert("RGBA")
        src.thumbnail((box, box), Image.LANCZOS)
        canvas = Image.new("RGBA", (size, size), tuple(background) + (255,))
        canvas.paste(src, ((size - src.width) // 2, (size - src.height) // 2), src)
        out = io.BytesIO()
        canvas.convert("RGB").save(out, format="PNG", optimize=True)
        return out.getvalue()
