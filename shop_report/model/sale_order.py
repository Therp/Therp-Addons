# -*- coding: utf-8 -*-
"""Extend sale.order model."""
##############################################################################
#
#    Odoo, an open source suite of business applications
#    This module copyright (C) 2014 Therp BV <http://therp.nl>.
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
from openerp.exceptions import except_orm
from openerp.tools.translate import _


class SaleOrder(models.Model):
    """Extend sale.order model.

    Set default shop from user, and pass shop id to invoice."""
    _inherit = "sale.order"

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        """Pass shop_id to invoice created."""
        invoice_vals = super(SaleOrder, self)._prepare_invoice(
            cr, uid, order, lines, context=context)
        invoice_vals['shop_id'] = (
            order.shop_id and order.shop_id.id or False)
        return invoice_vals

    def _get_default_shop(self, cr, uid, context=None):
        """Set default shop_id from current user's company."""
        company_id = self.pool.get('res.users').browse(
            cr, uid, uid, context=context).company_id.id
        shop_ids = self.pool.get('sale.shop', 'company.logo').search(
            cr, uid, [('company_id', '=', company_id)], context=context)
        if not shop_ids:
            raise except_orm(
                _('Error!'),
                _('There is no default shop for the current user\'s company!')
            )
        return shop_ids[0]

    shop_id = fields.Many2one(
        string='Shop',
        comodel_name='sale.shop',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
