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
    "name" : "Report addresses without country",
    "version" : "0.1r5",
    "author" : "Therp BV",
    "category": 'Generic Modules',
    'complexity': "normal",
    "description": """
In certain reports, we may opt to display partner addresses without a country,
as this may not be informative if the country is the same as the company's
partner. This module provides a function that does not print the partner
address' country in that case.

To use this function, call display_address(address, company) in your rml
reports instead of display_address(address).

    """,
    'website': 'http://therp.nl',
    'images' : [],
    'init_xml': [],
    "depends" : ['base'],
    'update_xml': [
    ],
    'demo_xml': [],
    'test': [ ],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
