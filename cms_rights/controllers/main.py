# -*- coding: utf-8 -*-
import re
import unicodedata
import openerp.http as http
from openerp.tools import ustr
from openerp.http import request
import logging
_logger = logging.getLogger(__name__)

class CMSRights(http.Controller):

    #list all saved page templates
    @http.route('/template/pages', website=True, type='json', auth="user")
    def website_template_pages_load(self, **kw):

        values = {}
        for field_name, field_value in kw.items():
            values[field_name] = field_value
        wms = [user.id for user in request.env['res.groups'].search([('name', '=', 'Webshop-Manager')]).users]

        #WMs can preview all saved page templates
        if request.env.user.id in wms:
            page_templates = request.env['ir.ui.view'].search([('is_webpage_template', '=', True)])
        #MMs can preview all saved page templates

        html_string = ""
        for page_template in page_templates:
            html_string += "<div class=\"page_template\">\n"
            html_string += "    <div class=\"page_template_preview_link\"><a href=\"/template/pages/preview/" + str(page_template.id) + "\" target=\"_blank\">Preview</a></div>\n"
            html_string += "    <div class=\"page_template_title\">" + page_template.name + "</div>\n"
            html_string += "    <div class=\"page_template_glass_overlay\" data-template=\"" + str(page_template.id) + "\"/>\n"
            html_string += "    <div class=\"iframe_wrap\"><iframe src=\"/template/pages/preview/" + str(page_template.id) + "\" class=\"webpage_preview\"/></div>\n"
            html_string += "    <br/>\n"
            html_string += "</div>\n"

        return {'html_string': html_string}

    #to preview saved page layouts before using it at new page creation
    @http.route('/template/pages/preview/<template_id>', website=True, type='http', auth="user")
    def website_template_pages_preview(self, template_id, **kw):
        template = request.env['ir.ui.view'].browse(int(template_id))
        if template.is_webpage_template:
            return http.request.render(template.id, {})

    #to preview MM's proposal before approval
    @http.route('/preview/<view_id>', website=True, type='http', auth="user")
    def propose_preview(self, view_id, **kw):
        view = request.env['ir.ui.view'].browse(int(view_id))
        return http.request.render(view.id, {})

    #to save page template for later use
    @http.route('/template/pages/save', website=True, type='json', auth="user")
    def website_template_pages_save(self, **kw):

        values = {}
        for field_name, field_value in kw.items():
            values[field_name] = field_value

        view_id = values['view_id']
        current_view = request.env['ir.ui.view'].browse(int(view_id))
        for inhe_id in current_view.inherit_children_ids:
            if inhe_id.name == current_view.name:
                current_view = inhe_id

        # Duplicate the current view
        new_view = current_view.copy({'user_id': request.env.user.id})

        # We need to modify the new page to classify it as a template
        new_view.is_webpage_template = True
        new_view.key = ''

        return {'code': 'good'}

    #create new page by using previous saved page templates
    @http.route('/template/pages/new', website=True, type='json', auth="user")
    def website_template_pages_new(self, **kw):
        values = {}
        for field_name, field_value in kw.items():
            values[field_name] = field_value

        if values['template_id']:
            page_template = request.env['ir.ui.view'].browse(int(values['template_id']))
        string = ustr(values['page_name'])
        unicode = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
        slug = re.sub('[\W_]', ' ', unicode).strip().lower()
        slug = re.sub('[-\s]+', '-', slug)
        page_name = slug
        template_module = "website"
        page_xmlid = "%s.%s" % (template_module, page_name)
        website_id = request.env.context.get('website_id')
        key = template_module + '.' + page_name

        # Create a new view with the content of the page template
        page = request.env['ir.ui.view'].create({'website_id': website_id,
                                                'key': key,
                                                'arch': page_template.arch.replace('website_template_pages.placeholder', page_xmlid),
                                                'name': page_name,
                                                'page': True,
                                                'type': 'qweb',
                                                'xml_id': page_xmlid,
                                                'state': 'new',
                                                'user_id': request.env.user.id})
        if page:
            email_to = ''
            wms = []
            for user in request.env['res.groups'].search([('name', '=', 'Webshop-Manager')]).users:
                if user.partner_id.email:
                    email_to += str(user.partner_id.email) + ','
                wms.append(user.id)

            if request.env.user.id not in wms:
                template_id = request.env['ir.model.data'].get_object_reference('cms_rights', 'send_page_request')[1]
                template_obj = request.env['mail.template'].browse(template_id)
                template_obj.email_to = email_to
                template_obj.send_mail(page.id, force_send=True)

        return {'page_name': page_name}
