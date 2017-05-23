# -*- coding: utf-8 -*-
# © 2013-2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Find Memory Leaks",
    "version": "7.0.1.0.1",
    "author": "Therp BV",
    "complexity": "normal",
    "description": """Provides wizard to find memory leak""",
    "category": "Server tools",
    "depends": [
        'base',
    ],
    "data": [
        'find_memory_leaks.xml',
    ],
    "auto_install": False,
    "installable": True,
    "external_dependencies": {
        'python': [
            'pdb',
            'objgraph',
            'guppy'
        ],
    },
}
