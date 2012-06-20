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
    "name": "Filters for all by Therp",
    "version": "1.0",
    "author": "Therp BV",
    "category": "Tools",
    "depends": ['base'],
    "description": """
In OpenERP search views, you can add save your own custom filters. This module
allows you to share your filters with the other users by clearing the user
field defined on the filter.

Filters can however only be modified or removed by the original creator, or
the ERP administrator.
    """,
    "data": [
        'view/ir_filters_view.xml',
        'security/ir_rule.xml',
        ],
}
