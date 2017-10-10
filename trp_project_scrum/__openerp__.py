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
    "name": "Therp specific adaptations for scrum",
    "category": "Therp addons",
    "version": "8.0.1.0.1",
    "author": "Therp BV",
    "website": 'http://therp.nl',
    "depends": [
        'trp_external_user',
        'project_timesheet',
        'project_scrum',
        'project_definition',
    ],
    "data": [
        'security/res_groups.xml',
        'security/ir_rules_collaborators_followers.xml',
        'security/ir.model.access.csv',
        'views/menu_definitions.xml',
        ],
}
