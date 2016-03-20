# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, an open source suite of business apps
#    This module copyright (C) 2014-2015 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from datetime import date
from openerp.osv.orm import Model
from openerp import api


class IrActionsTodo(Model):
    _inherit = 'ir.actions.todo'

    @api.model
    def install_dutch_language(self):
        if not self.env['res.lang'].search([('code', '=', 'nl_NL')]):
            self.env['base.language.install'].create({
                'lang': 'nl_NL',
            }).lang_install()

    def configure_accounting(self, cr, uid, context=None):
        ir_model_data = self.pool['ir.model.data']

        def xmlid(xmlid):
            return ir_model_data.xmlid_to_res_id(cr, uid, xmlid)

        installer_todo = self.browse(
            cr, uid,
            xmlid('account.account_configuration_installer_todo'),
            context=context)
        if installer_todo.state == 'open':
            account_installer = self.pool['account.installer']
            year = date.today().year
            installer_id = account_installer.create(
                cr, uid,
                {
                    'charts': 'l10n_nl',
                    'company_id': xmlid('base.main_company'),
                    'date_start': '{}-01-01'.format(year),
                    'date_stop': '{}-12-31'.format(year),
                    'period': 'month',
                },
                context=context)
            account_installer.action_next(
                cr, uid, [installer_id], context=context)

        installer_todo = self.browse(
            cr, uid,
            xmlid('account.action_wizard_multi_chart_todo'),
            context=context)
        if installer_todo.state == 'open':
            account_installer = self.pool['wizard.multi.charts.accounts']
            installer_id = account_installer.create(
                cr, uid,
                {
                    'chart_template_id':
                    xmlid('l10n_nl.l10nnl_chart_template'),
                    'company_id': xmlid('base.main_company'),
                    'currency_id': xmlid('base.EUR'),
                    'sale_tax': xmlid('l10n_nl.btw_21'),
                    'purchase_tax': xmlid('l10n_nl.btw_21_buy'),
                    'code_digits': 5,
                },
                context=context)
            account_installer.action_next(
                cr, uid, [installer_id], context=context)
