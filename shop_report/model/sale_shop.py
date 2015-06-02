# -*- coding: utf-8 -*-
"""Create sale.shop model."""
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
from openerp import models, fields


class SaleShop(models.Model):
    """Create sale.shop model.

    This model existed in 7.0 and before but was dropped in 8.0.
    Therefore we create the model van scratch, with just the fields needed
    for separate branding.
    """
    _name = "sale.shop"
    _description = """\
        Allow for multiple shops, with their own branding, within company."""

    name = fields.Char(
        string='Shop Name',
        size=64,
        required=True
    )
    company_id = fields.Many2one(
        string='Company',
        comodel_name='res.company',
        required=False
    )
    logo_company_id = fields.Many2one(
        string="Logo company",
        comodel_name='res.company',
        required=True
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
