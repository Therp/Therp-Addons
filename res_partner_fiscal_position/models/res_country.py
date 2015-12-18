# -*- coding: utf-8 -*-
# © 2011 Agile Business Group sagl (http://www.agilebg.com).
# © 2011 Domsense srl (http://www.domsense.com).
# © 2015 Therp BV (http://therp.nl).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class Country(models.Model):
    """Add fiscal position to country."""
    _inherit = 'res.country'

    property_account_position = fields.Many2one(
        comodel_name='account.fiscal.position',
        string="Default Fiscal Position",
        company_dependent=True,
        help="The fiscal position will determine"
             " taxes and the accounts used for the country,"
             " if not set specifically elsewere.",
    )
