# -*- coding: utf-8 -*-
# Copyright 2015-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models
from email.utils import COMMASPACE
from odoo.addons.base.ir.ir_mail_server import extract_rfc2822_addresses


class IrMailServer(models.Model):
    _inherit = 'ir.mail_server'

    @api.model
    def send_email(
            self, message, mail_server_id=None, smtp_server=None,
            smtp_port=None, smtp_user=None, smtp_password=None,
            smtp_encryption=None, smtp_debug=False, smtp_session=None):
        override_email = self.env.ref(
            'override_mail_recipients.override_email_to').value
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
            message, mail_server_id=mail_server_id,
            smtp_server=smtp_server, smtp_port=smtp_port, smtp_user=smtp_user,
            smtp_password=smtp_password, smtp_encryption=smtp_encryption,
            smtp_debug=smtp_debug, smtp_session=smtp_session)
