# -*- coding: utf-8 -*-
"""Extend sale.order model."""
##############################################################################
#
#    Copyright (C) 2014-2015 Therp BV <http://therp.nl>.
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
from openerp import api, models, fields


class SaleOrder(models.Model):
    """Extend sale.order model.

    Set default shop from user, and pass shop id to invoice.
    """
    _inherit = "sale.order"

    @api.multi
    def onchange_partner_id(self, partner_id):
        """When partner changes, branding company changes.

        Decorater @api.onchange did not work.
        """
        result = super(SaleOrder, self).onchange_partner_id(partner_id)
        partner_model = self.env['res.partner']
        vals = 'value' in result and result['value'] or {}
        if partner_id:
            partner_obj = partner_model.browse(partner_id)
            branding_company_id = (
                partner_obj and partner_obj.branding_company_id and
                partner_obj.branding_company_id.id or False)
        if not branding_company_id:
            branding_company_id = self._get_user_branding_company()
        vals['branding_company_id'] = branding_company_id
        result['value'] = vals
        return result

    def _get_user_branding_company(self):
        """Default branding dependent on active user."""
        user_model = self.env['res.users']
        user_objs = user_model.browse(self.env.uid)
        return (
            user_objs and user_objs[0].branding_company_id and
            user_objs[0].branding_company_id or False
        )

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        """Pass branding_company_id to invoice created."""
        invoice_vals = super(SaleOrder, self)._prepare_invoice(
            cr, uid, order, lines, context=context)
        invoice_vals['branding_company_id'] = (
            order.branding_company_id and order.branding_company_id.id or
            False
        )
        return invoice_vals

    branding_company_id = fields.Many2one(
        string='Branding Company',
        comodel_name='branding.company',
        default=_get_user_branding_company,
    )
