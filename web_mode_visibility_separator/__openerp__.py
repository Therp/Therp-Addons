# -*- coding: utf-8 -*-
# Copyright 2013-2021 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Separator visibility depending on view mode",
    "version": "6.1.1.0.1",
    "author": "Therp BV",
    "category": "Tools",
    "depends": ["web_mode_visibility"],
    "description": """
Use the following options keys on separator tags and other form widget
to hide them in either page or form mode:

- page_invisible
- form_invisible

This module is compatible with OpenERP 6.1.

This module no longer tries to patch view.rng, as the needed changes have been
applied to the view.rng in customized ocb-server repository.
    """,
    "js": [
        "static/src/js/web_mode_visibility.js",
    ],
}
