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
    "name": "External users",
    "version": "1.0r87",
    "author": "Therp BV",
    "category": 'Base',
    'complexity': "normal",
    "description": """
Define a group 'External Users' that only have access to selected partners,
usually their own organizations. These partners are indicated on the user's user
form. By default, this module only grants read access to these partners.

On a permission level, it seems necessary that the partners also need read access
to the database company partner, which this module also allows. Keep this in mind
when building functionality on top of this module that allows interaction with
the partner model. By means of precaution, this module does define separate
records for reading and writing so as to prevent modifications of the company
partner (even if global write access on partners are not granted to the external
users group in this module).

This module also disables the default assignment of the 'user' and 'partner manager'
groups to new users.
    """,
    'website': 'http://therp.nl',
    'images': [],
    'depends': ['base'],
    'data': [
        'data/ir_module_category.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'view/res_users.xml',
    ],
    'license': 'AGPL-3',
}
