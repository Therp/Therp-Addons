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
from openerp.osv import fields

class MailMessage(Model):
    _inherit = 'mail.message'

    def fetchmail_inbox_attach_existing(self, cr, uid, ids, context=None):
        return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'target': 'new',
                'res_model': 'fetchmail.inbox.attach.existing.wizard',
                'context': {
                    'default_mail_id': ids and ids[0],
                    'default_res_model': 'account.invoice',
                    },
                }

    def fetchmail_inbox_create(self, cr, uid, ids, context=None):
        return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'target': 'new',
                'res_model': 'fetchmail.inbox.create.wizard',
                'context': {
                    'default_mail_id': ids and ids[0],
                    },
                }


    def fetchmail_inbox_move_to_record(self, cr, uid, ids, res_model, res_id,
                                       context=None):
        inbox_ids = self.pool.get('fetchmail.inbox').search(
                cr, uid, [('message_ids', '=', ids)], context=context)
        self.write(
                cr, uid, ids,
                {
                    'model': res_model,
                    'res_id': res_id,
                },
                context=context)
        self.pool.get('fetchmail.inbox').unlink(cr, uid, inbox_ids,
                                                context=context)

