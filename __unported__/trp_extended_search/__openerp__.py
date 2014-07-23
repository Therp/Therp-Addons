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
    "name": "Extended Search by Therp",
    "description": """This addon for the OpenERP web client allows for more
detailed search queries in any search view. It does so by adding an extra drop
down with all the fields of the model that point to related models (many2one,
one2many and many2many). When such a field is selected, a new subordinate search
view for that field's related model appears.

Multiple subordinate search views can be embedded that way either on the main
model or recursively. Combinations with advanced filters are possible. Queries
composed with subordinate search views can be saved as a custom filter.

This is a web addon for OpenERP 6.1
""",
    "version": "1.0",
    "depends": ['web'],
    "js": ["static/src/js/*.js"],
    "css": ["static/src/css/*.css"],
    "qweb": ["static/src/xml/*.xml"],
    'web': True,
    'active': False,
    'web_preload': False,
    'installable': False,
}
