# -*- coding: utf-8 -*-
"""Create branding.company model."""
##############################################################################
#
#    Copyright (C) 2014-2015 Therp BV <http://therp.nl>.
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
from openerp import api, models, fields


class BrandingCompany(models.Model):
    """Create branding.company model."""
    _name = "branding.company"
    _description = """\
        Allows to replace standard company logo, name, address etc. in all
        supporting models and reports.
        """

    @api.model
    def get_partner_branding_company(self, partner_id):
        """Returns recordset with branding company for partner or False."""
        if not partner_id:
            return False
        partner_model = self.env['res.partner']
        partner_obj = partner_model.browse(partner_id)
        return partner_obj and partner_obj.branding_company_id or False

    @api.model
    def get_user_branding_company(self, uid):
        """Returns recordset with branding company for user or False."""
        user_model = self.env['res.users']
        user_objs = user_model.browse(uid)
        return user_objs and user_objs[0].branding_company_id or False

    @api.model
    def get_default_branding_company(self, partner_id, uid):
        """Returns branding company (recordset) for partner or user."""
        return (
            self.get_partner_branding_company(partner_id) or
            self.get_user_branding_company(uid) or
            False
        )

    name = fields.Char()
    logo = fields.Binary()
    rml_footer = fields.Text(
        string='Report Footer',
        help="""Footer text displayed at the bottom of all reports."""
    )
    email = fields.Char(
        string='Email',
        size=64
    )
    website = fields.Char(
        string='Website',
        size=64
    )
