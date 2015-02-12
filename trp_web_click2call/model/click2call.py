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

import re
import urllib, urllib2
from openerp.osv import fields, osv
from openerp.tools.translate import _

class res_users(osv.osv):
    _inherit = 'res.users'
    
    def __init__(self, pool, cr):
        super(res_users, self).__init__(pool, cr)
        self.SELF_WRITEABLE_FIELDS.append('phone_extension')

    _columns = {
        'phone_extension': fields.char('Extension', size=12),
        }
    
    def _check_phone(self, cr, uid, ids, context=None):
        users = self.read(
            cr, uid, ids, ['phone_extension'], context=context)
        for user in users:
            if (user['phone_extension'] and not
                re.match('^[\d+-]*$', user['phone_extension'])):
                return False
        return True

    _constraints = [
        (_check_phone,
         _('Phone numbers can only contain the following characters: '
           '01234567890+-'), ['phone_extension']),
        ]


class res_company(osv.osv):
    _inherit = 'res.company'
    _columns = {
        'pbx_shortname': fields.char('PBX shortname', size=12),
        'pbx_url': fields.char('PBX URL', size=256),
        }

class click2call_click2call(osv.osv_memory):
    _name = 'click2call.click2call'
    _description = 'Click2call'

    def callPBX(self, cr, uid, phone, context=None):
        """
        Retrieve all arguments from the database
        and the context, then compose the URL to
        call the Astium PBX with.
        """
        caller_id = 'Via OpenERP'
        if context and context.get('partner_id'):
            caller_id = self.pool.get('res.partner').read(
                cr, uid, context['partner_id'], ['name'], context=context)['name']
        user = self.pool.get('res.users').browse(
            cr, uid, uid, context=context)
        if not user.phone_extension:
            raise osv.except_osv(
                _('Error'),
                _('No extension defined in your user preferences'))
        if not user.company_id or not user.company_id.pbx_shortname:
            raise osv.except_osv(
                _('Error'),
                _('Could not retrieve the company\'s PBX shortname'))
        if not user.company_id or not user.company_id.pbx_url:
            raise osv.except_osv(
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
            response = urllib2.urlopen(user.company_id.pbx_url, encoded_args).read()
        except Exception, e:
            raise osv.except_osv(_("Error"), e)
        # Todo: raise on problematic responses
        return {'type': 'ir.actions.act_window_close'}
