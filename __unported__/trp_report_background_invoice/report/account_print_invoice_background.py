# -*- coding: utf-8 -*-
from openerp.report import report_sxw
from openerp.addons.account.report import account_print_invoice

report_sxw.report_sxw(
    'report.account.invoice.background',
    'account.invoice',
    'trp_report_background_invoice/report/account_print_invoice_background.rml',
    parser=account_print_invoice.account_invoice
)
