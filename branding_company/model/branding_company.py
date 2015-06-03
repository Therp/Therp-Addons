# -*- coding: utf-8 -*-
"""Create branding.company model."""
##############################################################################
#
#    Odoo, an open source suite of business applications
#    This module copyright (C) 2014-2015 Therp BV <http://therp.nl>.
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
from openerp import models, fields


class BrandingCompany(models.Model):
    """Create branding.company model."""
    _name = "branding.company"
    _description = """\
        Allows to replace standard company logo, name, address etc. in all
        supporting models and reports.
        """

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

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
