# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2011 - 2012 Therp BV (<http://therp.nl>).
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
    "name" : "Saved Selections",
    "version" : "0.1r19",
    "author" : "Therp BV",
    "category": 'Base',
    'complexity': "normal",
    "description": """Save selections of records of an arbitrary model. Add or remove
items on the fly. Share the selections with other users.
This addon has a web component and is only fully functional on the
web client, not GTK.

This module is compatible with OpenERP 6.1
    """,
    'website': 'http://therp.nl',
    'depends' : ['base', 'web'],
    'data': [
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
        'view/saved_selection.xml',
        'view/saved_selection_init.xml',
    ],
    'installable': True,
    'active': False,
    'web': True,
    "js": ["static/src/js/*.js"],
    "qweb": ["static/src/xml/base.xml"],
    "css": [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
