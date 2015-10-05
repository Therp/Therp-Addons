# -*- coding: utf-8 -*-
"""Adds a fiscal position to a country."""
##############################################################################
#
#    Copyright (C) 2011 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2011 Domsense srl (<http://www.domsense.com>)
#    Copyright (C) 2015 Therp BV (https://therp.nl)
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields


class Country(models.Model):
    """Adds a fiscal position to a country."""
    _inherit = 'res.country'
    property_account_position = fields.Many2one(
        comodel_name='account.fiscal.position',
        string="Default Fiscal Position",
        company_dependent=True,
        help="The fiscal position will determine taxes and the accounts"
             " used for the country, if not set specifically elsewere.",
    )
