# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
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
from openerp import models
from email.Utils import COMMASPACE
from openerp.addons.base.ir.ir_mail_server import extract_rfc2822_addresses


class IrMailServer(models.Model):
    _inherit = 'ir.mail_server'

    def send_email(
            self, cr, uid, message, mail_server_id=None, smtp_server=None,
            smtp_port=None, smtp_user=None, smtp_password=None,
            smtp_encryption=None, smtp_debug=False, context=None):
        override_email = self.pool['ir.model.data'].xmlid_to_object(
            cr, uid, 'override_mail_recipients.override_email_to',
            raise_if_not_found=True, context=context).value
        if override_email:
            for field in ['to', 'cc', 'bcc']:
                if not message[field]:
                    continue
                original = COMMASPACE.join(message.get_all(field, []))
                del message[field]
                message[field] = COMMASPACE.join(
                    '"%s" <%s>' % (
                        original.replace('\\', '').replace('"', '\\"')
                        .replace('<', '[').replace('>', ']')
                        .replace('@', '(at)'),
                        email
                    )
                    for email in extract_rfc2822_addresses(override_email))
        return super(IrMailServer, self).send_email(
            cr, uid, message, mail_server_id=mail_server_id,
            smtp_server=smtp_server, smtp_port=smtp_port, smtp_user=smtp_user,
            smtp_password=smtp_password, smtp_encryption=smtp_encryption,
            smtp_debug=smtp_debug, context=context)
