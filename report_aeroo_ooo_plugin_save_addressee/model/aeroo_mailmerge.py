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
import datetime
from openerp.osv.orm import Model
from openerp.osv import fields
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT


class AerooMailmerge(Model):
    _name = 'aeroo.mailmerge'
    _description = 'Mailmerge'
    _order = 'create_date desc, filter_id'

    _columns = {
        'filter_id': fields.many2one('ir.filters', 'Filter', required=True),
        'create_date': fields.datetime('Created', required=True),
        'create_uid': fields.many2one('res.users', 'User', required=True),
        'template': fields.binary('Template', required=True),
        'partner_ids': fields.many2many(
            'res.partner', 'aeroo_mailmerge_partner_rel', 'mailmerge_id',
            'partner_id', string='Partners'),
    }

    def name_get(self, cr, uid, ids, context=None):
        user = self.pool['res.users'].browse(cr, uid, uid, context=context)
        res_lang = self.pool['res.lang']
        lang = res_lang.browse(
            cr, uid,
            res_lang.search(
                cr, uid, [('code', '=', user.partner_id.lang)],
                context=context)[0],
            context=context)
        return [
            (this.id, '%s [%s]' % (
                this.filter_id.name,
                datetime.datetime.strptime(
                    this.create_date, DEFAULT_SERVER_DATETIME_FORMAT).strftime(
                    lang.date_format)))
            for this in self.browse(cr, uid, ids, context=context)
        ]
