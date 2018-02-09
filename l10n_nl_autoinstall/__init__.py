# -*- coding: utf-8 -*-
# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, tools, SUPERUSER_ID
from . import models


def post_init_hook(cr, pool):
    if tools.config['test_enable']:
        # in test mode, remove the modules autoinstalled by account's init hook
        auto_modules = ['account_check_printing', 'l10n_generic_coa']
        env = api.Environment(cr, SUPERUSER_ID, {})
        env['ir.module.module'].search([
            ('name', 'in', auto_modules),
        ]).button_uninstall()
