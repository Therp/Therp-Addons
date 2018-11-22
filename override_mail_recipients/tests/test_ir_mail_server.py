# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import SingleTransactionCase


class TestIrMailServer(SingleTransactionCase):

    post_install = True

    def setUp(self):
        super(TestIrMailServer, self).setUp()
        self.env.ref(
            'override_mail_recipients.override_email_to').value = 't@test.com'
        self.message = self.env['ir.mail_server'].build_email(
            email_from='from@example.com',
            email_to=['to@example.com'],
            subject='Subject',
            body='test body',
            email_cc=['cc@example.com'],
            email_bcc=['bcc@example.com'],
        )

    def test_send_email(self):
        self.env['ir.mail_server'].send_email(self.message)
        self.assertEquals(self.message['to'], '"to(at)example.com" <t@test.com>')
        self.assertEquals(self.message['cc'], '"cc(at)example.com" <t@test.com>')
