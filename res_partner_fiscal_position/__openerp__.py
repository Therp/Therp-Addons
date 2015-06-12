# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
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
    'name': 'Country fiscal position',
    'version': '8.0',
    'category': 'Accounting',
    'description': '''
     This module automatically select the fiscal position from the country
     table when selecting the country in the partner form.
     This module is based on the module account_fiscal_position_country
     of agilebg in this module the fiscal position is only used the invoice.
    ''',
    'author': 'Therp BV',
    'website': 'http://www.therp.nl',
    'depends': [
        'base',
        'account',
    ],
    'data': [
        'view/res_country.xml',
    ],
    "installable": True,
}
