# -*- coding: utf-8 -*-
"""Extend stock.picking with branding."""
##############################################################################
#
#    Copyright (C) 2014-2015 Therp BV <http://therp.nl>.
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
from openerp import models, fields


class StockPicking(models.Model):
    """Extend stock.picking with branding."""
    _inherit = 'stock.picking'

    def _compute_branding(self):
        """Branding for a delivery order is taken from sales order.

        We use the procurement group to find all relates sale orders.
        The first sale order found will determine the branding.
        """
        sale_model = self.env['sale.order']
        sale_orders = sale_model.search([
            ('procurement_group_id', '=', self.group_id.id)])
        return sale_orders.branding_id.id

    def _create_invoice_from_picking(
            self, cr, uid, picking, vals, context=None):
        """Add branding_id to invoice if present in stock.picking."""
        vals['branding_id'] = picking.branding_id.id
        return super(StockPicking, self)._create_invoice_from_picking(
            cr, uid, picking, vals, context=context)

    branding_id = fields.Many2one(
        string='Branding Company',
        comodel_name='branding.company',
        compute='_compute_branding',
        oldname='branding_company_id',
    )
