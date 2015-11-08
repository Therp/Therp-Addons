# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2012 Therp BV (<http://therp.nl>).
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
import urllib
import urllib2
from openerp import _, api, models, exceptions


class click2call_click2call(models.AbstractModel):
    _name = 'click2call.click2call'
    _description = 'Click2call'

    @api.multi
    def callPBX(self, phone):
        """
        Retrieve all arguments from the database
        and the context, then compose the URL to
        call the Astium PBX with.
        """
        caller_id = 'Via OpenERP'
        if self.env.context.get('partner_id'):
            caller_id = self.env['res.partner'].browse(
                [self.env.context['partner_id']]).name
        user = self.env.user
        if not user.phone_extension:
            raise exceptions.Warning(
                _('Error'),
                _('No extension defined in your user preferences'))
        if not user.company_id or not user.company_id.pbx_shortname:
            raise exceptions.Warning(
                _('Error'),
                _('Could not retrieve the company\'s PBX shortname'))
        if not user.company_id or not user.company_id.pbx_url:
            raise exceptions.Warning(
                _('Error'),
                _('Could not retrieve the company\'s PBX shortname'))
        query_args = {
            'dest': phone,
            'extension': user.phone_extension,
            'shortname': user.company_id.pbx_shortname,
            'CalleridName': caller_id,
        }

        encoded_args = urllib.urlencode(query_args)
        try:
            urllib2.urlopen(user.company_id.pbx_url, encoded_args).read()
        except Exception, e:
            raise exceptions.Warning(_("Error"), e)
        # Todo: raise on problematic responses
        return {'type': 'ir.actions.act_window_close'}
