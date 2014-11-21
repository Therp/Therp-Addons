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
from openerp.osv import fields, orm, osv
from openerp.tools.translate import _


class stock_picking(orm.Model):
    _inherit = 'stock.picking'
    _columns = {
        'customs_invoice_id': fields.many2one(
            'account.invoice', 'Customs Invoice',
            ),
    }


class stock_picking_out(orm.Model):
    _inherit = 'stock.picking.out'
    _columns = {
        'customs_invoice_id': fields.many2one(
            'account.invoice', 'Customs Invoice',
            ),
    }

    def create_customs_invoice(self, cr, uid, ids, context=None):
        picking = self.browse(cr, uid, ids, context=context)[0]
        if picking.sale_id:
            sale = picking.sale_id
        else:
            raise osv.except_osv(_('This delivery is not derived from a sale'),
                                 _('To create a customs invoice, \
                                 delivery must be derived from a sales \
                                 Order, the delivery you have chosen \
                                 does not have an associated sales order'))
        res = self._make_invoice(cr, uid, ids, sale, context=context)
        view = self.open_invoices(cr, uid, [res], context=context)
        return view

    def _prepare_customs_invoice_line(self, cr, uid, line, context=None):
        """
        Bits and bobs from sale_order_line::_prepare_order_line_invoice_line()
        in sale/sale.py
        """
        sale_line_obj = self.pool['sale.order.line']
        uosqty = sale_line_obj._get_line_qty(cr, uid, line, context=context)
        uos_id = sale_line_obj._get_line_uom(cr, uid, line, context=context)
        pu = line.price_unit
        if uosqty:
            pu = round(
                line.price_unit * line.product_uom_qty / uosqty,
                self.pool.get('decimal.precision').precision_get(
                    cr, uid, 'Product Price'))

        return {
            'name': line.name,
            'sequence': line.sequence,
            'origin': line.order_id.name,
            'price_unit': pu,
            'quantity': uosqty,
            'discount': line.discount,
            'uos_id': uos_id,
            'product_id': line.product_id.id,
            'invoice_line_tax_id': [(6, 0, [x.id for x in line.tax_id])],
            'account_analytic_id': line.order_id.project_id.id,
            }

    def _prepare_customs_invoice(self, cr, uid, ids, order, context=None):
        """
        Reuse the standard method from the sale model to create an invoice
        """
        invoice_line_ids = []
        invoice_line_obj = self.pool['account.invoice.line']
        for line in order.order_line:
            invoice_line_vals = self._prepare_customs_invoice_line(
                cr, uid, line, context=context)
            invoice_line_ids.append(
                invoice_line_obj.create(
                    cr, uid, invoice_line_vals, context=context))

        invoice_vals = self.pool['sale.order']._prepare_invoice(
            cr, uid, order, invoice_line_ids, context=context)
        invoice_vals.update(
            active=False,
            customs_invoice_for_picking_ids=[(6, 0, [ids[0]])],
            )
        return invoice_vals

    def _make_invoice(self, cr, uid, ids, order, context=None):
        """
        Get or create a customs invoice
        """
        inv_obj = self.pool.get('account.invoice')
        if context is None:
            context = {}
        record = self.browse(cr, uid, ids, context=context)[0]
        if record.customs_invoice_id:
            return record.customs_invoice_id.id
        inv = self._prepare_customs_invoice(
            cr, uid, ids, order, context=context)
        inv_id = inv_obj.create(cr, uid, inv, context=context)
        inv_obj.button_compute(cr, uid, [inv_id])
        return inv_id

    def open_invoices(self, cr, uid, invoice_ids, context=None):
        """ open a view on one of the given invoice_ids """
        ir_model_data = self.pool.get('ir.model.data')
        form_res = ir_model_data.get_object_reference(
            cr, uid, 'sale_invoice_customs', 'customs_invoice_form')
        form_id = form_res[1] or False

        return {
            'name': _('Customs Invoice'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice',
            'res_id': invoice_ids[0],
            'view_id': False,
            'views': [(form_id, 'form')],
            'context': "{'type': 'out_invoice', 'active': False}",
            'type': 'ir.actions.act_window',
        }
