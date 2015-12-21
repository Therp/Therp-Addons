# -*- coding: utf-8 -*-
# © 2014-2015 Therp BV (http://therp.nl).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Branding Company',
    'version': '8.0.1.0.1',
    'author': 'Therp BV',
    'website': 'http://therp.nl',
    'category': 'Sale',
    'depends': [
        'sale_stock',
    ],
    'data': [
        'view/branding_company.xml',
        'view/res_users.xml',
        'view/res_partner.xml',
        'view/sale_order.xml',
        'view/account_invoice.xml',
        'security/ir.model.access.csv',
    ],
}
