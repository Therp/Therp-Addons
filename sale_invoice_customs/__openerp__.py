# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Therp BV (<http://therp.nl>).
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
    "name": "sale_invoice_customs",
    "version": "1.0",
    "author": "Therp BV",
    "license": "AGPL-3",
    "complexity": "normal",
    "description": """
Create a specific invoice shipping document from a delivery, for customs
purposes. This document looks like an invoice, reuses the invoice table and
views but internally, these invoices will always be kept in draft state and
are set to inactive so that they don't influence the accounting and don't even
show up in other contexts. Only one customs invoice can be created per
shipping. In order to regenerate a customs invoice for a picking from scratch,
delete the existing one.
    """,
    "category": "",
    "depends": [
        'account',
        'stock',
        'sale'
    ],
    "data": [
        'view/sale_invoice_customs.xml',
    ],
    "js": [
    ],
    "css": [
    ],
    "qweb": [
    ],
    "test": [
    ],
    "installable": True,
    "external_dependencies": {
        'python': [],
    },
}
