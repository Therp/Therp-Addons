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
    "description": """
Use with project_scrum for Odoo 8.0 from
https://github.com/EL2DE/openerp8-addons.git

- Makes stages visible for non developers
- Adds a field for technical details, visible for developers
- Adds some placeholders for clarification
- Show followers on user stories
    """,
    "category": "Therp addons",
    "version": "1.0",
    "author": "Therp BV",
    "website": 'http://therp.nl',
    "depends": ['project_scrum'],
    "data": [
        "view/product_backlog.xml",
        "data/mail_message_subtype.xml",
        ],
}
