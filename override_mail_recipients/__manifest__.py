# Copyright 2015-2024 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Override mail recipients",
    "version": "16.0.1.0.0",
    "author": "Therp BV",
    "website": "https://github.com/OCA/web",
    "license": "AGPL-3",
    "category": "Tools",
    "summary": "Allows you to override all mail recipients for testing purposes",
    "depends": ["base"],
    "data": [
        "data/ir_config_parameter.xml",
        "data/installer.xml",
    ],
    "installable": True,
}
