# -*- coding: utf-8 -*-
# © 2015 Therp BV (http://therp.nl).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('country_id')
    def onchange_country_id(self):
        """Change partner fiscal position according to country of partner.

        This method will override existing fiscal positions, even if the
        partner has a fiscal position set, and the new country has not.
        """
        if not self.country_id:
            return False
        self.property_account_position = (
            self.country_id.property_account_position.id)
