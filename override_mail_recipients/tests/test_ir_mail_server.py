# Copyright 2018-2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=missing-docstring,protected-access
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
            email_bcc=['bcc@someotherdomain.com'])

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

    def test_domain_whitelist(self):
        self.env.ref(
            'override_mail_recipients.override_email_to'
        ).value = 'disable'
        self.env.ref(
            'override_mail_recipients.domain_whitelist'
        ).value = 'example.com'
        self.env['ir.mail_server'].patch_message(self.message)
        self.assertEquals(self.message['to'], 'to@example.com')
        self.assertEquals(self.message['cc'], 'cc@example.com')
        # bcc field will be fully deleted.
        self.assertEquals(self.message['bcc'], None)
        # Sending mail only outside of configured domain is an error.
        self.env.ref(
            'override_mail_recipients.domain_whitelist'
        ).value = 'domainnotinmessage.com'
        with self.assertRaises(AssertionError):
            self.env['ir.mail_server'].patch_message(self.message)

    def test_do_replacement(self):
        replacement = self.env['ir.mail_server']._do_replacement(
            '"Jansen \\ Pietersen" <jp@example.com>')
        self.assertEquals(
            replacement, '\\"Jansen  Pietersen\\" [jp(at)example.com]')
