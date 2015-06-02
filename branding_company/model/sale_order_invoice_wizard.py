# -*- coding: utf-8 -*-
"""Extend wizard model that creates invoices from sale-order."""
##############################################################################
#
#    Odoo, an open source suite of business applications
#    This module copyright (C) 2014-2015 Therp BV <http://therp.nl>.
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
from openerp import models


class SaleOrderInvoiceWizard(models.Model):
    """Extend sale.advance.payment.inv model.

    Pass shop id to newly created invoices.
    """
    _inherit = "sale.advance.payment.inv"

    def create_invoices(self, cr, uid, ids, context=None):
        """Add branding_company_id to new invoices created."""
        res = super(SaleOrderInvoiceWizard, self).create_invoices(
            cr, uid, ids, context=context)
        sale_ids = context.get('active_ids', [])
        if sale_ids:
            # Go through all active sale-orders.
            sale_model = self.pool['sale.order']
            for sale_obj in sale_model.browse(
                    cr, uid, sale_ids, context=context):
                if sale_obj.branding_company_id:
                    for invoice_obj in sale_obj.invoice_ids:
                        # Fill branding_company_id in invoices that don't
                        # have one yet.
                        if not invoice_obj.branding_company_id:
                            invoice_obj.write(
                                {'branding_company_id':
                                    sale_obj.branding_company_id.id},
                                context=context
                            )
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
