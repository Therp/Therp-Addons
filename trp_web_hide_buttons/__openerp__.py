# -*- encoding: utf-8 -*-
{
    'name': 'Therp hide buttons',
    'application': False,
    'version': '6.1.r069',
    'category': 'Tools',
    'description': '''
This module makes it possible to hide Create and Delete buttons from the
user, if requested through the context of the action defining the window.
To hide both buttons add the following element to the xml for the
ir.actions.act_window:
<field name="context">{'nodelete': '1', 'nocreate': '1'}</field>
''',
    'author': 'Therp B.V.',
    'website': 'http://www.therp.nl',
    'depends': [
        'web_kanban',
    ],
    'init_xml': [],
    'update_xml': [],
    'demo_xml': [],
    'installable': True,
    'js': ['static/src/js/trp_web_hide_buttons.js'],
    }
