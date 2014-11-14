# -*- coding: utf-8 -*-
from openerp.report import report_sxw
from openerp.addons.account.report import account_print_invoice

report_sxw.report_sxw(
    'report.account.invoice.nobackground',
    'account.invoice',
    'sale_invoice_customs/report/account_print_invoice_nobackground.rml',
    parser=account_print_invoice
)
