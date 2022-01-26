# Copyright 2016-2022 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
"""Define all post_init hooks for this module."""
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    """Set email template for all cron jobs to the scheduler error mailer template."""
    # pylint: disable=invalid-name,unused-argument
    env = api.Environment(cr, SUPERUSER_ID, {})
    mail_template = env.ref("scheduler_error_mailer.scheduler_error_mailer")
    all_crons = env["ir.cron"].with_context(active_test=False).search([])
    all_crons.write({"email_template_id": mail_template.id})
