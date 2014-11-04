# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2011 Domsense srl (<http://www.domsense.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from osv import fields, osv


class Country(osv.osv):
    _inherit = 'res.country'
    _columns = {
        #   'fiscal_position_id': fields.many2one(
        #   'account.fiscal.position','Default fiscal position'),
        'property_account_position': fields.property
        ('account.fiscal.position',
            type='many2one',
            relation='account.fiscal.position',
            string="Default Fiscal Position",
            method=True,
            view_load=True,
            help="""The fiscal position will determine
                 taxes and the accounts used for the country,
                 if not set specifically elsewere.""",),
    }
Country()
