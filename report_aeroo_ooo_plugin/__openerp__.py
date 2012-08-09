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
    "name" : "Aeroo reports plugin for OpenOffice.Org",
    "version" : "0.1r33",
    "author" : "Therp BV",
    "category": 'Generic Modules/Aeroo Reporting',
    'complexity': "normal",
    "description": """
This module provides an OpenOffice.org/LibreOffice extension plus a small
interface to the Aeroo Report module on the OpenERP side to allow mail merge
directly from the Writer application. Mail merge is performed on records
stored in the saved selection in OpenERP. The result is a single document in
editable ODF, appearing in a new office window.

The ability to perform mail merge on the fly reliefs the administrator from
having to create a Report XML record in the OpenERP database and upload the
template after every change.

Note that the ability to store and share selections of
OpenERP records is provided by the Saved Selection module by Therp BV. Due
to this dependency, this module is only fully functional in combination with
the OpenERP web client.

After installation of this module, you can download the extension file
from your OpenERP database under

Settings -> Customization -> Aeroo Reports -> Download Office Extension

Known issues:
If the resulting document does not contain page breaks between the merged
template on different records, make sure that the document ends with a
line break.

This module is compatible with OpenERP 6.1.
    """,
    "website": 'http://therp.nl',
    "images" : ['images/options.png', 'images/merge.png'],
    "depends" : ['report_aeroo', 'trp_saved_selection'],
    'data': [
        'view/get_plugin.xml',
    ],
}
