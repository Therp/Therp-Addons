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
        self._set_configuration('t@test.com')
        self._patch_message(self.message)
        self.assertEquals(
            self.message['to'], '"to(at)example.com" <t@test.com>')
        self.assertEquals(
            self.message['cc'], '"cc(at)example.com" <t@test.com>')

    def test_invalid_override(self):
        self._set_configuration('not going to work')
        with self.assertRaises(AssertionError):
            self._patch_message(self.message)

    def test_disable_override(self):
        self._set_configuration('disable')
        self._patch_message(self.message)
        self.assertEquals(
            self.message['to'], 'to@example.com')
        self.assertEquals(
            self.message['cc'], 'cc@example.com')

    def _set_configuration(self, value):
        """Set override mail configuration."""
        config_model = self.env['ir.config_parameter']
        config_model.set_param(
            'override_mail_recipients.override_to', value)

    def _patch_message(self, message):
        """Let mail server patch message, with test_override in context."""
        server_model = self.env['ir.mail_server'].with_context(
            test_override_mail=True)
        server_model.patch_message(message)
