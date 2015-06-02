# -*- coding: utf-8 -*-
"""Extend stock.picking with branding."""
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


class StockPicking(models.Model):
    """Extend stock.picking with branding."""
    _inherit = 'stock.picking'

    def _prepare_invoice(
            self, cr, uid, picking, partner, inv_type, journal_id,
            context=None):
        """Add branding_company_id to invoice if present in stock.picking."""
        vals = super(StockPicking, self)._prepare_invoice(
            cr, uid, picking, partner, inv_type, journal_id, context=context)
        if picking.branding_company_id:
            vals['branding_company_id'] = picking.branding_company_id.id
        return vals

    branding_company_id = fields.Many2one(
        string='Branding Company',
        comodel_name='branding.company',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
