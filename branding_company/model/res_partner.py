# -*- coding: utf-8 -*-
# © 2014-2015 Therp BV (http://therp.nl).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class ResPartner(models.Model):
    """Extend res.partner model to link partner to branding.

    Set default branding for documents created for this partner.
    """
    _inherit = "res.partner"

    branding_id = fields.Many2one(
        comodel_name='branding.company',
        string='Branding Company',
        oldname='branding_company_id',
    )
