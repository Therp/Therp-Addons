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
from openerp.osv import fields, orm

class account_invoice(orm.Model):
    _inherit = 'account.invoice'
    
    _columns = {
        'active': fields.boolean("Active"),
    }
    
    _defaults = {
        'active': True,
    }
    
    
    """def _check_valid(self, cr, uid, ids, context=None):
        return self.active==False or not(self.invoice_id)  
    
    _constraints = [(_check_valid, 'only inactive invoices can be associated with a stock_picking_out', ['active'])]
    """
