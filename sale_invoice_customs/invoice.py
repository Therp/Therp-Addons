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
from gdata.spreadsheet.text_db import Record

class account_invoice(orm.Model):
    _inherit = 'account.invoice'

    _columns = {
        'active': fields.boolean("Active"),
    }

    _defaults = {
        'active': True,
    }


    #FIX this check is not working, set to true
    def _check_valid_customs(self,cr,uid,ids,context=None):
        this = self.browse(cr, uid, ids, context=context)
        stock_pickings = self.pool.get('stock.picking')
        for data in this:
            if ((data.active==False and len(stock_pickings.search(cr,uid,[
                ('customs_invoice_id', '=' , data.id)
                ]))>0) or (data.active== True)):
                return True
        return True



    _constraints = [(_check_valid_customs,
        'All custom invoices must be tagged False', ['active']),]