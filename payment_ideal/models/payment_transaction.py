# -*- coding: utf-8 -*-
##############################################################################
#
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
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
from openerp import models, fields, api


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    ideal_entrance_code = fields.Char('Entrance code')
    ideal_issuer_id = fields.Char('Issuer')

    @api.model
    def ideal_create(self, values):
        return {
            'type': 'server2server',
        }

    @api.model
    def _ideal_form_get_tx_from_data(self, data):
        # this needs to be sudo because website_sale expects it
        return self.sudo().search([
            ('ideal_entrance_code', '=', data.get('ec')),
            ('acquirer_reference', '=', data.get('trxid')),
        ])

    @api.model
    def _ideal_form_validate(self, transaction, data):
        if transaction.ideal_entrance_code != data.get('ec') or\
                transaction.acquirer_reference != data.get('trxid'):
            return False
        return self._ideal_s2s_get_tx_status(transaction)

    @api.model
    def _ideal_s2s_get_tx_status(self, transaction):
        if transaction.state in ['pending']:
            connection = transaction.acquirer_id._ideal_connection()
            response = connection.request_transaction_status(
                transaction.acquirer_reference)
            if response.status in ['Expired', 'Cancelled']:
                transaction.write({'state': 'cancel'})
            elif response.status in ['Failure']:
                transaction.write({'state': 'error'})
            elif response.status in ['Success']:
                transaction.write({'state': 'done'})
                return True
        return False
