# Copyright 2024 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import api, models


class SmsApi(models.AbstractModel):
    _inherit = "sms.api"

    @api.model
    def _send_sms_batch(self, messages):
        """
        If message body is a masked string, pass the unmasked content to super
        Otherwise, read the sms' unmasked_body field and pass that if set
        """
        SmsSms = self.env["sms.sms"]
        messages = [
            dict(
                message,
                content=getattr(
                    message.get("content"),
                    "unmasked_content",
                    SmsSms.browse(message.get("res_id") or []).unmasked_body
                    or message.get("content"),
                ),
            )
            for message in messages
        ]
        return super()._send_sms_batch(messages)
