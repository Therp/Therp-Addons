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
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp import pooler
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class stock_picking(orm.Model):
    _inherit = 'stock.picking'
    
    _columns = {
        'customs_invoice_id': fields.many2one('account.invoice', 'New Invoice', required=False),
    }
    
    
class stock_picking_out(orm.Model):
    _inherit = 'stock.picking.out'
    
    def generate_from_stock(self,cr,uid,context=None):
        return {}
    
    def create_invoice(self, cr, uid, ids, context=None):
        picking=self.browse(cr,uid,ids,context=context)[0]
        if picking.sale_id:
            sale=picking.sale_id
        else:
            sale=generate_from_stock()
        
        """ create invoices for sale or@der connected tpo the stock picking """
        sale_obj = self.pool.get('sale.order')
        act_window = self.pool.get('ir.actions.act_window')

        res = self._make_invoice(cr,uid,sale,context=None)
        
        view=self.open_invoices(cr, uid, [res], context=None)
        return view
    
    
    def prepare_invoice_from_stock_move(self,cr, uid,lines, context=None):
        if context is None:
            context = {}
        journal_ids = self.pool.get('account.journal').search(cr, uid,
            [('type', '=', 'sale'), ('company_id', '=', self.company_id)],
            limit=1)
        if not journal_ids:
            raise osv.except_osv(_('Error!'),
                _('Please define journal for this company: "%s" (id:%d).') % (self.company_id.name, self.company_id.id))
        invoice_vals = {
            'name': self.client_order_ref or '',
            'origin': self.name,
            'type': 'out_invoice',
            'reference': self.client_order_ref or self.name,
            'account_id': self.partner_id.property_account_receivable.id,
            'partner_id': self.partner_invoice_id.id,
            'journal_id': journal_ids[0],
            'invoice_line': [(6, 0, lines)],
            'currency_id': 1,
            'comment': self.note,
            'date_invoice': context.get('date_invoice', False),
            'company_id': self.company_id.id,
            'user_id':  False
         }

        # Care for deprecated _inv_get() hook - FIXME: to be removed after 6.1
        #invoice_vals.update(self._inv_get(cr, uid, order, context=context))
        return invoice_vals


    def _prepare_invoice(self, cr, uid, order, context=None):
        """Prepare the dict of values to create the new invoice for a
           sales order. This method may be overridden to implement custom
           invoice generation (making sure to call super() to establish
           a clean extension chain).

           :param browse_record order: sale.order record to invoice
           :param list(int) line: list of invoice line IDs that must be
                                  attached to the invoice
           :return: dict of value to create() the invoice
        """
        if context is None:
            context = {}
        journal_ids = self.pool.get('account.journal').search(cr, uid,
            [('type', '=', 'sale'), ('company_id', '=', order.company_id.id)],
            limit=1)
        if not journal_ids:
            raise osv.except_osv(_('Error!'),
                _('Please define sales journal for this company: "%s" (id:%d).') % (order.company_id.name, order.company_id.id))
        invoice_lines = []
        for line in order.order_line:
            invoice_lines.append(
                (0, 0,
                 {
                     'name': line.name,
                     'price_unit': line.price_unit,
                     'account_id': order.partner_id.property_account_receivable.id,
                     'quantity': line.product_uom_qty,
                 })
            )
        invoice_vals = {
            'name': order.client_order_ref or '',
            'origin': order.name,
            'type': 'out_invoice',
            'reference': order.client_order_ref or order.name,
            'account_id': order.partner_id.property_account_receivable.id,
            'partner_id': order.partner_invoice_id.id,
            'journal_id': journal_ids[0],
            'invoice_line': invoice_lines,
            'currency_id': order.pricelist_id.currency_id.id,
            'comment': order.note,
            'payment_term': order.payment_term and order.payment_term.id or False,
            'fiscal_position': order.fiscal_position.id or order.partner_id.property_account_position.id,
            'date_invoice': context.get('date_invoice', False),
            'company_id': order.company_id.id,
            'user_id': order.user_id and order.user_id.id or False
        }

        # Care for deprecated _inv_get() hook - FIXME: to be removed after 6.1
        #invoice_vals.update(self._inv_get(cr, uid, order, context=context))
        return invoice_vals

    def _make_invoice(self, cr, uid, order, context=None):
        inv_obj = self.pool.get('account.invoice')
        obj_invoice_line = self.pool.get('account.invoice.line')
        if context is None:
            context = {}
        invoiced_sale_line_ids = self.pool.get('sale.order.line').search(cr, uid, [('order_id', '=', order.id), ('invoiced', '=', True)], context=context)
        from_line_invoice_ids = []
       
        inv = self._prepare_invoice(cr, uid, order, context=context)
        
        #obj_stock_move=self.pool.get('stock.move')
        #stock_move_ids = obj_stock_move.search(cr, uid, [('picking_id', '=', self.id), ], context=context)
        
        inv_id = inv_obj.create(cr, uid, inv, context=context)
        inv_obj.write(cr,uid,[inv_id],{'active': False},context=context)
        """data = inv_obj.onchange_payment_term_date_invoice(cr, uid, [inv_id], inv['payment_term'], time.strftime(DEFAULT_SERVER_DATE_FORMAT))
        if data.get('value', False):
            inv_obj.write(cr, uid, [inv_id], data['value'], context=context)"""
        inv_obj.button_compute(cr, uid, [inv_id])
        return inv_id

    def open_invoices(self, cr, uid, invoice_ids, context=None):
        """ open a view on one of the given invoice_ids """
        ir_model_data = self.pool.get('ir.model.data')
        form_res = ir_model_data.get_object_reference(cr, uid, 'sale_invoice_customs', 'customs_invoice_form')
        form_id = form_res[1] or False
        

        return {
            'name': _('Advance Invoice'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice',
            'res_id': invoice_ids[0],
            'view_id': False,
            'views': [(form_id,'form')],
            'context': "{'type': 'out_invoice'}",
            'type': 'ir.actions.act_window',
        }


    
    
        
        
    