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
    "name": "Fetchmail invoice",
    "version": "0.1r31",
    "author": "Therp BV",
    "category": 'Tools',
    "description": """

This module allows the fetchmail module to operate on invoices. 

Invoices are created as incoming invoices, with the partner that has the
email's sender address along with all the partner's financial settings.

A dummy partner is created for incoming emails from unknown addresses.

The actual emails can be inspected on a dedicated tab on the invoice
form which is otherwise invisible.

This module is compatible with OpenERP 6.1
""",
    "depends": [
        'fetchmail',
        'account'
        ],
    "data": [
        'view/invoice.xml',
        'data/partner_data.xml',
        'data/installer.xml',
        ],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
