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
from openerp import models, fields


class ProductBacklog(models.Model):
    _inherit = 'project.scrum.product.backlog'

    # New field
    tech_details = fields.Text('Technical details')

    # Change some field labels
    role_id = fields.Many2one(string='As a')
    for_then = fields.Char('So that')

    def create(self, cr, uid, values, context=None):
        """
        Subscribe the project manager to new user stories
        """
        res_id = super(ProductBacklog, self).create(
            cr, uid, values, context=context)
        story = self.browse(cr, uid, res_id, context=context)
        if story.project_id.user_id:
            story.message_subscribe_users(
                user_ids=[story.project_id.user_id.id],
                )
        return res_id
