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
    "name" : "Fetch mail into inbox",
    "version" : "1.0",
    "author" : "Therp BV",
    "complexity": "normal",
    "description": """
    In some cases, you may not want to have OpenERP create objects directly
    on mail arrival, but put them into an inbox for further (possibly manual)
    processing.

    This module provides the base for this workflow and elementary UI for
    processing.
    """,
    "category" : "Dependency",
    "depends" : [
        'fetchmail',
    ],
    "data" : [
        "wizard/fetchmail_inbox_create_wizard.xml",
        "wizard/fetchmail_inbox_attach_existing_wizard.xml",
        "view/mail_message.xml",
        "view/menu.xml",
        'security/ir.model.access.csv',
    ],
    "js": [
        'static/src/js/fetchmail_inbox.js',
    ],
    "css": [
    ],
    "qweb": [
    ],
    "auto_install": False,
    "installable": True,
    "external_dependencies" : {
        'python' : [],
    },
}
