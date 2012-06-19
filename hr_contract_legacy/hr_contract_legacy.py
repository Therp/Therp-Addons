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
import time
from osv import fields, osv

#Contract wage type period name
class hr_contract_wage_type_period(osv.osv):
    _name='hr.contract.wage.type.period'
    _description='Wage Period'
    _columns = {
        'name': fields.char('Period Name', size=50, required=True, select=True),
        'factor_days': fields.float('Hours in the period', digits=(12,4), required=True, help='This field is used by the timesheet system to compute the price of an hour of work wased on the contract of the employee')
    }
    _defaults = {
        'factor_days': 168.0
    }

#Contract wage type (hourly, daily, monthly, ...)
class hr_contract_wage_type(osv.osv):
    _name = 'hr.contract.wage.type'
    _description = 'Wage Type'
    _columns = {
        'name': fields.char('Wage Type Name', size=50, required=True, select=True),
        'period_id': fields.many2one('hr.contract.wage.type.period', 'Wage Period', required=True),
        'type': fields.selection([('gross','Gross'), ('net','Net')], 'Type', required=True),
        'factor_type': fields.float('Factor for hour cost', digits=(12,4), required=True, help='This field is used by the timesheet system to compute the price of an hour of work wased on the contract of the employee')
    }
    _defaults = {
        'type': 'gross',
        'factor_type': 1.8
    }
hr_contract_wage_type()

class hr_contract(osv.osv):
    _inherit = "hr.contract"
    _columns = {
        'wage_type_id': fields.many2one('hr.contract.wage.type', 'Wage Type', required=True),
        'advantages_net': fields.float('Net Advantages Value', digits=(16,2)),
        'advantages_gross': fields.float('Gross Advantages Value', digits=(16,2)),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
