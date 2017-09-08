# -*- coding: utf-8 -*-
{
    'name': 'CMS Rights',
    'category': 'Website',
    'summary': 'Extending and implementing an advanced user rights for Website access',
    'author': 'Aktiv Software',
    'website': 'www.aktivsoftware.com',
    'version': '1.0',
    'description': """
Proposal & Approval of website changes
========================================
This Application system allows you to describe the rights of specific roles(Webshop-Manager,Marketing-Manager)
in Odoo Website Builder app
    """,
    'depends': ['website', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/cms_rights_security.xml',
        'data/mail_template_data.xml',
        'views/website_templates.xml',
        'views/ir_ui_view_views.xml',
        'views/snippets.xml',
        'views/website_seo_redirection_view.xml',
        'wizard/template_approve_wizard.xml'
    ],
    'demo': [],
    'qweb': [
        'static/src/xml/editor.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
