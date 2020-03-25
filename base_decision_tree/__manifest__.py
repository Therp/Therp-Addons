# -*- coding: utf-8 -*-
# Copyright 2020 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Decision trees",
    "version": "10.0.1.0.0",
    "author": "Therp BV",
    "license": "AGPL-3",
    "category": "",
    "summary": "Allows you to manage decision trees for some process",
    "depends": [
        'base',
    ],
    "data": [
        "views/templates.xml",
        "security/res_groups.xml",
        'security/ir.model.access.csv',
        "views/decision_tree_node.xml",
    ],
    "installable": True,
    "application": False,
    "external_dependencies": {
        'python': [],
    },
}
