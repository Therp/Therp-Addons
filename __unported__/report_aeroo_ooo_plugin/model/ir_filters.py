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


class IrFilters(Model):
    _inherit = 'ir.filters'

    def get_libreoffice_filters(self, cr, uid, context=None):
        result = []
        for this in self.browse(
                cr, uid,
                self.search(
                    cr, uid,
                    [('user_id', 'in', [uid, False])],
                    order='model_id, name',
                    context=context),
                context=context):
            model = self.pool['ir.model'].browse(
                cr, uid,
                self.pool['ir.model'].search(
                    cr, uid, [('model', '=', this.model_id)],
                    context=context)[0],
                context)
            result.append(
                (
                    this.id,
                    "%s (%s)" % (this.name, model.name),
                )
            )
        return result
