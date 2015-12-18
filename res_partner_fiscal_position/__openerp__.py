# -*- encoding: utf-8 -*-
# © 2015 Therp BV (http://therp.nl).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Fiscal position by country',
    'version': '8.0.1.0.1',
    'license': 'AGPL-3',
    'category': 'Accounting',
    'author': 'Therp BV',
    'website': 'http://therp.nl',
    'depends': [
        'account',
    ],
    'data': [
        'views/res_country.xml',
        'wizards/partner_fiscal_position_update.xml',
    ],
    'installable': True,
}
