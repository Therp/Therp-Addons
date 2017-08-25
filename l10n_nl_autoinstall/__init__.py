# -*- coding: utf-8 -*-
# © 2014-2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import inspect
from . import models
from openerp import api, tools, SUPERUSER_ID
from openerp.modules.graph import Graph


def post_init_hook(cr, pool):
    if tools.config['test_enable']:
        # in test mode, remove the modules autoinstalled by account's init hook
        auto_modules = [
            'account_plaid', 'account_check_printing', 'l10n_generic_coa',
        ]
        env = api.Environment(cr, SUPERUSER_ID, {})
        env['ir.module.module'].search([
            ('name', 'in', auto_modules),
        ]).write({'state': 'uninstalled'})
        graph = _get_graph()
        for module in auto_modules:
            if module in graph:
                del graph[module]


def _get_graph():
    graph = None
    for frame, filename, lineno, funcname, line, index in inspect.stack():
        # walk up the stack until we've found a graph
        if 'graph' in frame.f_locals and isinstance(
            frame.f_locals['graph'], Graph
        ):
            graph = frame.f_locals['graph']
            break
    return graph
