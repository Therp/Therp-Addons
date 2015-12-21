# -*- coding: utf-8 -*-
# © 2015 Therp BV (http://therp.nl).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class ResUsers(models.Model):
    """Extend res.users model to link user to branding.

    Set default branding for sales orders and invoices created by this user.
    """
    _inherit = "res.users"

    branding_id = fields.Many2one(
        comodel_name='branding.company',
        string='Branding Company',
        oldname='branding_company_id',
    )
