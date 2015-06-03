#-*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Therp BV (<http://therp.nl>).
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
from openerp.osv import orm


class ResPartner(orm.Model):
    _inherit = 'res.partner'

    def on_change_country_id(
            self, cr, uid, ids, country_id, context=None):

        if not country_id:
            return {} 
        country = self.pool['res.country'].browse(cr, uid,
                                                  country_id, context=context)
        fis_pos_id = country.property_account_position.id

        return {'value': {'property_account_position': fis_pos_id}}
