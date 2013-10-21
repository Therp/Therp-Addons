# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>).
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
    "name": "Separator visibility depending on view mode",
    "version": "6.1.1.0r1",
    "author": "Therp BV",
    "category": "Tools",
    "depends": ['web_mode_visibility', 'override_import_xml_schema'],
    "description": """
Use the following options keys on separator tags and other form widget
to hide them in either page or form mode:

- page_invisible
- form_invisible

This module is compatible with OpenERP 6.1.
    """,
    'js': [
        'static/src/js/web_mode_visibility.js',
        ],
}
