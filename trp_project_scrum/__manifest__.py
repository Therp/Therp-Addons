# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Therp specific adaptations for scrum",
    "category": "Therp addons",
    "version": "10.0.1.0.0",
    "license": "AGPL-3",
    "author": "Therp BV",
    "website": 'https://therp.nl',
    "depends": [
        'trp_external_user',
        'project_scrum',
        'hr',
        'hr_timesheet',
    ],
    "data": [
        'security/res_groups.xml',
        'security/ir_rules.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
        ],
    "demo": [
        'demo/res_users.xml',
        'demo/project_project.xml',
        'demo/project_task.xml',
        ],
}
