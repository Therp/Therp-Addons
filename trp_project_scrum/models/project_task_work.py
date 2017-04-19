# -*- coding: utf-8 -*-
from openerp import _, api, exceptions, fields, models


class ProjectTaskWork(models.Model):
    _inherit = "project.task.work"

    @api.model
    def get_product_for_collaborator(self):
        # defaults for therp
        product_id = self.env['product.product'].browse(
            self.env['hr.employee']._getEmployeeProduct()
        )
        return product_id

    @api.model
    def get_user_related_details(self, user_id):
        emp_obj = self.env['hr.employee']
        user = self.env['res.users'].browse(
            user_id or self._uid
        )
        emp_id = user.employee_ids
        if not emp_id[0] and user.sudo().has_group(
                'trp_project_scrum.collaborators_followers'):
            product_id = self.sudo().get_product_for_collaborator()
            general_account = (
                product_id.categ_id.property_account_expense_categ.id
                or product_id.property_account_expense.id
            )
            if not general_account:
                raise exceptions.Warning(_(
                    'No account chosen for this user, and no other user to'
                    'copy account from was found, contact admin'))
            res = {
                'product_id': product_id.id,
                'journal_id': self.env['hr.employee']._getAnalyticJournal(),
                'general_account_id': general_account,
                'product_uom_id': product_id.uom_id.id
            }
            return res

        res = super(ProjectTaskWork, self).get_user_related_details(user_id)
        return res
