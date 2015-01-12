# -*- coding: utf-8 -*-

import re
from openerp.osv import orm, fields


class SaleOrderLine(orm.Model):
    _inherit = 'sale.order.line'

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
                          fiscal_position=False, flag=False, context=None):
        """
        Remove product code from sale order line name
        """
        res = super(SaleOrderLine, self).product_id_change(
            cr, uid, ids, pricelist, product, qty=qty, uom=uom,
            qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging,
                          fiscal_position=fiscal_position, flag=flag, context=context)
        if res.get('value', {}).get('name'):
            match = re.match('(\[[^\]]*\] )', res['value']['name'])
            if match:
                res['value']['name'] = res['value']['name'][len(match.group(1)):]
        return res

