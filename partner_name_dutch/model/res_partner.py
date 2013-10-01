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
from mako.template import Template
from openerp.osv.orm import Model
from openerp.osv import fields


class res_partner(Model):
    _inherit = 'res.partner'
    _name_fields = ['firstname', 'lastname', 'initials', 'infix']

    def _compute_name_custom(self, cursor, uid, ids, fname, arg,
                             context=None):
        if context is None:
            context = {}

        name_template = Template(
                context.get(
                    'name_format',
                    "${firstname or initials or ''}"
                    "${(firstname or initials) and ' ' or ''}"
                    "${infix or ''}${infix and ' ' or ''}${lastname}"))

        result = {}
        for rec in self.read(cursor, uid, ids, self._name_fields):
            result[rec['id']] = name_template.render(**rec)
        return result

    def _write_name(self, cursor, uid, partner_id, field_name, field_value,
            arg, context=None):
        return super(res_partner, self)._write_name(
                cursor, uid, partner_id, field_name, field_value, arg,
                context=context)

    _columns = {
            'name': fields.function(_compute_name_custom, string="Name",
                type="char", store=True,
                select=True, readonly=True,
                fnct_inv=_write_name),
            'initials': fields.char('Initials', size=8),
            'infix': fields.char('Infix', size=32),
            }
