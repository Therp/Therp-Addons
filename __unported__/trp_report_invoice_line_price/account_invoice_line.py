# -*- coding: utf-8 -*-
from osv import osv, fields
import decimal_precision as dp

class account_invoice_line(osv.osv): 
    _inherit = 'account.invoice.line'

    def _amount_line_single(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        """
        Provides 4 additional function fields to be used in 
        invoice reports. Note that the original invoice report uses
        price_unit, which may or may not include taxes according to
        product settings. These fields should unequivocally produce
        the price per units or per line, excluding and including taxes.

        Analogous to the standard method _amount_line in account/account_invoice.py
        """
        res = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        for line in self.browse(cr, uid, ids):
            price = line.price_unit * (1-(line.discount or 0.0)/100.0)
            taxes = tax_obj.compute_all(cr, uid, line.invoice_line_tax_id, price, 1, product=line.product_id, address_id=line.invoice_id.address_invoice_id, partner=line.invoice_id.partner_id)
            res[line.id] = {'price_unit_incl': taxes['total_included'],
                            'price_unit_excl': taxes['total']}
            taxes = tax_obj.compute_all(cr, uid, line.invoice_line_tax_id, price, line.quantity, product=line.product_id, address_id=line.invoice_id.address_invoice_id, partner=line.invoice_id.partner_id)
            res[line.id]['price_line_incl'] = taxes['total_included']
            res[line.id]['price_line_excl'] = taxes['total']
            if line.invoice_id:
                cur = line.invoice_id.currency_id
                res[line.id]['price_unit_incl'] = cur_obj.round(cr, uid, cur, res[line.id]['price_unit_incl'])
                res[line.id]['price_unit_excl'] = cur_obj.round(cr, uid, cur, res[line.id]['price_unit_excl'])
                res[line.id]['price_line_incl'] = cur_obj.round(cr, uid, cur, res[line.id]['price_line_incl'])
                res[line.id]['price_line_excl'] = cur_obj.round(cr, uid, cur, res[line.id]['price_line_excl'])
        return res

    _columns = {
        'price_unit_incl': fields.function(
            _amount_line_single, string='Unit price incl. taxes', type="float",
            digits_compute= dp.get_precision('Account'),
            multi='single', store=False),
        'price_unit_excl': fields.function(
            _amount_line_single, string='Unit price excl. taxes', type="float",
            digits_compute= dp.get_precision('Account'),
            multi='single', store=False),
        'price_line_incl': fields.function(
            _amount_line_single, string='Line subtotal incl. taxes', type="float",
            digits_compute= dp.get_precision('Account'),
            multi='single', store=False),
        'price_line_excl': fields.function(
            _amount_line_single, string='Line subtotal excl. taxes', type="float",
            digits_compute= dp.get_precision('Account'),
            multi='single', store=False),
        }

