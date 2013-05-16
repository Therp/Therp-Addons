# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>).
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

import os
from lxml import etree
from openerp.osv import orm
from openerp.tools import file_open
from openerp.tools.translate import _
from openerp.modules import get_module_path

class ir_ui_view(orm.Model):
    _inherit = 'ir.ui.view'
    
    def _auto_init(self, cr, context=None):
        """ Check for the necessary intervention in the rng file """
        relaxng_doc = etree.parse(
            file_open(os.path.join(
                    get_module_path('base'),'rng','view.rng')))
        if not relaxng_doc.xpath(
                '//rng:define[@name="separator"]'
                '/rng:element[@name="separator"]'
                '/rng:optional'
                '/rng:attribute[@name="options"]',
                namespaces={'rng': 'http://relaxng.org/ns/structure/1.0'}):
            raise orm.except_orm(
                _("Installation error"),
                _("Please adapt file 'view.rng' to allow the options attribute "
                  "on separator elements"))
        return super(ir_ui_view, self)._auto_init(cr, context=context)
