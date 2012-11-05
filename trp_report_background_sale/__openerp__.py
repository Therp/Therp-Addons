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
    "name" : "Backgrounds for sale order report",
    "version" : "0.1r67",
    "author" : "Therp BV",
    "category": 'Reporting',
    'complexity': "normal",
    "description": """

This module only contains the configuration for the sale order report, to be used with
trp_report_background.

    """,
    'website': 'http://therp.nl',
    'images' : [],
    'depends' : [
        'trp_report_background',
        'sale',
        ],
    'data': [
        'view/sale.xml',
        'data/report_background_config.xml',
        ],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
