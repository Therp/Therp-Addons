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
    "name": "Support branding",
    "description": """If you run an OpenERP support company and you support
customers without an OPW, you can brand the OpenERP instance
accordingly using this module. This module will replace the unfriendly
message about the OpenERP instance not being supported with the information
that your customers need to contact you.

Ths is a web module. You cannot install it through the OpenERP modules
interface. Instaed, to enable this module set 'active' to True in
support_branding/__openerp__.py and restart the OpenERP server.

To configure this module, please enter the values for thetwo
variables 'support_name' and 'support_link' in the file
support_branding/static/src/js/chrome.js.

This module is compatible with OpenERP 6.1.
""",
    "category": "Therp web addons",
    "version": "1.0r4",
    "author": "Therp BV",
    "website": 'http://therp.nl',
    "depends": ['web'],
    "js": ["static/src/js/chrome.js"],
    "qweb": ["static/src/xml/base.xml"],
    "css": [],
    'active': False,
}
