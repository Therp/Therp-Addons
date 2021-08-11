# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class IrCron(models.Model):
    _inherit = 'ir.cron'

    email_template_id = fields.Many2one(
        default=lambda self:
        self.env.ref('scheduler_error_mailer.scheduler_error_mailer'))
