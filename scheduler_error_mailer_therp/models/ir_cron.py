# Copyright 2016-2022 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
"""Change default template to the one we want."""
from odoo import fields, models


class IrCron(models.Model):
    """Change default template to the one we want."""
    _inherit = "ir.cron"

    email_template_id = fields.Many2one(
        default=lambda self: self.env.ref(
            "scheduler_error_mailer.scheduler_error_mailer"
        )
    )
