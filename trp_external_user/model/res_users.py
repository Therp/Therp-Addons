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
from openerp import api, fields, models, tools


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _get_group(self):
        # Disable default assignment of group 'users' and 'partner manager'
        res = super(ResUsers, self)._get_group()
        if tools.config['test_enable']:
            # don't change groups in test mode, a lot of tests rely on those
            # groups
            return res
        for group in ['group_user', 'group_partner_manager']:
            group_id = self.env.ref('base.%s' % group).id
            if group_id in res:
                res.remove(group_id)
        return res

    _defaults = {
        # Refresh method reference
        'groups_id': _get_group,
    }

    @api.one
    @api.depends('groups_id')
    def _is_external_user(self):
        self.is_external_user = self.env['ir.model.access'].sudo(self.id)\
            .check_groups('trp_external_user.group_external_user')

    external_user_partner_ids = fields.Many2many(
        'res.partner', 'trp_external_user_partner_id_rel',
        'user_id', 'partner_id',
        'External access to related partners')
    is_external_user = fields.Boolean(
        'Is external user', compute=_is_external_user)
