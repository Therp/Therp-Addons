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
    'name': 'Click2call',
    'category': 'web',
    'summary': 'Web widget for click2call on Astium PBX',
    'version': '8.0.1.0',
    'author': 'Therp BV',
    'website': 'http://therp.nl',
    'depends': ['web'],
    'data': [
        "view/qweb.xml",
        'view/click2call.xml',
        'view/partner.xml'
    ],
    'qweb': [
        'static/src/xml/click2call.xml',
    ],
    'external_dependencies': {
        'python': [
            'urllib',
            'urllib2',
        ],
    },
}
