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

class ResUsers(Model):
    _inherit = 'res.users'

    def _get_group(self,cr, uid, context=None):
        # Disable default assignment of group 'users' and 'partner manager'
        res = super(ResUsers, self)._get_group(cr, uid, context=context)
        dataobj = self.pool.get('ir.model.data')
        for group in ['group_user', 'group_partner_manager']:
            _model, group_id = dataobj.get_object_reference(cr, SUPERUSER_ID, 'base', group)
            if group_id in res:
                res.remove(group_id)
        return res

    _defaults = {
        # Refresh method reference
        'groups_id': _get_group,
        }

    def _is_external_user(
            self, cr, uid, ids, field_name, args, context=None):
        if not ids:
            return {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = {}
        access_obj = self.pool.get('ir.model.access')
        for res_id in ids:
            res[res_id] = access_obj.check_groups(
                cr, res_id, 'trp_external_user.group_external_user')
        return res

    _columns = {
        'external_user_partner_ids': fields.many2many(
            'res.partner', 'trp_external_user_partner_id_rel',
            'user_id', 'partner_id',
            'External access to related partners'),
        'is_external_user': fields.function(
            _is_external_user,
            string='Is external user', type='boolean'),
            }
