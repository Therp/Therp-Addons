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
from openerp.tools import xml_import, config, misc
from openerp import tools

_logger = logging.getLogger(__name__)

overrides = []

original_convert_xml_import = tools.convert_xml_import

def convert_xml_import(cr, module, xmlfile, idref=None, mode='init',
        noupdate=False, report=None):
    '''
    Copy of openerp.tools.convert_xml_import save for the xml transformation
    part
    '''
    doc = etree.parse(xmlfile)
    #local change
    relaxng = etree.parse(os.path.join(config['root_path'],'import_xml.rng' ))
    for override in overrides:
        _logger.debug('applying override %s' % str(overrides))
        transformation = etree.XSLT(etree.parse(tools.file_open(override)))
        relaxng = transformation(relaxng)
        _logger.debug('succeeded')
    try:
        relaxng = etree.RelaxNG(relaxng)
    #/local change
        relaxng.assert_(doc)
    except Exception:
        _logger.error('The XML file does not fit the required schema !')
        _logger.error(misc.ustr(relaxng.error_log.last_error))
        raise

    if idref is None:
        idref={}
    obj = xml_import(cr, module, idref, mode, report=report, noupdate=noupdate)
    obj.parse(doc.getroot())
    return True

tools.convert_xml_import = convert_xml_import
