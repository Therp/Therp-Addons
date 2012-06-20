# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2012 Therp BV (<http://therp.nl>).
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
    'name': 'Human Resources Contracts - legacy',
    'version': '1.0',
    'category': 'Generic Modules/Human Resources',
    'description': """
    Preserves the ability to keep track of
    advantages on contracts like it was in OpenERP 6.0

    This is meant for people upgrading from 6.0 who won't benefit from stepping 
    over to hr_payroll
    """,
    'author': 'Therp BV',
    'depends': ['hr_contract'],
    'update_xml': [
        'hr_contract_legacy_view.xml',
        'security/ir.model.access.csv'
        ],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
