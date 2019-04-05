# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    @api.multi
    @api.depends('project_ids')
    def _compute_project_ids_followers(self):
        for rec in self:
            rec.project_ids_followers = rec.project_ids.mapped(
                'message_partner_ids').ids

    project_ids_followers = fields.Many2many(
        'res.partner',
        compute='_compute_project_ids_followers',
        store=True,
    )
