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
import base64
from osv import osv, fields
from tools.translate import _

class account_invoice(osv.osv):
    _name = 'account.invoice'
    _inherit = ['mail.thread', 'account.invoice']

    def message_new(
        self, cr, uid, msg_dict, custom_values=None, context=None):
        """
        Override this mail.thread method in order to compose a set of
        valid values for the invoice to be created
        """       
        if context is None:
            context = {}
            
        users_pool = self.pool.get('res.users')
        attachment_pool = self.pool.get('ir.attachment')
        data_pool = self.pool.get('ir.model.data')

        # As the scheduler is run without language,
        # set the administrator's language
        if not context.get('lang'):
            context['lang'] = users_pool.read(
                cr, uid, uid, ['context_lang'])['context_lang']

        if custom_values is None:
            custom_values = {}

        custom_values.update({
                'type': 'in_invoice',
                })       

        email_from = msg_dict.get('from', False)
        if email_from:
            custom_values['name'] = _("Received by email from %s") % email_from

        email_date = msg_dict.get('date', False)
        if email_date:
            custom_values['date_invoice'] = email_date

        # Retrieve partner_id from the email address
        # and add related field values
        custom_values['partner_id'] = (
            self.message_partner_by_email(
                cr, uid, email_from, context=None)['partner_id']
            or data_pool.get_object_reference(
                cr, uid, 'fetchmail_invoice', 'default_partner')[1])
        custom_values.update(
            self.onchange_partner_id(
                cr, uid, [], 'in_invoice',
                custom_values['partner_id'],
                )['value']
            )

        # Create the resource
        res_id = super(account_invoice, self).message_new(
            cr, uid, msg_dict, custom_values=custom_values, context=context)
        
        return res_id
