# -*- coding: utf-8 -*-
# © 2015 Therp BV <http://therp.nl>
{
    "name": "Dutch chart of accounts - autoinstall",
    "version": "10.0.1.0.0",
    "author": "Therp BV",
    "category": 'Accounting & Finance',
    'website': 'http://therp.nl',
    'depends': ['l10n_nl'],
    'data': [
        'data/configure_accounting.xml',
    ],
    "license": 'AGPL-3',
    "post_init_hook": 'post_init_hook',
}
