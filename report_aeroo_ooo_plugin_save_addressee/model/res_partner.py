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
from openerp.osv.orm import Model
from openerp.tools.translate import _


class ResPartner(Model):
    _inherit = 'res.partner'

    def button_show_mailmerges(self, cr, uid, ids, context=None):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Mail merges'),
            'view_type': 'form',
            'views': [(False, 'tree'), (False, 'form')],
            'res_model': 'aeroo.mailmerge',
            'domain': [('partner_ids', 'in', ids)],
        }
