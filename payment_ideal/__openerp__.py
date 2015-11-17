# -*- coding: utf-8 -*-
##############################################################################
#
#    This module copyright (C) 2015 Therp BV <http://therp.nl>.
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
    "name": "iDeal payment acquirer",
    "version": "8.0.1.0.0",
    "author": "Therp BV",
    "license": "AGPL-3",
    "category": "eCommerce",
    "summary": "Use Dutch iDeal to process your payments",
    "depends": [
        'payment',
    ],
    "data": [
        "views/payment_transaction.xml",
        "views/templates.xml",
        "views/payment_acquirer.xml",
        "data/ir_actions_todo.xml",
    ],
    "installable": True,
    "external_dependencies": {
        'python': ['xmlsec'],
    },
    'price': 256,
    'currency': 'EUR',
}
