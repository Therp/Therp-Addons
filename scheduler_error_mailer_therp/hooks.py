# -*- coding: utf-8 -*-
# Copyright 2016-2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, pool):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["ir.cron"].with_context(active_test=False).search([]).write(
        {
            "email_template_id": env.ref(
                "scheduler_error_mailer.scheduler_error_mailer"
            ).id
        }
    )
