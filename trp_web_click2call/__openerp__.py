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
    'name': 'Web widget for click2call on Astium PBX',
    'category': 'web',
    'description':
        '''
Click2call is a simple extension on Asterisk based Astium PBX.
This module adds a field for the user's phone extension as well
as some simple configuration data on the company.
Phone numbers in OpenERP are complemented with buttons that perform the
call to the PBX so that the user gets connected with the partner
that the phone number belongs to.
        ''',
    'version': '6.1.r109',
    'author': 'Therp BV',
    'website': 'http://therp.nl',
    'depends': ['web'],
    'data': [
        'view/click2call.xml',
        'view/partner.xml'
        ],
    'js': [
        'static/src/js/click2call.js',
        ],
    'qweb': [
        'static/src/xml/click2call.xml',
        ],
    'css': [
        'static/src/css/click2call.css',
        ],
    'python' : [
        'urllib',
        'urllib2',
        ],
}
