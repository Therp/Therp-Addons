# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>).
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
from openerp.osv import orm, fields
import openerp.addons.decimal_precision as dp


class account_analytic_line(orm.Model):
    _inherit = 'account.analytic.line'

    def _get_debit_credit(self, cr, uid, ids, name, args, context=None):
        """
        Split up the line amount by sign
        """
        result = {}
        for line in self.read(
                cr, uid, ids, ['amount'], context=None):
            result[line['id']] = {'debit': 0.0, 'credit': 0.0}
            if line['amount'] > 0.0:
                result[line['id']]['debit'] = line['amount']
            else:
                result[line['id']]['credit'] = -line['amount']
        return result

    _columns = {
        'debit': fields.function(
            _get_debit_credit, type='float',
            digits_compute=dp.get_precision('Account'),
            multi='debcred', string="Debit"),
        'credit': fields.function(
            _get_debit_credit, type='float',
            digits_compute=dp.get_precision('Account'),
            multi='debcred', string="Credit"),
        }
