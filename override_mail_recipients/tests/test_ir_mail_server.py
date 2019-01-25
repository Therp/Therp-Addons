# -*- coding: utf-8 -*-
# Copyright 2018-2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import SingleTransactionCase


class TestIrMailServer(SingleTransactionCase):

    post_install = True

    def setUp(self):  # pylint: disable=invalid-name
        super(TestIrMailServer, self).setUp()
        self.message = self.env['ir.mail_server'].build_email(
            email_from='from@example.com',
            email_to=['to@example.com'],
            subject='Subject',
            body='test body',
            email_cc=['cc@example.com'],
            email_bcc=['bcc@example.com'])

    def test_valid_override(self):
        self.env.ref(
            'override_mail_recipients.override_email_to'
        ).value = 't@test.com'
        self.env['ir.mail_server'].patch_message(self.message)
        self.assertEquals(
            self.message['to'], '"to(at)example.com" <t@test.com>')
        self.assertEquals(
            self.message['cc'], '"cc(at)example.com" <t@test.com>')

    def test_invalid_override(self):
        self.env.ref(
            'override_mail_recipients.override_email_to'
        ).value = 'not going to work'
        with self.assertRaises(AssertionError):
            self.env['ir.mail_server'].patch_message(self.message)

    def test_disable_override(self):
        self.env.ref(
            'override_mail_recipients.override_email_to'
        ).value = 'disable'
        self.env['ir.mail_server'].patch_message(self.message)
        self.assertEquals(
            self.message['to'], 'to@example.com')
        self.assertEquals(
            self.message['cc'], 'cc@example.com')
