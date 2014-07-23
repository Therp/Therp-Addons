# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    This module copyright (c) 2012 Therp BV <http://therp.nl>
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

from osv import fields, osv

class res_company(osv.osv):
    """ 
    Add a boolean field to control auto-emailing of sale orders
    upon confirmation through the EDI interface.
    """
    _inherit = 'res.company'
    _columns = {
        'enable_edi_sale': fields.boolean(
            'Enable EDI sale order email',
            help="When enabled, the system will send out notification emails to "
            "your customer upon sale order confirmation with a link to the online "
            "sale order.",
            ),
        }
