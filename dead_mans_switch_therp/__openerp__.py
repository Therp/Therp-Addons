# -*- coding: utf-8 -*-
# © 2015 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Dead man's switch for Therp",
    "version": "8.0.1.0.0",
    "author": "Therp BV",
    "license": "AGPL-3",
    "category": "Monitoring",
    "summary": "Configure dead_mans_switch_client for Therp",
    "depends": [
        'dead_mans_switch_client',
    ],
    "data": [
        "data/ir_config_parameter.xml",
        "data/ir_actions.xml",
    ],
}
