# -*- coding: utf-8 -*-
# Copyright 2026 Trixocom
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).
import json
import logging

_logger = logging.getLogger(__name__)

PARAM_ACCOUNTING_MENU_BACKUP = "trixocom_debrand.accounting_menu_name_backup"

# Cómo se dice «Contabilidad» en cada idioma que podamos encontrar.
# La clave son los dos primeros caracteres del código de idioma.
NOMBRE_CONTABILIDAD = {
    "es": "Contabilidad",
    "pt": "Contabilidade",
    "it": "Contabilità",
    "fr": "Comptabilité",
    "en": "Accounting",
}


def rename_accounting_menu(env):
    """Llama «Contabilidad» al menú principal de Odoo.

    En Community ese menú se llama «Facturación», que es el nombre de una de
    sus partes, no del conjunto: ahí adentro están el plan de cuentas, los
    asientos, la conciliación y los reportes contables. Se renombra en todos
    los idiomas instalados.

    `account` no está en los depends a propósito: este módulo se instala
    también en bases sin contabilidad y forzarla ahí sería peor que no
    renombrar nada. Si el menú no existe, no hay nada que hacer; cuando se
    instale `account`, un `-u trixocom_debrand` lo deja con el nombre nuevo.

    Para volver atrás está el nombre original guardado en el parámetro del
    sistema `trixocom_debrand.accounting_menu_name_backup`.
    """
    menu = env.ref("account.menu_finance", raise_if_not_found=False)
    if not menu:
        return
    menu = menu.sudo()
    icp = env["ir.config_parameter"].sudo()
    # en_US va siempre: es el idioma de origen y el que ve cualquier usuario
    # cuyo idioma no esté instalado.
    idiomas = sorted(
        {code for code, _name in env["res.lang"].get_installed()} | {"en_US"})
    # El backup guarda el nombre original de cada idioma la primera vez que se
    # lo ve, sin pisar lo ya guardado.
    guardado = json.loads(icp.get_param(PARAM_ACCOUNTING_MENU_BACKUP) or "{}")
    faltantes = {
        code: menu.with_context(lang=code).name
        for code in idiomas if code not in guardado
    }
    if faltantes:
        guardado.update(faltantes)
        icp.set_param(PARAM_ACCOUNTING_MENU_BACKUP, json.dumps(guardado))
    menu.update_field_translations("name", {
        code: NOMBRE_CONTABILIDAD.get(code[:2], "Accounting") for code in idiomas
    })
    _logger.info(
        "trixocom_debrand: menu de Contabilidad renombrado en %s", idiomas)


def post_init_hook(env):
    rename_accounting_menu(env)
