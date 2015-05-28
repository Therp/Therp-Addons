# -*- coding: utf-8 -*-
"""Extend stock.picking for shop_report."""
##############################################################################
#
#    Odoo, an open source suite of business applications
#    This module copyright (C) 2014 Therp BV <http://therp.nl>.
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
from openerp.osv.orm import Model
from openerp.osv import fields


class StockPicking(Model):
    """Extend stock.picking for shop_report."""
    _inherit = 'stock.picking'

    def _prepare_invoice(
            self, cr, uid, picking, partner, inv_type, journal_id,
            context=None):
        """Add shop_id to invoice if present in stock.picking."""
        invoice_vals = super(StockPicking, self)._prepare_invoice(
            cr, uid, picking, partner, inv_type, journal_id, context=context)
        if picking.shop_id:
            invoice_vals['shop_id'] = picking.shop_id.id
        return invoice_vals

    _columns = {
        'shop_id': fields.related(
            'sale_id', 'shop_id', type='many2one', obj='sale.shop'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
