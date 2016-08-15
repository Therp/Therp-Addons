# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2012-2016 Therp BV (<http://therp.nl>).
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
    "name": "Support branding (Therp)",
    "summary": "Adds Therp's branding to an Odoo instance",
    "category": "Dependecy/Hidden",
    "version": "2.0",
    "author": "Therp BV",
    "website": 'http://therp.nl',
    "description": """Support branding (Therp)
========================

This module adds Therp specific branding to your odoo instance.""",
    "depends": [
        'support_branding',
    ],
    "data": [
        "data/ir_config_parameter.xml",
    ],
    'active': True,
}
