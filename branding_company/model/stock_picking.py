# -*- coding: utf-8 -*-
# © 2014-2015 Therp BV (http://therp.nl).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _compute_branding(self):
        """Branding for a delivery order is taken from sales order.

        We use the procurement group to find all related sale orders.
        The first sale order found will determine the branding.
        """
        sale_model = self.env['sale.order']
        for rec in self:
            sale_orders = sale_model.search([
                ('procurement_group_id', '=', rec.group_id.id),
            ])
            rec.branding_id = sale_orders.branding_id

    @api.model
    def _create_invoice_from_picking(self, picking, vals):
        """Add branding_id to invoice if present in stock.picking."""
        vals['branding_id'] = picking.branding_id.id
        return super(StockPicking, self)._create_invoice_from_picking(
            picking, vals)

    branding_id = fields.Many2one(
        string='Branding Company',
        comodel_name='branding.company',
        compute='_compute_branding',
        oldname='branding_company_id',
    )
