================
Trixocom Debrand
================

.. |badge_license| image:: https://img.shields.io/badge/licence-LGPL--3-blue.png
   :target: https://www.gnu.org/licenses/lgpl-3.0
   :alt: License: LGPL-3

|badge_license|

Reemplaza las referencias a la marca *Odoo* y oculta opciones *Enterprise*
en el backend, el portal, el sitio web, mails, reportes y links de
documentación de Odoo Community 19.0.

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

Backend
-------

* ``web.layout`` — title del browser y favicon
* ``web.brand_promotion_message`` — logo y URL "Powered by"
* ``web.login_layout`` — footer "Powered by Odoo" del login
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

Mails y reportes
----------------

* ``mail.mail_notification_layout`` / ``mail.mail_notification_light`` —
  footer "Powered by Odoo" en emails
* ``views/report_templates.xml`` — stub. Auditado: los ``external_layout_*``
  de Odoo 19 no llevan marca Odoo en el footer del PDF, sólo
  ``company.report_footer``

Portal
------

* ``portal.portal_record_sidebar`` — el "Powered by |logo odoo|" que aparece
  abajo del sidebar en ``/my/orders/<id>``, ``/my/invoices/<id>``, etc.
* ``portal.portal_my_security`` — link a ``odoo.com/documentation`` de las
  Developer API Keys (visible en modo debug)

Sitio web
---------

* ``website.layout`` — el botón de apps del frontend navega a ``/odoo`` en
  vez de abrir el dropdown
* ``website.brand_promotion`` — saca el "Create a free website" con link a
  ``odoo.com/app/website`` del footer
* ``website.show_website_info`` — la página ``/website/info`` deja de decir
  "instance of Odoo, the Open Source ERP", "Odoo Version" y de linkear las
  localizaciones a ``odoo.com/app/accounting``

Punto de venta
--------------

* Logo de la empresa en lugar del de Odoo (cajero y customer display)
* Ticket de venta sin marca Odoo

Fuera de este módulo
====================

El modal "Connect with your software" del portal de ventas y de compras vive
en ``sale`` y ``purchase``, y el mensaje del footer de eCommerce en
``website_sale``. Debrandearlos desde acá obligaría a ``trixocom_debrand`` a
depender de esos módulos y forzaría su instalación en clientes que no los
usan. Están cubiertos por los módulos puente del repo
`trixocom-debrand-apps <https://github.com/trixocom/trixocom-debrand-apps>`_
(``trixocom_debrand_sale``, ``trixocom_debrand_purchase``,
``trixocom_debrand_website_sale``), que se auto-instalan cuando corresponde.

Instalación
===========

::

    git clone https://github.com/trixocom/trixocom_debrand.git
    # vía odoofly:
    of repo add https://github.com/trixocom/trixocom_debrand.git -e main -b main
    of env init demo19 main
    of env install demo19 <db> trixocom_debrand

Tests
=====

::

    of env update demo19 <db> -m trixocom_debrand --test-tags trixocom_debrand

Autor
=====

Trixocom — https://www.trixocom.com
