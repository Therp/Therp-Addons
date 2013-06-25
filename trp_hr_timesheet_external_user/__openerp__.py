# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>).
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
    'name': 'Readonly access to time writen on a customer\'s account',
    'version': '1.0',
    'description': '''Gives your customers insight into the work you do for them.
    Clock icon: https://commons.wikimedia.org/wiki/File:Crystal_Clear_app_xclock.svg
    ''',
    'author': 'Therp BV',
    'category': 'External users',
    'website': 'http://therp.nl',
    'email': 'info@therp.nl',
    'depends': [
        'hr_timesheet',
        'trp_external_user',
        'view_groups_id',
        'trp_web_hide_buttons',
        ],
    'update_xml': [
        "security/groups.xml",
        "view/hr_analytic_timesheet.xml",
        "view/menu.xml",
        "security/ir.model.access.csv",
        "security/ir_rules.xml",
        ],
}
