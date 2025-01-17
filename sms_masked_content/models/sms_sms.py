# Copyright 2024 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import api, fields, models


class SmsSms(models.Model):
    _inherit = "sms.sms"

    unmasked_body = fields.Text(
        help="Field that temporarily holds body as it is to be sent"
    )

    @api.model_create_multi
    def create(self, vals_list):
        """
        Write unmasked_body if we get one passed
        """
        return super().create(
            dict(
                vals,
                unmasked_body=vals.get(
                    "unmasked_body", getattr(vals.get("body"), "unmasked_content", None)
                ),
            )
            for vals in vals_list
        )

    def write(self, vals):
        """
        When sms is marked as sent or cancelled, remove its unmasked body
        """
        if vals.get("state") in ("sent", "canceled"):
            vals["unmasked_body"] = False
        return super().write(vals)
