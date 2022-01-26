# -*- coding: utf-8 -*-
# Copyright 2016-2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class IrCron(models.Model):
    _inherit = "ir.cron"

    email_template_id = fields.Many2one(
        default=lambda self: self.env.ref(
            "scheduler_error_mailer.scheduler_error_mailer"
        )
    )
