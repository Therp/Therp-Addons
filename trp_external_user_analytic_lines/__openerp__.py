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
    "name": "Have external users read their analytic lines",
    "version": "1.0",
    "author": "Therp BV",
    "license": "AGPL-3",
    "complexity": "normal",
    "description": """
This addon allows external users readonly access to analytic lines written for
their configured customer(s).

Icon courtesy to http://commons.wikimedia.org/wiki/File:Geschiedenis_icon.png
    """,
    "category": "Accounting & Finance",
    "depends": [
        'trp_external_user',
        'analytic',
        'hr_timesheet',
        'project',
        'project_issue',
        'project_timesheet',
    ],
    "data": [
        "view/account_analytic_line.xml",
        "view/menu.xml",
        "security/res_groups.xml",
        'security/ir.model.access.csv',
        "security/ir_rule.xml",
    ],
    "js": [
    ],
    "css": [
    ],
    "qweb": [
    ],
    "test": [
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
    "external_dependencies": {
        'python': [],
    },
}
