# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Therp BV (<http://therp.nl>).
#    Most of the code in the method below Copyright (C) OpenERP S.A.    
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
from openerp import tools
from openerp import SUPERUSER_ID
from openerp.osv import orm
from openerp.addons.mail.mail_mail import mail_mail, _logger

def send(self, cr, uid, ids, auto_commit=False, recipient_ids=None, context=None):
        """
        Copy of this method in mail.mail. If an error occurs when sending
        a mail, write the error in the mail record itself.

        This method is monkeypatched into the original model, to preserve
        inheritance of this method.
        """
        ir_mail_server = self.pool.get('ir.mail_server')
        for mail in self.browse(cr, uid, ids, context=context):
            try:
                # handle attachments
                attachments = []
                for attach in mail.attachment_ids:
                    attachments.append((attach.datas_fname, base64.b64decode(attach.datas)))
                # specific behavior to customize the send email for notified partners
                email_list = []
                if recipient_ids:
                    partner_obj = self.pool.get('res.partner')
                    existing_recipient_ids = partner_obj.exists(cr, SUPERUSER_ID, recipient_ids, context=context)
                    for partner in partner_obj.browse(cr, SUPERUSER_ID, existing_recipient_ids, context=context):
                        email_list.append(self.send_get_email_dict(cr, uid, mail, partner=partner, context=context))
                else:
                    email_list.append(self.send_get_email_dict(cr, uid, mail, context=context))

                # build an RFC2822 email.message.Message object and send it without queuing
                res = None
                for email in email_list:
                    msg = ir_mail_server.build_email(
                        email_from = mail.email_from,
                        email_to = email.get('email_to'),
                        subject = email.get('subject'),
                        body = email.get('body'),
                        body_alternative = email.get('body_alternative'),
                        email_cc = tools.email_split(mail.email_cc),
                        reply_to = email.get('reply_to'),
                        attachments = attachments,
                        message_id = mail.message_id,
                        references = mail.references,
                        object_id = mail.res_id and ('%s-%s' % (mail.res_id, mail.model)),
                        subtype = 'html',
                        subtype_alternative = 'plain')
                    res = ir_mail_server.send_email(cr, uid, msg,
                        mail_server_id=mail.mail_server_id.id, context=context)
                if res:
                    mail.write({'state': 'sent', 'message_id': res})
                    mail_sent = True
                else:
                    mail.write({'state': 'exception'})
                    mail_sent = False

                # /!\ can't use mail.state here, as mail.refresh() will cause an error
                # see revid:odo@openerp.com-20120622152536-42b2s28lvdv3odyr in 6.1
                if mail_sent:
                    self._postprocess_sent_message(cr, uid, mail, context=context)
            except Exception, e:
                _logger.exception('failed sending mail.mail %s', mail.id)
                ### mail_error start changes
                vals = {'state': 'exception'}
                if 'error_msg' in mail._columns and e.args:
                    vals['error_msg'] = e.args[-1]
                mail.write(vals)
                ### mail_error stop changes

            if auto_commit == True:
                cr.commit()
        return True


class MailMailMonkeypatch(orm.AbstractModel):
    _name = 'mail.mail.monkeypatch'
    _description = 'Mail model monkeypatch'


    def _register_hook(self, cr):
        mail_mail.send = send
        return super(MailMailMonkeypatch, self)._register_hook(cr)
