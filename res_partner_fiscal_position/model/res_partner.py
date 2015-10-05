# -*- coding: utf-8 -*-
"""Extend model res.partner for country specific fiscal position."""
##############################################################################
#
#    Copyright (C) 2015 Therp BV <http://therp.nl>
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
from openerp import models, api


class ResPartner(models.Model):
    """Extend model res.partner for country specific fiscal position."""
    _inherit = 'res.partner'

    @api.onchange('country_id')
    def get_country_fiscal_position(self):
        """
        when changing the partner's country update the
        property_account_position to the one of that country
        """
        self.property_account_position = (
            self.country_id.property_account_position.id)
