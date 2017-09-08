from openerp import models, api


class TemplateApproval(models.TransientModel):
    _name = "template.approve.wizard"

    @api.multi
    def get_approve(self):
        view_pool = self.env['ir.ui.view']
        view_id = view_pool.browse(self._context.get('active_ids'))[0]
        key = view_id.key.split('__')[0]
        view = view_pool.search([('key', '=', key), ('website_id', '=', view_id.website_id.id), ('is_webpage_template', '=', False)])[0]
        view_id.write({'state': 'approved', 'key': key, 'name': view.name, 'priority': view.priority})
        main_view = view_pool.search([('state', '=', 'main'), ('key', '=', key + '__main'), ('website_id', '=', view_id.website_id.id), ('is_webpage_template', '=', False)])[0]
        if main_view:
            view.unlink()
        else:
            view.write({'state': 'main', 'key': key + '__main', 'name': view.name + ' Main', 'user_id': self._uid, 'priority': 0})

        template_id = view_id.env['ir.model.data'].get_object_reference('cms_rights', 'send_approval_email_template')[1]
        template_obj = view_id.env['mail.template'].browse(template_id)
        template_obj.email_to = str(view_id.user_id.partner_id.email)
        template_obj.send_mail(view_id.id, force_send=True)


class MainTemplateApproval(models.TransientModel):
    _name = "main.template.approve.wizard"

    @api.multi
    def to_reset(self):
        view_pool = self.env['ir.ui.view']
        view_id = view_pool.browse(self._context.get('active_ids'))[0]
        key = view_id.key.split('__')[0]
        view = view_pool.search([('key', '=', key), ('website_id', '=', view_id.website_id.id), ('is_webpage_template', '=', False)])[0]
        view_id.copy({'state': 'approved', 'key': key, 'name': view.name, 'priority': view.priority})
        view.unlink()
