# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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
import re
from openerp import models, fields, api, exceptions, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    def __init__(self, pool, cr):
        super(ResUsers, self).__init__(pool, cr)
        self.SELF_WRITEABLE_FIELDS.append('phone_extension')

    phone_extension = fields.Char('Extension')

    @api.constrains('phone_extension')
    @api.one
    def _check_phone(self):
        if self.phone_extension and not re.match(
                '^[\d+-]*$', self.phone_extension):
            raise exceptions.ValidationError(
                _('Phone numbers can only contain the following characters: '
                  '01234567890+-'))
