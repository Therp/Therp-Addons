# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Therp BV (<http://therp.nl>).
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
from openerp.osv.orm import TransientModel
from openerp.tools.safe_eval import safe_eval


class InstantAeroo(TransientModel):
    _inherit = 'instant.aeroo'

    def create_report(self, cr, uid, file_data, filter_id, context=None):
        saved_filter = self.pool['ir.filters'].browse(
            cr, uid, filter_id, context=context)
        partner_ids = []
        if saved_filter.model_id == 'res.partner':
            partner_ids = self.pool[saved_filter.model_id].search(
                cr, uid,
                safe_eval(saved_filter.domain),
                context=safe_eval(saved_filter.context))

        self.pool['aeroo.mailmerge'].create(
            cr, uid,
            {
                'filter_id': filter_id,
                'template': file_data,
                'partner_ids': [(6, 0, partner_ids)],
            },
            context=context)
        return super(InstantAeroo, self).create_report(
            cr, uid, file_data, filter_id, context=context)
