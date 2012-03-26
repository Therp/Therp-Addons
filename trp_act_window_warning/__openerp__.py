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
    "name": "Act window warning",
    "description": """
Allow developers to define a warning in their act_window definition,
similar to a warning in an on_change method's return value.

This module is compatible with OpenERP 6.1.
""",
    "category": "Therp web addons",
    "version": "1.0r11",
    "author": "Therp BV",
    "website": 'http://therp.nl',
    "depends": ['web'],
    "js": ["static/src/js/chrome.js"],
    "css": [],
    'active': False,
    'web': True,
}
