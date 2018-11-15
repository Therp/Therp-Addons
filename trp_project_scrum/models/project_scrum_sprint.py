# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProjectScrumSprint(models.Model):
    _inherit = 'project.scrum.sprint'
    _order = 'name ASC'
