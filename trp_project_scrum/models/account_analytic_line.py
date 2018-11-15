# -*- coding: utf-8 -*-
# Copyright 2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, exceptions, models


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.model
    def create(self, vals):
        vals.update(self._get_user_related_details())
        return super(AccountAnalyticLine, self).create(vals)

    @api.multi
    def write(self, vals):
        vals.update(self._get_user_related_details())
        return super(AccountAnalyticLine, self).write(vals)

    @api.model
    def _get_user_related_details(self):
        emp_id = self.env.user.sudo().employee_ids[0]
        res = {}
        if emp_id and self.env.user.sudo().has_group(
                'trp_project_scrum.collaborators_followers'):
            product_id = emp_id.product_id
            general_account = (
                product_id.categ_id.property_account_expense_categ.id
                or product_id.property_account_expense.id
            )
            if not general_account:
                raise exceptions.Warning(_(
                    'No account chosen for this user, and no other user to '
                    'copy account from was found, contact admin'))
            res = {
                'product_id': product_id.id,
                'general_account_id': general_account,
                'product_uom_id': product_id.uom_id.id
            }
        return res
