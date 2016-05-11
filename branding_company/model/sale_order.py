# -*- coding: utf-8 -*-
# © 2014-2015 Therp BV (http://therp.nl).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class SaleOrder(models.Model):
    """Extend sale.order model.

    Set default branding company from user, and pass branding company
    to invoice.
    """
    _inherit = "sale.order"

    @api.multi
    def onchange_partner_id(self, partner_id):
        """When partner changes, branding company changes.

        Would be nice if existing branding_id could be safe
        from change, but already existing onchange method only passes
        partner-id.

        Decorater @api.onchange did not work.
        """
        result = super(SaleOrder, self).onchange_partner_id(partner_id)
        if partner_id:
            branding_model = self.env['branding.company']
            branding = (
                branding_model.get_default_branding(
                    partner_id, self.env.uid)
            )
            if branding:
                vals = result.get('value', {})
                vals['branding_id'] = branding.id
                result['value'] = vals
        return result

    def _get_user_branding(self):
        """Default branding dependent on active user."""
        branding_model = self.env['branding.company']
        return branding_model.get_user_branding(self.env.uid).id

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        """Pass branding_id to invoice created."""
        invoice_vals = super(SaleOrder, self)._prepare_invoice(
            cr, uid, order, lines, context=context)
        invoice_vals['branding_id'] = order.branding_id.id
        return invoice_vals

    branding_id = fields.Many2one(
        string='Branding Company',
        comodel_name='branding.company',
        default=_get_user_branding,
        oldname='branding_company_id',
    )
