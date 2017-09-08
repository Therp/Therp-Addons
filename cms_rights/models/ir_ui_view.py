# -*- coding: utf-8 -*-
from openerp import models, fields, api, _, http
from lxml import html
import datetime
import re


class WebsitePageTemplate(models.Model):

    _name = "ir.ui.view"
    _inherit = ['ir.ui.view', 'mail.thread']

    state = fields.Selection([('new', 'New Page'), ('draft', 'Draft'), ('proposed', 'Proposed'), ('approved', 'Approved'), ('cancel', 'Cancelled'), ('main', 'Main')], readonly=True)
    image = fields.Binary(string="Image (Obsolete)")
    is_webpage_template = fields.Boolean(string="Webpage Template")
    user_id = fields.Many2one('res.users', string='User')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env['res.company']._company_default_get('ir.ui.view'))

    #preview saved page template
    @api.multi
    def to_preview(self):
        """ Redirect to Controller to Preview Template.
        """
        url = '/preview/%d?priority' % (self.id)
        return {
            'name': _('Preview Proposal'),
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    #action on approve button click
    @api.multi
    def get_approve(self):
        """ Return to Popup Wizard for Confirm Approval.
        """
        return {
                'name': _('Approve'),
                'view_type': 'form',
                "view_mode": 'form',
                'res_model': 'template.approve.wizard',
                'type': 'ir.actions.act_window',
                'target': 'new'
        }

    #re-set last changes of WMs before MMs request
    @api.multi
    def to_reset(self):
        """ Return to Popup Wizard for Reset Main Template.
        """
        return {
                'name': _('Reset'),
                'view_type': 'form',
                "view_mode": 'form',
                'res_model': 'main.template.approve.wizard',
                'type': 'ir.actions.act_window',
                'target': 'new'
        }

    @api.multi
    def to_cancel(self):
        """ Set state cancel on Cancel Button.
        """
        self.write({'state': 'cancel'})

    #reject the proposal of MMs page request
    @api.multi
    def to_reject(self):
        """ Delete/Remove Template on Reject Button Click.
        """
        key = self.key.split('_')[0]
        reject_list = self.search([('type', '=', 'qweb'), ('key', 'like', key)])
        reject_list.unlink()

    #action on "Propose" button click
    @api.multi
    def set_to_proposed(self):
        """ Set Proposed State on propose button click.
        """
        self.write({'state': 'proposed'})

    #find the templates need approval
    def contains_digits(self, new_key, current_key):
        """ Method to compare current key & new key value.
        """
        _digits = re.compile(current_key + '__+\d+_+\d')
        return bool(_digits.search(new_key))

    @api.multi
    def template_to_approve(self, value, xpath=None, force_send=False):
        """ On Propose Button Call this Method from JS.
        This Method is Copy same Template in ir.ui.view and create key with current date time.
        """
        date = datetime.datetime.now().strftime("%Y%m%d")
        time = datetime.datetime.now().strftime("%H%M")

        arch_section = html.fromstring(
            value, parser=html.HTMLParser(encoding='utf-8'))
        if xpath is None:
            # value is an embedded field on its own, not a view section
            self.save_embedded_field(arch_section)
            return

        for el in self.extract_embedded_fields(arch_section):
            self.save_embedded_field(el)

            # transform embedded field back to t-field
            el.getparent().replace(el, self.to_field_ref(el))

        for view in self:
            arch = self.replace_arch_section(view.id, xpath, arch_section)

        #send proposal mail to all webshop managers
        email_to = ''
        for user in self.env['res.groups'].search([('name', '=', 'Webshop-Manager')]).users:
            if user.partner_id.email:
                email_to += str(user.partner_id.email) + ','

        template_id = self.env['ir.model.data'].get_object_reference('cms_rights', 'send_proposal_email_template')[1]
        template_obj = self.env['mail.template'].browse(template_id)
        template_obj.email_to = email_to

        #Search View and write if already exists
        for view_id in self.env['ir.ui.view'].search([('type', '=', 'qweb'), ('user_id', '=', self._uid)]):
            if self.contains_digits(view_id.key, self.key) and view_id.state == 'proposed':
                view_id.write({'key': self.key + '__' + d + '_' + t, 'arch': self._pretty_arch(arch), 'user_id': self._uid, 'priority': 0})
                template_obj.send_mail(self.id, force_send=force_send)
                return

            if view_id.state == 'new':
                view_id.copy({'key': self.key.split('__')[0] + '__' + d + '_' + t, 'arch': self._pretty_arch(arch), 'user_id': self._uid, 'state': 'new', 'priority': 0});
                view_id.write({'user_id': self._uid, 'state': ''})
                return

            if self.contains_digits(view_id.key, self.key.split('__')[0]) and view_id.state == 'draft':
                view_id.write({'key': self.key.split('__')[0] + '__' + d + '_' + t, 'arch': self._pretty_arch(arch), 'user_id': self._uid, 'state': 'proposed', 'name' : self.name.replace('Draft','Proposal'), 'priority': 0})
                template_obj.send_mail(self.id, force_send=force_send)
                return

        #Duplicate the current view if not exists
        new_view = self.copy({'state': 'proposed', 'user_id': self._uid, 'priority': 0})
        if new_view:
            template_obj.send_mail(self.id, force_send=force_send)

        #We need to modify the new page to classify it as a template
        new_view.name = new_view.name + " - Proposal"
        new_view.key = new_view.key + '__' + d + '_' + t
        new_view.arch = self._pretty_arch(arch)

    #create draft template on click of "Save as Draft" button
    @api.multi
    def save_draft_template(self, value, xpath=None):
        """ On Save as Draft Button Call this Method from JS.
        This Method is save template as a draft(Not Published until Proposed) in ir.ui.view and create key with current date time.
        """
        date = datetime.datetime.now().strftime("%Y%m%d")
        time = datetime.datetime.now().strftime("%H%M")
        arch_section = html.fromstring(
            value, parser=html.HTMLParser(encoding='utf-8'))
        if xpath is None:
            # value is an embedded field on its own, not a view section
            self.save_embedded_field(arch_section)
            return

        for el in self.extract_embedded_fields(arch_section):
            self.save_embedded_field(el)

            # transform embedded field back to t-field
            el.getparent().replace(el, self.to_field_ref(el))

        for view in self:
            arch = self.replace_arch_section(view.id, xpath, arch_section)

        for view_id in self.env['ir.ui.view'].search([('type', '=', 'qweb'), ('user_id', '=', self._uid)]):
            if self.contains_digits(view_id.key, self.key.split('__')[0]) and view_id.state == 'draft':
                view_id.write({'key': self.key.split('__')[0] + '__' + d + '_' + t, 'arch': self._pretty_arch(arch), 'user_id': self._uid, 'priority': 0})
                return
        #Duplicate the current view
        new_view = self.copy({'state': 'draft', 'user_id': self._uid, 'priority': 0})
        #We need to modify the new page to classify it as a template
        new_view.name = new_view.name + " - Draft"
        new_view.key = new_view.key + '__' + d + '_' + t
        new_view.arch = self._pretty_arch(arch)

 