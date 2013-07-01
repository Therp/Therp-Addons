# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>).
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
from openerp.osv import fields
from openerp.osv.orm import Model
from openerp import SUPERUSER_ID

class IrUiViewSc(Model):
    _inherit = 'ir.ui.view_sc'

    def copy(self, cr, uid, id, default=None, context=None):
        '''Override to disable default shortcuts added by some addons in their
        res_partner.create overrides if the user is an external one'''
        if default and default.get('user_id'):
            user = self.pool.get('res.users').browse(
                    cr, uid, default.get('user_id'), context=context)
            if user.is_external_user:
                return False

        return super(IrUiViewSc, self).copy(cr, uid, id, default=default,
                                            context=context)
