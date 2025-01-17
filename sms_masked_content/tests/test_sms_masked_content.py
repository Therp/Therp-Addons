# Copyright 2024 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from unittest import mock

from odoo.tests.common import TransactionCase


def _contact_iap_success(local_endpoint, params):
    return [dict(message, state="success") for message in params["messages"]]


def _contact_iap_failure(local_endpoint, params):
    return [dict(message, state="server_error") for message in params["messages"]]


class TestSmsMaskedContent(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template = cls.env.ref("sms_masked_content.template_demo")
        cls.partner = cls.env.ref("base.user_demo").partner_id

    def test_masking_message_post(self):
        """Test that masked content is hidden"""
        last_sms = self.env["sms.sms"].search([], order="id desc", limit=1)
        last_message = self.env["mail.message"].search([], order="id desc", limit=1)

        # successful sending should remove the sms, only leave masked content
        with mock.patch.object(
            self.env["sms.api"].__class__, "_contact_iap"
        ) as contact_iap:
            contact_iap.side_effect = _contact_iap_success
            self.partner._message_sms_with_template(self.template)

        self.assertIn(
            self.partner.name, contact_iap.call_args.args[1]["messages"][0]["content"]
        )

        new_sms = self.env["sms.sms"].search([("id", ">", last_sms.id or 0)])
        new_message = self.env["mail.message"].search(
            [("id", ">", last_message.id or 0)]
        )
        self.assertFalse(new_sms)
        self.assertIn("XXX", new_message.body)
        self.assertNotIn(self.partner.name, new_message.body)

        last_message = new_message

        # failed sending should keep unmasked content in sms.sms#unmasked_body
        with mock.patch.object(
            self.env["sms.api"].__class__, "_contact_iap"
        ) as contact_iap:
            contact_iap.side_effect = _contact_iap_failure
            self.partner._message_sms_with_template(self.template)

        self.assertIn(
            self.partner.name, contact_iap.call_args.args[1]["messages"][0]["content"]
        )

        new_sms = self.env["sms.sms"].search([("id", ">", last_sms.id or 0)])
        new_message = self.env["mail.message"].search(
            [("id", ">", last_message.id or 0)]
        )
        self.assertEqual(new_sms.state, "error")
        self.assertNotIn(self.partner.name, new_sms.body)
        self.assertIn(self.partner.name, new_sms.unmasked_body)
        self.assertNotIn(self.partner.name, new_message.body)

        with mock.patch.object(
            self.env["sms.api"].__class__, "_contact_iap"
        ) as contact_iap:
            contact_iap.side_effect = _contact_iap_success
            new_sms._send(unlink_sent=False)

        self.assertIn(
            self.partner.name, contact_iap.call_args.args[1]["messages"][0]["content"]
        )

        new_message = self.env["mail.message"].search(
            [("id", ">", last_message.id or 0)]
        )
        self.assertEqual(new_sms.state, "sent")
        self.assertNotIn(self.partner.name, new_sms.body)
        self.assertFalse(new_sms.unmasked_body)
        self.assertNotIn(self.partner.name, new_message.body)

    def test_masking_composer(self):
        """
        Test that masking works for code using the composer
        """
        composer = self.env["sms.composer"].create(
            {
                "composition_mode": "mass",
                "res_model": self.partner._name,
                "res_id": self.partner.id,
                "res_ids": str(self.partner.id),
                "template_id": self.template.id,
                "mass_force_send": True,
            }
        )

        with mock.patch.object(
            self.env["sms.api"].__class__, "_contact_iap"
        ) as contact_iap:
            contact_iap.side_effect = _contact_iap_success
            composer.action_send_sms()

        self.assertIn(
            self.partner.name, contact_iap.call_args.args[1]["messages"][0]["content"]
        )

        last_sms = self.env["sms.sms"].search([], order="id desc", limit=1)
        last_message = self.env["mail.message"].search([], order="id desc", limit=1)

        with mock.patch.object(
            self.env["sms.api"].__class__, "_contact_iap"
        ) as contact_iap:
            contact_iap.side_effect = _contact_iap_failure
            composer.action_send_sms()

        self.assertIn(
            self.partner.name, contact_iap.call_args.args[1]["messages"][0]["content"]
        )

        new_sms = self.env["sms.sms"].search([("id", ">", last_sms.id or 0)])
        new_message = self.env["mail.message"].search(
            [("id", ">", last_message.id or 0)]
        )
        self.assertEqual(new_sms.state, "error")
        self.assertNotIn(self.partner.name, new_sms.body)
        self.assertIn(self.partner.name, new_sms.unmasked_body)
        self.assertNotIn(self.partner.name, new_message.body)
