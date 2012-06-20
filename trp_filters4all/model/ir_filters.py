# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2012 Therp BV (<http://therp.nl>).
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

from osv import osv, fields

class ir_filters(osv.osv):

    _inherit = 'ir.filters'

    _columns = {
        # set user_id to cascade to prevent a user's filters going
        # public after the user is deleted.
        # Update the help text as well.
        'user_id': fields.many2one(
            'res.users', 'User',
            help=("The user this filter is available to. When left empty the "
                  "filter is usable by everyone."),
            ondelete='CASCADE',
            ),
        'create_uid': fields.many2one(
            'res.users', 'Created by', readonly=True,
            help=("The user that created the filter and that is allowed to "
                  "change or delete the filter"),
            ),
        }

    def get_filters(self, cr, uid, model):
        """
        Allow users to make filters available for all users by 
        removing the user_id
        """
        # act_ids = self.search(cr,uid,[('model_id','=',model),('user_id','=',uid)])
        act_ids = self.search(cr,uid,[('model_id','=',model),'|',('user_id','=',uid),('user_id','=',False)])
        my_acts = self.read(cr, uid, act_ids, ['name', 'domain','context'])
        return my_acts
