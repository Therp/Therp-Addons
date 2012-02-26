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
    "name": "EDI Company Control - Invoices",
    "description": """

By default, OpenERP 6.1 sends out a mail to a customer or supplier upon the
confirmation of sale orders, customer invoices and purchase orders.

This module implements company level control of this feature for customer
invoices, adding a setting 'Enable EDI invoice emails'.

See also https://bugs.launchpad.net/openobject-addons/+bug/934242

This module is compatible with OpenERP 6.1.
""",
    "category": "Accounting & Finance",
    "version": "1.0r8",
    "author": "Therp BV",
    "website": 'http://therp.nl',
    "depends": ['account'],
    "update_xml": [
        'view/res_company_view.xml',
        'data/edi_data.xml',
        ],
    "js": [],
    "qweb": [],
    "css": [],
    'active': False,
}
