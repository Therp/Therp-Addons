# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
    'name': 'Report Creator',
    'version': '1.1',
    'category': 'Generic Modules/Base',
    'description': """This module allows you to create any statistic
report on several objects. It's a SQL query builder and browser
for and users.

After installing the module, it adds a menu to define custom report in
the "Dashboard" menu.

Please note that due to the nature of the tool, it offers the possibility
of SQL injections to the creators of new reports. Permissions to create
new reports should therefore not be given lightly.

This module is compatible with OpenERP 6.1. It is maintained by Therp BV
after being deprecated in OpenERP 6.1 for unknown reasons.

This module modifies a little piece of code in the 'web_graph' module
so as to maintain compatibility with the 6.1 web client.
""",
    'author': ['OpenERP SA', 'Axelor', 'Therp BV'],
    'website': '',
    'depends': ['base', 'board', 'web_graph'],
    'init_xml': [],
    'update_xml': [
        'security/ir.model.access.csv',
        'wizard/report_menu_create_view.xml',
        'base_report_creator_wizard.xml',
        'base_report_creator_view.xml'
    ],
    'demo_xml': [],
    'installable': True,
    'active': False,
    'certificate': '',
    'js': ["static/src/js/*.js"],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
