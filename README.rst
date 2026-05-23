================
Trixocom Debrand
================

.. |badge_license| image:: https://img.shields.io/badge/licence-LGPL--3-blue.png
   :target: https://www.gnu.org/licenses/lgpl-3.0
   :alt: License: LGPL-3

|badge_license|

Reemplaza las referencias a la marca *Odoo* y oculta opciones *Enterprise*
en el backend, mails, reportes y links de documentación de Odoo Community 19.0.

Todo es configurable vía **Settings → General Settings → Trixocom Debrand**:

* **Brand Name** — nombre que reemplaza a "Odoo" (default: *Trixocom ERP*)
* **Brand URL** — usada en footers y links *Powered by*
* **Documentation URL / Support URL** — links del menú de usuario; si están
  vacíos el item se oculta
* **Favicon URL** — path o URL absoluta al favicon
* **Hide Enterprise references** — oculta badges, banners y referencias
  al upsell Enterprise (default: activado)

Puntos cubiertos
================

* ``web.layout`` — title del browser y favicon
* ``web.brand_promotion_message`` — logo y URL "Powered by"
* ``web.login_layout`` — footer "Powered by Odoo" del login
* ``mail.mail_notification_layout`` / ``mail.mail_notification_light`` —
  footer "Powered by Odoo" en emails
* ``web.UpgradeDialog`` — diálogo de upsell Enterprise rebrandeado
* ``o_enterprise_label`` — badge "Enterprise/Empresa" en formularios de Settings
* **Settings Enterprise-only** — toda la opción (``.o_setting_box``) se oculta
  cuando contiene el badge ``o_enterprise_label``, no sólo el badge. En
  Community esos toggles nunca son funcionales (sólo abren el upgrade
  dialog). Si todas las opciones de una sección quedan ocultas, también se
  oculta el título y el contenedor de la sección.
* User menu — quita "My Odoo.com Account", agrega "Documentation" si está
  configurado
* ``support_url`` en ``session_info`` — pisa el default ``odoo.com/buy``

Instalación
===========

::

    git clone https://github.com/trixocom/trixocom_debrand.git
    # vía odoofly:
    of repo add https://github.com/trixocom/trixocom_debrand.git --env main --branch 19.0
    of env init main
    of env install demo19/main trixocom_debrand

Tests
=====

::

    of env update demo19/main trixocom_debrand --test-tags trixocom_debrand

Autor
=====

Trixocom — https://www.trixocom.com
