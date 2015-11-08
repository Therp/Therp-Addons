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
    "name": "Use case development",
    "version": "1.0r45",
    "author": "Therp BV",
    "category": 'Base',
    'complexity': "normal",
    "description": """
Compose collections of use case descriptions and print them with an aeroo
report which is included in this module.
    """,
    'website': 'http://therp.nl',
    'images': [],
    'depends': [
        'base',
        'report_aeroo',
        'trp_external_user',
    ],
    'data': [
        'view/use_case.xml',
        'view/use_case_inline.xml',
        'view/use_case_collection.xml',
        'report/report_use_case.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
    ],
    "license": 'AGPL-3',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
