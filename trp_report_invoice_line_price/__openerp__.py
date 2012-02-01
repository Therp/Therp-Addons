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
    "name" : "Invoice line price fields",
    "version" : "0.1r7",
    "author" : "Therp BV",
    "category": 'Accounting & Finance',
    'complexity': "normal",
    "description": """
        This module provides 4 additional function fields on the invoice line
        to be used in invoice reports. These fields should unequivocally produce
        the price per units or per line, excluding and including taxes.
        Note that the existing field price_unit, which is used in the default
        invoice report may or may not include taxes according to product settings. 

        The fields of the names are self explanatory:

        - price_unit_incl
        - price_unit_excl
        - price_line_incl
        - price_line_excl

    """,
    'website': 'http://therp.nl',
    'images' : [],
    'init_xml': [],
    "depends" : ['account'],
    'update_xml': [
    ],
    'demo_xml': [],
    'test': [ ],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
