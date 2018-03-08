# -*- coding: utf-8 -*-
# Copyright 2013-2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _default_groups(self):
        """Disable default assignment of group 'users' and 'partner manager'"""
        filter_groups = self.env.ref('base.group_user') + self.env.ref(
            'base.group_partner_manager'
        )
        return super(ResUsers, self)._default_groups().filtered(
            lambda x: not x & filter_groups
        )

    @api.depends('groups_id')
    def _compute_is_external_user(self):
        for this in self:
            this.is_external_user = self.env['ir.model.access'].sudo(this)\
                .check_groups('trp_external_user.group_external_user')

    external_user_partner_ids = fields.Many2many(
        'res.partner', 'trp_external_user_partner_id_rel',
        'user_id', 'partner_id',
        'External access to related partners',
    )
    is_external_user = fields.Boolean(
        'Is external user', compute='_compute_is_external_user',
    )
    groups_id = fields.Many2many(default=lambda self: self._default_groups())
