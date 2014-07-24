# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2012 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Aeroo reports plugin for OpenOffice.Org",
    "version": "0.1r33",
    "author": "Therp BV",
    "category": 'Generic Modules/Aeroo Reporting',
    'complexity': "normal",
    "description": """
Introduction
------------
This module provides an OpenOffice.org/LibreOffice extension plus a small
interface to the Aeroo Report module on the OpenERP side to allow mail merge
directly from the Writer application. Mail merge is performed on records
stored in the saved selection in Odoo. The result is a single document in
editable ODF, appearing in a new office window.

The ability to perform mail merge on the fly reliefs the administrator from
having to create a Report XML record in the OpenERP database and upload the
template after every change.

After installation of this module, you can download the extension file
from your Odoo database under

Settings -> Customization -> Aeroo Reports -> Download Office Extension

Usage
-----
In the web client, save a custom filter. When doing a mail merge, choose one of
those filters and your document will be filled with the records in the filter's
selection.

Requirements
------------

On the client side, you need to install the extension via Tools -> Extension
Manager -> Add. After installation, restart Writer in order to see the newly
created menus.

You also need python-uno (*not python3-uno*) installed on the client machines.

Configure access to your database via Tools -> Options -> LibreOffice Writer ->
Odoo Options.

Troubleshooting
---------------

If you experience an empty configuration dialog or missing translations,
probably your extension registry is corrupt.

``rm -rf ~/.config/libreoffice/4/user{extensions,uno_packages}``

fixes the problem, but you lose all installed extensions, their configuration
and you'll have to reinstall them.
""",
    "website": 'http://therp.nl',
    "images": ['images/options.png', 'images/merge.png'],
    "depends": ['report_aeroo'],
    'data': [
        'view/get_plugin.xml',
    ],
    'installable': True,
}
