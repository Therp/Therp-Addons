# Copyright 2015-2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Dutch chart of accounts - autoinstall",
    "version": "11.0.1.0.0",
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
