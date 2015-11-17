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
import uuid
import urllib
import werkzeug
import urlparse
from openerp import http, _


class PaymentIdeal(http.Controller):
    _redirect_url = '/payment/ideal/redirect'
    _return_url = '/payment/ideal/return'

    @http.route(_redirect_url, type='http', auth='none')
    def redirect(self, **kwargs):
        if not http.request.session.get('sale_transaction_id'):
            raise werkzeug.exceptions.NotFound()
        transaction = http.request.env['payment.transaction'].browse(
            http.request.session['sale_transaction_id'])
        if not transaction.acquirer_id.provider == 'ideal':
            raise werkzeug.exceptions.NotFound()
        if not kwargs.get('issuer_id'):
            if 'referer' in http.request.httprequest.headers:
                return werkzeug.utils.redirect(
                    http.request.httprequest.headers['referer'])
            raise werkzeug.exceptions.NotFound()
        if transaction.state in ['done']:
            raise werkzeug.exceptions.NotFound()
        if transaction.acquirer_reference:
            transaction.sudo().message_post(_(
                'Restarting transaction, old values were\n'
                '<dl>'
                '<dt>Issuer:</dt><dd>%s</dd>\n'
                '<dt>Acquirer reference:</dt><dd>%s</dd>\n'
                '<dt>Entrance code:</dt><dd>%s</dd>\n'
                '</dl>') % (
                    transaction.ideal_issuer_id,
                    transaction.acquirer_reference,
                    transaction.ideal_entrance_code
            ))
        ideal_connection = transaction.acquirer_id._ideal_connection()
        entrance_code = uuid.uuid4().hex
        return_url = urlparse.urljoin(
            http.request.env['ir.config_parameter'].sudo().get_param(
                'web.base.url'),
            self._return_url + (
                '?' + urllib.urlencode({'return_url': kwargs['return_url']})
                if kwargs.get('return_url')
                else ''))
        requested_transaction = ideal_connection.request_transaction(
            kwargs['issuer_id'], transaction.reference,
            str(transaction.amount), transaction.reference, entrance_code,
            return_url)
        transaction.sudo().write({
            'acquirer_reference': requested_transaction.transaction_id,
            'ideal_issuer_id': kwargs['issuer_id'],
            'ideal_entrance_code': entrance_code,
            'state': 'pending',
        })
        return werkzeug.utils.redirect(
            requested_transaction.issuer_authentication_url)

    @http.route(_return_url, type='http', auth='none')
    def returnurl(self, **kwargs):
        if http.request.env['payment.transaction'].form_feedback(
                kwargs, 'ideal'):
            return werkzeug.utils.redirect(kwargs.get('return_url', '/'))
        else:
            raise werkzeug.exceptions.NotFound()
