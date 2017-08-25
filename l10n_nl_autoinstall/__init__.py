# -*- coding: utf-8 -*-
# © 2014-2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import tools
from . import models


def post_init_hook(cr, pool):
    if tools.config['test_enable']:
        # in test mode, remove the modules autoinstalled by account's init hook
        auto_modules = [
            'account_plaid', 'account_check_printing', 'l10n_generic_coa',
        ]
        self.env['ir.module.module'].search([
            ('name', 'in', auto_modules),
        ]).button_uninstall()
