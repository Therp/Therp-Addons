# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>)
#    All Rights Reserved
#
#    Code snippets from openobject-server 6.1
#                          (C) 2004-2012 OpenERP S.A. (<http://openerp.com>)
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
import logging
from lxml import etree
from openerp.osv.orm import Model
from openerp import tools

overrides_view = []

_logger = logging.getLogger(__name__)

class ir_ui_view(Model):
    _inherit = 'ir.ui.view'

    #copy of the original
    def _check_xml(self, cr, uid, ids, context=None):
        for view in self.browse(cr, uid, ids, context):
            eview = etree.fromstring(view.arch.encode('utf8'))
            frng = tools.file_open(os.path.join('base','rng','view.rng'))
            try:
                relaxng_doc = etree.parse(frng)
                #local change
                for override in overrides_view:
                    _logger.debug('loading override %s' % override)
                    transformation = etree.XSLT(
                            etree.parse(tools.file_open(override)))
                    relaxng_doc = transformation(relaxng_doc)
                #_logger.debug(relaxng_doc)
                #/local change
                relaxng = etree.RelaxNG(relaxng_doc)
                if not relaxng.validate(eview):
                    for error in relaxng.error_log:
                        _logger.error(tools.ustr(error))
                    return False
            finally:
                frng.close()
        return True

    _constraints = [
            #pick up right reference for the constraint
            (_check_xml, 'Invalid XML for View Architecture!', ['arch'])
            ]
