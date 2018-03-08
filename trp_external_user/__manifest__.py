# -*- coding: utf-8 -*-
# Copyright 2013-2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "External users",
    "summary": "Allow external users on your system",
    "version": "10.0.1.0.0",
    "author": "Therp BV",
    "category": 'External users',
    'website': 'http://therp.nl',
    'depends': [
        'portal',
    ],
    'demo': [
        "demo/res_users.xml",
    ],
    'data': [
        'data/ir_module_category.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/res_users.xml',
    ],
    'license': 'AGPL-3',
}
