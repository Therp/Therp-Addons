# Copyright 2014-2018 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class IrActionsTodo(models.Model):
    _inherit = 'ir.actions.todo'

    @api.model
    def configure_language(self):
        if not self.env['res.lang'].search([('code', '=', 'nl_NL')]):
            self.env['base.language.install'].create({
                'lang': 'nl_NL'}).lang_install()
            # Only set all partners to dutch, just after installing language
            self.env['res.partner'].search([]).write({
                'lang': 'nl_NL',
                'tz': 'Europe/Amsterdam'})

    @api.model
    def configure_accounting(self):
        def xmlid(xmlid):
            return self.env.ref(xmlid).id

        if not self.env.user.company_id.chart_template_id:
            account_installer = self.env['wizard.multi.charts.accounts']
            installer = account_installer.create({
                'chart_template_id':
                xmlid('l10n_nl.l10nnl_chart_template'),
                'company_id': xmlid('base.main_company'),
                'currency_id': xmlid('base.EUR'),
                'sale_tax': xmlid('l10n_nl.btw_21'),
                'purchase_tax': xmlid('l10n_nl.btw_21_buy'),
                'code_digits': 5,
            })
            installer.action_next()
