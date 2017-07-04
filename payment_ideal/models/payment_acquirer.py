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
import base64
from collections import OrderedDict
from openerp import _, models, fields, api, exceptions, tools
try:
    try:
        import xmlsec
    except SystemError:
        import logging
        logging.error(
            'Unable to load xmlsec, payment_ideal is not going to work'
        )
    from .. import ideal
except ImportError:
    import logging
    logging.error('Unable to load xmlsec, payment_ideal is not going to work')


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    @api.model
    def _get_providers(self):
        return super(PaymentAcquirer, self)._get_providers() + [
            ('ideal', 'iDeal'),
        ]

    ideal_merchant_id = fields.Char(
        'Merchant ID', required_if_provider='ideal')
    ideal_merchant_sub_id = fields.Char(
        'Merchant Sub ID', required_if_provider='ideal', default='0')
    ideal_merchant_certificate = fields.Binary(
        'Your certificate', required_if_provider='ideal')
    ideal_merchant_privkey = fields.Binary(
        'Your private key', required_if_provider='ideal')
    ideal_merchant_privkey_passphrase = fields.Char(
        'Your private key\'s passphrase',
        help='Fill this in if your private key is encrypted')
    ideal_acquirer_endpoint = fields.Char(
        'Acquirer endpoint', required_if_provider='ideal')
    ideal_acquirer_certificate = fields.Binary(
        'Acquirer certificate', required_if_provider='ideal')

    @api.multi
    def ideal_get_form_action_url(self):
        return '/payment/ideal/redirect'

    @api.constrains(
        'ideal_merchant_privkey', 'ideal_merchant_privkey_passphrase')
    def _constrain_ideal_merchant_privkey(self):
        if not self.ideal_merchant_privkey:
            return
        try:
            self._ideal_merchant_privkey()
        except Exception, e:
            raise exceptions.ValidationError(
                _('Couldn\'t read your private key. Is the passphrase correct?'
                  '\nTechnical error message follows below\n%s') % str(e))

    @api.constrains(
        'ideal_merchant_certificate', 'ideal_merchant_privkey',
        'ideal_merchant_privkey_passphrase')
    def _constrain_ideal_merchant_certificate(self):
        if not self.ideal_merchant_certificate:
            return
        self._constrain_ideal_merchant_privkey()
        try:
            certificate = self._ideal_merchant_certificate()
            if not certificate:
                raise exceptions.ValidationError(
                    _('Your certificate didn\'t load'))
        except Exception as e:
            if isinstance(e, exceptions.ValidationError):
                raise e
            raise exceptions.ValidationError(
                _('Couldn\'t read your certificate\n'
                  'Technical error message follows below\n%s') % str(e))

    @api.constrains(
        'ideal_merchant_certificate', 'ideal_merchant_privkey',
        'ideal_merchant_privkey_passphrase', 'ideal_acquirer_endpoint',
        'ideal_acquirer_certificate')
    def _constrain_ideal_acquirer_endpoint(self):
        if not self.ideal_acquirer_endpoint:
            return
        try:
            connection = self._ideal_connection()
            connection.get_issuer_list()
        except Exception as e:
            raise exceptions.ValidationError(
                _('Couldn\'t connect to %s\n'
                  'Technical error message follows below\n%s') % (
                      self.ideal_acquirer_endpoint,
                      str(e))
            )

    @api.one
    @api.onchange('provider')
    def _onchange_provider(self):
        if self.provider == 'ideal':
            self.view_template_id = self.env.ref(
                'payment_ideal.ideal_payment_button')

    @api.multi
    def _ideal_merchant_privkey(self):
        self.ensure_one()
        return xmlsec.Key.from_memory(
            base64.b64decode(self.ideal_merchant_privkey),
            xmlsec.KeyFormat.PEM,
            password=self.ideal_merchant_privkey_passphrase)

    @api.multi
    def _ideal_merchant_certificate(self):
        self.ensure_one()
        return xmlsec.Key.from_memory(
            base64.b64decode(self.ideal_merchant_certificate),
            xmlsec.KeyFormat.CERT_PEM)

    @api.multi
    def _ideal_connection(self):
        self.ensure_one()
        if self.env.context.get('bin_size'):
            self = self.with_context(bin_size=False)
        return ideal.IDEALConnector(
            merchant=ideal.Merchant(
                self.ideal_merchant_id, self.ideal_merchant_sub_id,
                ideal.Cert(base64.b64decode(self.ideal_merchant_certificate)),
                ideal.Pem(base64.b64decode(self.ideal_merchant_privkey),
                          self.ideal_merchant_privkey_passphrase),
            ),
            acquirer=ideal.Acquirer(
                self.ideal_acquirer_endpoint,
                ideal.Cert(base64.b64decode(self.ideal_acquirer_certificate))
            ))

    @api.multi
    @tools.ormcache()
    def _ideal_issuer_list(self, endpoint):
        self.ensure_one()
        return self._ideal_connection().get_issuer_list()

    @api.multi
    def _ideal_issuer_countries(self):
        self.ensure_one()
        result = OrderedDict()
        for issuer in self._ideal_issuer_list(self.ideal_acquirer_endpoint):
            country = result.setdefault(issuer.list_type, [])
            country.append(issuer)
        return result
