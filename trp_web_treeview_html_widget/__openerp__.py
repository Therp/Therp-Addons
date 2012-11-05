# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2011-2012 Therp BV (<http://therp.nl>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Use html fields in tree views',
    'version': '1.0',
    'description': """
    This addon provides a widget that enables html display in tree views.
    Just use <field name="name" widget="trp_treeview_html" />

    ATTENTION ATTENTION ATTENTION
    This widget displays html as is comes from the database. Passing raw html to
    you browser can be a serious security risk. Escape your input ie with 
    cgi.escape and consider filtering it through 
    http://lxml.de/lxmlhtml.html#cleaning-up-html

    Use this widget only if you know what you're doing!
    """,
    'author': 'Therp BV',
    'website': 'http://www.therp.nl',
    "category": "Tools",
    "depends": ['web'],
    'js': ['static/src/js/trp_treeview_html.js'],
    'installable': True,
    'active': False,
    'certificate': '',
}
