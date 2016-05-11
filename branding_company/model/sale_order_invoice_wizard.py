# -*- coding: utf-8 -*-
# © 2014-2015 Therp BV (http://therp.nl).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models


class SaleOrderInvoiceWizard(models.Model):
    """Extend sale.advance.payment.inv model.

    Pass branding id to newly created invoices.
    """
    _inherit = "sale.advance.payment.inv"

    @api.multi
    def create_invoices(self):
        """Add branding_id to new invoices created."""
        res = super(SaleOrderInvoiceWizard, self).create_invoices()
        sale_ids = self.env.context.get('active_ids', [])
        if not sale_ids:
            return
        # Go through all active sale-orders.
        for sale_obj in self.env['sale.order'].browse(sale_ids):
            if sale_obj.branding_id:
                for invoice_obj in sale_obj.invoice_ids:
                    # Fill branding_id in invoices that don't have one yet.
                    if not invoice_obj.branding_id:
                        invoice_obj.write(
                            {'branding_id': sale_obj.branding_id.id},
                        )
        return res
