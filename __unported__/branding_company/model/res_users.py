# -*- coding: utf-8 -*-
"""Extend res.users model to link user to branding."""
##############################################################################
#
#    Copyright (C) 2015 Therp BV <http://therp.nl>.
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


class ResUsers(models.Model):
    """Extend res.users model to link user to branding.

    Set default branding for sales orders and invoices created by this user.
    """
    _inherit = "res.users"

    branding_id = fields.Many2one(
        string='Branding Company',
        comodel_name='branding.company',
        oldname='branding_company_id',
    )
