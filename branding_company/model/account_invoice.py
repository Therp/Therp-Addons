# -*- coding: utf-8 -*-
# © 2014-2015 Therp BV (http://therp.nl).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class AccountInvoice(models.Model):
    """Extend account.invoice with branding_id."""
    # pylint: disable=too-many-public-methods
    _inherit = 'account.invoice'

    @api.onchange('partner_id')
    def onchange_partner_id_api(self):
        """When partner changes, branding company changes."""
        # pylint: disable=no-member
        if self.partner_id:
            branding_model = self.env['branding.company']
            branding = (
                branding_model.get_default_branding(
                    self.partner_id, self.env.uid)
            )
            if branding:
                self.branding_id = branding.id

    def _get_user_branding(self):
        """Default branding dependent on active user."""
        branding_model = self.env['branding.company']
        return branding_model.get_user_branding(self.env.uid).id

    branding_id = fields.Many2one(
        string='Branding',
        comodel_name='branding.company',
        default=_get_user_branding,
        oldname='branding_company_id',
    )
