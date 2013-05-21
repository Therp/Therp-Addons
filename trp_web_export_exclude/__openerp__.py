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
    "name": "Allow to exclude fields in the export list",
    "version": "1.0r39",
    "author": "Therp BV",
    "category": "Tools",
    "depends": ['web'],
    "description": """
Mark fields not to show up in the list of exportable fields, nor in the list
of fields in an advanced filter. Go to Administration ->
Customizations -> Database Structure -> Fields. For fields that you do not want
to show up in the export list, check the box 'Exclude from export'.

Applies to the Export widget in the web client only (GTK client not supported)

Warning: this is a hackish module. Due to the applied technology of 'monkeypatching',
when installed on any database of an OpenERP instance, this module may affect the
functionality of all databases of that instance.
    """,
    'data': [
        'view/ir_model_fields.xml',
        ],
    'images': [
        'images/export_exclude.png',
        ],
    'js': ['static/src/js/search_exclude.js'],
}
