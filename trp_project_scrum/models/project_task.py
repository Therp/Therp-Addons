# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    def get_formview_id(self):
        if all(self.mapped('use_scrum')):
            return self.env.ref('project_scrum.view_ps_sprint_task_form2').id
        return False
